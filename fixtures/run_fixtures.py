#!/usr/bin/env python3
"""Mode A runner: execute the routing fixtures as a structured-output eval.

`check_fixtures.py` proves the fixtures are internally coherent. It cannot tell
you whether an assistant reading the spec actually routes a session correctly —
that behaviour lives in prose, so a prompt edit or a model change can loosen a
rule with nothing failing.

This runner closes that gap deterministically. Each case is put to a headless
`claude -p` session carrying only the spec, the case's `devices.yaml` and its
candidate records, with every tool and MCP server disabled. The answer comes
back as JSON constrained by a schema built from
`spec/routed-observation.schema.json`, so grading is `==` rather than a judge:
which device won each channel, under which rule and basis, what was merged,
what was preserved, and whether the system abstained.

It does NOT grade the prose — whether `must_disclose` actually reached the user
in readable words is Mode B's job (see README.md). What it does enforce here is
the structural half of that rule: an observation that has to disclose something
must carry a disclosure.

    python3 fixtures/run_fixtures.py                    # all cases, repo spec
    python3 fixtures/run_fixtures.py --case single-device-setup
    python3 fixtures/run_fixtures.py --spec plugin      # the shipped skill
    python3 fixtures/run_fixtures.py --spec both        # catch mirror drift
    python3 fixtures/run_fixtures.py --dry-run          # print the prompt, call nothing
    python3 fixtures/run_fixtures.py --self-test        # prove the grader grades
    python3 fixtures/run_fixtures.py --json report.json # machine-readable

Stdlib only, to match the rest of the repo.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCHEMA = ROOT / "spec" / "routed-observation.schema.json"
FIXTURES = ROOT / "fixtures" / "routing-cases.json"

SPEC_SOURCES = {
    "repo": ROOT / "CLAUDE.md",
    "plugin": ROOT / "plugins" / "metricbraid" / "skills" / "health-data-routing" / "SKILL.md",
}

DEDUPLICATION = ["collapse", "within_source_only", "none"]

# Mirrors the disclosure invariant in check_fixtures.py. Kept in sync by hand
# is exactly the failure this repo dislikes, so import it instead.
sys.path.insert(0, str(ROOT / "fixtures"))
from check_fixtures import SOFT_BASIS, WEAK_CONFIDENCE  # noqa: E402


# --------------------------------------------------------------------------
# The response schema, built from the canonical one so the vocabulary the
# model is allowed to answer in cannot drift from the vocabulary the fixtures
# are written in.
# --------------------------------------------------------------------------

def build_response_schema() -> dict:
    defs = json.loads(SCHEMA.read_text())["$defs"]

    def enum(name: str) -> list:
        return defs[name]["enum"]

    observation = {
        "type": "object",
        "additionalProperties": False,
        "required": ["metric", "channel", "routing_status", "selected_source",
                     "routing", "measurement", "merged_from_devices", "must_disclose"],
        "properties": {
            "metric": {"type": "string",
                       "description": "Exactly one of the metric names you were asked to route."},
            "channel": {"enum": enum("channel")},
            "routing_status": {"enum": enum("routing_status")},
            "selected_source": {
                "type": ["object", "null"],
                "additionalProperties": False,
                "required": ["device", "capability_class", "sensor_class"],
                "description": "null whenever routing_status is not 'routed'.",
                "properties": {
                    "device": {"type": "string",
                               "description": "The device id as declared in devices.yaml."},
                    "capability_class": {"enum": enum("capability_class")},
                    "sensor_class": {"enum": enum("sensor_class")},
                },
            },
            "routing": {
                "type": "object",
                "additionalProperties": False,
                "required": ["rule", "basis", "decided_by"],
                "properties": {
                    "rule": {"enum": enum("rule")},
                    "basis": {"enum": enum("routing_basis")},
                    "decided_by": {"type": "string",
                                   "description": "The specific mechanism that decided it, named."},
                },
            },
            "measurement": {
                "type": "object",
                "additionalProperties": False,
                "required": ["confidence"],
                "properties": {"confidence": {"enum": enum("measurement_confidence")}},
            },
            "merged_from_devices": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Device ids whose competing record of the same event was folded in.",
            },
            "must_disclose": {
                "type": "array",
                "items": {"type": "string"},
                "description": "What has to reach the user in the final answer.",
            },
        },
    }

    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["deduplication", "abstains", "competing_preserved", "observations"],
        "properties": {
            "deduplication": {"enum": DEDUPLICATION},
            "abstains": {"type": "boolean",
                         "description": "True if you decline to give a single number for any metric."},
            "competing_preserved": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Device ids whose disagreeing values you preserved rather than resolved.",
            },
            "observations": {"type": "array", "items": observation},
        },
    }


# --------------------------------------------------------------------------
# Prompt
# --------------------------------------------------------------------------

PROMPT_TEMPLATE = """\
This is a routing exercise against the spec in your context. Everything you
need is below — no tools, no integrations, nothing to look up.

## devices.yaml

```json
{config}
```

## Records the integrations returned

{given}

## Task

Route these metrics: {metrics}.

Return one observation per metric. For each, decide the channel it belongs to,
whether it routes at all, which source governs it, under which rule and on what
basis, how far the measurement itself can be trusted, which competing records
were folded in, and what has to be disclosed to the user.

Then state, for the set as a whole, whether deduplication collapsed anything,
whether you are abstaining from a single number for any metric, and which
devices' disagreeing values you are preserving rather than resolving.

Answer only with the structured object.
"""


def build_prompt(case: dict) -> str:
    metrics = [o["metric"] for o in case["expect"]["observations"]]
    return PROMPT_TEMPLATE.format(
        config=json.dumps(case["config"], indent=2),
        given="\n".join(f"- {line}" for line in case["given"]),
        metrics=", ".join(f"`{m}`" for m in metrics),
    )


# --------------------------------------------------------------------------
# Invocation
# --------------------------------------------------------------------------

def run_claude(prompt: str, spec_file: Path, schema: dict, model: str | None,
               timeout: int) -> tuple[dict | None, str, float]:
    """Return (parsed answer, error message, cost in USD)."""
    cmd = [
        "claude", "-p", prompt,
        "--append-system-prompt-file", str(spec_file),
        "--output-format", "json",
        "--json-schema", json.dumps(schema),
        # Hermetic: the case is the only input. No tools, no MCP servers, no
        # settings, no CLAUDE.md discovered from the cwd, no session on disk.
        "--tools", "",
        "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}',
        "--setting-sources", "",
        "--disable-slash-commands",
        "--no-session-persistence",
    ]
    if model:
        cmd += ["--model", model]

    with tempfile.TemporaryDirectory() as cwd:
        try:
            proc = subprocess.run(cmd, cwd=cwd, capture_output=True,
                                  text=True, timeout=timeout)
        except subprocess.TimeoutExpired:
            return None, f"timed out after {timeout}s", 0.0

    try:
        envelope = json.loads(proc.stdout)
    except json.JSONDecodeError:
        tail = (proc.stderr or proc.stdout or "").strip()[-300:]
        return None, f"claude produced no JSON envelope: {tail}", 0.0

    cost = envelope.get("total_cost_usd") or 0.0
    if envelope.get("is_error"):
        return None, str(envelope.get("result", "unknown error"))[:300], cost

    answer = extract_answer(envelope)
    if answer is None:
        return None, f"no structured object in the reply: {str(envelope.get('result'))[:200]}", cost
    return answer, "", cost


def extract_answer(envelope: dict) -> dict | None:
    """Find the structured object, whichever way this CLI version returns it."""
    for key in ("structured_output", "structuredOutput", "structured_result"):
        if isinstance(envelope.get(key), dict):
            return envelope[key]

    text = envelope.get("result")
    if isinstance(text, dict):
        return text
    if not isinstance(text, str):
        return None
    try:
        parsed = json.loads(text)
        return parsed if isinstance(parsed, dict) else None
    except json.JSONDecodeError:
        pass
    # Last resort: the object embedded in prose or a fenced block.
    start, depth = text.find("{"), 0
    if start < 0:
        return None
    for i in range(start, len(text)):
        depth += (text[i] == "{") - (text[i] == "}")
        if depth == 0:
            try:
                return json.loads(text[start:i + 1])
            except json.JSONDecodeError:
                return None
    return None


# --------------------------------------------------------------------------
# Grading
# --------------------------------------------------------------------------

def assertion(name: str, expected, actual) -> dict:
    return {"assertion": name, "expected": expected, "actual": actual,
            "ok": expected == actual}


def grade(case: dict, answer: dict) -> list[dict]:
    expect = case["expect"]
    results = [
        assertion("deduplication", expect.get("deduplication"), answer.get("deduplication")),
        assertion("abstains", expect["abstains"], answer.get("abstains")),
    ]

    if "competing_preserved" in expect:
        results.append(assertion(
            "competing_preserved",
            sorted(expect["competing_preserved"]),
            sorted(answer.get("competing_preserved") or []),
        ))

    by_metric = {o.get("metric"): o for o in answer.get("observations") or []}
    results.append(assertion(
        "observations reported",
        sorted(o["metric"] for o in expect["observations"]),
        sorted(by_metric),
    ))

    for want in expect["observations"]:
        metric = want["metric"]
        got = by_metric.get(metric)
        if got is None:
            results.append(assertion(f"{metric}: present", True, False))
            continue

        results.append(assertion(f"{metric}: channel", want["channel"], got.get("channel")))
        results.append(assertion(f"{metric}: routing_status",
                                 want["routing_status"], got.get("routing_status")))
        results.append(assertion(f"{metric}: rule",
                                 want["routing"]["rule"], (got.get("routing") or {}).get("rule")))
        results.append(assertion(f"{metric}: basis",
                                 want["routing"]["basis"], (got.get("routing") or {}).get("basis")))
        results.append(assertion(f"{metric}: confidence",
                                 want["measurement"]["confidence"],
                                 (got.get("measurement") or {}).get("confidence")))

        want_src, got_src = want.get("selected_source"), got.get("selected_source")
        results.append(assertion(f"{metric}: selected device",
                                 (want_src or {}).get("device"),
                                 (got_src or {}).get("device")))
        if want_src:
            for field in ("capability_class", "sensor_class"):
                if field in want_src:
                    results.append(assertion(f"{metric}: {field}",
                                             want_src[field], (got_src or {}).get(field)))

        results.append(assertion(f"{metric}: merged_from",
                                 sorted(want.get("merged_from_devices") or []),
                                 sorted(got.get("merged_from_devices") or [])))

        # The structural half of the disclosure rule. Whether the words are any
        # good is Mode B; whether anything was said at all is checkable here.
        basis = (got.get("routing") or {}).get("basis")
        confidence = (got.get("measurement") or {}).get("confidence")
        needs = (basis in SOFT_BASIS
                 or confidence in WEAK_CONFIDENCE
                 or got.get("routing_status") != "routed"
                 or bool(got.get("merged_from_devices")))
        if needs:
            results.append(assertion(f"{metric}: discloses something",
                                     True, bool(got.get("must_disclose"))))

    return results


# --------------------------------------------------------------------------
# Reporting
# --------------------------------------------------------------------------

def report(rows: list[dict], spec_label: str, model: str | None) -> None:
    width = max(len(r["case"]) for r in rows)
    print(f"\nspec: {spec_label}    model: {model or 'session default'}\n")
    print(f"{'case'.ljust(width)}  result   assertions")
    print("-" * (width + 34))

    for row in rows:
        if row["error"]:
            print(f"{row['case'].ljust(width)}  ERROR    {row['error'][:60]}")
            continue
        checks = row["assertions"]
        failed = [c for c in checks if not c["ok"]]
        verdict = "pass" if not failed else "FAIL"
        print(f"{row['case'].ljust(width)}  {verdict:<8} "
              f"{len(checks) - len(failed)}/{len(checks)}")
        for c in failed:
            print(f"{' ' * width}    ✗ {c['assertion']}: "
                  f"expected {c['expected']!r}, got {c['actual']!r}")

    passed = sum(1 for r in rows if not r["error"] and all(c["ok"] for c in r["assertions"]))
    cost = sum(r.get("cost_usd") or 0 for r in rows)
    print(f"\n{passed}/{len(rows)} cases passed"
          + (f"   ${cost:.2f}" if cost else ""))


# --------------------------------------------------------------------------
# Offline verification of the grader itself
# --------------------------------------------------------------------------

def self_test(cases: list[dict]) -> int:
    """Grade each case against its own expectations, then against a mutation.

    Proves the grader is actually wired to the fixtures: the identity pass must
    be clean, and a single flipped field must be caught. No API calls.
    """
    problems = []

    for case in cases:
        expect = case["expect"]
        ideal = {
            "deduplication": expect.get("deduplication"),
            "abstains": expect["abstains"],
            "competing_preserved": expect.get("competing_preserved", []),
            "observations": [
                {
                    "metric": o["metric"],
                    "channel": o["channel"],
                    "routing_status": o["routing_status"],
                    "selected_source": o.get("selected_source"),
                    "routing": o["routing"],
                    "measurement": o["measurement"],
                    "merged_from_devices": o.get("merged_from_devices", []),
                    "must_disclose": o.get("must_disclose", []),
                }
                for o in expect["observations"]
            ],
        }
        failed = [c for c in grade(case, ideal) if not c["ok"]]
        if failed:
            problems.append(f"{case['id']}: own expectations do not grade clean — "
                            + "; ".join(c["assertion"] for c in failed))

        # Flip the one thing every case has: hand the first observation to a
        # device that did not win it.
        mutated = json.loads(json.dumps(ideal))
        first = mutated["observations"][0]
        first["selected_source"] = {"device": "impostor",
                                    "capability_class": "self_reported",
                                    "sensor_class": "unspecified"}
        first["routing_status"] = "routed"
        if all(c["ok"] for c in grade(case, mutated)):
            problems.append(f"{case['id']}: a wrongly-routed answer still passed")

    for p in problems:
        print(f"FAIL     {p}")
    if problems:
        print(f"\n{len(problems)} problem(s) — the grader is not defending "
              f"{len(cases)} fixtures.")
        return 1
    print(f"OK  grader passes all {len(cases)} fixtures on their own expectations "
          f"and rejects a wrongly-routed answer in every one.")
    return 0


# --------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--case", action="append", metavar="ID",
                        help="run only this case (repeatable)")
    parser.add_argument("--spec", choices=["repo", "plugin", "both"], default="repo",
                        help="which copy of the spec to test (default: repo)")
    parser.add_argument("--model", help="pin a model, e.g. opus (default: session default)")
    parser.add_argument("--jobs", type=int, default=4, help="cases in parallel (default: 4)")
    parser.add_argument("--timeout", type=int, default=300, help="seconds per case (default: 300)")
    parser.add_argument("--json", metavar="PATH", help="write the full report here")
    parser.add_argument("--dry-run", action="store_true",
                        help="print the prompt and schema for each case, call nothing")
    parser.add_argument("--self-test", action="store_true",
                        help="verify the grader offline, then exit")
    args = parser.parse_args()

    cases = json.loads(FIXTURES.read_text())["cases"]
    if args.case:
        wanted = set(args.case)
        unknown = wanted - {c["id"] for c in cases}
        if unknown:
            print(f"unknown case(s): {', '.join(sorted(unknown))}", file=sys.stderr)
            return 2
        cases = [c for c in cases if c["id"] in wanted]

    if args.self_test:
        return self_test(cases)

    schema = build_response_schema()

    if args.dry_run:
        for case in cases:
            print(f"{'=' * 72}\n{case['id']}\n{'=' * 72}\n")
            print(build_prompt(case))
        print(f"{'=' * 72}\nresponse schema\n{'=' * 72}\n")
        print(json.dumps(schema, indent=2))
        return 0

    specs = ["repo", "plugin"] if args.spec == "both" else [args.spec]
    exit_code = 0
    full_report = {"model": args.model, "runs": []}

    for spec_name in specs:
        spec_file = SPEC_SOURCES[spec_name]
        if not spec_file.exists():
            print(f"missing spec source: {spec_file}", file=sys.stderr)
            return 2

        def run_one(case: dict) -> dict:
            answer, error, cost = run_claude(build_prompt(case), spec_file,
                                             schema, args.model, args.timeout)
            return {
                "case": case["id"],
                "error": error,
                "cost_usd": cost,
                "answer": answer,
                "assertions": grade(case, answer) if answer else [],
            }

        with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
            rows = list(pool.map(run_one, cases))

        label = f"{spec_name} ({spec_file.relative_to(ROOT)})"
        report(rows, label, args.model)
        full_report["runs"].append({"spec": spec_name, "cases": rows})

        if any(r["error"] or not all(c["ok"] for c in r["assertions"]) for r in rows):
            exit_code = 1

    if args.json:
        Path(args.json).write_text(json.dumps(full_report, indent=2) + "\n")
        print(f"\nreport written to {args.json}")

    return exit_code


if __name__ == "__main__":
    sys.exit(main())

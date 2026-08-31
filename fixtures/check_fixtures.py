#!/usr/bin/env python3
"""Structure check for MetricBraid's routing fixtures and spec examples.

Not a behavioural test — it cannot tell you whether an assistant routed a
session correctly. What it does enforce is that the vocabulary and the
invariants in CLAUDE.md hold across every file that claims to speak it, so the
spec, the rules and the test cases cannot quietly drift apart.

Checks:
  1. Every enum used in a fixture or example exists in the schema's $defs.
  2. routing_status agrees with selected_source and value.
  3. An unresolved observation preserves its competing values, or says that
     no rule applies.
  4. The disclosure rule from CLAUDE.md: anything provisional, preference-
     decided, unresolved, weakly measured, withheld or merged must carry at
     least one must_disclose entry.

Usage:
    python3 fixtures/check_fixtures.py          # check, exit non-zero on failure
    python3 fixtures/check_fixtures.py --list   # also print a summary table
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCHEMA = ROOT / "spec" / "routed-observation.schema.json"
FIXTURES = ROOT / "fixtures" / "routing-cases.json"
EXAMPLES = sorted((ROOT / "spec" / "examples").glob("*.json"))

WEAK_CONFIDENCE = {"low", "unvalidated", "unusable"}
SOFT_BASIS = {"provisional", "user_preference", "unresolved"}

errors: list[str] = []
warnings: list[str] = []


def fail(where: str, msg: str) -> None:
    errors.append(f"{where}: {msg}")


def load_enums() -> dict[str, set[str]]:
    defs = json.loads(SCHEMA.read_text())["$defs"]
    return {name: set(body["enum"]) for name, body in defs.items() if "enum" in body}


def check_observation(where: str, obs: dict, enums: dict[str, set[str]],
                      competing: list | None) -> None:
    """Shared invariants for a routed observation, in either file shape.

    `competing` is the preserved losing values, which live on the observation
    in a spec example and on the case in a fixture.
    """
    status = obs.get("routing_status")
    if status not in enums["routing_status"]:
        fail(where, f"routing_status {status!r} is not in the schema")

    if obs.get("channel") not in enums["channel"]:
        fail(where, f"channel {obs.get('channel')!r} is not in the schema")

    routing = obs.get("routing") or {}
    if routing.get("rule") not in enums["rule"]:
        fail(where, f"routing.rule {routing.get('rule')!r} is not in the schema")
    basis = routing.get("basis")
    if basis not in enums["routing_basis"]:
        fail(where, f"routing.basis {basis!r} is not in the schema")
    if not str(routing.get("decided_by", "")).strip():
        fail(where, "routing.decided_by is empty — the mechanism must be named")

    confidence = (obs.get("measurement") or {}).get("confidence")
    if confidence not in enums["measurement_confidence"]:
        fail(where, f"measurement.confidence {confidence!r} is not in the schema")

    src = obs.get("selected_source")
    if status == "routed" and not src:
        fail(where, "routing_status is 'routed' but no selected_source is named")
    if status in {"unresolved", "withheld"} and src:
        fail(where, f"routing_status is {status!r} but a selected_source is named")
    if src:
        if src.get("capability_class") not in enums["capability_class"]:
            fail(where, f"capability_class {src.get('capability_class')!r} is not in the schema")
        sensor = src.get("sensor_class")
        if sensor is not None and sensor not in enums["sensor_class"]:
            fail(where, f"sensor_class {sensor!r} is not in the schema")
        if not src.get("device"):
            fail(where, "selected_source has no device id")

    if basis == "unresolved" and status not in {"unresolved", "withheld"}:
        fail(where, "routing.basis is 'unresolved' but the observation is reported as routed")

    if status == "unresolved" and not competing:
        # Nothing resolved the routing. Either candidates disagree — in which
        # case both must survive — or no rule applies at all, which has to be
        # said in so many words rather than left as an empty conflict.
        if "no_rule_applies" not in str(routing.get("decided_by", "")):
            fail(where, "unresolved observation preserves no competing values and "
                        "does not say that no rule applies")

    merged = obs.get("merged_from") or obs.get("merged_from_devices") or []
    disclose = obs.get("must_disclose") or []
    needs_disclosure = (
        basis in SOFT_BASIS
        or confidence in WEAK_CONFIDENCE
        or status != "routed"
        or bool(merged)
    )
    if needs_disclosure and not disclose:
        fail(where, "must_disclose is empty, but the observation is provisional, "
                    "preference-decided, unresolved, weakly measured, withheld or merged")


def check_fixtures(enums) -> list[dict]:
    data = json.loads(FIXTURES.read_text())
    cases = data["cases"]
    seen = set()
    for case in cases:
        cid = case.get("id", "<no id>")
        where = f"fixture {cid}"
        for key in ("id", "title", "why_it_matters", "config", "given", "expect"):
            if not case.get(key):
                fail(where, f"missing required key {key!r}")
        if cid in seen:
            fail(where, "duplicate case id")
        seen.add(cid)

        expect = case.get("expect", {})
        if not expect.get("observations"):
            fail(where, "no expected observations")
        if not expect.get("must_not"):
            fail(where, "no must_not list — a fixture has to say what failure looks like")
        if "abstains" not in expect:
            fail(where, "does not state whether the system abstains")

        competing = expect.get("competing_preserved")
        for i, obs in enumerate(expect.get("observations", [])):
            check_observation(f"{where} obs[{i}]", obs, enums, competing)
    return cases


def check_examples(enums) -> None:
    for path in EXAMPLES:
        payload = json.loads(path.read_text())
        observations = payload if isinstance(payload, list) else [payload]
        for i, obs in enumerate(observations):
            where = f"{path.relative_to(ROOT)} [{i}]"
            check_observation(where, obs, enums, obs.get("competing"))
            if obs.get("routing_status") != "routed" and obs.get("value") is not None:
                fail(where, "value is set on an observation that was not routed")
            if obs.get("routing_status") == "routed" and obs.get("value") is None:
                fail(where, "routed observation has no value")
            window = obs.get("window") or {}
            if not window.get("start") or not window.get("end"):
                fail(where, "window is missing start or end")


def summarise(cases) -> None:
    width = max(len(c["id"]) for c in cases)
    print(f"\n{'case'.ljust(width)}  dedup              abstains  expected routing")
    print("-" * (width + 52))
    for case in cases:
        expect = case["expect"]
        bases = ", ".join(sorted({o["routing"]["basis"] for o in expect["observations"]}))
        print(f"{case['id'].ljust(width)}  {expect.get('deduplication', '?'):<18} "
              f"{str(expect['abstains']):<9} {bases}")


def main() -> int:
    enums = load_enums()
    cases = check_fixtures(enums)
    check_examples(enums)

    if "--list" in sys.argv:
        summarise(cases)

    print()
    for w in warnings:
        print(f"warning  {w}")
    if errors:
        for e in errors:
            print(f"FAIL     {e}")
        print(f"\n{len(errors)} problem(s) in {len(cases)} fixtures "
              f"and {len(EXAMPLES)} examples.")
        return 1
    print(f"OK  {len(cases)} fixtures, {len(EXAMPLES)} spec examples, "
          f"vocabulary consistent with {SCHEMA.relative_to(ROOT)}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

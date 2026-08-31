#!/usr/bin/env python3
"""Generate the plugin's copies of the repo's canonical files.

A Claude Code plugin has to be self-contained: the skill reads its own
`references/`, and `/metricbraid-init` copies its own `templates/`. So the
evidence dossiers and the routed-observation contract necessarily exist twice
in this repo.

What is NOT necessary is maintaining both by hand. The repo-root copies are
canonical — they are what the README and CLAUDE.md link to, what contributors
edit, and the only ones whose relative links are correct when browsing the
repo. Everything under plugins/metricbraid/ is generated from them by this
script, with the link rewrites each destination needs declared below.

    python3 scripts/sync_plugin.py            # regenerate
    python3 scripts/sync_plugin.py --check    # fail if out of date (CI)

Stdlib only, to match the rest of the repo.
"""

from __future__ import annotations

import argparse
import filecmp
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLUGIN = ROOT / "plugins" / "metricbraid"
SKILL_REFS = PLUGIN / "skills" / "health-data-routing" / "references"
TEMPLATES = PLUGIN / "templates"
GH = "https://github.com/drleahzou/MetricBraid/blob/main"

# Files that exist in the repo but not in the mirror: the watchlist is repo
# infrastructure (the weekly job reads it), and the seen-state is generated.
EVIDENCE_EXCLUDE = {"watchlist.yaml", ".watch-state.json"}

# Link rewrites, applied per destination. A mirrored file sits at a different
# depth and next to a different set of neighbours, so some of its relative
# links cannot resolve; each one is either repointed inside the plugin or sent
# to the repo on GitHub. Anything not listed here is copied byte-for-byte.
REWRITES: dict[str, list[tuple[str, str]]] = {
    "references/README.md": [
        ("[`CLAUDE.md`](../CLAUDE.md)", "[`CLAUDE.md`](../../../templates/CLAUDE.md)"),
        ("*(see `CLAUDE.md`)*", "*(see the skill's Rule D section)*"),
        ("[watchlist](watchlist.yaml)", f"[watchlist]({GH}/evidence/watchlist.yaml)"),
        ("[watchlist.yaml](watchlist.yaml)", f"[watchlist.yaml]({GH}/evidence/watchlist.yaml)"),
        ("[`.github/workflows/evidence-watch.yml`](../.github/workflows/evidence-watch.yml)",
         f"[`.github/workflows/evidence-watch.yml`]({GH}/.github/workflows/evidence-watch.yml)"),
        ("[`../spec/routed-observation.md`](../spec/routed-observation.md)",
         "[`routed-observation.md`](routed-observation.md)"),
    ],
    "references/rule-a-passive.md": [
        ("[`../spec/routed-observation.md`](../spec/routed-observation.md)",
         "[`routed-observation.md`](routed-observation.md)")],
    "references/rule-b-recorded-workouts.md": [
        ("[`../spec/routed-observation.md`](../spec/routed-observation.md)",
         "[`routed-observation.md`](routed-observation.md)")],
    "references/rule-c-incidental.md": [
        ("[`../spec/routed-observation.md`](../spec/routed-observation.md)",
         "[`routed-observation.md`](routed-observation.md)")],
    "references/devices/TEMPLATE.md": [
        ("[`../../spec/routed-observation.md`](../../spec/routed-observation.md)",
         "[`../routed-observation.md`](../routed-observation.md)")],
    "references/general/hr-sensor-placement.md": [
        ("[`watchlist.yaml`](../watchlist.yaml)", f"[`watchlist.yaml`]({GH}/evidence/watchlist.yaml)"),
        ("[`../../spec/routed-observation.md`](../../spec/routed-observation.md)",
         "[`../routed-observation.md`](../routed-observation.md)")],
    # The contract ships beside the dossiers it grades against; its examples,
    # schema and checker stay in the repo.
    "references/routed-observation.md": [
        ("[`CLAUDE.md`](../CLAUDE.md)", "[`CLAUDE.md`](../../../templates/CLAUDE.md)"),
        ("[`routed-observation.schema.json`](routed-observation.schema.json)",
         f"[`routed-observation.schema.json`]({GH}/spec/routed-observation.schema.json)"),
        ("Worked examples: [`examples/`](examples/).",
         f"Worked examples: [`spec/examples/`]({GH}/spec/examples/)."),
        ("[`examples/recorded-run-channel-split.json`](examples/recorded-run-channel-split.json)",
         f"[`recorded-run-channel-split.json`]({GH}/spec/examples/recorded-run-channel-split.json)"),
        ("[`examples/passive-conflict.json`](examples/passive-conflict.json)",
         f"[`passive-conflict.json`]({GH}/spec/examples/passive-conflict.json)"),
        ("[`examples/withheld-known-defect.json`](examples/withheld-known-defect.json)",
         f"[`withheld-known-defect.json`]({GH}/spec/examples/withheld-known-defect.json)"),
        ("[`fixtures/check_fixtures.py`](../fixtures/check_fixtures.py) validates the",
         f"[`fixtures/check_fixtures.py`]({GH}/fixtures/check_fixtures.py) in the\nMetricBraid repo validates the"),
    ],
    # An installed project has no evidence/ or spec/ directory — those ship
    # inside the plugin, or stay in the repo.
    "templates/CLAUDE.md": [
        ("| **Evidence** | [`evidence/`](evidence/) |",
         f"| **Evidence** | the plugin skill's `references/` ([online]({GH}/evidence/)) |"),
        ("| **Framework** | this file, [`spec/`](spec/) |",
         f"| **Framework** | this file, and the routed-observation contract ([`spec/`]({GH}/spec/)) |"),
        ("Dossiers live in `evidence/`, in two tiers:",
         "Dossiers ship with the plugin skill as\n`references/` (`evidence/` in the repo), in two tiers:"),
        ("""[`spec/routed-observation.md`](spec/routed-observation.md) and
[`spec/routed-observation.schema.json`](spec/routed-observation.schema.json).""",
         f"""the plugin skill's `references/routed-observation.md`
([online]({GH}/spec/routed-observation.md), with the
[JSON Schema]({GH}/spec/routed-observation.schema.json))."""),
        ("absorbed record still visible. See `spec/examples/` for the full JSON, plus a",
         f"absorbed record still visible. See [`spec/examples/`]({GH}/spec/examples/) for the full JSON, plus a"),
    ],
}


def plan() -> list[tuple[Path, Path]]:
    """(source, destination) for every generated file."""
    jobs = [
        (ROOT / "CLAUDE.md", TEMPLATES / "CLAUDE.md"),
        (ROOT / "devices.yaml", TEMPLATES / "devices.yaml"),
        (ROOT / "food-log.example.csv", TEMPLATES / "food-log.example.csv"),
        (ROOT / "spec" / "routed-observation.md", SKILL_REFS / "routed-observation.md"),
    ]
    for src in sorted((ROOT / "evidence").rglob("*")):
        if src.is_dir() or src.name in EVIDENCE_EXCLUDE:
            continue
        jobs.append((src, SKILL_REFS / src.relative_to(ROOT / "evidence")))
    return jobs


def rewrite_key(dest: Path) -> str:
    """REWRITES is keyed on the plugin-relative path with the skill prefix
    dropped, so `references/README.md` rather than the full nesting."""
    return str(dest.relative_to(PLUGIN)).replace("skills/health-data-routing/", "")


def render(src: Path, dest: Path) -> str:
    key = rewrite_key(dest)
    text = src.read_text()
    for old, new in REWRITES.get(key, []):
        if old not in text:
            raise SystemExit(
                f"sync_plugin: rewrite for {key} no longer matches its source.\n"
                f"  looked for: {old[:90]}\n"
                f"  in: {src.relative_to(ROOT)}\n"
                f"The canonical file changed; update REWRITES in this script."
            )
        # Every occurrence: a canonical file can link the same target twice,
        # and rewriting only the first leaves a dangling link in the mirror.
        text = text.replace(old, new)
    return text


def check_mcp() -> list[str]:
    """The two .mcp.json files are formatted differently on purpose, so compare
    what they declare rather than their bytes."""
    a = json.loads((ROOT / ".mcp.json").read_text())
    b = json.loads((PLUGIN / ".mcp.json").read_text())
    return [] if a == b else [".mcp.json and plugins/metricbraid/.mcp.json declare different servers"]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true",
                    help="report drift and exit non-zero instead of writing")
    args = ap.parse_args()

    stale: list[str] = []
    written = 0
    for src, dest in plan():
        rel = dest.relative_to(ROOT)
        if src.suffix in {".json", ".csv", ".yaml"} and rewrite_key(dest) not in REWRITES:
            current = dest.read_bytes() if dest.exists() else None
            new_bytes = src.read_bytes()
        else:
            current = dest.read_text().encode() if dest.exists() else None
            new_bytes = render(src, dest).encode()
        if current == new_bytes:
            continue
        if args.check:
            stale.append(f"out of date: {rel}  (generated from {src.relative_to(ROOT)})")
        else:
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(new_bytes)
            print(f"wrote {rel}")
            written += 1

    # Anything in the mirror with no canonical source is an orphan.
    expected = {d for _, d in plan()}
    for path in sorted(SKILL_REFS.rglob("*")):
        if path.is_file() and path not in expected:
            stale.append(f"orphan (no canonical source): {path.relative_to(ROOT)}")

    stale += check_mcp()

    if args.check:
        if stale:
            print("\n".join(stale))
            print("\nRun: python3 scripts/sync_plugin.py")
            return 1
        print(f"OK  plugin mirror is in sync with {len(plan())} canonical files.")
        return 0

    if stale:
        print("\n".join(stale))
        return 1
    print(f"OK  {written} file(s) written; {len(plan())} generated files in sync.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

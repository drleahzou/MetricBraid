#!/usr/bin/env python3
"""Evidence watch — check the watchlist for new material, and report it.

Reads `evidence/watchlist.yaml`, checks each source that declares a way to be
checked automatically, and reports anything not seen before.

    python3 scripts/evidence_watch.py --dry-run   # print findings, touch nothing
    python3 scripts/evidence_watch.py             # update state, write issue body

**A flag is never an automatic rule change.** This tool opens an issue for a
human to triage. It never edits a rule, a dossier, or the changelog. That
separation is deliberate: see "How a rule changes" in evidence/README.md.

State lives in `evidence/.watch-state.json` so a hit is reported once, not
every week. Delete an id from that file to have it resurface.
"""

import argparse
import json
import re
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
WATCHLIST = ROOT / "evidence" / "watchlist.yaml"
STATE = ROOT / "evidence" / ".watch-state.json"
ISSUE_BODY = ROOT / ".evidence-watch-issue.md"

PUBMED = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_SUMMARY = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
UA = "MetricBraid-evidence-watch/1.0 (+https://github.com/drleahzou/MetricBraid)"
TIMEOUT = 30
MAX_PER_SOURCE = 10


def get(url, params=None):
    if params:
        url = f"{url}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return r.read()


def check_pubmed(source):
    """Newest PMIDs matching the query, with titles."""
    raw = get(PUBMED, {"db": "pubmed", "term": source["query"],
                       "retmax": MAX_PER_SOURCE, "retmode": "json", "sort": "date"})
    ids = json.loads(raw)["esearchresult"].get("idlist", [])
    if not ids:
        return []
    raw = get(PUBMED_SUMMARY, {"db": "pubmed", "id": ",".join(ids), "retmode": "json"})
    result = json.loads(raw).get("result", {})
    out = []
    for pmid in ids:
        rec = result.get(pmid, {})
        out.append({
            "id": f"pmid:{pmid}",
            "title": rec.get("title", "(title unavailable)"),
            "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
            "date": rec.get("pubdate", ""),
        })
    return out


def check_feed(source):
    """Newest entries from an RSS or Atom feed, filtered by `match` keywords."""
    raw = get(source["feed"])
    root = ET.fromstring(raw)
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    items = root.findall(".//item") or root.findall(".//atom:entry", ns)

    def text(el, *names):
        for n in names:
            found = el.find(n) if not n.startswith("atom:") else el.find(n, ns)
            if found is not None:
                return (found.text or "").strip() or (found.get("href") or "").strip()
        return ""

    keywords = [k.lower() for k in source.get("match", [])]
    out = []
    for el in items[:40]:
        title = text(el, "title", "atom:title")
        link = text(el, "link", "atom:link") or ""
        if not link:
            le = el.find("atom:link", ns)
            link = le.get("href", "") if le is not None else ""
        uid = text(el, "guid", "atom:id") or link or title
        # Only surface entries whose title matches a watched keyword. Feeds
        # cover far more than device accuracy; without this every post fires.
        if keywords and not any(k in title.lower() for k in keywords):
            continue
        out.append({"id": uid, "title": title, "url": link,
                    "date": text(el, "pubDate", "atom:published")})
        if len(out) >= MAX_PER_SOURCE:
            break
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true",
                    help="report findings without writing state or an issue body")
    args = ap.parse_args()

    wl = yaml.safe_load(WATCHLIST.read_text())
    state = json.loads(STATE.read_text()) if STATE.exists() else {"seen": {}}
    seen = state.setdefault("seen", {})

    findings, errors, skipped = [], [], []

    for source in wl.get("sources", []):
        name = source.get("name", "(unnamed)")
        try:
            if source.get("type") == "pubmed_query":
                hits = check_pubmed(source)
            elif source.get("feed"):
                hits = check_feed(source)
            else:
                skipped.append(name)
                continue
        except Exception as e:  # a flaky feed must not fail the whole run
            errors.append(f"{name}: {type(e).__name__}: {e}")
            continue

        known = set(seen.get(name, []))
        new = [h for h in hits if h["id"] not in known]
        if new:
            findings.append((name, source.get("why", ""), new))
        # Record everything seen this run, new or not.
        seen[name] = sorted(known | {h["id"] for h in hits})

    # ---- report ----
    if errors:
        print("Errors (source skipped, not failed):", file=sys.stderr)
        for e in errors:
            print("  " + e, file=sys.stderr)
    if skipped:
        print(f"Not automatable, left to manual review: {', '.join(skipped)}",
              file=sys.stderr)

    if not findings:
        print("No new material.")
        if not args.dry_run:
            STATE.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n")
        return 0

    total = sum(len(n) for _, _, n in findings)
    lines = [
        f"Automated evidence watch found **{total} new item(s)** across "
        f"{len(findings)} source(s).",
        "",
        "> **A flag is never an automatic rule change.** Triage each item, then",
        "> either record it in `evidence/CHANGELOG.md` as reviewed-no-change, or",
        "> propose a rule edit. Both outcomes get logged — a quiet rule change is",
        "> indistinguishable from a bug.",
        "",
    ]
    for name, why, new in findings:
        lines.append(f"### {name}")
        if why:
            lines.append(f"*Watched because: {why}*")
        lines.append("")
        for h in new:
            date = f" — {h['date']}" if h.get("date") else ""
            lines.append(f"- [ ] [{h['title']}]({h['url']}){date}")
        lines.append("")
    lines += [
        "---",
        "",
        "**Triage checklist**",
        "",
        "- [ ] Does it meet the source-quality bar? (peer-reviewed vs a clinical",
        "      reference > independent tester with published methodology > never",
        "      vendor marketing or press coverage)",
        "- [ ] Read against the **primary source** — never an abstract, summary,",
        "      or press write-up alone.",
        "- [ ] Is it device-specific (`evidence/devices/`) or does it generalize",
        "      (`evidence/general/`)? Do not file a single-device finding as general.",
        "- [ ] Record the outcome in `evidence/CHANGELOG.md`, **including if the",
        "      conclusion is \"no change\"**.",
        "",
        f"<sub>Generated {datetime.now(timezone.utc):%Y-%m-%d} by "
        "`scripts/evidence_watch.py`.</sub>",
    ]
    body = "\n".join(lines)

    if args.dry_run:
        print(body)
    else:
        ISSUE_BODY.write_text(body)
        STATE.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n")
        print(f"Wrote {ISSUE_BODY} ({total} new items)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

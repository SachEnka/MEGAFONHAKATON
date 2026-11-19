#!/usr/bin/env python3
"""Show which outputs/decisions reference a claim id or evidence source."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description="Claim/source impact across project artifacts")
    parser.add_argument("project_id")
    parser.add_argument("query", help="Claim id (C001) or substring of source path/text")
    args = parser.parse_args()

    pdir = ROOT / "projects" / args.project_id
    if not pdir.exists():
        print(f"Project not found: {pdir}", file=sys.stderr)
        return 1

    q = args.query.strip()
    print(f"Impact search: project={args.project_id} query={q!r}\n")

    claims_path = pdir / "state" / "claims.jsonl"
    matched_claims = []
    if claims_path.exists():
        for ln in claims_path.read_text(encoding="utf-8").splitlines():
            if not ln.strip():
                continue
            obj = json.loads(ln)
            blob = json.dumps(obj, ensure_ascii=False)
            if q.lower() in blob.lower() or q == obj.get("id"):
                matched_claims.append(obj)
                print(f"CLAIM {obj.get('id')} [{obj.get('type')}] {obj.get('text')}")
                print(f"  source: {obj.get('source')}\n")

    patterns = [re.escape(q)]
    for c in matched_claims:
        if c.get("id"):
            patterns.append(re.escape(str(c["id"])))
    rx = re.compile("|".join(patterns), re.I)

    scan_dirs = [pdir / "outputs", pdir / "state", pdir / "evidence"]
    hits = []
    for d in scan_dirs:
        if not d.exists():
            continue
        for f in d.rglob("*"):
            if not f.is_file() or f.suffix.lower() not in {".md", ".html", ".jsonl", ".json"}:
                continue
            if f.name == "claims.jsonl":
                continue
            try:
                text = f.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            if rx.search(text):
                rel = f.relative_to(pdir)
                hits.append(str(rel))
                print(f"HIT {rel}")

    if not matched_claims and not hits:
        print("No matches.")
        return 1
    print(f"\nTotal file hits: {len(hits)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

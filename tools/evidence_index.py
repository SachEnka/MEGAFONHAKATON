#!/usr/bin/env python3
"""Build an evidence index markdown from evidence/*.md and claims.jsonl."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def extract_meta(text: str) -> dict[str, str]:
    meta = {}
    for key in ("Source", "Accessed", "Type"):
        m = re.search(rf"[-*]\s*{key}:\s*(.+)", text, re.I)
        if m:
            meta[key.lower()] = m.group(1).strip()
    title = text.splitlines()[0].lstrip("# ").strip() if text.strip() else ""
    meta["title"] = title
    return meta


def main() -> int:
    parser = argparse.ArgumentParser(description="Index evidence and claims")
    parser.add_argument("project_id")
    parser.add_argument(
        "--write",
        action="store_true",
        help="Write projects/<id>/evidence/INDEX.md (default: print only)",
    )
    args = parser.parse_args()

    pdir = ROOT / "projects" / args.project_id
    evid_dir = pdir / "evidence"
    if not evid_dir.exists():
        print(f"No evidence dir: {evid_dir}", file=sys.stderr)
        return 1

    lines = [f"# Evidence index — {args.project_id}", ""]
    lines.append("## Files")
    lines.append("| File | Title | Source | Type | Accessed |")
    lines.append("|------|-------|--------|------|----------|")

    for path in sorted(evid_dir.glob("*.md")):
        if path.name.upper() == "INDEX.MD":
            continue
        meta = extract_meta(path.read_text(encoding="utf-8"))
        lines.append(
            f"| `{path.name}` | {meta.get('title','')} | {meta.get('source','')} | "
            f"{meta.get('type','')} | {meta.get('accessed','')} |"
        )

    claims_path = pdir / "state" / "claims.jsonl"
    lines.append("")
    lines.append("## Claims")
    if claims_path.exists():
        lines.append("| ID | Type | Text | Source |")
        lines.append("|----|------|------|--------|")
        for ln in claims_path.read_text(encoding="utf-8").splitlines():
            if not ln.strip():
                continue
            try:
                obj = json.loads(ln)
            except json.JSONDecodeError:
                continue
            text = str(obj.get("text", "")).replace("|", "\\|")
            if len(text) > 120:
                text = text[:117] + "..."
            lines.append(
                f"| {obj.get('id','')} | {obj.get('type','')} | {text} | {obj.get('source','')} |"
            )
    else:
        lines.append("_No claims.jsonl_")

    out = "\n".join(lines) + "\n"
    if args.write:
        (evid_dir / "INDEX.md").write_text(out, encoding="utf-8")
        print(f"Wrote {evid_dir / 'INDEX.md'}")
    else:
        print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

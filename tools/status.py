#!/usr/bin/env python3
"""Show strategist project status from state/CURRENT.md and key artifacts."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PHASE_ARTIFACTS = {
    "gather": ["evidence"],
    "research": ["outputs/situation.md"],
    "options": ["outputs/options.md"],
    "strategy": [
        "outputs/product_strategy.md",
        "outputs/communication_strategy.md",
        "outputs/validation_plan.md",
    ],
    "after": ["state/decisions.md"],
}


def project_dir(project_id: str) -> Path:
    return ROOT / "projects" / project_id


def read_current(pdir: Path) -> str:
    path = pdir / "state" / "CURRENT.md"
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def extract_field(text: str, header: str) -> str:
    pattern = rf"##\s+{re.escape(header)}\s*\n(.*?)(?=\n##\s+|\Z)"
    m = re.search(pattern, text, re.S | re.I)
    return (m.group(1).strip() if m else "").strip()


def main() -> int:
    parser = argparse.ArgumentParser(description="Strategist project status")
    parser.add_argument("project_id", help="e.g. demo-megakino")
    args = parser.parse_args()

    pdir = project_dir(args.project_id)
    if not pdir.exists():
        print(f"Project not found: {pdir}", file=sys.stderr)
        return 1

    current = read_current(pdir)
    if not current:
        print(f"No state/CURRENT.md — run intake for `{args.project_id}`.")
        return 0

    phase = extract_field(current, "Phase") or "(unknown)"
    nxt = extract_field(current, "Next action") or "(none)"
    gate = extract_field(current, "Human gate") or "(n/a)"

    print(f"Project: {args.project_id}")
    print(f"Path:    {pdir}")
    print(f"Phase:   {phase}")
    print(f"Next:    {nxt}")
    print("Human gate:")
    print(gate if gate else "  (empty)")
    print()
    print("Artifacts:")
    checks = [
        ("brief.md", pdir / "brief.md"),
        ("state/CURRENT.md", pdir / "state" / "CURRENT.md"),
        ("state/ledger.md", pdir / "state" / "ledger.md"),
        ("state/claims.jsonl", pdir / "state" / "claims.jsonl"),
        ("state/decisions.md", pdir / "state" / "decisions.md"),
        ("outputs/situation.md", pdir / "outputs" / "situation.md"),
        ("outputs/options.md", pdir / "outputs" / "options.md"),
        ("outputs/product_strategy.md", pdir / "outputs" / "product_strategy.md"),
        ("outputs/communication_strategy.md", pdir / "outputs" / "communication_strategy.md"),
        ("outputs/validation_plan.md", pdir / "outputs" / "validation_plan.md"),
    ]
    evidence_dir = pdir / "evidence"
    ev_count = len(list(evidence_dir.glob("*.md"))) if evidence_dir.exists() else 0
    print(f"  [{'x' if ev_count else ' '}] evidence/*.md ({ev_count} files)")
    for label, path in checks:
        mark = "x" if path.exists() and path.stat().st_size > 0 else " "
        print(f"  [{mark}] {label}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

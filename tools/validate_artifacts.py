#!/usr/bin/env python3
"""Validate mandatory strategist artifacts for a project."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def fail(msg: str, errors: list[str]) -> None:
    errors.append(msg)


def check_nonempty(path: Path, errors: list[str], label: str | None = None) -> bool:
    name = label or str(path)
    if not path.exists():
        fail(f"Missing: {name}", errors)
        return False
    if path.stat().st_size == 0:
        fail(f"Empty: {name}", errors)
        return False
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate strategist project artifacts")
    parser.add_argument("project_id")
    parser.add_argument(
        "--strict-strategy",
        action="store_true",
        help="Require full strategy pack (default: require if options chosen / files present)",
    )
    args = parser.parse_args()

    pdir = ROOT / "projects" / args.project_id
    errors: list[str] = []
    warnings: list[str] = []

    if not pdir.exists():
        print(f"Project not found: {pdir}", file=sys.stderr)
        return 2

    check_nonempty(pdir / "brief.md", errors)
    check_nonempty(pdir / "state" / "CURRENT.md", errors)
    check_nonempty(pdir / "state" / "ledger.md", errors)

    claims = pdir / "state" / "claims.jsonl"
    if check_nonempty(claims, errors):
        lines = [ln for ln in claims.read_text(encoding="utf-8").splitlines() if ln.strip()]
        if len(lines) < 3:
            warnings.append("claims.jsonl has fewer than 3 claims")

    evidence = list((pdir / "evidence").glob("*.md")) if (pdir / "evidence").exists() else []
    if len(evidence) < 1:
        fail("No evidence/*.md files", errors)

    situation = pdir / "outputs" / "situation.md"
    if check_nonempty(situation, errors):
        text = situation.read_text(encoding="utf-8").lower()
        for needle in ("пробел", "gap", "не знаем"):
            if needle in text:
                break
        else:
            warnings.append("situation.md may lack an explicit gaps section")

    options = pdir / "outputs" / "options.md"
    if check_nonempty(options, errors):
        text = options.read_text(encoding="utf-8")
        # Expect at least 3 variant headings
        variants = re.findall(r"^##\s+Вариант", text, re.M)
        if len(variants) < 3:
            fail("options.md must contain at least 3 '## Вариант' sections", errors)
        low = text.lower()
        if "оставить" not in low and "status quo" not in low:
            warnings.append("options.md: status quo wording not detected")
        if "закрыть" not in low and "сузить" not in low and "kill" not in low:
            warnings.append("options.md: kill/narrow wording not detected")

    strategy_files = [
        pdir / "outputs" / "product_strategy.md",
        pdir / "outputs" / "communication_strategy.md",
        pdir / "outputs" / "validation_plan.md",
    ]
    present = sum(1 for p in strategy_files if p.exists() and p.stat().st_size > 0)
    current = (pdir / "state" / "CURRENT.md").read_text(encoding="utf-8").lower()
    needs_strategy = args.strict_strategy or present > 0 or "strategy" in current or "done" in current or "after" in current

    if needs_strategy:
        for p in strategy_files:
            check_nonempty(p, errors)
        prod = strategy_files[0]
        comm = strategy_files[1]
        if prod.exists() and comm.exists():
            # Soft coherence: communication should mention product alignment
            ctext = comm.read_text(encoding="utf-8").lower()
            if "продукт" not in ctext and "согласован" not in ctext:
                warnings.append("communication_strategy.md: no explicit product alignment wording")

    decisions = pdir / "state" / "decisions.md"
    if "done" in current or "after" in current:
        check_nonempty(decisions, errors)

    print(f"Validation: {args.project_id}")
    if warnings:
        print("Warnings:")
        for w in warnings:
            print(f"  - {w}")
    if errors:
        print("Errors:")
        for e in errors:
            print(f"  - {e}")
        print("FAIL")
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Reproducible CSV summary for strategist evidence (stdlib csv; pandas optional)."""
from __future__ import annotations

import argparse
import csv
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path


def mean(xs: list[float]) -> float:
    return sum(xs) / len(xs) if xs else float("nan")


def try_float(v: str) -> float | None:
    try:
        return float(str(v).replace(",", ".").strip())
    except (TypeError, ValueError):
        return None


def analyze_stdlib(path: Path, group_col: str | None, value_col: str | None) -> str:
    with path.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            return "Empty or invalid CSV (no headers)."
        rows = list(reader)
        fields = list(reader.fieldnames)

    lines = [
        f"# Table analysis — `{path.name}`",
        "",
        f"- Rows: {len(rows)}",
        f"- Columns: {', '.join(fields)}",
        "",
        "## Missing values",
    ]
    for col in fields:
        missing = sum(1 for r in rows if r.get(col) is None or str(r.get(col)).strip() == "")
        lines.append(f"- `{col}`: {missing} missing ({(missing/len(rows)*100 if rows else 0):.1f}%)")

    numeric_cols = []
    for col in fields:
        vals = [try_float(r.get(col, "")) for r in rows]
        nums = [v for v in vals if v is not None]
        if nums and len(nums) >= max(1, int(0.5 * len(rows))):
            numeric_cols.append(col)
            lines.append("")
            lines.append(f"## Numeric `{col}`")
            lines.append(f"- n={len(nums)}; min={min(nums)}; max={max(nums)}; mean={mean(nums):.4g}")

    if group_col and value_col:
        if group_col not in fields or value_col not in fields:
            lines.append("")
            lines.append(f"## Group error: need columns {group_col}, {value_col}")
        else:
            buckets: dict[str, list[float]] = defaultdict(list)
            for r in rows:
                g = str(r.get(group_col, "")).strip() or "(empty)"
                v = try_float(r.get(value_col, ""))
                if v is not None:
                    buckets[g].append(v)
            lines.append("")
            lines.append(f"## Group `{group_col}` × `{value_col}` (mean)")
            for g, vals in sorted(buckets.items(), key=lambda kv: -mean(kv[1])):
                lines.append(f"- {g}: n={len(vals)}; mean={mean(vals):.4g}")

    # categorical frequency for first non-numeric text col
    for col in fields:
        if col in numeric_cols:
            continue
        c = Counter(str(r.get(col, "")).strip() or "(empty)" for r in rows)
        lines.append("")
        lines.append(f"## Frequency `{col}` (top 10)")
        for k, n in c.most_common(10):
            lines.append(f"- {k}: {n}")
        break

    lines.append("")
    lines.append("## Reproducibility")
    lines.append(f"```bash\npython tools/analyze_table.py {path.as_posix()}")
    if group_col and value_col:
        lines[-1] += f" --group {group_col} --value {value_col}"
    lines[-1] += "\n```"
    lines.append("")
    lines.append("_Engine: Python stdlib csv. Units/periods must be validated by the agent against the source note._")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze CSV for strategist workflows")
    parser.add_argument("csv_path", type=Path)
    parser.add_argument("--group", dest="group_col", default=None)
    parser.add_argument("--value", dest="value_col", default=None)
    parser.add_argument("-o", "--output", type=Path, default=None)
    args = parser.parse_args()

    if not args.csv_path.exists():
        print(f"File not found: {args.csv_path}", file=sys.stderr)
        return 1

    report = analyze_stdlib(args.csv_path, args.group_col, args.value_col)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(report, encoding="utf-8")
        print(f"Wrote {args.output}")
    else:
        print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

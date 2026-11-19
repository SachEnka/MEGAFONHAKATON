#!/usr/bin/env python3
"""Append a cost/time ledger entry for a strategist project."""
from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description="Log estimated cost/time for a step")
    parser.add_argument("project_id")
    parser.add_argument("--note", required=True, help="What was done")
    parser.add_argument("--minutes", type=float, default=0.0, help="Wall time minutes")
    parser.add_argument("--model", default="cursor-agent", help="Model or route label")
    parser.add_argument("--input-tokens", type=int, default=0)
    parser.add_argument("--output-tokens", type=int, default=0)
    parser.add_argument("--usd", type=float, default=None, help="Override USD estimate")
    args = parser.parse_args()

    pdir = ROOT / "projects" / args.project_id
    state = pdir / "state"
    state.mkdir(parents=True, exist_ok=True)
    cost_path = state / "cost.jsonl"

    in_rate = float(os.getenv("COST_INPUT_PER_M", "3"))
    out_rate = float(os.getenv("COST_OUTPUT_PER_M", "15"))
    if args.usd is not None:
        usd = args.usd
    else:
        usd = (args.input_tokens / 1_000_000) * in_rate + (args.output_tokens / 1_000_000) * out_rate

    entry = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "note": args.note,
        "minutes": args.minutes,
        "model": args.model,
        "input_tokens": args.input_tokens,
        "output_tokens": args.output_tokens,
        "usd_estimate": round(usd, 4),
    }
    with cost_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    # Also append a short line to ledger if present
    ledger = state / "ledger.md"
    line = (
        f"\n### cost_log — {entry['ts']}\n"
        f"- Note: {args.note}\n"
        f"- Model: {args.model}; minutes: {args.minutes}; "
        f"tokens in/out: {args.input_tokens}/{args.output_tokens}; "
        f"usd≈{entry['usd_estimate']}\n"
    )
    if ledger.exists():
        with ledger.open("a", encoding="utf-8") as f:
            f.write(line)
    else:
        ledger.write_text("# Ledger\n" + line, encoding="utf-8")

    print(json.dumps(entry, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

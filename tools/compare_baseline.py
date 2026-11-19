#!/usr/bin/env python3
"""Compare agent run vs estimated manual / plain-chat baseline."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_cost_minutes(pdir: Path) -> tuple[float, float]:
    path = pdir / "state" / "cost.jsonl"
    minutes = 0.0
    usd = 0.0
    if not path.exists():
        return minutes, usd
    for ln in path.read_text(encoding="utf-8").splitlines():
        if not ln.strip():
            continue
        obj = json.loads(ln)
        minutes += float(obj.get("minutes") or 0)
        usd += float(obj.get("usd_estimate") or 0)
    return minutes, usd


def main() -> int:
    parser = argparse.ArgumentParser(description="Baseline comparison helper")
    parser.add_argument("project_id")
    parser.add_argument("--manual-hours", type=float, default=12.0, help="Analyst manual estimate")
    parser.add_argument("--plain-chat-hours", type=float, default=2.0, help="Unstructured chat estimate")
    parser.add_argument("--manual-usd", type=float, default=0.0, help="Optional labor cost")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    pdir = ROOT / "projects" / args.project_id
    agent_min, agent_usd = load_cost_minutes(pdir)
    agent_hours = agent_min / 60.0

    report = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "project_id": args.project_id,
        "agent_hours": round(agent_hours, 2),
        "agent_usd_estimate": round(agent_usd, 4),
        "manual_hours_estimate": args.manual_hours,
        "plain_chat_hours_estimate": args.plain_chat_hours,
        "manual_usd_estimate": args.manual_usd,
        "speedup_vs_manual": round(args.manual_hours / agent_hours, 2) if agent_hours else None,
        "notes": [
            "Agent hours from cost.jsonl wall-time notes (approximate).",
            "Manual/plain-chat hours are estimates for comparison, not lab measurements.",
            "Quality: agent enforces evidence, options, gaps; plain chat often skips them.",
        ],
    }

    md = [
        f"# Baseline comparison — {args.project_id}",
        "",
        f"- Generated: {report['ts']}",
        f"- Agent wall time (from cost log): **{report['agent_hours']} h**, usd≈{report['agent_usd_estimate']}",
        f"- Manual analyst estimate: **{report['manual_hours_estimate']} h**",
        f"- Plain chat estimate: **{report['plain_chat_hours_estimate']} h**",
        f"- Speedup vs manual (time): **{report['speedup_vs_manual']}x**" if report["speedup_vs_manual"] else "- Speedup: n/a (no agent minutes logged)",
        "",
        "## Qualitative",
        "- Agent: source-backed claims, ≥3 options, human gate, resume via CURRENT.md.",
        "- Plain chat: faster prose, weaker provenance and weaker post-decision continuity.",
        "- Manual: deeper stakeholder access possible; slower; cost = labor hours.",
        "",
    ]
    text = "\n".join(md)
    print(text)
    if args.write:
        out = pdir / "outputs" / "baseline_comparison.md"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
        (pdir / "state" / "baseline_comparison.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Smoke: Ollama health + validate; optional one-tool live round."""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from local_agent import ollama_client  # noqa: E402
from local_agent.config import OLLAMA_MODEL  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--live", action="store_true", help="Run short agent round")
    parser.add_argument("--project", default="demo-megakino")
    parser.add_argument("--model", default=None)
    args = parser.parse_args()

    health = ollama_client.check_health()
    if not health.get("ok"):
        print("FAIL ollama:", health.get("error"))
        return 2
    print("OK ollama;", "models:", len(health.get("models") or []))

    r = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "validate_artifacts.py"), args.project, "--strict-strategy"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    print(r.stdout.strip())
    if r.returncode != 0:
        print(r.stderr)
        print("FAIL validate")
        return 1
    print("OK validate", args.project)

    if args.live:
        from local_agent.agent_loop import run_agent

        model = args.model or OLLAMA_MODEL
        text = run_agent(
            project_id=args.project,
            user_message=(
                f"Через read_file прочитай projects/{args.project}/state/CURRENT.md "
                "и назови Phase. Ничего не меняй."
            ),
            model=model,
            max_rounds=3,
            verbose=True,
        )
        print("LIVE FINAL:", (text or "")[:500])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

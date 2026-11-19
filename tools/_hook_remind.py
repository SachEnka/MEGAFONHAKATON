#!/usr/bin/env python3
"""Cursor hook helper: remind to update ledger/cost after artifact edits."""
import sys

print(
    "[strategist-hook] Artifact changed. Update state/ledger.md "
    "and run: python tools/cost_log.py <project-id> --note \"...\"",
    file=sys.stderr,
)
sys.exit(0)

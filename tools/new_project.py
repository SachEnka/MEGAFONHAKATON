#!/usr/bin/env python3
"""Scaffold a new strategist project from templates."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description="Create projects/<id> skeleton")
    parser.add_argument("project_id")
    parser.add_argument("--title", default="", help="Short title for brief")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    if not re_match_id(args.project_id):
        print("project_id: use letters, numbers, dash/underscore only", file=sys.stderr)
        return 1

    pdir = ROOT / "projects" / args.project_id
    if pdir.exists() and not args.force:
        print(f"Already exists: {pdir} (use --force)", file=sys.stderr)
        return 1

    for sub in ("inputs", "evidence", "state", "outputs"):
        (pdir / sub).mkdir(parents=True, exist_ok=True)

    title = args.title or args.project_id
    brief = f"""# Бриф — {title}

## Размытый запрос
…

## Уточнено (intake)
| Поле | Значение |
|------|----------|
| Решение | |
| Получатель | |
| Ограничения | Только open data / материалы пользователя |
| Данные | |

## Успех
Situation + ≥3 options + product/comms/validation + decisions.
"""
    (pdir / "brief.md").write_text(brief, encoding="utf-8")

    tpl = ROOT / "templates"
    mapping = {
        "CURRENT.md": pdir / "state" / "CURRENT.md",
        "ledger.md": pdir / "state" / "ledger.md",
        "decisions.md": pdir / "state" / "decisions.md",
    }
    for name, dest in mapping.items():
        src = tpl / name
        if src.exists():
            text = src.read_text(encoding="utf-8").replace("`<id>`", f"`{args.project_id}`")
            dest.write_text(text, encoding="utf-8")
        else:
            dest.write_text(f"# {name}\n", encoding="utf-8")

    (pdir / "state" / "claims.jsonl").write_text("", encoding="utf-8")
    (pdir / "inputs" / "SOURCE_POLICY.md").write_text(
        "# Политика источников\n\nТолько open data и материалы пользователя. Без ПДн в репо.\n",
        encoding="utf-8",
    )

    # seed CURRENT phase
    cur = pdir / "state" / "CURRENT.md"
    if cur.exists():
        t = cur.read_text(encoding="utf-8")
        t = t.replace("`intake` | `gather`", "`intake`")
        cur.write_text(t, encoding="utf-8")

    print(f"Created {pdir}")
    print(f"Next: edit brief.md, then python -m local_agent --project {args.project_id}")
    return 0


def re_match_id(s: str) -> bool:
    import re

    return bool(re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,63}", s))


if __name__ == "__main__":
    raise SystemExit(main())

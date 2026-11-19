# Projects

Каждый проект — папка `projects/<id>/` с `brief.md`, `inputs/`, `evidence/`, `state/`, `outputs/`.

| Проект | Назначение |
|--------|------------|
| [`demo-megakino/`](demo-megakino/) | Основное демо сдачи (отчёт `report.md` / `report.html`) |
| [`demo-eva/`](demo-eva/) | Вторая задача — обобщение workflow |

Новый проект:

```bash
python tools/new_project.py my-case --title "Краткое имя"
```

Затем: материалы в `inputs/` и `python -m local_agent --project my-case` (или Cursor + `AGENTS.md`).

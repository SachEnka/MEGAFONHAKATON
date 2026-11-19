# Переносимость

## Что переносить

Вся папка репозитория (без `.env`, без `_vendor/`, без `local_sessions/` — они в gitignore).

Прогресс задачи = файлы в `projects/<id>/`. Новый чат / другая машина:

```text
Прочитай AGENTS.md и projects/<id>/state/CURRENT.md — продолжай.
```

или:

```bash
python -m local_agent --project <id>
```

## Среды

| Среда | Как |
|-------|-----|
| Cursor | Открыть папку; rules + skills |
| Ollama local | `python -m local_agent --check` затем run |
| Другой IDE | Те же markdown-инструкции; CLI tools |

## Checklist после переноса

1. `python tools/smoke_local.py --project demo-megakino`
2. `python tools/validate_artifacts.py demo-megakino --strict-strategy`
3. `python tools/validate_artifacts.py demo-eva --strict-strategy`
4. При Ollama: модель с tool calling (`qwen3:8b` или аналог)

## Windows notes

- Python 3.10+
- Для agency convert-скриптов нужен Git Bash (не обязателен для работы Стратега)
- Пути в tools — pathlib, кроссплатформенны

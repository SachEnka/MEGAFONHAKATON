# Пример checkpoint после паузы (для демо / видео)

Скопируйте в новый чат Cursor:

```text
Прочитай AGENTS.md и projects/demo-megakino/state/CURRENT.md — продолжай с сохранённого места.
```

Ниже — **как выглядел** CURRENT на паузе после options (исторический снимок). Сейчас актуальный CURRENT = `done`; этот файл нужен, чтобы жюри увидело механизм resume.

---

## Snapshot at pause (awaiting_human_choice)

```markdown
## Phase
awaiting_human_choice

## Last completed step
options.md готов (A–D), рекомендация C+B.

## Next action
Дождаться выбора человека; затем skill strategy-pack.

## Human gate
- Status: open
- Question: Какой вариант фиксируем?
```

Продолжение после ответа не пересобирает evidence заново: читает ledger и переходит к strategy.

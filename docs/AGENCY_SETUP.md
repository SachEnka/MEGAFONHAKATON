# Установка Agency Agents для хакатона

Репозиторий: https://github.com/msitarzewski/agency-agents

## Что уже сделано в этом проекте

1. Клон (shallow) → `_vendor/agency-agents/` (в `.gitignore`).
2. `scripts/convert.sh --tool cursor` → `.mdc` в `integrations/cursor/rules/`.
3. В проект скопирован **узкий** набор в `.cursor/rules/`:

| Файл | Роль |
|------|------|
| `product-manager.mdc` | Продуктовый лид / стратегия |
| `feedback-synthesizer.mdc` | Синтез фидбека |
| `trend-researcher.mdc` | Тренды рынка |
| `sprint-prioritizer.mdc` | Приоритеты / варианты |
| `ux-researcher.mdc` | UX-исследование |
| `ux-architect.mdc` | UX-архитектура |
| `persona-walkthrough-specialist.mdc` | Персоны / walkthrough |
| `research-synthesist.mdc` | Исследовательский синтез |
| `content-creator.mdc` | Контент / сообщения |
| `social-media-strategist.mdc` | Канальная стратегия |
| `growth-hacker.mdc` | Рост (гипотезы!) |
| `pr-communications-manager.mdc` | PR / коммуникации |
| `rapid-prototyper.mdc` | Быстрые прототипы |
| `prompt-engineer.mdc` | Промпты агента |
| `multi-agent-systems-architect.mdc` | Мультиагентная схема |

Наши правила `strategist-*.mdc` остаются always-on.

## Как пользоваться

```text
Прочитай AGENTS.md. Затем @research-synthesist обнови situation.md по evidence/.
```

```text
@product-manager и @social-media-strategist: согласуйте обещания communication_strategy с product_strategy.
```

Локально без Cursor:

```powershell
python -m local_agent --project demo-megakino
```

## Обновить agency-agents

```powershell
cd _vendor\agency-agents
git pull
& 'C:\Program Files\Git\bin\bash.exe' -lc './scripts/convert.sh --tool cursor'
# затем снова скопировать нужные .mdc в .cursor\rules
```

Альтернатива: десктоп-приложение [Agency Agents](https://github.com/msitarzewski/agency-agents-app/releases/latest) — ставит агентов в Cursor одним кликом.

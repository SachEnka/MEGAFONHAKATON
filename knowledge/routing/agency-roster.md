# Agency Agents (Cursor rules) — ростер для хакатона

Источник: [msitarzewski/agency-agents](https://github.com/msitarzewski/agency-agents)  
Установлены как project rules в `.cursor/rules/*.mdc` (`alwaysApply: false`).  
**Всегда поверх них действуют** `strategist-core` / `strategist-safety` (open data, факты≠гипотезы, human gate).

## Как активировать в Cursor

В чате упомяните правило, например:

```text
@product-manager Помоги уточнить JTBD для МегаКино по brief.md
@research-synthesist Собери картину ситуации из evidence/
@social-media-strategist Черновик коммуникационной стратегии строго по product_strategy.md
@ux-researcher Разбери барьер понимания на лендинге (только видимое)
```

Или: «Activate Product Manager mode and …».

## Карта на фазы Стратега

| Фаза Стратега | Agency agent (slug) | Зачем |
|---------------|---------------------|--------|
| Intake | `product-manager` | Уточнение проблемы, получателя, метрик успеха |
| Gather / research | `research-synthesist`, `trend-researcher`, `feedback-synthesizer` | Синтез источников, тренды, сигналы обратной связи |
| UX / пути | `ux-researcher`, `ux-architect`, `persona-walkthrough-specialist` | Интерфейс, персоны (синтетика помечать!) |
| Options / приоритеты | `sprint-prioritizer`, `product-manager` | Разные ставки, отказы, приоритеты |
| Product strategy | `product-manager`, `growth-hacker` | Ставка, экономика роста (осторожно с гипотезами) |
| Communication | `content-creator`, `social-media-strategist`, `pr-communications-manager` | Сообщение и каналы ⊆ продукт |
| Agent system / meta | `multi-agent-systems-architect`, `prompt-engineer`, `rapid-prototyper` | Устройство агента, промпты, быстрые прототипы |

## Локальный Ollama

`python -m local_agent` сам по себе не подгружает Cursor `@rules`. Для локального режима те же роли задаются через skills + `knowledge/routing/subagents.md`. При необходимости можно читать `.cursor/rules/<slug>.mdc` через `read_file` как reference persona.

## Переустановка / обновление

```powershell
# уже сделано: clone в _vendor/agency-agents + convert.sh --tool cursor
$src = '_vendor\agency-agents\integrations\cursor\rules'
$dst = '.cursor\rules'
# скопировать нужные .mdc (см. список в docs/AGENCY_SETUP.md)
```

Полный `install.sh` на Windows может требовать Git Bash; копирование `.mdc` вручную безопаснее и достаточно для хакатона.

## Не ставить «весь ростер»

283 агента засоряют контекст и мешают Стратегу. Держим узкий набор под продукт + исследование + коммуникации.

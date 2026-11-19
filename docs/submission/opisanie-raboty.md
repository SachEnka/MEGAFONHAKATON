# Описание работы — Стратег Фабрики продуктов

Документ для сдачи (экспорт в PDF). Репозиторий рабочей среды стратега: Cursor и/или локальный запуск.

---

## 1. Архитектура

**Процессы:** intake → gather → research → options (**human gate**) → strategy (product + communication + validation) → after (decisions / revise).

**Инструменты:**

- `python -m local_agent` — Ollama tool-calling loop, sandbox (пути, SSRF, allowlist CLI)
- Cursor rules + Agency specialists (`.cursor/rules/`)
- Skills в `skills/`
- CLI: `status`, `validate_artifacts`, `cost_log`, `evidence_index`, `analyze_table`, `compare_baseline`, `impact`, `new_project`, `smoke_local`
- Browser / web_fetch для open sources

**Знания раздельно:** инструкции (`AGENTS.md`, rules) · методы (`knowledge/`) · материалы проекта (`inputs/evidence`) · состояние (`state/`) · результаты (`outputs/`).

```
[Скриншот: дерево репозитория]
[Скриншот: CURRENT.md + ledger]
```

Подробнее: [../ARCHITECTURE.md](../ARCHITECTURE.md), [../SECURITY.md](../SECURITY.md).

---

## 2. Модели, сервисы, инструменты

| Компонент | Зачем |
|-----------|--------|
| Ollama + `qwen3:8b` (или аналог с tools) | Локальный оркестратор |
| Cursor LLM (альтернатива) | Тот же файловый контур в IDE |
| Agency Agents rules | Специалисты product/UX/research/comms |
| Python stdlib CLI | Валидация, таблицы, impact, cost |
| Web fetch allowlist | Публичные страницы МегаФона и др. |

Полный перечень: [../MODELS_TOOLS.md](../MODELS_TOOLS.md). **Облачные API-ключи для базового запуска не нужны.**

---

## 3. Ключевые промпты и инструкции

| Файл | Роль |
|------|------|
| `AGENTS.md` | Точка входа, фазы, безопасность, resume |
| `.cursor/rules/strategist-*.mdc` | Always-on правила |
| `.cursor/rules/agency-under-strategist.mdc` | Agency под Стратегом |
| `skills/*/SKILL.md` | Процедуры фаз + synthetic/ux/media |
| `knowledge/methods/*` | Методология артефактов |
| `local_agent/prompts.py` | System prompt для Ollama |

Resume:

> Прочитай AGENTS.md и projects/&lt;id&gt;/state/CURRENT.md — продолжай.

---

## 4. Дополнительный уровень (реализовано)

Синтетические интервью; UX; media-review (границы ASR); анализ таблиц; decision support + revise + impact; routing; skills; hooks; субагенты/Agency; MCP/браузер + CLI; KB INDEX; устойчивость; переносимость; baseline + eval provenance; локальный Ollama.

См. [../BONUS_FEATURES.md](../BONUS_FEATURES.md).

---

## 5. Демо-проекты

### Основной: МегаКино

- Отчёт: [`../../projects/demo-megakino/report.md`](../../projects/demo-megakino/report.md) / `report.html`
- Ставка: C+B (честный «один активный»); revise 2026-11-19 сохранил D1
- Evidence + claims C001–C020

### Вторая задача: Ева

- [`../../projects/demo-eva/report.md`](../../projects/demo-eva/report.md)
- Ставка: C (free антиспам + честный upsell)
- Доказывает обобщение workflow

```
[Скриншот: report.html МегаКино]
[Скриншот: validate OK обоих проектов]
```

---

## 6. Время, расходы, ошибки, помощь человека

| | МегаКино | Ева |
|--|----------|-----|
| Wall time (cost log) | ~2.4 ч | ~0.8 ч |
| vs manual (оценка) | ~14 ч → ~5.8× | ~8 ч → ~9.6× |
| Облачные ключи | 0 | 0 |

**Помощь человека:** уточнение брифа; human gate выбора варианта; приёмка обещаний; запись видео/PDF-скриншотов.

**Ошибки / уроки:**

- Состав 2023 ≠ 2026 — нельзя тащить market share как текущий факт.
- Демо-CSV отзывов легко принять за «данные оператора» — жёсткие пометки.
- Конфликт витрин Евы free vs paid — зафиксирован как факт разных публичных акцентов.
- PowerShell `Add-Content` ломал UTF-8 в claims — писать через UTF-8 tools.

Eval provenance: [../../eval/results.md](../../eval/results.md) — агент 10/10 привязок vs типичный plain chat.

---

## 7. Ограничения

[../LIMITATIONS.md](../LIMITATIONS.md): нет внутренних метрик; синтетика ≠ спрос; нет ASR-пайплайна; стоимость — оценка; агент не заменяет юридическую/партнёрскую проверку.

---

## 8. Запуск для жюри

```bash
python -m local_agent --check
python tools/smoke_local.py --project demo-megakino
python tools/validate_artifacts.py demo-megakino --strict-strategy
python tools/validate_artifacts.py demo-eva --strict-strategy
```

Или Cursor: открыть папку → команда resume / `@product-manager` + `AGENTS.md`.

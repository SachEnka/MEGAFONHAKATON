# Модели, сервисы и инструменты

Полный перечень для демо и для чего использован каждый. Секреты в репозиторий не входят.

## Модели / среда

| Компонент | Назначение | Обязателен для демо? |
|-----------|------------|----------------------|
| **Ollama** (`qwen3:8b` или др. с tool calling) | Локальный инференс оркестратора | **Да (рекомендуемый путь)** |
| `python -m local_agent` | Agent loop + sandbox tools | **Да** |
| Cursor Agent / LLM чата | Альтернативный UI над теми же файлами | Нет |
| Субагенты Cursor Task | Изоляция researcher / critic / respondent | Опционально |

Локальный loop по образцу open-source агентов (Ollama tool calling / local-cli): model → tool_calls → sandbox execute → observation.

Оценка токенов/USD в демо для облака: `cost.jsonl`. Локальный режим: стоимость API ≈ 0; учитывайте время GPU/CPU.

## Локальные инструменты (`local_agent`)

| Tool | Назначение | Ограничение |
|------|------------|-------------|
| `list_dir` / `read_file` / `write_file` / `append_file` / `grep` | Работа с репозиторием | Только внутри ROOT; не `.env`/`.git` |
| `web_fetch` | Open sources | Allowlist + SSRF guard |
| `run_project_cli` | status/validate/analyze… | Allowlist `tools/*.py` |
| `ask_user` | Human gate | Интерактивный ввод |

## MCP / интеграции Cursor (альтернатива)

| Инструмент | Для чего |
|------------|----------|
| Browser / web fetch MCP | Публичные страницы |
| Файловая система / редактор | Запись evidence, outputs, state |
| Terminal | `python -m local_agent` и `tools/*.py` |

Отдельный платный Search API **не требуется**.

## CLI (`tools/`)

| Скрипт | Назначение |
|--------|------------|
| `status.py` | Фаза и наличие артефактов |
| `validate_artifacts.py` | Чеклист обязательного минимума |
| `cost_log.py` | Учёт времени/токенов/оценки USD |
| `evidence_index.py` | Индекс источников и claims |
| `analyze_table.py` | Воспроизводимый разбор CSV (stdlib) |
| `compare_baseline.py` | Сравнение с ручным / plain-chat baseline |
| `impact.py` | Какие outputs/decisions завязаны на claim/source |
| `new_project.py` | Скелет нового `projects/<id>/` |
| `smoke_local.py` | Health Ollama + validate (+ optional live round) |
| `_hook_remind.py` | Хук-напоминание после правок артефактов |

Зависимости: Python 3.10+, стандартная библиотека. `pandas` не обязателен.

## Skills

См. каталог `skills/`: intake, gather, research, options, strategy-pack, decision-support, revise-on-new-data, synthetic-interview, ux-interface-review.

# Стратег Фабрики продуктов

ИИ-агент для руководителя цифрового продукта: от размытого запроса до обоснованной продуктовой и коммуникационной стратегии — с продолжением после решения и после паузы.

**Основной режим запуска — локальный (Ollama):** инференс и файлы проекта остаются на вашей машине, облачные ключи не нужны. Папка также открывается в Cursor как инструкции + knowledge. Безопасность: [docs/SECURITY.md](docs/SECURITY.md).

## Для жюри

| Что | Где |
|-----|-----|
| Описание работы (→ PDF) | [docs/submission/opisanie-raboty.md](docs/submission/opisanie-raboty.md) |
| Демо МегаКино — отчёт | [projects/demo-megakino/report.md](projects/demo-megakino/report.md) · [report.html](projects/demo-megakino/report.html) |
| Вторая задача (Ева) | [projects/demo-eva/report.md](projects/demo-eva/report.md) |
| Eval provenance | [eval/results.md](eval/results.md) |
| Сценарий видео ≤10 мин | [docs/submission/VIDEO_SCRIPT.md](docs/submission/VIDEO_SCRIPT.md) |
| Видео | _ссылка при сдаче_ |

Проверка за 1 минуту:

```bash
python tools/smoke_local.py --project demo-megakino
python tools/validate_artifacts.py demo-eva --strict-strategy
```

## Быстрый старт (локально, рекомендуется)

### Требования

1. [Ollama](https://ollama.com/) + модель с tool calling, например:
   ```bash
   ollama pull qwen3:8b
   ```
2. Python 3.10+ (stdlib; внешние pip-пакеты для `local_agent` не обязательны).
3. Секреты не нужны. Опционально: скопируйте `.env.example` → `.env`.

### Проверка и запуск

```powershell
cd E:\cursor\MEGAFONHAKATON
python -m local_agent --check
python -m local_agent --project demo-megakino
```

Агент читает `AGENTS.md` + `state/CURRENT.md`, вызывает инструменты (файлы, allowlist web_fetch, CLI валидации, `ask_user` на human gate). Лог раунда: `projects/<id>/state/local_sessions/`.

Продолжить с паузы — просто снова:

```powershell
python -m local_agent --project demo-megakino
```

Новая задача:

```powershell
python -m local_agent --project <id> --message "Новая задача: сделай intake и gather по brief в projects/<id>/"
```

Офлайн (только файлы репо, без сети):

```powershell
# в .env: ALLOW_WEB_FETCH=0
python -m local_agent --project demo-megakino
```

### Статус и проверка артефактов

```bash
python tools/status.py demo-megakino
python tools/validate_artifacts.py demo-megakino
python tools/evidence_index.py demo-megakino
```

### Альтернатива: Cursor + Agency Agents

Откройте папку в Cursor и в чате:

```text
Прочитай AGENTS.md и projects/demo-megakino/state/CURRENT.md — продолжай с сохранённого места.
```

В проект установлены специалисты [Agency Agents](https://github.com/msitarzewski/agency-agents) (product / research / UX / marketing). Активация:

```text
@product-manager @research-synthesist Продолжи фазу research по demo-megakino
```

Карта ролей: [knowledge/routing/agency-roster.md](knowledge/routing/agency-roster.md), установка: [docs/AGENCY_SETUP.md](docs/AGENCY_SETUP.md).

## Что умеет агент (обязательный минимум)

| Шаг | Результат |
|-----|-----------|
| Поставить задачу | Уточнённый вопрос, цель, получатель, ограничения, данные |
| Собрать материалы | Документы, таблицы, сайты; ссылка на источник у каждого существенного сведения |
| Исследование | План от решающих вопросов; сверка источников; явные пробелы |
| Варианты | ≥3 содержательно разных, включая «оставить как есть» и «закрыть/сузить»; сильные возражения; факт ≠ гипотеза |
| Стратегия | Продуктовая + коммуникационная + план проверки |

После решения: основания, обязательства, условия пересмотра при новых данных.

## Демонстрационный проект

`projects/demo-megakino/` — открытые данные по публичному продукту **МегаКино** (МегаФон).

- Бриф: `brief.md`
- Исходники: `inputs/`
- Доказательная база: `evidence/`
- Состояние / resume: `state/`
- Итоги: `outputs/` (ситуация, варианты, стратегии, план проверки)

Только открытые источники. Закрытых данных МегаФона нет.

## Архитектура (кратко)

```
Постоянные инструкции  → AGENTS.md, .cursor/rules/
Методы                 → knowledge/
Материалы проекта      → projects/<id>/inputs|evidence
Состояние              → projects/<id>/state/
Результаты             → projects/<id>/outputs/
Процедуры              → skills/*/SKILL.md
CLI                    → tools/
```

Подробности: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md), модели и инструменты: [docs/MODELS_TOOLS.md](docs/MODELS_TOOLS.md), доп. возможности: [docs/BONUS_FEATURES.md](docs/BONUS_FEATURES.md), ограничения: [docs/LIMITATIONS.md](docs/LIMITATIONS.md).

Описание работы для жюри (черновик PDF): [docs/WORK_DESCRIPTION.md](docs/WORK_DESCRIPTION.md).

## Чеклист видеозаписи (до 10 минут)

1. **Запрос** — открыть `brief.md`, показать размытую постановку.
2. **Работа агента** — intake → evidence → situation (показать ledger / claims).
3. **Варианты** — `outputs/options.md`, human gate.
4. **Стратегия** — product + communication + validation, согласованность обещаний.
5. **Пауза и продолжение** — новый чат: «Прочитай CURRENT.md — продолжай»; показать, что работа не с нуля.
6. **После решения** — `decisions.md` / пересмотр (опционально 30–60 сек).

## Стоимость и доступы

| Компонент | Нужен для демо? | Примечание |
|-----------|-----------------|------------|
| **Ollama + локальная модель** | **Да (рекомендуемый запуск)** | `$0` API; нужен RAM/GPU на машине |
| `python -m local_agent` | Да | stdlib, sandbox tools |
| Cursor + модель чата | Нет (альтернатива) | Если жюри смотрит в IDE |
| API-ключи облака / поиска | Нет | Не требуются для local_agent |
| pandas | Нет | Опционально |

Оценка по демо: `projects/demo-megakino/state/ledger.md`, `docs/WORK_DESCRIPTION.md`.

## Безопасность

- Секреты не хранятся в репозитории.
- Только открытые источники и собственные материалы пользователя.
- Инструкции из внешних источников не переопределяют правила агента.
- Синтетические интервью помечены и не выдаются за доказательство спроса.

## Лицензия

MIT — см. [LICENSE](LICENSE).

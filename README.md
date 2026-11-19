# Стратег Фабрики продуктов

Рабочее пространство для руководителя цифрового продукта: от размытого запроса до согласованных продуктовой и коммуникационной стратегий — с проверяемыми основаниями и продолжением после решения.

**Визуальные отчёты:** откройте [presentation/index.html](presentation/index.html) в браузере.

## Для жюри

| Что | Где |
|-----|-----|
| Описание работы | [docs/submission/opisanie-raboty.md](docs/submission/opisanie-raboty.md) |
| МегаКино | [projects/demo-megakino/report.html](projects/demo-megakino/report.html) |
| Ева (второй кейс) | [projects/demo-eva/report.html](projects/demo-eva/report.html) |
| Сценарий видео | [docs/submission/VIDEO_SCRIPT.md](docs/submission/VIDEO_SCRIPT.md) |
| Репозиторий | https://github.com/SachEnka/MEGAFONHAKATON |

```bash
python tools/smoke_local.py --project demo-megakino
python tools/validate_artifacts.py demo-eva --strict-strategy
```

## Быстрый старт

1. [Ollama](https://ollama.com/) и модель с вызовом инструментов, например `ollama pull qwen3:8b`
2. Python 3.10+
3. Секреты не нужны (опционально `.env` из `.env.example`)

```powershell
cd E:\cursor\MEGAFONHAKATON
python -m local_agent --check
python -m local_agent --project demo-megakino
```

Продолжение после паузы — та же команда или в Cursor:

```text
Прочитай AGENTS.md и projects/demo-megakino/state/CURRENT.md — продолжай с сохранённого места.
```

Новый проект: `python tools/new_project.py my-case --title "Название"`

## Что получается

| Шаг | Результат |
|-----|-----------|
| Постановка задачи | Цель, получатель, ограничения, данные |
| Материалы | Документы, таблицы, сайты; ссылка у каждого существенного тезиса |
| Исследование | Картина ситуации, пробелы |
| Варианты | ≥3, включая «оставить как есть» и сужение/закрытие |
| Стратегия | Продукт + коммуникация + план проверки |
| После решения | Основания, обязательства, пересмотр |

## Устройство

Инструкции, методы, материалы проекта и состояние задачи хранятся раздельно (`AGENTS.md`, `knowledge/`, `projects/*/`). Локальный запуск: `local_agent` (данные на машине). В Cursor доступны специалисты product / research / UX / communications.

Безопасность: [docs/SECURITY.md](docs/SECURITY.md) · архитектура: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)

## Данные

Только открытые источники и собственные материалы проекта. Закрытых данных компаний в репозитории нет.

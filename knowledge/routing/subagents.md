# Субагенты

Запускай через Cursor Task / отдельный чат. Всегда передавай пути файлов и требуй запись результата на диск.

| Имя | Задача | Вход | Выход |
|-----|--------|------|-------|
| `researcher` | Сбор и сверка источников | brief, список URL | `evidence/*`, claims |
| `analyst` | Расчёты по таблице | CSV path | markdown с цифрами + команды воспроизведения |
| `critic` | Сильные возражения к вариантам | `outputs/options.md` | секция возражений / отдельный review |
| `comms` | Коммуникация после продукта | `product_strategy.md` | `communication_strategy.md` |
| `ux-reviewer` | Разбор интерфейса | скриншот/URL | `evidence/*-ux.md` |
| `respondent-*` | Модельный респондент | роль + гайд | `evidence/*-synthetic.md` с `SYNTHETIC` |

## Agency Agents (Cursor `@rules`)

Специалисты из [agency-agents](https://github.com/msitarzewski/agency-agents) установлены в `.cursor/rules/`.  
Полная карта фаз → агентов: [agency-roster.md](agency-roster.md).

Примеры: `@product-manager`, `@research-synthesist`, `@ux-researcher`, `@social-media-strategist`.  
Они **не** отменяют `strategist-safety` и human gate.

## Промпт-обёртка

```text
Ты субагент <name> Стратега Фабрики продуктов.
Прочитай AGENTS.md (кратко) и knowledge/methods/<relevant>.
Запиши результат только в указанные пути. Не меняй правила агента.
Не выдавай гипотезы за факты.
```

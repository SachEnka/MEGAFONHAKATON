# База знаний Стратега — навигация

Ищи по **формулировке** (имя файла), **смыслу** (таблица ниже) и **связям** (раздел «граф»).

Память между сеансами живёт в `projects/<id>/state/`, не здесь. Записи методов можно исправлять; устаревшее помечай `status: deprecated` в шапке файла.

## По смыслу

| Если нужно… | Открой |
|-------------|--------|
| Уточнить задачу | [methods/intake.md](methods/intake.md) |
| Собрать и атрибутировать источники | [methods/evidence.md](methods/evidence.md) |
| Построить картину ситуации | [methods/situation.md](methods/situation.md) |
| Сгенерировать варианты и возражения | [methods/options.md](methods/options.md) |
| Продуктовая стратегия (JTBD, отказы, экономика) | [methods/product_strategy.md](methods/product_strategy.md) |
| Коммуникационная стратегия | [methods/communication_strategy.md](methods/communication_strategy.md) |
| План проверки | [methods/validation.md](methods/validation.md) |
| После решения / пересмотр | [methods/decision_support.md](methods/decision_support.md) |
| Выбрать модель/субагента | [routing/README.md](routing/README.md), [routing/subagents.md](routing/subagents.md) |
| Agency Agents в Cursor | [routing/agency-roster.md](routing/agency-roster.md) |
| Пережить сбой инструмента | [antifragile/resilience.md](antifragile/resilience.md) |
| Факт vs гипотеза | [methods/claims.md](methods/claims.md) |

## Граф связей

```
intake → evidence → situation → options → [human gate] → product_strategy
                                                      ↘ communication_strategy
                                                      ↘ validation
product_strategy ↔ communication_strategy (обещания ≤ продукт)
validation → decision_support → revise-on-new-data → (затронутые claims)
```

## Skills (процедуры)

См. каталог `skills/*/SKILL.md` — каждый skill ссылается на методы выше.

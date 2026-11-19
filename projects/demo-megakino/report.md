# Отчёт для решения — МегаКино (demo-megakino)

**Для жюри / руководителя продукта.** Open data only. Полные артефакты: `outputs/`, `evidence/`, `state/`.

## Рекомендация

Выбрать ставку **C + элементы B**: честное сообщение «платите как за один — выбираете, какой из пяти активен»; убрать допы с первого экрана; primary JTBD = сезонный выбор одного кинотеатра. Решение D1 сохранено после revise 2026-11-19 (паритет цены усиливает нужду в ясности опции смены, не отменяет механику).

См. [product_strategy.md](outputs/product_strategy.md), [communication_strategy.md](outputs/communication_strategy.md), [decisions.md](state/decisions.md).

## Картина ситуации (кратко)

| Тип | Утверждение | ID / источник |
|-----|-------------|----------------|
| Факт | 5 основных с переключением; не «все сразу» в FAQ | [C003](state/claims.jsonl) · [landing](evidence/20261104-megakino-landing.md) |
| Факт | 399 ₽ / 30 дней; состав с Кинопоиском | [C006](state/claims.jsonl) · [C015](state/claims.jsonl) |
| Факт | Исторически «один в моменте» (2023); состав тогда другой | [C008](state/claims.jsonl) · [C009](state/claims.jsonl) |
| Факт | Паритет ориентира с одиночными OTT ~299–399 ₽ | [C017](state/claims.jsonl) |
| Гипотеза | Hero создаёт expectation gap | [C010](state/claims.jsonl) · [ux](evidence/20261104-ux-landing.md) |
| Гипотеза | Без явной опции смены при паритете цены выгоднее прямой OTT | [C019](state/claims.jsonl) |
| Прогноз | Честный hero снизит негатив expectation gap (нужен A/B) | [C016](state/claims.jsonl) |

Пробелы: реальные churn/conversion, доля читающих FAQ — [situation.md](outputs/situation.md).

## Варианты

| | Суть | Возражение |
|--|------|------------|
| A Status quo | Не менять сообщение | Gap и паритет цены бьют по доверию |
| B Сузить | Жёстко «один из…», меньше широты | Потеря дифференциации vs одиночной OTT |
| **C+B (выбор)** | Честный сезон+свитч + допы со второго экрана | Честность может снизить top-of-funnel — мерить |
| D Бандл-перк | Толкать как perk тарифа | Не лечит post-connect confusion |

Подробно: [options.md](outputs/options.md).

## Стратегии

- **Продукт:** механика «один активный» first-class; отказы от «все пять сразу».  
- **Коммуникация:** ключ — «как за один — какой из пяти активен»; proof = состав, цена, лимиты смены.  
- **Проверка:** A/B hero + comprehension + early churn; стопы в [validation_plan.md](outputs/validation_plan.md).

## После решения / пересмотр

- Обязательства и роли: [decisions.md](state/decisions.md).  
- Revise 2026-11-19: [revision_log.md](state/revision_log.md) — D1 сохранён.  
- Resume: читать [CURRENT.md](state/CURRENT.md).

## Стоимость (оценка)

См. [baseline_comparison.md](outputs/baseline_comparison.md) и `state/cost.jsonl`: порядка **~2.4 ч** агента vs **~14 ч** ручной оценки; API/Ollama локально ≈ 0 доп. ключей.

## Как проверить репозиторий

```bash
python tools/validate_artifacts.py demo-megakino --strict-strategy
python tools/status.py demo-megakino
```

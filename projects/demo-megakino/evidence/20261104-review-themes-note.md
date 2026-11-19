# Демо-агрегат тем отзывов (методика)

- Source: `inputs/review_themes_aggregate.csv`
- Accessed: 2026-11-04
- Type: table
- Provenance: **synthetic aggregate for method demo** — см. `inputs/SOURCE_POLICY.md`

## Extract

Топ тем по `mentions` (из файла):

1. `value_unclear_five_vs_one` — 42 (28%) — negative  
2. `switching_friction` — 31 (21%) — negative  
3. `price_fair_vs_single_ott` — 24 (16%) — mixed  
4. `content_discovery` — 18 (12%) — negative  
5. `billing_with_mobile` — 15 (10%) — mixed  
…

Полный воспроизводимый разбор: `evidence/20261104-reviews-table-analysis.md`.

## Notes

Нельзя утверждать, что это распределение реальной базы МегаФона. В стратегии использовать как **гипотезы приоритета барьеров**, согласованные с тем, что видно на лендинге (UX evidence).

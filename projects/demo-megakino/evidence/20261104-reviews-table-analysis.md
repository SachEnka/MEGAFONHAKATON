# Table analysis — `review_themes_aggregate.csv`

- Rows: 8
- Columns: theme, mentions, share_pct, sentiment, note

## Missing values
- `theme`: 0 missing (0.0%)
- `mentions`: 0 missing (0.0%)
- `share_pct`: 0 missing (0.0%)
- `sentiment`: 0 missing (0.0%)
- `note`: 0 missing (0.0%)

## Numeric `mentions`
- n=8; min=8.0; max=42.0; mean=20.62

## Numeric `share_pct`
- n=8; min=5.0; max=28.0; mean=13.75

## Group `theme` × `mentions` (mean)
- value_unclear_five_vs_one: n=1; mean=42
- switching_friction: n=1; mean=31
- price_fair_vs_single_ott: n=1; mean=24
- content_discovery: n=1; mean=18
- billing_with_mobile: n=1; mean=15
- positive_variety: n=1; mean=15
- extra_catalogs_upsell: n=1; mean=12
- device_tv_setup: n=1; mean=8

## Frequency `theme` (top 10)
- value_unclear_five_vs_one: 1
- switching_friction: 1
- price_fair_vs_single_ott: 1
- content_discovery: 1
- billing_with_mobile: 1
- extra_catalogs_upsell: 1
- device_tv_setup: 1
- positive_variety: 1

## Reproducibility
```bash
python tools/analyze_table.py projects/demo-megakino/inputs/review_themes_aggregate.csv --group theme --value mentions
```

_Engine: Python stdlib csv. Units/periods must be validated by the agent against the source note._

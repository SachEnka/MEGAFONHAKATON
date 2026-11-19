# Table analysis — `store_review_themes_aggregate.csv`

- Rows: 5
- Columns: theme, mentions, share_pct, sentiment, note

## Missing values
- `theme`: 0 missing (0.0%)
- `mentions`: 0 missing (0.0%)
- `share_pct`: 0 missing (0.0%)
- `sentiment`: 0 missing (0.0%)
- `note`: 0 missing (0.0%)

## Numeric `mentions`
- n=5; min=16.0; max=36.0; mean=24

## Numeric `share_pct`
- n=5; min=14.0; max=30.0; mean=20

## Frequency `theme` (top 10)
- subscription_value_unclear: 1
- service_management_friction: 1
- billing_one_balance_positive: 1
- spam_of_offers: 1
- content_discovery_hard: 1

## Reproducibility
```bash
python tools/analyze_table.py E:/cursor/MEGAFONHAKATON/projects/demo-megakino/inputs/store_review_themes_aggregate.csv
```

_Engine: Python stdlib csv. Units/periods must be validated by the agent against the source note._

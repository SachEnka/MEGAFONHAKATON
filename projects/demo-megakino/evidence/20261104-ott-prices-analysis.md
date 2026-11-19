# Table analysis — `ott_price_snapshot.csv`

- Rows: 7
- Columns: service, plan_note, price_rub_30d, simultaneous_note, source_note, as_of

## Missing values
- `service`: 0 missing (0.0%)
- `plan_note`: 0 missing (0.0%)
- `price_rub_30d`: 0 missing (0.0%)
- `simultaneous_note`: 0 missing (0.0%)
- `source_note`: 0 missing (0.0%)
- `as_of`: 0 missing (0.0%)

## Numeric `price_rub_30d`
- n=7; min=299.0; max=399.0; mean=384.7

## Frequency `service` (top 10)
- MegaKino: 1
- START: 1
- Wink: 1
- KION: 1
- PREMIER: 1
- Kinopoisk: 1
- IVI: 1

## Reproducibility
```bash
python tools/analyze_table.py projects/demo-megakino/inputs/ott_price_snapshot.csv
```

_Engine: Python stdlib csv. Units/periods must be validated by the agent against the source note._

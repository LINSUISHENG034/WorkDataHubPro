# Annual Award Replay Runbook

## Goal

Run the `annual_award` validation slice end to end and determine whether the
`monthly_snapshot` output matches the accepted replay baseline.

## Inputs

- workbook path containing `TrusteeAwards` and `InvesteeAwards`
- config release `2026-04-11-annual-award-baseline`
- replay root `reference/historical_replays/annual_award`

## Command

```bash
uv run python -m work_data_hub_pro.apps.etl_cli.main replay-annual-award data/annual_award_2026_03.xlsx 2026-03
```

## Expected Output

- `publication_results=5`
- `projection_results=2`
- `compatibility_case=False`

If `compatibility_case=True`, inspect
`reference/historical_replays/annual_award/evidence/compatibility_cases/`
before merging.

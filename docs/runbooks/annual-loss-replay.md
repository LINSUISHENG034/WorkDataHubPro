# Annual Loss Replay Runbook

## Goal

Run the `annual_loss` validation slice end to end and determine whether the
`monthly_snapshot` output matches the accepted replay baseline.

## Inputs

- workbook path containing `企年受托流失(解约)` and `企年投资流失(解约)`
- config release `2026-04-12-annual-loss-baseline`
- replay root `reference/historical_replays/annual_loss`

## Command

```bash
uv run python -m work_data_hub_pro.apps.etl_cli.main replay-annual-loss data/annual_loss_2026_03.xlsx 2026-03
```

## Expected Output

- `publication_results=5`
- `projection_results=2`
- `compatibility_case=False`

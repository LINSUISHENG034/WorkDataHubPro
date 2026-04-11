# Annuity Performance Replay Runbook

## Goal

Run the first `WorkDataHubPro` validation slice end to end and determine whether
the `monthly_snapshot` output matches the accepted replay baseline.

## Inputs

- workbook path for the `AnnuityPerformance` sheet
- config release `2026-04-11-annuity-performance-baseline`
- replay root `reference/historical_replays/annuity_performance`

## Command

```bash
uv run python -m work_data_hub_pro.apps.etl_cli.main replay-annuity-performance data/annuity_performance_2026_03.xlsx 2026-03
```

## Expected Output

- `publication_results=4`
- `projection_results=2`
- `compatibility_case=False`

If `compatibility_case=True`, inspect `reference/historical_replays/annuity_performance/evidence/compatibility_cases/`
and create a human adjudication decision before merging.

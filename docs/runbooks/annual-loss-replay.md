# Annual Loss Replay Runbook

## Goal

Run the `annual_loss` validation slice end to end and determine whether the
`monthly_snapshot` output matches the accepted replay baseline.

## Inputs

- workbook path containing `企年受托流失(解约)` and `企年投资流失(解约)`
- config release `2026-04-12-annual-loss-baseline`
- replay root `reference/historical_replays/annual_loss`
- `customer_plan_history_2026_03.json` fixture under the replay root
- `WDHP_TEMP_ID_SALT` for governed fallback temp ids

## Wrapper Command

```bash
uv run python -m work_data_hub_pro.apps.etl_cli.main replay-annual-loss data/annual_loss_2026_03.xlsx 2026-03
```

## Expected Output

- `comparison_run_id=<generated>`
- `overall_outcome=passed`
- `publication_results=5`
- `projection_results=2`
- `compatibility_case=False`

## Evidence Paths

- `reference/historical_replays/annual_loss/evidence/trace/`
- `reference/historical_replays/annual_loss/evidence/compatibility_cases/`

## Agent CLI

Discover supported domains and registry roots:

```bash
uv run python -m work_data_hub_pro.apps.etl_cli.main replay list-domains
```

Run through the registry-backed agent surface:

```bash
uv run python -m work_data_hub_pro.apps.etl_cli.main replay run --domain annual_loss --workbook data/annual_loss_2026_03.xlsx --period 2026-03
```

Diagnose a completed comparison package:

```bash
uv run python -m work_data_hub_pro.apps.etl_cli.main replay diagnose --comparison-run-id annual_loss-2026-03-<run-id>
```

If `--replay-root` is omitted, the CLI uses the registry root from `replay list-domains`, not the caller's current working directory.

## Temp Identity Salt

Set `WDHP_TEMP_ID_SALT` before replay runs so governed fallback identities remain deterministic:

```bash
set WDHP_TEMP_ID_SALT=your-stable-secret
```

# Annuity Income Replay Runbook

## Goal

Run the `annuity_income` validation slice end to end and determine whether fact processing, identity resolution, reference derivation, and operator artifact visibility match the accepted baseline.

## Inputs

- workbook path containing the `收入明细` sheet
- config release `2026-04-14-annuity-income-baseline`
- replay root `reference/historical_replays/annuity_income`
- `WDHP_TEMP_ID_SALT` for governed fallback temp ids

## Wrapper Command

```bash
uv run python -m work_data_hub_pro.apps.etl_cli.main replay-annuity-income data/annuity_income_2026_03.xlsx 2026-03
```

## Expected Output

- `comparison_run_id=<generated>`
- `overall_outcome=passed`
- `publication_results=3`
- `projection_results=0`
- `compatibility_case=False`

## Evidence Paths

- `reference/historical_replays/annuity_income/evidence/trace/`
- `reference/historical_replays/annuity_income/evidence/compatibility_cases/`

## Agent CLI

Discover supported domains and registry roots:

```bash
uv run python -m work_data_hub_pro.apps.etl_cli.main replay list-domains
```

Run through the registry-backed agent surface:

```bash
uv run python -m work_data_hub_pro.apps.etl_cli.main replay run --domain annuity_income --workbook data/annuity_income_2026_03.xlsx --period 2026-03
```

Diagnose a completed comparison package:

```bash
uv run python -m work_data_hub_pro.apps.etl_cli.main replay diagnose --comparison-run-id annuity_income-2026-03-<run-id>
```

## Temp Identity Salt

Set `WDHP_TEMP_ID_SALT` before replay runs so governed fallback identities remain deterministic:

```bash
set WDHP_TEMP_ID_SALT=your-stable-secret
```

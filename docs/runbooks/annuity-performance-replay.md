# Annuity Performance Replay Runbook

## Goal

Run the first `WorkDataHubPro` validation slice end to end and determine whether
the `monthly_snapshot` output matches the accepted replay baseline.

## Inputs

- workbook path for the `AnnuityPerformance` sheet
- config release `2026-04-11-annuity-performance-baseline`
- replay root `reference/historical_replays/annuity_performance`
- registry-backed default root resolution through `replay list-domains`

## Wrapper Command

```bash
uv run python -m work_data_hub_pro.apps.etl_cli.main replay-annuity-performance data/annuity_performance_2026_03.xlsx 2026-03
```

## Expected Output

- `comparison_run_id=<generated>`
- `overall_outcome=passed`
- `publication_results=4`
- `projection_results=2`
- `compatibility_case=False`

If `compatibility_case=True`, inspect `reference/historical_replays/annuity_performance/evidence/compatibility_cases/`
and create a human adjudication decision before merging.

## Canonical workflow

Use `docs/runbooks/agent-maintenance-workflow.md` as the canonical maintenance workflow for source onboarding, governed rule changes, replay verification, evidence lookup, and compatibility case handling. Keep annuity performance workbook names, replay-root defaults, and expected output counts in this runbook.

## Agent CLI

Discover domains and default replay roots:

```bash
uv run python -m work_data_hub_pro.apps.etl_cli.main replay list-domains
```

Run through the registry-backed agent surface:

```bash
uv run python -m work_data_hub_pro.apps.etl_cli.main replay run --domain annuity_performance --workbook data/annuity_performance_2026_03.xlsx --period 2026-03
```

Diagnose a completed run by `comparison_run_id`:

```bash
uv run python -m work_data_hub_pro.apps.etl_cli.main replay diagnose --comparison-run-id annuity_performance-2026-03-<run-id>
```

Look up one output record through the persisted lineage and trace package:

```bash
uv run python -m work_data_hub_pro.apps.etl_cli.main replay lookup --comparison-run-id annuity_performance-2026-03-<run-id> --record-id <record-id>
```

Inspect or close a compatibility case through the file-backed CLI:

```bash
uv run python -m work_data_hub_pro.apps.etl_cli.main compatibility show-case --evidence-root reference/historical_replays/annuity_performance/evidence --case-id <case-id>
uv run python -m work_data_hub_pro.apps.etl_cli.main compatibility close-case --evidence-root reference/historical_replays/annuity_performance/evidence --case-id <case-id> --owner compatibility-review --resolution-note <note> --closure-evidence <path>
```

`replay run`, `replay diagnose`, and `replay lookup` emit machine-readable JSON. If `--replay-root` is omitted, the CLI uses the registry root instead of the caller's current working directory.

## Temp Identity Salt

Set `WDHP_TEMP_ID_SALT` before running replay commands in environments where fallback identity resolution may occur:

```bash
set WDHP_TEMP_ID_SALT=your-stable-secret
```

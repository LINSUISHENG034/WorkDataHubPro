# Annual Award Replay Runbook

## Goal

Run the `annual_award` validation slice end to end and determine whether the
`monthly_snapshot` output matches the accepted replay baseline.

## Inputs

- workbook path containing `TrusteeAwards` and `InvesteeAwards`
- config release `2026-04-11-annual-award-baseline`
- replay root `reference/historical_replays/annual_award`
- `customer_plan_history_2026_03.json` fixture under the replay root

## Wrapper Command

```bash
uv run python -m work_data_hub_pro.apps.etl_cli.main replay-annual-award data/annual_award_2026_03.xlsx 2026-03
```

## Expected Output

- `comparison_run_id=<generated>`
- `overall_outcome=passed`
- `publication_results=5`
- `projection_results=2`
- `compatibility_case=False`

If `compatibility_case=True`, inspect
`reference/historical_replays/annual_award/evidence/compatibility_cases/`
before merging.

## Canonical workflow

Use `docs/runbooks/agent-maintenance-workflow.md` as the canonical maintenance workflow for source onboarding, governed rule changes, replay verification, evidence lookup, and compatibility case handling. Keep annual award workbook names, replay-root defaults, and expected output counts in this runbook.

## Agent CLI

Discover supported domains and their default replay roots:

```bash
uv run python -m work_data_hub_pro.apps.etl_cli.main replay list-domains
```

Run the award replay through the registry-backed command:

```bash
uv run python -m work_data_hub_pro.apps.etl_cli.main replay run --domain annual_award --workbook data/annual_award_2026_03.xlsx --period 2026-03
```

Diagnose a completed comparison package:

```bash
uv run python -m work_data_hub_pro.apps.etl_cli.main replay diagnose --comparison-run-id annual_award-2026-03-<run-id>
```

Look up one output record through the persisted lineage and trace package:

```bash
uv run python -m work_data_hub_pro.apps.etl_cli.main replay lookup --comparison-run-id annual_award-2026-03-<run-id> --record-id <record-id>
```

Inspect or close a compatibility case through the file-backed CLI:

```bash
uv run python -m work_data_hub_pro.apps.etl_cli.main compatibility show-case --evidence-root reference/historical_replays/annual_award/evidence --case-id <case-id>
uv run python -m work_data_hub_pro.apps.etl_cli.main compatibility close-case --evidence-root reference/historical_replays/annual_award/evidence --case-id <case-id> --owner compatibility-review --resolution-note <note> --closure-evidence <path>
```

If `--replay-root` is omitted, the CLI uses the registry root from `replay list-domains`, not the caller's current working directory.

## Temp Identity Salt

Set `WDHP_TEMP_ID_SALT` before running replay commands in environments where fallback identity resolution may occur:

```bash
set WDHP_TEMP_ID_SALT=your-stable-secret
```

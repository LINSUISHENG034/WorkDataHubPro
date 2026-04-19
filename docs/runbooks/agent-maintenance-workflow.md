# Agent Maintenance Workflow

## Current bounded scope

Current bounded scope: annuity_performance, annual_award, annual_loss, annuity_income.

Adding a brand-new domain is not a doc-only change; it requires updates to src/work_data_hub_pro/apps/orchestration/replay/registry.py, config/domains/<domain>/, config/releases/, reference/historical_replays/<domain>/, and docs/runbooks/<domain>-replay.md.

This workflow is the canonical Phase 4 maintenance contract for the currently registered replay domains. It covers the repo-native surfaces for source onboarding, governed rule adjustment, replay verification, evidence lookup, and compatibility case handling. It does not claim dashboards, persistent storage backends, or manual JSON editing workflows.

## Add a source

Use the replay registry as the source of truth for the bounded onboarding surface.

1. Add or update the registry entry in `src/work_data_hub_pro/apps/orchestration/replay/registry.py`.
2. Add or update the domain config under `config/domains/<domain>/`.
3. Bind the governed release file under `config/releases/`.
4. Add or update replay assets under `reference/historical_replays/<domain>/`.
5. Add or update the domain runbook under `docs/runbooks/` so it points back to this canonical workflow.
6. Add or update contract or integration coverage under `tests/` when the registry path, CLI surface, or evidence contract changes.

For the domains already in scope, verify the registry-backed paths exist before running replay commands.

## Adjust a rule

Keep semantics-changing changes release-governed.

1. Update the affected domain configuration under `config/domains/<domain>/`.
2. Update the corresponding release binding under `config/releases/` when the effective rule surface changes.
3. Keep replay fixtures and accepted evidence under `reference/historical_replays/<domain>/` aligned with the implemented rule contract.
4. Update the domain runbook only when the documented workbook inputs or replay-root details change.
5. Run the narrowest relevant tests before full verification.

Do not treat rule changes as local-only edits. The bounded maintenance surface is committed config, committed replay assets, committed tests, and the CLI commands below.

## Run verify

Use the implemented CLI exactly as exposed by `src/work_data_hub_pro/apps/etl_cli/main.py`.

```bash
uv run python -m work_data_hub_pro.apps.etl_cli.main replay run --domain <domain> --workbook <path> --period <period>
uv run python -m work_data_hub_pro.apps.etl_cli.main replay diagnose --comparison-run-id <id>
uv run python -m work_data_hub_pro.apps.etl_cli.main replay lookup --comparison-run-id <id> --record-id <id>
uv run pytest -v
```

Use `replay list-domains` when you need to confirm the current registry-backed replay roots and runbook paths before invoking a domain run.

## Inspect evidence

Use the comparison run identifier returned by `replay run` as the lookup anchor.

1. Run `replay diagnose` to inspect the comparison package summary, checkpoint statuses, and package paths.
2. Run `replay lookup` to resolve one output record back to the persisted source and stage anchors.
3. Review the returned package paths under the replay root when you need the persisted evidence artifacts referenced by the CLI output.
4. Use the domain runbook for workbook names, replay-root defaults, and expected output counts specific to the active domain.

The lookup and diagnostics flow is intentionally file-backed and registry-backed for the current milestone.

## Compatibility case lifecycle

Use the implemented compatibility commands instead of editing case files by hand.

```bash
uv run python -m work_data_hub_pro.apps.etl_cli.main compatibility show-case --evidence-root <path> --case-id <id>
uv run python -m work_data_hub_pro.apps.etl_cli.main compatibility transition-case --evidence-root <path> --case-id <id> --status <status> --owner <owner> --resolution-note <note>
uv run python -m work_data_hub_pro.apps.etl_cli.main compatibility close-case --evidence-root <path> --case-id <id> --owner <owner> --resolution-note <note> --closure-evidence <path>
```

Use `compatibility show-case` to inspect the current lifecycle state, `compatibility transition-case` to move a case through the supported status flow, and `compatibility close-case` to record closure proof.

## Manual verification checklist

From a clean shell, follow this workflow end to end for one existing replay domain.

1. Inspect registry/config files.
2. Run `replay run`.
3. Run `replay diagnose`.
4. Run the lookup command.
5. Confirm the compatibility-case flow matches the implemented CLI.

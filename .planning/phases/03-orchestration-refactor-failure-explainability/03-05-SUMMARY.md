---
phase: 03-orchestration-refactor-failure-explainability
plan: "05"
subsystem: apps.etl-cli
tags: [cli, replay, runbooks, phase-3]
dependency-graph:
  requires:
    - 03-01
    - 03-02
    - 03-03
    - 03-04
  provides:
    - nested-replay-cli
    - registry-backed-domain-discovery
    - comparison-run-diagnose-command
  affects:
    - docs/runbooks/annuity-performance-replay.md
    - docs/runbooks/annual-award-replay.md
    - docs/runbooks/annual-loss-replay.md
tech-stack:
  added: []
  patterns:
    - machine-readable-replay-cli
    - registry-backed-cli-dispatch
    - typed-diagnose-missing-run-errors
key-files:
  created:
    - tests/contracts/test_replay_cli_contracts.py
  modified:
    - src/work_data_hub_pro/apps/etl_cli/main.py
    - tests/contracts/test_replay_diagnose_contracts.py
    - docs/runbooks/annuity-performance-replay.md
    - docs/runbooks/annual-award-replay.md
    - docs/runbooks/annual-loss-replay.md
decisions:
  - id: "T-03-09"
    summary: "The nested `replay` group emits JSON for agent workflows, while the three existing wrapper commands remain available for humans."
  - id: "T-03-10"
    summary: "Missing comparison packages are surfaced to the CLI as typed diagnose errors without changing the underlying diagnostics reader contract."
metrics:
  duration: "27m"
  completed: "2026-04-13T17:34:20+08:00"
  tasks: 5
  files: 6
---

# Phase 03 Plan 05: Replay CLI Surface - Summary

## One-liner

Added a registry-backed `replay` CLI with machine-readable run/diagnose output while preserving the three existing wrapper commands and updating the operator runbooks.

## Completed Tasks

| Task | Commit | Files |
|------|--------|-------|
| Add nested `replay` command group and preserve wrapper commands | 9ea27a4 | main.py, test_replay_cli_contracts.py |
| Add `replay diagnose` machine-readable output and typed missing-run behavior | 9ea27a4 | main.py, test_replay_diagnose_contracts.py |
| Update replay runbooks for wrapper and agent surfaces | 9ea27a4 | annuity-performance-replay.md, annual-award-replay.md, annual-loss-replay.md |
| Preserve legacy wrapper replay-root behavior for existing human flows | 278518f | main.py |

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Regression] Wrapper commands picked up registry-anchored replay roots and broke the existing loss explainability flow**
- **Found during:** final full-suite verification
- **Issue:** `replay-annual-loss` and the other wrapper commands started defaulting to repo-root replay directories, but the existing human-facing wrapper contract and explainability tests still rely on CWD-relative roots.
- **Fix:** Kept the nested `replay run` command registry-anchored for agents, but restored the three wrapper commands to their historical relative replay-root defaults.
- **Files modified:** `src/work_data_hub_pro/apps/etl_cli/main.py`
- **Commit:** 278518f

## Test Results

Targeted verification passed on the merged result:

- `uv run pytest tests/contracts/test_replay_cli_contracts.py tests/contracts/test_replay_diagnose_contracts.py -v`
- Result: 10 passed
- `rg -n "replay-annuity-performance|replay-annual-award|replay-annual-loss|replay run --domain|replay diagnose --comparison-run-id|replay list-domains|WDHP_TEMP_ID_SALT" docs/runbooks/annuity-performance-replay.md docs/runbooks/annual-award-replay.md docs/runbooks/annual-loss-replay.md`
- `rg -n "add_typer|replay run|replay list-domains|replay-annuity-performance|replay-annual-award|replay-annual-loss|comparison_run_id|overall_outcome|primary_failed_checkpoint|evidence_root|compatibility_case_id" src/work_data_hub_pro/apps/etl_cli/main.py tests/contracts/test_replay_cli_contracts.py`
- `rg -n "replay diagnose|load_replay_diagnostics|ReplayDiagnosticsNotFoundError|checkpoint_statuses|package_paths|comparison_run_id|overall_outcome" src/work_data_hub_pro/apps/etl_cli/main.py tests/contracts/test_replay_diagnose_contracts.py`
- Full-suite regression guard: `uv run pytest -v`
- Result: 140 passed

## Next Phase Readiness

- Phase 03 now has a stable human and agent replay surface over the same registry, diagnostics, and run-report contracts.
- Phase-level verification can judge the whole phase against OPS-01 and PIPE-03 without any remaining incomplete plans.

## Self-Check: PASSED

- Nested replay CLI surface exists and is contract-tested: VERIFIED
- Wrapper commands remain available: VERIFIED
- Runbooks document the implemented commands and `WDHP_TEMP_ID_SALT` prerequisite: VERIFIED

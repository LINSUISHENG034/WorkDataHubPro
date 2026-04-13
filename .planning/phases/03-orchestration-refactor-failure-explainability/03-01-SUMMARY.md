---
phase: 03-orchestration-refactor-failure-explainability
plan: "01"
subsystem: replay-contracts
tags: [replay, diagnostics, contracts, phase-3]
dependency-graph:
  requires: []
  provides:
    - replay-run-report-contracts
    - comparison-run-diagnostics
    - typed-replay-setup-errors
  affects:
    - 03-03
    - 03-04
    - 03-05
tech-stack:
  added: []
  patterns:
    - registry-backed-replay-diagnostics
    - stable-domain-metadata
    - typed-replay-setup-errors
key-files:
  created:
    - src/work_data_hub_pro/apps/orchestration/replay/contracts.py
    - src/work_data_hub_pro/apps/orchestration/replay/diagnostics.py
    - src/work_data_hub_pro/apps/orchestration/replay/errors.py
    - src/work_data_hub_pro/apps/orchestration/replay/registry.py
    - tests/contracts/test_replay_run_report.py
    - tests/contracts/test_replay_diagnose_contracts.py
    - tests/integration/test_replay_setup_failures.py
  modified:
    - src/work_data_hub_pro/governance/evidence_index/file_store.py
decisions:
  - id: "T-03-01"
    summary: "Replay diagnostics resolve comparison-run packages only through registry-declared replay roots."
  - id: "T-03-02"
    summary: "Replay setup and preflight failures use a typed exception hierarchy separate from run-report outcomes."
metrics:
  duration: "17m"
  completed: "2026-04-13T16:13:29+08:00"
  tasks: 5
  files: 8
---

# Phase 03 Plan 01: Replay Contract Foundation - Summary

## One-liner

Frozen replay run-report contracts, comparison-run diagnostics readers, and typed setup-failure translation ahead of the shared runtime refactor.

## Completed Tasks

| Task | Commit | Files |
|------|--------|-------|
| Create isolated plan-01 worktree | e5e03e1 | .worktrees/phase03/plan-01 |
| Define typed replay report and registry contracts | fe59cfe | contracts.py, registry.py, test_replay_run_report.py |
| Add registry-backed comparison-run diagnostics readers | 843948a | diagnostics.py, file_store.py, test_replay_diagnose_contracts.py |
| Freeze typed setup-exception translation | 6af3f39 | errors.py, test_replay_setup_failures.py |
| Clean up isolated replay worktree | 3e0774c | .worktrees/phase03/plan-01 |

## Deviations from Plan

None - plan executed as written.

## Test Results

Targeted verification passed on the merged result:

- `uv run pytest tests/contracts/test_replay_run_report.py tests/contracts/test_replay_diagnose_contracts.py tests/integration/test_replay_setup_failures.py -v`
- Result: 15 passed

## Next Phase Readiness

- `03-03` can adopt the shared replay runtime against frozen report, registry, and diagnostics contracts.
- CLI and later slice work can load comparison-run diagnostics without guessing evidence roots or shell-relative paths.

## Self-Check: PASSED

- Task commits present on `main`: VERIFIED
- Contract and diagnostics files exist on disk: VERIFIED
- Targeted replay contract and setup-failure tests: VERIFIED

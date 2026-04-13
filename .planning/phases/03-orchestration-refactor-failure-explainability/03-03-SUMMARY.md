---
phase: 03-orchestration-refactor-failure-explainability
plan: "03"
subsystem: replay-runtime
tags: [replay, annuity, runtime, phase-3]
dependency-graph:
  requires:
    - 03-01
  provides:
    - shared-replay-runtime
    - annuity-run-report-contract
    - typed-annuity-setup-failures
  affects:
    - 03-04
    - 03-05
    - tests/replay/test_annuity_performance_slice.py
tech-stack:
  added: []
  patterns:
    - shared-replay-runtime-primitives
    - finalized-comparison-run-packages
    - typed-replay-setup-failures
key-files:
  created:
    - src/work_data_hub_pro/apps/orchestration/replay/runtime.py
  modified:
    - src/work_data_hub_pro/apps/orchestration/replay/annuity_performance_slice.py
    - tests/integration/test_replay_setup_failures.py
    - tests/replay/test_annuity_performance_slice.py
    - tests/replay/test_phase2_annuity_performance_gates.py
decisions:
  - id: "T-03-05"
    summary: "The shared runtime owns replay scaffolding and package finalization, while slice files keep domain-specific services, fixtures, and payload shaping explicit."
  - id: "T-03-06"
    summary: "Completed annuity replay runs always write a comparison-run package and expose a typed run report, even when no compatibility case is created."
metrics:
  duration: "25m"
  completed: "2026-04-13T16:47:59+08:00"
  tasks: 4
  files: 5
---

# Phase 03 Plan 03: Annuity Shared Runtime Adoption - Summary

## One-liner

Adopted the first shared replay runtime in the annuity slice while preserving explicit domain wiring, typed setup failures, and completed-run evidence packages.

## Completed Tasks

| Task | Commit | Files |
|------|--------|-------|
| Extract shared replay primitives and adopt them in the annuity runner | d68b126 | runtime.py, annuity_performance_slice.py, test_annuity_performance_slice.py |
| Make annuity setup failures typed and keep completed mismatches on the run-report path | d68b126 | annuity_performance_slice.py, test_replay_setup_failures.py, test_phase2_annuity_performance_gates.py |

## Deviations from Plan

None - the validated runtime extraction and setup-failure coverage landed without extra scope beyond the declared write set.

## Test Results

Targeted verification passed on the merged result:

- `uv run pytest tests/integration/test_replay_setup_failures.py tests/replay/test_annuity_performance_slice.py tests/replay/test_phase2_annuity_performance_gates.py -v`
- Result: 15 passed

## Next Phase Readiness

- `03-04` can move the event-domain replay slices onto `runtime.py` without re-deciding typed setup-failure or evidence-package behavior.
- CLI and diagnostics work in `03-05` can rely on `run_report`, `primary_failure`, and stable evidence-path metadata from completed annuity runs.

## Self-Check: PASSED

- Shared runtime module and annuity slice adoption exist on disk: VERIFIED
- Typed setup-failure integration tests pass through the real annuity runner: VERIFIED
- Replay acceptance and gate suites stay green after the refactor: VERIFIED

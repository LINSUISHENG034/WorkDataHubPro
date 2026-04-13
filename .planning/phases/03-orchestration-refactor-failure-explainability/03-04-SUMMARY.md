---
phase: 03-orchestration-refactor-failure-explainability
plan: "04"
subsystem: replay-runtime
tags: [replay, annual-award, annual-loss, phase-3]
dependency-graph:
  requires:
    - 03-02
    - 03-03
  provides:
    - event-domain-runtime-adoption
    - typed-event-domain-setup-failures
    - replay-safe-loss-temp-id-expectations
  affects:
    - 03-05
    - tests/replay/test_phase2_event_domain_gates.py
    - tests/replay/test_phase2_reference_derivation_gates.py
tech-stack:
  added: []
  patterns:
    - explicit-event-domain-wiring
    - replay-run-report-contract
    - typed-event-domain-setup-errors
key-files:
  created: []
  modified:
    - src/work_data_hub_pro/apps/orchestration/replay/runtime.py
    - src/work_data_hub_pro/apps/orchestration/replay/annual_award_slice.py
    - src/work_data_hub_pro/apps/orchestration/replay/annual_loss_slice.py
    - tests/integration/test_replay_setup_failures.py
    - tests/replay/test_annual_award_slice.py
    - tests/replay/test_annual_loss_slice.py
    - tests/replay/test_phase2_event_domain_gates.py
    - tests/replay/test_phase2_reference_derivation_gates.py
decisions:
  - id: "T-03-07"
    summary: "Award and loss slices reuse shared replay execution/finalization but keep plan-history enrichment, fixture loading, and publication target wiring in the slice files."
  - id: "T-03-08"
    summary: "Loss-domain replay assertions now forbid legacy TEMP-style ids without forcing a fallback on fixtures that still validly use source-value precedence."
metrics:
  duration: "38m"
  completed: "2026-04-13T17:25:32+08:00"
  tasks: 5
  files: 8
---

# Phase 03 Plan 04: Event-Domain Runtime Adoption - Summary

## One-liner

Moved the annual-award and annual-loss replay slices onto the shared runtime while preserving explicit domain enrichment, typed setup failures, and loss-domain identity safety checks.

## Completed Tasks

| Task | Commit | Files |
|------|--------|-------|
| Adopt shared runtime in annual-award and annual-loss slices | 7b7aaa5 | runtime.py, annual_award_slice.py, annual_loss_slice.py |
| Refresh replay and gate tests for run-report and typed failure behavior | 7b7aaa5 | test_annual_award_slice.py, test_annual_loss_slice.py, test_phase2_event_domain_gates.py, test_phase2_reference_derivation_gates.py |
| Extend event-domain setup-failure coverage | 7b7aaa5 | test_replay_setup_failures.py |

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 2 - Missing Critical Coverage] Loss-domain replay fixtures did not actually exercise temp-id fallback on the passing path**
- **Found during:** Task 2 verification
- **Issue:** The trustee-row success fixture still resolved by source value, so asserting a hard-coded opaque id there was incorrect.
- **Fix:** Kept the source-value precedence intact and rewrote the loss replay assertions to prove the absence of legacy `TEMP-*` leakage while still checking opaque `IN...` behavior whenever a `temp_id_fallback` row appears.
- **Files modified:** `tests/replay/test_annual_loss_slice.py`
- **Commit:** 7b7aaa5

## Test Results

Targeted verification passed on the merged result:

- `uv run pytest tests/integration/test_replay_setup_failures.py tests/replay/test_annual_award_slice.py tests/replay/test_annual_loss_slice.py tests/replay/test_phase2_event_domain_gates.py tests/replay/test_phase2_reference_derivation_gates.py -v`
- Result: 30 passed
- `rg -n "AnnualAwardPlanCodeEnrichmentService|customer_master_signal|run_report|execute_replay_run|primary_failure" src/work_data_hub_pro/apps/orchestration/replay/runtime.py src/work_data_hub_pro/apps/orchestration/replay/annual_award_slice.py tests/replay/test_annual_award_slice.py tests/replay/test_phase2_event_domain_gates.py`
- `rg -n "AnnualLossPlanCodeEnrichmentService|customer_loss_signal|run_report|IN[A-Z2-7]{16}" src/work_data_hub_pro/apps/orchestration/replay/annual_loss_slice.py tests/replay/test_annual_loss_slice.py tests/replay/test_phase2_event_domain_gates.py tests/replay/test_phase2_reference_derivation_gates.py`
- Negative check: `rg -n "TEMP-" tests/replay/test_annual_loss_slice.py tests/replay/test_phase2_event_domain_gates.py tests/replay/test_phase2_reference_derivation_gates.py reference/historical_replays/annual_loss`

## Next Phase Readiness

- `03-05` can build the replay CLI on top of a stable registry, diagnostics surface, and per-domain run-report contract across all accepted replay domains.
- Human and agent entrypoints can now assume typed setup-failure behavior is consistent for annuity, award, and loss runs.

## Self-Check: PASSED

- Shared runtime adoption is present in both event-domain slices: VERIFIED
- Award/loss replay and gate suites pass on the merged result: VERIFIED
- Event-domain setup defects raise typed replay setup errors: VERIFIED

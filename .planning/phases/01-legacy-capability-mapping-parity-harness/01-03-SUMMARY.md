---
phase: 01
plan: 03
subsystem: legacy-capability-mapping-parity-harness
tags:
  - parity
  - replay
  - checkpoint
  - contracts
requires:
  - PAR-01
provides:
  - parity baseline schema with explicit sample strategy
  - evidence-backed mismatch report for the annuity deep sample
  - human checkpoint decision log with review history
  - contract validation for Phase 1 parity artifacts
affects:
  - .planning/phases/01-legacy-capability-mapping-parity-harness/schema/parity-baseline.schema.md
  - .planning/phases/01-legacy-capability-mapping-parity-harness/artifacts/parity-baseline.json
  - .planning/phases/01-legacy-capability-mapping-parity-harness/artifacts/mismatch-report.json
  - .planning/phases/01-legacy-capability-mapping-parity-harness/artifacts/decision-log.md
  - .planning/phases/01-legacy-capability-mapping-parity-harness/artifacts/runtime/phase1-parity-offline-2026-04-12-run-001/annuity_performance_2026_03.xlsx
  - .planning/phases/01-legacy-capability-mapping-parity-harness/artifacts/runtime/phase1-parity-offline-2026-04-12-run-001/annuity_performance_parity_evidence.json
  - tests/contracts/test_phase1_parity_baseline_artifacts.py
decisions:
  - Kept the mock annuity workbook as the must-pass deep sample and tracked the real workbook as supplemental contract-gap evidence per docs/gsd/reviews/2026-04-12-phase1-sample-strategy-review.md.
  - Recorded the initial checkpoint as changes-requested, then appended the later approved review instead of overwriting review history.
  - Treated a matched real replay run as a valid executed comparison row with severity none and an explicit evidence_ref.
metrics:
  verification_commands:
    - uv run pytest tests/contracts/test_phase1_parity_baseline_artifacts.py -v
    - uv run pytest tests/replay/test_annuity_performance_slice.py -v
    - uv run pytest tests/contracts -v
  completed_at: 2026-04-12
---

# Phase 01 Plan 03: Parity Baseline and Offline Checkpoint Summary

Phase 1 parity artifacts now include an executed annuity deep-sample comparison,
the sample-strategy split between must-pass and supplemental inputs, and a
completed human checkpoint history.

## Outcomes

- Defined and tightened the parity artifact schema so executed comparison rows
  require `status` and `evidence_ref`, even when the replay result is a match.
- Ran a real `annuity_performance` replay against the accepted legacy snapshot
  and recorded the executed comparison in `mismatch-report.json`.
- Added explicit `sample_strategy` metadata to the baseline and mismatch
  artifacts so the deterministic mock workbook remains the must-pass deep sample
  while the real workbook is preserved as supplemental contract-gap evidence.
- Appended the approved checkpoint result to `decision-log.md` while preserving
  the earlier `changes-requested` review entry.
- Added contract tests that enforce identity fields, sample strategy, executed
  evidence presence, and decision-log requirements.

## Verification

- `uv run pytest tests/contracts/test_phase1_parity_baseline_artifacts.py -v`
  Outcome: passed; 4 tests passed.
- `uv run pytest tests/replay/test_annuity_performance_slice.py -v`
  Outcome: passed; 2 replay tests passed.
- `uv run pytest tests/contracts -v`
  Outcome: passed; 22 contract tests passed.
- `rg -n "decision_owner|comparison_run_id|approved|approved-with-warn|changes-requested|follow_up" .planning/phases/01-legacy-capability-mapping-parity-harness/artifacts/decision-log.md`
  Outcome: passed; both the rejected and approved checkpoint entries are present.

## Commits

- `af58546` `test(governance.compatibility): add phase 1 parity artifact checks`

## Notes

- `.planning/` artifacts remain local-only under current repo policy, so the
  baseline, mismatch report, decision log, runtime workbook, and this summary
  were updated locally rather than committed.
- `reference/historical_replays/annuity_performance/evidence/trace/annuity_performance_2026-03__row_2.json`
  was generated as live replay evidence during execution and remains uncommitted
  local runtime evidence.

## Self-Check

PASSED

- Summary file exists at `.planning/phases/01-legacy-capability-mapping-parity-harness/01-03-SUMMARY.md`.
- Commit `af58546` exists in git history.
- Human checkpoint history contains the final approved result for `comparison_run_id=phase1-parity-offline-2026-04-12-run-001`.

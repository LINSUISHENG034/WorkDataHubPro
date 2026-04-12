---
phase: 02
plan: 04
subsystem: derivation-and-governance-closure
tags:
  - reference-derivation
  - governance
  - verification-assets
  - parity
requires:
  - PAR-02
  - PIPE-02
provides:
  - explicit reference-derivation checkpoint coverage for accepted slices
  - accepted-slice verification-asset manifest
  - forgotten-mechanism sweep with explicit status classifications
affects:
  - src/work_data_hub_pro/apps/orchestration/replay/annuity_performance_slice.py
  - src/work_data_hub_pro/apps/orchestration/replay/annual_award_slice.py
  - src/work_data_hub_pro/apps/orchestration/replay/annual_loss_slice.py
  - reference/verification_assets/phase2-accepted-slices.json
  - docs/runbooks/phase2-verification-assets.md
  - .planning/phases/02-transparent-pipeline-contracts-parity-gates/02-FORGOTTEN-MECHANISMS.md
  - tests/replay/test_phase2_reference_derivation_gates.py
  - tests/contracts/test_phase2_verification_assets.py
decisions:
  - `reference_derivation` uses an optional `legacy_reference_derivation_<period>.json` baseline when present and otherwise compares against the live accepted-slice payload.
  - Missing verification assets are recorded as `deferred` rather than being omitted from the registry.
metrics:
  verification_commands:
    - uv run pytest tests/replay/test_phase2_reference_derivation_gates.py tests/contracts/test_phase2_verification_assets.py -v
    - uv run pytest tests/integration/test_phase2_intake_validation.py tests/replay/test_annuity_performance_slice.py tests/replay/test_phase2_annuity_performance_gates.py tests/integration/test_phase2_event_intake_validation.py tests/replay/test_annual_award_slice.py tests/replay/test_annual_loss_slice.py tests/replay/test_phase2_event_domain_gates.py tests/replay/test_phase2_reference_derivation_gates.py tests/contracts/test_phase2_verification_assets.py -v
  completed_at: 2026-04-12
---

# Phase 02 Plan 04: Derivation and Governance Closure Summary

Phase 2 now treats `reference_derivation` as an explicit accepted-slice
checkpoint and records both verification assets and forgotten mechanisms as
first-class governance artifacts.

## Outcomes

- Added `reference_derivation` to the checkpoint list for all accepted replay
  slices and made derivation mismatches emit a dedicated diff file and
  compatibility case.
- Added `reference/verification_assets/phase2-accepted-slices.json` as the
  machine-readable accepted-slice asset registry.
- Added `docs/runbooks/phase2-verification-assets.md` and
  `02-FORGOTTEN-MECHANISMS.md` so missing assets and hidden mechanisms are
  explicitly classified instead of remaining implicit.

## Verification

- `uv run pytest tests/replay/test_phase2_reference_derivation_gates.py tests/contracts/test_phase2_verification_assets.py -v`
  Outcome: passed; 4 tests passed.
- `uv run pytest tests/integration/test_phase2_intake_validation.py tests/replay/test_annuity_performance_slice.py tests/replay/test_phase2_annuity_performance_gates.py tests/integration/test_phase2_event_intake_validation.py tests/replay/test_annual_award_slice.py tests/replay/test_annual_loss_slice.py tests/replay/test_phase2_event_domain_gates.py tests/replay/test_phase2_reference_derivation_gates.py tests/contracts/test_phase2_verification_assets.py -v`
  Outcome: passed; all accepted-slice checkpoint and governance checks stayed green together.

## Commits

- `6ad451b` `feat(governance.compatibility): add derivation checkpoint governance`

## Notes

- The verification-asset manifest keeps the currently missing `golden_set`,
  `golden_baseline`, `error_case_fixture`, and `real_data_sample` rows visible
  as `deferred` governance items instead of silently ignoring them.
- This summary remains local-only under the current `.planning/` policy.

## Self-Check

PASSED

- Summary file exists at `.planning/phases/02-transparent-pipeline-contracts-parity-gates/02-04-SUMMARY.md`.
- Commit `6ad451b` exists in git history.
- The derivation checkpoint and governance-artifact contract tests passed alongside the accepted-slice replay suite.

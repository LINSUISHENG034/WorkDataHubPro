---
phase: 02
plan: 05
subsystem: parity-gate-tier-runtime
tags:
  - ci
  - parity
  - runbook
  - verification
requires:
  - PAR-04
provides:
  - machine-readable PR/protected-branch/nightly gate matrix
  - fail-fast tier runner
  - human runbook for Phase 2 gate usage
affects:
  - config/verification/phase2-parity-gates.json
  - scripts/run_phase2_parity_gates.py
  - docs/runbooks/phase2-parity-gates.md
  - tests/contracts/test_phase2_ci_gate_matrix.py
decisions:
  - The gate manifest stays provider-neutral and uses repository-native commands only.
  - The runner fails fast on the first non-zero command so CI can block immediately.
metrics:
  verification_commands:
    - uv run pytest tests/contracts/test_phase2_ci_gate_matrix.py -v
    - rg -n '"pr"|"protected_branch"|"nightly"|test_annuity_performance_slice|test_annual_award_slice|test_annual_loss_slice|test_phase2_reference_derivation_gates|uv run pytest -v' config/verification/phase2-parity-gates.json
    - rg -n 'argparse|--tier|pr|protected_branch|nightly|subprocess' scripts/run_phase2_parity_gates.py
    - rg -n '## PR Gate|## Protected Branch Gate|## Nightly Gate|run_phase2_parity_gates.py' docs/runbooks/phase2-parity-gates.md
  completed_at: 2026-04-12
---

# Phase 02 Plan 05: Gate Tier Summary

Phase 2 now exposes explicit PR, protected-branch, and nightly parity-gate tiers
through a machine-readable manifest, a fail-fast runner, and a human runbook.

## Outcomes

- Added `config/verification/phase2-parity-gates.json` with the exact three
  required gate tiers.
- Added `scripts/run_phase2_parity_gates.py` so CI or local users can execute a
  tier by name without provider-specific glue.
- Added `docs/runbooks/phase2-parity-gates.md` and contract coverage for the
  tier matrix.

## Verification

- `uv run pytest tests/contracts/test_phase2_ci_gate_matrix.py -v`
  Outcome: passed; 2 tests passed.
- Structural grep checks confirmed the three tier names, runner flags, and runbook sections exist as planned.

## Commits

- `05f7172` `feat(governance.compatibility): add phase 2 gate tiers`

## Notes

- The gate runner is intentionally provider-neutral; CI integrations should call
  the runner rather than copying tier commands into multiple provider configs.
- This summary remains local-only under the current `.planning/` policy.

## Self-Check

PASSED

- Summary file exists at `.planning/phases/02-transparent-pipeline-contracts-parity-gates/02-05-SUMMARY.md`.
- Commit `05f7172` exists in git history.
- The Phase 2 gate-matrix contract test passed before phase completion tracking was updated.

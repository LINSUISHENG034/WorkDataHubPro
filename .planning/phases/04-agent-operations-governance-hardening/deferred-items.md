# Deferred Items

## 2026-04-19

- `uv run pytest -v` still fails in unrelated pre-existing contract areas outside Plan 04-02 scope, including:
  - `tests/contracts/test_annual_loss_governance_addendum_docs.py::test_annual_loss_acceptance_syncs_risk_register_without_retiring_open_runtime_gaps`
  - `tests/contracts/test_annuity_income_governance_docs.py::test_annuity_income_governance_docs_mark_slice_as_accepted`
  - `tests/contracts/test_legacy_semantic_map_first_wave_pilot.py::test_first_wave_pilot_repo_state_is_populated_and_real_evidence_backed`
- These failures were not introduced by the evidence redaction changes. Plan 04-02 acceptance tests passed, so the failures were left untouched per scope-boundary rules.

## 2026-04-19 - Plan 04-04

- `uv run pytest -v` still fails in unrelated pre-existing areas outside the runbook slice.
- Reproduced failure: `tests/contracts/test_annual_loss_governance_addendum_docs.py::test_annual_loss_acceptance_syncs_risk_register_without_retiring_open_runtime_gaps`.
- Cause: missing file `docs/superpowers/reviews/2026-04-11-legacy-risk-analysis-for-rebuild.md`.
- This was not introduced by the runbook or contract-test changes, so it was left untouched per scope-boundary rules.

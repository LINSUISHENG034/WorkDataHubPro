---
phase: 02
plan: 01
subsystem: governance-compatibility-foundation
tags:
  - parity
  - compatibility
  - checkpoint
  - evidence
requires:
  - PIPE-01
  - PAR-03
provides:
  - shared checkpoint and gate-summary contracts
  - reusable comparison-run package writer
  - expanded compatibility-case semantics for severity and precedent handling
  - contract and integration coverage for the Phase 2 foundation layer
affects:
  - src/work_data_hub_pro/platform/contracts/models.py
  - src/work_data_hub_pro/governance/compatibility/models.py
  - src/work_data_hub_pro/governance/compatibility/gate_models.py
  - src/work_data_hub_pro/governance/compatibility/gate_runtime.py
  - src/work_data_hub_pro/governance/adjudication/service.py
  - src/work_data_hub_pro/governance/evidence_index/file_store.py
  - tests/contracts/test_system_contracts.py
  - tests/contracts/test_phase2_gate_contracts.py
  - tests/integration/test_compatibility_adjudication.py
decisions:
  - Added a comparison-run package root under `comparison_runs/<comparison_run_id>` while preserving the existing `trace/` and `compatibility_cases/` evidence layout.
  - Kept `AdjudicationService.create_case(...)` backward-compatible by defaulting `checkpoint_name` to `monthly_snapshot` and generating a `comparison_run_id` when callers do not supply one yet.
  - Treated passed checkpoints as explicit `CheckpointResult` rows with fingerprints and anchor rows, not as implicit absence of failure artifacts.
metrics:
  verification_commands:
    - uv run pytest tests/contracts/test_system_contracts.py tests/contracts/test_phase2_gate_contracts.py tests/integration/test_compatibility_adjudication.py -v
    - rg -n "class CheckpointFingerprint|class CheckpointDiff|class CheckpointResult|class GateSummary|class ComparisonRunManifest|build_checkpoint_result|summarize_gate_results|write_comparison_run_package|comparison_run_id|checkpoint_name|trace_anchor_rows" src/work_data_hub_pro/governance/compatibility/gate_models.py src/work_data_hub_pro/governance/compatibility/gate_runtime.py src/work_data_hub_pro/platform/contracts/models.py
    - rg -n "severity|decision_status|precedent_status|precedent_key|expires_at|checkpoint_name|comparison_run_id|pending_review|none" src/work_data_hub_pro/governance/compatibility/models.py src/work_data_hub_pro/governance/adjudication/service.py
    - rg -n "manifest.json|gate-summary.json|checkpoint-results.json|source-intake-adaptation.json|lineage-impact.json|publication-results.json|compatibility-case.json|report.md|diffs" src/work_data_hub_pro/governance/evidence_index/file_store.py
  completed_at: 2026-04-12
---

# Phase 02 Plan 01: Gate Foundation Summary

Phase 2 now has a shared checkpoint contract layer, reusable comparison-run
package writers, and richer compatibility-case semantics that later replay
slices can adopt without inventing slice-local gate structures.

## Outcomes

- Added `CheckpointFingerprint`, `CheckpointDiff`, `CheckpointResult`,
  `GateSummary`, and `ComparisonRunManifest` as explicit machine-readable gate
  contracts.
- Added reusable `build_checkpoint_result`, `summarize_gate_results`, and
  `write_comparison_run_package` helpers to keep gate logic out of slice-local
  orchestration code.
- Expanded `CompatibilityCase` and `AdjudicationService.create_case(...)` to
  support Phase 2 severity, decision-status, precedent, expiry, checkpoint, and
  comparison-run semantics.
- Extended `FileEvidenceIndex` so failed-gate artifacts can be written under a
  deterministic comparison-run root while preserving the pre-existing trace and
  direct case storage paths.
- Added contract and integration coverage proving the new gate models serialize,
  comparison-run package files land at the required names, and adjudication
  persists the Phase 2 compatibility fields.

## Verification

- `uv run pytest tests/contracts/test_system_contracts.py tests/contracts/test_phase2_gate_contracts.py tests/integration/test_compatibility_adjudication.py -v`
  Outcome: passed; 5 tests passed.
- `rg -n "class CheckpointFingerprint|class CheckpointDiff|class CheckpointResult|class GateSummary|class ComparisonRunManifest|build_checkpoint_result|summarize_gate_results|write_comparison_run_package|comparison_run_id|checkpoint_name|trace_anchor_rows" src/work_data_hub_pro/governance/compatibility/gate_models.py src/work_data_hub_pro/governance/compatibility/gate_runtime.py src/work_data_hub_pro/platform/contracts/models.py`
  Outcome: passed; all required Phase 2 contract classes, helper entrypoints,
  and fields are present.
- `rg -n "severity|decision_status|precedent_status|precedent_key|expires_at|checkpoint_name|comparison_run_id|pending_review|none" src/work_data_hub_pro/governance/compatibility/models.py src/work_data_hub_pro/governance/adjudication/service.py`
  Outcome: passed; the expanded compatibility semantics and defaults are wired.
- `rg -n "manifest.json|gate-summary.json|checkpoint-results.json|source-intake-adaptation.json|lineage-impact.json|publication-results.json|compatibility-case.json|report.md|diffs" src/work_data_hub_pro/governance/evidence_index/file_store.py`
  Outcome: passed; all required comparison-run filenames are supported.

## Commits

- `8d845ec` `feat(governance.compatibility): add phase 2 gate foundation`

## Notes

- This summary remains local-only under the current repo policy for `.planning/`
  artifacts.
- The initial Wave 1 commit was created before the branch state stabilized;
  execution continued on `slice/transparent-pipeline-contracts-parity-gates-closure`
  after the branch was corrected.

## Self-Check

PASSED

- Summary file exists at `.planning/phases/02-transparent-pipeline-contracts-parity-gates/02-01-SUMMARY.md`.
- Commit `8d845ec` exists in git history.
- Targeted verification for the Wave 1 foundation passed before moving to Wave 2.

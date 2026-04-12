# Phase 2: Transparent Pipeline Contracts & Parity Gates - Research

**Date:** 2026-04-12
**Status:** Complete

## Research Goal

Determine the best execution decomposition for Phase 2 so the current replay harness can become a deterministic parity-gate system without expanding into later-phase runtime or operator scope.

## Scope Anchors

### Must Solve In Phase 2
- Make replay checkpoints explicit and machine-checkable.
- Attach stage-level rule and rationale evidence to parity review.
- Replace snapshot-only mismatch handling with deterministic compare plus adjudication semantics.
- Add CI gate hooks that reflect the now-shared replay runtime.

### Must Not Expand In Phase 2
- No production storage redesign.
- No operator-tooling closure.
- No queue/runtime closure.
- No broad governance or retention platform beyond the failed-gate evidence package.

## Current Runtime Baseline

### What Already Exists
- `src/work_data_hub_pro/platform/contracts/models.py` defines `InputBatch`, `InputRecord`, `CanonicalFactRecord`, and `FieldTraceEvent`.
- `src/work_data_hub_pro/platform/contracts/publication.py` defines `PublicationPlan`, `PublicationTarget`, and `PublicationResult`.
- Replay slices already execute a stable end-to-end stage chain in:
  - `src/work_data_hub_pro/apps/orchestration/replay/annuity_performance_slice.py`
  - `src/work_data_hub_pro/apps/orchestration/replay/annual_award_slice.py`
  - `src/work_data_hub_pro/apps/orchestration/replay/annual_loss_slice.py`
- Trace evidence is already written per `batch_id + anchor_row_no` in `src/work_data_hub_pro/governance/evidence_index/file_store.py`.
- Compatibility mismatch handling already exists, but only as a narrow pending-review case in:
  - `src/work_data_hub_pro/governance/compatibility/models.py`
  - `src/work_data_hub_pro/governance/adjudication/service.py`

### Gaps Relative To Phase 2
- No checkpoint contract or structured checkpoint result model exists.
- Replay slices compare only final `monthly_snapshot` rows; there is no deterministic intermediate gate system.
- `CompatibilityCase` cannot distinguish severity, precedent, exception scope, or expiry.
- Evidence output is trace-centric, not comparison-run-centric.
- Internal contract enforcement is still mostly by convention after raw workbook parsing.
- CI coverage exists as tests, but not as explicit parity-gate tiers.

## Design Conclusions

### 1. Build A Shared Gate Runtime, Not Slice-Specific One-Offs

The accepted replay slices share the same orchestration shape and publication/projection runtime. If Phase 2 adds checkpoint logic separately inside each slice, Phase 3 will need to undo that duplication immediately.

Recommended direction:
- Introduce a shared replay-gating module under `src/work_data_hub_pro/platform/` or `src/work_data_hub_pro/governance/compatibility/` for:
  - checkpoint definitions
  - checkpoint comparison results
  - gate summaries
  - diff serialization
  - evidence package writing
- Keep slice runners responsible for collecting stage outputs and invoking the shared gate runtime with domain-specific checkpoint payloads.

### 2. Keep Source Intake Tolerance Local To Intake

The user-approved review baseline is clear: tolerate messy real-data-style inputs only before normalization into internal contracts.

Recommended direction:
- Add explicit intake adaptation recording at the intake-service boundary.
- Normalize aliased/raw fields into stable internal contract payloads.
- Run strict validators only after `InputBatch` and `InputRecord` are constructed.
- Do not carry tolerance flags deeper into processing, identity, projection, or publication logic.

### 3. Separate Two Kinds Of Evidence

Phase 2 needs both:
- row-level explainability evidence for humans and agents
- comparison-run evidence for gate review and CI

Recommended direction:
- Preserve the existing `trace/` model for anchor-row explainability.
- Add a higher-level comparison-run package rooted by `comparison_run_id` that references trace artifacts rather than replacing them.

### 4. Extend Compatibility Cases Into A Control-Plane Contract

The current case model is too small for Phase 2.

Recommended additions:
- `severity`
- `decision_status`
- `precedent_status`
- `precedent_key`
- `expires_at`
- `checkpoint_name`
- `comparison_run_id`

Reason:
- PAR-03 cannot be satisfied with a generic pending-review blob.
- CI behavior needs stable machine-readable semantics for block versus warn.
- Temporary exceptions and durable precedents must remain distinguishable.

## Recommended Plan Decomposition

### Plan 02-01: Gate Contracts, Adjudication Semantics, And Evidence Package Foundation

Purpose:
- establish the shared models and persistence primitives that every later plan depends on

Key outputs:
- checkpoint and gate result contracts
- expanded compatibility/adjudication models
- comparison-run evidence writer and manifest structure
- contract tests for model shape and file output

Why first:
- downstream slice integration should not invent its own result structures
- CI wiring should depend on stable gate outputs, not the other way around

### Plan 02-02: Intake Adaptation And Deterministic Gate Execution For `annuity_performance`

Purpose:
- implement the first full Wave 1 gate path on the canonical deep-sample slice

Key outputs:
- real-data-style intake adaptation recording
- strict internal validators
- deterministic checkpoint payload generation for:
  - `source_intake`
  - `fact_processing`
  - `identity_resolution`
  - `contract_state`
  - `monthly_snapshot`
- replay and integration tests covering pass/fail outcomes and evidence package shape

Why second:
- `annuity_performance` is already the deepest accepted reference slice and should remain the proving ground

### Plan 02-03: Extend Shared Gate Runtime Across `annual_award` And `annual_loss`

Purpose:
- prove the gate runtime works across the accepted event-domain slices that share the replay/runtime surface

Key outputs:
- event-domain intake adaptation handling
- parity gate coverage for event-domain slices
- tests ensuring cross-slice consistency in gate results, adjudication semantics, and evidence outputs

Why separate from Plan 02-02:
- it preserves the deep-sample-first strategy from Phase 1
- it reduces blast radius if the checkpoint contract needs one more iteration after the first slice

### Plan 02-04: Tiered CI Gate Wiring And Planning/Runbook Surface Updates

Purpose:
- connect the new gate system to PR, protected-branch, and nightly verification paths

Key outputs:
- documented gate commands
- explicit test command matrix
- CI-ready grouping of replay checks
- contract/docs coverage proving Phase 2 gate semantics are now part of the project workflow

Why last:
- CI wiring should stabilize around the actual gate runtime, not lead it

## File Targets By Plan

### Plan 02-01 Likely Touches
- `src/work_data_hub_pro/governance/compatibility/models.py`
- `src/work_data_hub_pro/governance/adjudication/service.py`
- `src/work_data_hub_pro/governance/evidence_index/file_store.py`
- `src/work_data_hub_pro/platform/contracts/models.py`
- new shared gate runtime modules under `src/work_data_hub_pro/platform/` or `src/work_data_hub_pro/governance/compatibility/`
- `tests/contracts/test_system_contracts.py`
- new contract/integration tests for evidence package and adjudication semantics

### Plan 02-02 Likely Touches
- `src/work_data_hub_pro/capabilities/source_intake/annuity_performance/service.py`
- `src/work_data_hub_pro/apps/orchestration/replay/annuity_performance_slice.py`
- `src/work_data_hub_pro/platform/tracing/in_memory_trace_store.py`
- `src/work_data_hub_pro/platform/lineage/registry.py`
- replay and integration tests for `annuity_performance`

### Plan 02-03 Likely Touches
- `src/work_data_hub_pro/capabilities/source_intake/annual_award/service.py`
- `src/work_data_hub_pro/capabilities/source_intake/annual_loss/service.py`
- `src/work_data_hub_pro/apps/orchestration/replay/annual_award_slice.py`
- `src/work_data_hub_pro/apps/orchestration/replay/annual_loss_slice.py`
- replay and integration tests for event-domain parity gates

### Plan 02-04 Likely Touches
- `tests/replay/`
- `tests/contracts/`
- `docs/runbooks/` if Phase 2 execution needs replay-gate instructions
- possibly `pyproject.toml` only if command grouping or test markers are needed

## Key Risks And How Plans Should Address Them

### False Positives From Over-Strict Raw Intake
- Risk: real data fails too early for harmless schema drift
- Plan response: keep adaptation logic and minimum-skeleton rules at intake only

### False Negatives From Weak Intermediate Gate Payloads
- Risk: business-semantic drift escapes until `monthly_snapshot`
- Plan response: compare parity-critical fields at `fact_processing`, `identity_resolution`, and `contract_state`

### Reintroducing Slice Duplication
- Risk: Phase 2 duplicates logic that Phase 3 is supposed to remove
- Plan response: shared checkpoint and evidence runtime first; slice integration second

### Evidence Explosion Without Structure
- Risk: more files, but less diagnosability
- Plan response: comparison-run root with predictable filenames and manifest cross-links

## Verification Strategy

## Validation Architecture

Phase 2 validation should mirror the four execution layers of the phase:

1. Contract tests
- checkpoint result model shape
- expanded `CompatibilityCase` fields
- evidence manifest/file naming invariants

2. Integration tests
- intake adaptation recording
- strict validator failure paths
- adjudication service status/severity behavior
- publication operational gate visibility

3. Replay tests
- `annuity_performance` gate pass and gate fail cases
- `annual_award` and `annual_loss` gate pass/fail consistency
- evidence package emission on mismatch

4. Full-suite gate
- `uv run pytest -v` remains the phase-close verification command

Recommended command tiers:
- quick: targeted contract/integration/replay tests per plan
- full: `uv run pytest -v`

## Planning Notes

- Do not let Phase 2 absorb `reference_derivation` parity closure beyond the agreed Wave 2 placeholder.
- Do not solve production storage location for compatibility/evidence artifacts in this phase.
- Treat `publication` as an operational gate with explicit target/mode/transaction validation, not as a business-data parity comparator.
- Make `comparison_run_id` the stable root key for failed-gate artifacts and adjudication linkage.

## Recommended Outcome

Phase 2 should produce four executable plans in three waves:
- Wave 1: foundation
- Wave 2: deep-sample gate path plus event-domain extension
- Wave 3: CI and workflow wiring

This keeps the work aligned to the user-approved decision order, respects current architecture boundaries, and avoids forcing Phase 3 refactor work into Phase 2.

## RESEARCH COMPLETE

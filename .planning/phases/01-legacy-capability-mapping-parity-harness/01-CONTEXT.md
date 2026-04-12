# Phase 1: Legacy Capability Mapping & Parity Harness - Context

**Gathered:** 2026-04-12
**Status:** Ready for planning

<domain>
## Phase Boundary

Phase 1 delivers an authoritative, repeatable baseline for legacy-to-pro capability mapping and parity validation. Scope is limited to mapping semantics, baseline dataset definition, parity comparison rules, severity policy, evidence minimum, and first must-pass checkpoint design. It does not include broad implementation refactor or multi-domain deep migration.

</domain>

<decisions>
## Implementation Decisions

### Capability mapping model
- **D-01:** Use dual-layer mapping, with business capability as the primary key and stage/function chain as supporting traceability evidence.
- **D-02:** Each mapping row must include legacy behavior meaning, legacy owner/path, Pro owner/path, migration status, parity criticality, and ambiguity notes.

### Legacy coverage strategy
- **D-03:** Use `annuity_performance` as the Phase 1 deep sample slice.
- **D-04:** Register `annual_award` and `annual_loss` in the same matrix for breadth visibility, but do not deep-map them to equal depth in Phase 1.

### Parity comparison basis
- **D-05:** Adopt hybrid parity rule: final output must match, plus selective parity-critical intermediate checks.
- **D-06:** Required intermediate checkpoints for Phase 1 include intake/source recognition, canonical fact shape, identity resolution category, and publication payload key fields.

### Difference severity policy
- **D-07:** Use two severity tiers in Phase 1: `block` and `warn`.
- **D-08:** Any unclassified/new difference type defaults to `block` until explicitly categorized.
- **D-09:** `block` includes semantic output drift, key/publication-key drift, source recognition routing drift, non-adjudicable mismatches, and missing evidence.
- **D-10:** `warn` includes explainable bounded non-semantic differences that preserve final business semantics.

### First must-pass checkpoint
- **D-11:** First checkpoint is an offline report gate with human confirmation, not CI hard-fail.
- **D-12:** Required checkpoint outputs: mapping completeness status, baseline dataset identity, parity summary, mismatch severity table, and human decision log.

### Evidence and trace scope
- **D-13:** Fix minimum evidence set now: mapping matrix, baseline set, mismatch report, severity decision log.
- **D-14:** Defer full evidence directory standard to later phase after mismatch patterns stabilize.
- **D-15:** Even with minimum evidence, enforce stable identity fields now: domain, sample/batch id, baseline version, comparison run id, decision owner.

### the agent's Discretion
- Exact artifact serialization format (Markdown table vs CSV + Markdown summary) as long as required columns and identity fields are preserved.
- Naming conventions for intermediate local working files, provided canonical evidence outputs remain stable and traceable.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Phase decision baseline
- `.planning/ROADMAP.md` — Phase 1 scope, success criteria, and dependency constraints.
- `.planning/REQUIREMENTS.md` — MAP-01/02/03 and PAR-01 acceptance targets for this phase.
- `.planning/PROJECT.md` — rebuild principles: parity-first, non-black-box, incremental delivery.

### User-approved gray-area recommendations
- `docs/gsd/discuss/2026-04-12-phase-1-gray-area-recommendations.md` — approved decision source for all six Phase 1 gray areas.

### Architecture and governance anchors
- `docs/superpowers/specs/2026-04-11-workdatahubpro-rebuild-architecture-draft.md` — capability-first architecture baseline.
- `docs/superpowers/specs/2026-04-11-workdatahubpro-refactor-program.md` — rebuild program sequencing and guardrails.
- `docs/superpowers/specs/2026-04-11-workdatahubpro-first-wave-legacy-coverage-matrix.md` — legacy coverage references for first-wave scope.

### Codebase reality checks
- `.planning/codebase/ARCHITECTURE.md` — current runtime stage flow and boundary ownership.
- `.planning/codebase/CONCERNS.md` — known parity/trace/evidence/performance risks that influence Phase 1 decisions.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `src/work_data_hub_pro/apps/orchestration/replay/annuity_performance_slice.py`: strongest deep-sample candidate for end-to-end mapping proof.
- `src/work_data_hub_pro/capabilities/fact_processing/cleansing/manifest.py`: release+domain rule-pack binding logic for mapping rule ownership.
- `src/work_data_hub_pro/governance/adjudication/service.py`: existing compatibility-case pattern to align mismatch classification outputs.
- `tests/replay/test_annuity_performance_slice.py`: replay verification harness seed for Phase 1 parity checkpoint prototype.

### Established Patterns
- Capability-first package boundaries (`capabilities/`, `platform/`, `governance/`, `apps/`) should remain primary ownership frame.
- Replay slices currently duplicate orchestration flow; mapping must capture invariant stages vs domain-specific logic.
- Evidence/tracing artifacts are already file-based under `reference/historical_replays/`; Phase 1 should use this as temporary evidence carrier.

### Integration Points
- Legacy-to-pro mapping artifacts should link into replay slice entrypoints in `src/work_data_hub_pro/apps/etl_cli/main.py` and `src/work_data_hub_pro/apps/orchestration/replay/*.py`.
- Parity baseline dataset and mismatch report outputs should integrate with existing replay asset directories under `reference/historical_replays/`.
- Severity/adjudication vocabulary should align with governance compatibility constructs in `src/work_data_hub_pro/governance/compatibility/models.py`.

</code_context>

<specifics>
## Specific Ideas

- Approved strategy is "clarity over breadth": one deep sample slice + registered breadth.
- Approved checkpoint approach is "human-confirmed offline first", then evolve to CI blocker later.
- Approved parity doctrine is "final output must-match + selective critical intermediates", not full structural clone.

</specifics>

<deferred>
## Deferred Ideas

- Promote parity gate from offline human-confirmed to CI hard-fail only after mismatch semantics stabilize (target: Phase 2 alignment).
- Define full evidence directory taxonomy and retention/governance standard after Phase 1 mismatch observations are available.

</deferred>

---
*Phase: 01-legacy-capability-mapping-parity-harness*
*Context gathered: 2026-04-12*

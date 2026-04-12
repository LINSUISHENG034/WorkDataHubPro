# Phase 2: Transparent Pipeline Contracts & Parity Gates - Context

**Gathered:** 2026-04-12
**Status:** Ready for planning

<domain>
## Phase Boundary

Phase 2 turns the current replay harness into an explicit deterministic gate system for parity-critical behavior. Scope is limited to stage-boundary contracts, checkpoint taxonomy, adjudication semantics, failed-gate evidence packaging, and CI gating for accepted replay slices. It does not attempt to close broader production-runtime, storage-location, operator-tooling, or full future-wave governance questions.

</domain>

<decisions>
## Implementation Decisions

### Gate checkpoints
- **D-01:** Use a layered checkpoint model instead of treating every stage as the same kind of parity gate.
- **D-02:** Wave 1 parity checkpoints must include `source_intake`, `fact_processing`, `identity_resolution`, `contract_state`, and `monthly_snapshot`.
- **D-03:** `source_intake` is a controlled-tolerance contract gate, not a full business-semantic parity gate.
- **D-04:** `fact_processing`, `identity_resolution`, and `contract_state` are deterministic parity gates.
- **D-05:** `monthly_snapshot` remains the final must-match parity gate.
- **D-06:** `publication` is an operational and contract gate, not a content-level legacy parity gate.
- **D-07:** `reference_derivation` parity gating is required, but lands as Wave 2 closure rather than the first Wave 1 gate set.

### Adjudication model
- **D-08:** Expand `CompatibilityCase` with `severity`, richer `decision_status`, `precedent_status`, `precedent_key`, and `expires_at`.
- **D-09:** Severity remains two-tiered: `block` and `warn`, consistent with Phase 1.
- **D-10:** Every new difference must be recorded explicitly; no silent pass-through is allowed.
- **D-11:** `block` plus `pending_review` fails the gate.
- **D-12:** `warn` plus `pending_review` stays visible in gate output and does not disappear as a silent pass.
- **D-13:** Only previously approved precedent may auto-classify a known difference as acceptable.
- **D-14:** `approved_exception` means accepted for this occurrence only and does not promote the difference to durable precedent.
- **D-15:** Source-intake adaptation differences do not open a `CompatibilityCase` by default unless they break the minimum usable skeleton, violate normalized internal contracts, or alter business-semantic parity outcomes.

### Contract strictness
- **D-16:** Use dual-layer strictness: controlled tolerance at raw `source_intake`, then strict validation after normalization into internal stage contracts.
- **D-17:** After data enters internal contract space, fail fast on structural boundary violations.
- **D-18:** Do not build a large schema-registry platform in Phase 2.
- **D-19:** Keep deep business-semantic checks in replay gates rather than generic contract validators.
- **D-20:** `source_intake` may tolerate explicit field aliases, known file-name variants, extra non-golden columns, and missing non-golden columns when the minimum usable skeleton remains intact.
- **D-21:** Missing golden required fields must fail intake.
- **D-22:** If runtime cannot construct the minimum usable skeleton for `InputBatch` and `InputRecord`, intake must fail immediately.
- **D-23:** Internal validations must enforce required fields, type shape, stable `batch_id`/`domain`/`run_id`, required `anchor_row_no`, monotonic `event_seq`, and legal `PublicationPlan` field combinations.

### Source-intake baseline
- **D-24:** The external `source_intake` target for Phase 2 is `real-data-style`, not `legacy-style`.
- **D-25:** Current simplified `WorkDataHubPro` workbook inputs remain valid as synthetic deterministic fixtures only, not as the authoritative intake baseline.
- **D-26:** Golden required fields and minimum usable skeletons are domain-specific and must be defined for `annuity_performance`, `annual_award`, and `annual_loss` using the review-approved baselines.
- **D-27:** Blank enrichable fields such as event-domain `company_id` and `年金计划号` remain warning-tolerant when lookup and fallback logic still have sufficient context.

### CI gate scope
- **D-28:** Use tiered CI gates rather than either a single must-pass slice or the full broadest matrix on every PR.
- **D-29:** PR gate includes affected tests, source-intake tolerance tests, minimum-skeleton failure tests, `annuity_performance` replay, and explainability retrieval.
- **D-30:** Protected-branch merge gate includes all accepted replay slices.
- **D-31:** Nightly or release gate includes the full `pytest` suite plus broader replay and performance checks.

### Failed-gate evidence package
- **D-32:** Failed parity runs must emit a comparison-run evidence package rather than isolated row-trace files plus a final compatibility case only.
- **D-33:** The minimum package includes `manifest.json`, `gate-summary.json`, `checkpoint-results.json`, `source-intake-adaptation.json`, `diffs/<checkpoint>.json`, `trace/`, `lineage-impact.json`, `publication-results.json`, `compatibility-case.json`, and `report.md`.
- **D-34:** The evidence package must support both human review and downstream agent diagnosis.

### the agent's Discretion
- Exact serialization details for deterministic checkpoint fingerprints and hashes, provided the failed-gate package remains stable and machine-consumable.
- Exact naming of internal validator modules and checkpoint runner helpers, provided the gate taxonomy and semantics above remain unchanged.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Phase scope and accepted decisions
- `.planning/ROADMAP.md` — Phase 2 goal, scope, risks, and success criteria.
- `.planning/REQUIREMENTS.md` — `PAR-02`, `PAR-03`, `PAR-04`, `PIPE-01`, and `PIPE-02` acceptance targets.
- `.planning/PROJECT.md` — parity-first, transparent, incremental rebuild principles.
- `.planning/phases/01-legacy-capability-mapping-parity-harness/01-CONTEXT.md` — locked Phase 1 decisions that Phase 2 must carry forward.
- `docs/gsd/reviews/2026-04-12-phase2-gray-area-review.md` — user-approved decision baseline for all Phase 2 gray areas.

### Architecture and governance anchors
- `docs/superpowers/specs/2026-04-11-workdatahubpro-rebuild-architecture-draft.md` — explicit stage contracts, publication boundary, trace requirements, and compatibility-case intent.
- `docs/superpowers/specs/2026-04-11-workdatahubpro-refactor-program.md` — slice admission rules, first-wave governance, and outstanding cross-cutting runtime decisions.
- `docs/superpowers/specs/2026-04-11-workdatahubpro-first-wave-legacy-coverage-matrix.md` — accepted replay-slice coverage status and deferred cross-cutting rows.

### Codebase reality checks
- `.planning/codebase/ARCHITECTURE.md` — current replay flow, shared runtime, and evidence/adjudication placement.
- `.planning/codebase/CONCERNS.md` — known parity, contract, evidence, and CI/runtime risks that Phase 2 is intended to reduce.
- `.planning/codebase/TESTING.md` — current test boundary model and replay verification entrypoints.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `src/work_data_hub_pro/platform/contracts/models.py`: existing stage contracts (`InputBatch`, `InputRecord`, `CanonicalFactRecord`, `FieldTraceEvent`) to strengthen rather than replace.
- `src/work_data_hub_pro/platform/contracts/publication.py` and `src/work_data_hub_pro/platform/publication/service.py`: current `PublicationPlan` and `PublicationResult` flow for publication-gate enforcement.
- `src/work_data_hub_pro/governance/compatibility/models.py` and `src/work_data_hub_pro/governance/adjudication/service.py`: existing compatibility-case path to expand with severity, precedent, and exception semantics.
- `src/work_data_hub_pro/apps/orchestration/replay/annuity_performance_slice.py` plus parallel award/loss runners: current shared replay pattern where checkpoint and CI decisions will land.
- `tests/replay/test_annuity_performance_slice.py`, `tests/replay/test_annual_award_slice.py`, and `tests/replay/test_annual_loss_slice.py`: current replay acceptance tests to evolve into tiered parity gates.

### Established Patterns
- Capability-first boundaries remain fixed; Phase 2 should strengthen platform contracts and governance semantics without moving business logic into orchestration.
- Replay slices currently compare only final `monthly_snapshot` output; intermediate deterministic gates are still missing.
- Evidence and adjudication are already file-backed and queryable enough to extend into a comparison-run package without introducing a new persistence platform in this phase.
- Accepted slices share publication, projection, trace, and adjudication runtime, so CI gating decisions must treat the replay runtime as shared infrastructure.

### Integration Points
- Replay slice runners under `src/work_data_hub_pro/apps/orchestration/replay/` are the main insertion points for checkpoint execution and failed-gate evidence emission.
- `src/work_data_hub_pro/governance/evidence_index/file_store.py` is the existing artifact root for parity evidence expansion.
- `tests/contracts/`, `tests/integration/`, and `tests/replay/` will need aligned coverage for strict boundary validation, intake adaptation, adjudication semantics, and gate behavior.

</code_context>

<specifics>
## Specific Ideas

- The accepted target is a true Phase 2 gate system, not a heavier version of the Phase 1 snapshot-only replay harness.
- The accepted order is: checkpoint taxonomy first, adjudication semantics second, failed-gate evidence package third, boundary validators fourth, and tiered CI wiring last.
- `source_intake` should be tolerant only long enough to normalize real-data-style input into stable internal contracts; tolerance must not leak beyond that boundary.

</specifics>

<deferred>
## Deferred Ideas

- Physical storage location for `CompatibilityCase` and evidence index remains a broader program/runtime decision outside Phase 2 closure.
- Full `reference_derivation` parity-gate closure is deferred to Wave 2 within this phase direction, rather than the initial Wave 1 checkpoint set.
- Broader production-runtime, queue/runtime, and operator-tooling decisions remain governed by later program tracks and are not pulled into this phase.

</deferred>

---
*Phase: 02-transparent-pipeline-contracts-parity-gates*
*Context gathered: 2026-04-12*

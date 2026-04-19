# Phase 4: Agent Operations & Governance Hardening - Context

**Gathered:** 2026-04-13
**Status:** Ready for planning

<domain>
## Phase Boundary

Phase 4 makes the replay/governance system operationally handoff-ready after Phase 3. Scope is limited to three concrete capability areas already promised in the roadmap: a documented add-source / adjust-rule / run-verify workflow, queryable lineage/evidence lookup from outputs back to source/stage decisions, and governed evidence/adjudication hardening for redaction, severity, ownership, and closure proof. It does not introduce new runtime adapters, dashboards, or queue infrastructure; those remain later-phase work.

</domain>

<decisions>
## Implementation Decisions

### Operator workflow contract
- **D-01:** Phase 4 should center on one explicit repo-native workflow: add a source or adjust a rule through committed config/runbook surfaces, run verification, and inspect evidence using documented commands.
- **D-02:** Prefer extending the existing CLI and runbook surfaces over inventing a separate operator UI or hidden local-only scripts.
- **D-03:** Configuration changes that affect semantics must stay release-governed under `config/` and be paired with verification instructions in committed docs.

### Lineage and evidence lookup
- **D-04:** Lineage lookup should use query helpers over the existing `trace`, `lineage`, and comparison-run evidence structures rather than relying on humans or agents to browse JSON folders manually.
- **D-05:** The primary lookup anchors remain `comparison_run_id`, `batch_id`, `anchor_row_no`, and output identifiers; Phase 4 should make those lookups explicit and test-covered.
- **D-06:** Preserve file-backed evidence as the operational baseline for now; persistent storage/query adapters are deferred.

### Evidence redaction
- **D-07:** Redaction belongs at the evidence persistence boundary, not inside domain business logic.
- **D-08:** Default behavior should preserve auditability while redacting or masking raw business-identifying values such as names and other sensitive payload fields in persisted evidence artifacts.
- **D-09:** Redaction policy should be explicit and governed, not ad hoc per writer call.

### Adjudication lifecycle
- **D-10:** `CompatibilityCase` should become a fuller operational record with explicit severity, decision owner, closure evidence, and lifecycle status transitions.
- **D-11:** Phase 4 should formalize how a pending case becomes approved, rejected, or closed, and that lifecycle should be visible in committed artifacts/tests.
- **D-12:** Keep the control-plane model file-backed and repository-auditable for now instead of adding a new adjudication service backend.

### the agent's Discretion
- Exact CLI command names and file/module placement for lineage and governance helpers, provided they stay discoverable from committed runbooks and existing app boundaries.
- Exact redaction field list and masking representation, provided sensitive identifiers do not persist in plaintext evidence and audit anchors remain intact.
- Exact closure-proof schema for compatibility cases, provided severity, owner, status, and proof-of-closure are all explicit.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Phase scope and acceptance
- `.planning/ROADMAP.md` — Phase 4 goal, scope, requirements, and success criteria.
- `.planning/REQUIREMENTS.md` — `OPS-02`, `OPS-03`, `OPS-04`, `GOV-01`, and `GOV-03` acceptance targets.
- `.planning/PROJECT.md` — current validated constraints and the post-Phase-3 project state.
- `.planning/STATE.md` — current workflow state and recent execution notes.

### Prior phase decisions that constrain Phase 4
- `.planning/phases/03-orchestration-refactor-failure-explainability/03-CONTEXT.md` — locked replay entrypoint, diagnostics, and temp-id decisions from Phase 3.
- `.planning/phases/03-orchestration-refactor-failure-explainability/03-VERIFICATION.md` — what Phase 3 actually delivered and what Phase 4 can build on.
- `.planning/phases/02.1-phase-2-governance-remediation-truthful-gates-and-status-sync/02.1-CONTEXT.md` — truthful checkpoint and governance-state constraints that Phase 4 must preserve.

### Architecture and concerns
- `docs/superpowers/specs/2026-04-11-workdatahubpro-rebuild-architecture-draft.md` — capability/platform/governance/app boundaries and trace/evidence invariants.
- `.planning/codebase/CONCERNS.md` — current evidence-redaction, storage, operability, and trace-query concerns that Phase 4 addresses directly.
- `.planning/codebase/STRUCTURE.md` — current source tree and where operational/gov surfaces belong.
- `.planning/codebase/TESTING.md` — existing test-boundary patterns for contract/integration/replay/performance coverage.

### Code anchors
- `src/work_data_hub_pro/governance/evidence_index/file_store.py` — current evidence persistence and comparison-run read/write API surface.
- `src/work_data_hub_pro/platform/tracing/in_memory_trace_store.py` — current trace lookup boundary and scaling limitation.
- `src/work_data_hub_pro/platform/lineage/registry.py` — current lineage registry lookup boundary.
- `src/work_data_hub_pro/governance/compatibility/models.py` — current `CompatibilityCase` shape and lifecycle fields.
- `src/work_data_hub_pro/apps/etl_cli/main.py` — current CLI entrypoint surface after Phase 3.
- `docs/runbooks/annuity-performance-replay.md` — current human/operator replay guidance baseline.
- `docs/runbooks/annual-award-replay.md` — current human/operator replay guidance baseline.
- `docs/runbooks/annual-loss-replay.md` — current human/operator replay guidance baseline.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `src/work_data_hub_pro/apps/etl_cli/main.py`: already exposes stable replay commands and is the natural place to extend agent/operator entrypoints instead of inventing a new shell surface.
- `src/work_data_hub_pro/governance/evidence_index/file_store.py`: already centralizes comparison-run and trace persistence, so redaction and query helpers belong here or immediately adjacent to it.
- `src/work_data_hub_pro/platform/tracing/in_memory_trace_store.py` and `src/work_data_hub_pro/platform/lineage/registry.py`: current query seams are simple and local, which makes them good first targets for explicit lookup helpers and testable contracts.
- `src/work_data_hub_pro/governance/compatibility/models.py`: already contains severity and decision fields, but not a complete closure-proof lifecycle.

### Established Patterns
- Operational entrypoints live under `apps/` and are documented through runbooks in `docs/runbooks/`.
- Evidence and compatibility records are intentionally file-backed and repo-auditable in the current milestone.
- Business semantics stay out of governance and adapter layers; governance hardening should wrap persistence and adjudication records, not move domain logic.

### Integration Points
- `apps/etl_cli/` for stable operator/agent commands.
- `governance/evidence_index/` for evidence write/read hardening and redaction.
- `platform/tracing/` and `platform/lineage/` for output-to-source lookup surfaces.
- `governance/compatibility/` for lifecycle, severity, and closure-proof hardening.
- `docs/runbooks/` plus contract/integration tests for operator-facing workflow documentation and enforcement.

</code_context>

<specifics>
## Specific Ideas

- The preferred shape is “one documented workflow, one command surface, one query path,” not a scattered set of ad hoc operator notes.
- Redaction should be explicit enough that an agent can rely on the persisted evidence contract without needing tribal knowledge about what fields are safe.
- Compatibility cases should read like auditable records, not just mismatch snapshots with a pending flag.

</specifics>

<deferred>
## Deferred Ideas

- Persistent trace/evidence storage adapters and large-run operability remain later work (Phase 5 / runtime expansion).
- Operator dashboards and richer self-service interfaces remain out of scope for this phase.
- Full multi-surface rule-update UX beyond one documented add-source / adjust-rule / run-verify path is deferred.

</deferred>

---

*Phase: 04-agent-operations-governance-hardening*
*Context gathered: 2026-04-13*

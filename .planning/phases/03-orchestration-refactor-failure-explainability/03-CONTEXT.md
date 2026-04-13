# Phase 3: Orchestration Refactor & Failure Explainability - Context

**Gathered:** 2026-04-13
**Status:** Ready for planning

<domain>
## Phase Boundary

Phase 3 refactors the first-wave replay surface so the accepted replay slices share reusable orchestration mechanics without hiding domain behavior, while failure paths become typed and explainable for both developers and agents. Scope is limited to shared replay primitive extraction, typed run and setup failure contracts, stable agent-facing replay entrypoints, and governed temporary-identity fallback behavior. It does not close broader ETL/operator/runtime parity or deferred queue/reference-sync/manual operator surfaces.

</domain>

<decisions>
## Implementation Decisions

### Shared replay composition
- **D-01:** Extract shared replay primitives, but keep explicit per-domain replay runners.
- **D-02:** The shared primitive boundary includes trace and lineage scaffolding, checkpoint construction, gate summarization, evidence package assembly, publication-plan helper usage, and the orchestration loop skeleton for intake, processing, and identity resolution.
- **D-03:** Domain-specific runner contracts remain explicit for intake service selection, processor selection, enrichment steps, replay asset loading, publication target wiring, rule manifests, and hook-sensitive behavior.
- **D-04:** Phase 3 explicitly rejects a single fully generic replay runner with domain adapters as the primary abstraction target.

### Failure contract
- **D-05:** Adopt a split failure contract: typed exceptions for preflight, config, and setup failures; typed run reports for completed runs that reach replay outcome evaluation.
- **D-06:** The minimum typed run-report fields are `comparison_run_id`, `overall_outcome`, `checkpoint_results`, `primary_failure`, `compatibility_case`, and `evidence_paths`.
- **D-07:** Replay mismatch outcomes must remain distinct from setup failures; Phase 3 must not collapse governed parity differences and invalid-run failures into one undifferentiated object.

### Agent entrypoints
- **D-08:** Keep the current human-facing domain wrappers: `replay-annuity-performance`, `replay-annual-award`, and `replay-annual-loss`.
- **D-09:** Add a unified agent-facing replay CLI v1 surface: `replay run --domain <domain> --workbook <path> --period <period>`, `replay diagnose --comparison-run-id <id>`, and `replay list-domains`.
- **D-10:** The minimum agent-facing output contract is `comparison_run_id`, `overall_outcome`, `primary_failed_checkpoint`, `evidence_root`, and `compatibility_case_id`.

### Temporary identity policy
- **D-11:** Replace `TEMP-{company_name}` with a deterministic opaque temp-identity contract.
- **D-12:** Use the legacy deterministic generation model as the reference: normalize before hashing, use HMAC-based deterministic generation with governed salt, and keep the generated `company_id` opaque.
- **D-13:** Allow one governed global temp-id prefix setting, default it to `IN`, and treat the prefix as a config-release compatibility parameter rather than a runtime convenience toggle.
- **D-14:** Empty or placeholder names return `None` instead of generating a shared fake temp id.
- **D-15:** Raw company names remain in sidecar evidence only; they must not appear in `company_id`.
- **D-16:** Recommended helper boundary for fallback identity is `generate_temp_identity(...)`, `is_temp_identity(...)`, `normalize_identity_fallback_input(...)`, and `temp_identity_prefix()`.

### the agent's Discretion
- Exact names and module locations for extracted replay primitive helpers, provided the shared-versus-explicit boundary above remains visible.
- Final typed exception class names and final CLI presentation formatting, provided the locked failure and output contracts above are preserved.
- Exact sequencing for updating tests, runbooks, and config wiring during implementation, provided compatibility-sensitive temp-id and replay-entrypoint behavior remain governed.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Phase scope and locked decisions
- `.planning/ROADMAP.md` — Phase 3 goal, scope, risks, and success criteria.
- `.planning/REQUIREMENTS.md` — `PIPE-03`, `PIPE-04`, `OPS-01`, and `GOV-02` acceptance targets.
- `.planning/PROJECT.md` — parity-first, agent-operable, and transparency constraints that Phase 3 must preserve.
- `.planning/phases/02-transparent-pipeline-contracts-parity-gates/02-CONTEXT.md` — locked Phase 2 gate, adjudication, and evidence-shape decisions that Phase 3 must carry forward.
- `docs/gsd/grey-areas/2026-04-13-phase3-gray-area-decisions.md` — user-confirmed Phase 3 decision baseline for all four gray areas.
- `docs/gsd/reviews/2026-04-13-phase3-gray-area-governance-review.md` — supporting rationale, option boundary, and admission requirements behind the Phase 3 decision baseline.

### Architecture and program guardrails
- `docs/superpowers/specs/2026-04-11-workdatahubpro-rebuild-architecture-draft.md` — capability-first boundaries, identity-resolution contract, publication boundary, and replay/orchestration guardrails.
- `docs/superpowers/specs/2026-04-11-workdatahubpro-refactor-program.md` — first-wave program boundaries, deferred runtime/operator surfaces, and operator-entrypoint governance.
- `docs/superpowers/specs/2026-04-11-workdatahubpro-first-wave-legacy-coverage-matrix.md` — deferred cross-domain/runtime rows that Phase 3 must not silently absorb.

### Runtime reality and operator surface
- `.planning/codebase/CONCERNS.md` — current duplication, fragile failure surfaces, and temp-id leakage concerns that Phase 3 is intended to reduce.
- `docs/runbooks/annuity-performance-replay.md` — existing domain-specific replay wrapper and expected operator-facing output.
- `docs/runbooks/annual-award-replay.md` — existing domain-specific replay wrapper and accepted replay-root contract.
- `docs/runbooks/annual-loss-replay.md` — existing domain-specific replay wrapper and evidence-path expectations.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `src/work_data_hub_pro/apps/orchestration/replay/annuity_performance_slice.py`, `src/work_data_hub_pro/apps/orchestration/replay/annual_award_slice.py`, and `src/work_data_hub_pro/apps/orchestration/replay/annual_loss_slice.py`: current explicit per-domain runners already share a strong orchestration skeleton suitable for primitive extraction.
- `src/work_data_hub_pro/apps/etl_cli/main.py`: current domain wrapper commands are the baseline human-facing entrypoints that Phase 3 should retain.
- `src/work_data_hub_pro/governance/compatibility/gate_models.py` and `src/work_data_hub_pro/governance/adjudication/service.py`: existing gate and compatibility-case models are the natural base for the typed run-report boundary.
- `src/work_data_hub_pro/platform/publication/service.py` and `src/work_data_hub_pro/platform/contracts/publication.py`: current publication error/result surface shows where typed setup failures and typed run-report integration need to land.
- `src/work_data_hub_pro/capabilities/identity_resolution/service.py`: current cache/provider/fallback flow is the direct insertion point for governed opaque temp-id helpers.

### Established Patterns
- Accepted replay slices already keep operator-facing runbooks, replay roots, and wrappers domain-specific; Phase 3 should preserve that clarity.
- Replay slices share orchestration mechanics, but domain-specific asset loading, enrichment, and publication targets are materially different and must stay visible.
- Phase 2 already distinguishes run-completed parity mismatches from structural gate/setup semantics; Phase 3 should refine that distinction, not erase it.
- Business semantics belong in capability services, not in generic orchestration adapters or callbacks.

### Integration Points
- `src/work_data_hub_pro/apps/orchestration/replay/` for extracting shared replay primitives while preserving explicit per-domain runners.
- `src/work_data_hub_pro/apps/etl_cli/main.py` for the unified agent-facing replay layer on top of existing wrappers.
- `src/work_data_hub_pro/capabilities/identity_resolution/` plus governed config/release surfaces for deterministic temp-id generation and compatibility-controlled prefix handling.
- `docs/runbooks/` and replay-focused tests under `tests/replay/`, `tests/integration/`, and `tests/contracts/` for entrypoint, diagnostics, and temp-id contract validation.

</code_context>

<specifics>
## Specific Ideas

- "shared primitives, explicit runners" is the governing replay-composition posture.
- The replay surface should have dual entrypoints: stable domain wrappers for humans and runbooks, plus `replay run` / `replay diagnose` / `replay list-domains` for agents.
- The temp-id contract should preserve operator familiarity with `IN*` while preventing raw-name leakage in `company_id`.
- Typed diagnostics should separate "run could not start correctly" from "run completed and found a governed mismatch".

</specifics>

<deferred>
## Deferred Ideas

- Legacy-style replay/ETL execution parity such as `--all-domains`, file discovery controls, and DB diagnostics.
- Full `etl`, `operator`, and `adjudication` command trees beyond the replay CLI v1 surface.
- Final retain-or-replace decisions for `company_lookup_queue`, `reference_sync`, and manual `customer-mdm` surfaces.
- Broader future-domain generalization beyond first-wave needs, including treating `annuity_income` as a proof point for a fully generic replay runner.

</deferred>

---

*Phase: 03-orchestration-refactor-failure-explainability*
*Context gathered: 2026-04-13*

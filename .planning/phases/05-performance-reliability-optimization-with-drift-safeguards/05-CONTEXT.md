# Phase 5: Performance Reliability Optimization with Drift Safeguards - Context

**Gathered:** 2026-04-19
**Status:** Ready for planning

<domain>
## Phase Boundary

Phase 5 closes out v1 by addressing the confirmed performance and reliability bottlenecks recorded in `.planning/codebase/CONCERNS.md` without introducing semantic drift against legacy parity baselines. Scope is strictly limited to the three roadmap requirements PERF-01, PERF-02, PERF-03:

- PERF-01 — Optimize the two named hotspots (`contract_state._has_match` linear scan and `in_memory_trace_store.find` linear scan) and prove parity stability around the change.
- PERF-02 — Replace `KeyError`-prone publication policy access with schema-validated load and typed errors; surface partial-execution failure semantics.
- PERF-03 — Stand up an explicit, repeatable workload-tiered verification matrix (contract / integration / replay / performance) and wire it to the existing PR / protected-branch / nightly gate tiers.

Out of scope: persistent storage / queue runtime adapters (v2 RUN-01/02), additional publication channels (v2 RUN-03), operator dashboards (v2 UX-01), broader profile-driven hot-path scanning beyond the two CONCERNS-listed hotspots, and any rewrite of replay orchestration primitives delivered in Phase 3.

</domain>

<decisions>
## Implementation Decisions

### PERF-01 — Hotspot optimization scope and indexing
- **D-01:** Optimization scope is hard-locked to the two hotspots already named in `.planning/codebase/CONCERNS.md` — `capabilities/projections/contract_state.py::_has_match` and `platform/tracing/in_memory_trace_store.py::find`. Phase 5 will not opportunistically scan for additional hot paths; new hotspots discovered later belong in a follow-on phase.
- **D-02:** Replace the two linear scans with pre-built dict/set indexes: `set[(company_id, plan_code, period)]` for projection membership; `dict[(batch_id, anchor_row_no), list[event]]` for trace lookup. No `lru_cache` memoization layer; no store-level invalidation API.
- **D-03:** Apply changes in-place inside the existing functions/methods. Do not introduce a parallel `IndexedTraceStore` adapter, do not add a runtime feature-flag, do not change public signatures. Keeps capability-first boundaries flat and consistent with the project guideline to avoid speculative abstractions.
- **D-04:** Index lifecycle is build-once-at-call-site: build on first invocation per call (or per store snapshot), then read-only for the duration of that call. Matches the batch-oriented nature of replay runs and avoids touching any write path.

### PERF-01 ↔ Parity — Drift-safety harness
- **D-05:** Primary drift-safety mechanism is the existing replay acceptance suite under `tests/replay/` (annuity_performance / annual_award / annual_loss + Phase 02.1 fail-closed baselines). Each PERF-01 optimization commit must be green against the full replay suite before it lands. No new bespoke parity harness is added.
- **D-06:** Each hotspot optimization lands as its own atomic commit so any future regression can be reverted at hotspot granularity. No `_legacy()` shim functions in source; no runtime feature flag (consistent with D-03).
- **D-07:** If any micro-level oracle test is added during planning/execution to spot-check a hotspot, the convention is precomputed `(input, expected_output)` fixtures committed under `reference/perf-baselines/` — never retain a `_legacy()` dual implementation in source code.
- **D-08:** Conflict resolution authority: replay acceptance suite + Phase 02.1 deterministic baselines are the final arbiter. If any micro oracle test disagrees with the replay suite, the oracle/fixture is treated as suspect and re-derived; the replay suite verdict stands.

### PERF-02 — Publication policy validation and failure semantics
- **D-09:** Replace raw `payload[domain]` / `policy.targets[target_name]` access with a Pydantic v2 model for the publication policy file. Aligns with the existing Pydantic-based contracts under `platform/contracts/`.
- **D-10:** Typed error surface is a small four-class hierarchy under a common `PublicationPolicyError` base: `PolicyFileMissingError`, `PolicyParseError`, `UnknownDomainError`, `UnknownTargetError`. Mirrors the typed-diagnostic style established in Phase 3.
- **D-11:** Validation is performed at load time (`load_publication_policy`) — fail-fast on file absence, parse failure, and structural validation. `build_publication_plan` performs lookup-only validation (`UnknownTargetError`) at use time. Two-layer pattern keeps startup loud and per-build cheap.
- **D-12:** `PublicationService.execute` becomes fail-fast: on the first bundle-level failure, raise a typed `PublicationExecutionError` carrying the offending bundle and stop processing remaining bundles. This matches the `InMemoryTableStore`'s lack of transactional rollback semantics. The `success=True` literal currently set in `PublicationResult` must be replaced with a real success/failure value populated by execute logic, with regression tests proving the typed error path.
- **D-13:** Negative-path test coverage for unknown policy domain, unknown target, malformed policy file, and mid-bundle execution failure is in scope and lives under `tests/integration/test_publication_service.py` (the file already named in CONCERNS.md).

### PERF-03 — Verification matrix and benchmark governance
- **D-14:** Workload tiering is three levels — `smoke`, `standard`, `large`. `smoke` = small per-domain probe sufficient for fast feedback; `standard` = the existing replay acceptance suite over the three slices; `large` = multi-period / multi-year stress that exercises memory and trace-volume scaling.
- **D-15:** Tier-to-gate mapping uses the existing CI tiering from Phase 2: `smoke` runs on PR, `standard` runs on protected-branch merges, `large` runs nightly. No new gate tier is invented; existing tier owners stay accountable.
- **D-16:** Performance baselines live under `reference/perf-baselines/` as JSON (per-tier, per-target metrics: at minimum p50/p95 wall-clock and peak resident memory). Regression thresholds are expressed as relative ratios (e.g. "must not exceed baseline × 1.20") rather than absolute milliseconds, so machine variance does not produce false regressions. Mirrors the `reference/historical_replays/` baseline-asset convention from Phase 1.
- **D-17:** The verification matrix has two committed surfaces: a Markdown matrix table in `docs/runbooks/` documenting tier × suite × cadence × baseline, plus an executable `scripts/run_perf_matrix.py` (or equivalent under `src/work_data_hub_pro/apps/`) that runs a chosen tier locally and on CI. Pytest markers are not used as the primary tier mechanism; the script is the authoritative dispatcher.

### Claude's Discretion
- Exact Pydantic model field names and base error class location (`platform/publication/errors.py` vs inline in `service.py`), provided the four typed errors and the `PublicationPolicyError` base exist and are importable.
- Exact metric set inside `reference/perf-baselines/*.json` beyond the required p50/p95 wall-clock and peak memory; additional per-target metrics may be added if useful.
- Exact placement of `run_perf_matrix.py` (top-level `scripts/` vs `apps/etl_cli/` subcommand), provided it is invokable from a documented runbook command.
- Exact implementation of "build-once" inside the two hotspots (helper function vs inline dict comprehension), provided the resulting public function signatures and behavior are unchanged.
- Whether to add an internal micro oracle test alongside `tests/performance/test_trace_lookup_micro_benchmark.py`; if added, must follow D-07 convention.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Phase scope and acceptance
- `.planning/ROADMAP.md` — Phase 5 goal, scope, requirements, success criteria.
- `.planning/REQUIREMENTS.md` — `PERF-01`, `PERF-02`, `PERF-03` acceptance targets.
- `.planning/PROJECT.md` — current validated constraints, parity guarantees, and project state after Phase 04 completion.
- `.planning/STATE.md` — current workflow state and recent execution notes.

### Prior phase decisions that constrain Phase 5
- `.planning/phases/02-transparent-pipeline-contracts-parity-gates/02-CONTEXT.md` — deterministic parity gates, comparator semantics, CI tiering that PERF-03 builds on.
- `.planning/phases/03-orchestration-refactor-failure-explainability/03-CONTEXT.md` — typed-diagnostic and replay-entrypoint conventions that PERF-02 typed errors must follow.
- `.planning/phases/04-agent-operations-governance-hardening/04-CONTEXT.md` — file-backed evidence baseline and lineage helpers that constrain how PERF-01 changes interact with trace lookup.
- `.planning/phases/02.1-phase-2-governance-remediation-truthful-gates-and-status-sync/02.1-CONTEXT.md` — Phase 02.1 truthful baseline contracts that the replay acceptance suite (D-05) depends on; do not weaken.

### Architecture and concerns
- `docs/superpowers/specs/2026-04-11-workdatahubpro-rebuild-architecture-draft.md` — capability/platform/governance/app boundaries and trace/evidence invariants Phase 5 must preserve.
- `.planning/codebase/CONCERNS.md` — authoritative source for the two PERF-01 hotspots, the PERF-02 publication fragility, and the test-coverage gaps in scope.
- `.planning/codebase/STRUCTURE.md` — current source tree; informs where helpers and `run_perf_matrix.py` belong.
- `.planning/codebase/TESTING.md` — existing contract / integration / replay / performance boundary patterns that PERF-03 matrix consumes.

### Code anchors
- `src/work_data_hub_pro/capabilities/projections/contract_state.py` — `_has_match` hotspot target for D-02 indexing.
- `src/work_data_hub_pro/platform/tracing/in_memory_trace_store.py` — `find()` hotspot target for D-02 indexing.
- `src/work_data_hub_pro/platform/publication/service.py` — `load_publication_policy`, `build_publication_plan`, and `PublicationService.execute` are the PERF-02 surfaces.
- `src/work_data_hub_pro/platform/contracts/publication.py` — existing `PublicationMode`, `PublicationPlan`, `PublicationResult` shape that the typed errors and revised `success` field must remain compatible with.
- `config/policies/publication.json` — current policy file structure that the Pydantic v2 model in D-09 must accept.
- `tests/integration/test_publication_service.py` — target file for D-13 negative-path tests.
- `tests/performance/test_trace_lookup_micro_benchmark.py` — existing performance-suite anchor; D-14 / D-17 extend this boundary.
- `reference/historical_replays/` — convention reference for the new `reference/perf-baselines/` directory introduced in D-16.

### Discipline references
- `docs/disciplines/implementation-execution.md` — execution rules for Phase 5 implementation tasks.
- `docs/disciplines/implementation-toolchain.md` — `uv` usage, lockfile, and command style for any new scripts under D-17.
- `docs/disciplines/implementation-verification.md` — full-suite verification expectations that the verification matrix (PERF-03) operationalizes.
- `docs/disciplines/git-workflow.md` — commit/branch policy for the per-hotspot commit cadence in D-06.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `platform/contracts/` already centralizes Pydantic v2 typed contracts for the project; `PublicationPolicy` Pydantic model (D-09) belongs in or adjacent to this module.
- `tests/replay/` contains the deterministic replay acceptance suite for the three slices and the Phase 02.1 fail-closed baseline machinery. D-05 reuses this directly — no new harness required.
- `tests/performance/test_trace_lookup_micro_benchmark.py` is the existing performance-suite anchor; the verification matrix (D-14/D-17) extends rather than replaces it.
- `reference/historical_replays/` already establishes the "baseline assets in `reference/`" convention; `reference/perf-baselines/` (D-16) follows the same shape.
- The replay acceptance suite already exercises both `_has_match` (via projection comparison) and `find` (via trace lookup) on real per-slice data, which is what makes D-05 sufficient as the parity guarantor without a new harness.

### Established Patterns
- Typed diagnostics via dedicated exception hierarchies (Phase 3 pattern) — D-10's four-class hierarchy follows this.
- Validate-at-boundary, never inside domain logic (Phase 4 pattern) — D-11's load-time validation aligns.
- File-backed evidence and reference assets are the operational baseline (Phase 4 D-06) — `reference/perf-baselines/` keeps this discipline.
- Per-commit atomic landing with parity gates (Phase 2/3) — D-06's per-hotspot commit cadence aligns.
- CI tiering is fixed at PR / protected-branch / nightly (Phase 2) — D-15 maps onto this without inventing new tiers.

### Integration Points
- `capabilities/projections/contract_state.py` — surgical change to `_has_match`; no signature change.
- `platform/tracing/in_memory_trace_store.py` — surgical change to `find`; no signature change.
- `platform/publication/service.py` — three-touch surface (`load_publication_policy`, `build_publication_plan`, `PublicationService.execute`).
- `platform/contracts/` (or `platform/publication/errors.py`) — home for new `PublicationPolicyError` hierarchy.
- `tests/integration/test_publication_service.py` — D-13 negative-path coverage.
- `tests/performance/` — extended by D-14/D-17.
- `reference/perf-baselines/` — new directory introduced by D-16; mirror `reference/historical_replays/` in shape and governance.
- `docs/runbooks/` — new Markdown verification matrix and any per-tier execution guidance (D-17).
- `scripts/` (or `apps/etl_cli/` subcommand) — `run_perf_matrix.py` dispatcher (D-17).

</code_context>

<specifics>
## Specific Ideas

- The shape of Phase 5 should read as "two surgical optimizations, one publication-fragility fix, one verification matrix" — four narrow strands, no scope creep.
- Replay acceptance suite is the single source of truth for parity. Anything that disagrees with it is wrong (D-08).
- Typed errors and Pydantic models follow the project's established style; do not invent a new exception base or schema framework.
- Performance baselines must be relative-threshold so machine variance does not produce false regressions; absolute-millisecond gates are explicitly rejected.
- The verification matrix is a documented, executable artifact — both the human-readable Markdown matrix and the dispatcher script must exist and stay in sync.

</specifics>

<deferred>
## Deferred Ideas

- Persistent / pluggable storage, tracing, and evidence adapters beyond in-memory and file-backed — v2 RUN-01.
- Queue / retry runtime for large replay backlogs — v2 RUN-02.
- Additional publication channels and operational policy controls beyond the current shape — v2 RUN-03.
- Operator-facing dashboards for replay status, parity trend, and bottleneck diagnostics — v2 UX-01.
- Profile-driven hot-path scanning for additional optimization candidates beyond the two CONCERNS-listed hotspots — future phase, requires its own discuss/plan cycle.
- Best-effort rollback / true transactional semantics in `PublicationService.execute` — depends on a real transactional storage adapter (v2 RUN-01); explicitly out of Phase 5.
- Profile-driven verification-asset rows for `golden_set`, `golden_baseline`, `real_data_sample`, and dedicated error-case fixtures — Phase 2 carry-forward, remains deferred.

</deferred>

---

*Phase: 05-performance-reliability-optimization-with-drift-safeguards*
*Context gathered: 2026-04-19*

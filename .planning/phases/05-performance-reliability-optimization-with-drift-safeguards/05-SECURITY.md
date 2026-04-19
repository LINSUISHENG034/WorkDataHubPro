---
phase: 05
slug: performance-reliability-optimization-with-drift-safeguards
status: verified
threats_open: 0
asvs_level: 1
created: 2026-04-19
---

# Phase 05 — Security

> Per-phase security contract: threat register, accepted risks, and audit trail.

---

## Trust Boundaries

| Boundary | Description | Data Crossing |
|----------|-------------|---------------|
| fact / fixture rows -> projection membership logic | Index construction must preserve fact-hit versus fixture-hit booleans. | Canonical fact rows and fixture rows keyed by `company_id`, `plan_code`, and `period` |
| projection hotspot optimization -> replay parity gates | A faster membership path must not drift from accepted replay outputs. | Projection rows and replay snapshot comparisons |
| trace-event store snapshot -> lazy lookup index | Read-path indexing must preserve the current `_events` snapshot and refresh safely after later appends. | `FieldTraceEvent` collections keyed by `batch_id` and `anchor_row_no` |
| trace-event store -> explainability consumers | Faster lookup must not reorder or drop trace events that replay diagnostics depend on. | Explainability evidence retrieved by `batch_id + anchor_row_no` |
| publication policy file -> validated runtime contract | File absence, malformed JSON, or structural drift must fail before execution starts. | `config/policies/publication.json` payloads |
| publication target selection -> publication plan | Unknown targets must fail with typed errors instead of raw lookup failures. | Publication target names, plan fields, and transaction metadata |
| bundle execution -> publication results | A failing write must not be reported as success and must stop later bundles. | `PublicationPlan` bundles and `PublicationResult` outcomes |
| runbook matrix -> CI/local execution | Documented tiers must stay aligned with the dispatcher and baselines. | Tier names, cadence mapping, and dispatcher commands |
| committed baseline assets -> perf pass/fail behavior | Baselines must encode relative-threshold semantics clearly enough to enforce consistently. | `reference/perf-baselines/*.json` metric values and `threshold_ratio` |
| dispatcher surface -> project toolchain | The perf matrix must remain executable through repo-native commands. | `uv run python scripts/run_perf_matrix.py --tier ...` CLI surface |

---

## Threat Register

| Threat ID | Category | Component | Disposition | Mitigation | Status |
|-----------|----------|-----------|-------------|------------|--------|
| T-05-01 | T | contract-state membership logic | mitigate | Tuple-key membership lookup is implemented in `src/work_data_hub_pro/capabilities/projections/contract_state.py`, and exact boolean combinations are frozen by `tests/performance/test_contract_state_projection_benchmark.py` and `tests/integration/test_projection_outputs.py`. | closed |
| T-05-02 | R | parity drift after optimization | mitigate | Replay acceptance proof was rerun on 2026-04-19 with `uv run pytest tests/replay/test_annuity_performance_slice.py tests/replay/test_annual_award_slice.py tests/replay/test_annual_loss_slice.py -v`. | closed |
| T-05-03 | T | lazy trace read-path indexing | mitigate | Read-path-only keyed lookup remains in `src/work_data_hub_pro/platform/tracing/in_memory_trace_store.py`, with freshness and ordering frozen by `tests/performance/test_trace_lookup_micro_benchmark.py` and `tests/contracts/test_trace_lineage_runtime.py`. | closed |
| T-05-04 | R | explainability ordering drift | mitigate | Explainability replay proof was rerun on 2026-04-19 with `uv run pytest tests/replay/test_annuity_performance_explainability_slo.py tests/replay/test_annual_award_explainability_slo.py tests/replay/test_annual_loss_explainability_slo.py -v`. | closed |
| T-05-05 | R | publication policy loading | mitigate | Typed file, parse, and unknown-domain failures are implemented in `src/work_data_hub_pro/platform/publication/service.py` and exercised by `tests/integration/test_publication_service.py`. | closed |
| T-05-06 | T | bundle execution truthfulness | mitigate | Stop-on-first-failure behavior and `PublicationExecutionError` are implemented in `src/work_data_hub_pro/platform/publication/service.py` and exercised by `tests/integration/test_publication_service.py`. | closed |
| T-05-07 | R | perf matrix governance surface | mitigate | The runbook, dispatcher, and committed baseline assets are frozen by `tests/contracts/test_perf_matrix_contracts.py` and live in `docs/runbooks/performance-verification-matrix.md`, `scripts/run_perf_matrix.py`, and `reference/perf-baselines/`. | closed |

*Status: open · closed*
*Disposition: mitigate (implementation required) · accept (documented risk) · transfer (third-party)*

---

## Accepted Risks Log

| Risk ID | Threat Ref | Rationale | Accepted By | Date |
|---------|------------|-----------|-------------|------|

No accepted risks.

---

## Verification Evidence

- No `## Threat Flags` sections were present in `05-01-SUMMARY.md` through `05-04-SUMMARY.md`.
- `uv run pytest tests/performance/test_contract_state_projection_benchmark.py tests/integration/test_projection_outputs.py -v`
- `uv run pytest tests/replay/test_annuity_performance_slice.py tests/replay/test_annual_award_slice.py tests/replay/test_annual_loss_slice.py -v`
- `uv run pytest tests/performance/test_trace_lookup_micro_benchmark.py tests/contracts/test_trace_lineage_runtime.py -v`
- `uv run pytest tests/replay/test_annuity_performance_explainability_slo.py tests/replay/test_annual_award_explainability_slo.py tests/replay/test_annual_loss_explainability_slo.py -v`
- `uv run pytest tests/integration/test_publication_service.py -v`
- `uv run pytest tests/contracts/test_perf_matrix_contracts.py -v`

---

## Security Audit Trail

| Audit Date | Threats Total | Closed | Open | Run By |
|------------|---------------|--------|------|--------|
| 2026-04-19 | 7 | 7 | 0 | Codex |

---

## Sign-Off

- [x] All threats have a disposition (mitigate / accept / transfer)
- [x] Accepted risks documented in Accepted Risks Log
- [x] `threats_open: 0` confirmed
- [x] `status: verified` set in frontmatter

**Approval:** verified 2026-04-19

---
phase: 05
slug: performance-reliability-optimization-with-drift-safeguards
status: ready
nyquist_compliant: true
wave_0_complete: true
created: 2026-04-19
---

# Phase 05 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | `pytest 8.4.2` via `uv run pytest` |
| **Config file** | `pyproject.toml` |
| **Quick run command** | `uv run python scripts/run_perf_matrix.py --tier smoke` |
| **Full suite command** | `uv run pytest -v` |
| **Estimated runtime** | ~2 seconds for `smoke`; full suite varies with planning-contract scope |

---

## Sampling Rate

- **After every task commit:** Run the narrowest plan-specific pytest command from the table below.
- **After every plan wave:** Run `uv run python scripts/run_perf_matrix.py --tier smoke`.
- **Before `/gsd-verify-work`:** Run `uv run pytest -v`.
- **Max feedback latency:** ~2 seconds for smoke-tier feedback.

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 05-01-01 | 01 | 1 | PERF-01 | T-05-01 / T-05-02 | Contract-state projection preserves exact fact/fixture membership semantics while replacing repeated linear scans with pre-built membership indexes. | integration + performance + replay | `uv run pytest tests/performance/test_contract_state_projection_benchmark.py tests/integration/test_projection_outputs.py tests/replay/test_annuity_performance_slice.py tests/replay/test_annual_award_slice.py tests/replay/test_annual_loss_slice.py -v` | ✅ | ✅ green |
| 05-02-01 | 02 | 1 | PERF-01 | T-05-03 / T-05-04 | Trace lookup preserves exact `event_seq` ordering and anchor-based retrieval while avoiding repeated full-store linear scans. | contract + performance + replay | `uv run pytest tests/performance/test_trace_lookup_micro_benchmark.py tests/contracts/test_trace_lineage_runtime.py tests/replay/test_annuity_performance_explainability_slo.py tests/replay/test_annual_award_explainability_slo.py tests/replay/test_annual_loss_explainability_slo.py -v` | ✅ | ✅ green |
| 05-03-01 | 03 | 1 | PERF-02 | T-05-05 / T-05-06 | Publication policy loading and execution fail with typed, actionable errors instead of `KeyError` or false-success results. | integration | `uv run pytest tests/integration/test_publication_service.py -v` | ✅ | ✅ green |
| 05-04-01 | 04 | 2 | PERF-03 | T-05-07 | Matrix doc, dispatcher script, and committed perf baselines stay synchronized across `smoke`, `standard`, and `large` tiers. | contract + dispatcher | `uv run python scripts/run_perf_matrix.py --tier smoke` | ✅ | ✅ green |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [x] `tests/performance/test_contract_state_projection_benchmark.py` — contract-state hotspot benchmark and semantic fixture proof
- [x] `tests/contracts/test_trace_lineage_runtime.py` — lazy-index ordering and refresh proof for trace lookup
- [x] `tests/contracts/test_perf_matrix_contracts.py` — matrix doc / dispatcher / baseline asset drift protection
- [x] `reference/perf-baselines/smoke.json` — PR-tier baseline asset
- [x] `reference/perf-baselines/standard.json` — protected-branch baseline asset
- [x] `reference/perf-baselines/large.json` — nightly stress baseline asset
- [x] `docs/runbooks/performance-verification-matrix.md` — human-readable tier matrix
- [x] `scripts/run_perf_matrix.py` — authoritative perf-tier dispatcher

*Existing infrastructure covers the framework and runner requirements; Wave 0 for Phase 05 is complete.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Baseline ratios remain sensible on the local machine and are not obviously distorted by transient environment noise. | PERF-03 | Contract tests can prove files, commands, and thresholds exist, but cannot judge whether a newly captured baseline is operationally credible on the machine that generated it. | Run `uv run python scripts/run_perf_matrix.py --tier smoke` and `uv run python scripts/run_perf_matrix.py --tier standard`, compare the emitted metrics with `reference/perf-baselines/*.json`, and confirm the chosen relative thresholds remain plausible before updating committed baselines. |

---

## Validation Audit 2026-04-19

| Metric | Count |
|--------|-------|
| Gaps found | 0 |
| Resolved | 0 |
| Escalated | 0 |

No Nyquist validation gaps were found. The existing Phase 05 validation surface already covered every completed requirement; this audit corrected stale draft metadata and recorded current evidence.

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or existing test infrastructure support
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all missing verification references
- [x] No watch-mode flags
- [x] Feedback latency < 240s
- [x] `nyquist_compliant: true` set in frontmatter

---

## Recorded Evidence

- `uv run pytest tests/performance/test_contract_state_projection_benchmark.py tests/integration/test_projection_outputs.py tests/replay/test_annuity_performance_slice.py tests/replay/test_annual_award_slice.py tests/replay/test_annual_loss_slice.py -v` — passed (`14 passed`)
- `uv run pytest tests/performance/test_trace_lookup_micro_benchmark.py tests/contracts/test_trace_lineage_runtime.py tests/replay/test_annuity_performance_explainability_slo.py tests/replay/test_annual_award_explainability_slo.py tests/replay/test_annual_loss_explainability_slo.py -v` — passed (`8 passed`)
- `uv run pytest tests/integration/test_publication_service.py tests/contracts/test_perf_matrix_contracts.py -v` — passed (`12 passed`)
- `uv run python scripts/run_perf_matrix.py --tier smoke` — passed; emitted `p50=0.7459259000024758`, `p95=0.7459259000024758`, `peak_memory=69.0`
- `uv run pytest -v` — failed on `tests/contracts/test_phase2_governance_status_sync.py::{test_phase2_status_sync_across_project_phase6_artifacts,test_phase6_roadmap_entry_has_three_plans,test_requirements_keep_dated_phase6_reverification_note}` because the current `.planning/ROADMAP.md` and `.planning/REQUIREMENTS.md` no longer satisfy those repository-wide Phase 6 governance-doc expectations

**Approval:** audited 2026-04-19 (Nyquist-compliant; repository full suite currently blocked by unrelated Phase 6 planning drift)

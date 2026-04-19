---
phase: 05
slug: performance-reliability-optimization-with-drift-safeguards
status: draft
nyquist_compliant: true
wave_0_complete: false
created: 2026-04-19
---

# Phase 05 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | `pytest 8.4.x` via `uv run pytest` |
| **Config file** | `pyproject.toml` |
| **Quick run command** | `uv run pytest tests/integration/test_publication_service.py tests/performance/test_trace_lookup_micro_benchmark.py tests/performance/test_contract_state_projection_benchmark.py tests/contracts/test_perf_matrix_contracts.py -v` |
| **Full suite command** | `uv run pytest -v` |
| **Estimated runtime** | ~240 seconds |

---

## Sampling Rate

- **After every task commit:** Run the narrowest plan-specific pytest command from the table below.
- **After every plan wave:** Run the quick run command above.
- **Before `/gsd-verify-work`:** `uv run pytest -v`
- **Max feedback latency:** 240 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 05-01-01 | 01 | 1 | PERF-01 | T-05-01 / T-05-02 | Contract-state projection preserves exact fact/fixture membership semantics while replacing repeated linear scans with pre-built membership indexes. | integration + performance + replay | `uv run pytest tests/performance/test_contract_state_projection_benchmark.py tests/replay/test_annuity_performance_slice.py tests/replay/test_annual_award_slice.py tests/replay/test_annual_loss_slice.py -v` | ❌ W0 | ⬜ pending |
| 05-02-01 | 02 | 1 | PERF-01 | T-05-03 / T-05-04 | Trace lookup preserves exact `event_seq` ordering and anchor-based retrieval while avoiding repeated full-store linear scans. | contract/integration + performance + replay | `uv run pytest tests/performance/test_trace_lookup_micro_benchmark.py tests/replay/test_annuity_performance_explainability_slo.py tests/replay/test_annual_award_explainability_slo.py tests/replay/test_annual_loss_explainability_slo.py -v` | ✅ partial / ❌ W0 extension | ⬜ pending |
| 05-03-01 | 03 | 1 | PERF-02 | T-05-05 / T-05-06 | Publication policy loading and execution fail with typed, actionable errors instead of `KeyError` or false-success results. | integration | `uv run pytest tests/integration/test_publication_service.py -v` | ✅ exists / ❌ negative paths | ⬜ pending |
| 05-04-01 | 04 | 2 | PERF-03 | T-05-07 | Matrix doc, dispatcher script, and committed perf baselines stay synchronized across `smoke`, `standard`, and `large` tiers. | contract | `uv run pytest tests/contracts/test_perf_matrix_contracts.py -v` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `tests/performance/test_contract_state_projection_benchmark.py` — contract-state hotspot benchmark and semantic fixture proof
- [ ] `tests/contracts/test_perf_matrix_contracts.py` — matrix doc / dispatcher / baseline asset drift protection
- [ ] `reference/perf-baselines/smoke.json` — PR-tier baseline asset
- [ ] `reference/perf-baselines/standard.json` — protected-branch baseline asset
- [ ] `reference/perf-baselines/large.json` — nightly stress baseline asset
- [ ] `docs/runbooks/performance-verification-matrix.md` — human-readable tier matrix
- [ ] `scripts/run_perf_matrix.py` — authoritative perf-tier dispatcher

*Existing infrastructure covers the framework and runner requirements; Wave 0 is only new test-module and asset creation.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Baseline ratios remain sensible on the local machine and are not obviously distorted by transient environment noise. | PERF-03 | Contract tests can prove files, commands, and thresholds exist, but cannot judge whether a newly captured baseline is operationally credible on the machine that generated it. | Run `uv run python scripts/run_perf_matrix.py --tier smoke` and `uv run python scripts/run_perf_matrix.py --tier standard`, compare the emitted metrics with `reference/perf-baselines/*.json`, and confirm the chosen relative thresholds remain plausible before updating committed baselines. |

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or existing test infrastructure support
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all missing verification references
- [x] No watch-mode flags
- [x] Feedback latency < 240s
- [x] `nyquist_compliant: true` set in frontmatter

**Approval:** pending

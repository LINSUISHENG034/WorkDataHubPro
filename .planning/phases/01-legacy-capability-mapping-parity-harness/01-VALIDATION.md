---
phase: 01
slug: legacy-capability-mapping-parity-harness
status: approved
nyquist_compliant: true
wave_0_complete: true
created: 2026-04-12
---

# Phase 01 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 8.x |
| **Config file** | `pyproject.toml` |
| **Quick run command** | `uv run pytest tests/contracts -v` |
| **Full suite command** | `uv run pytest -v` |
| **Estimated runtime** | ~180 seconds |

---

## Sampling Rate

- **After every task commit:** Run `uv run pytest tests/contracts -v`
- **After every plan wave:** Run `uv run pytest tests/contracts tests/integration tests/replay -v`
- **Before `/gsd-verify-work`:** Full suite must be green (`uv run pytest -v`)
- **Max feedback latency:** 180 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 01-01-03 | 01 | 1 | MAP-01, MAP-02 | T-01-01 / T-01-02 | Mapping artifacts preserve ownership, stage-chain traceability, and source-recognition reviewability | contract | `uv run pytest tests/contracts/test_phase1_mapping_artifacts.py -v` | ✅ | ✅ green |
| 01-02-03 | 02 | 2 | MAP-03 | T-01-04 / T-01-05 / T-01-06 | Rule migration classification and default-to-block severity policy are explicit and auditable | integration | `uv run pytest tests/integration/test_phase1_rule_classification.py -v` | ✅ | ✅ green |
| 01-03-02 | 03 | 2 | PAR-01 | T-01-07 / — | Deep-sample parity comparison is executed against a real replay run and captured in mismatch artifacts | replay | `uv run pytest tests/replay/test_annuity_performance_slice.py -v` | ✅ | ✅ green |
| 01-03-03 | 03 | 2 | PAR-01 | T-01-07 / T-01-08 | Baseline identity, mismatch-report shape, and decision-log linkage are machine-checkable | contract | `uv run pytest tests/contracts/test_phase1_parity_baseline_artifacts.py -v` | ✅ | ✅ green |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [x] `tests/contracts/test_phase1_mapping_artifacts.py` — MAP-01 and MAP-02 artifact schema and stage-chain traceability checks
- [x] `tests/contracts/test_phase1_parity_baseline_artifacts.py` — PAR-01 baseline identity, mismatch-report, and decision-log schema checks
- [x] `tests/integration/test_phase1_rule_classification.py` — MAP-03 classification and severity-policy integrity checks

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Legacy semantic intent equivalence for edge-case records | MAP-03, PAR-01 | Legacy source intent cannot be fully inferred from artifacts alone | Sample 10 high-risk records from `E:\Projects\WorkDataHub` outputs and compare human-readable interpretation vs Pro mapping notes and executed mismatch-report classifications |

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references
- [x] No watch-mode flags
- [x] Feedback latency < 180s
- [x] `nyquist_compliant: true` set in frontmatter

## Recorded Evidence

- `uv run pytest tests/contracts/test_phase1_mapping_artifacts.py -v` — passed
- `uv run pytest tests/integration/test_phase1_rule_classification.py -v` — passed
- `uv run pytest tests/replay/test_annuity_performance_slice.py -v` — passed
- `uv run pytest tests/contracts/test_phase1_parity_baseline_artifacts.py -v` — passed
- `uv run pytest -v` — passed

**Approval:** approved

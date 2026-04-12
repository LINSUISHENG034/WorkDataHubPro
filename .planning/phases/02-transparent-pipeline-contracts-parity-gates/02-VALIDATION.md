---
phase: 02
slug: transparent-pipeline-contracts-parity-gates
status: draft
nyquist_compliant: false
wave_0_complete: true
created: 2026-04-12
---

# Phase 02 - Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 8.x |
| **Config file** | `pyproject.toml` |
| **Quick run command** | `uv run pytest tests/<target> -v` |
| **Full suite command** | `uv run pytest -v` |
| **Estimated runtime** | ~30-90 seconds for targeted checks, longer for full suite |

---

## Sampling Rate

- **After every task commit:** Run the narrowest relevant `uv run pytest tests/<target> -v` command.
- **After every plan wave:** Run `uv run pytest -v`.
- **Before `/gsd-verify-work`:** Full suite must be green.
- **Max feedback latency:** 90 seconds for targeted checks.

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 02-01-01 | 01 | 1 | PIPE-01 / PAR-03 | T-02-01 | checkpoint and adjudication contracts are explicit and machine-readable | contract | `uv run pytest tests/contracts/test_system_contracts.py -v` | ✅ | pending |
| 02-01-02 | 01 | 1 | PAR-03 | T-02-02 | compatibility cases record severity, precedent, and decision status | integration | `uv run pytest tests/integration/test_compatibility_adjudication.py -v` | ✅ | pending |
| 02-02-01 | 02 | 2 | PIPE-01 / PIPE-02 | T-02-03 | intake adaptation is recorded and strict validators stop invalid internal contracts | integration | `uv run pytest tests/integration/test_annuity_performance_* -v` | ❌ W0 | pending |
| 02-02-02 | 02 | 2 | PAR-02 | T-02-04 | annuity performance emits deterministic checkpoint results and failed-gate evidence | replay | `uv run pytest tests/replay/test_annuity_performance_slice.py -v` | ✅ | pending |
| 02-03-01 | 03 | 2 | PAR-02 / PIPE-02 | T-02-05 | event-domain slices emit consistent checkpoint and evidence outputs | replay | `uv run pytest tests/replay/test_annual_award_slice.py tests/replay/test_annual_loss_slice.py -v` | ✅ | pending |
| 02-04-01 | 04 | 3 | PAR-04 | T-02-06 | CI-tier commands map cleanly to PR, protected-branch, and nightly gates | contract | `uv run pytest tests/contracts -v` | ✅ | pending |

*Status: pending / green / red / flaky*

---

## Wave 0 Requirements

- [ ] `tests/contracts/test_phase2_gate_contracts.py` - contract coverage for checkpoint result and evidence manifest shapes
- [ ] `tests/integration/test_phase2_intake_validation.py` - intake adaptation and strict-validator negative paths
- [ ] `tests/replay/test_phase2_gate_evidence.py` - comparison-run evidence package assertions

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| PR / protected-branch / nightly command mapping is understandable to maintainers | PAR-04 | workflow ergonomics and docs clarity are not fully automatable | Review the final Phase 2 runbook or planning docs and confirm the three CI tiers use explicit commands and slice coverage expectations |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all missing references
- [ ] No watch-mode flags
- [ ] Feedback latency < 90s for targeted checks
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending

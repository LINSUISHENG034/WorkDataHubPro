---
phase: 02
slug: transparent-pipeline-contracts-parity-gates
status: draft
nyquist_compliant: false
wave_0_complete: false
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
| 02-01-01 | 01 | 1 | PIPE-01 / PAR-03 | T-02-01 | checkpoint contracts and shared gate-runtime entrypoints are explicit and machine-readable | contract | `uv run pytest tests/contracts/test_system_contracts.py tests/contracts/test_phase2_gate_contracts.py -v` | ❌ W0 | pending |
| 02-01-02 | 01 | 1 | PAR-03 | T-02-02 | compatibility cases record severity, precedent, and checkpoint identity | integration | `uv run pytest tests/integration/test_compatibility_adjudication.py -v` | ✅ | pending |
| 02-02-01 | 02 | 2 | PIPE-01 / PIPE-02 | T-02-04 | intake adaptation is recorded and strict validators stop invalid internal contracts | integration | `uv run pytest tests/integration/test_phase2_intake_validation.py -v` | ❌ W0 | pending |
| 02-02-02 | 02 | 2 | PAR-02 | T-02-05 | annuity performance emits deterministic checkpoint results and failed-gate evidence through the shared runtime | replay | `uv run pytest tests/replay/test_annuity_performance_slice.py tests/replay/test_phase2_annuity_performance_gates.py tests/replay/test_annuity_performance_explainability_slo.py -v` | ❌ W0 | pending |
| 02-03-01 | 03 | 2 | PAR-02 / PIPE-02 | T-02-08 | event-domain slices emit consistent checkpoint names and evidence outputs | replay | `uv run pytest tests/integration/test_phase2_event_intake_validation.py tests/replay/test_annual_award_slice.py tests/replay/test_annual_loss_slice.py tests/replay/test_phase2_event_domain_gates.py -v` | ❌ W0 | pending |
| 02-04-01 | 04 | 3 | PAR-02 / PIPE-02 | T-02-10 | accepted slices expose `reference_derivation` as an explicit deterministic checkpoint | replay | `uv run pytest tests/replay/test_phase2_reference_derivation_gates.py -v` | ❌ W0 | pending |
| 02-04-02 | 04 | 3 | PAR-02 | T-02-11 | verification assets and forgotten mechanisms use explicit status-based governance artifacts | contract | `uv run pytest tests/contracts/test_phase2_verification_assets.py -v` | ❌ W0 | pending |
| 02-05-01 | 05 | 4 | PAR-04 | T-02-13 | CI-tier commands map cleanly to PR, protected-branch, and nightly gates | contract | `uv run pytest tests/contracts/test_phase2_ci_gate_matrix.py -v` | ❌ W0 | pending |

*Status: pending / green / red / flaky*

---

## Wave 0 Requirements

- [ ] `tests/contracts/test_phase2_gate_contracts.py` - contract coverage for checkpoint result and evidence manifest shapes
- [ ] `tests/integration/test_phase2_intake_validation.py` - intake adaptation and strict-validator negative paths
- [ ] `tests/replay/test_phase2_annuity_performance_gates.py` - annuity failed-gate package assertions
- [ ] `tests/integration/test_phase2_event_intake_validation.py` - event-domain intake tolerance and minimum-skeleton paths
- [ ] `tests/replay/test_phase2_event_domain_gates.py` - cross-slice event-domain gate consistency
- [ ] `tests/replay/test_phase2_reference_derivation_gates.py` - explicit derivation-checkpoint coverage
- [ ] `tests/contracts/test_phase2_verification_assets.py` - asset-manifest and forgotten-mechanism governance checks
- [ ] `tests/contracts/test_phase2_ci_gate_matrix.py` - CI gate-tier contract checks

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| PR / protected-branch / nightly command mapping is understandable to maintainers | PAR-04 | workflow ergonomics and docs clarity are not fully automatable | Review the final Phase 2 runbook or planning docs and confirm the three CI tiers use explicit commands and slice coverage expectations |
| Verification-asset manifest and forgotten-mechanism sweep are understandable to reviewers | PAR-02 / PIPE-02 | status clarity and governance readability are not fully automatable | Review the final manifest and sweep output and confirm missing assets or mechanisms are classified explicitly as `accepted`, `deferred`, or `retired` |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all missing references
- [ ] No watch-mode flags
- [ ] Feedback latency < 90s for targeted checks
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending

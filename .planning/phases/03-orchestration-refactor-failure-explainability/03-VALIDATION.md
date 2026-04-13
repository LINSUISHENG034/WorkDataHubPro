---
phase: 03
slug: orchestration-refactor-failure-explainability
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-04-13
---

# Phase 03 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | `pytest 8.4.2` via `uv run pytest` |
| **Config file** | `pyproject.toml` (`addopts = "--basetemp=.pytest_tmp"`) |
| **Quick run command** | `uv run pytest tests/contracts/test_phase2_gate_contracts.py tests/integration/test_identity_resolution.py tests/integration/test_publication_service.py -v` |
| **Full suite command** | `uv run pytest -v` |
| **Estimated runtime** | ~30 seconds for quick runs; full suite varies by replay fixture load |

---

## Sampling Rate

- **After every task commit:** Run the task-matched targeted `uv run pytest ... -v` command from the task acceptance criteria
- **After every plan wave:** Run `uv run pytest -v`
- **Before `/gsd-verify-work`:** Full suite must be green
- **Max feedback latency:** 30 seconds for targeted checks

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 03-01-01 | 01 | 1 | PIPE-03 | T-03-01 | Replay setup/config/path failures return typed replay-specific exceptions instead of raw `FileNotFoundError`, `ValueError`, or `KeyError` leakage | contract + integration | `uv run pytest tests/contracts/test_replay_run_report.py tests/integration/test_replay_setup_failures.py -v` | ❌ W0 | ⬜ pending |
| 03-01-02 | 01 | 1 | PIPE-04 | T-03-02 | Shared replay primitives preserve parity-stable behavior across all three accepted slice runners | replay | `uv run pytest tests/replay/test_annuity_performance_slice.py tests/replay/test_annual_award_slice.py tests/replay/test_annual_loss_slice.py -v` | ✅ / ✅ / ✅ | ⬜ pending |
| 03-02-01 | 02 | 1 | GOV-02 | T-03-03 | Temp IDs are deterministic opaque `IN...` values, placeholder names return `None`, and raw business names never appear in `company_id` | integration | `uv run pytest tests/integration/test_temp_identity_policy.py tests/integration/test_identity_resolution.py -v` | ❌ W0 / ✅ | ⬜ pending |
| 03-03-01 | 03 | 2 | OPS-01 | T-03-04 | `replay run`, `replay diagnose`, and `replay list-domains` expose stable machine-readable outputs and do not rely on hidden working-directory context | CLI contract | `uv run pytest tests/contracts/test_replay_cli_contracts.py tests/contracts/test_replay_diagnose_contracts.py -v` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `tests/contracts/test_replay_run_report.py` — freeze the serializable replay run-report schema and `primary_failure` derivation
- [ ] `tests/contracts/test_replay_cli_contracts.py` — lock `replay run` and `replay list-domains` command outputs
- [ ] `tests/contracts/test_replay_diagnose_contracts.py` — lock `replay diagnose --comparison-run-id` output and missing-run behavior
- [ ] `tests/integration/test_replay_setup_failures.py` — cover typed replay setup/config/path exceptions
- [ ] `tests/integration/test_temp_identity_policy.py` — cover deterministic `IN...` temp IDs, placeholder-to-`None`, and raw-name-free `company_id`

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Phase 3 runbook wording and examples remain aligned with the new dual CLI surface | OPS-01 | The repo has runbook contract tests, but wording quality and command discoverability still need a human pass after command additions | Read `docs/runbooks/annuity-performance-replay.md`, `docs/runbooks/annual-award-replay.md`, and `docs/runbooks/annual-loss-replay.md`; confirm each still exposes a stable human-facing command and points to the same evidence roots after the new `replay` subcommands are introduced |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 30s for targeted checks
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending

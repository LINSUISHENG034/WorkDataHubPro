---
phase: 03
slug: orchestration-refactor-failure-explainability
status: ready
nyquist_compliant: true
wave_0_complete: true
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
| **Quick run command** | `uv run pytest tests/contracts/test_replay_run_report.py tests/contracts/test_replay_diagnose_contracts.py tests/integration/test_temp_identity_policy.py -v` |
| **Full suite command** | `uv run pytest -v` |
| **Estimated runtime** | ~30 seconds for targeted checks; full suite varies by replay fixture load |

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
| 03-01-01 | 01 | 1 | PIPE-03, OPS-01 | T-03-01 / T-03-03 | Replay contracts and domain metadata expose the typed run-report fields plus stable registry metadata and runner dispatch references for all three wrapper commands | contract | `uv run pytest tests/contracts/test_replay_run_report.py -v` | ❌ W0 | ⬜ pending |
| 03-01-02 | 01 | 1 | OPS-01 | T-03-01 | `comparison_run_id` resolves through governed replay roots into structured diagnostics for completed passed, warning, and failed runs without hidden CWD context | contract | `uv run pytest tests/contracts/test_replay_diagnose_contracts.py -v` | ❌ W0 | ⬜ pending |
| 03-01-03 | 01 | 1 | PIPE-03 | T-03-02 | Replay setup, config, and baseline failures raise typed replay setup exceptions instead of leaking raw runtime exceptions | integration | `uv run pytest tests/integration/test_replay_setup_failures.py -v` | ❌ W0 | ⬜ pending |
| 03-02-01 | 02 | 1 | GOV-02 | T-03-04 / T-03-05 | Temp-id generation is deterministic, opaque, HMAC-based, prefix-governed, and placeholder-aware | integration | `uv run pytest tests/integration/test_temp_identity_policy.py -v` | ❌ W0 | ⬜ pending |
| 03-02-02 | 02 | 1 | GOV-02 | T-03-04 / T-03-06 | Identity resolution preserves precedence rules while preventing raw-name leakage in `company_id` and `evidence_refs` | integration | `uv run pytest tests/integration/test_temp_identity_policy.py tests/integration/test_identity_resolution.py -v` | ❌ W0 / ✅ | ⬜ pending |
| 03-03-01 | 03 | 2 | PIPE-04 | T-03-07 | The annuity slice adopts shared replay primitives while keeping annuity-specific services, assets, and publication wiring explicit | replay | `uv run pytest tests/replay/test_annuity_performance_slice.py -v` | ✅ | ⬜ pending |
| 03-03-02 | 03 | 2 | PIPE-03 | T-03-08 / T-03-09 | The annuity slice proves typed setup failures, typed `primary_failure`, and comparison-run package writing for every completed replay outcome | integration + replay | `uv run pytest tests/integration/test_replay_setup_failures.py tests/replay/test_phase2_annuity_performance_gates.py -v` | ❌ W0 / ✅ | ⬜ pending |
| 03-04-01 | 04 | 3 | PIPE-04 | T-03-10 | The annual-award slice adopts the shared runtime without hiding event-domain enrichment or publication semantics | replay | `uv run pytest tests/replay/test_annual_award_slice.py tests/replay/test_phase2_event_domain_gates.py -k award -v` | ✅ / ✅ | ⬜ pending |
| 03-04-02 | 04 | 3 | GOV-02, PIPE-04 | T-03-11 / T-03-12 | The annual-loss slice adopts the shared runtime and all replay expectations move from `TEMP-*` to governed opaque `IN...` identifiers | replay | `uv run pytest tests/replay/test_annual_loss_slice.py tests/replay/test_phase2_event_domain_gates.py tests/replay/test_phase2_reference_derivation_gates.py -k loss -v` | ✅ / ✅ / ✅ | ⬜ pending |
| 03-04-03 | 04 | 3 | PIPE-03 | T-03-16 | Award/loss-specific setup assets such as customer-plan-history fixtures and event-domain replay assets still raise typed replay setup exceptions after shared-runtime adoption | integration | `uv run pytest tests/integration/test_replay_setup_failures.py -k "award or loss" -v` | ❌ W0 | ⬜ pending |
| 03-05-01 | 05 | 4 | OPS-01 | T-03-13 / T-03-14 | `replay run` and `replay list-domains` expose stable machine-readable output while preserving the three human wrapper commands | CLI contract | `uv run pytest tests/contracts/test_replay_cli_contracts.py -v` | ❌ W0 | ⬜ pending |
| 03-05-02 | 05 | 4 | OPS-01, PIPE-03 | T-03-14 | `replay diagnose` exposes typed machine-readable diagnostics for completed runs with or without compatibility cases, plus typed missing-run behavior, through the same governed report contract | CLI contract | `uv run pytest tests/contracts/test_replay_diagnose_contracts.py -v` | ❌ W0 → ✅ after 03-01 | ⬜ pending |
| 03-05-03 | 05 | 4 | OPS-01 | T-03-15 | The three replay runbooks document the preserved wrappers, the new replay CLI, and the `WDHP_TEMP_ID_SALT` prerequisite without drifting into deferred command surfaces | docs contract | `rg -n "replay-annuity-performance|replay-annual-award|replay-annual-loss|replay run --domain|replay diagnose --comparison-run-id|replay list-domains|WDHP_TEMP_ID_SALT" docs/runbooks/annuity-performance-replay.md docs/runbooks/annual-award-replay.md docs/runbooks/annual-loss-replay.md` | ✅ / ✅ / ✅ | ⬜ pending |

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

All phase behaviors have automated verification. Human review of runbook clarity remains useful, but Phase 3 does not depend on any manual-only acceptance gate.

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references
- [x] No watch-mode flags
- [x] Feedback latency < 30s for targeted checks
- [x] `nyquist_compliant: true` set in frontmatter

**Approval:** approved 2026-04-13

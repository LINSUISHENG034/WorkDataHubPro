---
phase: 04
slug: agent-operations-governance-hardening
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-04-13
---

# Phase 04 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | `pytest 8.4.x` via `uv run pytest` |
| **Config file** | `pyproject.toml` |
| **Quick run command** | `uv run pytest tests/contracts/test_phase4_lookup_contracts.py tests/contracts/test_phase4_evidence_redaction_contracts.py tests/contracts/test_phase4_compatibility_cli_contracts.py tests/contracts/test_phase4_runbook_contracts.py tests/integration/test_phase4_lineage_lookup.py tests/integration/test_phase4_evidence_redaction.py tests/integration/test_compatibility_adjudication.py -v` |
| **Full suite command** | `uv run pytest -v` |
| **Estimated runtime** | ~180 seconds |

---

## Sampling Rate

- **After every task commit:** Run the narrowest plan-specific pytest command from the table below.
- **After every plan wave:** Run the quick run command above.
- **Before `/gsd-verify-work`:** `uv run pytest -v`
- **Max feedback latency:** 180 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 04-01-01 | 01 | 1 | OPS-03 / OPS-04 | T-04-01 / T-04-02 | Lookup rejects path-like `comparison_run_id` values and resolves output rows to anchors, lineage, and trace evidence through governed package readers only. | contract + integration | `uv run pytest tests/contracts/test_phase4_lookup_contracts.py tests/integration/test_phase4_lineage_lookup.py -v` | ❌ W0 | ⬜ pending |
| 04-02-01 | 02 | 2 | GOV-01 / OPS-04 | T-04-04 / T-04-05 | Evidence artifacts mask configured sensitive values before persistence while preserving `comparison_run_id`, `batch_id`, `record_id`, `anchor_row_no`, `stage_id`, and `rule_id`. | contract + integration | `uv run pytest tests/contracts/test_phase4_evidence_redaction_contracts.py tests/integration/test_phase4_evidence_redaction.py -v` | ❌ W0 | ⬜ pending |
| 04-03-01 | 03 | 2 | GOV-03 / OPS-04 | T-04-07 / T-04-08 | Compatibility cases require explicit owner, lifecycle status, and closure proof before they can leave `pending_review`. | contract + integration | `uv run pytest tests/contracts/test_phase4_compatibility_cli_contracts.py tests/integration/test_compatibility_adjudication.py -v` | ❌ W0 | ⬜ pending |
| 04-04-01 | 04 | 3 | OPS-02 / OPS-04 | T-04-10 | The canonical agent workflow runbook references exact commands and repo paths for add-source / adjust-rule / run-verify / inspect-evidence behavior. | contract | `uv run pytest tests/contracts/test_phase4_runbook_contracts.py -v` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `tests/contracts/test_phase4_lookup_contracts.py` — lookup CLI and evidence-path contract coverage
- [ ] `tests/integration/test_phase4_lineage_lookup.py` — output-to-source lineage lookup integration coverage
- [ ] `tests/contracts/test_phase4_evidence_redaction_contracts.py` — governed redaction policy contract coverage
- [ ] `tests/integration/test_phase4_evidence_redaction.py` — persistence-boundary masking coverage
- [ ] `tests/contracts/test_phase4_compatibility_cli_contracts.py` — compatibility lifecycle CLI contract coverage
- [ ] `tests/contracts/test_phase4_runbook_contracts.py` — workflow/runbook drift protection

*Existing infrastructure covers the framework and runner requirements; Wave 0 is only new test-module creation.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| A non-author can follow the maintenance workflow from docs without hidden context. | OPS-02 / OPS-04 | Contract tests can freeze commands and paths, but not whether the workflow reads coherently to a fresh operator. | From a clean shell, follow `docs/runbooks/agent-maintenance-workflow.md` end to end for one existing replay domain: inspect registry/config files, run `replay run`, run `replay diagnose`, run the new lookup command, and confirm the documented compatibility-case flow matches the implemented CLI. |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or existing test infrastructure support
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all missing verification references
- [ ] No watch-mode flags
- [ ] Feedback latency < 180s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending

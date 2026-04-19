---
status: complete
phase: 04-agent-operations-governance-hardening
source:
  - .planning/phases/04-agent-operations-governance-hardening/04-01-SUMMARY.md
  - .planning/phases/04-agent-operations-governance-hardening/04-02-SUMMARY.md
  - .planning/phases/04-agent-operations-governance-hardening/04-03-SUMMARY.md
  - .planning/phases/04-agent-operations-governance-hardening/04-04-SUMMARY.md
started: 2026-04-19T01:58:56.179518Z
updated: 2026-04-19T02:04:12.028502Z
---

## Current Test

[testing complete]

## Tests

### 1. Cold Start Smoke Test
expected: From a clean shell, the CLI starts without boot errors and exposes the Phase 4 operator surfaces. At minimum, `uv run python -m work_data_hub_pro.apps.etl_cli.main replay --help` shows `lookup`, and `uv run python -m work_data_hub_pro.apps.etl_cli.main compatibility --help` shows `show-case`, `transition-case`, and `close-case`.
result: pass

### 2. Canonical Maintenance Workflow
expected: The canonical runbook at `docs/runbooks/agent-maintenance-workflow.md` clearly documents the bounded add-source, adjust-rule, run-verify, inspect-evidence, and compatibility-case workflow, and the registered domain runbooks point back to that workflow instead of duplicating conflicting steps.
result: pass

### 3. Output-to-Source Replay Lookup
expected: Running `replay lookup` for a valid comparison run and record returns machine-readable lineage details that include the comparison run id, record id, batch id, anchor row, origin rows, parent record ids, trace path, artifact gaps, checkpoint statuses, and compatibility case id.
result: pass

### 4. Redacted Evidence Still Preserves Lookup Anchors
expected: Persisted evidence masks sensitive payload fields, but replay lookup still resolves the expected anchors such as `trace_path`, `origin_row_nos`, `parent_record_ids`, and `artifact_gaps` instead of breaking lookup.
result: pass

### 5. Compatibility Case Lifecycle Commands
expected: The compatibility CLI supports inspecting a case, transitioning it with owner and resolution note, and closing it with closure evidence. The returned payload keeps lifecycle state, resolved outcome, decision owner, and closure proof machine-readable.
result: pass

### 6. Machine-Readable Failure Paths
expected: Invalid or incomplete replay lookup and compatibility-case requests fail closed with explicit JSON error codes instead of partial or ambiguous output.
result: pass

## Summary

total: 6
passed: 6
issues: 0
pending: 0
skipped: 0
blocked: 0

## Gaps

[none yet]

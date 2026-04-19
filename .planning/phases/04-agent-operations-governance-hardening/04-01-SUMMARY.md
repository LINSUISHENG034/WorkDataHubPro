---
phase: 04-agent-operations-governance-hardening
plan: 01
subsystem: apps
tags: [replay, lineage, evidence, cli, diagnostics]
requires:
  - phase: 03-orchestration-refactor-failure-explainability
    provides: replay diagnostics, comparison-run packaging, and registry-backed replay CLI surfaces
provides:
  - lookup-ready replay evidence paths for source-intake and lineage packages
  - fail-closed row-level replay lookup helper with explicit error codes
  - machine-readable `replay lookup` CLI contract and negative-path integration coverage
affects: [OPS-03, OPS-04, replay diagnostics, incident response]
tech-stack:
  added: []
  patterns: [file-backed replay lookup contract, fail-closed lineage package readers, machine-readable CLI errors]
key-files:
  created:
    - src/work_data_hub_pro/apps/orchestration/replay/lookup.py
    - tests/contracts/test_phase4_lookup_contracts.py
    - tests/integration/test_phase4_lineage_lookup.py
  modified:
    - src/work_data_hub_pro/apps/orchestration/replay/contracts.py
    - src/work_data_hub_pro/apps/orchestration/replay/runtime.py
    - src/work_data_hub_pro/apps/orchestration/replay/diagnostics.py
    - src/work_data_hub_pro/governance/compatibility/gate_runtime.py
    - src/work_data_hub_pro/governance/evidence_index/file_store.py
    - src/work_data_hub_pro/apps/etl_cli/main.py
key-decisions:
  - "Persist lookup-ready lineage as `records` entries with explicit `trace_path` and `artifact_gaps` instead of browsing raw directories."
  - "Keep replay lookup file-backed and CLI-driven by reusing diagnostics validation and evidence-index readers rather than refactoring tracing or lineage modules."
patterns-established:
  - "Replay lookup requests must provide exactly one selector and return explicit machine-readable error codes on failure."
  - "Malformed or missing lineage packages fail closed instead of degrading to partial output."
requirements-completed: [OPS-03, OPS-04]
duration: 1h
completed: 2026-04-19
---

# Phase 4 Plan 01: Output-to-source replay lookup summary

**Fail-closed replay lookup now resolves comparison-run rows back to source-stage lineage, retained trace evidence, and explicit artifact gaps through one machine-readable CLI and helper contract.**

## Performance

- **Duration:** 1h
- **Started:** 2026-04-19T00:00:00Z
- **Completed:** 2026-04-19T00:00:00Z
- **Tasks:** 3
- **Files modified:** 9

## Accomplishments
- Extended replay evidence packaging so source-intake and lineage artifacts are first-class, path-addressable package members.
- Added typed replay lookup loading and a `replay lookup` CLI that rejects invalid, ambiguous, and malformed requests with explicit error codes.
- Proved happy-path, failed-run, and negative-path lookup behavior with contract and integration coverage, including explicit `trace_missing` handling.

## Task Commits

Each task was committed atomically:

1. **Task 1: Extend the comparison-run package and evidence-path contract for lookup-ready source and lineage data** - `539eefd` (feat)
2. **Task 2: Add typed replay lookup helpers and a machine-readable CLI command with explicit ambiguity handling** - `9654036` (feat)
3. **Task 3: Cover happy-path, failed-run, and negative-path lookup behavior without expanding trace or lineage helper scope** - `f0e1e3d` (fix)

**Plan metadata:** recorded in the final docs planning-state commit for this plan.

## Files Created/Modified
- `E:/Projects/WorkDataHubPro/.claude/worktrees/slice-phase4-agent-ops-hardening/src/work_data_hub_pro/apps/orchestration/replay/contracts.py` - extends replay evidence paths with lookup-ready source-intake and lineage package members
- `E:/Projects/WorkDataHubPro/.claude/worktrees/slice-phase4-agent-ops-hardening/src/work_data_hub_pro/apps/orchestration/replay/runtime.py` - normalizes persisted lineage lookup records and explicit `trace_missing` artifact gaps
- `E:/Projects/WorkDataHubPro/.claude/worktrees/slice-phase4-agent-ops-hardening/src/work_data_hub_pro/apps/orchestration/replay/diagnostics.py` - exposes the new evidence-path members in diagnostics payloads
- `E:/Projects/WorkDataHubPro/.claude/worktrees/slice-phase4-agent-ops-hardening/src/work_data_hub_pro/apps/orchestration/replay/lookup.py` - adds the typed replay lookup result, fail-closed error contract, and selector enforcement
- `E:/Projects/WorkDataHubPro/.claude/worktrees/slice-phase4-agent-ops-hardening/src/work_data_hub_pro/governance/compatibility/gate_runtime.py` - guarantees default package path coverage for lookup-ready replay artifacts
- `E:/Projects/WorkDataHubPro/.claude/worktrees/slice-phase4-agent-ops-hardening/src/work_data_hub_pro/governance/evidence_index/file_store.py` - adds fail-closed readers for source-intake and lineage packages
- `E:/Projects/WorkDataHubPro/.claude/worktrees/slice-phase4-agent-ops-hardening/src/work_data_hub_pro/apps/etl_cli/main.py` - adds the `replay lookup` command and machine-readable JSON error payloads
- `E:/Projects/WorkDataHubPro/.claude/worktrees/slice-phase4-agent-ops-hardening/tests/contracts/test_phase4_lookup_contracts.py` - freezes the lookup helper and CLI contract shape
- `E:/Projects/WorkDataHubPro/.claude/worktrees/slice-phase4-agent-ops-hardening/tests/integration/test_phase4_lineage_lookup.py` - proves happy-path, failed-run, ambiguity, invalid input, and malformed-package behavior

## Decisions Made
- Persisted lineage lookup payloads under the exact top-level shape `{"records": [...]}` so later readers do not depend on slice-specific ad hoc summaries.
- Used the existing diagnostics comparison-run identifier validation rule to keep lookup path traversal protections identical to diagnose behavior.
- Returned JSON errors from the CLI in the exact shape `{"error": "<code>", "comparison_run_id": "<id>"}` to make failures machine-readable for agents.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Updated diagnostics to construct the expanded evidence path contract**
- **Found during:** Task 3 (integration verification)
- **Issue:** `load_replay_diagnostics(...)` still instantiated `ReplayEvidencePaths` with the pre-lookup field set, causing end-to-end lookup integration to fail even though the runtime and contract tests had passed.
- **Fix:** Added `source_intake_adaptation` and `lineage_impact` path resolution to diagnostics report construction.
- **Files modified:** `src/work_data_hub_pro/apps/orchestration/replay/diagnostics.py`
- **Verification:** `uv run pytest tests/integration/test_phase4_lineage_lookup.py -v` and `uv run pytest tests/contracts/test_phase4_lookup_contracts.py tests/integration/test_phase4_lineage_lookup.py -v`
- **Committed in:** `f0e1e3d`

---

**Total deviations:** 1 auto-fixed (1 Rule 1 bug)
**Impact on plan:** Correctness-only fix required to make the planned lookup contract work end to end. No scope creep.

## Issues Encountered
- Initial integration tests patched the diagnostics registry at the wrong seam because `load_replay_lookup()` imports the diagnostics loader directly; the tests were corrected to patch the lookup module dependency instead.
- The first missing-package contract test needed a minimal manifest fixture so the fail-closed lineage reader could reach the intended missing-file path instead of failing earlier on manifest absence.

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- Replay lookup is now stable enough for the later runbook and incident-diagnostics work in Phase 4.
- The remaining Phase 4 plans can build on explicit lookup surfaces without refactoring tracing or lineage storage.

## Known Stubs
None.

## Self-Check: PASSED
- Verified summary and key files exist on disk.
- Verified task commits `539eefd`, `9654036`, and `f0e1e3d` exist in git history.

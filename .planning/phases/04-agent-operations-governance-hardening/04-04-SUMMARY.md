---
phase: 04-agent-operations-governance-hardening
plan: 04
subsystem: docs.architecture
tags: [runbooks, replay, cli, contracts, governance]
requires:
  - phase: 04-agent-operations-governance-hardening
    provides: replay lookup, evidence redaction, and compatibility lifecycle CLI surfaces from Plans 01-03
provides:
  - canonical bounded agent maintenance workflow runbook
  - aligned registered-domain replay runbooks
  - contract tests binding docs to registry paths and CLI help surfaces
affects: [OPS-02, OPS-04, runbooks, incident-response, replay-operations]
tech-stack:
  added: []
  patterns: [canonical runbook delegation, registry-backed runbook drift protection, CLI help contract verification]
key-files:
  created:
    - docs/runbooks/agent-maintenance-workflow.md
    - tests/contracts/test_phase4_runbook_contracts.py
  modified:
    - docs/runbooks/annuity-performance-replay.md
    - docs/runbooks/annual-award-replay.md
    - docs/runbooks/annual-loss-replay.md
    - docs/runbooks/annuity-income-replay.md
key-decisions:
  - "Use one canonical runbook for the bounded add-source, adjust-rule, run-verify, inspect-evidence workflow and make domain runbooks delegate to it instead of duplicating process guidance."
  - "Protect workflow documentation with executable checks against replay registry paths and Typer help output, not doc strings alone."
patterns-established:
  - "Registered replay-domain runbooks must reference docs/runbooks/agent-maintenance-workflow.md for shared maintenance flow and keep only domain-local workbook and replay-root details inline."
  - "Operational runbook claims must match implemented replay and compatibility CLI commands exactly enough to be asserted by contract tests."
requirements-completed: [OPS-02, OPS-04]
duration: 57 min
completed: 2026-04-19
---

# Phase 4 Plan 04: Agent maintenance workflow and incident runbooks Summary

**Canonical bounded maintenance runbook now ties replay verification, lookup, and compatibility case handling to the implemented registry-backed CLI across all four registered domains.**

## Performance

- **Duration:** 57 min
- **Started:** 2026-04-19T00:00:00Z
- **Completed:** 2026-04-19T00:56:43Z
- **Tasks:** 3
- **Files modified:** 6

## Accomplishments
- Added one canonical workflow runbook that freezes the current Phase 4 maintenance scope, repo paths, and exact replay and compatibility command forms.
- Updated the annuity performance, annual award, annual loss, and annuity income runbooks to delegate to the canonical workflow while keeping domain-specific workbook details local.
- Added contract coverage that verifies registered runbook, release, and domain-config paths exist and that CLI help exposes the documented lookup and compatibility commands.

## Task Commits

Each task was committed atomically:

1. **Task 1: Write the canonical agent maintenance workflow runbook with exact scope bounds and command forms** - `528e99c` (docs)
2. **Task 2: Align all registered domain runbooks to the canonical workflow without duplicating unsupported claims** - `ad85e0f` (docs)
3. **Task 3: Add contract tests that verify registry paths and CLI help surfaces, not only doc strings** - `521f1f6` (test)

## Files Created/Modified
- `E:/Projects/WorkDataHubPro/.claude/worktrees/slice-phase4-agent-ops-hardening/docs/runbooks/agent-maintenance-workflow.md` - canonical bounded add-source, adjust-rule, run-verify, inspect-evidence, and compatibility-case workflow
- `E:/Projects/WorkDataHubPro/.claude/worktrees/slice-phase4-agent-ops-hardening/docs/runbooks/annuity-performance-replay.md` - delegates shared maintenance flow to the canonical workflow and includes lookup and compatibility command forms
- `E:/Projects/WorkDataHubPro/.claude/worktrees/slice-phase4-agent-ops-hardening/docs/runbooks/annual-award-replay.md` - delegates shared maintenance flow to the canonical workflow and includes lookup and compatibility command forms
- `E:/Projects/WorkDataHubPro/.claude/worktrees/slice-phase4-agent-ops-hardening/docs/runbooks/annual-loss-replay.md` - delegates shared maintenance flow to the canonical workflow and includes lookup and compatibility command forms
- `E:/Projects/WorkDataHubPro/.claude/worktrees/slice-phase4-agent-ops-hardening/docs/runbooks/annuity-income-replay.md` - delegates shared maintenance flow to the canonical workflow and includes lookup and compatibility command forms
- `E:/Projects/WorkDataHubPro/.claude/worktrees/slice-phase4-agent-ops-hardening/tests/contracts/test_phase4_runbook_contracts.py` - freezes registry path existence, CLI help discoverability, and canonical runbook delegation contracts

## Validation

- `uv run pytest tests/contracts/test_phase4_runbook_contracts.py -v`
- `uv run pytest -v` (fails in unrelated pre-existing areas; see Deferred Issues)

## Decisions Made
- Used the canonical runbook as the only shared maintenance workflow and kept the domain runbooks limited to domain-local workbook, replay-root, and expected-output details.
- Verified workflow claims against `REPLAY_DOMAINS` file paths and Typer help output so docs stay bounded to real repo-native surfaces.
- Included `annuity_income` in the same delegated workflow surface as the other currently registered replay domains.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking issue] Executed without `04-REVIEWS.md` because the referenced planning input was absent from the worktree**
- **Found during:** Task 1 setup
- **Issue:** `04-04-PLAN.md` referenced `.planning/phases/04-agent-operations-governance-hardening/04-REVIEWS.md`, but no such file existed in the worktree.
- **Fix:** Executed against the available plan, context, research, and validation artifacts while preserving the plan’s bounded-scope intent and stronger contract-test requirement.
- **Files modified:** none
- **Verification:** confirmed the file was absent and the implemented deliverables matched the plan frontmatter, task actions, and validation command.
- **Committed in:** none

---

**Total deviations:** 1 auto-fixed (1 Rule 3 blocking input gap)
**Impact on plan:** No scope creep. The missing review input did not require runtime changes; execution stayed within the plan’s stated deliverables and verification path.

## Issues Encountered
- A worktree shell did not have `gsd-sdk` available, so plan-state updates were applied by editing committed planning docs directly instead of using SDK helper commands.
- The repository-level full-suite run surfaced unrelated failures outside this plan’s changed files, including a missing `docs/superpowers/reviews/2026-04-11-legacy-risk-analysis-for-rebuild.md` referenced by `tests/contracts/test_annual_loss_governance_addendum_docs.py`.

## Deferred Issues
- `uv run pytest -v` is not fully green in this worktree due to unrelated pre-existing failures outside the runbook slice. Reproduced failure: `tests/contracts/test_annual_loss_governance_addendum_docs.py::test_annual_loss_acceptance_syncs_risk_register_without_retiring_open_runtime_gaps` fails because `docs/superpowers/reviews/2026-04-11-legacy-risk-analysis-for-rebuild.md` is missing.

## Known Stubs

None.

## Threat Flags

None.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness
- Phase 4 now has one canonical maintenance workflow and executable runbook drift protection for all currently registered replay domains.
- Remaining follow-up should focus on the unrelated repository-wide failing tests before using a full-suite-green claim for broader release readiness.

## Self-Check: PASSED
- Found summary file: `E:/Projects/WorkDataHubPro/.claude/worktrees/slice-phase4-agent-ops-hardening/.planning/phases/04-agent-operations-governance-hardening/04-04-SUMMARY.md`
- Found commit: `528e99c`
- Found commit: `ad85e0f`
- Found commit: `521f1f6`

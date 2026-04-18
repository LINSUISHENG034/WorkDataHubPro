# WorkDataHubPro Wiki BI Round 33 Reference Sync Governance Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Tighten `docs/wiki-bi/` around `reference_sync` so the wiki can directly explain its target inventory, incremental sync-state contract, and current `reference_derivation -> publication` replacement boundary without scattering those conclusions across multiple pages.

**Architecture:** Keep this round evidence-first. Create one object-level evidence page for `reference_sync`, keep `reference-sync.md` as the governing surface page, reconnect the existing aggregate evidence pages and one high-traffic standard page back to the new evidence object, then write back round sediment plus a narrow docs contract to keep the new evidence route reachable.

**Tech Stack:** Markdown in `docs/wiki-bi/` and `docs/superpowers/plans/`, small pytest docs contract in `tests/contracts/`, legacy evidence from `E:\Projects\WorkDataHub`, PowerShell, `rg`, git worktrees, `uv`, `pytest`

---

## Scope Check

This plan covers:

- one new object-level evidence page for `reference_sync`
- tightening `reference-sync.md` so it can delegate details instead of carrying every sub-boundary inline
- tightening `reference-and-backfill-evidence.md` and `operator-and-surface-evidence.md` so `reference_sync` no longer relies only on aggregate wording
- reconnecting the new evidence page from `backfill.md` and `output-correctness.md`
- updating `index.md`, `log.md`, `wiki-absorption-roadmap.md`, and `absorption-rounds/index.md`
- adding one narrow docs contract test to protect reachability

This plan does not cover:

- re-admitting repo-native `reference_sync` runtime, schedule, or state store
- `company_lookup_queue`, manual `customer-mdm`, or enterprise persistence closure
- changing `src/`, `config/`, or replay/reference assets
- semantic-map registry mutation or wave closeout

## Suggested Branch

- `docs/wiki-round-33`

## Baseline Note

The isolated worktree already exists at `E:\Projects\WorkDataHubPro\.worktrees\docs-wiki-round-33` on branch `docs/wiki-round-33`.

Baseline environment check:

- `uv sync --dev` completed successfully in the worktree.
- `uv run pytest -v` currently has **4 pre-existing failures** unrelated to this docs scope:
  - `tests/contracts/test_annual_loss_governance_addendum_docs.py::test_annual_loss_acceptance_syncs_risk_register_without_retiring_open_runtime_gaps`
  - `tests/contracts/test_annuity_income_governance_docs.py::test_annuity_income_governance_docs_mark_slice_as_accepted`
  - `tests/contracts/test_legacy_semantic_map_first_wave_pilot.py::test_first_wave_pilot_repo_state_is_populated_and_real_evidence_backed`
  - `tests/integration/test_legacy_semantic_map_first_wave_pilot_flow.py::test_run_first_wave_pilot_rebuilds_active_successor_wave_deterministically`
- The first two fail because `docs/superpowers/reviews/2026-04-11-legacy-risk-analysis-for-rebuild.md` is missing from the checked-in tree.
- The latter two fail because the checked-in successor wave now compiles `13` claims while those tests still expect `7`.

This round must not claim those failures were introduced by the docs changes.

## Files To Create

- `docs/wiki-bi/evidence/reference-sync-runtime-and-state-evidence.md`
- `docs/wiki-bi/_meta/absorption-rounds/round-33-reference-sync-governance.md`
- `tests/contracts/test_reference_sync_wiki_docs.py`

## Files To Modify

- `docs/wiki-bi/surfaces/reference-sync.md`
- `docs/wiki-bi/evidence/reference-and-backfill-evidence.md`
- `docs/wiki-bi/evidence/operator-and-surface-evidence.md`
- `docs/wiki-bi/concepts/backfill.md`
- `docs/wiki-bi/standards/output-correctness/output-correctness.md`
- `docs/wiki-bi/index.md`
- `docs/wiki-bi/log.md`
- `docs/wiki-bi/_meta/absorption-rounds/index.md`
- `docs/wiki-bi/_meta/wiki-absorption-roadmap.md`

### Task 1: Create The `reference_sync` Object-Level Evidence Page

**Files:**
- Create: `docs/wiki-bi/evidence/reference-sync-runtime-and-state-evidence.md`
- Modify: `docs/wiki-bi/surfaces/reference-sync.md`

- [x] **Step 1: Create the new evidence page**

Write `docs/wiki-bi/evidence/reference-sync-runtime-and-state-evidence.md`.

The page must aggregate three threads:

- legacy target inventory
- legacy incremental sync-state contract
- current accepted replacement boundary through `reference_derivation -> publication`

Primary sources to keep explicit:

- `E:\Projects\WorkDataHub\config\reference_sync.yml`
- `E:\Projects\WorkDataHub\src\work_data_hub\orchestration\reference_sync_ops.py`
- `E:\Projects\WorkDataHub\src\work_data_hub\io\repositories\sync_state_repository.py`
- `E:\Projects\WorkDataHub\src\work_data_hub\domain\reference_backfill\sync_models.py`
- `tests/integration/test_reference_derivation.py`
- `tests/integration/test_publication_service.py`

The page must make clear:

- `reference_sync` is governed through an explicit target inventory, not as a helper
- incremental sync state is a stable legacy contract
- current accepted slices replace hidden sync runtime with `reference_derivation -> publication`
- replacement of runtime breadth does not retire target-inventory or source-of-truth memory

- [x] **Step 2: Tighten the surface page**

Update `docs/wiki-bi/surfaces/reference-sync.md` so it remains the governing surface page but now delegates detailed evidence to the new object-level page.

The intended result is:

- `reference-sync.md` stays readable
- the page no longer carries the entire sync-state / replacement story inline
- the new evidence page becomes the canonical route for the detailed runtime/state boundary

### Task 2: Reconnect The Aggregate Evidence And Standards Layer

**Files:**
- Modify: `docs/wiki-bi/evidence/reference-and-backfill-evidence.md`
- Modify: `docs/wiki-bi/evidence/operator-and-surface-evidence.md`
- Modify: `docs/wiki-bi/concepts/backfill.md`
- Modify: `docs/wiki-bi/standards/output-correctness/output-correctness.md`

- [x] **Step 1: Tighten the two aggregate evidence pages**

Update:

- `docs/wiki-bi/evidence/reference-and-backfill-evidence.md`
- `docs/wiki-bi/evidence/operator-and-surface-evidence.md`

The intended result is:

- `reference-and-backfill-evidence.md` points to the new page for target inventory / sync-state / replacement details
- `operator-and-surface-evidence.md` stops leaving `reference_sync` only as a row in a decision table and now routes to the new object-level evidence page

- [x] **Step 2: Reconnect one concept page and one high-traffic standard page**

Update:

- `docs/wiki-bi/concepts/backfill.md`
- `docs/wiki-bi/standards/output-correctness/output-correctness.md`

The intended result is:

- readers looking at the `backfill` / `reference_sync` boundary get a direct route to the new evidence page
- the high-traffic output-correctness page exposes the provenance split with a direct evidence route, not only a generic statement

### Task 3: Add Navigation, Sediment, And A Minimal Docs Contract

**Files:**
- Create: `docs/wiki-bi/_meta/absorption-rounds/round-33-reference-sync-governance.md`
- Create: `tests/contracts/test_reference_sync_wiki_docs.py`
- Modify: `docs/wiki-bi/index.md`
- Modify: `docs/wiki-bi/log.md`
- Modify: `docs/wiki-bi/_meta/absorption-rounds/index.md`
- Modify: `docs/wiki-bi/_meta/wiki-absorption-roadmap.md`

- [x] **Step 1: Update the main index**

In `docs/wiki-bi/index.md`:

- add a discoverable FAQ / maintainer route for `reference_sync` runtime/state governance
- register the new evidence page in the evidence catalog
- keep the current index structure intact

- [x] **Step 2: Create the Round 33 sediment note**

Write `docs/wiki-bi/_meta/absorption-rounds/round-33-reference-sync-governance.md` documenting:

- why this round focused on `reference_sync` rather than broader runtime closure
- what is now stable
- what remains deferred

- [x] **Step 3: Add a narrow docs contract**

Create `tests/contracts/test_reference_sync_wiki_docs.py`.

The test should only assert stable, high-signal conditions:

- the new evidence page exists and mentions both target inventory and `last_synced_at`
- `reference-sync.md` routes to it
- `index.md` exposes it

Do not make the test brittle by asserting entire paragraphs verbatim.

- [x] **Step 4: Update roadmap/index metadata and append the log**

Update:

- `docs/wiki-bi/_meta/absorption-rounds/index.md`
- `docs/wiki-bi/_meta/wiki-absorption-roadmap.md`
- `docs/wiki-bi/log.md`

The updates must show:

- Round 33 completed
- `reference_sync` now has an object-level evidence route
- runtime breadth still remains deferred
- likely next follow-on work is `manual customer-mdm` / enterprise persistence rather than another nearby business-semantic object

## Validation Steps

- [x] Run reachability and keyword checks:
  - `rg -n "reference_sync|last_synced_at|reference_derivation|publication|target inventory" docs/wiki-bi tests/contracts`
- [x] Review only the intended docs/test diff:
  - `git diff -- docs/wiki-bi docs/superpowers/plans tests/contracts`
- [x] Run formatting/sanity check:
  - `git diff --check`
- [x] Run the new narrow docs contract:
  - `uv run pytest tests/contracts/test_reference_sync_wiki_docs.py -v`
- [x] Re-run the relevant existing anchors:
  - `uv run pytest tests/integration/test_reference_derivation.py tests/integration/test_publication_service.py -v`
- [x] Re-run the full suite after the docs round completes:
  - `uv run pytest -v`
  - Expected: the same 4 pre-existing failures remain; no new failures introduced by Round 33

## Completion Criteria

This round is complete when:

- `reference_sync` no longer relies only on aggregate pages to explain target inventory, incremental state, and current replacement boundary
- the wiki can directly answer why `reference_sync` is still governed even though repo-native runtime remains deferred
- `reference-sync.md`, `reference-and-backfill-evidence.md`, and `output-correctness.md` all route to the new evidence page
- Round 33 navigation and sediment are written back in `index.md`, `log.md`, and `_meta/absorption-rounds/`
- the new docs contract passes
- validation shows no new failures beyond the known pre-existing baseline failures

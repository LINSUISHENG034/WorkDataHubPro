# WorkDataHubPro Wiki BI Round 36 Manual Customer MDM And Persistence Closure Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Tighten `docs/wiki-bi/` around manual `customer-mdm` commands and enterprise enrichment persistence so the wiki can directly explain what legacy operator/runtime surfaces existed, what their stable semantic layering is, and why the current accepted runtime still treats them as deferred rather than silently retained.

**Architecture:** Keep this round evidence-first. Create one object-level evidence page for manual `customer-mdm` runtime boundaries and one object-level evidence page for enterprise enrichment persistence layering, keep the existing surface pages as the governing routes, reconnect aggregate evidence and standards pages back to the new evidence objects, then write back round sediment plus navigation so the new closure is reachable without reopening broad runtime design.

**Tech Stack:** Markdown in `docs/wiki-bi/` and `docs/superpowers/plans/`, legacy evidence from `E:\Projects\WorkDataHub`, current specs/tests/code under `WorkDataHubPro`, PowerShell, `rg`, git worktrees, `uv`, `pytest`

---

## Scope Check

This plan covers:

- one new object-level evidence page for manual `customer-mdm` runtime/operator boundaries
- one new object-level evidence page for enterprise enrichment persistence layering
- tightening `customer-mdm-commands.md` and `enterprise-enrichment-persistence.md` so they delegate details rather than carrying all boundary text inline
- tightening `operator-and-surface-evidence.md`, `identity-and-lookup-evidence.md`, and `customer-mdm-lifecycle-evidence.md` so the new evidence pages become the canonical detailed routes
- updating `index.md`, `log.md`, `wiki-absorption-roadmap.md`, and `absorption-rounds/index.md`
- adding a Round 36 sediment note

This plan does not cover:

- re-admitting repo-native manual `customer-mdm` commands
- re-admitting repo-native persistence tables such as `enrichment_requests`, `enrichment_index`, `base_info`, `business_info`, or `biz_label`
- `company_lookup_queue` retry/runtime closure
- standalone tooling closure
- changes under `src/`, `config/`, or `tests/`

## Suggested Branch

- `docs/wiki-bi-round34`

## Baseline Note

The isolated worktree exists at `E:\Projects\WorkDataHubPro\.worktrees\docs-wiki-bi-round34` on branch `docs/wiki-bi-round34`.

Baseline environment check after the Round 35 commit:

- `git status --short` is clean.
- `uv run pytest -v` currently passes cleanly: `292 passed`.
- Round 34 and Round 35 are already committed on this branch as `ca4bace` and `2e6a32e`.

This round should keep the branch green and produce the next narrow docs-only commit.

## Files To Create

- `docs/wiki-bi/evidence/customer-mdm-manual-runtime-evidence.md`
- `docs/wiki-bi/evidence/enterprise-enrichment-persistence-evidence.md`
- `docs/wiki-bi/_meta/absorption-rounds/round-36-manual-customer-mdm-and-persistence-closure.md`

## Files To Modify

- `docs/wiki-bi/surfaces/customer-mdm-commands.md`
- `docs/wiki-bi/surfaces/enterprise-enrichment-persistence.md`
- `docs/wiki-bi/evidence/customer-mdm-lifecycle-evidence.md`
- `docs/wiki-bi/evidence/identity-and-lookup-evidence.md`
- `docs/wiki-bi/evidence/operator-and-surface-evidence.md`
- `docs/wiki-bi/standards/semantic-correctness/identity-governance.md`
- `docs/wiki-bi/index.md`
- `docs/wiki-bi/log.md`
- `docs/wiki-bi/_meta/absorption-rounds/index.md`
- `docs/wiki-bi/_meta/wiki-absorption-roadmap.md`

### Task 1: Create The Manual `customer-mdm` Runtime Evidence Route

**Files:**
- Create: `docs/wiki-bi/evidence/customer-mdm-manual-runtime-evidence.md`
- Modify: `docs/wiki-bi/surfaces/customer-mdm-commands.md`
- Modify: `docs/wiki-bi/evidence/customer-mdm-lifecycle-evidence.md`

- [ ] **Step 1: Create the new evidence page**

Write `docs/wiki-bi/evidence/customer-mdm-manual-runtime-evidence.md`.

The page must aggregate three threads:

- legacy manual command surface (`sync`, `snapshot`, `init-year`, `validate`, `cutover`)
- relationship to the default annuity-performance-triggered hook chain
- current accepted runtime boundary where projection semantics exist but repo-native manual commands remain deferred

Primary sources to keep explicit:

- `E:\Projects\WorkDataHub\src\work_data_hub\cli\__main__.py`
- `E:\Projects\WorkDataHub\src\work_data_hub\cli\customer_mdm\sync.py`
- `E:\Projects\WorkDataHub\src\work_data_hub\cli\customer_mdm\snapshot.py`
- `E:\Projects\WorkDataHub\src\work_data_hub\cli\customer_mdm\init_year.py`
- `E:\Projects\WorkDataHub\src\work_data_hub\cli\customer_mdm\validate.py`
- `E:\Projects\WorkDataHub\src\work_data_hub\cli\customer_mdm\cutover.py`
- `E:\Projects\WorkDataHub\docs\deployment_run_guide.md`
- `docs/superpowers/specs/2026-04-11-workdatahubpro-refactor-program.md`
- `docs/superpowers/specs/2026-04-11-workdatahubpro-first-wave-legacy-coverage-matrix.md`
- `src/work_data_hub_pro/apps/etl_cli/main.py`

The page must make clear:

- legacy manual `customer-mdm` commands are real operator surfaces
- `sync`, `snapshot`, `init-year`, and `cutover` are write surfaces; `validate` is read-only
- manual commands are recovery / recompute surfaces, not the default monthly primary trigger when the hook chain is available
- current accepted runtime proves projection semantics without admitting repo-native manual command surfaces

- [ ] **Step 2: Tighten the surface page**

Update `docs/wiki-bi/surfaces/customer-mdm-commands.md` so it remains the governing surface page but delegates detailed runtime/current-boundary evidence to the new object-level evidence page.

- [ ] **Step 3: Reconnect the lifecycle evidence page**

Update `docs/wiki-bi/evidence/customer-mdm-lifecycle-evidence.md` so it routes to the new manual-runtime evidence page for operator boundary details instead of carrying all runtime-closure implications itself.

### Task 2: Create The Enterprise Persistence Evidence Route

**Files:**
- Create: `docs/wiki-bi/evidence/enterprise-enrichment-persistence-evidence.md`
- Modify: `docs/wiki-bi/surfaces/enterprise-enrichment-persistence.md`
- Modify: `docs/wiki-bi/evidence/identity-and-lookup-evidence.md`
- Modify: `docs/wiki-bi/standards/semantic-correctness/identity-governance.md`

- [ ] **Step 1: Create the new evidence page**

Write `docs/wiki-bi/evidence/enterprise-enrichment-persistence-evidence.md`.

The page must aggregate:

- cache and queue persistence (`enrichment_index`, `company_name_index`, `enrichment_requests`)
- provider-retention root (`base_info`)
- downstream normalized / parsed persistence (`business_info`, `biz_label`)
- current accepted runtime boundary where identity behavior is protected without repo-native persistence surfaces

Primary sources to keep explicit:

- `E:\Projects\WorkDataHub\src\work_data_hub\infrastructure\enrichment\repository\enrichment_index_ops.py`
- `E:\Projects\WorkDataHub\src\work_data_hub\infrastructure\enrichment\repository\other_ops.py`
- `E:\Projects\WorkDataHub\src\work_data_hub\infrastructure\enrichment\business_info_repository.py`
- `E:\Projects\WorkDataHub\src\work_data_hub\infrastructure\enrichment\biz_label_repository.py`
- `E:\Projects\WorkDataHub\src\work_data_hub\infrastructure\enrichment\data_refresh_service.py`
- `docs/superpowers/specs/2026-04-11-workdatahubpro-refactor-program.md`
- `docs/superpowers/specs/2026-04-11-workdatahubpro-first-wave-legacy-coverage-matrix.md`
- `src/work_data_hub_pro/capabilities/identity_resolution/service.py`

The page must make clear:

- `enrichment_index` / `company_name_index` and `enrichment_requests` are not the same persistence role as `base_info`
- `base_info` is the provider-retention root while `business_info` / `biz_label` are downstream normalized or parsed persistence
- current accepted runtime protects the identity behavior chain, not the full legacy persistence footprint
- deferred persistence should remain explicit rather than silently promoted to active runtime

- [ ] **Step 2: Tighten the surface page**

Update `docs/wiki-bi/surfaces/enterprise-enrichment-persistence.md` so it delegates detailed layering and current-boundary evidence to the new evidence page.

- [ ] **Step 3: Reconnect identity-governance routes**

Update:

- `docs/wiki-bi/evidence/identity-and-lookup-evidence.md`
- `docs/wiki-bi/standards/semantic-correctness/identity-governance.md`

The intended result is:

- identity-governance pages have a direct route to the new persistence evidence
- cache / queue / provider persistence is no longer only a side mention inside broader identity text

### Task 3: Reconnect The Aggregate Surface Dispatcher

**Files:**
- Modify: `docs/wiki-bi/evidence/operator-and-surface-evidence.md`

- [ ] **Step 1: Tighten the aggregate evidence page**

Update `docs/wiki-bi/evidence/operator-and-surface-evidence.md` so:

- manual `customer-mdm` commands route to the new evidence page for current-boundary detail
- enterprise persistence routes to the new evidence page for cache/queue/provider layering detail
- the aggregate page remains a dispatcher, not a duplicate copy of the new pages

### Task 4: Write Back Round 36 Navigation And Sediment

**Files:**
- Create: `docs/wiki-bi/_meta/absorption-rounds/round-36-manual-customer-mdm-and-persistence-closure.md`
- Modify: `docs/wiki-bi/index.md`
- Modify: `docs/wiki-bi/log.md`
- Modify: `docs/wiki-bi/_meta/absorption-rounds/index.md`
- Modify: `docs/wiki-bi/_meta/wiki-absorption-roadmap.md`

- [ ] **Step 1: Update the main index**

In `docs/wiki-bi/index.md`:

- add discoverable FAQ / maintainer routes for manual `customer-mdm` runtime and enterprise persistence layering
- register the two new evidence pages in the evidence catalog
- keep the current index structure intact

- [ ] **Step 2: Create the Round 36 sediment note**

Write `docs/wiki-bi/_meta/absorption-rounds/round-36-manual-customer-mdm-and-persistence-closure.md` documenting:

- why this round focused on manual `customer-mdm` runtime and enterprise persistence rather than queue/runtime re-admission
- what is now stable
- what remains deferred

- [ ] **Step 3: Update roadmap/index metadata and append the log**

Update:

- `docs/wiki-bi/_meta/absorption-rounds/index.md`
- `docs/wiki-bi/_meta/wiki-absorption-roadmap.md`
- `docs/wiki-bi/log.md`

The updates must show:

- Round 36 completed
- manual `customer-mdm` and enterprise persistence now have object-level evidence routes
- repo-native runtime re-admission still remains deferred
- the next likely follow-on shifts to `company_lookup_queue` retry/runtime closure, standalone tooling closure, or another explicit runtime/operator decision package rather than another nearby business-semantics object

## Validation Steps

- [ ] Run reachability and keyword checks:
  - `rg -n "customer-mdm|enrichment_index|enrichment_requests|base_info|business_info|biz_label" docs/wiki-bi`
- [ ] Review only the intended docs diff:
  - `git diff -- docs/wiki-bi docs/superpowers/plans`
- [ ] Run formatting/sanity check:
  - `git diff --check`
- [ ] Re-run the full suite after the docs round completes:
  - `uv run pytest -v`
  - Expected: still green with `292 passed`

## Completion Criteria

This round is complete when:

- manual `customer-mdm` runtime boundaries no longer rely only on the surface page and lifecycle evidence to be understood
- enterprise enrichment persistence layering no longer relies only on aggregate surface text to be understood
- the wiki can directly answer why both surfaces remain governed even though repo-native current runtime stays deferred
- Round 36 navigation and sediment are written back in `index.md`, `log.md`, and `_meta/absorption-rounds/`
- validation keeps the repo green

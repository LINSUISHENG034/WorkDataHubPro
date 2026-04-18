# WorkDataHubPro Wiki BI Round 31 Closeout Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Increase legacy business-semantics coverage in `docs/wiki-bi/` by absorbing the still-missing relationship-breadth object `关联机构数`, promoting `管理资格` into a durable concept page, and tightening the dispatcher-level treatment of `其他年金计划` / `其他开拓机构` / `组合代码`.

**Architecture:** Keep the current object-first wiki maintenance pattern. Update the two existing dispatcher evidence pages first, promote only the highest-value remaining misunderstood objects into concept pages, reconnect the affected concept/contract/evidence entry points, then write back round sediment so the absorption story remains discoverable without creating a broad duplicate summary page.

**Tech Stack:** Markdown in `docs/wiki-bi/` and `docs/superpowers/plans/`, legacy evidence from `E:\Projects\WorkDataHub`, PowerShell, `rg`, git worktrees, `uv`, `pytest`

---

## Scope Check

This plan covers:

- one new relationship-breadth concept page for `关联机构数`
- one new classification-family concept page for `管理资格`
- tightening `customer-master-signals-evidence.md` so relationship-breadth signals are explicitly split into dominant, breadth-count, and breadth-list layers
- tightening `classification-family-evidence.md` so `管理资格` and `组合代码` no longer read like the same object family role
- reconnecting the new concepts from the most relevant concept, field-processing, domain, and output-contract pages
- updating `index.md`, `log.md`, `wiki-absorption-roadmap.md`, and `absorption-rounds/index.md`
- adding a Round 31 sediment note

This plan does not cover:

- creating standalone concept pages for `其他年金计划`, `其他开拓机构`, or `组合代码`
- semantic-map registry mutation or wave closeout
- runtime/operator discovery topics such as `company_lookup_queue`, `reference_sync`, or `customer-mdm` command runtime
- changes under `src/` or `config/`

## Suggested Branch

- `docs/wiki-round-31`

## Baseline Note

The isolated worktree already exists at `E:\Projects\WorkDataHubPro\.worktrees\docs-wiki-round-31` on branch `docs/wiki-round-31`.

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

- `docs/wiki-bi/concepts/related-branch-count.md`
- `docs/wiki-bi/concepts/management-qualification.md`
- `docs/wiki-bi/_meta/absorption-rounds/round-31-relationship-breadth-and-classification-closeout.md`

## Files To Modify

- `docs/wiki-bi/evidence/customer-master-signals-evidence.md`
- `docs/wiki-bi/evidence/classification-family-evidence.md`
- `docs/wiki-bi/concepts/backfill.md`
- `docs/wiki-bi/concepts/primary-branch.md`
- `docs/wiki-bi/concepts/related-plan-count.md`
- `docs/wiki-bi/concepts/plan-type.md`
- `docs/wiki-bi/evidence/annuity-performance-field-processing-evidence.md`
- `docs/wiki-bi/evidence/annuity-income-field-processing-evidence.md`
- `docs/wiki-bi/evidence/annual-loss-field-processing-evidence.md`
- `docs/wiki-bi/domains/annuity-performance.md`
- `docs/wiki-bi/domains/annuity-income.md`
- `docs/wiki-bi/standards/output-correctness/annuity-performance-output-contract.md`
- `docs/wiki-bi/standards/output-correctness/annuity-income-output-contract.md`
- `docs/wiki-bi/standards/output-correctness/annual-award-output-contract.md`
- `docs/wiki-bi/standards/output-correctness/annual-loss-output-contract.md`
- `docs/wiki-bi/index.md`
- `docs/wiki-bi/log.md`
- `docs/wiki-bi/_meta/absorption-rounds/index.md`
- `docs/wiki-bi/_meta/wiki-absorption-roadmap.md`

### Task 1: Promote `关联机构数` And Tighten The Relationship-Breadth Family

**Files:**
- Create: `docs/wiki-bi/concepts/related-branch-count.md`
- Modify: `docs/wiki-bi/evidence/customer-master-signals-evidence.md`
- Modify: `docs/wiki-bi/concepts/related-plan-count.md`
- Modify: `docs/wiki-bi/concepts/primary-branch.md`
- Modify: `docs/wiki-bi/concepts/backfill.md`

- [x] **Step 1: Tighten the customer-master signal dispatcher**

Update `docs/wiki-bi/evidence/customer-master-signals-evidence.md` so it explicitly distinguishes:

- dominant-value signals: `主拓机构`, `关键年金计划`
- breadth-count signals: `关联计划数`, `关联机构数`
- breadth-list signals: `其他年金计划`, `其他开拓机构`
- classification/history signals: `年金客户类型`, `tags`

The page must still preserve the standard evidence skeleton and make clear that:

- `关联机构数` is a stable legacy output and is not just an omitted sibling of `关联计划数`
- `其他年金计划` and `其他开拓机构` remain dispatcher-level explanation objects this round
- `关联机构数` answers count-of-branches breadth, not dominant branch ownership and not the concrete branch list itself

Primary sources to keep explicit in the evidence page:

- `E:\Projects\WorkDataHub\config\foreign_keys.yml`
- `E:\Projects\WorkDataHub\docs\verification_guide_real_data.md`
- `E:\Projects\WorkDataHub\docs\domains\annuity_performance-capability-map.md`
- `E:\Projects\WorkDataHub\docs\domains\annuity_income-capability-map.md`
- `E:\Projects\WorkDataHub\docs\domains\annual_award-capability-map.md`
- `E:\Projects\WorkDataHub\docs\domains\annual_loss-capability-map.md`

- [x] **Step 2: Create `related-branch-count.md`**

Write `docs/wiki-bi/concepts/related-branch-count.md` with title `# 关联机构数`.

The page must answer:

- what `关联机构数` means in customer-master semantics
- why it is a relationship-breadth count signal rather than a dominant-value signal
- why it should not be confused with `主拓机构`
- why it should not be confused with `其他开拓机构`
- why it belongs beside `关联计划数` without duplicating that page

The page must link back to:

- `./backfill.md`
- `./primary-branch.md`
- `./related-plan-count.md`
- `../evidence/customer-master-signals-evidence.md`

- [x] **Step 3: Reconnect the adjacent relationship-breadth concepts**

Update:

- `docs/wiki-bi/concepts/related-plan-count.md`
- `docs/wiki-bi/concepts/primary-branch.md`
- `docs/wiki-bi/concepts/backfill.md`

The intended result is:

- `关联计划数` and `关联机构数` read as sibling breadth-count objects
- `主拓机构` is clearly separated from institution breadth
- `backfill` now points to both breadth-count concepts without turning into a summary hub

### Task 2: Promote `管理资格` And Tighten The Classification Family

**Files:**
- Create: `docs/wiki-bi/concepts/management-qualification.md`
- Modify: `docs/wiki-bi/evidence/classification-family-evidence.md`
- Modify: `docs/wiki-bi/concepts/plan-type.md`
- Modify: `docs/wiki-bi/evidence/annuity-performance-field-processing-evidence.md`
- Modify: `docs/wiki-bi/evidence/annuity-income-field-processing-evidence.md`
- Modify: `docs/wiki-bi/evidence/annual-loss-field-processing-evidence.md`

- [x] **Step 1: Tighten the classification dispatcher**

Update `docs/wiki-bi/evidence/classification-family-evidence.md` so it makes the layered roles more explicit:

- input interpretation anchor: `计划类型`
- downstream explanation anchor: `业务类型`
- customer-master aggregated classification: `年金计划类型`, `管理资格`
- portfolio anchor: `组合代码`

The page must make clear that:

- `管理资格` is a customer-master aggregation result derived through `concat_distinct`
- `管理资格` is not a raw copy of one fact row’s `业务类型`
- `组合代码` remains a portfolio/classification anchor, not an enterprise identity or customer-master classification synonym

Primary sources to keep explicit in the evidence page:

- `E:\Projects\WorkDataHub\config\foreign_keys.yml`
- `E:\Projects\WorkDataHub\docs\business-background\年金计划类型与客户名称业务背景.md`
- `E:\Projects\WorkDataHub\docs\cleansing-rules\annuity-performance.md`
- `E:\Projects\WorkDataHub\docs\cleansing-rules\annuity-income.md`
- `E:\Projects\WorkDataHub\docs\verification_guide_real_data.md`
- `E:\Projects\WorkDataHub\docs\guides\infrastructure\backfill-mechanism-guide.md`

- [x] **Step 2: Create `management-qualification.md`**

Write `docs/wiki-bi/concepts/management-qualification.md` with title `# 管理资格`.

The page must answer:

- what `管理资格` means in customer-master semantics
- why it is an aggregated classification rather than an input-side raw field
- why it should not be collapsed into `业务类型`
- why it belongs in the same family as `年金计划类型` without becoming the same object

The page must link back to:

- `./plan-type.md`
- `./backfill.md`
- `../evidence/classification-family-evidence.md`

- [x] **Step 3: Reconnect the field-processing and concept entry points**

Update:

- `docs/wiki-bi/concepts/plan-type.md`
- `docs/wiki-bi/evidence/annuity-performance-field-processing-evidence.md`
- `docs/wiki-bi/evidence/annuity-income-field-processing-evidence.md`
- `docs/wiki-bi/evidence/annual-loss-field-processing-evidence.md`

The intended result is:

- the classification family no longer routes only through the dispatcher
- `管理资格` is directly reachable from the pages that already explain the layered field family
- `组合代码` remains connected as a sibling anchor but intentionally stays out of concept-page promotion this round

### Task 3: Reconnect High-Traffic Domain And Contract Entry Points

**Files:**
- Modify: `docs/wiki-bi/domains/annuity-performance.md`
- Modify: `docs/wiki-bi/domains/annuity-income.md`
- Modify: `docs/wiki-bi/standards/output-correctness/annuity-performance-output-contract.md`
- Modify: `docs/wiki-bi/standards/output-correctness/annuity-income-output-contract.md`
- Modify: `docs/wiki-bi/standards/output-correctness/annual-award-output-contract.md`
- Modify: `docs/wiki-bi/standards/output-correctness/annual-loss-output-contract.md`

- [x] **Step 1: Tighten the highest-traffic domains**

Update:

- `docs/wiki-bi/domains/annuity-performance.md`
- `docs/wiki-bi/domains/annuity-income.md`

These pages should route readers to:

- `关联机构数` as the institution-side breadth sibling of `关联计划数`
- `管理资格` through the classification family path

Do not broaden the domain pages into field-by-field summaries.

- [x] **Step 2: Tighten the output contracts**

Update:

- `docs/wiki-bi/standards/output-correctness/annuity-performance-output-contract.md`
- `docs/wiki-bi/standards/output-correctness/annuity-income-output-contract.md`
- `docs/wiki-bi/standards/output-correctness/annual-award-output-contract.md`
- `docs/wiki-bi/standards/output-correctness/annual-loss-output-contract.md`

The intended result is:

- customer-master signal families explicitly distinguish dominant values, breadth counts, breadth lists, and classification outputs
- `关联机构数` is acknowledged where `关联计划数` and `其他开拓机构` semantics are already in play
- `管理资格` is treated as a governed classification result rather than an implied implementation detail

### Task 4: Write Back Round 31 Navigation And Sediment

**Files:**
- Create: `docs/wiki-bi/_meta/absorption-rounds/round-31-relationship-breadth-and-classification-closeout.md`
- Modify: `docs/wiki-bi/index.md`
- Modify: `docs/wiki-bi/log.md`
- Modify: `docs/wiki-bi/_meta/absorption-rounds/index.md`
- Modify: `docs/wiki-bi/_meta/wiki-absorption-roadmap.md`

- [x] **Step 1: Update the main index**

In `docs/wiki-bi/index.md`:

- add discoverable entry points for `关联机构数` and `管理资格`
- register the new concept pages in the concepts catalog
- keep the current index structure intact

- [x] **Step 2: Create the Round 31 sediment note**

Write `docs/wiki-bi/_meta/absorption-rounds/round-31-relationship-breadth-and-classification-closeout.md` documenting:

- why `关联机构数` and `管理资格` were promoted now
- which pages were updated
- which objects intentionally remain deferred (`其他年金计划`, `其他开拓机构`, `组合代码`)
- why this round still remains in business-semantics scope rather than reopening runtime/operator discovery

- [x] **Step 3: Update roadmap/index metadata and append the log**

Update:

- `docs/wiki-bi/_meta/absorption-rounds/index.md`
- `docs/wiki-bi/_meta/wiki-absorption-roadmap.md`
- `docs/wiki-bi/log.md`

The updates must show:

- Round 31 completed
- `关联机构数` and `管理资格` are no longer only dispatcher-level mentions
- `其他年金计划`, `其他开拓机构`, and `组合代码` remain the follow-on candidates after Round 31
- the next stage after Round 31 still returns to semantic-map-first runtime/operator discovery unless a later raw-source sweep proves another business-semantic object is promotion-ready

## Validation Steps

- [x] Run reachability and keyword checks:
  - `rg -n "关联机构数|管理资格|其他年金计划|其他开拓机构|组合代码|主拓机构|关联计划数" docs/wiki-bi`
- [x] Review only the intended docs diff:
  - `git diff -- docs/wiki-bi docs/superpowers/plans`
- [x] Run formatting/sanity check:
  - `git diff --check`
- [x] Re-run the full suite after the docs round completes:
  - `uv run pytest -v`
  - Expected: the same 4 pre-existing failures remain; no new failures introduced by Round 31

## Completion Criteria

This round is complete when:

- `关联机构数` is no longer absent from durable wiki coverage
- `管理资格` is no longer only a dispatcher-level classification mention
- the wiki can directly answer how `关联机构数` differs from `主拓机构` and `其他开拓机构`
- the wiki can directly answer how `管理资格` differs from `业务类型` and `组合代码`
- high-traffic customer-master and classification entry points route to the new concept pages
- Round 31 navigation and sediment are written back in `index.md`, `log.md`, and `_meta/absorption-rounds/`
- validation shows no new failures beyond the known pre-existing baseline failures

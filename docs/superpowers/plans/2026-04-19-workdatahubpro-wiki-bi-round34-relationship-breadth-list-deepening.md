# WorkDataHubPro Wiki BI Round 34 Relationship-Breadth List Deepening Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Increase legacy business-semantics coverage in `docs/wiki-bi/` by promoting the still-dispatcher-only relationship-breadth list signals `其他年金计划` and `其他开拓机构` into durable concept pages, then reconnect the surrounding signal-family pages so dominant value, breadth count, and breadth list semantics can be answered directly.

**Architecture:** Keep the current object-first wiki maintenance pattern. Tighten the existing customer-master signal dispatcher first, promote only the two remaining relationship-breadth list objects that now have enough legacy evidence and repeated reader value, reconnect the adjacent concept/domain/output-contract entry points, then write back round sediment so the new coverage is discoverable without creating another broad summary page.

**Tech Stack:** Markdown in `docs/wiki-bi/` and `docs/superpowers/plans/`, legacy evidence from `E:\Projects\WorkDataHub`, PowerShell, `rg`, git worktrees, `uv`, `pytest`

---

## Scope Check

This plan covers:

- one new relationship-breadth list concept page for `其他年金计划`
- one new relationship-breadth list concept page for `其他开拓机构`
- tightening `customer-master-signals-evidence.md` so dominant value, breadth count, and breadth list layers are explicit and symmetric
- reconnecting the new concepts from adjacent customer-master signal concepts, high-traffic domains, and output-contract pages
- updating `index.md`, `log.md`, `wiki-absorption-roadmap.md`, and `absorption-rounds/index.md`
- adding a Round 34 sediment note

This plan does not cover:

- promoting `组合代码` into a standalone concept page
- creating a standalone `is_churned_this_year` object page
- `manual customer-mdm`, enterprise persistence, `company_lookup_queue`, or `reference_sync` runtime/surface closure
- changes under `src/`, `config/`, or `tests/`

## Suggested Branch

- `docs/wiki-bi-round34`

## Baseline Note

The isolated worktree exists at `E:\Projects\WorkDataHubPro\.worktrees\docs-wiki-bi-round34` on branch `docs/wiki-bi-round34`.

Baseline environment check:

- `uv sync --dev` completed successfully in the worktree.
- `uv run pytest -v` currently passes cleanly: `292 passed`.
- The worktree is clean after environment sync and generated build artifacts were removed.

This round should keep that clean validation posture.

## Files To Create

- `docs/wiki-bi/concepts/other-annuity-plans.md`
- `docs/wiki-bi/concepts/other-branches.md`
- `docs/wiki-bi/_meta/absorption-rounds/round-34-relationship-breadth-list-deepening.md`

## Files To Modify

- `docs/wiki-bi/evidence/customer-master-signals-evidence.md`
- `docs/wiki-bi/concepts/backfill.md`
- `docs/wiki-bi/concepts/key-annuity-plan.md`
- `docs/wiki-bi/concepts/primary-branch.md`
- `docs/wiki-bi/concepts/related-plan-count.md`
- `docs/wiki-bi/concepts/related-branch-count.md`
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

### Task 1: Tighten The Dispatcher And Promote Breadth-List Objects

**Files:**
- Create: `docs/wiki-bi/concepts/other-annuity-plans.md`
- Create: `docs/wiki-bi/concepts/other-branches.md`
- Modify: `docs/wiki-bi/evidence/customer-master-signals-evidence.md`

- [ ] **Step 1: Tighten the customer-master signal dispatcher**

Update `docs/wiki-bi/evidence/customer-master-signals-evidence.md` so the signal family is expressed as four explicit layers:

- dominant-value signals: `主拓机构`, `关键年金计划`
- breadth-count signals: `关联计划数`, `关联机构数`
- breadth-list signals: `其他年金计划`, `其他开拓机构`
- classification/history signals: `年金客户类型`, `tags`

The page must make clear that:

- `其他年金计划` is the list-sibling of `关键年金计划` and `关联计划数`, not a noisy duplicate of either one
- `其他开拓机构` is the list-sibling of `主拓机构` and `关联机构数`, not a dominant-branch claim
- both list objects are formal legacy outputs, not incidental string formatting artifacts
- Round 34 promotes only the two breadth-list objects; `组合代码` stays outside this round

Primary sources to keep explicit:

- `E:\Projects\WorkDataHub\config\foreign_keys.yml`
- `E:\Projects\WorkDataHub\docs\verification_guide_real_data.md`
- `E:\Projects\WorkDataHub\docs\domains\annuity_performance-capability-map.md`
- `E:\Projects\WorkDataHub\docs\domains\annuity_income-capability-map.md`
- `E:\Projects\WorkDataHub\docs\domains\annual_award-capability-map.md`
- `E:\Projects\WorkDataHub\docs\domains\annual_loss-capability-map.md`

- [ ] **Step 2: Create `other-annuity-plans.md`**

Write `docs/wiki-bi/concepts/other-annuity-plans.md` with title `# 其他年金计划`.

The page must answer:

- what `其他年金计划` means in customer-master semantics
- why it is a breadth-list signal rather than a dominant-value signal
- why it should not be confused with `关键年金计划`
- why it should not be collapsed into `关联计划数`
- why it belongs beside those two plan-side objects without duplicating them

The page must link back to:

- `./backfill.md`
- `./key-annuity-plan.md`
- `./related-plan-count.md`
- `../evidence/customer-master-signals-evidence.md`

- [ ] **Step 3: Create `other-branches.md`**

Write `docs/wiki-bi/concepts/other-branches.md` with title `# 其他开拓机构`.

The page must answer:

- what `其他开拓机构` means in customer-master semantics
- why it is a breadth-list signal rather than a dominant-value signal
- why it should not be confused with `主拓机构`
- why it should not be collapsed into `关联机构数`
- why it belongs beside those two branch-side objects without duplicating them

The page must link back to:

- `./backfill.md`
- `./primary-branch.md`
- `./related-branch-count.md`
- `../evidence/customer-master-signals-evidence.md`

### Task 2: Reconnect The Adjacent Signal Family Pages

**Files:**
- Modify: `docs/wiki-bi/concepts/backfill.md`
- Modify: `docs/wiki-bi/concepts/key-annuity-plan.md`
- Modify: `docs/wiki-bi/concepts/primary-branch.md`
- Modify: `docs/wiki-bi/concepts/related-plan-count.md`
- Modify: `docs/wiki-bi/concepts/related-branch-count.md`

- [ ] **Step 1: Tighten the plan-side signal family**

Update:

- `docs/wiki-bi/concepts/key-annuity-plan.md`
- `docs/wiki-bi/concepts/related-plan-count.md`

The intended result is:

- `关键年金计划` reads as dominant-value anchor
- `关联计划数` reads as breadth-count anchor
- `其他年金计划` reads as breadth-list anchor
- all three pages explicitly separate dominant vs count vs list semantics

- [ ] **Step 2: Tighten the branch-side signal family**

Update:

- `docs/wiki-bi/concepts/primary-branch.md`
- `docs/wiki-bi/concepts/related-branch-count.md`

The intended result is:

- `主拓机构` reads as dominant-value anchor
- `关联机构数` reads as breadth-count anchor
- `其他开拓机构` reads as breadth-list anchor
- all three pages explicitly separate dominant vs count vs list semantics

- [ ] **Step 3: Reconnect `backfill` without turning it into a summary hub**

Update `docs/wiki-bi/concepts/backfill.md` so it now points to both new breadth-list concept pages alongside the existing dominant/count objects, while still preserving the page’s current role as boundary explanation rather than field catalog.

### Task 3: Reconnect High-Traffic Domain And Contract Entry Points

**Files:**
- Modify: `docs/wiki-bi/domains/annuity-performance.md`
- Modify: `docs/wiki-bi/domains/annuity-income.md`
- Modify: `docs/wiki-bi/standards/output-correctness/annuity-performance-output-contract.md`
- Modify: `docs/wiki-bi/standards/output-correctness/annuity-income-output-contract.md`
- Modify: `docs/wiki-bi/standards/output-correctness/annual-award-output-contract.md`
- Modify: `docs/wiki-bi/standards/output-correctness/annual-loss-output-contract.md`

- [ ] **Step 1: Tighten the two highest-traffic domains**

Update:

- `docs/wiki-bi/domains/annuity-performance.md`
- `docs/wiki-bi/domains/annuity-income.md`

These pages should route readers to the new breadth-list concept pages where the surrounding signal family is already discussed. Do not broaden the domain pages into field-by-field walkthroughs.

- [ ] **Step 2: Tighten the output contracts**

Update:

- `docs/wiki-bi/standards/output-correctness/annuity-performance-output-contract.md`
- `docs/wiki-bi/standards/output-correctness/annuity-income-output-contract.md`
- `docs/wiki-bi/standards/output-correctness/annual-award-output-contract.md`
- `docs/wiki-bi/standards/output-correctness/annual-loss-output-contract.md`

The intended result is:

- customer-master signal families explicitly distinguish dominant values, breadth counts, and breadth lists
- `其他年金计划` and `其他开拓机构` are treated as governed outputs, not implied leftover strings
- cross-domain references point back to the new concept pages instead of stopping at the dispatcher

### Task 4: Write Back Round 34 Navigation And Sediment

**Files:**
- Create: `docs/wiki-bi/_meta/absorption-rounds/round-34-relationship-breadth-list-deepening.md`
- Modify: `docs/wiki-bi/index.md`
- Modify: `docs/wiki-bi/log.md`
- Modify: `docs/wiki-bi/_meta/absorption-rounds/index.md`
- Modify: `docs/wiki-bi/_meta/wiki-absorption-roadmap.md`

- [ ] **Step 1: Update the main index**

In `docs/wiki-bi/index.md`:

- add discoverable FAQ or maintainer entry points for the two new breadth-list objects
- register both concept pages in the concepts catalog
- keep the current index structure intact

- [ ] **Step 2: Create the Round 34 sediment note**

Write `docs/wiki-bi/_meta/absorption-rounds/round-34-relationship-breadth-list-deepening.md` documenting:

- why the two breadth-list objects were promotion-ready now
- which pages were updated
- why `组合代码` remains deferred to a later classification/portfolio wave
- why this round still remains in business-semantics scope rather than reopening runtime/operator discovery

- [ ] **Step 3: Update roadmap/index metadata and append the log**

Update:

- `docs/wiki-bi/_meta/absorption-rounds/index.md`
- `docs/wiki-bi/_meta/wiki-absorption-roadmap.md`
- `docs/wiki-bi/log.md`

The updates must show:

- Round 34 completed
- the relationship-breadth family now covers dominant value, breadth count, and breadth list on both plan and branch sides
- `组合代码` remains the main business-semantics follow-on candidate
- the next likely wave after this round is either `组合代码` / portfolio-anchor tightening or a return to manual `customer-mdm` / enterprise persistence discovery

## Validation Steps

- [ ] Run reachability and keyword checks:
  - `rg -n "其他年金计划|其他开拓机构|关键年金计划|主拓机构|关联计划数|关联机构数" docs/wiki-bi`
- [ ] Review only the intended docs diff:
  - `git diff -- docs/wiki-bi docs/superpowers/plans`
- [ ] Run formatting/sanity check:
  - `git diff --check`
- [ ] Re-run the full suite after the docs round completes:
  - `uv run pytest -v`
  - Expected: still green with `292 passed`

## Completion Criteria

This round is complete when:

- `其他年金计划` is no longer only a dispatcher-level mention
- `其他开拓机构` is no longer only a dispatcher-level mention
- the wiki can directly answer how the plan-side signal family separates dominant value, breadth count, and breadth list
- the wiki can directly answer how the branch-side signal family separates dominant value, breadth count, and breadth list
- high-traffic domain and output-contract entry points route to the new concept pages
- Round 34 navigation and sediment are written back in `index.md`, `log.md`, and `_meta/absorption-rounds/`
- validation keeps the repo green

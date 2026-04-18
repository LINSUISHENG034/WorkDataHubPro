# WorkDataHubPro Wiki BI Round 30 Relationship Breadth Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Increase legacy business-semantics coverage in `docs/wiki-bi/` by promoting `关联计划数` from a dispatcher-only relationship-breadth mention into a durable concept page that can be answered directly from the wiki.

**Architecture:** Keep the Round 29 object-first pattern. Update the existing customer-master signal dispatcher first, promote only `关联计划数` into a concept page, reconnect the related concept/contract/domain entry points, then write back navigation and round sediment so Round 30 is discoverable without opening a new broad summary layer.

**Tech Stack:** Markdown in `docs/wiki-bi/` and `docs/superpowers/plans/`, legacy evidence from `E:\Projects\WorkDataHub`, PowerShell, `rg`, git worktrees, `uv`, `pytest`

---

## Scope Check

This plan covers:

- one new concept page for `关联计划数`
- tightening `customer-master-signals-evidence.md` so relationship-breadth signals are more explicitly separated
- reconnecting the new concept from the most relevant concept, domain, and output-contract pages
- updating `index.md`, `log.md`, `wiki-absorption-roadmap.md`, and `absorption-rounds/index.md`
- adding a Round 30 sediment note

This plan does not cover:

- `其他年金计划` or `其他开拓机构` as standalone concept pages
- `管理资格` or `组合代码` object promotion
- runtime/operator discovery topics such as `company_lookup_queue`, `reference_sync`, or `customer-mdm` command runtime
- changes under `src/`, `tests/`, or `config/`

## Suggested Branch

- `docs/wiki-bi-round30-breadth`

## Baseline Note

The isolated worktree already exists at `E:\Projects\WorkDataHubPro\.worktrees\docs-wiki-bi-round30-breadth` on branch `docs/wiki-bi-round30-breadth`.

Baseline environment check:

- `uv sync --dev` completed successfully in the worktree.
- `uv run pytest -v` currently has **2 pre-existing failures** unrelated to this docs scope:
  - `tests/contracts/test_legacy_semantic_map_first_wave_pilot.py::test_first_wave_pilot_repo_state_is_populated_and_real_evidence_backed`
  - `tests/integration/test_legacy_semantic_map_first_wave_pilot_flow.py::test_run_first_wave_pilot_rebuilds_active_successor_wave_deterministically`
- Both failures currently expect the active successor wave to compile `7` claims while the checked-in repository now compiles `9`.

This round must not claim those failures were introduced by the docs changes.

## Files To Create

- `docs/wiki-bi/concepts/related-plan-count.md`
- `docs/wiki-bi/_meta/absorption-rounds/round-30-relationship-breadth-deepening.md`

## Files To Modify

- `docs/wiki-bi/evidence/customer-master-signals-evidence.md`
- `docs/wiki-bi/concepts/backfill.md`
- `docs/wiki-bi/concepts/key-annuity-plan.md`
- `docs/wiki-bi/domains/annuity-performance.md`
- `docs/wiki-bi/domains/annuity-income.md`
- `docs/wiki-bi/standards/output-correctness/annuity-performance-output-contract.md`
- `docs/wiki-bi/standards/output-correctness/annuity-income-output-contract.md`
- `docs/wiki-bi/index.md`
- `docs/wiki-bi/log.md`
- `docs/wiki-bi/_meta/absorption-rounds/index.md`
- `docs/wiki-bi/_meta/wiki-absorption-roadmap.md`

### Task 1: Promote `关联计划数` Into A Durable Concept Page

**Files:**
- Create: `docs/wiki-bi/concepts/related-plan-count.md`
- Modify: `docs/wiki-bi/evidence/customer-master-signals-evidence.md`

- [ ] **Step 1: Tighten the customer-master signal dispatcher**

Update `docs/wiki-bi/evidence/customer-master-signals-evidence.md` so it explicitly distinguishes:

- dominant-value signals: `主拓机构`, `关键年金计划`
- relationship-breadth signals: `关联计划数`, `其他年金计划`, `其他开拓机构`
- classification/history signals: `年金客户类型`, `tags`

The page must still preserve the standard evidence skeleton and make clear that:

- `关联计划数` is the next promoted object this round
- `其他年金计划` and `其他开拓机构` remain dispatcher-level explanation objects
- `关联计划数` is not the same thing as “all plan identifiers copied out of facts”

Primary sources to keep explicit in the evidence page:

- `E:\Projects\WorkDataHub\config\foreign_keys.yml`
- `E:\Projects\WorkDataHub\docs\verification_guide_real_data.md`
- `E:\Projects\WorkDataHub\docs\domains\annuity_performance-capability-map.md`
- `E:\Projects\WorkDataHub\docs\domains\annuity_income-capability-map.md`
- `E:\Projects\WorkDataHub\docs\domains\annual_award-capability-map.md`
- `E:\Projects\WorkDataHub\docs\domains\annual_loss-capability-map.md`

- [ ] **Step 2: Create `related-plan-count.md`**

Write `docs/wiki-bi/concepts/related-plan-count.md` with title `# 关联计划数`.

The page must answer:

- what `关联计划数` means in customer-master semantics
- why it is a relationship-breadth signal rather than a dominant-value signal
- why it should not be confused with `关键年金计划`
- why it should not be confused with snapshot-side `plan_count`
- why it does not by itself enumerate the exact set of related plans

The page must link back to:

- `./backfill.md`
- `./key-annuity-plan.md`
- `../evidence/customer-master-signals-evidence.md`
- `../concepts/snapshot-granularity.md`

### Task 2: Reconnect The New Concept To Existing High-Traffic Pages

**Files:**
- Modify: `docs/wiki-bi/concepts/backfill.md`
- Modify: `docs/wiki-bi/concepts/key-annuity-plan.md`
- Modify: `docs/wiki-bi/domains/annuity-performance.md`
- Modify: `docs/wiki-bi/domains/annuity-income.md`
- Modify: `docs/wiki-bi/standards/output-correctness/annuity-performance-output-contract.md`
- Modify: `docs/wiki-bi/standards/output-correctness/annuity-income-output-contract.md`

- [ ] **Step 1: Tighten adjacent concept pages**

Update:

- `docs/wiki-bi/concepts/backfill.md`
- `docs/wiki-bi/concepts/key-annuity-plan.md`

so both pages point to `related-plan-count.md` and explain the distinction:

- `关键年金计划` = dominant plan anchor
- `关联计划数` = breadth/count signal

Do not broaden those concept pages into mini-summary hubs. Keep the edits narrow.

- [ ] **Step 2: Tighten the most relevant domain and contract entry points**

Update:

- `docs/wiki-bi/domains/annuity-performance.md`
- `docs/wiki-bi/domains/annuity-income.md`
- `docs/wiki-bi/standards/output-correctness/annuity-performance-output-contract.md`
- `docs/wiki-bi/standards/output-correctness/annuity-income-output-contract.md`

The intended result is:

- high-traffic domains that already mention `关联计划数` route the reader to the new concept page
- output contracts distinguish “dominant plan” from “relationship breadth”

Do not add the new concept to unrelated pages just for symmetry.

### Task 3: Write Back Round 30 Navigation And Sediment

**Files:**
- Create: `docs/wiki-bi/_meta/absorption-rounds/round-30-relationship-breadth-deepening.md`
- Modify: `docs/wiki-bi/index.md`
- Modify: `docs/wiki-bi/log.md`
- Modify: `docs/wiki-bi/_meta/absorption-rounds/index.md`
- Modify: `docs/wiki-bi/_meta/wiki-absorption-roadmap.md`

- [ ] **Step 1: Update the main index**

In `docs/wiki-bi/index.md`:

- add a FAQ or maintainer-entry route for `关联计划数`
- register `related-plan-count.md` in the concepts catalog
- keep the current index structure intact

- [ ] **Step 2: Create the Round 30 sediment note**

Write `docs/wiki-bi/_meta/absorption-rounds/round-30-relationship-breadth-deepening.md` documenting:

- why `关联计划数` was chosen before `其他年金计划` and `其他开拓机构`
- which pages were updated
- which relationship-breadth objects intentionally remain deferred
- why this round stays in business-semantics scope rather than reopening runtime/operator discovery

- [ ] **Step 3: Update roadmap/index metadata and append the log**

Update:

- `docs/wiki-bi/_meta/absorption-rounds/index.md`
- `docs/wiki-bi/_meta/wiki-absorption-roadmap.md`
- `docs/wiki-bi/log.md`

The updates must show:

- Round 30 completed
- follow-on relationship-breadth candidates still deferred
- next work after Round 30 remains either `管理资格` promotion or semantic-map-first runtime/operator discovery

## Validation Steps

- [ ] Run reachability and keyword checks:
  - `rg -n "关联计划数|其他年金计划|其他开拓机构|关键年金计划|plan_count" docs/wiki-bi`
- [ ] Review only the intended docs diff:
  - `git diff -- docs/wiki-bi docs/superpowers/plans`
- [ ] Run formatting/sanity check:
  - `git diff --check`
- [ ] Re-run the full suite after the docs round completes:
  - `uv run pytest -v`
  - Expected: the same 2 pre-existing semantic-map failures remain; no new failures introduced by Round 30

## Completion Criteria

This round is complete when:

- `关联计划数` is no longer only a dispatcher mention
- the wiki can directly answer how `关联计划数` differs from `关键年金计划` and snapshot `plan_count`
- high-traffic customer-master signal entry points route to the new concept page
- Round 30 navigation and sediment are written back in `index.md`, `log.md`, and `_meta/absorption-rounds/`
- validation shows no new failures beyond the known pre-existing semantic-map baseline failures

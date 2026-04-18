# WorkDataHubPro Wiki BI Customer-Master-Derived Signals Round

**Date:** 2026-04-18
**Status:** Done
**Target Repository:** `E:\Projects\WorkDataHubPro`

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Close the biggest remaining `wiki-bi` business-semantic gap by turning legacy customer-master-derived signals into durable concept and evidence pages that can answer what `tags`, `主拓机构`, `关键年金计划`, `关联计划数`, and `年金客户类型` mean without falling back to raw legacy config/code.

**Architecture:** Keep `docs/wiki-bi/` object-first. Add one cross-domain evidence dispatcher for customer-master-derived signals, add only the missing concept pages that repeatedly surface in legacy behavior (`tags`, `主拓机构`), then tighten the existing `backfill`, `customer_type`, domain, and output-contract pages so the new signal family is reachable from the main navigation and clearly separated from snapshot statuses.

**Tech Stack:** Markdown in `docs/wiki-bi/` and `docs/superpowers/plans/`, legacy evidence from `E:\Projects\WorkDataHub`, PowerShell, `rg`, git, `uv`, `pytest`

---

## Scope Check

This plan covers:

- a new cross-domain evidence page for customer-master-derived signals
- new concept pages for `tags` and `主拓机构`
- tightening `backfill` and `customer_type` so they point to the new signal family instead of carrying scattered partial explanations
- tightening four domain/output-contract entry points so they expose customer-master signal semantics as first-class business outcomes
- updating `index.md`, `log.md`, and the absorption-round metadata for a substantial maintenance round

This plan does not cover:

- a dedicated `is_churned_this_year` object split
- new runtime/operator surface adjudication beyond the customer-master signal semantics already evidenced by legacy docs/config
- a standalone `plan-code-enrichment` concept page
- changes under `src/`, `tests/`, or `config/`

## Suggested Branch

- `docs/wiki-bi-customer-master-signals`

## Baseline Note

The isolated worktree already exists at `E:\Projects\WorkDataHubPro\.worktrees\docs-wiki-bi-customer-master-signals` on branch `docs/wiki-bi-customer-master-signals`.

Baseline environment check:

- `uv sync --dev` completed successfully in the worktree.
- `uv run pytest -v` currently has **2 pre-existing failures** unrelated to this docs scope:
  - `tests/contracts/test_legacy_semantic_map_first_wave_pilot.py::test_first_wave_pilot_repo_state_is_populated_and_real_evidence_backed`
  - `tests/integration/test_legacy_semantic_map_first_wave_pilot_flow.py::test_run_first_wave_pilot_rebuilds_active_successor_wave_deterministically`
- Both failures expect the active successor wave to compile 5 claims, while the checked-in registry currently compiles 7 claims.

This round must not claim those failures were introduced by the docs change.

## Files To Create

- `docs/wiki-bi/concepts/tags.md`
- `docs/wiki-bi/concepts/primary-branch.md`
- `docs/wiki-bi/evidence/customer-master-signals-evidence.md`
- `docs/wiki-bi/_meta/absorption-rounds/round-28-customer-master-derived-signals.md`

## Files To Modify

- `docs/wiki-bi/concepts/backfill.md`
- `docs/wiki-bi/concepts/customer-type.md`
- `docs/wiki-bi/domains/annuity-performance.md`
- `docs/wiki-bi/domains/annuity-income.md`
- `docs/wiki-bi/domains/annual-award.md`
- `docs/wiki-bi/domains/annual-loss.md`
- `docs/wiki-bi/standards/output-correctness/annuity-performance-output-contract.md`
- `docs/wiki-bi/standards/output-correctness/annuity-income-output-contract.md`
- `docs/wiki-bi/standards/output-correctness/annual-award-output-contract.md`
- `docs/wiki-bi/standards/output-correctness/annual-loss-output-contract.md`
- `docs/wiki-bi/index.md`
- `docs/wiki-bi/log.md`
- `docs/wiki-bi/_meta/wiki-absorption-roadmap.md`
- `docs/wiki-bi/_meta/absorption-rounds/index.md`

### Task 1: Create The Missing Object Pages For Customer-Master Signals

**Files:**
- Create: `docs/wiki-bi/concepts/tags.md`
- Create: `docs/wiki-bi/concepts/primary-branch.md`
- Create: `docs/wiki-bi/evidence/customer-master-signals-evidence.md`

- [ ] **Step 1: Draft the new cross-domain evidence dispatcher**

Write `docs/wiki-bi/evidence/customer-master-signals-evidence.md` with the standard evidence skeleton:

- `结论主题`
- `证据记录`
- `本轮已吸收的稳定结论`
- `哪些来源是强证`
- `哪些来源只是旁证`
- `对象级分发入口`
- `当前证据缺口`

The page must explicitly cover:

- `tags` as customer-master event trail, not snapshot status
- `主拓机构` and `关键年金计划` as weighted dominant values
- `关联计划数` / `其他年金计划` / `其他开拓机构` as aggregated relationship signals
- domain-specific weighting columns from legacy (`期末资产规模`, `固费`, `计划规模`)
- the boundary between customer-master signals and snapshot-state semantics

Primary evidence sources to cite in the page:

- `E:\Projects\WorkDataHub\config\foreign_keys.yml`
- `E:\Projects\WorkDataHub\docs\verification_guide_real_data.md`
- `E:\Projects\WorkDataHub\docs\domains\annuity_performance-capability-map.md`
- `E:\Projects\WorkDataHub\docs\domains\annuity_income-capability-map.md`
- `E:\Projects\WorkDataHub\docs\domains\annual_award-capability-map.md`
- `E:\Projects\WorkDataHub\docs\domains\annual_loss-capability-map.md`
- `E:\Projects\WorkDataHub\docs\business-background\客户主数据回填与状态来源分析.md`

- [ ] **Step 2: Draft the `tags` concept page**

Write `docs/wiki-bi/concepts/tags.md` so it answers:

- what `tags` are in this project context
- why tags belong to customer-master/backfill semantics rather than snapshot status
- why `yyMM新建` / `yyMM中标` / `yyMM流失` are business-semantic signals instead of harmless formatting
- what misunderstandings to avoid when reading tags next to `is_new` / `is_winning_this_year` / `is_loss_reported`

The page must link back to:

- `concepts/backfill.md`
- `concepts/customer-type.md`
- `evidence/customer-master-signals-evidence.md`
- `standards/semantic-correctness/customer-status-semantics.md`

- [ ] **Step 3: Draft the `主拓机构` concept page**

Write `docs/wiki-bi/concepts/primary-branch.md` with the title `# 主拓机构` and make it answer:

- what object this field represents in customer/reference semantics
- why it is a weighted dominant-value decision rather than a raw source column copy
- why `主拓机构` is not the same thing as the input-side `机构名称` / `机构代码`
- why the dominant-value rule differs across domains

The page must link back to:

- `concepts/backfill.md`
- `evidence/customer-master-signals-evidence.md`
- `standards/output-correctness/annuity-performance-output-contract.md`

### Task 2: Tighten Existing Durable Pages Around The New Signal Family

**Files:**
- Modify: `docs/wiki-bi/concepts/backfill.md`
- Modify: `docs/wiki-bi/concepts/customer-type.md`
- Modify: four domain pages under `docs/wiki-bi/domains/`
- Modify: four output contracts under `docs/wiki-bi/standards/output-correctness/`

- [ ] **Step 1: Update `backfill` and `customer_type`**

In `docs/wiki-bi/concepts/backfill.md`:

- make the customer-master-derived signal family explicit
- call out `tags`, `主拓机构`, `关键年金计划`, and relationship-count signals as governed outputs
- add links to the two new concept pages and the new evidence dispatcher

In `docs/wiki-bi/concepts/customer-type.md`:

- make the temporal/categorical ambiguity more explicit
- connect `新客` / `新客*` / `中标客户` / `流失客户` to the new signal family page
- reinforce that `customer_type` and `tags` are classification/history signals, not snapshot statuses

- [ ] **Step 2: Update the four output contracts**

In each of these files:

- `annuity-performance-output-contract.md`
- `annuity-income-output-contract.md`
- `annual-award-output-contract.md`
- `annual-loss-output-contract.md`

Add concise language that points to the new customer-master signal family instead of leaving `customer_master_signal`, `customer_loss_signal`, tags, and dominant values as scattered references.

Each contract should explicitly surface the customer-master signal consequence relevant to that domain:

- `annuity_performance`: dominant values + `yyMM新建` + relationship counts
- `annuity_income`: `新客*` classification and fee-weighted dominant values
- `annual_award`: `yyMM中标` and `中标客户` classification
- `annual_loss`: `yyMM流失` and `流失客户` classification

- [ ] **Step 3: Update the four domain navigation pages**

In each of these files:

- `docs/wiki-bi/domains/annuity-performance.md`
- `docs/wiki-bi/domains/annuity-income.md`
- `docs/wiki-bi/domains/annual-award.md`
- `docs/wiki-bi/domains/annual-loss.md`

Add the new concept/evidence links only where they improve navigation. Keep the domain pages thin. Do not turn them into implementation walkthroughs.

The intended result is:

- a maintainer can enter from any high-traffic domain page
- jump to the customer-master signal explanation
- and then jump to the cross-domain evidence dispatcher

### Task 3: Write Back Navigation, Round Sediment, And Maintenance History

**Files:**
- Modify: `docs/wiki-bi/index.md`
- Modify: `docs/wiki-bi/log.md`
- Modify: `docs/wiki-bi/_meta/wiki-absorption-roadmap.md`
- Modify: `docs/wiki-bi/_meta/absorption-rounds/index.md`
- Create: `docs/wiki-bi/_meta/absorption-rounds/round-28-customer-master-derived-signals.md`

- [ ] **Step 1: Update the main index**

In `docs/wiki-bi/index.md`:

- add FAQ/navigation entries for customer-master-derived signals
- register `tags` and `主拓机构` in the concepts catalog
- register `customer-master-signals-evidence.md` in the evidence catalog
- preserve the existing navigation shape: maintainer entry -> reading intent -> FAQ cards -> full catalog

- [ ] **Step 2: Add the round note and meta links**

Create `docs/wiki-bi/_meta/absorption-rounds/round-28-customer-master-derived-signals.md` documenting:

- why this round was prioritized after Round 27
- which business-semantic gap it closes
- what pages were created/tightened
- what gaps intentionally remain out of scope (`is_churned_this_year`, broader operator/runtime closure, standalone plan-code-enrichment object page)

Then update:

- `docs/wiki-bi/_meta/absorption-rounds/index.md`
- `docs/wiki-bi/_meta/wiki-absorption-roadmap.md`

so Round 28 appears as the new completed maintenance round.

- [ ] **Step 3: Append the log entry**

Append one `log.md` entry with the exact timestamped heading format already used by the wiki.

The bullets must mention:

- the new customer-master signal evidence dispatcher
- the new `tags` and `主拓机构` concept pages
- the fact that this round tightens cross-domain customer-master semantics rather than expanding runtime/operator scope

## Validation Steps

- [ ] Run keyword reachability checks:
  - `rg -n "customer-master signal|customer-master-derived|主拓机构|yyMM中标|yyMM流失|yyMM新建|新客\*" docs/wiki-bi`
- [ ] Review only the intended docs diff:
  - `git diff -- docs/wiki-bi docs/superpowers/plans`
- [ ] Verify the new pages are reachable from `docs/wiki-bi/index.md`
- [ ] Confirm modified evidence pages still preserve the expected mini-template structure
- [ ] Re-run the full suite once after the docs round completes:
  - `uv run pytest -v`
  - Expected: the same two pre-existing semantic-map failures may remain; the docs round must not introduce new failures

## Completion Criteria

This round is complete when:

- `wiki-bi` can answer customer-master-derived signal questions without sending the reader straight to legacy config/code
- `tags` and `主拓机构` are durable object pages instead of TODO-shaped mentions
- the customer-master signal family is cross-linked from the four high-traffic domains and their output contracts
- `index.md`, `log.md`, and Round 28 sediment all reflect the new maintenance round
- final validation shows no new test regressions beyond the known pre-existing semantic-map failures

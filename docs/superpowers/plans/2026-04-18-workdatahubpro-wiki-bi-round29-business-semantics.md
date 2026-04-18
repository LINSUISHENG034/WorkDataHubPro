# WorkDataHubPro Wiki BI Round 29 Business Semantics Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Expand `docs/wiki-bi/` coverage of legacy business semantics by promoting the highest-value Round 29 objects into durable wiki pages without turning discovery-ledger material into fake product truth.

**Architecture:** Keep `docs/wiki-bi/` object-first and evidence-led. Promote only one relationship-breadth object page this round (`关键年金计划`), tighten `is_churned_this_year` inside shared status pages instead of forcing an unstable split, and introduce one cross-domain classification dispatcher so `计划类型` / `业务类型` / `管理资格` / `组合代码` / `年金计划类型` stop living only in scattered field-processing notes.

**Tech Stack:** Markdown in `docs/wiki-bi/` and `docs/superpowers/plans/`, legacy evidence from `E:\Projects\WorkDataHub`, PowerShell, `rg`, git worktrees, `uv`, `pytest`

---

## Scope Check

This plan covers:

- one new concept page for `关键年金计划`
- one new cross-domain evidence dispatcher for classification-family semantics
- tightening shared status pages so `is_churned_this_year` becomes materially more answerable without creating a premature standalone page
- tightening the customer-master signal dispatcher so relationship-breadth signals are separated more clearly
- updating navigation, round sediment, and maintenance history for a substantial Round 29 wiki change

This plan does not cover:

- `company_lookup_queue`, `reference_sync`, enterprise persistence, manual `customer-mdm` commands, or other runtime/operator closure work
- semantic-map registry/compiler/reporting plumbing
- changes under `src/`, `tests/`, or `config/`
- broad one-page summaries that duplicate existing wiki structure

## Suggested Branch

- `docs/wiki-bi-round29-business-semantics`

## Baseline Note

The isolated worktree already exists at `E:\Projects\WorkDataHubPro\.worktrees\docs-wiki-bi-round29-business-semantics` on branch `docs/wiki-bi-round29-business-semantics`.

Baseline environment check:

- `uv sync --dev` completed successfully in the worktree.
- `uv run pytest -v` currently has **2 pre-existing failures** unrelated to this docs scope:
  - `tests/contracts/test_legacy_semantic_map_first_wave_pilot.py::test_first_wave_pilot_repo_state_is_populated_and_real_evidence_backed`
  - `tests/integration/test_legacy_semantic_map_first_wave_pilot_flow.py::test_run_first_wave_pilot_rebuilds_active_successor_wave_deterministically`
- Both failures come from checked-in semantic-map successor-wave expectations on untouched branch state.

This round must not claim those failures were introduced by the docs changes.

## Files To Create

- `docs/wiki-bi/concepts/key-annuity-plan.md`
- `docs/wiki-bi/evidence/classification-family-evidence.md`

## Files To Modify

- `docs/wiki-bi/evidence/customer-master-signals-evidence.md`
- `docs/wiki-bi/concepts/backfill.md`
- `docs/wiki-bi/concepts/primary-branch.md`
- `docs/wiki-bi/concepts/customer-status.md`
- `docs/wiki-bi/standards/semantic-correctness/customer-status-semantics.md`
- `docs/wiki-bi/evidence/status-and-snapshot-evidence.md`
- `docs/wiki-bi/evidence/is-loss-reported-evidence.md`
- `docs/wiki-bi/concepts/plan-type.md`
- `docs/wiki-bi/evidence/annuity-performance-field-processing-evidence.md`
- `docs/wiki-bi/evidence/annuity-income-field-processing-evidence.md`
- `docs/wiki-bi/evidence/annual-loss-field-processing-evidence.md`
- `docs/wiki-bi/standards/output-correctness/annuity-performance-output-contract.md`
- `docs/wiki-bi/standards/output-correctness/annuity-income-output-contract.md`
- `docs/wiki-bi/index.md`
- `docs/wiki-bi/log.md`
- `docs/wiki-bi/_meta/absorption-rounds/round-29-legacy-business-semantics-expansion.md`
- `docs/wiki-bi/_meta/absorption-rounds/index.md`
- `docs/wiki-bi/_meta/wiki-absorption-roadmap.md`

### Task 1: Promote The Highest-Value Relationship-Breadth Object

**Files:**
- Create: `docs/wiki-bi/concepts/key-annuity-plan.md`
- Modify: `docs/wiki-bi/evidence/customer-master-signals-evidence.md`
- Modify: `docs/wiki-bi/concepts/backfill.md`
- Modify: `docs/wiki-bi/concepts/primary-branch.md`
- Modify: `docs/wiki-bi/standards/output-correctness/annuity-performance-output-contract.md`
- Modify: `docs/wiki-bi/standards/output-correctness/annuity-income-output-contract.md`

- [ ] **Step 1: Create the `关键年金计划` concept page**

Write `docs/wiki-bi/concepts/key-annuity-plan.md` so it answers:

- what `关键年金计划` is in customer-master semantics
- why it is a weighted dominant-value output rather than a direct copy of `计划代码`
- why it often appears next to `主拓机构` and `关联计划数`
- why it is cross-domain and not private to one domain pipeline

The page must include links to:

- `../concepts/backfill.md`
- `../concepts/primary-branch.md`
- `../evidence/customer-master-signals-evidence.md`
- `../standards/output-correctness/annuity-performance-output-contract.md`

- [ ] **Step 2: Tighten the customer-master signal dispatcher**

Update `docs/wiki-bi/evidence/customer-master-signals-evidence.md` to split its stable findings more clearly into:

- dominant-value signals
- relationship-breadth signals
- classification/history signals

The page must still keep the standard evidence skeleton and explicitly state:

- `关键年金计划` is now promoted to a durable concept page
- `关联计划数` remains a dispatcher-held signal this round
- `其他年金计划` / `其他开拓机构` remain dispatcher-level explanation objects

- [ ] **Step 3: Reconnect existing concept pages**

Update:

- `docs/wiki-bi/concepts/backfill.md`
- `docs/wiki-bi/concepts/primary-branch.md`
- `docs/wiki-bi/standards/output-correctness/annuity-performance-output-contract.md`
- `docs/wiki-bi/standards/output-correctness/annuity-income-output-contract.md`

so the concept is reachable from both adjacent concept pages and high-traffic output-contract pages instead of remaining an unnamed adjacent field cluster.

The edits must stay narrow:

- no broad refactor of surrounding prose
- only enough text to explain the relationship between backfill, dominant-value selection, and the new concept page

### Task 2: Tighten `is_churned_this_year` Without Forcing A Premature Object Split

**Files:**
- Modify: `docs/wiki-bi/concepts/customer-status.md`
- Modify: `docs/wiki-bi/standards/semantic-correctness/customer-status-semantics.md`
- Modify: `docs/wiki-bi/evidence/status-and-snapshot-evidence.md`
- Modify: `docs/wiki-bi/evidence/is-loss-reported-evidence.md`

- [ ] **Step 1: Tighten the concept and standard pages**

Update `customer-status.md` and `customer-status-semantics.md` so `is_churned_this_year` explicitly states:

- it is a monthly churn judgement
- it is sourced from current-month `business."规模明细"` AUM logic
- missing current-month rows are interpreted as zero for the matched grain
- it is not the same thing as annual loss-reporting

The wording must preserve the three-layer split:

- concept/semantic truth in concept + standard pages
- source-backed nuance in evidence pages
- no operator/runtime mechanics promoted into semantic truth

- [ ] **Step 2: Tighten the aggregate evidence page**

Update `docs/wiki-bi/evidence/status-and-snapshot-evidence.md` so the current gap text no longer says only “still better left in the theme page”.

Instead, make it explicit that:

- `is_churned_this_year` now has stronger shared-page coverage
- the remaining unsplit part is the dual-grain detail (`product_line` vs `plan`)
- the object is still intentionally not split into its own evidence page this round

- [ ] **Step 3: Reaffirm the non-equivalence with `is_loss_reported`**

Update `docs/wiki-bi/evidence/is-loss-reported-evidence.md` so the non-equivalence is easier to discover from the object page itself:

- `is_loss_reported` = annual reported-loss fact
- `is_churned_this_year` = monthly AUM-zero-or-missing judgement

Do not turn `is-loss-reported-evidence.md` into a second aggregate status page. Add only the cross-link and the sharper boundary sentence.

### Task 3: Add A Cross-Domain Classification Dispatcher

**Files:**
- Create: `docs/wiki-bi/evidence/classification-family-evidence.md`
- Modify: `docs/wiki-bi/concepts/plan-type.md`
- Modify: `docs/wiki-bi/evidence/annuity-performance-field-processing-evidence.md`
- Modify: `docs/wiki-bi/evidence/annuity-income-field-processing-evidence.md`
- Modify: `docs/wiki-bi/evidence/annual-loss-field-processing-evidence.md`

- [ ] **Step 1: Create the classification-family dispatcher**

Write `docs/wiki-bi/evidence/classification-family-evidence.md` with the standard evidence skeleton and cover:

- `计划类型`
- `年金计划类型`
- `业务类型`
- `管理资格`
- `组合代码`

The dispatcher must answer:

- which of these are input classifications
- which are aggregated customer-master classifications
- which are portfolio/classification anchors rather than identity truth
- why they should not be collapsed into one layer

Primary evidence sources to cite:

- `E:\Projects\WorkDataHub\docs\business-background\年金计划类型与客户名称业务背景.md`
- `E:\Projects\WorkDataHub\docs\cleansing-rules\annuity-performance.md`
- `E:\Projects\WorkDataHub\docs\cleansing-rules\annuity-income.md`
- `E:\Projects\WorkDataHub\docs\verification_guide_real_data.md`
- `E:\Projects\WorkDataHub\config\foreign_keys.yml`

- [ ] **Step 2: Tighten the existing `plan_type` concept**

Update `docs/wiki-bi/concepts/plan-type.md` so it explicitly distinguishes:

- input-side `计划类型`
- aggregated customer-master `年金计划类型`
- the role of `组合代码` and `业务类型` in how plan type gets interpreted

The page should remain a concept page, not a field-processing walkthrough.

- [ ] **Step 3: Add narrow cross-links from field-processing evidence**

Update the three field-processing evidence pages so they point to the new classification dispatcher at the exact places where classification semantics are already discussed:

- `annuity-performance-field-processing-evidence.md`
- `annuity-income-field-processing-evidence.md`
- `annual-loss-field-processing-evidence.md`

Only add narrow routing language. Do not duplicate the full dispatcher content into those pages.

### Task 4: Write Back Navigation, Round Sediment, And History

**Files:**
- Modify: `docs/wiki-bi/index.md`
- Modify: `docs/wiki-bi/log.md`
- Modify: `docs/wiki-bi/_meta/absorption-rounds/round-29-legacy-business-semantics-expansion.md`
- Modify: `docs/wiki-bi/_meta/absorption-rounds/index.md`
- Modify: `docs/wiki-bi/_meta/wiki-absorption-roadmap.md`

- [ ] **Step 1: Update the main index**

In `docs/wiki-bi/index.md`:

- add or tighten FAQ entries for `关键年金计划`, `is_churned_this_year`, and classification-family semantics
- register `key-annuity-plan.md` in the concepts catalog
- register `classification-family-evidence.md` in the evidence catalog
- keep the current maintainer-entry / reading-intent / FAQ / full-catalog structure intact

- [ ] **Step 2: Tighten Round 29 as an executed round**

Update the Round 29 note and meta indexes so they reflect the actual execution shape:

- Package A promoted one object page (`关键年金计划`)
- Package B tightened shared churn semantics without a standalone page split
- Package C created a dispatcher before deciding on any further concept splits

The sediment must explain why this sequencing better matches evidence maturity than a blind three-package parallel rollout.

- [ ] **Step 3: Append the log entry**

Append one new timestamped log entry in `docs/wiki-bi/log.md` that mentions:

- the new `关键年金计划` concept page
- the new classification-family dispatcher
- the churn semantics tightening on shared status pages
- the fact that this round stayed in business-semantics scope and did not reopen runtime/operator closure

## Validation Steps

- [ ] Run reachability and keyword checks:
  - `rg -n "关键年金计划|classification family|管理资格|is_churned_this_year|AUM|yyMM" docs/wiki-bi`
- [ ] Review only the intended docs diff:
  - `git diff -- docs/wiki-bi docs/superpowers/plans`
- [ ] Verify the new pages are reachable from `docs/wiki-bi/index.md`
- [ ] Confirm modified evidence pages still preserve the expected mini-template structure
- [ ] Re-run the full suite after the docs round completes:
  - `uv run pytest -v`
  - Expected: the same two pre-existing semantic-map failures may remain; the docs round must not introduce new failures

## Completion Criteria

This round is complete when:

- `关键年金计划` is a durable concept page instead of a dispatcher-only mention
- `is_churned_this_year` is materially more answerable from shared status pages without claiming a false standalone split
- classification-family semantics no longer live only in scattered field-processing notes
- `index.md`, `log.md`, and Round 29 meta pages reflect the executed maintenance round
- final validation shows no new failures beyond the known pre-existing semantic-map baseline failures

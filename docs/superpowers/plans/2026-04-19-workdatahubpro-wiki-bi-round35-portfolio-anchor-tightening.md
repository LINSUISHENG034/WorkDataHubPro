# WorkDataHubPro Wiki BI Round 35 Portfolio Anchor Tightening Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Increase legacy business-semantics coverage in `docs/wiki-bi/` by promoting `组合代码` into a durable concept page and tightening the surrounding classification family so the wiki can answer `组合代码` as a portfolio/classification anchor instead of leaving it trapped in dispatcher and field-processing mentions.

**Architecture:** Keep this round concept-first but evidence-backed. Tighten the classification dispatcher first, promote only the `组合代码` object into a dedicated concept page, reconnect the adjacent concept, field-processing, domain, and contract entry points, then write back round sediment so the wiki explicitly records that the remaining high-value business-semantics queue has narrowed.

**Tech Stack:** Markdown in `docs/wiki-bi/` and `docs/superpowers/plans/`, legacy evidence from `E:\Projects\WorkDataHub`, PowerShell, `rg`, git worktrees, `uv`, `pytest`

---

## Scope Check

This plan covers:

- one new concept page for `组合代码`
- tightening `classification-family-evidence.md` so `组合代码` is treated as a first-class portfolio anchor
- reconnecting the new concept from `plan_type`, `management_qualification`, `backfill`, field-processing evidence, high-traffic domains, and input/output contracts
- updating `index.md`, `log.md`, `wiki-absorption-roadmap.md`, and `absorption-rounds/index.md`
- adding a Round 35 sediment note

This plan does not cover:

- creating a new surface page for `mapping.组合计划`
- reopening event-domain-only classification semantics beyond link tightening
- `manual customer-mdm`, enterprise persistence, `reference_sync`, or `company_lookup_queue` discovery work
- changes under `src/`, `config/`, or `tests/`

## Suggested Branch

- `docs/wiki-bi-round34`

## Baseline Note

The isolated worktree exists at `E:\Projects\WorkDataHubPro\.worktrees\docs-wiki-bi-round34` on branch `docs/wiki-bi-round34`.

Baseline environment check after the Round 34 commit:

- `git status --short` is clean.
- `uv run pytest -v` currently passes cleanly: `292 passed`.
- Round 34 is already committed as `ca4bace`.

This round should keep the branch green and produce a second narrow docs-only commit.

## Files To Create

- `docs/wiki-bi/concepts/portfolio-code.md`
- `docs/wiki-bi/_meta/absorption-rounds/round-35-portfolio-anchor-tightening.md`

## Files To Modify

- `docs/wiki-bi/evidence/classification-family-evidence.md`
- `docs/wiki-bi/concepts/plan-type.md`
- `docs/wiki-bi/concepts/management-qualification.md`
- `docs/wiki-bi/concepts/backfill.md`
- `docs/wiki-bi/evidence/annuity-performance-field-processing-evidence.md`
- `docs/wiki-bi/evidence/annuity-income-field-processing-evidence.md`
- `docs/wiki-bi/domains/annuity-performance.md`
- `docs/wiki-bi/domains/annuity-income.md`
- `docs/wiki-bi/standards/input-reality/annuity-performance-input-contract.md`
- `docs/wiki-bi/standards/input-reality/annuity-income-input-contract.md`
- `docs/wiki-bi/standards/output-correctness/annuity-performance-output-contract.md`
- `docs/wiki-bi/standards/output-correctness/annuity-income-output-contract.md`
- `docs/wiki-bi/index.md`
- `docs/wiki-bi/log.md`
- `docs/wiki-bi/_meta/absorption-rounds/index.md`
- `docs/wiki-bi/_meta/wiki-absorption-roadmap.md`

### Task 1: Tighten The Classification Dispatcher And Promote `组合代码`

**Files:**
- Create: `docs/wiki-bi/concepts/portfolio-code.md`
- Modify: `docs/wiki-bi/evidence/classification-family-evidence.md`

- [ ] **Step 1: Tighten the classification dispatcher**

Update `docs/wiki-bi/evidence/classification-family-evidence.md` so it more directly expresses the layered stack:

- input interpretation anchor: `计划类型`
- downstream explanation anchor: `业务类型`
- customer-master aggregated classification: `年金计划类型`, `管理资格`
- portfolio / classification anchor: `组合代码`

The page must make clear that:

- `组合代码` is not enterprise identity truth
- `组合代码` is not customer-master aggregated classification
- `组合代码` is the stable anchor that ties fact rows to `mapping.组合计划` and portfolio-level interpretation
- the field’s business value is larger than “regex cleanup + defaulting”

Primary sources to keep explicit:

- `E:\Projects\WorkDataHub\docs\business-background\年金计划类型与客户名称业务背景.md`
- `E:\Projects\WorkDataHub\config\foreign_keys.yml`
- `E:\Projects\WorkDataHub\docs\cleansing-rules\annuity-performance.md`
- `E:\Projects\WorkDataHub\docs\cleansing-rules\annuity-income.md`
- `E:\Projects\WorkDataHub\docs\verification_guide_real_data.md`
- `E:\Projects\WorkDataHub\src\work_data_hub\domain\reference_backfill\service.py`

- [ ] **Step 2: Create `portfolio-code.md`**

Write `docs/wiki-bi/concepts/portfolio-code.md` with title `# 组合代码`.

The page must answer:

- what `组合代码` means in business semantics
- why it is a portfolio/classification anchor rather than enterprise identity truth
- why it should not be collapsed into `计划类型`, `业务类型`, `管理资格`, or customer-master `年金计划类型`
- why it matters both on the fact side and the `mapping.组合计划` side

The page must link back to:

- `./plan-type.md`
- `./management-qualification.md`
- `./backfill.md`
- `../evidence/classification-family-evidence.md`

### Task 2: Reconnect The Adjacent Concept And Field-Processing Pages

**Files:**
- Modify: `docs/wiki-bi/concepts/plan-type.md`
- Modify: `docs/wiki-bi/concepts/management-qualification.md`
- Modify: `docs/wiki-bi/concepts/backfill.md`
- Modify: `docs/wiki-bi/evidence/annuity-performance-field-processing-evidence.md`
- Modify: `docs/wiki-bi/evidence/annuity-income-field-processing-evidence.md`

- [ ] **Step 1: Tighten the adjacent concept pages**

Update:

- `docs/wiki-bi/concepts/plan-type.md`
- `docs/wiki-bi/concepts/management-qualification.md`
- `docs/wiki-bi/concepts/backfill.md`

The intended result is:

- `plan_type` no longer carries `组合代码` only as a passing sibling mention
- `管理资格` more directly contrasts itself with `组合代码`
- `backfill` explains that portfolio/reference derivation is part of the same governed story, not only customer-master signals

- [ ] **Step 2: Tighten the two field-processing evidence pages**

Update:

- `docs/wiki-bi/evidence/annuity-performance-field-processing-evidence.md`
- `docs/wiki-bi/evidence/annuity-income-field-processing-evidence.md`

The intended result is:

- `组合代码` is described as more than a formatting cleanup target
- the field-processing pages route to the new concept page
- the defaulting and normalization rules are explicitly framed as protecting the portfolio anchor contract

### Task 3: Reconnect High-Traffic Domain And Contract Entry Points

**Files:**
- Modify: `docs/wiki-bi/domains/annuity-performance.md`
- Modify: `docs/wiki-bi/domains/annuity-income.md`
- Modify: `docs/wiki-bi/standards/input-reality/annuity-performance-input-contract.md`
- Modify: `docs/wiki-bi/standards/input-reality/annuity-income-input-contract.md`
- Modify: `docs/wiki-bi/standards/output-correctness/annuity-performance-output-contract.md`
- Modify: `docs/wiki-bi/standards/output-correctness/annuity-income-output-contract.md`

- [ ] **Step 1: Tighten the high-traffic domains**

Update:

- `docs/wiki-bi/domains/annuity-performance.md`
- `docs/wiki-bi/domains/annuity-income.md`

These pages should route readers to the new `组合代码` concept page as the portfolio-anchor answer path. Do not broaden the domains into field catalogs.

- [ ] **Step 2: Tighten the input/output contracts**

Update:

- `docs/wiki-bi/standards/input-reality/annuity-performance-input-contract.md`
- `docs/wiki-bi/standards/input-reality/annuity-income-input-contract.md`
- `docs/wiki-bi/standards/output-correctness/annuity-performance-output-contract.md`
- `docs/wiki-bi/standards/output-correctness/annuity-income-output-contract.md`

The intended result is:

- input contracts acknowledge `组合代码` as a high-value portfolio anchor rather than a throwaway auxiliary field
- output contracts explain why `mapping.组合计划` and portfolio-level semantics depend on it
- readers get a direct route from high-traffic contracts to the new concept page

### Task 4: Write Back Round 35 Navigation And Sediment

**Files:**
- Create: `docs/wiki-bi/_meta/absorption-rounds/round-35-portfolio-anchor-tightening.md`
- Modify: `docs/wiki-bi/index.md`
- Modify: `docs/wiki-bi/log.md`
- Modify: `docs/wiki-bi/_meta/absorption-rounds/index.md`
- Modify: `docs/wiki-bi/_meta/wiki-absorption-roadmap.md`

- [ ] **Step 1: Update the main index**

In `docs/wiki-bi/index.md`:

- add a direct FAQ for `组合代码`
- register the new concept page in the concepts catalog
- keep the current index structure intact

- [ ] **Step 2: Create the Round 35 sediment note**

Write `docs/wiki-bi/_meta/absorption-rounds/round-35-portfolio-anchor-tightening.md` documenting:

- why `组合代码` crossed the standalone object threshold now
- which pages were updated
- why this round closes the remaining high-value business-semantics candidate queue
- why the next likely step returns to manual `customer-mdm` / enterprise persistence discovery

- [ ] **Step 3: Update roadmap/index metadata and append the log**

Update:

- `docs/wiki-bi/_meta/absorption-rounds/index.md`
- `docs/wiki-bi/_meta/wiki-absorption-roadmap.md`
- `docs/wiki-bi/log.md`

The updates must show:

- Round 35 completed
- `组合代码` no longer remains only in dispatcher / field-processing text
- the next follow-on is no longer another obvious nearby business-semantics object, but a return to surface/runtime discovery unless new evidence changes the queue

## Validation Steps

- [ ] Run reachability and keyword checks:
  - `rg -n "组合代码|portfolio anchor|组合计划|classification anchor" docs/wiki-bi`
- [ ] Review only the intended docs diff:
  - `git diff -- docs/wiki-bi docs/superpowers/plans`
- [ ] Run formatting/sanity check:
  - `git diff --check`
- [ ] Re-run the full suite after the docs round completes:
  - `uv run pytest -v`
  - Expected: still green with `292 passed`

## Completion Criteria

This round is complete when:

- `组合代码` has a durable concept page
- the wiki can directly answer why `组合代码` is a portfolio/classification anchor rather than identity truth or customer-master aggregation
- high-traffic concept, field-processing, domain, and contract pages route to the new concept page
- Round 35 navigation and sediment are written back in `index.md`, `log.md`, and `_meta/absorption-rounds/`
- validation keeps the repo green

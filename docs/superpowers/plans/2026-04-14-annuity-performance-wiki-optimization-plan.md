# Annuity Performance Wiki Optimization Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Upgrade `docs/wiki-bi/` so it can answer annuity-performance questions in a concrete input-transform-output form instead of only giving high-level semantic navigation.

**Architecture:** Keep `docs/wiki-bi/domains/annuity-performance.md` as the thin navigation page, but add a small number of contract-grade wiki pages that make the input contract, output contract, and field-processing semantics explicit. Reuse legacy `annuity_performance` domain docs, capability maps, cleansing rules, runbooks, and config contracts as raw sources, then rewrite them into durable wiki objects instead of mirroring the old repository structure.

**Tech Stack:** Markdown in `docs/wiki-bi/`, legacy raw sources from `E:\Projects\WorkDataHub`, existing `docs/wiki-bi` concepts/domains/standards/evidence structure

---

## Scope Check

This plan is intentionally narrow.

It covers:

- evaluating whether `wiki-bi` can answer annuity-performance I/O questions
- identifying concrete gaps against the desired answer shape
- mapping those gaps to durable wiki destinations
- proposing exact new/updated wiki pages needed to close the gaps

It does not cover:

- changing runtime code in `src/`
- changing tests or config behavior
- redefining the overall `wiki-bi` schema
- broad governance work outside annuity-performance

## Current Assessment

### Summary Judgment

Current `wiki-bi` can only partially answer the ideal annuity-performance question set.

Practical score:

- `5/10` for operator-grade or implementation-guiding answers
- `7/10` for high-level semantic/navigation answers

### Where The Current Wiki Is Strong

- It clearly states that `annuity_performance` handles scale-related facts and is the core domain that connects input reality, identity resolution, backfill, and contract/snapshot behavior.
- It already preserves the three major output layers:
  - fact output
  - customer/reference backfill
  - contract / snapshot outputs
- It already preserves the most important surrounding semantics:
  - `company_id`
  - `temp_id`
  - `backfill`
  - customer status
  - snapshot granularity

### Where The Current Wiki Fails Against The Ideal Answer Shape

#### 1. Input-Side Gaps

- It does not state the exact annuity-performance file patterns in `wiki-bi`.
- It does not state the exact annuity-performance sheet name in `wiki-bi`.
- It does not list the annuity-performance input fields in a durable page.
- It does not distinguish:
  - required skeleton fields
  - optional fields
  - fields whose absence makes a source invalid
- It does not separate workbook-shape contract from generic input-reality principles.

#### 2. Output-Side Gaps

- It does not provide a single annuity-performance output contract page.
- It names output layers, but not a complete output inventory.
- It does not clearly separate:
  - direct fact output
  - backfill targets
  - derived downstream tables
- It does not expose the delete/refresh contract or the practical sink list in a durable wiki page.

#### 3. Processing-Side Gaps

- It does not enumerate the annuity-performance fields that actually undergo transformation.
- It does not classify processing into:
  - engineering/data-quality uplift
  - business-semantic transformation
- It does not provide an explicit mapping from field -> rule -> business meaning -> final sink.
- It does not explain which processing steps are merely normalization and which ones materially change business interpretation.

## Legacy Findings To Ground The Wiki

The legacy repository already contains enough source material to answer the ideal question much more concretely.

### Input Contract Facts Found In Legacy

From `E:\Projects\WorkDataHub\docs\domains\annuity_performance.md` and `config/data_sources.yml`:

- Input path: `data/real_data/{YYYYMM}/收集数据/数据采集`
- File patterns:
  - `*年金规模收入*.xlsx`
  - `*规模*收入数据*.xlsx`
- Exclusion pattern:
  - `*回复*`
- Workbook shape:
  - Excel workbook
- Sheet name:
  - `规模明细`
- Version strategy:
  - `highest_number`

From `E:\Projects\WorkDataHub\docs\cleansing-rules\annuity-performance.md`:

- Bronze required fields:
  - `月度`
  - `计划代码`
  - `客户名称`
  - `期末资产规模`
- Gold required fields include:
  - `月度`
  - `计划代码`
  - `company_id`
  - `期初资产规模`
  - `期末资产规模`
  - `投资收益`

### Output Contract Facts Found In Legacy

From `E:\Projects\WorkDataHub\docs\domains\annuity_performance.md` and `annuity_performance-capability-map.md`:

- Direct fact sink:
  - `business."规模明细"`
- Delete/refresh key:
  - `月度`
  - `业务类型`
  - `计划类型`
- Backfill targets:
  - `mapping."年金计划"`
  - `mapping."组合计划"`
  - `mapping."产品线"`
  - `mapping."组织架构"`
  - `customer."客户明细"`
- Derived downstream targets:
  - `customer."客户年金计划"`
  - `customer."客户业务月度快照"`
  - `customer."客户计划月度快照"`

### Field-Processing Facts Found In Legacy

From `E:\Projects\WorkDataHub\docs\cleansing-rules\annuity-performance.md` and `annuity_performance-capability-map.md`:

Important transformed fields include:

- `计划代码`
- `产品线代码`
- `机构代码`
- `组合代码`
- `客户名称`
- `年金账户名`
- `年金账户号`
- `company_id`
- downstream `contract_status`
- downstream snapshot status fields

Important engineering/data-quality uplift rules include:

- column renaming
- date parsing / standardization
- trimming / null normalization
- special-code correction
- portfolio defaulting
- branch-code mapping

Important business-semantic transformation rules include:

- company identity resolution
- plan-code defaulting by `计划类型`
- backfill aggregation into customer/reference objects
- contract-state derivation
- snapshot-state derivation

## Recommended Wiki Optimization Direction

The wiki should not become a code walkthrough.

It should become strong enough to answer:

1. what the source contract is
2. what the output contract is
3. which transformations are business-significant
4. which transformations are merely engineering normalization

### Recommended New Durable Pages

#### 1. Input Contract Page

Create:

- `docs/wiki-bi/standards/input-reality/annuity-performance-input-contract.md`

This page should answer:

- exact path
- file format
- file-pattern keywords
- exact sheet name
- version strategy
- source exclusions
- minimum required skeleton fields
- fields tolerated as missing
- conditions that make a workbook invalid

#### 2. Output Contract Page

Create:

- `docs/wiki-bi/standards/output-correctness/annuity-performance-output-contract.md`

This page should answer:

- direct fact sink
- delete/refresh scope
- backfill targets
- derived downstream tables
- which outputs belong to the domain itself
- which outputs are downstream effects after hooks/backfill

#### 3. Field Processing Semantics Page

Create:

- `docs/wiki-bi/evidence/annuity-performance-field-processing-evidence.md`

This page should answer, field by field:

- raw source field
- canonical field
- transformation type
- whether the rule is engineering uplift or business-semantic
- rule rationale
- downstream sink(s)

### Recommended Tightening Of Existing Pages

Update:

- `docs/wiki-bi/domains/annuity-performance.md`
- `docs/wiki-bi/evidence/input-reality-evidence.md`
- `docs/wiki-bi/standards/input-reality/input-reality-contracts.md`
- `docs/wiki-bi/standards/output-correctness/output-correctness.md`
- `docs/wiki-bi/concepts/backfill.md`

Purpose:

- keep the domain page thin, but point directly to the new contract-grade pages
- avoid repeating full details in multiple places
- preserve the current wiki shape while improving answer quality

## Proposed File Structure

### Files To Create

- `docs/wiki-bi/standards/input-reality/annuity-performance-input-contract.md`
- `docs/wiki-bi/standards/output-correctness/annuity-performance-output-contract.md`
- `docs/wiki-bi/evidence/annuity-performance-field-processing-evidence.md`
- `docs/wiki-bi/_meta/absorption-rounds/round-15-annuity-performance-io-contracts.md`

### Files To Modify

- `docs/wiki-bi/domains/annuity-performance.md`
- `docs/wiki-bi/standards/input-reality/input-reality-contracts.md`
- `docs/wiki-bi/standards/output-correctness/output-correctness.md`
- `docs/wiki-bi/evidence/input-reality-evidence.md`
- `docs/wiki-bi/concepts/backfill.md`
- `docs/wiki-bi/index.md`
- `docs/wiki-bi/log.md`
- `docs/wiki-bi/_meta/absorption-rounds/index.md`

## Implementation Tasks

### Task 1: Add Annuity Performance Input Contract Page

**Files:**
- Create: `docs/wiki-bi/standards/input-reality/annuity-performance-input-contract.md`
- Modify: `docs/wiki-bi/standards/input-reality/input-reality-contracts.md`

- [ ] **Step 1: Write the annuity-performance input contract**

Document:

- workbook format
- file patterns
- exclusion patterns
- exact sheet name
- version strategy
- minimum required skeleton fields
- invalid-source conditions

- [ ] **Step 2: Link it from the generic input-reality page**

Add the page as the annuity-performance-specific contract instead of leaving only generic directory-level guidance.

- [ ] **Step 3: Verify path and cross-links**

Check that the new page is reachable from:

- `domains/annuity-performance.md`
- `standards/input-reality/input-reality-contracts.md`
- `index.md`

### Task 2: Add Annuity Performance Output Contract Page

**Files:**
- Create: `docs/wiki-bi/standards/output-correctness/annuity-performance-output-contract.md`
- Modify: `docs/wiki-bi/standards/output-correctness/output-correctness.md`

- [ ] **Step 1: Write the output contract**

Document:

- direct fact sink
- refresh/delete scope
- backfill targets
- derived downstream tables
- the boundary between domain output and downstream projections

- [ ] **Step 2: Link it from the generic output-correctness page**

Make annuity-performance the first concrete example of a domain-specific output contract.

- [ ] **Step 3: Verify consistency**

Ensure the output contract agrees with current durable concepts:

- `backfill`
- `customer-status`
- `snapshot_granularity`

### Task 3: Add Field-Processing Evidence Page

**Files:**
- Create: `docs/wiki-bi/evidence/annuity-performance-field-processing-evidence.md`
- Modify: `docs/wiki-bi/domains/annuity-performance.md`
- Modify: `docs/wiki-bi/concepts/backfill.md`

- [ ] **Step 1: Write the processing matrix**

For key fields, classify processing into:

- engineering/data-quality uplift
- business-semantic transformation

Minimum fields to include:

- `月度`
- `计划代码`
- `业务类型`
- `产品线代码`
- `机构代码`
- `组合代码`
- `客户名称`
- `年金账户名`
- `年金账户号`
- `company_id`

- [ ] **Step 2: Connect the page to the domain and backfill pages**

Use the domain page as the entrypoint and `backfill.md` as the semantic bridge for downstream targets.

- [ ] **Step 3: Verify that the page explains transformation intent rather than code order**

If a section reads like pipeline-step narration instead of durable semantics, rewrite it.

### Task 4: Record The Absorption Round

**Files:**
- Create: `docs/wiki-bi/_meta/absorption-rounds/round-15-annuity-performance-io-contracts.md`
- Modify: `docs/wiki-bi/_meta/absorption-rounds/index.md`
- Modify: `docs/wiki-bi/index.md`
- Modify: `docs/wiki-bi/log.md`

- [ ] **Step 1: Write the round summary**

Capture:

- raw sources used
- stable findings promoted into wiki
- why these pages were needed

- [ ] **Step 2: Update indexes**

Add the new durable pages to:

- `docs/wiki-bi/index.md`
- `docs/wiki-bi/_meta/absorption-rounds/index.md`

- [ ] **Step 3: Append log entry**

Record the annuity-performance I/O-contract optimization round in `docs/wiki-bi/log.md`.

## Validation

For the docs work itself, verify:

- no broken links in `docs/wiki-bi`
- no duplicate summary pages created unnecessarily
- `annuity-performance` remains a navigation page, not an implementation walkthrough
- the new pages let a reader answer the three ideal question groups:
  - input
  - output
  - processing

Suggested command:

```powershell
git diff -- docs/wiki-bi docs/superpowers/plans
```

## Expected Outcome

After this optimization, `wiki-bi` should be able to produce a high-quality answer to the ideal question shape for `annuity_performance`:

- 输入端：文件、sheet、必需字段、无效源条件
- 输出端：事实输出、回填输出、派生输出
- 处理端：字段处理项，以及工程性处理 vs 业务语义处理的分层

## Execution Handoff

Plan complete and saved to `docs/superpowers/plans/2026-04-14-annuity-performance-wiki-optimization-plan.md`.

Two execution options:

1. Subagent-Driven (recommended) - dispatch a fresh subagent per task and review between tasks
2. Inline Execution - execute the documentation tasks directly in this session

# WorkDataHubPro Wiki Maintenance Next-Phase Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Upgrade the current `wiki-bi` maintenance workflow so it reuses and tightens the existing domain-upgrade framework, treats `annuity_income` as a first-class confirmed domain, and adds explicit implementation-evidence, identity-narrative, and lint controls.

**Architecture:** Do not replace the current `docs/wiki-bi/_meta/wiki-domain-upgrade-framework.md`. Optimize it in place, then execute one concrete exemplar round around `annuity_income` so the framework is tested against a second confirmed domain after `annuity_performance`. Keep durable business knowledge in `docs/wiki-bi/`, operational memory in absorption rounds, and execution guidance in `docs/superpowers/plans/`.

**Tech Stack:** Markdown in `docs/wiki-bi/` and `docs/superpowers/plans/`, current `WorkDataHubPro` wiki structure, legacy raw sources from `E:\Projects\WorkDataHub`, PowerShell, `rg`

---

## Scope Check

This plan covers:

- optimizing the existing `wiki-domain-upgrade-framework` instead of replacing it
- explicitly recognizing `annuity_income` as a confirmed domain-upgrade target
- adding a reusable implementation-evidence writeback pattern
- adding an identity-narrative consolidation pass
- adding a dedicated wiki-maintenance lint checklist and running it on touched pages
- writing the resulting updates back to `index.md`, `log.md`, and a new absorption round

This plan does not cover:

- changing runtime code in `src/work_data_hub_pro/`
- reworking the top-level `docs/system/` authority model
- reopening already-closed `annuity_performance` gaps
- broad non-domain wiki expansion unrelated to the five approved directions

## Proposed File Structure

### Files To Create

- `docs/wiki-bi/_meta/wiki-maintenance-lint-checklist.md`
- `docs/wiki-bi/_meta/absorption-rounds/round-18-annuity-income-domain-upgrade-and-maintenance-controls.md`
- `docs/wiki-bi/standards/input-reality/annuity-income-input-contract.md`
- `docs/wiki-bi/standards/output-correctness/annuity-income-output-contract.md`
- `docs/wiki-bi/evidence/annuity-income-field-processing-evidence.md`

### Files To Modify

- `docs/wiki-bi/_meta/wiki-domain-upgrade-framework.md`
- `docs/wiki-bi/domains/annuity-income.md`
- `docs/wiki-bi/evidence/annuity-income-gap-evidence.md`
- `docs/wiki-bi/evidence/annuity-income-branch-mapping-evidence.md`
- `docs/wiki-bi/evidence/annuity-income-id5-retirement-evidence.md`
- `docs/wiki-bi/evidence/annuity-income-operator-artifacts-evidence.md`
- `docs/wiki-bi/concepts/company-id.md`
- `docs/wiki-bi/standards/semantic-correctness/identity-governance.md`
- `docs/wiki-bi/index.md`
- `docs/wiki-bi/log.md`
- `docs/wiki-bi/_meta/absorption-rounds/index.md`

## Task 1: Optimize The Existing Domain-Upgrade Framework

**Files:**
- Modify: `docs/wiki-bi/_meta/wiki-domain-upgrade-framework.md`
- Modify: `docs/wiki-bi/index.md`
- Modify: `docs/wiki-bi/log.md`

- [ ] **Step 1: Reframe the framework as an optimization target, not a replacement**

Update the opening sections so they say:

```md
- this framework is the current canonical maintenance playbook for contract-grade domain upgrades
- future work should tighten this document in place instead of creating parallel playbooks
- new rounds should feed back improvements discovered during execution
```

- [ ] **Step 2: Expand the “current recommended boundaries” section**

Add explicit language that the currently confirmed domain-upgrade set is:

```md
- `annuity_performance`
- `annual_award`
- `annual_loss`
- `annuity_income`
```

and state that `annuity_income` is not merely a future slice placeholder but an already-confirmed domain whose wiki should be upgraded when its answer surface remains weaker than peer domains.

- [ ] **Step 3: Add three new control sections to the framework**

Add these headings and durable rules:

```md
## Implementation Evidence Writeback
- when a wiki-guided conclusion is later verified by current tests, replay assets, or runbooks, the affected page should add explicit `current_test`, `current_reference_asset`, or `current_runbook` evidence
- do not leave implementation-backed conclusions only in logs or chat

## Identity Narrative Consolidation
- when identity behavior spans compatibility inventory, active runtime path, retirement decisions, and operator expectations, the wiki must separate those layers explicitly
- avoid mixing “still loadable historical artifacts” with “currently executed priority order”

## Maintenance Lint Gate
- every substantial wiki-maintenance round should run a small lint checklist before completion
- lint should cover inbound links, active gap dispositions, implementation-evidence visibility, and date-time log entries
```

- [ ] **Step 4: Add one FAQ/index pointer and one log entry**

Add one short catalog/FAQ pointer in `docs/wiki-bi/index.md` that tells readers the framework now covers `annuity_income` as well as event-style domains, then append a new `log.md` entry using the timestamp format:

```md
## [2026-04-15 HH:MM] maintain | 收紧 domain-upgrade framework 适用边界
```

## Task 2: Create The Wiki Maintenance Lint Checklist

**Files:**
- Create: `docs/wiki-bi/_meta/wiki-maintenance-lint-checklist.md`
- Modify: `docs/wiki-bi/_meta/wiki-domain-upgrade-framework.md`
- Modify: `docs/wiki-bi/index.md`

- [ ] **Step 1: Create the checklist file**

Write `docs/wiki-bi/_meta/wiki-maintenance-lint-checklist.md` with this exact top structure:

```md
# wiki maintenance lint checklist

## Purpose

Provide a lightweight pre-completion gate for substantial `docs/wiki-bi/` maintenance rounds.

## Checks

- durable pages changed in this round are listed in `docs/wiki-bi/index.md`
- `docs/wiki-bi/log.md` has a same-round append-only entry with `YYYY-MM-DD HH:MM`
- no active gap is left without an explicit disposition
- implementation-backed conclusions cite current evidence where available
- cross-links from domain page -> standards/evidence and evidence -> supported pages remain intact
- no new broad summary page was created where an existing object page should have been updated
```

- [ ] **Step 2: Wire the checklist back into the framework**

Under the framework’s new lint section, add a direct link to `./wiki-maintenance-lint-checklist.md` and instruct future rounds to run it whenever durable pages change materially.

- [ ] **Step 3: Register the checklist in the root index**

Add a new meta entry in `docs/wiki-bi/index.md` for the checklist so it becomes discoverable rather than hidden only by path knowledge.

## Task 3: Upgrade `annuity_income` To Contract-Grade Domain Coverage

**Files:**
- Create: `docs/wiki-bi/standards/input-reality/annuity-income-input-contract.md`
- Create: `docs/wiki-bi/standards/output-correctness/annuity-income-output-contract.md`
- Create: `docs/wiki-bi/evidence/annuity-income-field-processing-evidence.md`
- Modify: `docs/wiki-bi/domains/annuity-income.md`
- Modify: `docs/wiki-bi/index.md`
- Modify: `docs/wiki-bi/log.md`

- [ ] **Step 1: Create the input contract page**

Use this section skeleton:

```md
# `annuity_income` 输入合同

> standard_type: `input-reality`
> related_standard_types: `verification-method`, `output-correctness`

## 标准对象
## 输入介质与发现规则
## Sheet 合同
## 最小字段骨架
## 运行时容忍边界
## 无效源条件
## 相关概念
## 相关证据
## 相关验证方法
```

The content should come from current `annuity_income` raw sources and existing evidence pages, not copied wholesale from old docs.

- [ ] **Step 2: Create the output contract page**

Use this section skeleton:

```md
# `annuity_income` 输出合同

> standard_type: `output-correctness`
> related_standard_types: `verification-method`, `input-reality`

## 标准对象
## direct fact output
## backfill targets
## derived downstream outputs
## 正确性判断边界
## 相关概念
## 相关证据
```

- [ ] **Step 3: Create the field-processing evidence page**

Use this section skeleton:

```md
# `annuity_income` 字段处理证据

## 结论主题
## 关键字段处理矩阵
## 工程性质量提升
## 业务语义处理
## 当前实现证据
## 仍需补强的缺口
```

The matrix must at minimum cover:

```md
- `计划代码`
- `客户名称`
- `年金账户名`
- `company_id`
- branch mapping related fields
- unresolved-name / failed-record artifact touchpoints
```

- [ ] **Step 4: Rewire the domain page**

Update `docs/wiki-bi/domains/annuity-income.md` so it becomes the thin navigation page for:

```md
- input contract
- output contract
- field-processing evidence
- branch mapping evidence
- ID5 retirement evidence
- operator artifacts evidence
```

and explicitly remove any wording that implies `annuity_income` is still only “institutional memory waiting to be implemented”.

## Task 4: Consolidate Identity Narrative And Implementation Evidence

**Files:**
- Modify: `docs/wiki-bi/evidence/annuity-income-gap-evidence.md`
- Modify: `docs/wiki-bi/evidence/annuity-income-branch-mapping-evidence.md`
- Modify: `docs/wiki-bi/evidence/annuity-income-id5-retirement-evidence.md`
- Modify: `docs/wiki-bi/evidence/annuity-income-operator-artifacts-evidence.md`
- Modify: `docs/wiki-bi/concepts/company-id.md`
- Modify: `docs/wiki-bi/standards/semantic-correctness/identity-governance.md`

- [ ] **Step 1: Normalize the identity story into explicit layers**

For the touched pages, ensure each relevant section distinguishes:

```md
- compatibility inventory / historical memory
- active runtime path
- retired behavior that must not be reintroduced
- operator-visible consequences
```

- [ ] **Step 2: Add implementation-evidence fields where current evidence exists**

For each page that now relies on current project evidence, add explicit references in prose such as:

```md
- `current_test`
- `current_reference_asset`
- `current_runbook`
```

Do not invent these references; only add them where current repo evidence already exists or is directly cited by the page.

- [ ] **Step 3: Reduce catch-all summary pressure**

Tighten `docs/wiki-bi/evidence/annuity-income-gap-evidence.md` so it points out to object-level evidence pages instead of retaining all detail inline. The aggregate page should become a dispatcher, not the only place where readers can recover the identity story.

## Task 5: Record Round 18 And Run The Lint Gate

**Files:**
- Create: `docs/wiki-bi/_meta/absorption-rounds/round-18-annuity-income-domain-upgrade-and-maintenance-controls.md`
- Modify: `docs/wiki-bi/_meta/absorption-rounds/index.md`
- Modify: `docs/wiki-bi/log.md`

- [ ] **Step 1: Create the new absorption-round document**

Use this exact opening block:

```md
# Round 18：`annuity_income` domain upgrade and maintenance controls

> 状态：Completed
> 日期：2026-04-15
> 主题簇：maintenance / annuity-income / maintenance-controls

## 本轮目标

- 在现有 domain-upgrade framework 基础上优化维护流程
- 把 `annuity_income` 从“已确认但未对称升级”的 domain 推进到合同级问答能力
- 为后续 round 增加 implementation-evidence 与 lint gate
```

- [ ] **Step 2: Update the round index and append the log**

Add the new round to `_meta/absorption-rounds/index.md`, then append one log entry describing:

```md
- framework optimization
- annuity_income contract-grade upgrade
- identity narrative consolidation
- lint checklist admission
```

- [ ] **Step 3: Run the lint checklist against the touched pages**

Run:

```powershell
rg -n "annuity-income-input-contract|annuity-income-output-contract|annuity-income-field-processing-evidence|wiki-maintenance-lint-checklist|round-18-annuity-income-domain-upgrade-and-maintenance-controls" docs/wiki-bi
git diff -- docs/wiki-bi docs/superpowers/plans
```

Expected:

```md
- every new durable page is reachable from `index.md` or its owning page
- `log.md` contains a same-round timestamped entry
- the new checklist file is reachable from the framework and root index
```

## Validation

For the docs work, verify:

- `docs/wiki-bi/_meta/wiki-domain-upgrade-framework.md` now reads like the canonical optimized playbook, not a one-off annuity-performance note
- `annuity_income` has the same contract-grade answer shape as the domains already treated as confirmed upgrade targets
- implementation evidence is explicitly named where available
- identity pages now distinguish active path vs compatibility/historical inventory
- the new lint checklist is discoverable and runnable

Suggested commands:

```powershell
rg -n "annuity_income|annuity-income|wiki-maintenance-lint-checklist|Implementation Evidence Writeback|Identity Narrative Consolidation|Maintenance Lint Gate" docs/wiki-bi
git diff -- docs/wiki-bi docs/superpowers/plans
```

## Expected Outcome

After this plan is executed:

- the existing domain-upgrade framework will be stronger instead of duplicated
- `annuity_income` will no longer lag behind peer confirmed domains in wiki answer quality
- implementation-backed conclusions will have an explicit writeback pattern
- identity-governance pages will separate active runtime path from compatibility inventory more cleanly
- future wiki rounds will have a lightweight lint gate before completion

## Execution Handoff

Plan complete and saved to `docs/superpowers/plans/2026-04-15-workdatahubpro-wiki-maintenance-next-phase-plan.md`.

Two execution options:

1. Subagent-Driven (recommended) - I dispatch a fresh subagent per task, review between tasks, fast iteration
2. Inline Execution - Execute tasks in this session using executing-plans, batch execution with checkpoints

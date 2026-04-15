# WorkDataHubPro Wiki BI Legacy Semantic Absorption Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Expand `docs/wiki-bi/` by mining hidden business semantics from `E:\Projects\WorkDataHub` and turn that mining into a repeatable, reviewable subagent workflow that starts with single-module pilots and ends with a parallel multi-module absorption wave.

**Architecture:** Keep `docs/wiki-bi/` as the durable synthesis layer and do not mirror legacy implementation structure. First freeze a module map that covers domain and cross-cutting semantic areas, then run a coverage-first subagent review, then validate the execution pattern through three single-module worktree pilots, and only then scale to parallel subagent execution on the remaining modules. Because the user explicitly requires `.worktrees/` isolation for subagent execution, use linked worktrees even though the content changes are docs-only.

**Tech Stack:** Markdown in `docs/wiki-bi/` and `docs/superpowers/plans/`, legacy raw sources from `E:\Projects\WorkDataHub`, linked git worktrees under `.worktrees/`, PowerShell, `rg`, git, Codex subagents

---

## Scope Check

This plan covers:

- building a coverage-first absorption program instead of ad hoc wiki edits
- defining a stable module decomposition across current wiki structure and legacy source families
- reviewing that module map with subagents before execution starts
- validating the subagent task design through three single-module pilot loops
- scaling to a multi-subagent parallel wave only after the pilot gates pass

This plan does not cover:

- changing runtime code under `src/work_data_hub_pro/`
- reworking the top-level rebuild blueprint or first-wave coverage matrix
- replacing existing `wiki-bi` governance documents with a new parallel process
- merging unchecked subagent output directly into `main`

## Proposed File Structure

### Files To Create

- `docs/wiki-bi/_meta/wiki-legacy-semantic-absorption-module-map.md`
- `docs/wiki-bi/_meta/wiki-subagent-worktree-playbook.md`
- `docs/wiki-bi/_meta/legacy-semantic-coverage-review.md`
- `docs/wiki-bi/evidence/reference-and-backfill-evidence.md`
- `docs/wiki-bi/evidence/customer-mdm-lifecycle-evidence.md`
- `docs/wiki-bi/_meta/absorption-rounds/round-24-reference-backfill-pilot.md`
- `docs/wiki-bi/_meta/absorption-rounds/round-25-identity-governance-pilot.md`
- `docs/wiki-bi/_meta/absorption-rounds/round-26-status-snapshot-pilot.md`
- `docs/wiki-bi/_meta/absorption-rounds/round-27-parallel-legacy-semantic-wave-01.md`

### Files To Modify

- `docs/wiki-bi/_meta/wiki-domain-upgrade-framework.md`
- `docs/wiki-bi/_meta/wiki-absorption-roadmap.md`
- `docs/wiki-bi/_meta/absorption-rounds/index.md`
- `docs/wiki-bi/index.md`
- `docs/wiki-bi/log.md`
- `docs/wiki-bi/concepts/backfill.md`
- `docs/wiki-bi/concepts/company-id.md`
- `docs/wiki-bi/concepts/temp-id.md`
- `docs/wiki-bi/concepts/customer-status.md`
- `docs/wiki-bi/concepts/snapshot-granularity.md`
- `docs/wiki-bi/standards/semantic-correctness/identity-governance.md`
- `docs/wiki-bi/standards/semantic-correctness/customer-status-semantics.md`
- `docs/wiki-bi/standards/output-correctness/output-correctness.md`
- `docs/wiki-bi/standards/verification-method/golden-scenarios.md`
- `docs/wiki-bi/standards/verification-method/real-data-validation.md`
- `docs/wiki-bi/evidence/identity-and-lookup-evidence.md`
- `docs/wiki-bi/evidence/status-and-snapshot-evidence.md`
- `docs/wiki-bi/evidence/operator-and-surface-evidence.md`
- `docs/wiki-bi/evidence/verification-assets-evidence.md`
- `docs/wiki-bi/evidence/validation-result-history-evidence.md`
- `docs/wiki-bi/surfaces/reference-sync.md`
- `docs/wiki-bi/surfaces/company-lookup-queue.md`
- `docs/wiki-bi/surfaces/customer-mdm-commands.md`
- `docs/wiki-bi/surfaces/enterprise-enrichment-persistence.md`
- `docs/wiki-bi/surfaces/failed-record-export.md`
- `docs/wiki-bi/surfaces/unknown-names-csv.md`
- `docs/wiki-bi/surfaces/standalone-tooling.md`
- `docs/wiki-bi/domains/annuity-performance.md`
- `docs/wiki-bi/domains/annuity-income.md`
- `docs/wiki-bi/domains/annual-award.md`
- `docs/wiki-bi/domains/annual-loss.md`
- `docs/wiki-bi/standards/input-reality/annuity-performance-input-contract.md`
- `docs/wiki-bi/standards/input-reality/annuity-income-input-contract.md`
- `docs/wiki-bi/standards/input-reality/annual-award-input-contract.md`
- `docs/wiki-bi/standards/input-reality/annual-loss-input-contract.md`
- `docs/wiki-bi/standards/output-correctness/annuity-performance-output-contract.md`
- `docs/wiki-bi/standards/output-correctness/annuity-income-output-contract.md`
- `docs/wiki-bi/standards/output-correctness/annual-award-output-contract.md`
- `docs/wiki-bi/standards/output-correctness/annual-loss-output-contract.md`
- `docs/wiki-bi/evidence/annuity-performance-field-processing-evidence.md`
- `docs/wiki-bi/evidence/annuity-income-field-processing-evidence.md`
- `docs/wiki-bi/evidence/annual-award-field-processing-evidence.md`
- `docs/wiki-bi/evidence/annual-loss-field-processing-evidence.md`

## Module Coverage Model

The execution must use this eight-module decomposition, because it gives disjoint or near-disjoint write ownership while covering the main legacy source families that still hide business meaning:

| Module | Coverage Focus | Primary Legacy Sources | Primary Wiki Targets |
|------|------|------|------|
| `M1` | `annuity_performance` hidden field semantics and downstream meaning | `docs/domains/annuity_performance*.md`, runbook, `pipeline_builder.py`, `service.py`, `schemas.py`, `helpers.py` | domain page, input contract, output contract, field-processing evidence |
| `M2` | `annuity_income` hidden field semantics and operator-visible differences | `docs/domains/annuity_income*.md`, runbook, `pipeline_builder.py`, `service.py`, `schemas.py`, `helpers.py` | domain page, input contract, output contract, field-processing evidence |
| `M3` | `annual_award` hidden multi-sheet and enrichment semantics | `docs/domains/annual_award*.md`, runbook, `pipeline_builder.py`, `service.py`, `schemas.py`, `helpers.py` | domain page, input contract, output contract, field-processing evidence |
| `M4` | `annual_loss` hidden multi-sheet and temporal lookup semantics | `docs/domains/annual_loss*.md`, runbook, `pipeline_builder.py`, `service.py`, `schemas.py`, `helpers.py` | domain page, input contract, output contract, field-processing evidence |
| `M5` | identity resolution, `temp_id`, override mappings, branch mappings, enrichment persistence boundaries | `config/mappings/company_id/*`, `config/mappings/company_branch.yml`, `config/eqc_confidence.yml`, `infrastructure/enrichment/*`, `domain/company_enrichment/*`, business-background docs | concept pages, identity standard, identity evidence, queue and persistence surfaces |
| `M6` | reference derivation, backfill, master-data propagation, publication-facing meaning | `config/foreign_keys.yml`, `config/reference_sync.yml`, `domain/reference_backfill/*`, `orchestration/reference_sync_ops.py`, `io/loader/*`, customer-master background docs | `backfill.md`, `reference-sync.md`, new reference/backfill evidence page, output correctness, domain links |
| `M7` | customer status, yearly lifecycle, strategic/existing semantics, snapshot consequences | `config/customer_status_rules.yml`, `config/customer_mdm.yaml`, `customer_mdm/*`, `cli/customer_mdm/*`, `cli/etl/hooks.py`, status background docs | customer-status concepts, status standard, new customer-MDM lifecycle evidence page, customer-MDM surface |
| `M8` | operator/runtime/verification governance including CLI surfaces, failed artifacts, replay and parity memory | `docs/guides/validation/*`, `docs/reference/data_processing_guide.md`, runbooks, `cli/etl/*`, `orchestration/jobs.py`, `orchestration/ops/*`, `infrastructure/validation/*` | operator/surface evidence, verification evidence, validation-result-history evidence, tooling surfaces, domain links |

Coverage rule:

- every legacy source family listed above must map to one owning module
- any source family that cannot be placed cleanly must be added to the module map before pilot execution starts
- `M5`, `M6`, and `M7` are the pilot modules because they stress three different wiki shapes:
  - concept + evidence + surface
  - evidence + domain link + correctness boundary
  - concept + standard + operator surface

## Task 1: Freeze The Module Map And The Subagent Playbook

**Files:**
- Create: `docs/wiki-bi/_meta/wiki-legacy-semantic-absorption-module-map.md`
- Create: `docs/wiki-bi/_meta/wiki-subagent-worktree-playbook.md`
- Modify: `docs/wiki-bi/_meta/wiki-absorption-roadmap.md`
- Modify: `docs/wiki-bi/index.md`
- Modify: `docs/wiki-bi/log.md`

- [ ] **Step 1: Create the module-map document**

Write `docs/wiki-bi/_meta/wiki-legacy-semantic-absorption-module-map.md` with this opening structure and table:

```md
# wiki legacy semantic absorption module map

> 状态：Active
> 日期：2026-04-16
> 目标：把 `E:\Projects\WorkDataHub` 中仍藏在实现里的业务语义按可并行吸收的模块固定下来。

## Coverage Intent

- 先覆盖 legacy source families，再安排 subagent 执行顺序
- 每个模块都必须能回答“读哪些 raw sources、更新哪些 wiki pages、怎样验收”
- 模块边界优先服务 reviewability，而不是复制 legacy 目录结构

## Modules

| Module | Coverage Focus | Primary Legacy Sources | Primary Wiki Targets | Pilot Status |
|------|------|------|------|------|
| `M1` | `annuity_performance` hidden field semantics and downstream meaning | `docs/domains/annuity_performance*.md`, runbook, `pipeline_builder.py`, `service.py`, `schemas.py`, `helpers.py` | domain page, input contract, output contract, field-processing evidence | `parallel-wave` |
| `M2` | `annuity_income` hidden field semantics and operator-visible differences | `docs/domains/annuity_income*.md`, runbook, `pipeline_builder.py`, `service.py`, `schemas.py`, `helpers.py` | domain page, input contract, output contract, field-processing evidence | `parallel-wave` |
| `M3` | `annual_award` hidden multi-sheet and enrichment semantics | `docs/domains/annual_award*.md`, runbook, `pipeline_builder.py`, `service.py`, `schemas.py`, `helpers.py` | domain page, input contract, output contract, field-processing evidence | `parallel-wave` |
| `M4` | `annual_loss` hidden multi-sheet and temporal lookup semantics | `docs/domains/annual_loss*.md`, runbook, `pipeline_builder.py`, `service.py`, `schemas.py`, `helpers.py` | domain page, input contract, output contract, field-processing evidence | `parallel-wave` |
| `M5` | identity resolution, `temp_id`, override mappings, branch mappings, enrichment persistence boundaries | `config/mappings/company_id/*`, `config/mappings/company_branch.yml`, `config/eqc_confidence.yml`, `infrastructure/enrichment/*`, `domain/company_enrichment/*`, business-background docs | concept pages, identity standard, identity evidence, queue and persistence surfaces | `pilot-02` |
| `M6` | reference derivation, backfill, master-data propagation, publication-facing meaning | `config/foreign_keys.yml`, `config/reference_sync.yml`, `domain/reference_backfill/*`, `orchestration/reference_sync_ops.py`, `io/loader/*`, customer-master background docs | `backfill.md`, `reference-sync.md`, new reference/backfill evidence page, output correctness, domain links | `pilot-01` |
| `M7` | customer status, yearly lifecycle, strategic/existing semantics, snapshot consequences | `config/customer_status_rules.yml`, `config/customer_mdm.yaml`, `customer_mdm/*`, `cli/customer_mdm/*`, `cli/etl/hooks.py`, status background docs | customer-status concepts, status standard, new customer-MDM lifecycle evidence page, customer-MDM surface | `pilot-03` |
| `M8` | operator/runtime/verification governance including CLI surfaces, failed artifacts, replay and parity memory | `docs/guides/validation/*`, `docs/reference/data_processing_guide.md`, runbooks, `cli/etl/*`, `orchestration/jobs.py`, `orchestration/ops/*`, `infrastructure/validation/*` | operator/surface evidence, verification evidence, validation-result-history evidence, tooling surfaces, domain links | `parallel-wave` |
```

Use the exact eight-module model from this plan, not a fresh decomposition.

- [ ] **Step 2: Create the subagent/worktree playbook**

Write `docs/wiki-bi/_meta/wiki-subagent-worktree-playbook.md` with these exact governing sections:

```md
# wiki subagent worktree playbook

## Purpose

Define how one subagent updates one wiki module in one linked worktree, and how the main session reviews and merges that result.

## Hard Rules

- one subagent owns one module and one disjoint write set
- all subagent execution happens in `.worktrees/`
- subagent output never merges to `main` without human review in the root worktree
- open questions may land in `evidence/`, but never as stable findings in concept/standard/domain main prose
- domain pages stay thin navigation pages

## Required Review Gates

- touched evidence pages still expose `结论主题` + `证据记录` + strong/supporting split + `当前证据缺口`
- touched concept and standard pages separate stable findings from implementation trace
- `index.md`, `log.md`, and the round note are updated in the same change
- new pages are reachable from an owning page and from `index.md`
- the subagent changed only its assigned file set
```

- [ ] **Step 3: Register the two new meta pages**

Add both files to:

- `docs/wiki-bi/index.md`
- `docs/wiki-bi/_meta/wiki-absorption-roadmap.md`

Use a new roadmap section that says:

```md
## Subagent-Governed Legacy Semantic Absorption

Goal:

- absorb hidden legacy semantics through a coverage-first module map
- validate the subagent workflow through three pilot modules before parallel scaling
```

- [ ] **Step 4: Append a planning log entry**

Append this log subject in `docs/wiki-bi/log.md`:

```md
## [2026-04-16 HH:MM] plan | legacy semantic absorption module map and subagent playbook
```

The bullets must mention:

- the eight-module coverage model
- `.worktrees/` as the required isolation mode for subagent execution
- three single-module pilots before a parallel wave

## Task 2: Run Coverage-First Subagent Review And Refine The Module Map

**Files:**
- Create: `docs/wiki-bi/_meta/legacy-semantic-coverage-review.md`
- Modify: `docs/wiki-bi/_meta/wiki-legacy-semantic-absorption-module-map.md`
- Modify: `docs/wiki-bi/_meta/wiki-subagent-worktree-playbook.md`
- Modify: `docs/wiki-bi/log.md`

- [ ] **Step 1: Launch two read-only subagents with non-overlapping questions**

Use one explorer for legacy source-family coverage and one explorer for wiki-governance fit.

Give the first explorer this prompt:

```text
Assess the coverage breadth of the wiki-bi legacy semantic absorption module map.
Return:
1. missing or weakly covered legacy source families
2. which module should own each missing family
3. the top three coverage risks if we execute the current map unchanged
Do not edit files.
```

Give the second explorer this prompt:

```text
Assess whether the wiki-bi absorption module map fits current wiki governance.
Return:
1. rule conflicts with wiki-domain-upgrade-framework, wiki-absorption-workflow, and wiki-maintenance-lint-checklist
2. missing review gates before merging subagent-authored wiki updates
3. risks in scaling from one-module pilot to parallel execution
Do not edit files.
```

- [ ] **Step 2: Capture the subagent findings in a durable review note**

Create `docs/wiki-bi/_meta/legacy-semantic-coverage-review.md` with this exact skeleton:

```md
# legacy semantic coverage review

> 状态：Completed
> 日期：2026-04-16

## Subagent Questions
## Coverage Findings
## Governance Findings
## Module Map Adjustments
## Pilot Gate Adjustments
## Remaining Open Questions
```

Do not copy raw subagent text verbatim. Convert it into durable findings and explicit adjustments.

- [ ] **Step 3: Refine the module map**

Update `docs/wiki-bi/_meta/wiki-legacy-semantic-absorption-module-map.md` so it includes:

```md
## Coverage Gaps Closed By Review
- which source families were originally under-covered
- which module now owns them

## Guardrails Added After Review
- why the module boundaries are now acceptable for pilot execution
```

- [ ] **Step 4: Tighten the playbook if the review surfaced merge or lint gaps**

If the review finds missing control points, add them to `docs/wiki-bi/_meta/wiki-subagent-worktree-playbook.md` under:

```md
## Pilot Exit Criteria
## Parallel Wave Admission Criteria
```

- [ ] **Step 5: Append a coverage-review log entry**

Append this log subject in `docs/wiki-bi/log.md`:

```md
## [2026-04-16 HH:MM] review | legacy semantic absorption coverage and governance
```

The bullets must state:

- what coverage blind spots were found
- what changed in the module map
- what merge gates were added before pilot execution

## Task 3: Pilot 01 In A Dedicated Worktree On Module `M6` Reference And Backfill Semantics

**Files:**
- Create: `docs/wiki-bi/evidence/reference-and-backfill-evidence.md`
- Create: `docs/wiki-bi/_meta/absorption-rounds/round-24-reference-backfill-pilot.md`
- Modify: `docs/wiki-bi/concepts/backfill.md`
- Modify: `docs/wiki-bi/surfaces/reference-sync.md`
- Modify: `docs/wiki-bi/evidence/operator-and-surface-evidence.md`
- Modify: `docs/wiki-bi/standards/output-correctness/output-correctness.md`
- Modify: `docs/wiki-bi/domains/annuity-performance.md`
- Modify: `docs/wiki-bi/domains/annuity-income.md`
- Modify: `docs/wiki-bi/domains/annual-award.md`
- Modify: `docs/wiki-bi/domains/annual-loss.md`
- Modify: `docs/wiki-bi/index.md`
- Modify: `docs/wiki-bi/log.md`
- Modify: `docs/wiki-bi/_meta/absorption-rounds/index.md`

- [ ] **Step 1: Create the pilot worktree and branch**

Run:

```powershell
git worktree add .worktrees/wiki-bi-pilot-01 -b docs/wiki-bi-pilot-01 main
git -C .worktrees/wiki-bi-pilot-01 status -sb
```

Expected:

- a new linked worktree exists at `.worktrees/wiki-bi-pilot-01`
- branch `docs/wiki-bi-pilot-01` starts from current `main`

- [ ] **Step 2: Dispatch one subagent with an explicit write set**

The subagent must own only these files:

```text
docs/wiki-bi/evidence/reference-and-backfill-evidence.md
docs/wiki-bi/concepts/backfill.md
docs/wiki-bi/surfaces/reference-sync.md
docs/wiki-bi/evidence/operator-and-surface-evidence.md
docs/wiki-bi/standards/output-correctness/output-correctness.md
docs/wiki-bi/domains/annuity-performance.md
docs/wiki-bi/domains/annuity-income.md
docs/wiki-bi/domains/annual-award.md
docs/wiki-bi/domains/annual-loss.md
docs/wiki-bi/index.md
docs/wiki-bi/log.md
docs/wiki-bi/_meta/absorption-rounds/index.md
docs/wiki-bi/_meta/absorption-rounds/round-24-reference-backfill-pilot.md
```

The subagent prompt must require:

```text
- mine semantics from config/foreign_keys.yml, config/reference_sync.yml, domain/reference_backfill/*, orchestration/reference_sync_ops.py, io/loader/*, and customer-master business-background docs
- write stable findings first into evidence, then tighten concept/surface/domain links
- keep domain pages thin
- classify unresolved items as evidence gaps, not stable conclusions
```

- [ ] **Step 3: Review the pilot diff before any merge**

Run:

```powershell
git -C .worktrees/wiki-bi-pilot-01 diff -- docs/wiki-bi
rg -n "reference-and-backfill-evidence|reference_sync|backfill|当前证据缺口" .worktrees/wiki-bi-pilot-01/docs/wiki-bi
```

Expected:

- the new evidence page has the standard evidence skeleton
- `backfill.md` stays semantic, not implementation-walkthrough driven
- domain pages link to the new evidence page without becoming thick narrative pages

- [ ] **Step 4: Merge only if the pilot passes the playbook gates**

If the review passes, run:

```powershell
git -C .worktrees/wiki-bi-pilot-01 add docs/wiki-bi
git -C .worktrees/wiki-bi-pilot-01 commit -m "docs(docs.architecture): absorb reference and backfill semantics into wiki"
git merge --ff-only docs/wiki-bi-pilot-01
git worktree remove .worktrees/wiki-bi-pilot-01
git branch -d docs/wiki-bi-pilot-01
```

If the review fails, do not merge. Update the playbook first, then rerun the pilot in a fresh worktree.

- [ ] **Step 5: Record prompt-quality lessons**

Write `docs/wiki-bi/_meta/absorption-rounds/round-24-reference-backfill-pilot.md` with this exact opening block:

```md
# Round 24：reference and backfill pilot

> 状态：Completed
> 日期：2026-04-16
> 主题簇：reference-derivation / backfill / subagent-pilot

## 本轮目标

- 用单一 subagent 验证 reference/backfill 模块的 wiki 吸收任务设计
- 检查 evidence-first 写法和 domain thin-navigation 规则能否稳定保持
- 记录下一次 pilot 要怎样收紧 prompt 和 review gate
```

## Task 4: Pilot 02 In A Dedicated Worktree On Module `M5` Identity Governance

**Files:**
- Create: `docs/wiki-bi/_meta/absorption-rounds/round-25-identity-governance-pilot.md`
- Modify: `docs/wiki-bi/concepts/company-id.md`
- Modify: `docs/wiki-bi/concepts/temp-id.md`
- Modify: `docs/wiki-bi/standards/semantic-correctness/identity-governance.md`
- Modify: `docs/wiki-bi/evidence/identity-and-lookup-evidence.md`
- Modify: `docs/wiki-bi/surfaces/company-lookup-queue.md`
- Modify: `docs/wiki-bi/surfaces/enterprise-enrichment-persistence.md`
- Modify: `docs/wiki-bi/index.md`
- Modify: `docs/wiki-bi/log.md`
- Modify: `docs/wiki-bi/_meta/absorption-rounds/index.md`
- Modify: `docs/wiki-bi/_meta/wiki-subagent-worktree-playbook.md`

- [ ] **Step 1: Create the second pilot worktree**

Run:

```powershell
git worktree add .worktrees/wiki-bi-pilot-02 -b docs/wiki-bi-pilot-02 main
git -C .worktrees/wiki-bi-pilot-02 status -sb
```

- [ ] **Step 2: Dispatch one subagent using the refined playbook**

The subagent must own only these files:

```text
docs/wiki-bi/concepts/company-id.md
docs/wiki-bi/concepts/temp-id.md
docs/wiki-bi/standards/semantic-correctness/identity-governance.md
docs/wiki-bi/evidence/identity-and-lookup-evidence.md
docs/wiki-bi/surfaces/company-lookup-queue.md
docs/wiki-bi/surfaces/enterprise-enrichment-persistence.md
docs/wiki-bi/index.md
docs/wiki-bi/log.md
docs/wiki-bi/_meta/absorption-rounds/index.md
docs/wiki-bi/_meta/absorption-rounds/round-25-identity-governance-pilot.md
```

The prompt must explicitly require separation of:

```text
- active runtime path
- compatibility inventory / historical memory
- retired fallback behavior
- operator-visible consequence
```

- [ ] **Step 3: Review whether the second pilot is cleaner than Pilot 01**

Run:

```powershell
git -C .worktrees/wiki-bi-pilot-02 diff -- docs/wiki-bi
rg -n "active runtime path|historical memory|retired|operator-visible" .worktrees/wiki-bi-pilot-02/docs/wiki-bi
```

Expected:

- identity pages are more layered than in prior wiki text
- queue and persistence surfaces do not collapse back into one summary blob
- no new orphan page is introduced

- [ ] **Step 4: Merge only if the refined prompt reduces review friction**

Run:

```powershell
git -C .worktrees/wiki-bi-pilot-02 add docs/wiki-bi
git -C .worktrees/wiki-bi-pilot-02 commit -m "docs(docs.architecture): deepen identity governance semantics in wiki"
git merge --ff-only docs/wiki-bi-pilot-02
git worktree remove .worktrees/wiki-bi-pilot-02
git branch -d docs/wiki-bi-pilot-02
```

If the review still reveals repeated defects, stop here and tighten the playbook again before Pilot 03.

- [ ] **Step 5: Record what changed in the prompt design**

In `docs/wiki-bi/_meta/absorption-rounds/round-25-identity-governance-pilot.md`, add:

```md
## Prompt Changes From Round 24
## Review Friction Reduced
## Review Friction Still Present
## Adjustments Required Before Parallel Execution
```

## Task 5: Pilot 03 In A Dedicated Worktree On Module `M7` Status And Snapshot Semantics

**Files:**
- Create: `docs/wiki-bi/evidence/customer-mdm-lifecycle-evidence.md`
- Create: `docs/wiki-bi/_meta/absorption-rounds/round-26-status-snapshot-pilot.md`
- Modify: `docs/wiki-bi/concepts/customer-status.md`
- Modify: `docs/wiki-bi/concepts/snapshot-granularity.md`
- Modify: `docs/wiki-bi/standards/semantic-correctness/customer-status-semantics.md`
- Modify: `docs/wiki-bi/evidence/status-and-snapshot-evidence.md`
- Modify: `docs/wiki-bi/surfaces/customer-mdm-commands.md`
- Modify: `docs/wiki-bi/index.md`
- Modify: `docs/wiki-bi/log.md`
- Modify: `docs/wiki-bi/_meta/absorption-rounds/index.md`
- Modify: `docs/wiki-bi/_meta/wiki-subagent-worktree-playbook.md`

- [ ] **Step 1: Create the third pilot worktree**

Run:

```powershell
git worktree add .worktrees/wiki-bi-pilot-03 -b docs/wiki-bi-pilot-03 main
git -C .worktrees/wiki-bi-pilot-03 status -sb
```

- [ ] **Step 2: Dispatch one subagent on the status module**

The subagent must own only these files:

```text
docs/wiki-bi/evidence/customer-mdm-lifecycle-evidence.md
docs/wiki-bi/concepts/customer-status.md
docs/wiki-bi/concepts/snapshot-granularity.md
docs/wiki-bi/standards/semantic-correctness/customer-status-semantics.md
docs/wiki-bi/evidence/status-and-snapshot-evidence.md
docs/wiki-bi/surfaces/customer-mdm-commands.md
docs/wiki-bi/index.md
docs/wiki-bi/log.md
docs/wiki-bi/_meta/absorption-rounds/index.md
docs/wiki-bi/_meta/absorption-rounds/round-26-status-snapshot-pilot.md
```

The prompt must require:

```text
- mine semantics from config/customer_status_rules.yml, config/customer_mdm.yaml, customer_mdm/*, cli/customer_mdm/*, cli/etl/hooks.py, and status background docs
- keep formula memory, yearly lifecycle, and operator command surfaces distinct
- put command/runtime specifics into evidence or surface pages, not the concept main prose
```

- [ ] **Step 3: Review whether the task design is now stable across a third archetype**

Run:

```powershell
git -C .worktrees/wiki-bi-pilot-03 diff -- docs/wiki-bi
rg -n "customer-mdm-lifecycle-evidence|is_new|is_winning_this_year|is_loss_reported|status_year" .worktrees/wiki-bi-pilot-03/docs/wiki-bi
```

Expected:

- the new lifecycle evidence page captures yearly-init, sync, snapshot, and ratchet-style meaning without turning into a CLI manual
- status concept and standard pages become clearer without duplicating all command details
- the review feedback is now mostly page-content judgment, not structural cleanup

- [ ] **Step 4: Merge and then declare the prompt design stable only if the third review passes**

Run:

```powershell
git -C .worktrees/wiki-bi-pilot-03 add docs/wiki-bi
git -C .worktrees/wiki-bi-pilot-03 commit -m "docs(docs.architecture): absorb status lifecycle semantics into wiki"
git merge --ff-only docs/wiki-bi-pilot-03
git worktree remove .worktrees/wiki-bi-pilot-03
git branch -d docs/wiki-bi-pilot-03
```

If the third pilot still needs major structural cleanup, do not start the parallel wave.

- [ ] **Step 5: Promote the pilot prompt to the durable playbook**

Update `docs/wiki-bi/_meta/wiki-subagent-worktree-playbook.md` so it includes:

```md
## Stable Task Prompt Shape
- raw sources
- exact write set
- forbidden page drift
- evidence-first ordering
- merge gates
```

## Task 6: Run Parallel Wave 01 On The Remaining Five Modules

**Files:**
- Create: `docs/wiki-bi/_meta/absorption-rounds/round-27-parallel-legacy-semantic-wave-01.md`
- Modify: `docs/wiki-bi/_meta/wiki-legacy-semantic-absorption-module-map.md`
- Modify: `docs/wiki-bi/index.md`
- Modify: `docs/wiki-bi/log.md`
- Modify: `docs/wiki-bi/_meta/absorption-rounds/index.md`
- Modify: `docs/wiki-bi/evidence/operator-and-surface-evidence.md`
- Modify: `docs/wiki-bi/evidence/verification-assets-evidence.md`
- Modify: `docs/wiki-bi/evidence/validation-result-history-evidence.md`
- Modify: `docs/wiki-bi/surfaces/failed-record-export.md`
- Modify: `docs/wiki-bi/surfaces/unknown-names-csv.md`
- Modify: `docs/wiki-bi/surfaces/standalone-tooling.md`
- Modify: `docs/wiki-bi/standards/verification-method/golden-scenarios.md`
- Modify: `docs/wiki-bi/standards/verification-method/real-data-validation.md`
- Modify: `docs/wiki-bi/domains/annuity-performance.md`
- Modify: `docs/wiki-bi/domains/annuity-income.md`
- Modify: `docs/wiki-bi/domains/annual-award.md`
- Modify: `docs/wiki-bi/domains/annual-loss.md`
- Modify: `docs/wiki-bi/standards/input-reality/annuity-performance-input-contract.md`
- Modify: `docs/wiki-bi/standards/input-reality/annuity-income-input-contract.md`
- Modify: `docs/wiki-bi/standards/input-reality/annual-award-input-contract.md`
- Modify: `docs/wiki-bi/standards/input-reality/annual-loss-input-contract.md`
- Modify: `docs/wiki-bi/standards/output-correctness/annuity-performance-output-contract.md`
- Modify: `docs/wiki-bi/standards/output-correctness/annuity-income-output-contract.md`
- Modify: `docs/wiki-bi/standards/output-correctness/annual-award-output-contract.md`
- Modify: `docs/wiki-bi/standards/output-correctness/annual-loss-output-contract.md`
- Modify: `docs/wiki-bi/evidence/annuity-performance-field-processing-evidence.md`
- Modify: `docs/wiki-bi/evidence/annuity-income-field-processing-evidence.md`
- Modify: `docs/wiki-bi/evidence/annual-award-field-processing-evidence.md`
- Modify: `docs/wiki-bi/evidence/annual-loss-field-processing-evidence.md`

- [ ] **Step 1: Admit the parallel wave only if all three pilots passed**

Update the module map to mark:

```md
- `M5`: `accepted-pilot`
- `M6`: `accepted-pilot`
- `M7`: `accepted-pilot`
- `M1`, `M2`, `M3`, `M4`, `M8`: `wave-01`
```

Do not admit the parallel wave if any pilot was merged only after major manual rewrite.

- [ ] **Step 2: Create one worktree per remaining module**

Run:

```powershell
git worktree add .worktrees/wiki-bi-module-ap -b docs/wiki-bi-module-ap main
git worktree add .worktrees/wiki-bi-module-ai -b docs/wiki-bi-module-ai main
git worktree add .worktrees/wiki-bi-module-aa -b docs/wiki-bi-module-aa main
git worktree add .worktrees/wiki-bi-module-al -b docs/wiki-bi-module-al main
git worktree add .worktrees/wiki-bi-module-ops -b docs/wiki-bi-module-ops main
```

Ownership map:

- `.worktrees/wiki-bi-module-ap` -> `M1`
- `.worktrees/wiki-bi-module-ai` -> `M2`
- `.worktrees/wiki-bi-module-aa` -> `M3`
- `.worktrees/wiki-bi-module-al` -> `M4`
- `.worktrees/wiki-bi-module-ops` -> `M8`

- [ ] **Step 3: Dispatch one subagent per worktree with disjoint write sets**

Use the stable prompt shape from the playbook.

Each subagent must be told:

```text
- you are not alone in the codebase
- do not edit files outside your assigned module write set
- do not revert or normalize work done by other module workers
- if a finding crosses into another module, leave it as an evidence gap or note instead of editing the other module’s files
```

- [ ] **Step 4: Review and merge each module independently**

Run the review commands in this exact form:

```powershell
git -C .worktrees/wiki-bi-module-ap diff -- docs/wiki-bi
git -C .worktrees/wiki-bi-module-ai diff -- docs/wiki-bi
git -C .worktrees/wiki-bi-module-aa diff -- docs/wiki-bi
git -C .worktrees/wiki-bi-module-al diff -- docs/wiki-bi
git -C .worktrees/wiki-bi-module-ops diff -- docs/wiki-bi
rg -n "当前证据缺口|supported_pages|current_test|current_reference_asset|current_runbook" .worktrees/wiki-bi-module-ap/docs/wiki-bi .worktrees/wiki-bi-module-ai/docs/wiki-bi .worktrees/wiki-bi-module-aa/docs/wiki-bi .worktrees/wiki-bi-module-al/docs/wiki-bi .worktrees/wiki-bi-module-ops/docs/wiki-bi
```

Merge only the modules that pass review:

```powershell
git -C .worktrees/wiki-bi-module-ap add docs/wiki-bi
git -C .worktrees/wiki-bi-module-ap commit -m "docs(docs.architecture): deepen annuity-performance semantic coverage in wiki"
git merge --ff-only docs/wiki-bi-module-ap
git worktree remove .worktrees/wiki-bi-module-ap
git branch -d docs/wiki-bi-module-ap

git -C .worktrees/wiki-bi-module-ai add docs/wiki-bi
git -C .worktrees/wiki-bi-module-ai commit -m "docs(docs.architecture): deepen annuity-income semantic coverage in wiki"
git merge --ff-only docs/wiki-bi-module-ai
git worktree remove .worktrees/wiki-bi-module-ai
git branch -d docs/wiki-bi-module-ai

git -C .worktrees/wiki-bi-module-aa add docs/wiki-bi
git -C .worktrees/wiki-bi-module-aa commit -m "docs(docs.architecture): deepen annual-award semantic coverage in wiki"
git merge --ff-only docs/wiki-bi-module-aa
git worktree remove .worktrees/wiki-bi-module-aa
git branch -d docs/wiki-bi-module-aa

git -C .worktrees/wiki-bi-module-al add docs/wiki-bi
git -C .worktrees/wiki-bi-module-al commit -m "docs(docs.architecture): deepen annual-loss semantic coverage in wiki"
git merge --ff-only docs/wiki-bi-module-al
git worktree remove .worktrees/wiki-bi-module-al
git branch -d docs/wiki-bi-module-al

git -C .worktrees/wiki-bi-module-ops add docs/wiki-bi
git -C .worktrees/wiki-bi-module-ops commit -m "docs(docs.architecture): deepen operator and verification semantics in wiki"
git merge --ff-only docs/wiki-bi-module-ops
git worktree remove .worktrees/wiki-bi-module-ops
git branch -d docs/wiki-bi-module-ops
```

If one module fails review, hold only that module back. Do not block already-clean modules from merging.

- [ ] **Step 5: Record the full-wave closeout**

Create `docs/wiki-bi/_meta/absorption-rounds/round-27-parallel-legacy-semantic-wave-01.md` with these mandatory sections:

```md
# Round 27：parallel legacy semantic wave 01

> 状态：Completed
> 日期：2026-04-16
> 主题簇：parallel-wave / wiki-bi / legacy-semantics

## Modules Executed
## Modules Merged
## Modules Held Back
## Reusable Prompt Pattern
## Review Failure Patterns
## Next Wave Admission Rules
```

## Validation

For the full program, verify:

- the module map covers both first-wave domain semantics and cross-cutting semantics hidden in config/code/operator paths
- every pilot ran in its own linked worktree and merged only after review
- the parallel wave used disjoint write sets and did not rely on one shared dirty workspace
- touched evidence pages still obey the current wiki evidence skeleton
- touched domain pages remain navigation-oriented
- `index.md`, `log.md`, and `_meta/absorption-rounds/index.md` remain aligned with all new or revised durable pages

Suggested commands:

```powershell
rg -n "legacy semantic absorption|reference-and-backfill-evidence|customer-mdm-lifecycle-evidence|wave 01|pilot" docs/wiki-bi
git diff -- docs/wiki-bi docs/superpowers/plans
git status -sb
```

## Expected Outcome

After this plan is executed:

- `wiki-bi` will have a durable module map for continuing legacy-semantic absorption instead of relying on opportunistic edits
- the subagent workflow will be validated through three reviewed pilots before any parallel scaling
- hidden business semantics from reference/backfill, identity governance, and status lifecycle will be absorbed through controlled pilot rounds
- the remaining domain and operator/verification modules will be ready for safe parallel execution with explicit worktree isolation and merge gates

## Execution Handoff

Plan complete and saved to `docs/superpowers/plans/2026-04-16-workdatahubpro-wiki-bi-legacy-semantic-absorption-plan.md`.

Two execution options:

1. Subagent-Driven (recommended) - I dispatch a fresh subagent per task, review between tasks, fast iteration
2. Inline Execution - Execute tasks in this session using executing-plans, batch execution with checkpoints

Which approach?

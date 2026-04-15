# WorkDataHubPro Wiki BI Production-Sample Augmentation Plan

> **Statu:** Not Implemented

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Upgrade `docs/wiki-bi/` so it reflects not only contract-grade legacy behavior but also observed production-sample reality from `E:\Projects\WorkDataHub\data\real_data\202602\收集数据\`, giving the next Pro refactor phase more concrete business guidance.

**Architecture:** Keep `wiki-bi` in its current role as a problem-space and evidence-space wiki. Use the legacy repository and the `202602` production sample to strengthen durable evidence, distinguish accepted contracts from observed production variants, and explicitly classify adjacent operator workbooks instead of letting them remain implicit institutional memory. Do not copy raw production files into the repo and do not let one observed month silently overwrite existing accepted contracts.

**Tech Stack:** Markdown in `docs/wiki-bi/` and `docs/superpowers/plans/`, legacy `WorkDataHub` docs/config/code, real production workbook metadata from `E:\Projects\WorkDataHub\data\real_data\202602\收集数据\`, PowerShell, `rg`, `uv run python`

---

## Why This Plan Now

- `docs/wiki-bi/evidence/input-reality-evidence.md` already says the wiki still lacks object-level evidence for concrete workbook shape and sample type.
- `docs/wiki-bi/standards/verification-method/real-data-validation.md` explicitly says real-data sample is still a governed target, not a repo-native closed asset.
- The architecture blueprint says legacy parity is evidence for adjudication, not a structural template, so the right next move is to absorb more behavior reality without copying old architecture.
- The `202602` sample shows concrete realities that the wiki does not yet state directly:
  - the annuity workbook family currently contains both `规模明细` and `收入明细` in one physical workbook
  - `业务收集\V1\台账登记v1.xlsx` contains the accepted event-domain sheets plus many adjacent operator sheets
  - `业务收集\V1\【截至2月汇总】26年企年受托投资中标流失清单 20260305.xlsx` exists as an adjacent summary workbook with different sheet names and should not be silently conflated with the accepted event-domain input contract

## Scope Check

This plan covers:

- strengthening `wiki-bi` with production-sample-backed evidence
- separating stable accepted contracts from observed workbook variants
- making adjacent operator workbooks and summary sheets explicit wiki objects
- updating domain pages so they can answer “what does real production data look like” more concretely than they do today

This plan does not cover:

- changing runtime code in `src/work_data_hub_pro/`
- checking raw production data into the repository
- rewriting accepted input contracts based on one observed month without explicit evidence framing
- reopening first-wave slice admission or coverage-matrix status by itself

## Proposed File Structure

### Files To Create

- `docs/wiki-bi/_meta/absorption-rounds/round-23-production-sample-augmentation.md`
- `docs/wiki-bi/evidence/annuity-workbook-family-evidence.md`
- `docs/wiki-bi/evidence/business-collection-workbook-variants-evidence.md`
- `docs/wiki-bi/surfaces/business-collection-ledger-workbook.md`

### Files To Modify

- `docs/wiki-bi/_meta/wiki-absorption-roadmap.md`
- `docs/wiki-bi/_meta/absorption-rounds/index.md`
- `docs/wiki-bi/index.md`
- `docs/wiki-bi/log.md`
- `docs/wiki-bi/evidence/input-reality-evidence.md`
- `docs/wiki-bi/evidence/operator-and-surface-evidence.md`
- `docs/wiki-bi/standards/input-reality/input-reality-contracts.md`
- `docs/wiki-bi/standards/verification-method/real-data-validation.md`
- `docs/wiki-bi/standards/input-reality/annuity-performance-input-contract.md`
- `docs/wiki-bi/standards/input-reality/annuity-income-input-contract.md`
- `docs/wiki-bi/standards/input-reality/annual-award-input-contract.md`
- `docs/wiki-bi/standards/input-reality/annual-loss-input-contract.md`
- `docs/wiki-bi/domains/annuity-performance.md`
- `docs/wiki-bi/domains/annuity-income.md`
- `docs/wiki-bi/domains/annual-award.md`
- `docs/wiki-bi/domains/annual-loss.md`

## Execution Guardrails

- reproduce workbook metadata from the external `202602` sample before editing any durable wiki page
- keep new object-level evidence pages on the standard skeleton:
  - `## 结论主题`
  - `## 证据记录`
  - `## 本轮已吸收的稳定结论`
  - `## 哪些来源是强证`
  - `## 哪些来源只是旁证`
  - `## 当前证据缺口`
- treat the two new evidence pages as observation pages first:
  - `annuity-workbook-family-evidence.md` records workbook-family findings and bounded claims only
  - `business-collection-workbook-variants-evidence.md` records workbook-variant findings and bounded claims only
- treat `surfaces/business-collection-ledger-workbook.md` as the interpretation and governance page:
  - explain why the ledger workbook is a surface
  - do not duplicate full sheet-by-sheet evidence already captured in the evidence page
- when recording workbook metadata derived from external production samples in an evidence table, use `current_reference_asset` and state explicitly in `notes` that:
  - the source is external workbook metadata observed from a non-repo-native production file
  - only workbook metadata and sheet names are being written back
  - the raw production workbook is not committed into this repository

## Task 1: Reproduce External Sample Metadata And Admit A Dedicated Production-Sample Augmentation Round

**Files:**
- Create: `docs/wiki-bi/_meta/absorption-rounds/round-23-production-sample-augmentation.md`
- Modify: `docs/wiki-bi/_meta/wiki-absorption-roadmap.md`
- Modify: `docs/wiki-bi/_meta/absorption-rounds/index.md`
- Modify: `docs/wiki-bi/index.md`
- Modify: `docs/wiki-bi/log.md`

- [ ] **Step 1: Reproduce workbook metadata before editing durable pages**

Run:

```powershell
@'
from pathlib import Path
from openpyxl import load_workbook
files = [
    Path(r'E:\Projects\WorkDataHub\data\real_data\202602\收集数据\数据采集\V1\【年金规模收入】26年2月年金业务规模明细(手工汇总)v1.xlsx'),
    Path(r'E:\Projects\WorkDataHub\data\real_data\202602\收集数据\业务收集\V1\台账登记v1.xlsx'),
    Path(r'E:\Projects\WorkDataHub\data\real_data\202602\收集数据\业务收集\V1\【截至2月汇总】26年企年受托投资中标流失清单 20260305.xlsx'),
]
for path in files:
    wb = load_workbook(path, read_only=True)
    print(path.name)
    print("  sheets=" + ", ".join(wb.sheetnames))
    wb.close()
'@ | uv run python -
```

Expected:

- the annuity workbook prints `规模明细, 收入明细`
- `台账登记v1.xlsx` prints a long sheet list including `企年受托流失(解约)` and `企年投资流失(解约)`
- the summary workbook prints `表1 受托考核加扣分反馈` and `表2 投资考核加扣分反馈`

- [ ] **Step 2: Confirm the current wiki still states workbook-shape evidence as a gap**

Run:

```powershell
rg -n "workbook shape|sample 类型|对象级 evidence|real-data sample" docs/wiki-bi
```

Expected:

- matches in `docs/wiki-bi/evidence/input-reality-evidence.md`
- matches in `docs/wiki-bi/standards/verification-method/real-data-validation.md`
- no existing round dedicated to production-sample augmentation

- [ ] **Step 3: Add Round 23 to the absorption roadmap**

Add a new section to `docs/wiki-bi/_meta/wiki-absorption-roadmap.md` with this structure:

```md
## Round 23: production-sample augmentation

Goal:

- absorb concrete workbook-family and workbook-variant reality from the legacy project and `202602` production sample
- strengthen wiki answers about real production input without collapsing observed variants into accepted contracts
- classify adjacent business-collection workbooks as explicit surfaces or evidence objects

Entry pages:

- `evidence/input-reality-evidence.md`
- `standards/input-reality/input-reality-contracts.md`
- `standards/verification-method/real-data-validation.md`
- `evidence/operator-and-surface-evidence.md`

Status:

- planned
```

- [ ] **Step 4: Create the Round 23 document with planned closeout sections**

Create `docs/wiki-bi/_meta/absorption-rounds/round-23-production-sample-augmentation.md` with this opening block and section structure:

```md
# Round 23: production-sample augmentation

> 状态：Planned
> 日期：2026-04-15
> 主题簇：input-reality / production-sample / operator-surface

## 本轮目标

- 用 `E:\Projects\WorkDataHub` 与 `E:\Projects\WorkDataHub\data\real_data\202602\收集数据\` 补强 wiki 对真实生产数据形态的表达
- 把 accepted contract 与 observed production variants 明确分层
- 把台账型 workbook、汇总型 workbook 与相邻 sheet 现实升级成显式治理对象

## Raw Sources

- `E:\Projects\WorkDataHub\config\data_sources.yml`
- `E:\Projects\WorkDataHub\docs\domains\annuity_performance-capability-map.md`
- `E:\Projects\WorkDataHub\docs\domains\annuity_income-capability-map.md`
- `E:\Projects\WorkDataHub\docs\domains\annual_award-capability-map.md`
- `E:\Projects\WorkDataHub\docs\domains\annual_loss-capability-map.md`
- `E:\Projects\WorkDataHub\data\real_data\202602\收集数据\数据采集\V1\【年金规模收入】26年2月年金业务规模明细(手工汇总)v1.xlsx`
- `E:\Projects\WorkDataHub\data\real_data\202602\收集数据\业务收集\V1\台账登记v1.xlsx`
- `E:\Projects\WorkDataHub\data\real_data\202602\收集数据\业务收集\V1\【截至2月汇总】26年企年受托投资中标流失清单 20260305.xlsx`

## Exit Criteria

- concrete workbook-family and workbook-variant evidence exists as durable pages
- four first-wave domain pages can answer “real production data currently looks like what” with bounded, sourced statements
- adjacent operator workbooks are no longer left as unnamed context outside the wiki

## Planned Stable Findings

- the `202602` annuity workbook family currently exposes both `规模明细` and `收入明细` in one physical workbook while keeping domain-specific sheet contracts separate
- the `业务收集\V1` folder currently contains both accepted event-domain sheets and adjacent operator/summarization workbooks that must not be auto-promoted into accepted contracts
- workbook metadata from external production samples can be written back as bounded evidence without turning raw files into repository assets

## Reusable Maintenance Lessons To Validate

- object-level workbook evidence should land in `evidence/` before downstream contract and domain pages are tightened
- workbook-variant observation pages and surface-governance pages should not carry the same responsibility
- one observed month can strengthen explainability and discovery guidance without redefining a universal input contract

## Next Entry Points If Variance Remains Open

- `evidence/input-reality-evidence.md`
- `evidence/operator-and-surface-evidence.md`
- `standards/verification-method/real-data-validation.md`
```

- [ ] **Step 5: Register the round in index and log**

Update:

- `docs/wiki-bi/_meta/absorption-rounds/index.md`
- `docs/wiki-bi/index.md`
- `docs/wiki-bi/log.md`

Use this log subject:

```md
## [2026-04-15 HH:MM] plan | Round 23 production-sample augmentation

- planned a wiki maintenance round focused on legacy plus `202602` production-sample reality
- scoped the round around workbook-family evidence, workbook variants, and business-collection adjacent surfaces
```

## Task 2: Create Durable Evidence For The Two Production Workbook Families

**Files:**
- Create: `docs/wiki-bi/evidence/annuity-workbook-family-evidence.md`
- Create: `docs/wiki-bi/evidence/business-collection-workbook-variants-evidence.md`
- Modify: `docs/wiki-bi/evidence/input-reality-evidence.md`
- Modify: `docs/wiki-bi/standards/input-reality/input-reality-contracts.md`

- [ ] **Step 1: Capture the annuity workbook family as its own evidence object using the standard evidence skeleton**

Create `docs/wiki-bi/evidence/annuity-workbook-family-evidence.md` with these required findings:

```md
- `数据采集\V1\【年金规模收入】26年2月年金业务规模明细(手工汇总)v1.xlsx` currently contains both `规模明细` and `收入明细`
- this strengthens the existing wiki claim that `annuity_performance` and `annuity_income` share one workbook family but consume different sheets
- shared physical workbook does not collapse the two domains into one contract; sheet contract remains domain-specific
```

Required source anchors:

```md
- `E:\Projects\WorkDataHub\config\data_sources.yml`
- workbook metadata observed from `E:\Projects\WorkDataHub\data\real_data\202602\收集数据\数据采集\V1\【年金规模收入】26年2月年金业务规模明细(手工汇总)v1.xlsx`
- relevant capability maps for `annuity_performance` and `annuity_income`
```

Page requirements:

```md
- keep the standard object-evidence skeleton:
  - `## 结论主题`
  - `## 证据记录`
  - `## 本轮已吸收的稳定结论`
  - `## 哪些来源是强证`
  - `## 哪些来源只是旁证`
  - `## 当前证据缺口`
- include at least one `current_reference_asset` evidence row whose `notes` explicitly say the workbook metadata comes from an external, non-repo-native production file
- keep the page at observation/evidence level; do not use it to argue that the workbook family is itself a surface object
```

- [ ] **Step 2: Capture business-collection workbook variants as their own evidence object using the standard evidence skeleton**

Create `docs/wiki-bi/evidence/business-collection-workbook-variants-evidence.md` with these required findings:

```md
- `业务收集\V1\台账登记v1.xlsx` contains the accepted event-domain sheets and many adjacent sheets
- `业务收集\V1\【截至2月汇总】26年企年受托投资中标流失清单 20260305.xlsx` is a real adjacent workbook with different sheet names such as `表1 受托考核加扣分反馈` and `表2 投资考核加扣分反馈`
- these adjacent workbooks should be treated as observed production variants or operator surfaces unless stronger evidence admits them into a domain input contract
```

Required source anchors:

```md
- `E:\Projects\WorkDataHub\config\data_sources.yml`
- workbook metadata observed from the two `业务收集\V1` files above
- relevant capability maps for `annual_award` and `annual_loss`
```

Page requirements:

```md
- keep the standard object-evidence skeleton:
  - `## 结论主题`
  - `## 证据记录`
  - `## 本轮已吸收的稳定结论`
  - `## 哪些来源是强证`
  - `## 哪些来源只是旁证`
  - `## 当前证据缺口`
- include `current_reference_asset` evidence rows for the external workbook metadata observations and mark in `notes` that only metadata and sheet names are being written back
- keep the page at observation/evidence level; do not use it to fully explain why the ledger workbook is a governance surface
```

- [ ] **Step 3: Rewire the aggregate input-reality pages**

Update `docs/wiki-bi/evidence/input-reality-evidence.md` so it:

- links to `annuity-workbook-family-evidence.md`
- links to `business-collection-workbook-variants-evidence.md`
- changes the current gap wording from generic “workbook shape still missing” to more specific remaining gaps

Update `docs/wiki-bi/standards/input-reality/input-reality-contracts.md` so it adds:

```md
- accepted contract and observed production variant are different evidence layers
- observed workbook variants can strengthen input reality understanding without automatically becoming accepted source contracts
```

## Task 3: Tighten The Four Domain Input Contracts And Navigation Pages

**Files:**
- Modify: `docs/wiki-bi/standards/input-reality/annuity-performance-input-contract.md`
- Modify: `docs/wiki-bi/standards/input-reality/annuity-income-input-contract.md`
- Modify: `docs/wiki-bi/standards/input-reality/annual-award-input-contract.md`
- Modify: `docs/wiki-bi/standards/input-reality/annual-loss-input-contract.md`
- Modify: `docs/wiki-bi/domains/annuity-performance.md`
- Modify: `docs/wiki-bi/domains/annuity-income.md`
- Modify: `docs/wiki-bi/domains/annual-award.md`
- Modify: `docs/wiki-bi/domains/annual-loss.md`

- [ ] **Step 1: Upgrade the two annuity-domain contracts**

In both annuity-domain input contracts, add an “observed production reality” subsection that says:

```md
- the current observed `202602` workbook family contains both `规模明细` and `收入明细` in one physical workbook
- `annuity_performance` still owns the `规模明细` sheet contract
- `annuity_income` still owns the `收入明细` sheet contract
- the shared workbook family strengthens workbook-discovery and explainability understanding, not domain collapse
```

Add `annuity-workbook-family-evidence.md` to related evidence in:

- `docs/wiki-bi/standards/input-reality/annuity-performance-input-contract.md`
- `docs/wiki-bi/standards/input-reality/annuity-income-input-contract.md`
- `docs/wiki-bi/domains/annuity-performance.md`
- `docs/wiki-bi/domains/annuity-income.md`

- [ ] **Step 2: Upgrade the two event-domain contracts**

In both event-domain input contracts, add an “observed production reality” subsection that says:

```md
- `台账登记v1.xlsx` is a currently observed production workbook that contains the accepted event-domain sheets
- the same business-collection folder also contains adjacent summary and attachment-style workbooks
- those adjacent workbooks should not be silently rewritten into the accepted event-domain contract without stronger source support
```

Add `business-collection-workbook-variants-evidence.md` to related evidence in:

- `docs/wiki-bi/standards/input-reality/annual-award-input-contract.md`
- `docs/wiki-bi/standards/input-reality/annual-loss-input-contract.md`
- `docs/wiki-bi/domains/annual-award.md`
- `docs/wiki-bi/domains/annual-loss.md`

- [ ] **Step 3: Make the domain pages answer the user’s original question more directly**

Update each of the four domain pages so they can answer:

```md
- what the accepted source contract is
- what is currently observed in `202602`
- which part is stable contract
- which part is only observed production variant or adjacent operator reality
```

Do not turn these domain pages into code walkthroughs or execution diaries.

## Task 4: Register Business-Collection Ledger Reality As An Explicit Surface

**Files:**
- Create: `docs/wiki-bi/surfaces/business-collection-ledger-workbook.md`
- Modify: `docs/wiki-bi/evidence/operator-and-surface-evidence.md`
- Modify: `docs/wiki-bi/index.md`

- [ ] **Step 1: Create the new surface page with a non-duplicative boundary**

Create `docs/wiki-bi/surfaces/business-collection-ledger-workbook.md` with these required sections:

```md
# business collection ledger workbook

## Surface Object
## Why It Is A Surface Instead Of A Domain Contract
## Observed Production Reality
## Relationship To `annual_award` And `annual_loss`
## Non-Goals
## Key Evidence
```

The page must state:

```md
- `台账登记v1.xlsx` is not just a neutral container; it is a workbook-level operator surface with multiple adjacent sheets
- the presence of adjacent sheets means “business collection workbook” is a broader runtime/operator object than either single event-domain contract
- summary workbooks in the same folder should be classified here or in evidence first, not auto-admitted into event-domain input contracts
```

Boundary rule:

```md
- this page is the interpretation/governance layer for the ledger workbook as a surface
- do not repeat full sheet inventories already captured in `business-collection-workbook-variants-evidence.md` except when a short example is needed
- prefer linking back to the evidence page for workbook-shape details and to domain input-contract pages for accepted event-domain contracts
```

- [ ] **Step 2: Link the new surface back into the surface evidence dispatcher**

Update `docs/wiki-bi/evidence/operator-and-surface-evidence.md` so it:

- links to `surfaces/business-collection-ledger-workbook.md`
- states that production-sample workbook variants in `业务收集` are now explicitly tracked as a surface/evidence topic instead of remaining only in chat or folder memory

- [ ] **Step 3: Register the new surface in the root catalog**

Add one entry to `docs/wiki-bi/index.md` under Surfaces:

```md
- [business collection ledger workbook](./surfaces/business-collection-ledger-workbook.md) : 识别 `业务收集` 下台账型 workbook 及其相邻 summary / attachment 现实属于显式治理 surface。
```

## Task 5: Tighten Real-Data Validation Guidance For Production-Sample Writeback

**Files:**
- Modify: `docs/wiki-bi/standards/verification-method/real-data-validation.md`
- Modify: `docs/wiki-bi/evidence/input-reality-evidence.md`

- [ ] **Step 1: Add a production-sample writeback rule**

Add these rules to `docs/wiki-bi/standards/verification-method/real-data-validation.md`:

```md
- workbook metadata observed from real production samples may be written back as evidence even when raw files themselves are not repository assets
- such writeback must record whether the finding is accepted contract, observed variant, or adjacent operator reality
- one observed month may strengthen or falsify assumptions, but it does not by itself promote a variant into a universal contract
```

- [ ] **Step 2: Update the remaining gap statement**

Tighten `docs/wiki-bi/evidence/input-reality-evidence.md` so the remaining gap is no longer “we know nothing concrete”, but instead:

```md
- additional months and more object-level workbook-variant evidence are still needed
- current `202602` observations improve confidence but do not yet close multi-month production variance
```

## Task 6: Verify The Documentation Network And Stop Conditions

**Files:**
- Verify: `docs/wiki-bi/`
- Verify: `docs/superpowers/plans/2026-04-15-workdatahubpro-wiki-bi-production-sample-augmentation-plan.md`

- [ ] **Step 1: Verify the new object-level evidence pages still follow the required skeleton and metadata-source convention**

Run:

```powershell
rg -n "## 结论主题|## 证据记录|## 本轮已吸收的稳定结论|## 哪些来源是强证|## 哪些来源只是旁证|## 当前证据缺口|current_reference_asset" docs/wiki-bi/evidence/annuity-workbook-family-evidence.md docs/wiki-bi/evidence/business-collection-workbook-variants-evidence.md
```

Expected:

- both new evidence pages expose the full standard skeleton
- both new evidence pages include `current_reference_asset`
- the pages make it explicit that only workbook metadata and sheet names were written back from external production files

- [ ] **Step 2: Verify the new pages are reachable**

Run:

```powershell
rg -n "round-23-production-sample-augmentation|annuity-workbook-family-evidence|business-collection-workbook-variants-evidence|business-collection-ledger-workbook" docs/wiki-bi
```

Expected:

- matches in the new pages
- matches in `docs/wiki-bi/index.md`
- matches in `docs/wiki-bi/log.md`
- matches in the relevant contract or evidence dispatcher pages

- [ ] **Step 3: Verify the final claims stay within the planned guardrails and page-boundary split**

Run:

```powershell
rg -n "accepted contract|observed production reality|observed production variant|adjacent operator|surface" docs/wiki-bi
git diff -- docs/wiki-bi docs/superpowers/plans
```

Expected:

- touched pages clearly separate accepted contract from observed production variant
- workbook-variant evidence pages stay on observation/evidence duty, while `business-collection-ledger-workbook.md` carries the surface interpretation duty
- no diff adds raw data payloads or workbook contents beyond necessary metadata and sheet names

- [ ] **Step 4: Close the round note with execution results instead of leaving only the opening block**

Before ending the round, update `docs/wiki-bi/_meta/absorption-rounds/round-23-production-sample-augmentation.md` so it contains a completed closeout, not just the initial scaffold.

Minimum closeout content:

```md
## Stable Findings Absorbed

- list the durable findings that actually made it into `evidence/`, `standards/`, `surfaces/`, and `domains/`

## Reusable Maintenance Lessons

- state what this round proved about object-level workbook evidence, external sample writeback, and surface/evidence separation

## Next Entry Points

- name the next unresolved page or question if multi-month variance is still open
```

- [ ] **Step 5: Stop if the evidence level is weaker than the prose claim**

If any new page tries to claim:

```md
- a universal contract from one observed month
- that a summary workbook is an accepted domain source without stronger support
- that adjacent operator sheets are part of a fact-domain contract by default
```

stop and rewrite the page as:

```md
- observed production variant
- adjacent operator reality
- open question requiring more months or stronger source support
```

## Expected Outcome

After this plan is executed:

- `wiki-bi` will answer the production-data-shape question with concrete, sourced statements instead of only abstract contract summaries
- the four first-wave domains will each distinguish accepted source contract from current production observation
- `业务收集` workbook reality will no longer remain an unnamed context blob outside the wiki
- the next Pro refactor phase will have more credible guidance about what is true in production, what is only observed, and what remains unresolved

## Execution Handoff

Plan complete and saved to `docs/superpowers/plans/2026-04-15-workdatahubpro-wiki-bi-production-sample-augmentation-plan.md`.

Two execution options:

1. Subagent-Driven (recommended) - I dispatch a fresh subagent per task, review between tasks, fast iteration
2. Inline Execution - Execute tasks in this session using executing-plans, batch execution with checkpoints

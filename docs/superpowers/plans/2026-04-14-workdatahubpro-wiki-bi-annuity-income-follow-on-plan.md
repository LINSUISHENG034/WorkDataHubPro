# Wiki BI Annuity Income Follow-On Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn `docs/wiki-bi/` into a direct admission input for the pending `annuity_income` first-wave slice instead of continuing with lower-priority generic wiki expansion.

**Architecture:** Keep `wiki-bi` in the problem-space role defined by its own schema: absorb stable findings, split durable evidence where the current pages already show repeatable gaps, then hand those findings to a dedicated `annuity_income` slice plan. Do not mix this work with Phase E runtime decisions such as `company_lookup_queue`, `reference_sync`, or manual `customer-mdm` retention unless a raw source proves they block `annuity_income` slice admission directly.

**Tech Stack:** Markdown, repository governance specs, legacy `WorkDataHub` docs/config/code references, PowerShell, `rg`

---

## Why This Plan Now

- `docs/wiki-bi/_meta/wiki-absorption-roadmap.md` says the first six absorption rounds are complete and follow-on work should now be selected intentionally.
- `docs/wiki-bi/_meta/absorption-rounds/round-06-annuity-income.md` says the most valuable unfinished thread is `annuity_income` branch mapping, ID5 retirement, and unknown-name/operator artifact detail.
- `docs/wiki-bi/_meta/absorption-rounds/round-07-is-new-evidence-split.md` proves object-level evidence splitting works, but it is a lower program priority than the only unclosed first-wave domain.
- `docs/superpowers/specs/2026-04-11-workdatahubpro-refactor-program.md` marks `annuity_income` as the next recommended slice.
- `docs/superpowers/specs/2026-04-11-workdatahubpro-first-wave-legacy-coverage-matrix.md` shows AI-001 through AI-005 are still pending and there is no accepted executable slice.

## Scope And Non-Goals

- In scope:
  - a new `wiki-bi` absorption round focused on `annuity_income` slice admission
  - object-level evidence extraction for the specific `annuity_income` gaps already called out by the wiki
  - a tracked executable slice plan for `annuity_income`
  - coverage-matrix updates that move `annuity_income` rows from implicit future work to an explicit planned path
- Out of scope:
  - generic follow-on splits such as `is_winning_this_year` or `is_loss_reported`
  - final retain/replace/retire decisions for `company_lookup_queue`, `reference_sync`, or manual `customer-mdm` commands
  - Phase E production runtime closure

### Task 1: Admit Round 08 For `annuity_income`

**Files:**
- Create: `docs/wiki-bi/_meta/absorption-rounds/round-08-annuity-income-slice-admission.md`
- Modify: `docs/wiki-bi/_meta/wiki-absorption-roadmap.md`
- Modify: `docs/wiki-bi/_meta/absorption-rounds/index.md`
- Modify: `docs/wiki-bi/index.md`
- Modify: `docs/wiki-bi/log.md`

- [ ] **Step 1: Confirm `annuity_income` is still missing a dedicated slice plan**

Run:

```powershell
rg -n "annuity_income|annuity income" docs/superpowers/plans
```

Expected: references from earlier slice plans and governance addenda exist, but no dedicated `docs/superpowers/plans/*annuity-income*.md` slice plan exists yet.

- [ ] **Step 2: Add Round 08 to `wiki-absorption-roadmap.md`**

Insert this block after the Round 07 section:

```md
## Round 08: `annuity_income` slice admission package

Goal:

- convert `annuity_income` institutional memory into slice-admission-ready evidence
- split branch-mapping, ID5 retirement, and operator-artifact gaps into durable evidence objects
- feed the next executable slice plan without turning `wiki-bi` into an execution diary

Entry pages:

- `evidence/annuity-income-gap-evidence.md`
- `evidence/identity-and-lookup-evidence.md`
- `evidence/operator-and-surface-evidence.md`
- `evidence/verification-assets-evidence.md`

Status:

- planned
```

- [ ] **Step 3: Create the new round document**

Create `docs/wiki-bi/_meta/absorption-rounds/round-08-annuity-income-slice-admission.md` with this starting content:

```md
# Round 08: `annuity_income` slice admission package

> Status: Planned
> Date: 2026-04-14
> Theme: annuity-income / slice-admission bridge

## Goal

- translate `wiki-bi` institutional memory into slice-admission-ready evidence
- close the highest-value `annuity_income` evidence gaps before writing the executable slice plan

## Raw Sources

- `E:\Projects\WorkDataHub\docs\domains\annuity_income.md`
- `E:\Projects\WorkDataHub\docs\domains\annuity_income-capability-map.md`
- `E:\Projects\WorkDataHub\docs\cleansing-rules\annuity-income.md`
- `E:\Projects\WorkDataHub\docs\guides\validation\legacy-parity-validation.md`
- `docs/superpowers/audits/2026-04-12-legacy-code-audit.md`
- `docs/superpowers/audits/2026-04-12-verification-assets-search-findings.md`

## Target Pages

- `docs/wiki-bi/evidence/annuity-income-gap-evidence.md`
- `docs/wiki-bi/evidence/annuity-income-branch-mapping-evidence.md`
- `docs/wiki-bi/evidence/annuity-income-id5-retirement-evidence.md`
- `docs/wiki-bi/evidence/annuity-income-operator-artifacts-evidence.md`
- `docs/wiki-bi/domains/annuity-income.md`
- `docs/wiki-bi/surfaces/unknown-names-csv.md`
- `docs/wiki-bi/surfaces/failed-record-export.md`

## Exit Criteria

- `annuity_income` no longer depends on one catch-all evidence page for its most repeated gaps
- the wiki points directly to durable evidence for branch mapping, ID5 retirement, and operator artifacts
- the next executable slice plan can cite wiki pages instead of only audits and institutional memory
```

- [ ] **Step 4: Update the round index, root index, and log**

Add one new catalog entry for Round 08 to `docs/wiki-bi/_meta/absorption-rounds/index.md`, one new meta entry to `docs/wiki-bi/index.md`, and one append-only entry to `docs/wiki-bi/log.md` with this subject:

```md
## [2026-04-14] plan | Round 08 `annuity_income` slice admission package

- planned the next `wiki-bi` round around `annuity_income` branch mapping, ID5 retirement, and operator artifacts
- aligned the round target with the first-wave governance baseline that marks `annuity_income` as the next recommended slice
```

- [ ] **Step 5: Commit the roadmap admission**

Run:

```powershell
git add docs/wiki-bi/_meta/wiki-absorption-roadmap.md docs/wiki-bi/_meta/absorption-rounds/index.md docs/wiki-bi/_meta/absorption-rounds/round-08-annuity-income-slice-admission.md docs/wiki-bi/index.md docs/wiki-bi/log.md
git commit -m "docs(wiki-bi): admit annuity income follow-on round"
```

### Task 2: Split The `annuity_income` Evidence Gaps The Wiki Already Names

**Files:**
- Create: `docs/wiki-bi/evidence/annuity-income-branch-mapping-evidence.md`
- Create: `docs/wiki-bi/evidence/annuity-income-id5-retirement-evidence.md`
- Create: `docs/wiki-bi/evidence/annuity-income-operator-artifacts-evidence.md`
- Modify: `docs/wiki-bi/evidence/annuity-income-gap-evidence.md`
- Modify: `docs/wiki-bi/evidence/identity-and-lookup-evidence.md`
- Modify: `docs/wiki-bi/evidence/operator-and-surface-evidence.md`
- Modify: `docs/wiki-bi/evidence/verification-assets-evidence.md`
- Modify: `docs/wiki-bi/domains/annuity-income.md`
- Modify: `docs/wiki-bi/standards/verification-method/golden-scenarios.md`
- Modify: `docs/wiki-bi/surfaces/unknown-names-csv.md`
- Modify: `docs/wiki-bi/surfaces/failed-record-export.md`

- [ ] **Step 1: Create the branch-mapping evidence page**

Create `docs/wiki-bi/evidence/annuity-income-branch-mapping-evidence.md` with this starting content:

```md
# `annuity_income` branch mapping evidence

## Conclusion Theme

This page tracks the `COMPANY_BRANCH_MAPPING` override memory that still affects `annuity_income` semantics and validation scope.

## Evidence Records

| evidence_id | source_type | evidence_strength | coverage_state | supported_pages | last_verified | notes |
|---|---|---|---|---|---|---|
| E-AI-BM-001 | legacy_doc | strong | open_question | `annuity-income`, `company-id`, `plan-type` | 2026-04-14 | `E:\Projects\WorkDataHub\docs\cleansing-rules\annuity-income.md` records 6 manual overrides that are not yet explicitly absorbed in the rebuild. |
| E-AI-BM-002 | audit | supporting | absorbed | `annuity-income`, `identity-and-lookup-evidence` | 2026-04-14 | `docs/superpowers/audits/2026-04-12-verification-assets-search-findings.md` keeps the branch-mapping gap visible as a first-wave risk. |

## Stable Findings

- branch mapping is not a minor cleanup note; it changes how `annuity_income` identity is interpreted
- the missing override memory belongs in a durable page, not only in a catch-all gap summary

## Current Evidence Gap

- current rebuild ownership for these overrides is still not written down in a slice plan or config target
```

- [ ] **Step 2: Create the ID5 retirement evidence page**

Create `docs/wiki-bi/evidence/annuity-income-id5-retirement-evidence.md` with this starting content:

```md
# `annuity_income` ID5 retirement evidence

## Conclusion Theme

This page tracks the explicit retirement of ID5 fallback for `annuity_income`.

## Evidence Records

| evidence_id | source_type | evidence_strength | coverage_state | supported_pages | last_verified | notes |
|---|---|---|---|---|---|---|
| E-AI-ID5-001 | legacy_doc | strong | absorbed | `annuity-income`, `company-id`, `temp-id` | 2026-04-14 | `E:\Projects\WorkDataHub\docs\cleansing-rules\annuity-income.md` says the old ID5 fallback was dropped and should not be reintroduced accidentally. |
| E-AI-ID5-002 | legacy_doc | supporting | absorbed | `golden-scenarios`, `real-data-validation` | 2026-04-14 | `E:\Projects\WorkDataHub\docs\guides\validation\legacy-parity-validation.md` preserves validation memory around the post-ID5 path. |

## Stable Findings

- ID5 retirement is a governed historical decision, not an implementation detail
- future `annuity_income` work must prove it preserves the post-retirement behavior instead of reviving a forbidden fallback path

## Current Evidence Gap

- current rebuild tests do not yet protect this retirement explicitly
```

- [ ] **Step 3: Create the operator-artifacts evidence page**

Create `docs/wiki-bi/evidence/annuity-income-operator-artifacts-evidence.md` with this starting content:

```md
# `annuity_income` operator artifacts evidence

## Conclusion Theme

This page tracks the operator-facing artifacts that legacy `annuity_income` produced, especially unresolved-name and failed-record outputs.

## Evidence Records

| evidence_id | source_type | evidence_strength | coverage_state | supported_pages | last_verified | notes |
|---|---|---|---|---|---|---|
| E-AI-OA-001 | audit | strong | absorbed | `annuity-income`, `unknown-names-csv`, `failed-record-export` | 2026-04-14 | `docs/superpowers/audits/2026-04-12-legacy-code-audit.md` identifies `unknown_names_csv` and failed-record outputs as real operator-facing artifacts. |
| E-AI-OA-002 | audit | strong | absorbed | `annuity-income`, `operator-and-surface-evidence` | 2026-04-14 | `docs/superpowers/audits/2026-04-12-verification-assets-search-findings.md` keeps artifact parity visible as a first-wave gap, not a debug-only concern. |

## Stable Findings

- `annuity_income` has operator-facing artifact obligations in addition to fact-processing obligations
- unresolved-name and failed-record visibility must be decided explicitly during slice planning

## Current Evidence Gap

- the rebuild has no explicit artifact contract, runbook path, or validation evidence for these outputs yet
```

- [ ] **Step 4: Repoint the aggregate evidence pages**

Apply these content changes:

```md
In `docs/wiki-bi/evidence/annuity-income-gap-evidence.md`, replace the broad gap bullets with direct links to:
- `annuity-income-branch-mapping-evidence.md`
- `annuity-income-id5-retirement-evidence.md`
- `annuity-income-operator-artifacts-evidence.md`

In `docs/wiki-bi/evidence/identity-and-lookup-evidence.md`, add the new branch-mapping and ID5 pages to the related evidence discussion.

In `docs/wiki-bi/evidence/operator-and-surface-evidence.md`, add the new operator-artifacts page as the primary `annuity_income` artifact pointer.

In `docs/wiki-bi/evidence/verification-assets-evidence.md`, note that the `annuity_income` validation-memory section now links out to the ID5 and artifact detail pages instead of carrying all detail inline.
```

- [ ] **Step 5: Update the domain, standards, and surface pages**

Make these link additions:

```md
Add to `docs/wiki-bi/domains/annuity-income.md`:
- `annuity-income-branch-mapping-evidence.md`
- `annuity-income-id5-retirement-evidence.md`
- `annuity-income-operator-artifacts-evidence.md`

Add to `docs/wiki-bi/standards/verification-method/golden-scenarios.md`:
- a note that `annuity_income` slice admission must protect post-ID5 identity scenarios and artifact visibility scenarios

Add to `docs/wiki-bi/surfaces/unknown-names-csv.md` and `docs/wiki-bi/surfaces/failed-record-export.md`:
- a link to `annuity-income-operator-artifacts-evidence.md` under key evidence
```

- [ ] **Step 6: Commit the evidence split**

Run:

```powershell
git add docs/wiki-bi/evidence/annuity-income-branch-mapping-evidence.md docs/wiki-bi/evidence/annuity-income-id5-retirement-evidence.md docs/wiki-bi/evidence/annuity-income-operator-artifacts-evidence.md docs/wiki-bi/evidence/annuity-income-gap-evidence.md docs/wiki-bi/evidence/identity-and-lookup-evidence.md docs/wiki-bi/evidence/operator-and-surface-evidence.md docs/wiki-bi/evidence/verification-assets-evidence.md docs/wiki-bi/domains/annuity-income.md docs/wiki-bi/standards/verification-method/golden-scenarios.md docs/wiki-bi/surfaces/unknown-names-csv.md docs/wiki-bi/surfaces/failed-record-export.md
git commit -m "docs(wiki-bi): split annuity income evidence gaps"
```

### Task 3: Write The Dedicated `annuity_income` Slice Plan And Governance Linkage

**Files:**
- Create: `docs/superpowers/plans/2026-04-14-workdatahubpro-annuity-income-validation-slice.md`
- Modify: `docs/superpowers/specs/2026-04-11-workdatahubpro-first-wave-legacy-coverage-matrix.md`

- [ ] **Step 1: Create the dedicated slice-plan header**

Create `docs/superpowers/plans/2026-04-14-workdatahubpro-annuity-income-validation-slice.md` with this opening block:

```md
# WorkDataHubPro Annuity Income Validation Slice Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Close the remaining first-wave domain gap by implementing and validating the `annuity_income` slice without silently reviving retired identity behavior or dropping operator-facing artifacts.

**Architecture:** Reuse the accepted single-sheet and publication runtime already proven by `annuity_performance`. Keep `annuity_income`-specific cleansing, branch-mapping memory, ID5 retirement protection, and operator-artifact behavior explicit inside the slice instead of hiding them in generic helpers or deferred Phase E operator decisions.

**Tech Stack:** Python, pytest, Markdown runbooks, replay assets, governed config, explicit publication runtime
```

- [ ] **Step 2: Map the coverage rows into the slice-plan scope**

Include this scope table near the top of the plan:

```md
| Matrix Row | Scope In Slice |
|---|---|
| AI-001 | single-sheet workbook intake and row anchoring |
| AI-002 | canonical cleansing and fact processing |
| AI-003 | identity, derivation, and explicit publication path |
| AI-004 | unresolved-name and failed-record operator artifacts |
| AI-005 | service-delegation execution path with explicit no-hook guard |
| CT-016 | shared operator artifact parity handled to the degree needed for `annuity_income` slice acceptance |
```

- [ ] **Step 3: Lock the file targets and test targets**

Use these exact target paths in the slice plan:

```md
Source targets:
- `src/work_data_hub_pro/capabilities/source_intake/annuity_income/`
- `src/work_data_hub_pro/capabilities/fact_processing/annuity_income/`
- `src/work_data_hub_pro/capabilities/reference_derivation/`
- `src/work_data_hub_pro/apps/etl_cli/`
- `config/domains/annuity_income/`

Test targets:
- `tests/integration/test_annuity_income_intake.py`
- `tests/integration/test_annuity_income_processing.py`
- `tests/integration/test_annuity_income_operator_artifacts.py`
- `tests/replay/test_annuity_income_slice.py`
- `tests/replay/test_annuity_income_explainability_slo.py`
```

- [ ] **Step 4: Update the coverage matrix to point to the new plan**

Update AI-001 through AI-005 so:

```md
- `Owning Spec / Plan` becomes `2026-04-14-workdatahubpro-annuity-income-validation-slice.md`
- `Status` becomes `planned`
```

Keep CT-011 through CT-015 deferred. Do not pull Phase E surface decisions into the `annuity_income` slice plan unless a raw source proves they are a hard admission dependency.

- [ ] **Step 5: Commit the slice admission**

Run:

```powershell
git add docs/superpowers/plans/2026-04-14-workdatahubpro-annuity-income-validation-slice.md docs/superpowers/specs/2026-04-11-workdatahubpro-first-wave-legacy-coverage-matrix.md
git commit -m "plan(annuity-income): admit validation slice"
```

### Task 4: Verify The Documentation Network Before Execution Starts

**Files:**
- Verify: `docs/wiki-bi/`
- Verify: `docs/superpowers/plans/2026-04-14-workdatahubpro-annuity-income-validation-slice.md`
- Verify: `docs/superpowers/specs/2026-04-11-workdatahubpro-first-wave-legacy-coverage-matrix.md`

- [ ] **Step 1: Verify the new wiki pages are reachable from the catalog**

Run:

```powershell
rg -n "Round 08|annuity-income-branch-mapping-evidence|annuity-income-id5-retirement-evidence|annuity-income-operator-artifacts-evidence" docs/wiki-bi
```

Expected: matches in the new evidence pages, `docs/wiki-bi/index.md`, `docs/wiki-bi/log.md`, `docs/wiki-bi/_meta/wiki-absorption-roadmap.md`, and `docs/wiki-bi/_meta/absorption-rounds/round-08-annuity-income-slice-admission.md`.

- [ ] **Step 2: Verify the slice plan covers every pending `annuity_income` row**

Run:

```powershell
rg -n "AI-001|AI-002|AI-003|AI-004|AI-005|CT-016" docs/superpowers/specs/2026-04-11-workdatahubpro-first-wave-legacy-coverage-matrix.md docs/superpowers/plans/2026-04-14-workdatahubpro-annuity-income-validation-slice.md
```

Expected: every pending `annuity_income` row appears in the coverage matrix and is mapped in the new slice plan.

- [ ] **Step 3: Verify the worktree only contains intended documentation changes**

Run:

```powershell
git status -sb
```

Expected: only the intended `docs/wiki-bi/`, `docs/superpowers/plans/`, and coverage-matrix edits remain staged or modified.

- [ ] **Step 4: Stop if the raw sources still leave branch mapping or artifact behavior as open questions**

If the raw sources do not support stable findings for branch mapping ownership or operator artifact obligations, stop after the wiki updates and leave the slice plan unadmitted. Record the blockers in:

```md
- `docs/wiki-bi/evidence/annuity-income-branch-mapping-evidence.md`
- `docs/wiki-bi/evidence/annuity-income-operator-artifacts-evidence.md`
- `docs/wiki-bi/_meta/absorption-rounds/round-08-annuity-income-slice-admission.md`
```

Only continue into code execution once the slice plan and coverage-matrix linkage are explicit and the wiki no longer treats the core `annuity_income` gaps as unnamed institutional memory.

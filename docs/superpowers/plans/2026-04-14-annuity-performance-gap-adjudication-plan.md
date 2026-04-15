# Annuity Performance Gap Adjudication Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Resolve the remaining confirmed annuity-performance wiki-vs-code gaps by separating them into wiki-only corrections, code-fix candidates, and intentional differences that must be explicitly documented instead of silently tolerated.

**Architecture:** Treat the current `docs/wiki-bi/evidence/annuity-performance-implementation-gap-evidence.md` page as the authoritative gap register. Use it to drive three sharply separated workstreams: durable wiki corrections, legacy-code bug candidates, and contract-drift adjudications. Do not blur documentation cleanup with runtime bug fixing; each gap should exit the queue with an explicit disposition.

**Tech Stack:** Markdown in `docs/wiki-bi/` and `docs/superpowers/plans/`, legacy source under `E:\Projects\WorkDataHub`, optional later code changes under `E:\Projects\WorkDataHub`

---

## Scope Check

This plan covers:

- adjudicating the remaining active annuity-performance gap items
- deciding which gaps are:
  - wiki-only fixes
  - code-fix candidates
  - intentional differences / accepted drift
- recording those decisions durably
- optionally preparing code-fix work as follow-on plans

This plan does not cover:

- immediately editing legacy runtime code
- changing WorkDataHubPro runtime behavior
- re-opening already adjudicated non-gaps (`GAP-AP-001`, `GAP-AP-006`)
- broad multi-domain cleanup outside annuity-performance

## Current Gap Register

Active items after follow-up adjudication:

- `GAP-AP-002` — wiki too narrow on missing `客户名称`
- `GAP-AP-003` — active runtime path vs schema-level contract drift
- `GAP-AP-004` — high-probability code issue in `fk_organization`
- `GAP-AP-005` — high-probability code issue in `集团企业客户号` → `年金账户号`
- `GAP-AP-007` — YAML priority drift between resolver docs/facade/core and active YAML strategy

Inactive / resolved non-gaps:

- `GAP-AP-001`
- `GAP-AP-006`

## Adjudication Targets

### Group A: Wiki-Only Correction

#### `GAP-AP-002`

Current decision direction:

- keep as wiki correction
- no code change required for now

Desired end state:

- input contract page clearly states that missing `客户名称` is a degraded input condition
- no remaining language implies it is always an invalid source when `计划代码` still enables resolution

### Group B: Code-Fix Candidates

#### `GAP-AP-004`

Current hypothesis:

- `foreign_keys.yml` for `fk_organization` likely references `机构` after `MappingStep` has already renamed it to `机构名称`

Required adjudication question:

- does backfill operate on canonical post-mapping rows in all active annuity-performance paths?

If yes:

- this is a code/config bug candidate

If no:

- downgrade to documentation clarification

#### `GAP-AP-005`

Current hypothesis:

- `.astype(str).replace("nan", None).str.lstrip("C")` may materialize real Python `None` as `"None"` and copy it into `年金账户号`

Required adjudication question:

- can this value actually reach persisted outputs or downstream logic as the literal string `"None"`?

If yes:

- this is a code bug candidate

If no:

- downgrade to implementation note

### Group C: Intentional Difference Or Contract Drift

#### `GAP-AP-003`

Current hypothesis:

- the domain has a stricter schema-level gold contract that the active service path does not enforce

Required adjudication question:

- is this an intentional layering choice
  - schema contract exists for validation workflows only
  - helper conversion exists for permissive runtime continuation

or:

- an accidental drift that should be closed by invoking `validate_gold_dataframe()` in the active path

#### `GAP-AP-007`

Current hypothesis:

- resolver-facing docs and some code comments still describe a 5-level YAML priority order
- active YAML strategy now executes only 3 levels

Required adjudication question:

- should the old 5-level description be removed everywhere as stale documentation drift
- or are some unused codepaths still semantically depending on the 5-level model

## Proposed File Structure

### Files To Modify

- `docs/wiki-bi/evidence/annuity-performance-implementation-gap-evidence.md`
- `docs/wiki-bi/_meta/absorption-rounds/round-16-annuity-performance-gap-audit.md`
- `docs/wiki-bi/log.md`

### Optional Follow-On Plan Files

- `docs/superpowers/plans/2026-04-14-annuity-performance-code-gap-fixes.md`
- `docs/superpowers/plans/2026-04-14-annuity-performance-contract-drift-adjudication.md`

## Implementation Tasks

### Task 1: Close The Wiki-Only Gap

**Files:**
- Modify: `docs/wiki-bi/standards/input-reality/annuity-performance-input-contract.md`
- Modify: `docs/wiki-bi/evidence/annuity-performance-implementation-gap-evidence.md`
- Modify: `docs/wiki-bi/log.md`

- [ ] **Step 1: Re-check `GAP-AP-002` against current wiki wording**

Confirm the input contract no longer says missing `客户名称` always invalidates the source.

- [ ] **Step 2: Mark `GAP-AP-002` as fully resolved if wording is sufficient**

If the current wording is already correct, update the gap page status from active gap to resolved wiki correction.

- [ ] **Step 3: Append adjudication note to the log**

Record that the annuity-performance input contract now treats missing `客户名称` as degraded input rather than an automatic invalid-source condition.

### Task 2: Adjudicate `GAP-AP-004`

**Files:**
- Modify: `docs/wiki-bi/evidence/annuity-performance-implementation-gap-evidence.md`
- Optional create: `docs/superpowers/plans/2026-04-14-annuity-performance-code-gap-fixes.md`

- [ ] **Step 1: Verify the exact data shape passed into backfill**

Inspect the active annuity-performance path and confirm whether backfill consumes post-mapping canonical rows.

- [ ] **Step 2: Record the disposition**

Possible dispositions:

- `confirmed_code_bug_candidate`
- `downgraded_to_doc_clarification`
- `needs_more_runtime_evidence`

- [ ] **Step 3: If confirmed, open a code-fix plan**

Create a follow-on plan file that states the exact config/code change required for `fk_organization`.

### Task 3: Adjudicate `GAP-AP-005`

**Files:**
- Modify: `docs/wiki-bi/evidence/annuity-performance-implementation-gap-evidence.md`
- Optional create: `docs/superpowers/plans/2026-04-14-annuity-performance-code-gap-fixes.md`

- [ ] **Step 1: Trace `集团企业客户号` null handling through to `年金账户号`**

Verify whether the literal string `"None"` can survive into modeled rows, backfill, or persisted outputs.

- [ ] **Step 2: Record the disposition**

Possible dispositions:

- `confirmed_code_bug_candidate`
- `harmless_internal_artifact`
- `needs_more_runtime_evidence`

- [ ] **Step 3: If confirmed, append the exact code-fix requirement**

Document the minimal safe fix path in the follow-on code-fix plan.

### Task 4: Adjudicate `GAP-AP-003` And `GAP-AP-007`

**Files:**
- Modify: `docs/wiki-bi/evidence/annuity-performance-implementation-gap-evidence.md`
- Optional create: `docs/superpowers/plans/2026-04-14-annuity-performance-contract-drift-adjudication.md`

- [ ] **Step 1: Decide whether `GAP-AP-003` is intentional contract layering or accidental drift**

Use current service entrypoints and validation usage sites to classify it.

- [ ] **Step 2: Decide whether `GAP-AP-007` is stale documentation drift or semantically active**

Compare:

- `config.mapping_loader`
- resolver facade docs/comments
- resolver core docs/comments
- active `yaml_strategy`

- [ ] **Step 3: Record both outcomes**

For each gap, mark one of:

- `intentional_difference`
- `stale_documentation_drift`
- `code_fix_candidate`
- `needs_more_evidence`

### Task 5: Produce The Post-Adjudication Snapshot

**Files:**
- Modify: `docs/wiki-bi/evidence/annuity-performance-implementation-gap-evidence.md`
- Modify: `docs/wiki-bi/_meta/absorption-rounds/round-16-annuity-performance-gap-audit.md`
- Modify: `docs/wiki-bi/log.md`

- [ ] **Step 1: Add a status section to the gap page**

Group all gap items into:

- resolved wiki corrections
- confirmed code-fix candidates
- intentional differences
- still-open investigations

- [ ] **Step 2: Update Round 16 summary**

Reflect the adjudication outcomes instead of leaving Round 16 as an open-ended gap listing.

- [ ] **Step 3: Append the final log note**

Record the post-audit adjudication state for annuity-performance.

## Validation

For docs work:

- confirm `docs/wiki-bi` still has no broken links
- confirm every active gap has an explicit disposition
- confirm resolved non-gaps are not still presented as open defects

Suggested command:

```powershell
git diff -- docs/wiki-bi docs/superpowers/plans
```

## Expected Outcome

After this plan is executed:

- annuity-performance will have a clean, adjudicated gap register
- only true code-fix candidates will remain open
- wiki-only fixes and intentional differences will no longer be mixed together
- any required code follow-up will already have its own next-step plan

## Execution Handoff

Plan complete and saved to `docs/superpowers/plans/2026-04-14-annuity-performance-gap-adjudication-plan.md`.

Two execution options:

1. Subagent-Driven (recommended) - I dispatch a fresh subagent per task, review between tasks, fast iteration
2. Inline Execution - Execute the adjudication tasks in this session

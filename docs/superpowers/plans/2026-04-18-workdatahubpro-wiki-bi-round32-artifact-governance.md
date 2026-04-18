# WorkDataHubPro Wiki BI Round 32 Shared Unresolved Artifact Governance Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Tighten `docs/wiki-bi/` around shared unresolved-name and failed-record artifacts so the wiki can directly explain how deferred queue runtime is replaced by operator-visible artifacts, while still keeping cross-domain parity gaps explicit.

**Architecture:** Keep the next round evidence-first. Create one cross-domain evidence dispatcher for `unknown_names_csv` plus failed-record export, keep `annuity_income` artifact evidence as the slice-specific accepted replacement anchor, reconnect the relevant surface and identity-governance pages to that shared page, then write back round sediment and a small docs contract so the new dispatcher cannot become orphaned.

**Tech Stack:** Markdown in `docs/wiki-bi/` and `docs/superpowers/plans/`, small pytest docs contract in `tests/contracts/`, legacy evidence from `E:\Projects\WorkDataHub`, PowerShell, `rg`, git worktrees, `uv`, `pytest`

---

## Scope Check

This plan covers:

- one new shared evidence page for unresolved-name and failed-record artifacts
- tightening `operator-and-surface-evidence.md` and `identity-and-lookup-evidence.md` so shared operator-visible consequences stop living only as gap text
- tightening `company-lookup-queue.md`, `unknown-names-csv.md`, and `failed-record-export.md` so they point to the same shared artifact story
- reconnecting the new shared evidence page from `company-id`, `identity-governance`, and at least one high-traffic domain / contract page
- updating `index.md`, `log.md`, `wiki-absorption-roadmap.md`, and `absorption-rounds/index.md`
- adding one narrow docs contract test to protect the new shared page from becoming unreachable

This plan does not cover:

- queue persistence, retry orchestration, or operator runtime re-admission
- `reference_sync` current-side runtime closure
- `customer-mdm` manual command retain / replace decisions
- `其他年金计划`, `其他开拓机构`, or `组合代码` promotion
- semantic-map registry mutation or wave closeout

## Suggested Branch

- `docs/wiki-round-32`

## Baseline Note

The isolated worktree already exists at `E:\Projects\WorkDataHubPro\.worktrees\docs-wiki-round-32` on branch `docs/wiki-round-32`.

Baseline environment check:

- `uv sync --dev` completed successfully in the worktree.
- `uv run pytest -v` currently has **4 pre-existing failures** unrelated to this docs scope:
  - `tests/contracts/test_annual_loss_governance_addendum_docs.py::test_annual_loss_acceptance_syncs_risk_register_without_retiring_open_runtime_gaps`
  - `tests/contracts/test_annuity_income_governance_docs.py::test_annuity_income_governance_docs_mark_slice_as_accepted`
  - `tests/contracts/test_legacy_semantic_map_first_wave_pilot.py::test_first_wave_pilot_repo_state_is_populated_and_real_evidence_backed`
  - `tests/integration/test_legacy_semantic_map_first_wave_pilot_flow.py::test_run_first_wave_pilot_rebuilds_active_successor_wave_deterministically`
- The first two fail because `docs/superpowers/reviews/2026-04-11-legacy-risk-analysis-for-rebuild.md` is missing from the checked-in tree.
- The latter two fail because the checked-in successor wave now compiles `13` claims while those tests still expect `7`.

This round must not claim those failures were introduced by the docs changes.

## Files To Create

- `docs/wiki-bi/evidence/unresolved-name-and-failed-record-evidence.md`
- `docs/wiki-bi/_meta/absorption-rounds/round-32-shared-unresolved-artifact-governance.md`
- `tests/contracts/test_shared_operator_artifact_wiki_docs.py`

## Files To Modify

- `docs/wiki-bi/evidence/operator-and-surface-evidence.md`
- `docs/wiki-bi/evidence/identity-and-lookup-evidence.md`
- `docs/wiki-bi/evidence/annuity-income-operator-artifacts-evidence.md`
- `docs/wiki-bi/surfaces/company-lookup-queue.md`
- `docs/wiki-bi/surfaces/unknown-names-csv.md`
- `docs/wiki-bi/surfaces/failed-record-export.md`
- `docs/wiki-bi/standards/semantic-correctness/identity-governance.md`
- `docs/wiki-bi/concepts/company-id.md`
- `docs/wiki-bi/domains/annuity-income.md`
- `docs/wiki-bi/domains/annuity-performance.md`
- `docs/wiki-bi/standards/output-correctness/annuity-income-output-contract.md`
- `docs/wiki-bi/index.md`
- `docs/wiki-bi/log.md`
- `docs/wiki-bi/_meta/absorption-rounds/index.md`
- `docs/wiki-bi/_meta/wiki-absorption-roadmap.md`

### Task 1: Create The Shared Unresolved Artifact Evidence Dispatcher

**Files:**
- Create: `docs/wiki-bi/evidence/unresolved-name-and-failed-record-evidence.md`
- Modify: `docs/wiki-bi/evidence/operator-and-surface-evidence.md`
- Modify: `docs/wiki-bi/evidence/identity-and-lookup-evidence.md`
- Modify: `docs/wiki-bi/evidence/annuity-income-operator-artifacts-evidence.md`

- [x] **Step 1: Create the new shared evidence page**

Write `docs/wiki-bi/evidence/unresolved-name-and-failed-record-evidence.md`.

The page must aggregate:

- legacy `annuity_income` unknown-name and failed-record artifacts
- legacy `annuity_performance` unknown-name and failed-record artifacts
- legacy `annual_award` / `annual_loss` failed-record export breadth
- current accepted replacement evidence from `annuity_income` tests, replay assets, and runbook

The page must explicitly distinguish:

- stable historical breadth
- current accepted replacement evidence
- still-open cross-domain parity gaps

Primary sources to keep explicit:

- `E:\Projects\WorkDataHub\docs\domains\annuity_income-capability-map.md`
- `E:\Projects\WorkDataHub\docs\cleansing-rules\annuity-income.md`
- `E:\Projects\WorkDataHub\src\work_data_hub\domain\annuity_performance\service.py`
- `E:\Projects\WorkDataHub\src\work_data_hub\domain\annual_award\service.py`
- `E:\Projects\WorkDataHub\src\work_data_hub\domain\annual_loss\service.py`
- `tests/integration/test_annuity_income_operator_artifacts.py`
- `tests/contracts/test_annuity_income_replay_assets.py`
- `tests/replay/test_annuity_income_slice.py`
- `docs/runbooks/annuity-income-replay.md`

- [x] **Step 2: Tighten the two aggregate evidence pages**

Update:

- `docs/wiki-bi/evidence/operator-and-surface-evidence.md`
- `docs/wiki-bi/evidence/identity-and-lookup-evidence.md`

The intended result is:

- `operator-and-surface-evidence.md` stops leaving shared artifact parity only as a gap line and instead dispatches to the new object-level evidence page
- `identity-and-lookup-evidence.md` makes unresolved identity visibility read as a governed consequence, not just a side note under queue/artifact mentions

- [x] **Step 3: Reposition the income-specific artifact page**

Update `docs/wiki-bi/evidence/annuity-income-operator-artifacts-evidence.md` so it remains the accepted slice-specific object page, but now points upward to the new shared dispatcher instead of reading like the only evidence anchor for the whole artifact family.

### Task 2: Tighten The Surface And Identity Pages Around Operator-Visible Consequence

**Files:**
- Modify: `docs/wiki-bi/surfaces/company-lookup-queue.md`
- Modify: `docs/wiki-bi/surfaces/unknown-names-csv.md`
- Modify: `docs/wiki-bi/surfaces/failed-record-export.md`
- Modify: `docs/wiki-bi/standards/semantic-correctness/identity-governance.md`
- Modify: `docs/wiki-bi/concepts/company-id.md`

- [x] **Step 1: Tighten the three surface pages**

Update:

- `docs/wiki-bi/surfaces/company-lookup-queue.md`
- `docs/wiki-bi/surfaces/unknown-names-csv.md`
- `docs/wiki-bi/surfaces/failed-record-export.md`

The intended result is:

- queue deferred no longer reads like “artifact handling exists somewhere else”; it points to an explicit shared evidence page
- `unknown_names_csv` is described as legacy dual-domain breadth plus current income-only accepted replacement
- failed-record export is described as legacy broader-than-income behavior plus current parity gap, not as either fully accepted or purely hypothetical

- [x] **Step 2: Reconnect identity-governance and company-id**

Update:

- `docs/wiki-bi/standards/semantic-correctness/identity-governance.md`
- `docs/wiki-bi/concepts/company-id.md`

The intended result is:

- unresolved identity visibility points to one shared artifact evidence anchor
- `company_id` and identity governance continue to state that operator-visible consequence is required, but now with a more precise evidence route

### Task 3: Reconnect High-Traffic Domain And Contract Entry Points

**Files:**
- Modify: `docs/wiki-bi/domains/annuity-income.md`
- Modify: `docs/wiki-bi/domains/annuity-performance.md`
- Modify: `docs/wiki-bi/standards/output-correctness/annuity-income-output-contract.md`

- [x] **Step 1: Tighten the domain entry points**

Update:

- `docs/wiki-bi/domains/annuity-income.md`
- `docs/wiki-bi/domains/annuity-performance.md`

The intended result is:

- `annuity_income` points readers from its accepted artifact contract to the new shared evidence page
- `annuity_performance` becomes a discoverable route into the legacy shared artifact breadth and current parity gap, without falsely claiming current accepted artifact closure

- [x] **Step 2: Tighten the accepted output-contract route**

Update `docs/wiki-bi/standards/output-correctness/annuity-income-output-contract.md` so its “artifact visibility” statements route to the new shared evidence page while still keeping the accepted slice-specific evidence explicit.

### Task 4: Add Navigation, Sediment, And A Minimal Docs Contract

**Files:**
- Create: `docs/wiki-bi/_meta/absorption-rounds/round-32-shared-unresolved-artifact-governance.md`
- Create: `tests/contracts/test_shared_operator_artifact_wiki_docs.py`
- Modify: `docs/wiki-bi/index.md`
- Modify: `docs/wiki-bi/log.md`
- Modify: `docs/wiki-bi/_meta/absorption-rounds/index.md`
- Modify: `docs/wiki-bi/_meta/wiki-absorption-roadmap.md`

- [x] **Step 1: Update the main index**

In `docs/wiki-bi/index.md`:

- add a discoverable FAQ / maintainer route for the shared unresolved-name and failed-record artifact story
- register the new shared evidence page in the evidence catalog
- keep the current index structure intact

- [x] **Step 2: Create the Round 32 sediment note**

Write `docs/wiki-bi/_meta/absorption-rounds/round-32-shared-unresolved-artifact-governance.md` documenting:

- why this round moved to semantic-map-first adjacent runtime/operator discovery instead of promoting more business-semantic objects
- why the new page is an evidence dispatcher, not a closure claim
- which artifact contracts are currently accepted and which remain open

- [x] **Step 3: Add a narrow docs contract**

Create `tests/contracts/test_shared_operator_artifact_wiki_docs.py`.

The test should only assert stable, high-signal conditions:

- the new shared evidence page exists and mentions both `unknown_names_csv` and failed-record export
- key surface pages route to it
- the main index exposes it

Do not make the test brittle by asserting entire paragraphs verbatim.

- [x] **Step 4: Update roadmap/index metadata and append the log**

Update:

- `docs/wiki-bi/_meta/absorption-rounds/index.md`
- `docs/wiki-bi/_meta/wiki-absorption-roadmap.md`
- `docs/wiki-bi/log.md`

The updates must show:

- Round 32 completed
- shared unresolved-name / failed-record artifact governance now has a durable evidence dispatcher
- current accepted artifact closure remains income-specific
- broader cross-domain artifact parity still remains follow-on work

## Validation Steps

- [x] Run reachability and keyword checks:
  - `rg -n "unknown_names_csv|failed-record|failed_records|unresolved-name|artifact parity|temp_id_fallback" docs/wiki-bi tests/contracts`
- [x] Review only the intended docs/test diff:
  - `git diff -- docs/wiki-bi docs/superpowers/plans tests/contracts`
- [x] Run formatting/sanity check:
  - `git diff --check`
- [x] Run the new narrow docs contract:
  - `uv run pytest tests/contracts/test_shared_operator_artifact_wiki_docs.py -v`
- [x] Re-run the relevant existing docs/runtime anchors:
  - `uv run pytest tests/contracts/test_annuity_income_wiki_guidance_docs.py tests/contracts/test_annuity_income_replay_assets.py tests/integration/test_annuity_income_operator_artifacts.py -v`
- [x] Re-run the full suite after the docs round completes:
  - `uv run pytest -v`
  - Expected: the same 4 pre-existing failures remain; no new failures introduced by Round 32

## Completion Criteria

This round is complete when:

- `unknown_names_csv` and failed-record export no longer rely only on scattered slice-specific or gap-only references
- queue deferred vs artifact replacement is easier to answer from one shared evidence route
- the wiki can explicitly say “income is current accepted artifact closure; cross-domain parity is not yet closed”
- high-traffic identity / surface / domain pages route to the new shared evidence page
- Round 32 navigation and sediment are written back in `index.md`, `log.md`, and `_meta/absorption-rounds/`
- the new docs contract passes
- validation shows no new failures beyond the known pre-existing baseline failures

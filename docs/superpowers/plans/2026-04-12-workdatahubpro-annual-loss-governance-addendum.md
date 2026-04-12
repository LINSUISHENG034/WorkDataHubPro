# Annual Loss Governance Addendum Implementation Plan

**Date:** 2026-04-12
**Status:** Done
**Target Repository:** `E:\Projects\WorkDataHubPro`

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the minimum governance-only follow-on work that the active `annual_loss` slice needs so acceptance updates remain consistent across the coverage matrix, refactor program, and canonical risk register without editing the original implementation plan.

**Architecture:** Treat this as a narrow docs-and-contract addendum to `docs/superpowers/plans/2026-04-12-workdatahubpro-annual-loss-validation-slice.md`. Keep the accepted-slice story focused on `AL-001` through `AL-004`, `XD-002`, and `XD-005`, while preserving the newly registered Phase E runtime/operator surfaces (`CT-011` through `CT-016`) as still-open follow-on work. Use one additive contract test file so governance drift is caught without rewriting the original plan's Task 8.

**Tech Stack:** Python 3.12+, `uv`, `pytest`, Markdown, standard-library `pathlib`

---

## Scope Check

This plan covers:

- one additive governance-doc regression test file for the `annual_loss` acceptance addendum
- coverage-matrix wording updates required when `annual_loss` moves from `planned` to `accepted`
- refactor-program wording updates required when `annual_loss` becomes the first accepted Phase D breadth slice
- risk-register wording updates required so the canonical risk source reflects the accepted `annual_loss` slice and keeps `XD-005` explicit

This plan does not cover:

- any implementation work from Tasks 1 through 7 of the original `annual_loss` slice plan
- any modification to `docs/superpowers/plans/2026-04-12-workdatahubpro-annual-loss-validation-slice.md`
- closing `CT-011` through `CT-016`
- Phase E production-runtime/operator design
- the `annuity_income` slice

The deliberate consequence is that this addendum remains docs-only and can be executed after the original plan's runtime work is ready, without changing the accepted implementation boundary of the `annual_loss` slice itself.

## Suggested Branch

- `slice/annual-loss-closure`

## File Structure

Create or modify these files in this order so the governance addendum stays additive and independently testable:

- `tests/contracts/test_annual_loss_governance_addendum_docs.py`: additive governance assertions for `annual_loss` acceptance, `XD-005`, Phase E runtime surfaces, and risk-register synchronization
- `docs/superpowers/specs/2026-04-11-workdatahubpro-first-wave-legacy-coverage-matrix.md`: accepted `annual_loss` summary, accepted `AL-*` rows, `CT-005` note wording, and `XD-005` post-acceptance wording
- `docs/superpowers/specs/2026-04-11-workdatahubpro-refactor-program.md`: accepted Phase D breadth-slice wording while preserving the expanded Phase E backlog
- `docs/superpowers/reviews/2026-04-11-legacy-risk-analysis-for-rebuild.md`: accepted-slice current-position wording and `CR-008` narrative sync for `XD-005`

### Task 1: Add Coverage-Matrix Governance Guard For `annual_loss`

**Files:**
- Create: `tests/contracts/test_annual_loss_governance_addendum_docs.py`
- Modify: `docs/superpowers/specs/2026-04-11-workdatahubpro-first-wave-legacy-coverage-matrix.md`

- [ ] **Step 1: Write the failing test**

```python
# tests/contracts/test_annual_loss_governance_addendum_docs.py
from pathlib import Path


COVERAGE_MATRIX = Path(
    "docs/superpowers/specs/2026-04-11-workdatahubpro-first-wave-legacy-coverage-matrix.md"
)


def test_annual_loss_acceptance_updates_coverage_matrix_without_dropping_runtime_surfaces() -> None:
    coverage_matrix = COVERAGE_MATRIX.read_text(encoding="utf-8")

    assert "| `annual_loss` | accepted breadth-closure slice |" in coverage_matrix
    assert "| `annuity_income` | next recommended single-sheet breadth slice |" in coverage_matrix
    assert "| AL-001 | multi-sheet loss-domain intake contract | capability |" in coverage_matrix
    assert "| AL-004 | loss fact publication consumed by downstream status rules | projection |" in coverage_matrix
    assert "| CT-011 | `company_lookup_queue` special orchestration domain and async retry/runtime contract |" in coverage_matrix
    assert "| CT-016 | shared unresolved-name and failed-record operator artifact parity across first-wave runs |" in coverage_matrix
    assert "current accepted event-domain slices prove replay-backed and current-row lookup behavior" in coverage_matrix
    assert "| XD-005 | contract-state output (`customer.客户年金计划`) influences `annual_award` and `annual_loss` plan-code enrichment behavior |" in coverage_matrix
    assert "annual_loss acceptance now proves this dependency explicitly while it remains active for both event-domain slices" in coverage_matrix
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/contracts/test_annual_loss_governance_addendum_docs.py::test_annual_loss_acceptance_updates_coverage_matrix_without_dropping_runtime_surfaces -v`
Expected: FAIL with `AssertionError` because `annual_loss` is still `planned` and the post-acceptance `XD-005` wording is not present yet.

- [ ] **Step 3: Write minimal implementation**

````markdown
# docs/superpowers/specs/2026-04-11-workdatahubpro-first-wave-legacy-coverage-matrix.md
| `annual_loss` | accepted breadth-closure slice | `annuity_income` remains the only unclosed first-wave domain |
| `annuity_income` | next recommended single-sheet breadth slice | no accepted executable slice yet |

| AL-001 | multi-sheet loss-domain intake contract | capability | legacy migration workflow and paired event-domain references | future `capabilities/source_intake/annual_loss/` | `capabilities` | architecture blueprint + 2026-04-12 annual loss slice plan | `accepted` | `tests/integration/test_annual_loss_intake.py`, `tests/replay/test_annual_loss_slice.py` | N/A | merged anchors stay queryable by batch + anchor row |
| AL-002 | canonical loss event transformation | capability | legacy domain behavior and capability-map-equivalent references | future `capabilities/fact_processing/annual_loss/` | `capabilities` | architecture blueprint + 2026-04-12 annual loss slice plan | `accepted` | `tests/integration/test_annual_loss_processing.py`, `tests/replay/test_annual_loss_slice.py` | N/A | governed rule-pack binding and date parsing are explicit |
| AL-003 | identity / plan-code handling for loss rows | mechanism | legacy event-domain behavior | shared contracts plus domain-specific wiring | `capabilities` | 2026-04-12 annual loss slice plan | `accepted` | `tests/integration/test_identity_resolution.py`, `tests/integration/test_annual_loss_plan_code_enrichment.py`, `tests/replay/test_annual_loss_slice.py` | N/A | current-row lookup order and fallback semantics are now proven in the accepted slice |
| AL-004 | loss fact publication consumed by downstream status rules | projection | downstream snapshot dependency implied by current fixtures and blueprint | explicit publication plus projection evidence | `platform` + `capabilities` | 2026-04-12 annual loss slice plan | `accepted` | `tests/integration/test_projection_outputs.py`, `tests/replay/test_annual_loss_slice.py`, `tests/replay/test_annual_loss_explainability_slo.py` | N/A | the slice replaces fixture-only loss dependency with published fact coverage |

| CT-005 | history-aware event-domain contract lookup and temporal enrichment semantics | mechanism | `docs/domains/annual_award-capability-map.md`, `docs/domains/annual_loss-capability-map.md`, legacy contract lookup behavior | future temporal lookup contract for event-domain plan-code enrichment | `capabilities` + `reference` | merged first-wave legacy coverage risk register + future annual loss / event-domain parity follow-on plan | `pending` | future lookup contract tests, historical replay evidence, and event-domain slice validation | N/A | current accepted event-domain slices prove replay-backed and current-row lookup behavior, not a full repository-wide temporal selection contract for historical/current contract rows |

| XD-002 | `annual_loss` facts influence downstream snapshot status triggered by `annuity_performance` | event-domain closure matters for customer status correctness | active dependency | closed by the accepted `annual_loss` slice with published-fact projection coverage |
| XD-005 | contract-state output (`customer.客户年金计划`) influences `annual_award` and `annual_loss` plan-code enrichment behavior | event-domain slices are not fully independent from annuity-performance-side contract-state closure | active dependency | annual_loss acceptance now proves this dependency explicitly while it remains active for both event-domain slices |
````

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/contracts/test_annual_loss_governance_addendum_docs.py::test_annual_loss_acceptance_updates_coverage_matrix_without_dropping_runtime_surfaces -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add tests/contracts/test_annual_loss_governance_addendum_docs.py docs/superpowers/specs/2026-04-11-workdatahubpro-first-wave-legacy-coverage-matrix.md
@'
docs(docs.governance): add annual_loss coverage-matrix addendum

Record `annual_loss` as an accepted breadth-closure slice without dropping the
newly registered runtime/operator surfaces or the explicit `XD-005`
contract-state dependency.

Validation:
- uv run pytest tests/contracts/test_annual_loss_governance_addendum_docs.py::test_annual_loss_acceptance_updates_coverage_matrix_without_dropping_runtime_surfaces -v
'@ | git commit -F -
```

### Task 2: Add Refactor-Program Governance Guard For `annual_loss`

**Files:**
- Modify: `tests/contracts/test_annual_loss_governance_addendum_docs.py`
- Modify: `docs/superpowers/specs/2026-04-11-workdatahubpro-refactor-program.md`

- [ ] **Step 1: Extend the failing test file**

```python
# tests/contracts/test_annual_loss_governance_addendum_docs.py
REFACTOR_PROGRAM = Path(
    "docs/superpowers/specs/2026-04-11-workdatahubpro-refactor-program.md"
)


def test_annual_loss_acceptance_updates_refactor_program_but_keeps_phase_e_tracks() -> None:
    refactor_program = REFACTOR_PROGRAM.read_text(encoding="utf-8")

    assert "- the first Phase D breadth slice for `annual_loss`" in refactor_program
    assert "- compatibility adjudication and evidence indexing exist for the first three accepted slices" in refactor_program
    assert "- replay assets and runbooks exist for `annuity_performance`, `annual_award`, and `annual_loss`" in refactor_program
    assert "- the paired event-domain dependency path is accepted with committed coverage updates" in refactor_program
    assert "- `annuity_income` does not have an accepted executable slice yet" in refactor_program
    assert "| 3 | `annual_loss` | accepted breadth-closure slice | closes the paired event-domain dependency path before the final single-sheet breadth slice |" in refactor_program
    assert "| 4 | `annuity_income` | next recommended single-sheet breadth slice | extends first-wave coverage after event-domain breadth risk is reduced |" in refactor_program
    assert "| deferred lookup queue runtime | legacy supports queued provider processing, retries, and recovery outside the main fact run | deferred | separate queue/runtime plan |" in refactor_program
    assert "| reference bootstrap / reference-sync runtime | legacy uses an explicit `reference_sync` orchestration surface plus incremental state | deferred | separate reference bootstrap/runtime plan |" in refactor_program
    assert "| enterprise identity / EQC persistence surfaces | legacy persists cache, queue, and raw/cleansed EQC data beyond fact-domain outputs | deferred | separate identity persistence plan |" in refactor_program
    assert "| manual customer-status command surfaces and shared operator artifacts | legacy supports `customer-mdm` manual commands and cross-domain unresolved-name / failed-record artifacts | deferred | separate operator-tools / artifact-governance plan |" in refactor_program
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/contracts/test_annual_loss_governance_addendum_docs.py::test_annual_loss_acceptance_updates_refactor_program_but_keeps_phase_e_tracks -v`
Expected: FAIL with `AssertionError` because the program spec still presents `annual_loss` as the next recommended slice.

- [ ] **Step 3: Write minimal implementation**

````markdown
# docs/superpowers/specs/2026-04-11-workdatahubpro-refactor-program.md
- the first Phase D breadth slice for `annual_loss`

- compatibility adjudication and evidence indexing exist for the first three accepted slices
- replay assets and runbooks exist for `annuity_performance`, `annual_award`, and `annual_loss`
- the paired event-domain dependency path is accepted with committed coverage updates

- `annuity_income` does not have an accepted executable slice yet

| 3 | `annual_loss` | accepted breadth-closure slice | closes the paired event-domain dependency path before the final single-sheet breadth slice |
| 4 | `annuity_income` | next recommended single-sheet breadth slice | extends first-wave coverage after event-domain breadth risk is reduced |
````

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/contracts/test_annual_loss_governance_addendum_docs.py::test_annual_loss_acceptance_updates_refactor_program_but_keeps_phase_e_tracks -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add tests/contracts/test_annual_loss_governance_addendum_docs.py docs/superpowers/specs/2026-04-11-workdatahubpro-refactor-program.md
@'
docs(docs.governance): sync annual_loss acceptance with refactor program

Update the program baseline so `annual_loss` is recorded as the first accepted
Phase D breadth slice while the expanded Phase E backlog remains deferred.

Validation:
- uv run pytest tests/contracts/test_annual_loss_governance_addendum_docs.py::test_annual_loss_acceptance_updates_refactor_program_but_keeps_phase_e_tracks -v
'@ | git commit -F -
```

### Task 3: Add Risk-Register Governance Guard For `annual_loss`

**Files:**
- Modify: `tests/contracts/test_annual_loss_governance_addendum_docs.py`
- Modify: `docs/superpowers/reviews/2026-04-11-legacy-risk-analysis-for-rebuild.md`

- [ ] **Step 1: Extend the failing test file**

```python
# tests/contracts/test_annual_loss_governance_addendum_docs.py
RISK_REGISTER = Path(
    "docs/superpowers/reviews/2026-04-11-legacy-risk-analysis-for-rebuild.md"
)


def test_annual_loss_acceptance_syncs_risk_register_without_retiring_open_runtime_gaps() -> None:
    risk_register = RISK_REGISTER.read_text(encoding="utf-8")

    assert "- `annual_loss` remains an accepted breadth-closure slice." in risk_register
    assert "- `annuity_income` remains the only unclosed first-wave executable slice." in risk_register
    assert "Current accepted event-domain slices prove:" in risk_register
    assert "| `CR-008` | history-aware event-domain lookup and temporal enrichment semantics | supplemental `SFR-004` | `pending first-wave gap` | `AA-004`, `AL-003`, `CT-005`, `XD-005` |" in risk_register
    assert "| `CR-014` | deferred-lookup queue runtime, retry semantics, and special orchestration domain closure | `2026-04-12 legacy audit` | `deferred runtime/operator gap` | `CT-011`, `XD-003` |" in risk_register
    assert "| `CR-019` | shared unresolved-name and failed-record operator artifact parity across first-wave runs | `2026-04-12 legacy audit` | `pending first-wave gap` | `CT-016` |" in risk_register
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/contracts/test_annual_loss_governance_addendum_docs.py::test_annual_loss_acceptance_syncs_risk_register_without_retiring_open_runtime_gaps -v`
Expected: FAIL with `AssertionError` because the risk register still says `annual_loss` is unclosed and `CR-008` has not been reworded for the accepted slice state.

- [ ] **Step 3: Write minimal implementation**

````markdown
# docs/superpowers/reviews/2026-04-11-legacy-risk-analysis-for-rebuild.md
- `annual_loss` remains an accepted breadth-closure slice.
- `annuity_income` remains the only unclosed first-wave executable slice.

### `CR-008` History-Aware Event-Domain Lookup And Temporal Enrichment Semantics

Current accepted event-domain slices prove:
```` 

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/contracts/test_annual_loss_governance_addendum_docs.py::test_annual_loss_acceptance_syncs_risk_register_without_retiring_open_runtime_gaps -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add tests/contracts/test_annual_loss_governance_addendum_docs.py docs/superpowers/reviews/2026-04-11-legacy-risk-analysis-for-rebuild.md
@'
docs(docs.governance): sync annual_loss acceptance with risk register

Keep the canonical risk register aligned with annual_loss acceptance while
preserving the still-open runtime and operator follow-on risks.

Validation:
- uv run pytest tests/contracts/test_annual_loss_governance_addendum_docs.py::test_annual_loss_acceptance_syncs_risk_register_without_retiring_open_runtime_gaps -v
'@ | git commit -F -
```

### Task 4: Run Additive Governance Verification

**Files:**
- Verify only: `tests/contracts/test_annual_loss_governance_docs.py`
- Verify only: `tests/contracts/test_annual_loss_governance_addendum_docs.py`

- [ ] **Step 1: Run the combined governance-doc contract tests**

Run: `uv run pytest tests/contracts/test_annual_loss_governance_docs.py tests/contracts/test_annual_loss_governance_addendum_docs.py -v`
Expected: PASS

- [ ] **Step 2: Re-run the replay-facing governance checks from the original slice**

Run: `uv run pytest tests/contracts/test_annual_loss_governance_docs.py tests/contracts/test_annual_loss_governance_addendum_docs.py tests/replay/test_annual_loss_slice.py tests/replay/test_annual_loss_explainability_slo.py -v`
Expected: PASS

- [ ] **Step 3: Record the verification result in the work log or PR text**

```text
Validation:
- uv run pytest tests/contracts/test_annual_loss_governance_docs.py tests/contracts/test_annual_loss_governance_addendum_docs.py -v
- uv run pytest tests/contracts/test_annual_loss_governance_docs.py tests/contracts/test_annual_loss_governance_addendum_docs.py tests/replay/test_annual_loss_slice.py tests/replay/test_annual_loss_explainability_slo.py -v
```

This addendum does not replace the original slice plan's final full-suite gate.
Keep the original plan's final `uv run pytest -v` requirement unchanged.

## Self-Review

### Spec Coverage

- The addendum covers the only governance gaps introduced by the updated governance baseline: `XD-005`, accepted-state wording for `annual_loss`, additive preservation of `CT-011` through `CT-016`, and risk-register synchronization.
- The addendum stays out of Tasks 1 through 7 of the original `annual_loss` slice plan and does not expand the slice into Phase E runtime work.
- The refactor-program updates remain limited to accepted-slice state and do not attempt to close deferred Phase E tracks.

### Placeholder Scan

- No `TBD`, `TODO`, `implement later`, `fill in details`, or generic "sync docs" instructions remain.
- Every task names the exact files, exact assertions, exact markdown snippets, and exact commands needed to implement the addendum.
- The plan does not refer back to the original plan with "similar to Task 8"; it spells out the additive work explicitly.

### Type Consistency

- Status vocabulary stays aligned with the active governance documents: `accepted breadth-closure slice`, `next recommended single-sheet breadth slice`, `pending first-wave gap`, and `deferred runtime/operator gap`.
- Row IDs used in the tests and snippets match the current governance baseline: `AL-001` through `AL-004`, `CT-005`, `CT-011` through `CT-016`, `XD-002`, and `XD-005`.
- The addendum keeps `annual_loss` accepted while preserving the deferred/runtime state of `CT-011` through `CT-016`, so the docs do not over-claim broader first-wave closure.

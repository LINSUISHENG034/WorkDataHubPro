# WorkDataHubPro Annuity Income Validation Slice Implementation Plan

**Date:** 2026-04-14
**Status:** Done
**Target Repository:** `E:\Projects\WorkDataHubPro`

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Close the remaining first-wave domain gap by implementing and validating the `annuity_income` slice without silently reviving retired identity behavior or dropping operator-facing artifacts.

**Architecture:** Reuse the accepted single-sheet and publication runtime already proven by `annuity_performance`. Keep `annuity_income`-specific cleansing, branch-mapping memory, ID5 retirement protection, and operator-artifact behavior explicit inside the slice instead of hiding them in generic helpers or deferred Phase E operator decisions.

**Tech Stack:** Python 3.12+, `uv`, `pytest`, `openpyxl`, `typer`, standard-library `dataclasses`, `json`, `pathlib`

---

## Scope Check

This plan covers:

- single-sheet workbook intake for `收入明细`
- governed `annuity_income` normalization and canonical fact processing
- explicit protection for `COMPANY_BRANCH_MAPPING` manual overrides
- explicit protection for ID5 fallback retirement
- unresolved-name and failed-record operator artifacts
- explicit derivation and publication flow for `annuity_income`
- service-delegation execution and explicit no-hook contract
- replay assets, runbook, explainability evidence, and coverage-matrix linkage

This plan does not cover:

- `company_lookup_queue` production runtime closure
- `reference_sync` runtime retention or replacement
- manual `customer-mdm` operator command closure
- production storage / deferred publication runtime design
- full cross-domain operator artifact parity beyond the `annuity_income` share needed for slice admission

The deliberate consequence is that `annuity_income` becomes an admitted executable slice without collapsing Phase D breadth work into Phase E runtime decisions.

## Suggested Branch

- `slice/annuity-income-closure`

## Coverage Row Mapping

| Matrix Row | Scope In Slice |
|---|---|
| AI-001 | single-sheet workbook intake and row anchoring |
| AI-002 | canonical cleansing and fact processing |
| AI-003 | identity, derivation, and explicit publication path |
| AI-004 | unresolved-name and failed-record operator artifacts |
| AI-005 | service-delegation execution path with explicit no-hook guard |
| CT-016 | shared operator artifact parity handled only to the degree needed for `annuity_income` slice acceptance |

## File Structure

Create or modify these files in this order so the slice closes with one explicit chain:

- `src/work_data_hub_pro/capabilities/source_intake/annuity_income/service.py`
- `tests/integration/test_annuity_income_intake.py`
- `src/work_data_hub_pro/capabilities/fact_processing/annuity_income/service.py`
- `config/domains/annuity_income/cleansing.json`
- `config/releases/2026-04-14-annuity-income-baseline.json`
- `tests/integration/test_annuity_income_processing.py`
- `tests/integration/test_annuity_income_operator_artifacts.py`
- `src/work_data_hub_pro/capabilities/reference_derivation/service.py`
- `config/policies/publication.json`
- `tests/integration/test_reference_derivation.py`
- `tests/integration/test_publication_service.py`
- `src/work_data_hub_pro/apps/orchestration/replay/annuity_income_slice.py`
- `src/work_data_hub_pro/apps/etl_cli/main.py`
- `reference/historical_replays/annuity_income/legacy_monthly_snapshot_2026_03.json`
- `reference/historical_replays/annuity_income/annuity_performance_fixture_2026_03.json`
- `reference/historical_replays/annuity_income/customer_plan_history_2026_03.json`
- `docs/runbooks/annuity-income-replay.md`
- `tests/contracts/test_annuity_income_replay_assets.py`
- `tests/replay/test_annuity_income_slice.py`
- `tests/replay/test_annuity_income_explainability_slo.py`
- `docs/superpowers/specs/2026-04-11-workdatahubpro-first-wave-legacy-coverage-matrix.md`

### Task 1: Implement `annuity_income` Single-Sheet Intake

**Files:**
- Create: `src/work_data_hub_pro/capabilities/source_intake/annuity_income/service.py`
- Test: `tests/integration/test_annuity_income_intake.py`

- [ ] **Step 1: Write the failing intake test**

```python
from openpyxl import Workbook

from work_data_hub_pro.capabilities.source_intake.annuity_income.service import (
    AnnuityIncomeIntakeService,
)


def test_annuity_income_intake_reads_shou_ru_ming_xi_sheet_and_preserves_anchor_rows(
    tmp_path,
) -> None:
    workbook_path = tmp_path / "annuity_income_2026_03.xlsx"
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "收入明细"
    sheet.append(["月度", "机构", "机构名称", "计划号", "客户名称", "业务类型", "计划类型"])
    sheet.append(["2026年03月", "G01", "北京其他", "PLAN-A", "示例客户", "受托", "单一计划"])
    workbook.save(workbook_path)

    batch = AnnuityIncomeIntakeService().read_batch(workbook_path, period="2026-03")

    assert batch.domain == "annuity_income"
    assert batch.row_count == 1
    assert batch.records[0].anchor_row_no == 2
```

- [ ] **Step 2: Run the targeted test and verify it fails**

Run: `uv run pytest tests/integration/test_annuity_income_intake.py -v`

Expected: FAIL because the intake service does not exist yet.

- [ ] **Step 3: Implement the intake service**

Implement a service that:

- reads only the `收入明细` sheet
- preserves `anchor_row_no`
- emits the standard intake batch/record contract used by accepted slices
- records workbook path and period in the batch metadata

- [ ] **Step 4: Re-run the targeted test**

Run: `uv run pytest tests/integration/test_annuity_income_intake.py -v`

Expected: PASS

### Task 2: Implement Governed `annuity_income` Fact Processing

**Files:**
- Create: `src/work_data_hub_pro/capabilities/fact_processing/annuity_income/service.py`
- Create: `config/domains/annuity_income/cleansing.json`
- Create: `config/releases/2026-04-14-annuity-income-baseline.json`
- Test: `tests/integration/test_annuity_income_processing.py`

- [ ] **Step 1: Write the failing processing test**

```python
from work_data_hub_pro.capabilities.fact_processing.annuity_income.service import (
    AnnuityIncomeFactProcessingService,
)


def test_annuity_income_processing_applies_branch_mapping_fee_defaults_and_name_normalization() -> None:
    service = AnnuityIncomeFactProcessingService()
    processed = service.process_records(
        [
            {
                "月度": "2026年03月",
                "机构": "",
                "机构名称": "北京其他",
                "计划号": "PLAN-A",
                "客户名称": "示例客户  ",
                "业务类型": "受托",
                "计划类型": "单一计划",
                "组合代码": "",
                "固费": None,
            }
        ]
    )

    row = processed[0]
    assert row["机构代码"] == "G37"
    assert row["固费"] == 0
    assert row["客户名称"] == "示例客户"
```

- [ ] **Step 2: Run the targeted processing test and verify it fails**

Run: `uv run pytest tests/integration/test_annuity_income_processing.py -v`

Expected: FAIL because the processing service and domain config are not present yet.

- [ ] **Step 3: Implement the minimal governed processing flow**

Implement:

- `COMPANY_BRANCH_MAPPING` support including the six manual overrides recorded in the legacy cleansing rules
- date normalization for `月度`
- fee defaults and portfolio defaults
- customer-name normalization and preserved `年金账户名`
- release binding through `config/releases/2026-04-14-annuity-income-baseline.json`

- [ ] **Step 4: Re-run the processing test**

Run: `uv run pytest tests/integration/test_annuity_income_processing.py -v`

Expected: PASS

### Task 3: Protect Identity Semantics And Operator Artifacts

**Files:**
- Modify: `src/work_data_hub_pro/capabilities/fact_processing/annuity_income/service.py`
- Test: `tests/integration/test_annuity_income_operator_artifacts.py`

- [ ] **Step 1: Write the failing identity and artifact tests**

```python
from work_data_hub_pro.capabilities.fact_processing.annuity_income.service import (
    AnnuityIncomeFactProcessingService,
)


def test_annuity_income_never_uses_id5_fallback_for_company_id() -> None:
    service = AnnuityIncomeFactProcessingService()
    row = service.process_records(
        [
            {
                "计划号": "",
                "客户名称": "未知客户",
                "年金账户名": "旧账户名",
            }
        ]
    )[0]

    assert row["company_id"].startswith("IN")


def test_annuity_income_emits_unknown_name_and_failed_record_artifacts_when_enabled(tmp_path) -> None:
    service = AnnuityIncomeFactProcessingService(output_dir=tmp_path)
    result = service.process_with_artifacts([...], export_unknown_names=True)

    assert result.unknown_names_csv is not None
    assert result.failed_records_csv is not None
```

- [ ] **Step 2: Run the targeted artifact test and verify it fails**

Run: `uv run pytest tests/integration/test_annuity_income_operator_artifacts.py -v`

Expected: FAIL because ID5 protection and artifact outputs are not wired yet.

- [ ] **Step 3: Implement the identity guardrails**

Implement:

- no ID5 fallback path
- temp-ID fallback or equivalent governed unresolved path
- explicit `unknown_names_csv` and failed-record artifact outputs
- service result fields that make artifact presence queryable in replay and runbooks

- [ ] **Step 4: Re-run the artifact test**

Run: `uv run pytest tests/integration/test_annuity_income_operator_artifacts.py -v`

Expected: PASS

### Task 4: Extend Derivation, Publication, And The No-Hook Contract

**Files:**
- Modify: `src/work_data_hub_pro/capabilities/reference_derivation/service.py`
- Modify: `config/policies/publication.json`
- Test: `tests/integration/test_reference_derivation.py`
- Test: `tests/integration/test_publication_service.py`

- [ ] **Step 1: Write the failing publication-path assertions**

```python
def test_annuity_income_publication_plan_exposes_fact_and_customer_signal_targets(publication_policy) -> None:
    targets = publication_policy["annuity_income"]

    assert "fact_annuity_income" in targets
    assert "customer_master_signal" in targets
```

- [ ] **Step 2: Run the derivation and publication tests**

Run: `uv run pytest tests/integration/test_reference_derivation.py tests/integration/test_publication_service.py -v`

Expected: FAIL for missing `annuity_income` publication coverage.

- [ ] **Step 3: Implement explicit derivation and no-hook protection**

Implement:

- `annuity_income` derivation inputs for reference/customer signals
- explicit publication targets and modes
- a regression guard that `annuity_income` still does not trigger the post-load hook chain

- [ ] **Step 4: Re-run the derivation and publication tests**

Run: `uv run pytest tests/integration/test_reference_derivation.py tests/integration/test_publication_service.py -v`

Expected: PASS

### Task 5: Wire Replay Assets, CLI Entry Point, And Explainability Evidence

**Files:**
- Create: `src/work_data_hub_pro/apps/orchestration/replay/annuity_income_slice.py`
- Modify: `src/work_data_hub_pro/apps/etl_cli/main.py`
- Create: `reference/historical_replays/annuity_income/legacy_monthly_snapshot_2026_03.json`
- Create: `reference/historical_replays/annuity_income/annuity_performance_fixture_2026_03.json`
- Create: `reference/historical_replays/annuity_income/customer_plan_history_2026_03.json`
- Create: `docs/runbooks/annuity-income-replay.md`
- Test: `tests/contracts/test_annuity_income_replay_assets.py`
- Test: `tests/replay/test_annuity_income_slice.py`
- Test: `tests/replay/test_annuity_income_explainability_slo.py`

- [ ] **Step 1: Write the failing replay-asset and slice tests**

```python
def test_annuity_income_replay_assets_are_registered() -> None:
    ...


def test_annuity_income_slice_replays_fact_artifact_and_projection_results() -> None:
    ...
```

- [ ] **Step 2: Run the replay-focused tests and verify they fail**

Run: `uv run pytest tests/contracts/test_annuity_income_replay_assets.py tests/replay/test_annuity_income_slice.py tests/replay/test_annuity_income_explainability_slo.py -v`

Expected: FAIL because the replay slice and assets do not exist yet.

- [ ] **Step 3: Implement the replay path**

Implement:

- a replay runner for `annuity_income`
- CLI routing in `apps/etl_cli/main.py`
- baseline assets for fact output, artifact visibility, and explainability retrieval
- a runbook with expected outputs and intentional-diff handling for ID5 retirement

- [ ] **Step 4: Re-run the replay-focused tests**

Run: `uv run pytest tests/contracts/test_annuity_income_replay_assets.py tests/replay/test_annuity_income_slice.py tests/replay/test_annuity_income_explainability_slo.py -v`

Expected: PASS

### Task 6: Close Governance Linkage And Run Slice Verification

**Files:**
- Modify: `docs/superpowers/specs/2026-04-11-workdatahubpro-first-wave-legacy-coverage-matrix.md`

- [ ] **Step 1: Update the coverage matrix after code/tests are in place**

Move AI-001 through AI-005 from `planned` to the correct execution status as the slice advances.

- [ ] **Step 2: Run the slice-targeted verification suite**

Run:

```powershell
uv run pytest tests/integration/test_annuity_income_intake.py tests/integration/test_annuity_income_processing.py tests/integration/test_annuity_income_operator_artifacts.py tests/integration/test_reference_derivation.py tests/integration/test_publication_service.py tests/contracts/test_annuity_income_replay_assets.py tests/replay/test_annuity_income_slice.py tests/replay/test_annuity_income_explainability_slo.py -v
```

Expected: PASS

- [ ] **Step 3: Run the repository-wide suite before claiming acceptance**

Run:

```powershell
uv run pytest -v
```

Expected: PASS

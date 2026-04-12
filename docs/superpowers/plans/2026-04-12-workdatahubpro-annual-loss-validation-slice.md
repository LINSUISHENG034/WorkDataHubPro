# Annual Loss Validation Slice Implementation Plan

**Date:** 2026-04-12
**Status:** Done
**Target Repository:** `E:\Projects\WorkDataHubPro`

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the third executable `WorkDataHubPro` validation slice so `annual_loss` runs end to end through merge-aware multi-sheet intake, governed loss fact processing, current-contract plan-code enrichment, explicit publication, downstream status projection consumption, replay, and compatibility adjudication.

**Architecture:** Extend the accepted `annuity_performance` and `annual_award` runtime instead of introducing a parallel event-domain stack. Keep multi-sheet workbook behavior isolated to `capabilities/source_intake/annual_loss`, keep loss-domain normalization and fallback semantics inside `capabilities/fact_processing/annual_loss`, and reuse the existing publication, tracing, lineage, replay, and adjudication runtime. Seed replay with `annuity_performance` and `annual_award` fixtures so the slice can close the `annual_loss -> contract_state -> monthly_snapshot` dependency path without pulling `annuity_income` or Phase E production-runtime decisions into the same slice.

**Tech Stack:** Python 3.12+, `uv`, `pytest`, `openpyxl`, `typer`, standard-library `dataclasses`, `enum`, `json`, `pathlib`

---

## Scope Check

This plan covers:

- a merge-aware multi-sheet intake contract for `annual_loss`
- governed loss-event normalization, date parsing, and canonical fact processing
- reuse of the shared identity-resolution contract with loss-domain fixtures
- current-contract `plan_code` lookup with `valid_to = 9999-12-31` protection and `AN001` / `AN002` fallback defaults
- explicit `annual_loss` fact publication plus loss-derived customer-signal publication
- downstream projection consumption of published `annual_loss` facts while keeping snapshot output keys stable
- replay orchestration, runbook, explainability evidence, and compatibility adjudication
- governance-document updates required to mark `annual_loss` accepted and advance `annuity_income` to the next recommended slice

This plan does not cover:

- the `annuity_income` executable slice
- production storage / deferred publication runtime design
- live provider integration beyond the existing cache-first identity interface
- full customer-master / projection semantic-width parity beyond the accepted validation bridge
- Dagster wiring or broader operator-tooling rollout

The deliberate consequence is that the slice reuses the accepted runtime and narrows the net-new work to `annual_loss` behavior that is still fixture-only today: multi-sheet loss intake, loss-specific transformation, current-contract plan-code lookup, loss-signal derivation, and projection closure for `is_loss_reported`.

## Suggested Branch

- `slice/annual-loss-closure`

## File Structure

Create or modify these files in this order so the slice closes with one explicit chain:

- `src/work_data_hub_pro/capabilities/source_intake/annual_loss/service.py`: merge-aware loss workbook intake with stable merged anchors and preserved sheet provenance
- `tests/integration/test_annual_loss_intake.py`: multi-sheet intake contract test
- `src/work_data_hub_pro/capabilities/fact_processing/cleansing/rules.py`: shared normalization helpers for event-domain period, date, business-type, and plan-type cleansing
- `src/work_data_hub_pro/capabilities/fact_processing/cleansing/manifest.py`: `annual_loss` rule-pack registration
- `config/domains/annual_loss/cleansing.json`: `annual_loss` enablement and activation order
- `config/releases/2026-04-12-annual-loss-baseline.json`: release binding for the slice
- `src/work_data_hub_pro/capabilities/fact_processing/annual_loss/service.py`: canonical loss-event processing
- `tests/integration/test_annual_loss_processing.py`: loss processing contract
- `src/work_data_hub_pro/capabilities/fact_processing/annual_loss/plan_code_lookup.py`: current-contract lookup and domain-default fallback for missing `plan_code`
- `tests/integration/test_annual_loss_plan_code_enrichment.py`: plan-code enrichment coverage
- `src/work_data_hub_pro/capabilities/reference_derivation/service.py`: loss-derived customer signal generation
- `config/policies/publication.json`: `annual_loss` publication targets
- `tests/integration/test_reference_derivation.py`: loss derivation coverage
- `tests/integration/test_publication_service.py`: loss publication policy coverage
- `src/work_data_hub_pro/capabilities/projections/contract_state.py`: published `annual_loss` fact consumption with compatibility bridge
- `tests/integration/test_projection_outputs.py`: projection regression for published loss facts
- `src/work_data_hub_pro/apps/orchestration/replay/annual_loss_slice.py`: explicit third-slice runner
- `src/work_data_hub_pro/apps/etl_cli/main.py`: CLI entrypoint for `annual_loss` replay
- `tests/replay/test_annual_loss_slice.py`: end-to-end replay path and diff-path adjudication
- `reference/historical_replays/annual_loss/annuity_performance_fixture_2026_03.json`: read-only dependency fixture
- `reference/historical_replays/annual_loss/annual_award_fixture_2026_03.json`: read-only dependency fixture
- `reference/historical_replays/annual_loss/customer_plan_history_2026_03.json`: replayed customer-plan history with current-row markers
- `reference/historical_replays/annual_loss/legacy_monthly_snapshot_2026_03.json`: locked baseline for adjudication
- `docs/runbooks/annual-loss-replay.md`: operator replay instructions
- `tests/contracts/test_annual_loss_replay_assets.py`: replay asset contract
- `tests/replay/test_annual_loss_explainability_slo.py`: slice-level explainability retrieval acceptance test
- `docs/superpowers/specs/2026-04-11-workdatahubpro-first-wave-legacy-coverage-matrix.md`: Phase D coverage updates
- `docs/superpowers/specs/2026-04-11-workdatahubpro-refactor-program.md`: program-position updates after slice acceptance
- `tests/contracts/test_annual_loss_governance_docs.py`: governance-doc closure checks

### Task 1: Implement Merge-Aware `annual_loss` Intake

**Files:**
- Create: `src/work_data_hub_pro/capabilities/source_intake/annual_loss/service.py`
- Test: `tests/integration/test_annual_loss_intake.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/integration/test_annual_loss_intake.py
from openpyxl import Workbook

from work_data_hub_pro.capabilities.source_intake.annual_loss.service import (
    AnnualLossIntakeService,
)


def test_annual_loss_intake_merges_trustee_and_investee_sheets_into_stable_anchor_sequence(
    tmp_path,
) -> None:
    workbook_path = tmp_path / "annual_loss_2026_03.xlsx"
    workbook = Workbook()
    trustee = workbook.active
    trustee.title = "企年受托流失(解约)"
    trustee.append(
        [
            "上报月份",
            "业务类型",
            "计划类型",
            "客户全称",
            "机构",
            "年金计划号",
            "流失日期",
            "计划规模",
            "受托人",
            "company_id",
            "区域",
            "年金中心",
            "上报人",
            "考核标签",
        ]
    )
    trustee.append(
        [
            "2026年03月",
            "受托",
            "集合",
            "共享客户（流失）",
            "北京",
            "",
            "",
            "80",
            "原受托机构A",
            "company-001",
            "华北",
            "中心A",
            "测试",
            "drop-me",
        ]
    )
    investee = workbook.create_sheet("企年投资流失(解约)")
    investee.append(
        [
            "上报月份",
            "业务类型",
            "计划类型",
            "客户全称",
            "机构",
            "年金计划号",
            "流失日期",
            "计划规模",
            "受托人",
            "company_id",
            "区域",
            "年金中心",
            "上报人",
            "考核标签",
        ]
    )
    investee.append(
        [
            "2026年03月",
            "投管",
            "单一",
            "新客流失",
            "未知机构",
            "",
            "2026-03-15",
            "60",
            "原受托机构B",
            "",
            "华东",
            "中心B",
            "测试",
            "drop-me",
        ]
    )
    workbook.save(workbook_path)

    result = AnnualLossIntakeService().read_batch(
        run_id="run-001",
        period="2026-03",
        source_files=[workbook_path],
    )

    assert result.batch.batch_id == "annual_loss:2026-03"
    assert result.batch.row_count == 2
    assert [record.anchor_row_no for record in result.records] == [2, 3]
    assert [record.origin_row_nos for record in result.records] == [[2], [2]]
    assert [record.raw_payload["source_sheet"] for record in result.records] == [
        "企年受托流失(解约)",
        "企年投资流失(解约)",
    ]
    assert [record.raw_payload["客户全称"] for record in result.records] == [
        "共享客户（流失）",
        "新客流失",
    ]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/integration/test_annual_loss_intake.py -v`
Expected: FAIL with `ModuleNotFoundError` for `work_data_hub_pro.capabilities.source_intake.annual_loss.service`

- [ ] **Step 3: Write minimal implementation**

```python
# src/work_data_hub_pro/capabilities/source_intake/annual_loss/service.py
from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from hashlib import sha256
from pathlib import Path

from openpyxl import load_workbook

from work_data_hub_pro.platform.contracts.models import (
    FieldTraceEvent,
    InputBatch,
    InputRecord,
)


@dataclass(frozen=True)
class IntakeResult:
    batch: InputBatch
    records: list[InputRecord]
    trace_events: list[FieldTraceEvent]


class AnnualLossIntakeService:
    domain = "annual_loss"
    sheet_names = ("企年受托流失(解约)", "企年投资流失(解约)")
    stage_id = "source_intake"

    def read_batch(
        self,
        *,
        run_id: str,
        period: str,
        source_files: list[Path],
    ) -> IntakeResult:
        snapshot_hash = sha256()
        records: list[InputRecord] = []
        trace_events: list[FieldTraceEvent] = []
        merged_anchor_row_no = 2

        for source_file in source_files:
            workbook = load_workbook(source_file, read_only=True, data_only=True)
            try:
                for sheet_name in self.sheet_names:
                    sheet = workbook[sheet_name]
                    headers = [
                        cell.value
                        for cell in next(sheet.iter_rows(min_row=1, max_row=1))
                    ]
                    for source_row_no, row in enumerate(
                        sheet.iter_rows(min_row=2, values_only=True),
                        start=2,
                    ):
                        payload = dict(zip(headers, row, strict=True)) | {
                            "source_sheet": sheet_name,
                            "source_row_no": source_row_no,
                        }
                        snapshot_hash.update(
                            repr((source_file.name, sheet_name, source_row_no, payload)).encode("utf-8")
                        )
                        record_id = (
                            f"{run_id}:{source_file.stem}:{sheet_name}:{source_row_no}"
                        )
                        record = InputRecord(
                            run_id=run_id,
                            record_id=record_id,
                            batch_id=f"{self.domain}:{period}",
                            anchor_row_no=merged_anchor_row_no,
                            origin_row_nos=[source_row_no],
                            parent_record_ids=[],
                            stage_row_no=merged_anchor_row_no,
                            raw_payload=payload,
                        )
                        records.append(record)
                        trace_events.append(
                            FieldTraceEvent(
                                trace_id=f"trace:{record_id}",
                                event_id=f"{record_id}:intake",
                                event_seq=0,
                                run_id=run_id,
                                batch_id=record.batch_id,
                                record_id=record.record_id,
                                anchor_row_no=record.anchor_row_no,
                                stage_id=self.stage_id,
                                field_name="raw_payload",
                                value_before=None,
                                value_after=payload,
                                rule_id="capture-input",
                                rule_version="1",
                                config_release_id="system:source-intake",
                                action_type="snapshot",
                                timestamp=datetime.now(UTC).isoformat(),
                                success=True,
                            )
                        )
                        merged_anchor_row_no += 1
            finally:
                workbook.close()

        batch = InputBatch(
            batch_id=f"{self.domain}:{period}",
            domain=self.domain,
            period=period,
            source_files=[str(path) for path in source_files],
            input_snapshot_id=snapshot_hash.hexdigest(),
            row_count=len(records),
        )
        return IntakeResult(batch=batch, records=records, trace_events=trace_events)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/integration/test_annual_loss_intake.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/work_data_hub_pro/capabilities/source_intake/annual_loss/service.py tests/integration/test_annual_loss_intake.py
@'
feat(source-intake): add merge-aware annual_loss intake

Introduce the multi-sheet intake service for `annual_loss` so trustee and
investee loss rows enter one explicit input stream with stable merged anchors
and preserved source-sheet provenance.

Validation:
- uv run pytest tests/integration/test_annual_loss_intake.py -v
'@ | git commit -F -
```

### Task 2: Implement Governed `annual_loss` Fact Processing

**Files:**
- Modify: `src/work_data_hub_pro/capabilities/fact_processing/cleansing/rules.py`
- Modify: `src/work_data_hub_pro/capabilities/fact_processing/cleansing/manifest.py`
- Create: `config/domains/annual_loss/cleansing.json`
- Create: `config/releases/2026-04-12-annual-loss-baseline.json`
- Create: `src/work_data_hub_pro/capabilities/fact_processing/annual_loss/service.py`
- Test: `tests/integration/test_annual_loss_processing.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/integration/test_annual_loss_processing.py
from pathlib import Path

from work_data_hub_pro.capabilities.fact_processing.annual_loss.service import (
    AnnualLossProcessor,
)
from work_data_hub_pro.capabilities.fact_processing.cleansing.manifest import (
    CleansingManifest,
)
from work_data_hub_pro.platform.contracts.models import InputRecord


def test_annual_loss_processor_normalizes_loss_fields_dates_and_product_line() -> None:
    manifest = CleansingManifest.load(
        release_path=Path("config/releases/2026-04-12-annual-loss-baseline.json"),
        domain_path=Path("config/domains/annual_loss/cleansing.json"),
    )
    record = InputRecord(
        run_id="run-001",
        record_id="run-001:annual_loss:2",
        batch_id="annual_loss:2026-03",
        anchor_row_no=2,
        origin_row_nos=[2],
        parent_record_ids=[],
        stage_row_no=2,
        raw_payload={
            "上报月份": "2026年03月",
            "业务类型": "投管",
            "计划类型": "集合",
            "客户全称": "  共享客户（流失）  ",
            "机构": "未知机构",
            "年金计划号": None,
            "流失日期": "2026-03-15",
            "受托人": "原受托机构A",
            "company_id": "",
            "source_sheet": "企年投资流失(解约)",
            "source_row_no": 2,
        },
    )

    result = AnnualLossProcessor(manifest).process(record)

    assert result.fact.domain == "annual_loss"
    assert result.fact.fact_type == "annual_loss"
    assert result.fact.fields["company_name"] == "共享客户（流失）"
    assert result.fact.fields["plan_code"] == ""
    assert result.fact.fields["plan_type"] == "集合计划"
    assert result.fact.fields["business_type"] == "企年投资"
    assert result.fact.fields["product_line_code"] == "PL201"
    assert result.fact.fields["period"] == "2026-03"
    assert result.fact.fields["loss_date"] == "2026-03-15"
    assert result.fact.fields["institution_code"] == "G00"
    assert len(result.trace_events) == 6
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/integration/test_annual_loss_processing.py -v`
Expected: FAIL with `FileNotFoundError` for `config/releases/2026-04-12-annual-loss-baseline.json` or `ModuleNotFoundError` for `annual_loss.service`

- [ ] **Step 3: Write minimal implementation**

```python
# src/work_data_hub_pro/capabilities/fact_processing/cleansing/rules.py
EVENT_BUSINESS_TYPE_MAPPING = {
    "受托": "企年受托",
    "投资": "企年投资",
    "投管": "企年投资",
    "企年受托": "企年受托",
    "企年投资": "企年投资",
}

EVENT_PLAN_TYPE_MAPPING = {
    "集合": "集合计划",
    "单一": "单一计划",
    "集合计划": "集合计划",
    "单一计划": "单一计划",
}


def normalize_event_business_type(value: Any) -> str:
    normalized = str(value or "").strip()
    return EVENT_BUSINESS_TYPE_MAPPING.get(normalized, normalized)


def normalize_event_plan_type(value: Any) -> str:
    normalized = str(value or "").strip()
    return EVENT_PLAN_TYPE_MAPPING.get(normalized, normalized)


def normalize_period(value: Any) -> str:
    digits = "".join(character for character in str(value or "") if character.isdigit())
    if len(digits) >= 6:
        return f"{digits[:4]}-{digits[4:6]}"
    return str(value or "").strip()


def normalize_event_date(value: Any) -> str | None:
    digits = "".join(character for character in str(value or "") if character.isdigit())
    if not digits:
        return None
    if len(digits) == 6:
        return f"{digits[:4]}-{digits[4:6]}-01"
    return f"{digits[:4]}-{digits[4:6]}-{digits[6:8]}"
```

```python
# src/work_data_hub_pro/capabilities/fact_processing/cleansing/manifest.py
    ("annual-loss-core", "2026.04.12"): {
        "company_name": CleansingRule(
            rule_id="normalize-company-name",
            version="1",
            field_name="company_name",
            transform=lambda value: str(value or "").strip(),
        ),
        "plan_code": CleansingRule(
            rule_id="normalize-plan-code",
            version="1",
            field_name="plan_code",
            transform=normalize_plan_code,
        ),
        "plan_type": CleansingRule(
            rule_id="normalize-plan-type",
            version="1",
            field_name="plan_type",
            transform=normalize_event_plan_type,
        ),
        "business_type": CleansingRule(
            rule_id="normalize-business-type",
            version="1",
            field_name="business_type",
            transform=normalize_event_business_type,
        ),
        "period": CleansingRule(
            rule_id="normalize-period",
            version="1",
            field_name="period",
            transform=normalize_period,
        ),
        "loss_date": CleansingRule(
            rule_id="normalize-loss-date",
            version="1",
            field_name="loss_date",
            transform=normalize_event_date,
        ),
    },
```

```json
// config/domains/annual_loss/cleansing.json
{
  "domain": "annual_loss",
  "rule_pack_id": "annual-loss-core",
  "rule_pack_version": "2026.04.12",
  "activation_order": [
    "company_name",
    "plan_code",
    "plan_type",
    "business_type",
    "period",
    "loss_date"
  ],
  "enabled_fields": [
    "company_name",
    "plan_code",
    "plan_type",
    "business_type",
    "period",
    "loss_date"
  ]
}
```

```json
// config/releases/2026-04-12-annual-loss-baseline.json
{
  "release_id": "2026-04-12-annual-loss-baseline",
  "rule_pack_versions": {
    "annual_loss": "2026.04.12"
  },
  "domains": {
    "annual_loss": "config/domains/annual_loss/cleansing.json"
  }
}
```

```python
# src/work_data_hub_pro/capabilities/fact_processing/annual_loss/service.py
from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime

from work_data_hub_pro.capabilities.fact_processing.cleansing.manifest import (
    CleansingManifest,
)
from work_data_hub_pro.platform.contracts.models import (
    CanonicalFactRecord,
    FieldTraceEvent,
    InputRecord,
)


PRODUCT_LINE_CODE_MAPPING = {"企年投资": "PL201", "企年受托": "PL202"}


@dataclass(frozen=True)
class ProcessingResult:
    fact: CanonicalFactRecord
    trace_events: list[FieldTraceEvent]


class AnnualLossProcessor:
    stage_id = "fact_processing"

    def __init__(self, manifest: CleansingManifest) -> None:
        self._manifest = manifest

    def process(self, record: InputRecord) -> ProcessingResult:
        cleaned_fields = {
            "company_name": record.raw_payload.get("客户全称"),
            "source_company_id": record.raw_payload.get("company_id"),
            "plan_code": record.raw_payload.get("年金计划号"),
            "plan_type": record.raw_payload.get("计划类型"),
            "business_type": record.raw_payload.get("业务类型"),
            "period": record.raw_payload.get("上报月份"),
            "loss_date": record.raw_payload.get("流失日期"),
            "institution_name": record.raw_payload.get("机构"),
            "previous_trustee": record.raw_payload.get("受托人"),
            "source_sheet": record.raw_payload.get("source_sheet"),
            "source_row_no": record.raw_payload.get("source_row_no"),
        }
        trace_events: list[FieldTraceEvent] = []

        for event_seq, active_rule in enumerate(self._manifest.active_rules, start=1):
            before = cleaned_fields.get(active_rule.field_name)
            after = active_rule.rule.transform(before)
            cleaned_fields[active_rule.field_name] = after
            trace_events.append(
                FieldTraceEvent(
                    trace_id=f"trace:{record.record_id}",
                    event_id=f"{record.record_id}:{event_seq}",
                    event_seq=event_seq,
                    run_id=record.run_id,
                    batch_id=record.batch_id,
                    record_id=record.record_id,
                    anchor_row_no=record.anchor_row_no,
                    stage_id=self.stage_id,
                    field_name=active_rule.field_name,
                    value_before=before,
                    value_after=after,
                    rule_id=active_rule.rule.rule_id,
                    rule_version=f"{self._manifest.rule_pack_version}.{active_rule.rule.version}",
                    config_release_id=self._manifest.release_id,
                    action_type="cleanse",
                    timestamp=datetime.now(UTC).isoformat(),
                    success=True,
                )
            )

        cleaned_fields["product_line_code"] = PRODUCT_LINE_CODE_MAPPING.get(
            str(cleaned_fields["business_type"]),
            "",
        )
        cleaned_fields["institution_code"] = "G00"

        fact = CanonicalFactRecord(
            run_id=record.run_id,
            record_id=f"fact:{record.record_id}",
            batch_id=record.batch_id,
            domain="annual_loss",
            fact_type="annual_loss",
            fields=cleaned_fields,
            lineage_ref=record.record_id,
            trace_ref=f"trace:{record.record_id}",
        )
        return ProcessingResult(fact=fact, trace_events=trace_events)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/integration/test_annual_loss_processing.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/work_data_hub_pro/capabilities/fact_processing/cleansing/rules.py src/work_data_hub_pro/capabilities/fact_processing/cleansing/manifest.py config/domains/annual_loss/cleansing.json config/releases/2026-04-12-annual-loss-baseline.json src/work_data_hub_pro/capabilities/fact_processing/annual_loss/service.py tests/integration/test_annual_loss_processing.py
@'
feat(fact-processing): add governed annual_loss processor

Introduce the governed `annual_loss` rule pack, release binding, and canonical
loss-event processor so period, date, plan-type, and business-type behavior are
explicit and replayable.

Validation:
- uv run pytest tests/integration/test_annual_loss_processing.py -v
'@ | git commit -F -
```

### Task 3: Implement Current-Contract Plan-Code Enrichment For `annual_loss`

**Files:**
- Create: `src/work_data_hub_pro/capabilities/fact_processing/annual_loss/plan_code_lookup.py`
- Test: `tests/integration/test_annual_loss_plan_code_enrichment.py`

- [ ] **Step 1: Write the failing tests**

```python
# tests/integration/test_annual_loss_plan_code_enrichment.py
from work_data_hub_pro.capabilities.fact_processing.annual_loss.plan_code_lookup import (
    AnnualLossPlanCodeEnrichmentService,
    CustomerPlanHistoryLookup,
)
from work_data_hub_pro.platform.contracts.models import CanonicalFactRecord


def test_annual_loss_plan_code_enrichment_prefers_current_contract_rows_and_plan_type_prefix() -> None:
    service = AnnualLossPlanCodeEnrichmentService(
        CustomerPlanHistoryLookup(
            [
                {
                    "company_id": "company-001",
                    "product_line_code": "PL202",
                    "plan_code": "S7999",
                    "effective_period": "2025-12",
                    "valid_to": "9999-12-31",
                },
                {
                    "company_id": "company-001",
                    "product_line_code": "PL202",
                    "plan_code": "P9001",
                    "effective_period": "2025-12",
                    "valid_to": "9999-12-31",
                },
                {
                    "company_id": "company-001",
                    "product_line_code": "PL202",
                    "plan_code": "P7000",
                    "effective_period": "2024-12",
                    "valid_to": "2025-12-31",
                },
            ]
        )
    )
    fact = CanonicalFactRecord(
        run_id="run-001",
        record_id="fact-001",
        batch_id="annual_loss:2026-03",
        domain="annual_loss",
        fact_type="annual_loss",
        fields={
            "company_id": "company-001",
            "product_line_code": "PL202",
            "plan_type": "集合计划",
            "plan_code": "",
            "period": "2026-03",
        },
        lineage_ref="record-001",
        trace_ref="trace:record-001",
    )

    enriched = service.enrich(
        fact,
        anchor_row_no=2,
        config_release_id="2026-04-12-annual-loss-baseline",
    )

    assert enriched.fact.fields["plan_code"] == "P9001"
    assert enriched.trace_events[0].rule_id == "customer_plan_history_lookup"


def test_annual_loss_plan_code_enrichment_falls_back_to_domain_default_when_lookup_misses() -> None:
    service = AnnualLossPlanCodeEnrichmentService(CustomerPlanHistoryLookup([]))
    fact = CanonicalFactRecord(
        run_id="run-001",
        record_id="fact-002",
        batch_id="annual_loss:2026-03",
        domain="annual_loss",
        fact_type="annual_loss",
        fields={
            "company_id": "company-002",
            "product_line_code": "PL201",
            "plan_type": "单一计划",
            "plan_code": "",
            "period": "2026-03",
        },
        lineage_ref="record-002",
        trace_ref="trace:record-002",
    )

    enriched = service.enrich(
        fact,
        anchor_row_no=3,
        config_release_id="2026-04-12-annual-loss-baseline",
    )

    assert enriched.fact.fields["plan_code"] == "AN002"
    assert enriched.trace_events[0].rule_id == "domain_default_plan_code"
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/integration/test_annual_loss_plan_code_enrichment.py -v`
Expected: FAIL with `ModuleNotFoundError` for `work_data_hub_pro.capabilities.fact_processing.annual_loss.plan_code_lookup`

- [ ] **Step 3: Write minimal implementation**

```python
# src/work_data_hub_pro/capabilities/fact_processing/annual_loss/plan_code_lookup.py
from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime

from work_data_hub_pro.platform.contracts.models import (
    CanonicalFactRecord,
    FieldTraceEvent,
)


@dataclass(frozen=True)
class EnrichedLossFact:
    fact: CanonicalFactRecord
    trace_events: list[FieldTraceEvent]


class CustomerPlanHistoryLookup:
    def __init__(self, rows: list[dict[str, object]]) -> None:
        self._rows = rows

    def select_plan_code(
        self,
        *,
        company_id: str,
        product_line_code: str,
        plan_type: str,
    ) -> str | None:
        candidates = sorted(
            [
                row
                for row in self._rows
                if row["company_id"] == company_id
                and row["product_line_code"] == product_line_code
                and str(row.get("valid_to", "9999-12-31")) == "9999-12-31"
            ],
            key=lambda row: str(row["effective_period"]),
            reverse=True,
        )
        preferred_prefix = "P" if plan_type == "集合计划" else "S"
        for row in candidates:
            plan_code = str(row["plan_code"])
            if plan_code.startswith(preferred_prefix):
                return plan_code
        return str(candidates[0]["plan_code"]) if candidates else None


class AnnualLossPlanCodeEnrichmentService:
    stage_id = "fact_processing.plan_code_enrichment"

    def __init__(self, lookup: CustomerPlanHistoryLookup) -> None:
        self._lookup = lookup

    def enrich(
        self,
        fact: CanonicalFactRecord,
        *,
        anchor_row_no: int,
        config_release_id: str,
    ) -> EnrichedLossFact:
        before = str(fact.fields.get("plan_code") or "")
        if before:
            plan_code = before
            method = "preserve_source_plan_code"
        else:
            lookup_plan_code = self._lookup.select_plan_code(
                company_id=str(fact.fields["company_id"]),
                product_line_code=str(fact.fields["product_line_code"]),
                plan_type=str(fact.fields["plan_type"]),
            )
            if lookup_plan_code is not None:
                plan_code = lookup_plan_code
                method = "customer_plan_history_lookup"
            else:
                plan_code = "AN001" if str(fact.fields["plan_type"]) == "集合计划" else "AN002"
                method = "domain_default_plan_code"

        updated_fields = dict(fact.fields)
        updated_fields["plan_code"] = plan_code
        updated_fact = CanonicalFactRecord(
            run_id=fact.run_id,
            record_id=fact.record_id,
            batch_id=fact.batch_id,
            domain=fact.domain,
            fact_type=fact.fact_type,
            fields=updated_fields,
            lineage_ref=fact.lineage_ref,
            trace_ref=fact.trace_ref,
        )
        trace_event = FieldTraceEvent(
            trace_id=fact.trace_ref,
            event_id=f"{fact.record_id}:plan-code",
            event_seq=150,
            run_id=fact.run_id,
            batch_id=fact.batch_id,
            record_id=fact.record_id,
            anchor_row_no=anchor_row_no,
            stage_id=self.stage_id,
            field_name="plan_code",
            value_before=before,
            value_after=plan_code,
            rule_id=method,
            rule_version="1",
            config_release_id=config_release_id,
            action_type="enrich_plan_code",
            timestamp=datetime.now(UTC).isoformat(),
            success=True,
        )
        return EnrichedLossFact(fact=updated_fact, trace_events=[trace_event])
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run pytest tests/integration/test_annual_loss_plan_code_enrichment.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/work_data_hub_pro/capabilities/fact_processing/annual_loss/plan_code_lookup.py tests/integration/test_annual_loss_plan_code_enrichment.py
@'
feat(fact-processing): add annual_loss current-contract plan-code enrichment

Introduce current-contract plan-code lookup for `annual_loss` and preserve the
legacy fallback defaults when the replayed customer-plan history has no match.

Validation:
- uv run pytest tests/integration/test_annual_loss_plan_code_enrichment.py -v
'@ | git commit -F -
```

### Task 4: Extend Reference Derivation And Publication Policy For Loss Signals

**Files:**
- Modify: `src/work_data_hub_pro/capabilities/reference_derivation/service.py`
- Modify: `config/policies/publication.json`
- Modify: `tests/integration/test_reference_derivation.py`
- Modify: `tests/integration/test_publication_service.py`

- [ ] **Step 1: Write the failing tests**

```python
# tests/integration/test_reference_derivation.py
def test_reference_derivation_adds_customer_loss_signal_for_annual_loss() -> None:
    service = ReferenceDerivationService()
    fact = CanonicalFactRecord(
        run_id="run-001",
        record_id="fact-001",
        batch_id="annual_loss:2026-03",
        domain="annual_loss",
        fact_type="annual_loss",
        fields={
            "company_name": "共享客户（流失）",
            "company_id": "company-001",
            "plan_code": "P9001",
            "period": "2026-03",
        },
        lineage_ref="record-001",
        trace_ref="trace:record-001",
    )

    candidates = service.derive([fact])

    assert [candidate.target_object for candidate in candidates] == [
        "company_reference",
        "customer_loss_signal",
    ]
    assert candidates[1].candidate_payload["customer_type"] == "LOSS_CUSTOMER"
    assert candidates[1].candidate_payload["loss_tag"] == "2603-LOSS"
```

```python
# tests/integration/test_publication_service.py
def test_publication_service_supports_annual_loss_fact_and_signal_targets() -> None:
    storage = InMemoryTableStore()
    service = PublicationService(storage)
    policy = load_publication_policy(
        Path("config/policies/publication.json"),
        domain="annual_loss",
    )

    results = service.execute(
        [
            PublicationBundle(
                plan=build_publication_plan(
                    policy=policy,
                    publication_id="publication-loss-facts",
                    target_name="fact_annual_loss",
                    target_kind="fact",
                    refresh_keys=["batch_id"],
                    upsert_keys=[],
                    source_batch_id="annual_loss:2026-03",
                    source_run_id="run-001",
                ),
                rows=[{"record_id": "fact-001", "batch_id": "annual_loss:2026-03", "company_id": "company-001", "plan_code": "P9001", "period": "2026-03"}],
            ),
            PublicationBundle(
                plan=build_publication_plan(
                    policy=policy,
                    publication_id="publication-loss-signal",
                    target_name="customer_loss_signal",
                    target_kind="reference",
                    refresh_keys=[],
                    upsert_keys=["company_id", "period"],
                    source_batch_id="annual_loss:2026-03",
                    source_run_id="run-001",
                ),
                rows=[{"company_id": "company-001", "period": "2026-03", "customer_type": "LOSS_CUSTOMER"}],
            ),
        ]
    )

    assert [result.target_name for result in results] == [
        "fact_annual_loss",
        "customer_loss_signal",
    ]
    assert storage.read("customer_loss_signal")[0]["customer_type"] == "LOSS_CUSTOMER"
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/integration/test_reference_derivation.py tests/integration/test_publication_service.py -v`
Expected: FAIL because `annual_loss` derivation and publication targets are not registered yet

- [ ] **Step 3: Write minimal implementation**

```python
# src/work_data_hub_pro/capabilities/reference_derivation/service.py
            if fact.domain == "annual_loss":
                period = str(fact.fields["period"])
                candidates.append(
                    DerivationCandidate(
                        target_object="customer_loss_signal",
                        candidate_payload={
                            "company_id": fact.fields["company_id"],
                            "period": period,
                            "plan_code": fact.fields["plan_code"],
                            "customer_type": "LOSS_CUSTOMER",
                            "loss_tag": f"{period[2:4]}{period[5:7]}-LOSS",
                            "source_fact_id": fact.record_id,
                        },
                        source_record_ids=[fact.record_id],
                        derivation_rule_id="customer-loss-from-annual-loss",
                        derivation_rule_version="1",
                    )
                )
```

```json
// config/policies/publication.json
"annual_loss": {
  "fact_annual_loss": {
    "mode": "REFRESH",
    "transaction_group": "fact-publication",
    "idempotency_scope": "batch"
  },
  "company_reference": {
    "mode": "UPSERT",
    "transaction_group": "reference-publication",
    "idempotency_scope": "company_id"
  },
  "customer_loss_signal": {
    "mode": "UPSERT",
    "transaction_group": "reference-publication",
    "idempotency_scope": "company_id+period"
  },
  "contract_state": {
    "mode": "REFRESH",
    "transaction_group": "projection-publication",
    "idempotency_scope": "period"
  },
  "monthly_snapshot": {
    "mode": "APPEND_ONLY",
    "transaction_group": "projection-publication",
    "idempotency_scope": "run"
  }
}
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run pytest tests/integration/test_reference_derivation.py tests/integration/test_publication_service.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/work_data_hub_pro/capabilities/reference_derivation/service.py config/policies/publication.json tests/integration/test_reference_derivation.py tests/integration/test_publication_service.py
@'
feat(reference-derivation): add annual_loss signal publication

Extend the derivation and publication policy so `annual_loss` can emit explicit
loss facts and customer-loss signals instead of staying a fixture-only
dependency.

Validation:
- uv run pytest tests/integration/test_reference_derivation.py tests/integration/test_publication_service.py -v
'@ | git commit -F -
```

### Task 5: Update Projections To Consume Published `annual_loss` Facts

**Files:**
- Modify: `src/work_data_hub_pro/capabilities/projections/contract_state.py`
- Test: `tests/integration/test_projection_outputs.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/integration/test_projection_outputs.py
def test_projections_consume_published_annual_loss_facts_with_compatibility_bridge() -> None:
    storage = InMemoryTableStore(
        seed={
            "fact_annuity_performance": [
                {"record_id": "fact-perf-001", "company_id": "company-001", "plan_code": "P9001", "period": "2026-03"}
            ],
            "fixture_annual_award": [
                {"company_id": "company-001", "plan_code": "P9001", "period": "2026-03", "source_record_id": "award-001"}
            ],
            "fact_annual_loss": [
                {"record_id": "fact-loss-001", "company_id": "company-001", "plan_code": "P9001", "period": "2026-03"}
            ],
        }
    )
    contract_state = ContractStateProjection(storage)
    contract_rows = contract_state.run(
        publication_ids=["publication-loss-facts"],
        period="2026-03",
    )
    storage.refresh("contract_state", contract_rows.rows)

    monthly_snapshot = MonthlySnapshotProjection(storage)
    snapshot_rows = monthly_snapshot.run(
        publication_ids=["publication-contract-state"],
        period="2026-03",
    )

    assert contract_rows.rows == [
        {
            "company_id": "company-001",
            "plan_code": "P9001",
            "period": "2026-03",
            "has_annuity_performance": True,
            "has_annual_award_fact": False,
            "has_annual_award_fixture": True,
            "has_annual_loss_fact": True,
            "has_annual_loss_fixture": True,
        }
    ]
    assert snapshot_rows.rows == [
        {"period": "2026-03", "contract_state_rows": 1, "award_fixture_rows": 1, "loss_fixture_rows": 1}
    ]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/integration/test_projection_outputs.py -v`
Expected: FAIL because `contract_state` still only reads `fixture_annual_loss`

- [ ] **Step 3: Write minimal implementation**

```python
# src/work_data_hub_pro/capabilities/projections/contract_state.py
        award_fact_rows = self._storage.read("fact_annual_award")
        award_fixture_rows = self._storage.read("fixture_annual_award")
        loss_fact_rows = self._storage.read("fact_annual_loss")
        loss_fixture_rows = self._storage.read("fixture_annual_loss")

        rows: list[dict[str, object]] = []
        for row in performance_rows:
            company_id = row["company_id"]
            plan_code = row["plan_code"]
            has_award_fact = self._has_match(
                award_fact_rows,
                company_id=company_id,
                plan_code=plan_code,
                period=period,
            )
            has_award_fixture = has_award_fact or self._has_match(
                award_fixture_rows,
                company_id=company_id,
                plan_code=plan_code,
                period=period,
            )
            has_loss_fact = self._has_match(
                loss_fact_rows,
                company_id=company_id,
                plan_code=plan_code,
                period=period,
            )
            has_loss_fixture = has_loss_fact or self._has_match(
                loss_fixture_rows,
                company_id=company_id,
                plan_code=plan_code,
                period=period,
            )
            rows.append(
                {
                    "company_id": company_id,
                    "plan_code": plan_code,
                    "period": period,
                    "has_annuity_performance": True,
                    "has_annual_award_fact": has_award_fact,
                    "has_annual_award_fixture": has_award_fixture,
                    "has_annual_loss_fact": has_loss_fact,
                    "has_annual_loss_fixture": has_loss_fixture,
                }
            )
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/integration/test_projection_outputs.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/work_data_hub_pro/capabilities/projections/contract_state.py tests/integration/test_projection_outputs.py
@'
feat(projections): bridge published annual_loss facts into contract_state

Teach the validation projection bridge to consume published `annual_loss` facts
while keeping the snapshot-facing compatibility fields stable for existing
replay baselines.

Validation:
- uv run pytest tests/integration/test_projection_outputs.py -v
'@ | git commit -F -
```

### Task 6: Wire The `annual_loss` Replay Slice And CLI Entry Point

**Files:**
- Create: `src/work_data_hub_pro/apps/orchestration/replay/annual_loss_slice.py`
- Modify: `src/work_data_hub_pro/apps/etl_cli/main.py`
- Test: `tests/replay/test_annual_loss_slice.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/replay/test_annual_loss_slice.py
def test_annual_loss_slice_replay_closes_chain_and_matches_legacy_snapshot(tmp_path) -> None:
    workbook_path = tmp_path / "annual_loss_2026_03.xlsx"
    _write_workbook(workbook_path)
    replay_root = tmp_path / "reference" / "historical_replays" / "annual_loss"
    _write_replay_assets(
        replay_root,
        legacy_snapshot_rows=[
            {"period": "2026-03", "contract_state_rows": 1, "award_fixture_rows": 1, "loss_fixture_rows": 1}
        ],
    )

    outcome = run_annual_loss_slice(
        workbook=workbook_path,
        period="2026-03",
        replay_root=replay_root,
    )

    assert [result.target_name for result in outcome.publication_results] == [
        "fact_annual_loss",
        "company_reference",
        "customer_loss_signal",
        "contract_state",
        "monthly_snapshot",
    ]
    assert [result.projection_name for result in outcome.projection_results] == [
        "contract_state",
        "monthly_snapshot",
    ]
    assert outcome.compatibility_case is None
```

```python
# tests/replay/test_annual_loss_slice.py
def test_annual_loss_slice_replay_creates_compatibility_case_when_snapshot_differs(tmp_path) -> None:
    workbook_path = tmp_path / "annual_loss_2026_03.xlsx"
    _write_workbook(workbook_path)
    replay_root = tmp_path / "reference" / "historical_replays" / "annual_loss"
    _write_replay_assets(
        replay_root,
        legacy_snapshot_rows=[
            {"period": "2026-03", "contract_state_rows": 99, "award_fixture_rows": 99, "loss_fixture_rows": 99}
        ],
    )

    outcome = run_annual_loss_slice(
        workbook=workbook_path,
        period="2026-03",
        replay_root=replay_root,
    )

    assert outcome.compatibility_case is not None
    assert outcome.compatibility_case.involved_anchor_row_nos == [2, 3]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/replay/test_annual_loss_slice.py -v`
Expected: FAIL with `ModuleNotFoundError` for `work_data_hub_pro.apps.orchestration.replay.annual_loss_slice`

- [ ] **Step 3: Write minimal implementation**

```python
# src/work_data_hub_pro/apps/orchestration/replay/annual_loss_slice.py
manifest = CleansingManifest.load(
    release_path=Path("config/releases/2026-04-12-annual-loss-baseline.json"),
    domain_path=Path("config/domains/annual_loss/cleansing.json"),
)
processor = AnnualLossProcessor(manifest)
resolver = CacheFirstIdentityResolutionService(
    cache=InMemoryIdentityCache({}),
    provider=StaticIdentityProvider({"新客流失": "company-002"}),
)
plan_code_enrichment = AnnualLossPlanCodeEnrichmentService(
    CustomerPlanHistoryLookup(_load_rows(replay_root / "customer_plan_history_2026_03.json"))
)
storage = InMemoryTableStore(
    seed={
        "fact_annuity_performance": _load_rows(replay_root / "annuity_performance_fixture_2026_03.json"),
        "fixture_annual_award": _load_rows(replay_root / "annual_award_fixture_2026_03.json"),
    }
)
publication_policy = load_publication_policy(
    Path("config/policies/publication.json"),
    domain="annual_loss",
)
```

```python
# src/work_data_hub_pro/apps/orchestration/replay/annual_loss_slice.py
publication_results = publication.execute(
    [
        PublicationBundle(
            plan=build_publication_plan(
                policy=publication_policy,
                publication_id="publication-loss-facts",
                target_name="fact_annual_loss",
                target_kind="fact",
                refresh_keys=["batch_id"],
                upsert_keys=[],
                source_batch_id=batch.batch_id,
                source_run_id=run_id,
            ),
            rows=[fact.fields | {"record_id": fact.record_id, "batch_id": fact.batch_id} for fact in loss_facts],
        ),
        PublicationBundle(
            plan=build_publication_plan(
                policy=publication_policy,
                publication_id="publication-company-reference",
                target_name="company_reference",
                target_kind="reference",
                refresh_keys=[],
                upsert_keys=["company_id"],
                source_batch_id=batch.batch_id,
                source_run_id=run_id,
            ),
            rows=[candidate.candidate_payload for candidate in derivation_candidates if candidate.target_object == "company_reference"],
        ),
        PublicationBundle(
            plan=build_publication_plan(
                policy=publication_policy,
                publication_id="publication-loss-signal",
                target_name="customer_loss_signal",
                target_kind="reference",
                refresh_keys=[],
                upsert_keys=["company_id", "period"],
                source_batch_id=batch.batch_id,
                source_run_id=run_id,
            ),
            rows=[candidate.candidate_payload for candidate in derivation_candidates if candidate.target_object == "customer_loss_signal"],
        ),
    ]
)
```

```python
# src/work_data_hub_pro/apps/etl_cli/main.py
from work_data_hub_pro.apps.orchestration.replay.annual_loss_slice import (
    run_annual_loss_slice,
)


@app.command("replay-annual-loss")
def replay_annual_loss(
    workbook: Path,
    period: str,
    replay_root: Path = Path("reference/historical_replays/annual_loss"),
) -> None:
    outcome = run_annual_loss_slice(
        workbook=workbook,
        period=period,
        replay_root=replay_root,
    )
    typer.echo(f"publication_results={len(outcome.publication_results)}")
    typer.echo(f"projection_results={len(outcome.projection_results)}")
    typer.echo(f"compatibility_case={outcome.compatibility_case is not None}")
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/replay/test_annual_loss_slice.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/work_data_hub_pro/apps/orchestration/replay/annual_loss_slice.py src/work_data_hub_pro/apps/etl_cli/main.py tests/replay/test_annual_loss_slice.py
@'
feat(apps.orchestration): add annual_loss replay slice

Wire the third executable slice end to end so `annual_loss` closes through
intake, processing, identity, plan-code enrichment, publication, projections,
and compatibility adjudication.

Validation:
- uv run pytest tests/replay/test_annual_loss_slice.py -v
'@ | git commit -F -
```

### Task 7: Add Replay Assets, Runbook, And Explainability Validation

**Files:**
- Create: `reference/historical_replays/annual_loss/annuity_performance_fixture_2026_03.json`
- Create: `reference/historical_replays/annual_loss/annual_award_fixture_2026_03.json`
- Create: `reference/historical_replays/annual_loss/customer_plan_history_2026_03.json`
- Create: `reference/historical_replays/annual_loss/legacy_monthly_snapshot_2026_03.json`
- Create: `docs/runbooks/annual-loss-replay.md`
- Create: `tests/contracts/test_annual_loss_replay_assets.py`
- Create: `tests/replay/test_annual_loss_explainability_slo.py`

- [ ] **Step 1: Write the failing tests**

```python
# tests/contracts/test_annual_loss_replay_assets.py
import json
from pathlib import Path


def test_annual_loss_replay_assets_and_runbook_exist() -> None:
    replay_root = Path("reference/historical_replays/annual_loss")

    assert (replay_root / "annuity_performance_fixture_2026_03.json").exists()
    assert (replay_root / "annual_award_fixture_2026_03.json").exists()
    assert (replay_root / "customer_plan_history_2026_03.json").exists()
    assert (replay_root / "legacy_monthly_snapshot_2026_03.json").exists()
    assert Path("docs/runbooks/annual-loss-replay.md").exists()


def test_annual_loss_customer_plan_history_marks_current_rows() -> None:
    history = json.loads(
        Path(
            "reference/historical_replays/annual_loss/customer_plan_history_2026_03.json"
        ).read_text(encoding="utf-8")
    )

    assert any(row["valid_to"] == "9999-12-31" for row in history)
    assert any(row["valid_to"] != "9999-12-31" for row in history)
```

```python
# tests/replay/test_annual_loss_explainability_slo.py
def test_annual_loss_replay_keeps_primary_evidence_retrieval_inside_five_minutes(
    tmp_path,
) -> None:
    workbook_path = tmp_path / "annual_loss_2026_03.xlsx"
    workbook = Workbook()
    trustee = workbook.active
    trustee.title = "企年受托流失(解约)"
    trustee.append(
        [
            "上报月份",
            "业务类型",
            "计划类型",
            "客户全称",
            "机构",
            "年金计划号",
            "流失日期",
            "计划规模",
            "受托人",
            "company_id",
            "区域",
            "年金中心",
            "上报人",
            "考核标签",
        ]
    )
    investee = workbook.create_sheet("企年投资流失(解约)")
    investee.append(
        [
            "上报月份",
            "业务类型",
            "计划类型",
            "客户全称",
            "机构",
            "年金计划号",
            "流失日期",
            "计划规模",
            "受托人",
            "company_id",
            "区域",
            "年金中心",
            "上报人",
            "考核标签",
        ]
    )
    investee.append(
        [
            "2026年03月",
            "投管",
            "单一",
            "新客流失",
            "未知机构",
            "",
            "2026-03-15",
            "60",
            "原受托机构B",
            "",
            "华东",
            "中心B",
            "测试",
            "drop-me",
        ]
    )
    workbook.save(workbook_path)

    replay_root = tmp_path / "reference" / "historical_replays" / "annual_loss"
    _write_replay_assets(replay_root)

    started = perf_counter()
    run_annual_loss_slice(
        workbook=workbook_path,
        period="2026-03",
        replay_root=replay_root,
    )
    evidence_path = replay_root / "evidence" / "trace" / "annual_loss_2026-03__row_2.json"
    payload = json.loads(evidence_path.read_text(encoding="utf-8"))
    elapsed = perf_counter() - started

    assert evidence_path.exists()
    assert elapsed < 300
    assert any(
        item["stage_id"] == "source_intake"
        and item["value_after"]["source_sheet"] == "企年投资流失(解约)"
        for item in payload
    )
    assert any(
        item["stage_id"] == "fact_processing.plan_code_enrichment"
        and item["value_after"] == "S9009"
        for item in payload
    )
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/contracts/test_annual_loss_replay_assets.py tests/replay/test_annual_loss_explainability_slo.py -v`
Expected: FAIL because the replay assets and runbook are missing

- [ ] **Step 3: Write minimal implementation**

```json
// reference/historical_replays/annual_loss/annuity_performance_fixture_2026_03.json
[
  {
    "record_id": "perf-001",
    "company_id": "company-001",
    "plan_code": "P9001",
    "period": "2026-03",
    "source_record_id": "perf-001"
  }
]
```

```json
// reference/historical_replays/annual_loss/annual_award_fixture_2026_03.json
[
  {
    "company_id": "company-001",
    "plan_code": "P9001",
    "period": "2026-03",
    "award_code": "AWARD-01",
    "source_record_id": "award-001"
  }
]
```

```json
// reference/historical_replays/annual_loss/customer_plan_history_2026_03.json
[
  {
    "company_id": "company-001",
    "product_line_code": "PL202",
    "plan_code": "P9001",
    "effective_period": "2025-12",
    "valid_to": "9999-12-31"
  },
  {
    "company_id": "company-002",
    "product_line_code": "PL201",
    "plan_code": "S9009",
    "effective_period": "2025-12",
    "valid_to": "9999-12-31"
  },
  {
    "company_id": "company-001",
    "product_line_code": "PL202",
    "plan_code": "P7000",
    "effective_period": "2024-12",
    "valid_to": "2025-12-31"
  }
]
```

```json
// reference/historical_replays/annual_loss/legacy_monthly_snapshot_2026_03.json
[
  {
    "period": "2026-03",
    "contract_state_rows": 1,
    "award_fixture_rows": 1,
    "loss_fixture_rows": 1
  }
]
```

````markdown
# docs/runbooks/annual-loss-replay.md
# Annual Loss Replay Runbook

## Goal

Run the `annual_loss` validation slice end to end and determine whether the
`monthly_snapshot` output matches the accepted replay baseline.

## Inputs

- workbook path containing `企年受托流失(解约)` and `企年投资流失(解约)`
- config release `2026-04-12-annual-loss-baseline`
- replay root `reference/historical_replays/annual_loss`

## Command

```bash
uv run python -m work_data_hub_pro.apps.etl_cli.main replay-annual-loss data/annual_loss_2026_03.xlsx 2026-03
```

## Expected Output

- `publication_results=5`
- `projection_results=2`
- `compatibility_case=False`
````

Asset rules for this task:

- derive these JSON artifacts from locked legacy replay extracts, not handwritten synthetic rows
- keep the projection join keys actually used by the current status path: `company_id`, `plan_code`, and `period`
- keep `effective_period` and `valid_to` in `customer_plan_history_2026_03.json` so current-row filtering stays protected by replay assets
- treat the replay-level explainability test as the actual slice acceptance gate for evidence retrieval

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run pytest tests/contracts/test_annual_loss_replay_assets.py tests/replay/test_annual_loss_explainability_slo.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add reference/historical_replays/annual_loss/annuity_performance_fixture_2026_03.json reference/historical_replays/annual_loss/annual_award_fixture_2026_03.json reference/historical_replays/annual_loss/customer_plan_history_2026_03.json reference/historical_replays/annual_loss/legacy_monthly_snapshot_2026_03.json docs/runbooks/annual-loss-replay.md tests/contracts/test_annual_loss_replay_assets.py tests/replay/test_annual_loss_explainability_slo.py
@'
docs(runbooks): add annual_loss replay assets and runbook

Check in the replay fixtures, locked baseline, and operator instructions that
the `annual_loss` slice needs for replay and explainability validation.

Validation:
- uv run pytest tests/contracts/test_annual_loss_replay_assets.py tests/replay/test_annual_loss_explainability_slo.py -v
'@ | git commit -F -
```

### Task 8: Close Phase D Governance For `annual_loss` And Run Full Verification

**Files:**
- Modify: `docs/superpowers/specs/2026-04-11-workdatahubpro-first-wave-legacy-coverage-matrix.md`
- Modify: `docs/superpowers/specs/2026-04-11-workdatahubpro-refactor-program.md`
- Create: `tests/contracts/test_annual_loss_governance_docs.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/contracts/test_annual_loss_governance_docs.py
from pathlib import Path


def test_annual_loss_governance_docs_mark_slice_as_accepted_and_advance_annuity_income() -> None:
    coverage_matrix = Path(
        "docs/superpowers/specs/2026-04-11-workdatahubpro-first-wave-legacy-coverage-matrix.md"
    ).read_text(encoding="utf-8")
    refactor_program = Path(
        "docs/superpowers/specs/2026-04-11-workdatahubpro-refactor-program.md"
    ).read_text(encoding="utf-8")

    assert "| `annual_loss` | accepted breadth-closure slice |" in coverage_matrix
    assert "| AL-001 | multi-sheet loss-domain intake contract |" in coverage_matrix
    assert "| AL-004 | loss fact publication consumed by downstream status rules |" in coverage_matrix
    assert "| 3 | `annual_loss` | accepted breadth-closure slice |" in refactor_program
    assert "| 4 | `annuity_income` | next recommended single-sheet breadth slice |" in refactor_program
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/contracts/test_annual_loss_governance_docs.py -v`
Expected: FAIL because the governance specs still describe `annual_loss` as planned / next recommended

- [ ] **Step 3: Write minimal implementation**

````markdown
# docs/superpowers/specs/2026-04-11-workdatahubpro-first-wave-legacy-coverage-matrix.md
| `annual_loss` | accepted breadth-closure slice | `annuity_income` remains the only unclosed first-wave domain |
| `annuity_income` | next recommended single-sheet breadth slice | no accepted executable slice yet |

| AL-001 | multi-sheet loss-domain intake contract | capability | legacy migration workflow and paired event-domain references | `capabilities/source_intake/annual_loss/service.py` | `capabilities` | architecture blueprint + annual loss slice plan | `accepted` | `tests/integration/test_annual_loss_intake.py`, `tests/replay/test_annual_loss_slice.py` | N/A | merged anchors stay queryable by batch + anchor row |
| AL-002 | canonical loss event transformation | capability | legacy domain behavior and capability-map-equivalent references | `capabilities/fact_processing/annual_loss/` | `capabilities` | architecture blueprint + annual loss slice plan | `accepted` | `tests/integration/test_annual_loss_processing.py`, `tests/replay/test_annual_loss_slice.py` | N/A | governed rule-pack binding and date parsing are explicit |
| AL-003 | identity / plan-code handling for loss rows | mechanism | legacy event-domain behavior | shared identity contract plus loss-specific current-contract lookup | `capabilities` | annual loss slice plan | `accepted` | `tests/integration/test_identity_resolution.py`, `tests/integration/test_annual_loss_plan_code_enrichment.py`, replay evidence | N/A | source company id now wins before cache/provider fallback and current-row lookup keeps `valid_to` filtering explicit |
| AL-004 | loss fact publication consumed by downstream status rules | projection | downstream snapshot dependency implied by current fixtures and blueprint | explicit publication plus projection evidence | `platform` + `capabilities` | annual loss slice plan | `accepted` | `tests/integration/test_projection_outputs.py`, `tests/replay/test_annual_loss_slice.py`, `tests/replay/test_annual_loss_explainability_slo.py` | N/A | the slice replaces fixture-only loss dependency with published fact coverage |

| XD-002 | `annual_loss` facts influence downstream snapshot status triggered by `annuity_performance` | event-domain closure matters for customer status correctness | active dependency | closed by the accepted `annual_loss` slice with published-fact projection coverage |
````

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

- [ ] **Step 4: Run verification**

Run:
- `uv run pytest tests/integration/test_annual_loss_intake.py tests/integration/test_annual_loss_processing.py tests/integration/test_annual_loss_plan_code_enrichment.py tests/integration/test_identity_resolution.py tests/integration/test_reference_derivation.py tests/integration/test_publication_service.py tests/integration/test_projection_outputs.py tests/contracts/test_annual_loss_replay_assets.py tests/contracts/test_annual_loss_governance_docs.py tests/replay/test_annual_loss_slice.py tests/replay/test_annual_loss_explainability_slo.py tests/replay/test_annual_award_slice.py tests/replay/test_annual_award_explainability_slo.py tests/replay/test_annuity_performance_slice.py tests/replay/test_annuity_performance_explainability_slo.py -v`
- `uv run pytest -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add docs/superpowers/specs/2026-04-11-workdatahubpro-first-wave-legacy-coverage-matrix.md docs/superpowers/specs/2026-04-11-workdatahubpro-refactor-program.md tests/contracts/test_annual_loss_governance_docs.py
@'
docs(docs.architecture): close annual_loss slice governance loop

Update the first-wave governance assets so `annual_loss` is explicitly recorded
as accepted and `annuity_income` becomes the unambiguous next breadth slice.

Validation:
- uv run pytest tests/contracts/test_annual_loss_governance_docs.py -v
- uv run pytest -v
'@ | git commit -F -
```

## Self-Review

### Spec Coverage

- The architecture blueprint Sections 3, 5, 6, and 7 are covered by Tasks 1 through 8: the slice closes through multi-sheet intake, governed fact processing, shared identity resolution, explicit publication, projections, runtime evidence, and adjudication.
- The refactor program Section 7 sequencing and Section 8 admission rules are respected by targeting the next recommended slice and closing the paired event-domain dependency path before `annuity_income`.
- Coverage-matrix rows `AL-001` through `AL-004` each map to one or more concrete tasks, tests, replay assets, and final governance updates.
- Cross-domain dependency `XD-002` is handled explicitly by Task 5 and Task 6 instead of staying a fixture-only assumption.
- Production storage, live provider integration, and broader operator tooling stay out of scope so the slice remains aligned with Phase D breadth closure instead of expanding into Phase E.

### Placeholder Scan

- No `TBD`, `TODO`, `implement later`, `fill in details`, or `Similar to Task` placeholders remain.
- Every task contains exact file paths, concrete code, exact commands, and explicit expected outcomes.
- The replay fixtures, governance updates, and runbook paths are named explicitly instead of being left as generic follow-up notes.

### Type Consistency

- Intake identifiers stay consistent across the plan: `batch_id="annual_loss:2026-03"`, merged `anchor_row_no`, and preserved `origin_row_nos`.
- The `annual_loss` release ID stays consistent across config, replay, and runtime wiring: `2026-04-12-annual-loss-baseline`.
- The loss publication targets stay consistent across derivation, publication, replay, and verification tasks: `fact_annual_loss`, `company_reference`, `customer_loss_signal`, `contract_state`, and `monthly_snapshot`.
- The plan-code enrichment stage name stays consistent across tests and implementation: `fact_processing.plan_code_enrichment`.
- Snapshot-facing output keys remain stable across accepted slices while the bridge becomes more explicit: `has_annual_loss_fixture` remains the compatibility field, and `has_annual_loss_fact` is additive.

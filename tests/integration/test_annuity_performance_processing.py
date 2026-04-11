from pathlib import Path

from work_data_hub_pro.capabilities.fact_processing.annuity_performance.service import (
    AnnuityPerformanceProcessor,
)
from work_data_hub_pro.capabilities.fact_processing.cleansing.manifest import (
    CleansingManifest,
)
from work_data_hub_pro.platform.contracts.models import InputRecord


def test_fact_processing_applies_governed_cleansing_and_emits_trace_events() -> None:
    manifest = CleansingManifest.load(
        release_path=Path("config/releases/2026-04-11-annuity-performance-baseline.json"),
        domain_path=Path("config/domains/annuity_performance/cleansing.json"),
    )
    processor = AnnuityPerformanceProcessor(manifest)
    record = InputRecord(
        run_id="run-001",
        record_id="record-001",
        batch_id="annuity_performance:2026-03",
        anchor_row_no=2,
        origin_row_nos=[2],
        parent_record_ids=[],
        stage_row_no=2,
        raw_payload={
            "company_name": "  Acme  ",
            "plan_code": "plan-a",
            "period": "2026-03",
            "sales_amount": "1,200.50",
        },
    )

    result = processor.process(record)

    assert manifest.rule_pack_id == "annuity-performance-core"
    assert manifest.rule_pack_version == "2026.04.11"
    assert result.fact.fields["company_name"] == "ACME"
    assert result.fact.fields["plan_code"] == "PLAN-A"
    assert result.fact.fields["sales_amount"] == 1200.5
    assert [event.field_name for event in result.trace_events] == [
        "company_name",
        "plan_code",
        "sales_amount",
    ]
    assert [event.rule_version for event in result.trace_events] == [
        "2026.04.11.1",
        "2026.04.11.1",
        "2026.04.11.1",
    ]


def test_fact_processing_records_failed_trace_event_when_field_is_missing() -> None:
    manifest = CleansingManifest.load(
        release_path=Path("config/releases/2026-04-11-annuity-performance-baseline.json"),
        domain_path=Path("config/domains/annuity_performance/cleansing.json"),
    )
    processor = AnnuityPerformanceProcessor(manifest)
    record = InputRecord(
        run_id="run-001",
        record_id="record-002",
        batch_id="annuity_performance:2026-03",
        anchor_row_no=2,
        origin_row_nos=[2],
        parent_record_ids=[],
        stage_row_no=2,
        raw_payload={
            "company_name": "  Acme  ",
            "plan_code": "plan-a",
            "period": "2026-03",
        },
    )

    result = processor.process(record)

    assert result.fact.fields["company_name"] == "ACME"
    assert result.fact.fields["plan_code"] == "PLAN-A"
    assert "sales_amount" not in result.fact.fields
    assert result.trace_events[-1].field_name == "sales_amount"
    assert result.trace_events[-1].success is False
    assert result.trace_events[-1].error_message == "missing field: sales_amount"

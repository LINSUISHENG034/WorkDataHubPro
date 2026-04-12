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


def test_annual_loss_processor_normalizes_non_zero_padded_loss_date() -> None:
    manifest = CleansingManifest.load(
        release_path=Path("config/releases/2026-04-12-annual-loss-baseline.json"),
        domain_path=Path("config/domains/annual_loss/cleansing.json"),
    )
    record = InputRecord(
        run_id="run-001",
        record_id="run-001:annual_loss:3",
        batch_id="annual_loss:2026-03",
        anchor_row_no=3,
        origin_row_nos=[3],
        parent_record_ids=[],
        stage_row_no=3,
        raw_payload={
            "上报月份": "2026年03月",
            "业务类型": "投管",
            "计划类型": "集合",
            "客户全称": "  共享客户（流失）  ",
            "机构": "未知机构",
            "年金计划号": None,
            "流失日期": "2026-3-5",
            "受托人": "原受托机构A",
            "company_id": "",
            "source_sheet": "企年投资流失(解约)",
            "source_row_no": 3,
        },
    )

    result = AnnualLossProcessor(manifest).process(record)

    assert result.fact.fields["loss_date"] == "2026-03-05"


def test_annual_loss_processor_refuses_ambiguous_short_loss_date() -> None:
    manifest = CleansingManifest.load(
        release_path=Path("config/releases/2026-04-12-annual-loss-baseline.json"),
        domain_path=Path("config/domains/annual_loss/cleansing.json"),
    )
    record = InputRecord(
        run_id="run-001",
        record_id="run-001:annual_loss:4",
        batch_id="annual_loss:2026-03",
        anchor_row_no=4,
        origin_row_nos=[4],
        parent_record_ids=[],
        stage_row_no=4,
        raw_payload={
            "上报月份": "2026年03月",
            "业务类型": "投管",
            "计划类型": "集合",
            "客户全称": "  共享客户（流失）  ",
            "机构": "未知机构",
            "年金计划号": None,
            "流失日期": "2026031",
            "受托人": "原受托机构A",
            "company_id": "",
            "source_sheet": "企年投资流失(解约)",
            "source_row_no": 4,
        },
    )

    result = AnnualLossProcessor(manifest).process(record)

    assert result.fact.fields["loss_date"] is None

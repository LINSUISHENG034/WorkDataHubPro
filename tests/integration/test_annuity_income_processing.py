from pathlib import Path

from work_data_hub_pro.capabilities.fact_processing.annuity_income.service import (
    AnnuityIncomeProcessor,
)
from work_data_hub_pro.capabilities.fact_processing.cleansing.manifest import (
    CleansingManifest,
)
from work_data_hub_pro.platform.contracts.models import InputRecord


def test_annuity_income_processor_applies_branch_mapping_fee_defaults_and_name_normalization() -> None:
    manifest = CleansingManifest.load(
        release_path=Path("config/releases/2026-04-14-annuity-income-baseline.json"),
        domain_path=Path("config/domains/annuity_income/cleansing.json"),
    )
    record = InputRecord(
        run_id="run-001",
        record_id="run-001:annuity_income:2",
        batch_id="annuity_income:2026-03",
        anchor_row_no=2,
        origin_row_nos=[2],
        parent_record_ids=[],
        stage_row_no=2,
        raw_payload={
            "月度": "2026年03月",
            "业务类型": "职年受托",
            "计划类型": "单一计划",
            "客户名称": "  示例客户  ",
            "机构名称": "北京其他",
            "计划号": "PLAN-A",
            "固费": None,
            "source_sheet": "收入明细",
            "source_row_no": 2,
        },
    )

    result = AnnuityIncomeProcessor(manifest).process(record)

    assert result.fact.domain == "annuity_income"
    assert result.fact.fact_type == "annuity_income"
    assert result.fact.fields["company_name"] == "示例客户"
    assert result.fact.fields["institution_code"] == "G37"
    assert result.fact.fields["fixed_fee"] == 0.0

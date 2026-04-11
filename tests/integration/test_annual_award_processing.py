from pathlib import Path

from work_data_hub_pro.capabilities.fact_processing.annual_award.service import (
    AnnualAwardProcessor,
)
from work_data_hub_pro.capabilities.fact_processing.cleansing.manifest import (
    CleansingManifest,
)
from work_data_hub_pro.platform.contracts.models import InputRecord


def test_annual_award_processor_normalizes_fields_and_business_type() -> None:
    manifest = CleansingManifest.load(
        release_path=Path("config/releases/2026-04-11-annual-award-baseline.json"),
        domain_path=Path("config/domains/annual_award/cleansing.json"),
    )
    record = InputRecord(
        run_id="run-001",
        record_id="run-001:annual_award:2",
        batch_id="annual_award:2026-03",
        anchor_row_no=2,
        origin_row_nos=[2],
        parent_record_ids=[],
        stage_row_no=2,
        raw_payload={
            "company_name": " Acme ",
            "source_company_id": "company-001",
            "plan_code": None,
            "plan_type": " collective ",
            "product_line_code": " pl-ret ",
            "period": "2026-03",
            "award_amount": "5,000.25",
            "source_sheet": "TrusteeAwards",
            "source_row_no": 2,
        },
    )

    result = AnnualAwardProcessor(manifest).process(record)

    assert result.fact.domain == "annual_award"
    assert result.fact.fact_type == "annual_award"
    assert result.fact.fields["company_name"] == "ACME"
    assert result.fact.fields["plan_code"] == ""
    assert result.fact.fields["plan_type"] == "COLLECTIVE"
    assert result.fact.fields["product_line_code"] == "PL-RET"
    assert result.fact.fields["award_amount"] == 5000.25
    assert result.fact.fields["business_type"] == "trustee_award"
    assert len(result.trace_events) == 5

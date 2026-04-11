from openpyxl import Workbook

from work_data_hub_pro.capabilities.source_intake.annual_award.service import (
    AnnualAwardIntakeService,
)


def test_annual_award_intake_merges_sheet_rows_into_stable_anchor_sequence(
    tmp_path,
) -> None:
    workbook_path = tmp_path / "annual_award_2026_03.xlsx"
    workbook = Workbook()
    trustee = workbook.active
    trustee.title = "TrusteeAwards"
    trustee.append(
        [
            "company_name",
            "source_company_id",
            "plan_code",
            "plan_type",
            "product_line_code",
            "period",
            "award_amount",
        ]
    )
    trustee.append(
        ["Acme", "company-001", "", "collective", "pl-ret", "2026-03", "5000"]
    )
    investee = workbook.create_sheet("InvesteeAwards")
    investee.append(
        [
            "company_name",
            "source_company_id",
            "plan_code",
            "plan_type",
            "product_line_code",
            "period",
            "award_amount",
        ]
    )
    investee.append(["Beta", "", "", "single", "pl-alt", "2026-03", "1000"])
    workbook.save(workbook_path)

    result = AnnualAwardIntakeService().read_batch(
        run_id="run-001",
        period="2026-03",
        source_files=[workbook_path],
    )

    assert result.batch.batch_id == "annual_award:2026-03"
    assert result.batch.row_count == 2
    assert [record.anchor_row_no for record in result.records] == [2, 3]
    assert [record.origin_row_nos for record in result.records] == [[2], [2]]
    assert [record.raw_payload["source_sheet"] for record in result.records] == [
        "TrusteeAwards",
        "InvesteeAwards",
    ]
    assert [record.raw_payload["source_row_no"] for record in result.records] == [2, 2]

from openpyxl import Workbook

from work_data_hub_pro.capabilities.source_intake.annuity_income.service import (
    AnnuityIncomeIntakeService,
)


def test_annuity_income_intake_reads_income_sheet_and_preserves_anchor_rows(
    tmp_path,
) -> None:
    workbook_path = tmp_path / "annuity_income_2026_03.xlsx"
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "收入明细"
    sheet.append(
        [
            "月度",
            "机构",
            "机构名称",
            "计划号",
            "客户名称",
            "业务类型",
            "计划类型",
        ]
    )
    sheet.append(
        [
            "2026年03月",
            "",
            "北京其他",
            "PLAN-A",
            "示例客户",
            "职年受托",
            "单一计划",
        ]
    )
    workbook.save(workbook_path)

    result = AnnuityIncomeIntakeService().read_batch(
        run_id="run-001",
        period="2026-03",
        source_files=[workbook_path],
    )

    assert result.batch.batch_id == "annuity_income:2026-03"
    assert result.batch.row_count == 1
    assert [record.anchor_row_no for record in result.records] == [2]
    assert result.records[0].raw_payload["机构名称"] == "北京其他"
    assert result.records[0].raw_payload["source_row_no"] == 2

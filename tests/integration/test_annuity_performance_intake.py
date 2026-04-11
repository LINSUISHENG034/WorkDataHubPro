from openpyxl import Workbook

from work_data_hub_pro.capabilities.source_intake.annuity_performance.service import (
    AnnuityPerformanceIntakeService,
)


def test_annuity_performance_intake_builds_anchor_preserving_records(tmp_path) -> None:
    workbook_path = tmp_path / "annuity_performance_2026_03.xlsx"
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "AnnuityPerformance"
    sheet.append(["company_name", "plan_code", "period", "sales_amount"])
    sheet.append(["Acme", "PLAN-A", "2026-03", 1200.5])
    workbook.save(workbook_path)

    service = AnnuityPerformanceIntakeService()
    result = service.read_batch(
        run_id="run-001",
        period="2026-03",
        source_files=[workbook_path],
    )

    assert result.batch.batch_id == "annuity_performance:2026-03"
    assert result.batch.row_count == 1
    assert result.records[0].anchor_row_no == 2
    assert result.records[0].origin_row_nos == [2]
    assert result.records[0].raw_payload["company_name"] == "Acme"
    assert result.trace_events[0].stage_id == "source_intake"
    assert result.trace_events[0].field_name == "raw_payload"
    assert result.trace_events[0].anchor_row_no == 2

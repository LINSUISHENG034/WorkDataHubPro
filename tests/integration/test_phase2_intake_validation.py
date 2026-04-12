from __future__ import annotations

from pathlib import Path

import pytest
from openpyxl import Workbook

from work_data_hub_pro.capabilities.source_intake.annuity_performance.service import (
    AnnuityPerformanceIntakeService,
)


def _write_workbook(
    path: Path,
    *,
    headers: list[str],
    rows: list[list[object]],
) -> None:
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "AnnuityPerformance"
    sheet.append(headers)
    for row in rows:
        sheet.append(row)
    workbook.save(path)


def test_annuity_intake_accepts_aliases_and_records_adaptation(tmp_path) -> None:
    workbook_path = tmp_path / "annuity_performance_real_style.xlsx"
    _write_workbook(
        workbook_path,
        headers=[
            "月度",
            "业务类型",
            "客户名称",
            "计划类型",
            "期末资产规模",
            "额外备注",
        ],
        rows=[["2026-03", "受托", "Acme", "集合", "1200.50", "drop-me"]],
    )

    result = AnnuityPerformanceIntakeService().read_batch(
        run_id="run-001",
        period="2026-03",
        source_files=[workbook_path],
    )

    record = result.records[0]
    adaptation = record.raw_payload["source_intake_adaptation"]

    assert record.raw_payload["period"] == "2026-03"
    assert record.raw_payload["business_type"] == "受托"
    assert record.raw_payload["company_name"] == "Acme"
    assert record.raw_payload["plan_type"] == "集合"
    assert record.raw_payload["ending_assets"] == "1200.50"
    assert record.raw_payload["sales_amount"] == "1200.50"
    assert adaptation["aliases_applied"]["月度"] == "period"
    assert adaptation["aliases_applied"]["期末资产规模"] == "ending_assets"
    assert adaptation["ignored_columns"] == ["额外备注"]
    assert "plan_code" in adaptation["missing_non_golden_columns"]


def test_annuity_intake_rejects_missing_minimum_skeleton(tmp_path) -> None:
    workbook_path = tmp_path / "annuity_performance_invalid.xlsx"
    _write_workbook(
        workbook_path,
        headers=["月度", "客户名称", "计划类型"],
        rows=[["2026-03", "Acme", "集合"]],
    )

    with pytest.raises(ValueError, match="business_type|ending_assets"):
        AnnuityPerformanceIntakeService().read_batch(
            run_id="run-001",
            period="2026-03",
            source_files=[workbook_path],
        )

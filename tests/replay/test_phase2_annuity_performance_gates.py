from __future__ import annotations

import json
from pathlib import Path

from openpyxl import Workbook

from work_data_hub_pro.apps.orchestration.replay.annuity_performance_slice import (
    run_annuity_performance_slice,
)
from tests.replay.test_annuity_performance_slice import _bootstrap_intermediate_baselines


def _write_workbook(path: Path) -> None:
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "AnnuityPerformance"
    sheet.append(["company_name", "plan_code", "period", "sales_amount"])
    sheet.append(["Acme", "PLAN-A", "2026-03", "1200.50"])
    workbook.save(path)


def _write_replay_assets(
    replay_root: Path,
    *,
    legacy_snapshot_rows: list[dict[str, object]],
) -> None:
    replay_root.mkdir(parents=True, exist_ok=True)
    (replay_root / "annual_award_fixture_2026_03.json").write_text(
        json.dumps(
            [
                {
                    "company_id": "company-001",
                    "plan_code": "PLAN-A",
                    "period": "2026-03",
                    "award_code": "AWARD-01",
                    "source_sheet": "AwardRegister",
                    "source_record_id": "award-001",
                }
            ],
            indent=2,
        ),
        encoding="utf-8",
    )
    (replay_root / "annual_loss_fixture_2026_03.json").write_text(
        json.dumps(
            [
                {
                    "company_id": "company-001",
                    "plan_code": "PLAN-Z",
                    "period": "2026-03",
                    "loss_code": "LOSS-99",
                    "source_sheet": "LossRegister",
                    "source_record_id": "loss-001",
                }
            ],
            indent=2,
        ),
        encoding="utf-8",
    )
    (replay_root / "legacy_monthly_snapshot_2026_03.json").write_text(
        json.dumps(legacy_snapshot_rows, indent=2),
        encoding="utf-8",
    )


def test_annuity_gate_passes(tmp_path) -> None:
    workbook_path = tmp_path / "annuity_performance_2026_03.xlsx"
    _write_workbook(workbook_path)
    replay_root = tmp_path / "reference" / "historical_replays" / "annuity_performance"
    _write_replay_assets(
        replay_root,
        legacy_snapshot_rows=[
            {
                "period": "2026-03",
                "contract_state_rows": 1,
                "award_fixture_rows": 1,
                "loss_fixture_rows": 0,
            }
        ],
    )
    _bootstrap_intermediate_baselines(workbook_path, replay_root)

    outcome = run_annuity_performance_slice(
        workbook=workbook_path,
        period="2026-03",
        replay_root=replay_root,
    )

    assert outcome.gate_summary.overall_outcome == "passed"
    assert outcome.gate_summary.status_counts["passed"] == 6
    assert outcome.compatibility_case is None


def test_annuity_gate_writes_failed_package(tmp_path) -> None:
    workbook_path = tmp_path / "annuity_performance_2026_03.xlsx"
    _write_workbook(workbook_path)
    replay_root = tmp_path / "reference" / "historical_replays" / "annuity_performance"
    _write_replay_assets(
        replay_root,
        legacy_snapshot_rows=[
            {
                "period": "2026-03",
                "contract_state_rows": 99,
                "award_fixture_rows": 99,
                "loss_fixture_rows": 99,
            }
        ],
    )
    _bootstrap_intermediate_baselines(workbook_path, replay_root)

    outcome = run_annuity_performance_slice(
        workbook=workbook_path,
        period="2026-03",
        replay_root=replay_root,
    )

    package_root = (
        replay_root / "evidence" / "comparison_runs" / outcome.comparison_run_id
    )

    assert outcome.gate_summary.overall_outcome == "failed"
    assert outcome.compatibility_case is not None
    assert (package_root / "manifest.json").exists()
    assert (package_root / "gate-summary.json").exists()
    assert (package_root / "checkpoint-results.json").exists()
    assert (package_root / "source-intake-adaptation.json").exists()
    assert (package_root / "lineage-impact.json").exists()
    assert (package_root / "publication-results.json").exists()
    assert (package_root / "compatibility-case.json").exists()
    assert (package_root / "report.md").exists()
    assert (package_root / "diffs" / "monthly_snapshot.json").exists()

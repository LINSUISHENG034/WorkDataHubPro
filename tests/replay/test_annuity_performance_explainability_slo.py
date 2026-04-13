import json
from pathlib import Path
from time import perf_counter

from openpyxl import Workbook

from work_data_hub_pro.apps.orchestration.replay.annuity_performance_slice import (
    run_annuity_performance_slice,
)
from tests.replay.test_annuity_performance_slice import _bootstrap_intermediate_baselines


def _write_replay_assets(replay_root: Path) -> None:
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
        json.dumps(
            [
                {
                    "period": "2026-03",
                    "contract_state_rows": 1,
                    "award_fixture_rows": 1,
                    "loss_fixture_rows": 0,
                }
            ],
            indent=2,
        ),
        encoding="utf-8",
    )


def test_full_replay_keeps_primary_evidence_retrieval_inside_five_minutes(tmp_path) -> None:
    workbook_path = tmp_path / "annuity_performance_2026_03.xlsx"
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "AnnuityPerformance"
    sheet.append(["company_name", "plan_code", "period", "sales_amount"])
    sheet.append(["Acme", "PLAN-A", "2026-03", "1200.50"])
    workbook.save(workbook_path)

    replay_root = tmp_path / "reference" / "historical_replays" / "annuity_performance"
    _write_replay_assets(replay_root)
    _bootstrap_intermediate_baselines(workbook_path, replay_root)

    started = perf_counter()
    run_annuity_performance_slice(
        workbook=workbook_path,
        period="2026-03",
        replay_root=replay_root,
    )
    evidence_path = (
        replay_root / "evidence" / "trace" / "annuity_performance_2026-03__row_2.json"
    )
    payload = json.loads(evidence_path.read_text(encoding="utf-8"))
    elapsed = perf_counter() - started

    assert evidence_path.exists()
    assert elapsed < 300
    assert any(item["stage_id"] == "source_intake" for item in payload)
    assert any(item["stage_id"] == "identity_resolution" for item in payload)
    assert any(item["value_before"] != item["value_after"] for item in payload)

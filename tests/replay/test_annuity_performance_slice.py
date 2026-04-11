import json
from pathlib import Path

from openpyxl import Workbook

from work_data_hub_pro.apps.orchestration.replay.annuity_performance_slice import (
    run_annuity_performance_slice,
)


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


def test_full_slice_replay_closes_chain_and_matches_legacy_snapshot(tmp_path) -> None:
    workbook_path = tmp_path / "annuity_performance_2026_03.xlsx"
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "AnnuityPerformance"
    sheet.append(["company_name", "plan_code", "period", "sales_amount"])
    sheet.append(["Acme", "PLAN-A", "2026-03", "1200.50"])
    workbook.save(workbook_path)

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

    outcome = run_annuity_performance_slice(
        workbook=workbook_path,
        period="2026-03",
        replay_root=replay_root,
    )

    assert [result.target_name for result in outcome.publication_results] == [
        "fact_annuity_performance",
        "company_reference",
        "contract_state",
        "monthly_snapshot",
    ]
    assert [result.projection_name for result in outcome.projection_results] == [
        "contract_state",
        "monthly_snapshot",
    ]
    assert outcome.compatibility_case is None
    row_events = outcome.trace_store.find(
        batch_id="annuity_performance:2026-03",
        anchor_row_no=2,
    )
    assert {event.stage_id for event in row_events} == {
        "source_intake",
        "fact_processing",
        "identity_resolution",
    }
    lineage_links = outcome.lineage_registry.all()
    assert len(lineage_links) == 1
    assert lineage_links[0].origin_row_nos == [2]
    assert lineage_links[0].anchor_row_no == 2
    assert lineage_links[0].parent_record_ids == [row_events[0].record_id]


def test_full_slice_replay_creates_compatibility_case_when_snapshot_differs(tmp_path) -> None:
    workbook_path = tmp_path / "annuity_performance_2026_03.xlsx"
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "AnnuityPerformance"
    sheet.append(["company_name", "plan_code", "period", "sales_amount"])
    sheet.append(["Acme", "PLAN-A", "2026-03", "1200.50"])
    workbook.save(workbook_path)

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

    outcome = run_annuity_performance_slice(
        workbook=workbook_path,
        period="2026-03",
        replay_root=replay_root,
    )

    assert outcome.compatibility_case is not None
    case_path = (
        replay_root
        / "evidence"
        / "compatibility_cases"
        / f"{outcome.compatibility_case.case_id}.json"
    )
    assert case_path.exists()

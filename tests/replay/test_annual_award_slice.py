import json
from pathlib import Path

from openpyxl import Workbook

from work_data_hub_pro.apps.orchestration.replay.annual_award_slice import (
    run_annual_award_slice,
)


def _write_replay_assets(
    replay_root: Path,
    *,
    legacy_snapshot_rows: list[dict[str, object]],
) -> None:
    replay_root.mkdir(parents=True, exist_ok=True)
    (replay_root / "annuity_performance_fixture_2026_03.json").write_text(
        json.dumps(
            [
                {
                    "record_id": "perf-001",
                    "company_id": "company-001",
                    "plan_code": "P9001",
                    "period": "2026-03",
                    "source_record_id": "perf-001",
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
                    "plan_code": "LOSS-99",
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
    (replay_root / "customer_plan_history_2026_03.json").write_text(
        json.dumps(
            [
                {
                    "company_id": "company-001",
                    "product_line_code": "PL-RET",
                    "plan_code": "P9001",
                    "effective_period": "2025-12",
                },
                {
                    "company_id": "company-002",
                    "product_line_code": "PL-ALT",
                    "plan_code": "S9009",
                    "effective_period": "2025-12",
                },
            ],
            indent=2,
        ),
        encoding="utf-8",
    )
    (replay_root / "legacy_monthly_snapshot_2026_03.json").write_text(
        json.dumps(legacy_snapshot_rows, indent=2),
        encoding="utf-8",
    )


def _write_workbook(workbook_path: Path) -> None:
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


def test_annual_award_slice_replay_closes_chain_and_matches_legacy_snapshot(
    tmp_path,
) -> None:
    workbook_path = tmp_path / "annual_award_2026_03.xlsx"
    _write_workbook(workbook_path)
    replay_root = tmp_path / "reference" / "historical_replays" / "annual_award"
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

    outcome = run_annual_award_slice(
        workbook=workbook_path,
        period="2026-03",
        replay_root=replay_root,
    )

    assert [result.target_name for result in outcome.publication_results] == [
        "fact_annual_award",
        "company_reference",
        "customer_master_signal",
        "contract_state",
        "monthly_snapshot",
    ]
    assert [result.projection_name for result in outcome.projection_results] == [
        "contract_state",
        "monthly_snapshot",
    ]
    assert outcome.compatibility_case is None
    row_events = outcome.trace_store.find(
        batch_id="annual_award:2026-03",
        anchor_row_no=3,
    )
    assert {event.stage_id for event in row_events} == {
        "source_intake",
        "fact_processing",
        "identity_resolution",
        "fact_processing.plan_code_enrichment",
    }
    assert [link.anchor_row_no for link in outcome.lineage_registry.all()] == [2, 3]


def test_annual_award_slice_replay_creates_compatibility_case_when_snapshot_differs(
    tmp_path,
) -> None:
    workbook_path = tmp_path / "annual_award_2026_03.xlsx"
    _write_workbook(workbook_path)
    replay_root = tmp_path / "reference" / "historical_replays" / "annual_award"
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

    outcome = run_annual_award_slice(
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

import json
from pathlib import Path
from time import perf_counter

from openpyxl import Workbook

from work_data_hub_pro.apps.orchestration.replay.annual_award_slice import (
    run_annual_award_slice,
)


def _write_replay_assets(replay_root: Path) -> None:
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
        json.dumps([], indent=2),
        encoding="utf-8",
    )
    (replay_root / "customer_plan_history_2026_03.json").write_text(
        json.dumps(
            [
                {
                    "company_id": "company-002",
                    "product_line_code": "PL-ALT",
                    "plan_code": "S9009",
                    "effective_period": "2025-12",
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
                    "award_fixture_rows": 0,
                    "loss_fixture_rows": 0,
                }
            ],
            indent=2,
        ),
        encoding="utf-8",
    )


def test_annual_award_replay_keeps_primary_evidence_retrieval_inside_five_minutes(
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

    replay_root = tmp_path / "reference" / "historical_replays" / "annual_award"
    _write_replay_assets(replay_root)

    started = perf_counter()
    run_annual_award_slice(
        workbook=workbook_path,
        period="2026-03",
        replay_root=replay_root,
    )
    evidence_path = replay_root / "evidence" / "trace" / "annual_award_2026-03__row_2.json"
    payload = json.loads(evidence_path.read_text(encoding="utf-8"))
    elapsed = perf_counter() - started

    assert evidence_path.exists()
    assert elapsed < 300
    assert any(
        item["stage_id"] == "source_intake"
        and item["value_after"]["source_sheet"] == "InvesteeAwards"
        for item in payload
    )
    assert any(
        item["stage_id"] == "fact_processing.plan_code_enrichment"
        and item["value_after"] == "S9009"
        for item in payload
    )

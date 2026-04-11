import json
from pathlib import Path


def test_annual_award_replay_assets_and_runbook_exist() -> None:
    replay_root = Path("reference/historical_replays/annual_award")

    assert (replay_root / "annuity_performance_fixture_2026_03.json").exists()
    assert (replay_root / "annual_loss_fixture_2026_03.json").exists()
    assert (replay_root / "customer_plan_history_2026_03.json").exists()
    assert (replay_root / "legacy_monthly_snapshot_2026_03.json").exists()
    assert Path("docs/runbooks/annual-award-replay.md").exists()


def test_annual_award_replay_assets_match_accepted_baseline() -> None:
    replay_root = Path("reference/historical_replays/annual_award")

    annuity_performance_fixture = json.loads(
        (replay_root / "annuity_performance_fixture_2026_03.json").read_text(
            encoding="utf-8"
        )
    )
    annual_loss_fixture = json.loads(
        (replay_root / "annual_loss_fixture_2026_03.json").read_text(encoding="utf-8")
    )
    customer_plan_history = json.loads(
        (replay_root / "customer_plan_history_2026_03.json").read_text(
            encoding="utf-8"
        )
    )
    legacy_snapshot = json.loads(
        (replay_root / "legacy_monthly_snapshot_2026_03.json").read_text(
            encoding="utf-8"
        )
    )

    assert annuity_performance_fixture == [
        {
            "record_id": "perf-001",
            "company_id": "company-001",
            "plan_code": "P9001",
            "period": "2026-03",
            "source_record_id": "perf-001",
        }
    ]
    assert annual_loss_fixture == [
        {
            "company_id": "company-001",
            "plan_code": "LOSS-99",
            "period": "2026-03",
            "loss_code": "LOSS-99",
            "source_sheet": "LossRegister",
            "source_record_id": "loss-001",
        }
    ]
    assert customer_plan_history == [
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
    ]
    assert legacy_snapshot == [
        {
            "period": "2026-03",
            "contract_state_rows": 1,
            "award_fixture_rows": 1,
            "loss_fixture_rows": 0,
        }
    ]

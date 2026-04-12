import json
from pathlib import Path


def test_annual_loss_replay_assets_and_runbook_exist() -> None:
    replay_root = Path("reference/historical_replays/annual_loss")

    assert (replay_root / "annuity_performance_fixture_2026_03.json").exists()
    assert (replay_root / "annual_award_fixture_2026_03.json").exists()
    assert (replay_root / "customer_plan_history_2026_03.json").exists()
    assert (replay_root / "legacy_monthly_snapshot_2026_03.json").exists()
    assert Path("docs/runbooks/annual-loss-replay.md").exists()


def test_annual_loss_customer_plan_history_marks_current_rows() -> None:
    replay_root = Path("reference/historical_replays/annual_loss")
    annuity_fixture = json.loads(
        (replay_root / "annuity_performance_fixture_2026_03.json").read_text(
            encoding="utf-8"
        )
    )
    award_fixture = json.loads(
        (replay_root / "annual_award_fixture_2026_03.json").read_text(
            encoding="utf-8"
        )
    )
    snapshot = json.loads(
        (replay_root / "legacy_monthly_snapshot_2026_03.json").read_text(
            encoding="utf-8"
        )
    )
    history = json.loads(
        (replay_root / "customer_plan_history_2026_03.json").read_text(
            encoding="utf-8"
        )
    )

    for row in annuity_fixture:
        assert {"company_id", "plan_code", "period"} <= row.keys()
    for row in award_fixture:
        assert {"company_id", "plan_code", "period"} <= row.keys()
    for row in snapshot:
        assert {"period", "contract_state_rows", "award_fixture_rows", "loss_fixture_rows"} <= row.keys()
    for row in history:
        assert {"company_id", "plan_code", "effective_period", "valid_to"} <= row.keys()
    assert any(row["valid_to"] == "9999-12-31" for row in history)
    assert any(row["valid_to"] != "9999-12-31" for row in history)

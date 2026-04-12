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
    history = json.loads(
        Path(
            "reference/historical_replays/annual_loss/customer_plan_history_2026_03.json"
        ).read_text(encoding="utf-8")
    )

    assert any(row["valid_to"] == "9999-12-31" for row in history)
    assert any(row["valid_to"] != "9999-12-31" for row in history)

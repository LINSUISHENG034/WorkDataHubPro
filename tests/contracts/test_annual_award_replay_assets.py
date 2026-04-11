from pathlib import Path


def test_annual_award_replay_assets_and_runbook_exist() -> None:
    replay_root = Path("reference/historical_replays/annual_award")

    assert (replay_root / "annuity_performance_fixture_2026_03.json").exists()
    assert (replay_root / "annual_loss_fixture_2026_03.json").exists()
    assert (replay_root / "customer_plan_history_2026_03.json").exists()
    assert (replay_root / "legacy_monthly_snapshot_2026_03.json").exists()
    assert Path("docs/runbooks/annual-award-replay.md").exists()

from pathlib import Path


def test_replay_assets_and_runbook_exist_for_annuity_performance_slice() -> None:
    replay_root = Path("reference/historical_replays/annuity_performance")

    assert (replay_root / "annual_award_fixture_2026_03.json").exists()
    assert (replay_root / "annual_loss_fixture_2026_03.json").exists()
    assert (replay_root / "legacy_monthly_snapshot_2026_03.json").exists()

    runbook = Path("docs/runbooks/annuity-performance-replay.md")
    assert runbook.exists()
    contents = runbook.read_text(encoding="utf-8")
    assert "replay-annuity-performance" in contents
    assert "compatibility_case=False" in contents

import json
from pathlib import Path


def test_annuity_income_replay_assets_and_runbook_exist() -> None:
    replay_root = Path("reference/historical_replays/annuity_income")

    assert (replay_root / "legacy_fact_processing_2026_03.json").exists()
    assert (replay_root / "legacy_identity_resolution_2026_03.json").exists()
    assert (replay_root / "legacy_reference_derivation_2026_03.json").exists()
    assert (replay_root / "legacy_operator_artifacts_2026_03.json").exists()
    assert Path("docs/runbooks/annuity-income-replay.md").exists()


def test_annuity_income_operator_artifact_baseline_marks_visibility_contract() -> None:
    replay_root = Path("reference/historical_replays/annuity_income")
    operator_artifacts = json.loads(
        (replay_root / "legacy_operator_artifacts_2026_03.json").read_text(
            encoding="utf-8"
        )
    )

    assert operator_artifacts
    assert {"record_id", "unknown_names_csv", "failed_records_csv"} <= operator_artifacts[0].keys()

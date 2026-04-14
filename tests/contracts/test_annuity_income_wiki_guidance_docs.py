from pathlib import Path


def test_annuity_income_wiki_pages_now_reference_implementation_backing() -> None:
    branch_mapping = Path(
        "docs/wiki-bi/evidence/annuity-income-branch-mapping-evidence.md"
    ).read_text(encoding="utf-8")
    id5_retirement = Path(
        "docs/wiki-bi/evidence/annuity-income-id5-retirement-evidence.md"
    ).read_text(encoding="utf-8")
    operator_artifacts = Path(
        "docs/wiki-bi/evidence/annuity-income-operator-artifacts-evidence.md"
    ).read_text(encoding="utf-8")
    annuity_income_domain = Path("docs/wiki-bi/domains/annuity-income.md").read_text(
        encoding="utf-8"
    )
    wiki_log = Path("docs/wiki-bi/log.md").read_text(encoding="utf-8")

    assert "tests/integration/test_annuity_income_processing.py" in branch_mapping
    assert "config/domains/annuity_income/cleansing.json" in branch_mapping

    assert "tests/integration/test_annuity_income_operator_artifacts.py" in id5_retirement
    assert "reference/historical_replays/annuity_income/legacy_identity_resolution_2026_03.json" in id5_retirement

    assert "tests/contracts/test_annuity_income_replay_assets.py" in operator_artifacts
    assert "docs/runbooks/annuity-income-replay.md" in operator_artifacts
    assert "tests/replay/test_annuity_income_slice.py" in operator_artifacts

    assert "当前 current project 已有显式 validation slice、runbook、replay assets 与 targeted tests" in annuity_income_domain
    assert "wiki-guided implementation loop" in wiki_log

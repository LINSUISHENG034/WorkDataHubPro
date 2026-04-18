from pathlib import Path


def test_shared_unresolved_artifact_wiki_docs_are_reachable() -> None:
    shared_evidence = Path(
        "docs/wiki-bi/evidence/unresolved-name-and-failed-record-evidence.md"
    ).read_text(encoding="utf-8")
    unknown_names = Path("docs/wiki-bi/surfaces/unknown-names-csv.md").read_text(
        encoding="utf-8"
    )
    failed_record = Path("docs/wiki-bi/surfaces/failed-record-export.md").read_text(
        encoding="utf-8"
    )
    queue_surface = Path("docs/wiki-bi/surfaces/company-lookup-queue.md").read_text(
        encoding="utf-8"
    )
    wiki_index = Path("docs/wiki-bi/index.md").read_text(encoding="utf-8")

    assert "unknown_names_csv" in shared_evidence
    assert "failed-record export" in shared_evidence
    assert "annuity_income" in shared_evidence

    assert "unresolved-name-and-failed-record-evidence.md" in unknown_names
    assert "unresolved-name-and-failed-record-evidence.md" in failed_record
    assert "unresolved-name-and-failed-record-evidence.md" in queue_surface
    assert "unresolved-name-and-failed-record-evidence.md" in wiki_index

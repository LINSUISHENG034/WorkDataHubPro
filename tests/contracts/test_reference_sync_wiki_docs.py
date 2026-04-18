from pathlib import Path


def test_reference_sync_wiki_docs_are_reachable() -> None:
    evidence_page = Path(
        "docs/wiki-bi/evidence/reference-sync-runtime-and-state-evidence.md"
    ).read_text(encoding="utf-8")
    surface_page = Path("docs/wiki-bi/surfaces/reference-sync.md").read_text(
        encoding="utf-8"
    )
    wiki_index = Path("docs/wiki-bi/index.md").read_text(encoding="utf-8")

    assert "target inventory" in evidence_page
    assert "last_synced_at" in evidence_page
    assert "reference_derivation -> publication" in evidence_page

    assert "reference-sync-runtime-and-state-evidence.md" in surface_page
    assert "reference-sync-runtime-and-state-evidence.md" in wiki_index

from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SEMANTIC_MAP_ROOT = REPO_ROOT / "docs" / "wiki-bi" / "_meta" / "legacy-semantic-map"


def test_semantic_map_repo_docs_are_governed() -> None:
    assert SEMANTIC_MAP_ROOT.is_dir()

    expected_paths = [
        SEMANTIC_MAP_ROOT / "README.md",
        SEMANTIC_MAP_ROOT / "manifest.json",
        SEMANTIC_MAP_ROOT / "execution" / "entry-surfaces.yaml",
        SEMANTIC_MAP_ROOT / "execution" / "paths" / ".gitkeep",
        SEMANTIC_MAP_ROOT / "execution" / "stages" / ".gitkeep",
        SEMANTIC_MAP_ROOT / "sources" / "families.yaml",
        SEMANTIC_MAP_ROOT / "waves" / "index.yaml",
        SEMANTIC_MAP_ROOT / "subsystems" / ".gitkeep",
        SEMANTIC_MAP_ROOT / "objects" / ".gitkeep",
    ]
    for path in expected_paths:
        assert path.exists(), f"Expected semantic-map bootstrap artifact at {path}"

    manifest = json.loads((SEMANTIC_MAP_ROOT / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["canonical_seed_sources"] == [
        "execution/entry-surfaces.yaml",
        "sources/families.yaml",
        "waves/index.yaml",
    ]

    readme_text = (SEMANTIC_MAP_ROOT / "README.md").read_text(encoding="utf-8")
    assert "internal discovery ledger" in readme_text
    assert "not durable wiki content" in readme_text
    assert "active owner:" in readme_text
    assert "archive trigger:" in readme_text

    wiki_index_text = (REPO_ROOT / "docs" / "wiki-bi" / "index.md").read_text(encoding="utf-8")
    assert "legacy-semantic-map" not in wiki_index_text

    lint_checklist_text = (
        REPO_ROOT / "docs" / "wiki-bi" / "_meta" / "wiki-maintenance-lint-checklist.md"
    ).read_text(encoding="utf-8")
    assert "docs/wiki-bi/_meta/legacy-semantic-map/" in lint_checklist_text
    assert "excluded from durable-page reachability and template checks" in lint_checklist_text
    assert "still remains absent from `docs/wiki-bi/index.md`" in lint_checklist_text
    assert "owner, archive trigger, and non-durable boundary" in lint_checklist_text

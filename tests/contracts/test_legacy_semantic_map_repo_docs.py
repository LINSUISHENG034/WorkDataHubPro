from __future__ import annotations

import json
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[2]
SEMANTIC_MAP_ROOT = REPO_ROOT / "docs" / "wiki-bi" / "_meta" / "legacy-semantic-map"


def test_semantic_map_repo_docs_are_governed() -> None:
    assert SEMANTIC_MAP_ROOT.is_dir()

    expected_paths = [
        SEMANTIC_MAP_ROOT / "AGENTS.md",
        SEMANTIC_MAP_ROOT / "README.md",
        SEMANTIC_MAP_ROOT / "manifest.json",
        SEMANTIC_MAP_ROOT / "execution" / "entry-surfaces.yaml",
        SEMANTIC_MAP_ROOT
        / "execution"
        / "paths"
        / "ep-manual-cli-entrypoints-annuity-performance-manual-entry.yaml",
        SEMANTIC_MAP_ROOT / "execution" / "stages" / ".gitkeep",
        SEMANTIC_MAP_ROOT / "sources" / "families.yaml",
        SEMANTIC_MAP_ROOT / "waves" / "index.yaml",
        SEMANTIC_MAP_ROOT / "reports" / "current" / "coverage-status.json",
        SEMANTIC_MAP_ROOT / "reports" / "current" / "integrity-status.json",
        SEMANTIC_MAP_ROOT
        / "reports"
        / "waves"
        / "wave-2026-04-17-first-wave-pilot"
        / "coverage-status.json",
        SEMANTIC_MAP_ROOT
        / "reports"
        / "waves"
        / "wave-2026-04-17-first-wave-pilot"
        / "integrity-status.json",
        SEMANTIC_MAP_ROOT
        / "reports"
        / "waves"
        / "wave-2026-04-17-semantic-governance-reframe"
        / "coverage-status.json",
        SEMANTIC_MAP_ROOT
        / "reports"
        / "waves"
        / "wave-2026-04-17-semantic-governance-reframe"
        / "integrity-status.json",
        SEMANTIC_MAP_ROOT
        / "reports"
        / "waves"
        / "wave-2026-04-17-semantic-governance-reframe"
        / "semantic-discovery-status.json",
        SEMANTIC_MAP_ROOT
        / "reports"
        / "waves"
        / "wave-2026-04-17-semantic-governance-reframe"
        / "semantic-readiness-status.json",
        SEMANTIC_MAP_ROOT / "subsystems" / "ss-annuity-performance.yaml",
        SEMANTIC_MAP_ROOT / "subsystems" / "index.yaml",
        SEMANTIC_MAP_ROOT / "objects" / "obj-annuity-performance-legacy-fact-processing.yaml",
        SEMANTIC_MAP_ROOT / "objects" / "index.yaml",
        SEMANTIC_MAP_ROOT / "semantic" / "index.yaml",
        SEMANTIC_MAP_ROOT / "semantic" / "concepts" / "sem-concept-customer-status.yaml",
        SEMANTIC_MAP_ROOT / "edges" / "execution-to-subsystem.yaml",
        SEMANTIC_MAP_ROOT / "edges" / "execution-to-object.yaml",
        SEMANTIC_MAP_ROOT / "edges" / "subsystem-to-object.yaml",
        SEMANTIC_MAP_ROOT / "edges" / "object-to-object.yaml",
        SEMANTIC_MAP_ROOT / "edges" / "source-to-node.yaml",
        SEMANTIC_MAP_ROOT / "candidates" / "subsystem-candidates.yaml",
        SEMANTIC_MAP_ROOT / "candidates" / "object-candidates.yaml",
        SEMANTIC_MAP_ROOT
        / "claims"
        / "wave-2026-04-17-first-wave-pilot"
        / "execution"
        / "claim-wave-2026-04-17-first-wave-pilot-annuity-performance-execution.yaml",
        SEMANTIC_MAP_ROOT
        / "claims"
        / "wave-2026-04-17-first-wave-pilot"
        / "subsystems"
        / "claim-wave-2026-04-17-first-wave-pilot-annuity-performance-subsystem.yaml",
        SEMANTIC_MAP_ROOT
        / "claims"
        / "wave-2026-04-17-first-wave-pilot"
        / "objects"
        / "claim-wave-2026-04-17-first-wave-pilot-annuity-performance-object.yaml",
        SEMANTIC_MAP_ROOT
        / "claims"
        / "wave-2026-04-17-semantic-governance-reframe"
        / "semantic"
        / "claim-wave-2026-04-17-semantic-governance-reframe-core.yaml",
        SEMANTIC_MAP_ROOT
        / "ingress"
        / "waves"
        / "wave-2026-04-17-semantic-governance-reframe"
        / "index.yaml",
        SEMANTIC_MAP_ROOT
        / "ingress"
        / "waves"
        / "wave-2026-04-17-semantic-governance-reframe"
        / "question-clusters"
        / ".gitkeep",
        SEMANTIC_MAP_ROOT
        / "ingress"
        / "waves"
        / "wave-2026-04-17-semantic-governance-reframe"
        / "findings"
        / ".gitkeep",
    ]
    for path in expected_paths:
        assert path.exists(), f"Expected semantic-map pilot artifact at {path}"

    manifest = json.loads((SEMANTIC_MAP_ROOT / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["canonical_seed_sources"] == [
        "execution/entry-surfaces.yaml",
        "sources/families.yaml",
        "waves/index.yaml",
    ]
    assert manifest["generated_canonical_files"]
    assert manifest["compiled_claim_ids"]
    assert manifest["compiled_claim_ids"] == manifest["compiled_claims_by_wave"][
        "wave-2026-04-17-semantic-governance-reframe"
    ]
    assert "wave-2026-04-17-first-wave-pilot" in manifest["compiled_claims_by_wave"]
    assert "wave-2026-04-17-semantic-governance-reframe" in manifest["compiled_claims_by_wave"]

    readme_text = (SEMANTIC_MAP_ROOT / "README.md").read_text(encoding="utf-8")
    assert "internal discovery ledger" in readme_text
    assert "not durable wiki content" in readme_text
    assert "active owner:" in readme_text
    assert "archive trigger:" in readme_text
    assert "ordinary distributed agents may write only under `claims/<wave_id>/`" in readme_text
    assert (
        "the semantic-ingress workflow may also write proposal-grade records under "
        "`ingress/waves/<wave_id>/`" in readme_text
    )
    assert "canonical registry files remain main-thread-managed" in readme_text
    assert "canonical compilation is a main-thread-only operation" in readme_text

    agents_text = (SEMANTIC_MAP_ROOT / "AGENTS.md").read_text(encoding="utf-8")
    assert "semantic ingress workflow" in agents_text
    assert "ingress/waves/<wave_id>/" in agents_text
    assert "ordinary distributed agents may write only under `claims/<wave_id>/`" in agents_text
    assert (
        "the semantic-ingress workflow may also write proposal-grade records under "
        "`ingress/waves/<wave_id>/`" in agents_text
    )
    assert (
        "current repo materials may be read only for routing, duplicate detection, "
        "or durable target awareness" in agents_text
    )
    assert "must not be cited as business-semantic evidence for ingress" in agents_text

    ingress_index = yaml.safe_load(
        (
            SEMANTIC_MAP_ROOT
            / "ingress"
            / "waves"
            / "wave-2026-04-17-semantic-governance-reframe"
            / "index.yaml"
        ).read_text(encoding="utf-8")
    )
    assert ingress_index == {
        "wave_id": "wave-2026-04-17-semantic-governance-reframe",
        "question_clusters": [],
        "findings": [],
    }

    wiki_index_text = (REPO_ROOT / "docs" / "wiki-bi" / "index.md").read_text(encoding="utf-8")
    assert "legacy-semantic-map" not in wiki_index_text

    lint_checklist_text = (
        REPO_ROOT / "docs" / "wiki-bi" / "_meta" / "wiki-maintenance-lint-checklist.md"
    ).read_text(encoding="utf-8")
    assert "docs/wiki-bi/_meta/legacy-semantic-map/" in lint_checklist_text
    assert "excluded from durable-page reachability and template checks" in lint_checklist_text
    assert "still remains absent from `docs/wiki-bi/index.md`" in lint_checklist_text
    assert "owner, archive trigger, and non-durable boundary" in lint_checklist_text

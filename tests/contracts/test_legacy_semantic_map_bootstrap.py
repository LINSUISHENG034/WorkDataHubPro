from __future__ import annotations

import json
import re
from pathlib import Path

import yaml

from scripts.legacy_semantic_map.bootstrap import bootstrap_semantic_map
from scripts.legacy_semantic_map.models import (
    CLAIM_TYPES,
    COVERAGE_STATES,
    EVIDENCE_STRENGTHS,
    SOURCE_TYPES,
    STATUSES,
    TRIAGE_STATUSES,
    WAVE_ID_PATTERN,
)


def test_semantic_map_enums_and_wave_id_shape() -> None:
    assert STATUSES == (
        "seeded",
        "active",
        "candidate",
        "deferred",
        "archived",
    )
    assert CLAIM_TYPES == (
        "direct_observation",
        "inferred_from_sources",
        "compiled_summary",
        "open_question",
    )
    assert SOURCE_TYPES == (
        "legacy_doc",
        "legacy_config",
        "legacy_test",
        "legacy_code",
        "current_spec",
        "current_audit",
        "current_wiki",
        "current_reference_asset",
    )
    assert EVIDENCE_STRENGTHS == (
        "strong",
        "supporting",
        "weak",
    )
    assert COVERAGE_STATES == (
        "seeded",
        "mapped",
        "partial",
        "closed",
        "deferred",
    )
    assert TRIAGE_STATUSES == (
        "new",
        "accepted",
        "rejected",
        "deferred",
        "merged",
    )

    assert re.fullmatch(WAVE_ID_PATTERN, "wave-2026-04-16-registry-bootstrap")
    assert re.fullmatch(WAVE_ID_PATTERN, "wave-1999-12-31-a")
    assert not re.fullmatch(WAVE_ID_PATTERN, "wave-2026-4-16-registry-bootstrap")
    assert not re.fullmatch(WAVE_ID_PATTERN, "wave-2026-04-16-Registry-Bootstrap")
    assert not re.fullmatch(WAVE_ID_PATTERN, "bootstrap-wave-2026-04-16")


def test_bootstrap_semantic_map_writes_minimal_registry(tmp_path: Path) -> None:
    registry_root = tmp_path / "legacy-semantic-map"

    bootstrap_semantic_map(registry_root)

    expected_files = {
        "README.md",
        "manifest.json",
        "execution/entry-surfaces.yaml",
        "execution/paths/.gitkeep",
        "execution/stages/.gitkeep",
        "sources/families.yaml",
        "waves/index.yaml",
        "reports/current/.gitkeep",
        "reports/waves/wave-2026-04-16-registry-bootstrap/.gitkeep",
        "subsystems/.gitkeep",
        "subsystems/index.yaml",
        "objects/.gitkeep",
        "objects/index.yaml",
        "edges/execution-to-subsystem.yaml",
        "edges/execution-to-object.yaml",
        "edges/subsystem-to-object.yaml",
        "edges/object-to-object.yaml",
        "edges/source-to-node.yaml",
        "candidates/subsystem-candidates.yaml",
        "candidates/object-candidates.yaml",
        "semantic/index.yaml",
        "semantic/concepts/.gitkeep",
        "semantic/rules/.gitkeep",
        "semantic/non-equivalences/.gitkeep",
        "semantic/lifecycles/.gitkeep",
        "semantic/fact-families/.gitkeep",
        "semantic/decision-anchors/.gitkeep",
        "semantic/question-sets/.gitkeep",
        "claims/wave-2026-04-16-registry-bootstrap/execution/.gitkeep",
        "claims/wave-2026-04-16-registry-bootstrap/subsystems/.gitkeep",
        "claims/wave-2026-04-16-registry-bootstrap/objects/.gitkeep",
        "claims/wave-2026-04-16-registry-bootstrap/semantic/.gitkeep",
        "ingress/waves/wave-2026-04-16-registry-bootstrap/index.yaml",
        "ingress/waves/wave-2026-04-16-registry-bootstrap/question-clusters/.gitkeep",
        "ingress/waves/wave-2026-04-16-registry-bootstrap/findings/.gitkeep",
    }
    actual_files = {
        path.relative_to(registry_root).as_posix()
        for path in registry_root.rglob("*")
        if path.is_file()
    }
    assert actual_files == expected_files

    readme_text = (registry_root / "README.md").read_text(encoding="utf-8")
    assert "internal discovery ledger" in readme_text
    assert "not durable wiki content" in readme_text
    assert "active owner:" in readme_text
    assert "archive trigger:" in readme_text
    assert "must never be added to `docs/wiki-bi/index.md`" in readme_text
    assert "ordinary distributed agents may write only under `claims/<wave_id>/`" in readme_text
    assert (
        "the semantic-ingress workflow may also write proposal-grade records under "
        "`ingress/waves/<wave_id>/`" in readme_text
    )
    assert "canonical registry files remain main-thread-managed" in readme_text
    assert "canonical compilation is a main-thread-only operation" in readme_text
    assert "ingress/waves/<wave_id>/" in readme_text
    assert (
        "semantic ingress uses legacy-only business-semantic evidence from "
        "`E:\\Projects\\WorkDataHub`" in readme_text
    )
    assert "promotion to final shared truth is also main-thread-only" in readme_text

    manifest = json.loads((registry_root / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["canonical_seed_sources"] == [
        "execution/entry-surfaces.yaml",
        "sources/families.yaml",
        "waves/index.yaml",
    ]
    assert manifest["generated_canonical_files"] == []
    assert manifest["compiled_claim_ids"] == []
    assert manifest["compiled_claims_by_wave"] == {}

    semantic_index = yaml.safe_load(
        (registry_root / "semantic" / "index.yaml").read_text(encoding="utf-8")
    )
    assert semantic_index == {"semantic_nodes": []}

    entry_surfaces = yaml.safe_load(
        (registry_root / "execution" / "entry-surfaces.yaml").read_text(encoding="utf-8")
    )
    assert [item["entry_family"] for item in entry_surfaces["seeded_entry_surfaces"]] == [
        "manual_cli_entrypoints",
        "manual_cli_entrypoints",
        "manual_cli_entrypoints",
        "manual_cli_entrypoints",
        "manual_cli_entrypoints",
        "scheduled_orchestrated_entrypoints",
        "scheduled_orchestrated_entrypoints",
    ]

    source_families = yaml.safe_load(
        (registry_root / "sources" / "families.yaml").read_text(encoding="utf-8")
    )
    assert [item["family_id"] for item in source_families["seeded_high_priority_source_families"]] == [
        "legacy-domain-capability-maps",
        "legacy-operator-runtime-surfaces",
        "legacy-identity-and-reference-runtime",
        "current-first-wave-governance-specs",
        "current-wiki-bi-surfaces",
        "current-replay-and-reference-assets",
    ]

    waves_index = yaml.safe_load(
        (registry_root / "waves" / "index.yaml").read_text(encoding="utf-8")
    )
    assert waves_index["active_wave_id"] == "wave-2026-04-16-registry-bootstrap"
    assert waves_index["waves"] == [
        {
            "wave_id": "wave-2026-04-16-registry-bootstrap",
            "title": "Registry bootstrap",
            "status": "active",
            "wave_ordinal": 1,
            "seeded_entry_surfaces": [
                "annuity_performance",
                "annual_award",
                "annual_loss",
                "annuity_income",
                "customer_mdm",
                "company_lookup_queue",
                "reference_sync",
            ],
            "seeded_high_priority_source_families": [
                "legacy-domain-capability-maps",
                "legacy-operator-runtime-surfaces",
                "legacy-identity-and-reference-runtime",
                "current-first-wave-governance-specs",
                "current-wiki-bi-surfaces",
                "current-replay-and-reference-assets",
            ],
            "admitted_subsystems": [],
            "durable_wiki_targets_accepted": False,
            "findings_disposition_complete": False,
            "depends_on_active_wave_working_state": False,
            "opened_at": "2026-04-16",
            "closed_at": None,
        }
    ]

    ingress_index = yaml.safe_load(
        (
            registry_root
            / "ingress"
            / "waves"
            / "wave-2026-04-16-registry-bootstrap"
            / "index.yaml"
        ).read_text(encoding="utf-8")
    )
    assert ingress_index == {
        "wave_id": "wave-2026-04-16-registry-bootstrap",
        "question_clusters": [],
        "findings": [],
    }

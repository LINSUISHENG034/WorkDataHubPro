from __future__ import annotations

import json
from pathlib import Path
import shutil

import yaml

from scripts.legacy_semantic_map.bootstrap import bootstrap_semantic_map
from scripts.legacy_semantic_map.orchestrate_wave import orchestrate_wave


REPO_ROOT = Path(__file__).resolve().parents[2]
SEMANTIC_MAP_ROOT = REPO_ROOT / "docs" / "wiki-bi" / "_meta" / "legacy-semantic-map"
SOURCE_WAVE_ID = "wave-2026-04-17-customer-status-semantic-pilot"
SUCCESSOR_WAVE_ID = "wave-2026-04-17-semantic-governance-reframe"


def _copy_registry_tree(tmp_path: Path) -> Path:
    registry_root = tmp_path / "legacy-semantic-map"
    shutil.copytree(SEMANTIC_MAP_ROOT, registry_root)
    return registry_root


def test_orchestrate_wave_writes_only_standard_claim_scopes(tmp_path: Path) -> None:
    registry_root = _copy_registry_tree(tmp_path)

    result = orchestrate_wave(registry_root, SUCCESSOR_WAVE_ID)
    claim_paths = sorted(result["claim_paths"])

    assert claim_paths
    assert all(
        "/execution/" in path
        or "/subsystems/" in path
        or "/objects/" in path
        or "/semantic/" in path
        for path in claim_paths
    )


def test_orchestrate_wave_is_idempotent_by_trigger_id(tmp_path: Path) -> None:
    registry_root = _copy_registry_tree(tmp_path)

    first = orchestrate_wave(registry_root, SUCCESSOR_WAVE_ID, trigger_id="trigger-001")
    second = orchestrate_wave(registry_root, SUCCESSOR_WAVE_ID, trigger_id="trigger-001")

    assert first["compiled_claim_ids"] == second["compiled_claim_ids"]
    assert first["generated_canonical_files"] == second["generated_canonical_files"]


def test_orchestrate_wave_preserves_existing_witness_registry_files(tmp_path: Path) -> None:
    registry_root = tmp_path / "legacy-semantic-map"
    bootstrap_semantic_map(registry_root)

    for source_claim in (SEMANTIC_MAP_ROOT / "claims" / SOURCE_WAVE_ID / "semantic").glob("*.yaml"):
        destination = registry_root / "claims" / SOURCE_WAVE_ID / "semantic" / source_claim.name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_claim, destination)

    waves_index = yaml.safe_load((registry_root / "waves" / "index.yaml").read_text(encoding="utf-8"))
    waves_index["active_wave_id"] = SUCCESSOR_WAVE_ID
    waves_index["waves"] = [
        {
            "wave_id": SOURCE_WAVE_ID,
            "title": "Customer status semantic pilot",
            "status": "closed",
            "wave_ordinal": 3,
            "opened_at": "2026-04-17",
            "seeded_entry_surfaces": [],
            "seeded_high_priority_source_families": [],
            "admitted_subsystems": [],
            "durable_wiki_targets_accepted": True,
            "findings_disposition_complete": True,
            "depends_on_active_wave_working_state": False,
            "closed_at": "2026-04-17",
            "semantic_question_set_id": "customer-status-semantic-pilot",
        },
        {
            "wave_id": SUCCESSOR_WAVE_ID,
            "title": "Semantic governance reframe",
            "status": "active",
            "wave_ordinal": 4,
            "opened_at": "2026-04-17",
            "seeded_entry_surfaces": [],
            "seeded_high_priority_source_families": [],
            "admitted_subsystems": [],
            "durable_wiki_targets_accepted": False,
            "findings_disposition_complete": False,
            "depends_on_active_wave_working_state": False,
            "closed_at": None,
        },
    ]
    (registry_root / "waves" / "index.yaml").write_text(
        yaml.safe_dump(waves_index, sort_keys=False, allow_unicode=False),
        encoding="utf-8",
    )

    (registry_root / "objects" / "obj-existing.yaml").write_text(
        yaml.safe_dump(
            {
                "object_id": "obj-existing",
                "title": "Existing object",
                "compiled_from_claims": ["claim-existing-object"],
            },
            sort_keys=False,
            allow_unicode=False,
        ),
        encoding="utf-8",
    )
    (registry_root / "objects" / "index.yaml").write_text(
        yaml.safe_dump(
            {"objects": [{"object_id": "obj-existing", "path": "objects/obj-existing.yaml"}]},
            sort_keys=False,
            allow_unicode=False,
        ),
        encoding="utf-8",
    )
    (registry_root / "subsystems" / "ss-existing.yaml").write_text(
        yaml.safe_dump(
            {
                "subsystem_id": "ss-existing",
                "title": "Existing subsystem",
                "compiled_from_claims": ["claim-existing-subsystem"],
            },
            sort_keys=False,
            allow_unicode=False,
        ),
        encoding="utf-8",
    )
    (registry_root / "subsystems" / "index.yaml").write_text(
        yaml.safe_dump(
            {
                "subsystems": [
                    {"subsystem_id": "ss-existing", "path": "subsystems/ss-existing.yaml"}
                ]
            },
            sort_keys=False,
            allow_unicode=False,
        ),
        encoding="utf-8",
    )
    for filename, payload in (
        (
            "edges/execution-to-object.yaml",
            {
                "edges": [
                    {
                        "from_id": "ep-existing",
                        "to_id": "obj-existing",
                        "relationship": "discovers_object",
                        "compiled_from_claims": ["claim-existing-edge"],
                    }
                ]
            },
        ),
        (
            "edges/source-to-node.yaml",
            {
                "edges": [
                    {
                        "from_id": "docs/domains/annuity_performance-capability-map.md",
                        "to_id": "obj-existing",
                        "relationship": "supports_claim_target",
                        "compiled_from_claims": ["claim-existing-edge"],
                    }
                ]
            },
        ),
        (
            "candidates/object-candidates.yaml",
            {
                "object_candidates": [
                    {
                        "candidate_id": "cand-existing-object",
                        "triage_status": "deferred",
                        "priority": "high",
                        "first_seen_wave": SOURCE_WAVE_ID,
                    }
                ]
            },
        ),
    ):
        target = registry_root / filename
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(
            yaml.safe_dump(payload, sort_keys=False, allow_unicode=False),
            encoding="utf-8",
        )
    (registry_root / "manifest.json").write_text(
        json.dumps(
            {
                "artifact": "legacy-semantic-map-registry",
                "canonical_seed_sources": [
                    "execution/entry-surfaces.yaml",
                    "sources/families.yaml",
                    "waves/index.yaml",
                ],
                "generated_canonical_files": [
                    "objects/index.yaml",
                    "subsystems/index.yaml",
                    "edges/execution-to-object.yaml",
                    "edges/source-to-node.yaml",
                    "candidates/object-candidates.yaml",
                ],
                "compiled_claim_ids": ["claim-existing-object"],
                "compiled_claims_by_wave": {SOURCE_WAVE_ID: ["claim-existing-object"]},
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    orchestrate_wave(registry_root, SUCCESSOR_WAVE_ID)

    object_index = yaml.safe_load((registry_root / "objects" / "index.yaml").read_text(encoding="utf-8"))
    subsystem_index = yaml.safe_load((registry_root / "subsystems" / "index.yaml").read_text(encoding="utf-8"))
    object_edges = yaml.safe_load(
        (registry_root / "edges" / "execution-to-object.yaml").read_text(encoding="utf-8")
    )

    assert object_index["objects"] == [{"object_id": "obj-existing", "path": "objects/obj-existing.yaml"}]
    assert subsystem_index["subsystems"] == [
        {"subsystem_id": "ss-existing", "path": "subsystems/ss-existing.yaml"}
    ]
    assert object_edges["edges"] == [
        {
            "from_id": "ep-existing",
            "to_id": "obj-existing",
            "relationship": "discovers_object",
            "compiled_from_claims": ["claim-existing-edge"],
        }
    ]

from __future__ import annotations

import json
from pathlib import Path

import yaml

from .models import (
    BOOTSTRAP_WAVE,
    CANONICAL_SEED_SOURCES,
    bootstrap_wave_payload,
    seeded_entry_surfaces_payload,
    seeded_source_families_payload,
)

DEFAULT_REGISTRY_ROOT = (
    Path(__file__).resolve().parents[2] / "docs" / "wiki-bi" / "_meta" / "legacy-semantic-map"
)

EMPTY_REGISTRY_PAYLOADS = {
    "subsystems/index.yaml": {"subsystems": []},
    "objects/index.yaml": {"objects": []},
    "semantic/index.yaml": {"semantic_nodes": []},
    "edges/execution-to-subsystem.yaml": {"edges": []},
    "edges/execution-to-object.yaml": {"edges": []},
    "edges/subsystem-to-object.yaml": {"edges": []},
    "edges/object-to-object.yaml": {"edges": []},
    "edges/source-to-node.yaml": {"edges": []},
    "candidates/subsystem-candidates.yaml": {"subsystem_candidates": []},
    "candidates/object-candidates.yaml": {"object_candidates": []},
}

README_TEXT = """# Legacy Semantic Map

This subtree is an internal discovery ledger for legacy semantic mapping work.
It is not durable wiki content.
It must never be added to `docs/wiki-bi/index.md`.

distributed agents may write only under `claims/<wave_id>/`.
canonical registry files remain main-thread-managed.
canonical compilation is a main-thread-only operation.

active owner: the main-thread maintainer of the current semantic-map wave
archive trigger: acceptance of the target durable wiki updates plus disposition of remaining findings for that wave
"""


def _write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def _write_json(path: Path, payload: object) -> None:
    _write_text(path, json.dumps(payload, indent=2))


def _write_yaml(path: Path, payload: object) -> None:
    _write_text(path, yaml.safe_dump(payload, sort_keys=False, allow_unicode=False))


def bootstrap_semantic_map(registry_root: Path = DEFAULT_REGISTRY_ROOT) -> Path:
    registry_root.mkdir(parents=True, exist_ok=True)

    for relative_dir in (
        "execution/paths",
        "execution/stages",
        "reports/current",
        f"reports/waves/{BOOTSTRAP_WAVE.wave_id}",
        "subsystems",
        "objects",
        "semantic/concepts",
        "semantic/rules",
        "semantic/non-equivalences",
        "semantic/lifecycles",
        "semantic/fact-families",
        "semantic/decision-anchors",
        "semantic/question-sets",
        f"claims/{BOOTSTRAP_WAVE.wave_id}/execution",
        f"claims/{BOOTSTRAP_WAVE.wave_id}/subsystems",
        f"claims/{BOOTSTRAP_WAVE.wave_id}/objects",
    ):
        directory = registry_root / relative_dir
        directory.mkdir(parents=True, exist_ok=True)
        _write_text(directory / ".gitkeep", "")

    _write_text(registry_root / "README.md", README_TEXT)
    _write_json(
        registry_root / "manifest.json",
        {
            "artifact": "legacy-semantic-map-registry",
            "canonical_seed_sources": list(CANONICAL_SEED_SOURCES),
            "generated_canonical_files": [],
            "compiled_claim_ids": [],
            "compiled_claims_by_wave": {},
        },
    )
    _write_yaml(
        registry_root / "execution" / "entry-surfaces.yaml",
        seeded_entry_surfaces_payload(),
    )
    _write_yaml(
        registry_root / "sources" / "families.yaml",
        seeded_source_families_payload(),
    )
    _write_yaml(
        registry_root / "waves" / "index.yaml",
        bootstrap_wave_payload(),
    )
    for relative_path, payload in EMPTY_REGISTRY_PAYLOADS.items():
        _write_yaml(registry_root / relative_path, payload)
    return registry_root


def main() -> None:
    bootstrap_semantic_map()


if __name__ == "__main__":
    main()

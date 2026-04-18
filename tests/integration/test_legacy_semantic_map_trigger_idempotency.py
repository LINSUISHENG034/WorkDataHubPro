from __future__ import annotations

import shutil
from pathlib import Path

from scripts.legacy_semantic_map.orchestrate_wave import orchestrate_wave


REPO_ROOT = Path(__file__).resolve().parents[2]
SEMANTIC_MAP_ROOT = REPO_ROOT / "docs" / "wiki-bi" / "_meta" / "legacy-semantic-map"
SUCCESSOR_WAVE_ID = "wave-2026-04-17-semantic-governance-reframe"


def _copy_registry_tree(tmp_path: Path) -> Path:
    registry_root = tmp_path / "legacy-semantic-map"
    shutil.copytree(SEMANTIC_MAP_ROOT, registry_root)
    return registry_root


def test_orchestrate_wave_trigger_idempotency(tmp_path: Path) -> None:
    registry_root = _copy_registry_tree(tmp_path)

    first = orchestrate_wave(registry_root, SUCCESSOR_WAVE_ID, trigger_id="trigger-001")
    second = orchestrate_wave(registry_root, SUCCESSOR_WAVE_ID, trigger_id="trigger-001")

    assert first["compiled_claim_ids"] == second["compiled_claim_ids"]
    assert first["generated_canonical_files"] == second["generated_canonical_files"]


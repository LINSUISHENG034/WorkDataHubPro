from __future__ import annotations

import json
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


def test_semantic_governance_reframe_flow_generates_additive_outputs(tmp_path: Path) -> None:
    registry_root = _copy_registry_tree(tmp_path)

    payload = orchestrate_wave(registry_root, SUCCESSOR_WAVE_ID)
    assert payload["wave_id"] == SUCCESSOR_WAVE_ID

    coverage_payload = json.loads((registry_root / payload["coverage_report"]).read_text(encoding="utf-8"))
    assert coverage_payload["wave_id"] == SUCCESSOR_WAVE_ID
    assert (
        registry_root
        / "reports"
        / "waves"
        / SUCCESSOR_WAVE_ID
        / "semantic-readiness-status.json"
    ).exists()

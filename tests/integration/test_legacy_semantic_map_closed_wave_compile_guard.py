from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from scripts.legacy_semantic_map.pilot import run_first_wave_pilot


REPO_ROOT = Path(__file__).resolve().parents[2]
SEMANTIC_MAP_ROOT = REPO_ROOT / "docs" / "wiki-bi" / "_meta" / "legacy-semantic-map"


def _copy_registry_tree(tmp_path: Path) -> Path:
    registry_root = tmp_path / "legacy-semantic-map"
    shutil.copytree(SEMANTIC_MAP_ROOT, registry_root)
    return registry_root


def test_closed_wave_compile_guard_rejects_historical_write(tmp_path: Path) -> None:
    registry_root = _copy_registry_tree(tmp_path)

    with pytest.raises(ValueError, match="active open wave"):
        run_first_wave_pilot(
            registry_root,
            wave_id="wave-2026-04-17-customer-status-semantic-pilot",
        )


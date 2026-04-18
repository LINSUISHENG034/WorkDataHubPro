from __future__ import annotations

import json
import shutil
from pathlib import Path

from scripts.legacy_semantic_map.orchestrate_wave import SUCCESSOR_WAVE_ID, orchestrate_wave
from scripts.legacy_semantic_map.pilot import (
    pilot_claim_paths,
    run_first_wave_pilot,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
SEMANTIC_MAP_ROOT = REPO_ROOT / "docs" / "wiki-bi" / "_meta" / "legacy-semantic-map"


def _copy_dependency_tree(tmp_repo_root: Path) -> Path:
    registry_root = tmp_repo_root / "docs" / "wiki-bi" / "_meta" / "legacy-semantic-map"
    shutil.copytree(SEMANTIC_MAP_ROOT, registry_root)
    return registry_root


def test_run_first_wave_pilot_rebuilds_active_successor_wave_deterministically(
    tmp_path: Path,
) -> None:
    tmp_repo_root = tmp_path / "repo"
    registry_root = _copy_dependency_tree(tmp_repo_root)
    orchestrate_wave(registry_root, SUCCESSOR_WAVE_ID)
    initial_claim_paths = pilot_claim_paths(registry_root, SUCCESSOR_WAVE_ID)
    assert len(initial_claim_paths) == 7

    first_result = run_first_wave_pilot(
        registry_root,
        wave_id=SUCCESSOR_WAVE_ID,
        claim_paths=initial_claim_paths,
    )
    first_coverage = json.loads(
        first_result.reports.current_coverage_report.read_text(encoding="utf-8")
    )
    first_integrity = json.loads(
        first_result.reports.current_integrity_report.read_text(encoding="utf-8")
    )
    manifest = json.loads((registry_root / "manifest.json").read_text(encoding="utf-8"))

    assert first_coverage["wave_id"] == SUCCESSOR_WAVE_ID
    assert first_coverage["wave_status"] == "green"
    assert first_integrity["closeout_ready"] is False
    assert first_integrity["archive_ready"] is False
    assert "durable_wiki_targets_not_accepted" in first_integrity["blocking_reasons"]
    assert manifest["compiled_claims_by_wave"][SUCCESSOR_WAVE_ID] == manifest[
        "compiled_claim_ids"
    ]

    second_result = run_first_wave_pilot(
        registry_root,
        wave_id=SUCCESSOR_WAVE_ID,
        claim_paths=pilot_claim_paths(registry_root, SUCCESSOR_WAVE_ID),
    )
    assert (
        second_result.reports.current_coverage_report.read_text(encoding="utf-8")
        == first_result.reports.current_coverage_report.read_text(encoding="utf-8")
    )
    assert (
        second_result.reports.current_integrity_report.read_text(encoding="utf-8")
        == first_result.reports.current_integrity_report.read_text(encoding="utf-8")
    )

from __future__ import annotations

import json
import shutil
from pathlib import Path

from scripts.legacy_semantic_map.reporting import generate_reports

REPO_ROOT = Path(__file__).resolve().parents[2]
SEMANTIC_MAP_ROOT = REPO_ROOT / "docs" / "wiki-bi" / "_meta" / "legacy-semantic-map"
SEMANTIC_PILOT_WAVE_ID = "wave-2026-04-17-customer-status-semantic-pilot"


def _copy_registry_tree(tmp_repo_root: Path) -> Path:
    registry_root = tmp_repo_root / "docs" / "wiki-bi" / "_meta" / "legacy-semantic-map"
    shutil.copytree(SEMANTIC_MAP_ROOT, registry_root)
    return registry_root


def test_customer_status_semantic_pilot_is_checked_in_and_rerunnable(tmp_path: Path) -> None:
    question_set_path = (
        SEMANTIC_MAP_ROOT
        / "semantic"
        / "question-sets"
        / "customer-status-semantic-pilot.yaml"
    )
    assert question_set_path.exists()

    tmp_repo_root = tmp_path / "repo"
    registry_root = _copy_registry_tree(tmp_repo_root)
    claim_paths = sorted(
        (registry_root / "claims" / SEMANTIC_PILOT_WAVE_ID / "semantic").glob("*.yaml")
    )
    assert len(claim_paths) == 3

    report_result = generate_reports(registry_root, wave_id=SEMANTIC_PILOT_WAVE_ID)

    wave_coverage = json.loads(report_result.wave_coverage_report.read_text(encoding="utf-8"))
    wave_integrity = json.loads(report_result.wave_integrity_report.read_text(encoding="utf-8"))

    assert (registry_root / "semantic" / "index.yaml").exists()
    assert (registry_root / "semantic" / "concepts" / "sem-concept-customer-status.yaml").exists()
    assert (
        registry_root
        / "semantic"
        / "non-equivalences"
        / "sem-non-equivalence-customer-master-vs-status.yaml"
    ).exists()
    assert wave_coverage["wave_id"] == SEMANTIC_PILOT_WAVE_ID
    assert wave_coverage["wave_status"] == "red"
    assert wave_coverage["semantic_question_coverage_pct"] == 0.0
    assert wave_coverage["semantic_non_equivalence_coverage_pct"] == 0.0
    assert wave_coverage["stub_primary_source_count"] == 0
    assert wave_integrity["wave_status"] == "red"
    assert "semantic_question_coverage_incomplete" in wave_integrity["blocking_reasons"]
    assert "missing_wave_compiled_claim_index" in wave_integrity["blocking_reasons"]

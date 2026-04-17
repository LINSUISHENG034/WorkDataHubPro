from __future__ import annotations

import json
import shutil
from pathlib import Path

from scripts.legacy_semantic_map.compiler import compile_claim_artifacts
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

    compile_result = compile_claim_artifacts(registry_root, claim_paths)
    report_result = generate_reports(registry_root, wave_id=SEMANTIC_PILOT_WAVE_ID)

    wave_coverage = json.loads(report_result.wave_coverage_report.read_text(encoding="utf-8"))
    wave_integrity = json.loads(report_result.wave_integrity_report.read_text(encoding="utf-8"))

    assert "semantic/index.yaml" in compile_result.written_files
    assert "semantic/concepts/sem-concept-customer-status.yaml" in compile_result.written_files
    assert (
        "semantic/non-equivalences/sem-non-equivalence-customer-master-vs-status.yaml"
        in compile_result.written_files
    )
    assert wave_coverage["wave_id"] == SEMANTIC_PILOT_WAVE_ID
    assert wave_coverage["semantic_question_coverage_pct"] == 100.0
    assert wave_coverage["semantic_non_equivalence_coverage_pct"] == 100.0
    assert wave_coverage["stub_primary_source_count"] == 0
    assert wave_coverage["absorption_contract_completion_pct"] == 100.0
    assert wave_integrity["wave_status"] in {"yellow", "green"}

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


def test_orchestrate_successor_wave_generates_wave_outputs(tmp_path: Path) -> None:
    registry_root = _copy_registry_tree(tmp_path)

    payload = orchestrate_wave(registry_root, SUCCESSOR_WAVE_ID)

    assert payload["wave_id"] == SUCCESSOR_WAVE_ID
    assert payload["claim_paths"]
    assert (registry_root / payload["coverage_report"]).exists()
    assert (registry_root / payload["integrity_report"]).exists()


def test_orchestrate_wave_mutates_only_temp_registry_copy(tmp_path: Path) -> None:
    registry_root = _copy_registry_tree(tmp_path)
    repo_rule_before = (
        SEMANTIC_MAP_ROOT / "semantic" / "rules" / "sem-rule-is-new-definition.yaml"
    ).read_text(encoding="utf-8")
    source_claims_before = sorted(
        path.name
        for path in (
            registry_root
            / "claims"
            / "wave-2026-04-17-customer-status-semantic-pilot"
            / "semantic"
        ).glob("*.yaml")
    )
    repo_reports_before = sorted(
        path.relative_to(SEMANTIC_MAP_ROOT).as_posix()
        for path in (SEMANTIC_MAP_ROOT / "reports" / "waves" / SUCCESSOR_WAVE_ID).glob("*")
    )

    payload = orchestrate_wave(registry_root, SUCCESSOR_WAVE_ID)

    assert source_claims_before
    assert source_claims_before == sorted(
        path.name
        for path in (
            registry_root
            / "claims"
            / "wave-2026-04-17-customer-status-semantic-pilot"
            / "semantic"
        ).glob("*.yaml")
    )
    assert (registry_root / payload["coverage_report"]).exists()
    assert (registry_root / payload["integrity_report"]).exists()
    assert sorted(
        path.relative_to(SEMANTIC_MAP_ROOT).as_posix()
        for path in (SEMANTIC_MAP_ROOT / "reports" / "waves" / SUCCESSOR_WAVE_ID).glob("*")
    ) == repo_reports_before
    assert (
        SEMANTIC_MAP_ROOT / "semantic" / "rules" / "sem-rule-is-new-definition.yaml"
    ).read_text(encoding="utf-8") == repo_rule_before


def test_orchestrate_wave_repeated_runs_stabilize_outputs(tmp_path: Path) -> None:
    registry_root = _copy_registry_tree(tmp_path)

    first = orchestrate_wave(
        registry_root,
        SUCCESSOR_WAVE_ID,
        trigger_id="trigger-key-semantics-001",
    )
    first_rule = (
        registry_root / "semantic" / "rules" / "sem-rule-is-new-definition.yaml"
    ).read_text(encoding="utf-8")
    first_readiness = (
        registry_root
        / "reports"
        / "waves"
        / SUCCESSOR_WAVE_ID
        / "semantic-readiness-status.json"
    ).read_text(encoding="utf-8")

    second = orchestrate_wave(
        registry_root,
        SUCCESSOR_WAVE_ID,
        trigger_id="trigger-key-semantics-001",
    )
    second_rule = (
        registry_root / "semantic" / "rules" / "sem-rule-is-new-definition.yaml"
    ).read_text(encoding="utf-8")
    second_readiness = (
        registry_root
        / "reports"
        / "waves"
        / SUCCESSOR_WAVE_ID
        / "semantic-readiness-status.json"
    ).read_text(encoding="utf-8")

    assert first["compiled_claim_ids"] == second["compiled_claim_ids"]
    assert first["generated_canonical_files"] == second["generated_canonical_files"]
    assert first_rule == second_rule
    assert first_readiness == second_readiness

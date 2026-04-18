from __future__ import annotations

import json
import shutil
from pathlib import Path

import yaml

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
    readiness_payload = json.loads(
        (
            registry_root
            / "reports"
            / "waves"
            / SUCCESSOR_WAVE_ID
            / "semantic-readiness-status.json"
        ).read_text(encoding="utf-8")
    )
    discovery_payload = json.loads(
        (
            registry_root
            / "reports"
            / "waves"
            / SUCCESSOR_WAVE_ID
            / "semantic-discovery-status.json"
        ).read_text(encoding="utf-8")
    )
    assert coverage_payload["wave_id"] == SUCCESSOR_WAVE_ID
    assert discovery_payload["recommendation_counts"]["recommended_stable_canonical"] >= 4
    assert discovery_payload["recommendation_counts"]["recommended_contested"] >= 1
    assert "sem-non-equivalence-customer-type-vs-is-new" in discovery_payload[
        "contested_proposal_ids"
    ]
    assert "sem-non-equivalence-customer-type-vs-is-new" in readiness_payload[
        "blocked_semantic_ids"
    ]
    assert "sem-rule-is-new-definition" in readiness_payload["handoff_ready_semantic_ids"]

    stable_rule = yaml.safe_load(
        (
            registry_root / "semantic" / "rules" / "sem-rule-is-new-definition.yaml"
        ).read_text(encoding="utf-8")
    )
    contested_non_equivalence = yaml.safe_load(
        (
            registry_root
            / "semantic"
            / "non-equivalences"
            / "sem-non-equivalence-customer-type-vs-is-new.yaml"
        ).read_text(encoding="utf-8")
    )
    second_rule = yaml.safe_load(
        (
            registry_root
            / "semantic"
            / "rules"
            / "sem-rule-status-source-splitting.yaml"
        ).read_text(encoding="utf-8")
    )
    second_non_equivalence = yaml.safe_load(
        (
            registry_root
            / "semantic"
            / "non-equivalences"
            / "sem-non-equivalence-customer-master-vs-status.yaml"
        ).read_text(encoding="utf-8")
    )

    assert stable_rule["proposal_governance"]["recommendation_status"] == (
        "recommended_stable_canonical"
    )
    assert contested_non_equivalence["proposal_governance"]["recommendation_status"] == (
        "recommended_contested"
    )
    assert "contradiction_unresolved" in contested_non_equivalence["blocked_by"]
    assert second_rule["proposal_governance"]["recommendation_status"] == (
        "recommended_stable_canonical"
    )
    assert second_non_equivalence["proposal_governance"]["recommendation_status"] == (
        "recommended_stable_canonical"
    )

from __future__ import annotations

import json
from pathlib import Path

from scripts.legacy_semantic_map.probe import probe_wave


REPO_ROOT = Path(__file__).resolve().parents[2]
SEMANTIC_MAP_ROOT = REPO_ROOT / "docs" / "wiki-bi" / "_meta" / "legacy-semantic-map"
SUCCESSOR_WAVE_ID = "wave-2026-04-17-semantic-governance-reframe"


def test_probe_wave_temp_loop_reports_stability_and_generated_outputs() -> None:
    claim_paths = [
        SEMANTIC_MAP_ROOT
        / "claims"
        / SUCCESSOR_WAVE_ID
        / "semantic"
        / "claim-wave-2026-04-17-semantic-governance-reframe-core.yaml",
        SEMANTIC_MAP_ROOT
        / "claims"
        / SUCCESSOR_WAVE_ID
        / "semantic"
        / "claim-wave-2026-04-17-semantic-governance-reframe-lifecycle.yaml",
        SEMANTIC_MAP_ROOT
        / "claims"
        / SUCCESSOR_WAVE_ID
        / "semantic"
        / "claim-wave-2026-04-17-semantic-governance-reframe-rules.yaml",
    ]

    result = probe_wave(
        SEMANTIC_MAP_ROOT,
        wave_id=SUCCESSOR_WAVE_ID,
        claim_paths=claim_paths,
        reruns=2,
    )
    payload = result.to_payload()
    temp_root = Path(payload["temp_registry_root"])

    assert temp_root.exists()
    assert payload["compiled_claim_ids"] == [
        "claim-wave-2026-04-17-semantic-governance-reframe-core",
        "claim-wave-2026-04-17-semantic-governance-reframe-lifecycle",
        "claim-wave-2026-04-17-semantic-governance-reframe-rules",
    ]
    assert "semantic/rules/sem-rule-is-new-definition.yaml" in payload[
        "generated_canonical_files"
    ]
    assert payload["stability_checks"][0]["changed_files"] == [
        "reports/waves/wave-2026-04-17-semantic-governance-reframe/integrity-status.json"
    ]
    assert payload["stability_checks"][1]["stable"] is True
    assert payload["stability_checks"][1]["changed_files"] == []

    integrity_payload = json.loads(
        (temp_root / payload["wave_integrity_report"]).read_text(encoding="utf-8")
    )
    readiness_payload = json.loads(
        (temp_root / payload["semantic_readiness_report"]).read_text(encoding="utf-8")
    )

    assert integrity_payload["wave_id"] == SUCCESSOR_WAVE_ID
    assert integrity_payload["immutability_check_passed"] is True
    assert readiness_payload["handoff_ready_semantic_ids"]

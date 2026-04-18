from __future__ import annotations

from pathlib import Path

import pytest

from scripts.legacy_semantic_map.probe import ACTIVE_SUCCESSOR_WAVE_ID, main, probe_wave


REPO_ROOT = Path(__file__).resolve().parents[2]
SEMANTIC_MAP_ROOT = REPO_ROOT / "docs" / "wiki-bi" / "_meta" / "legacy-semantic-map"
SUCCESSOR_WAVE_ID = "wave-2026-04-17-semantic-governance-reframe"


def test_probe_wave_rejects_claim_outside_wave_root() -> None:
    stray_claim = REPO_ROOT / "docs" / "wiki-bi" / "_meta" / "legacy-semantic-map" / "README.md"

    with pytest.raises(ValueError, match=f"claims/{SUCCESSOR_WAVE_ID}"):
        probe_wave(
            SEMANTIC_MAP_ROOT,
            wave_id=SUCCESSOR_WAVE_ID,
            claim_paths=[stray_claim],
            reruns=0,
        )


def test_probe_cli_defaults_to_active_successor_wave() -> None:
    source = (REPO_ROOT / "scripts" / "legacy_semantic_map" / "probe.py").read_text(
        encoding="utf-8"
    )

    assert ACTIVE_SUCCESSOR_WAVE_ID == SUCCESSOR_WAVE_ID
    assert 'default=ACTIVE_SUCCESSOR_WAVE_ID' in source
    assert 'temporary semantic-map registry copy' in source


def test_probe_cli_rejects_negative_reruns() -> None:
    with pytest.raises(ValueError, match="--reruns must be >= 0"):
        main([
            "--registry-root",
            str(SEMANTIC_MAP_ROOT),
            "--reruns",
            "-1",
        ])


def test_probe_output_has_stability_summary(tmp_path: Path) -> None:
    claim_path = (
        SEMANTIC_MAP_ROOT
        / "claims"
        / SUCCESSOR_WAVE_ID
        / "semantic"
        / "claim-wave-2026-04-17-semantic-governance-reframe-rules.yaml"
    )

    result = probe_wave(
        SEMANTIC_MAP_ROOT,
        wave_id=SUCCESSOR_WAVE_ID,
        claim_paths=[claim_path],
        reruns=1,
    )
    payload = result.to_payload()

    assert payload["temp_registry_root"] != payload["source_registry_root"]
    assert payload["source_claim_paths"] == [
        f"claims/{SUCCESSOR_WAVE_ID}/semantic/claim-wave-2026-04-17-semantic-governance-reframe-rules.yaml"
    ]
    assert payload["stability_checks"][0]["iteration"] == 2
    assert "stable" in payload["stability_checks"][0]
    assert "changed_files" in payload["stability_checks"][0]
    assert "wave_integrity_report" in payload
    assert "semantic_readiness_report" in payload

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from scripts.legacy_semantic_map.bootstrap import bootstrap_semantic_map
from scripts.legacy_semantic_map.claims import (
    ClaimArtifact,
    ClaimDiscoveredObjectRecord,
    ClaimSourceRecord,
    write_claim_artifact,
)
from scripts.legacy_semantic_map.compiler import compile_claim_artifacts
from scripts.legacy_semantic_map.pilot import run_first_wave_pilot
from scripts.legacy_semantic_map.reporting import generate_reports


def _seed_registry_with_open_and_closed_waves(tmp_path: Path) -> Path:
    registry_root = tmp_path / "legacy-semantic-map"
    bootstrap_semantic_map(registry_root)
    payload = yaml.safe_load((registry_root / "waves" / "index.yaml").read_text(encoding="utf-8"))
    payload["active_wave_id"] = "wave-open"
    payload["waves"] = [
        {
            "wave_id": "wave-closed",
            "title": "Closed historical wave",
            "status": "closed",
            "wave_ordinal": 1,
            "opened_at": "2026-04-16",
            "seeded_entry_surfaces": [],
            "seeded_high_priority_source_families": [],
            "admitted_subsystems": [],
            "durable_wiki_targets_accepted": True,
            "findings_disposition_complete": True,
            "depends_on_active_wave_working_state": False,
            "closed_at": "2026-04-16",
        },
        {
            "wave_id": "wave-open",
            "title": "Open active wave",
            "status": "active",
            "wave_ordinal": 2,
            "opened_at": "2026-04-17",
            "seeded_entry_surfaces": [],
            "seeded_high_priority_source_families": [],
            "admitted_subsystems": [],
            "durable_wiki_targets_accepted": False,
            "findings_disposition_complete": False,
            "depends_on_active_wave_working_state": False,
            "closed_at": None,
        },
    ]
    (registry_root / "waves" / "index.yaml").write_text(
        yaml.safe_dump(payload, sort_keys=False, allow_unicode=False),
        encoding="utf-8",
    )
    return registry_root


def _build_object_claim(*, wave_id: str, claim_id: str) -> ClaimArtifact:
    return ClaimArtifact(
        claim_id=claim_id,
        wave_id=wave_id,
        claim_scope="objects",
        claim_target_id="obj-wave-guard-fixture",
        sources_read=[
            ClaimSourceRecord(
                source_ref="docs/domains/annuity_performance-capability-map.md",
                source_type="legacy_doc",
                note="Wave-guard fixture source.",
            )
        ],
        objects_discovered=[
            ClaimDiscoveredObjectRecord(
                object_id="obj-wave-guard-fixture",
                title="Wave guard fixture",
                summary="Wave guard fixture object.",
                source_refs=["docs/domains/annuity_performance-capability-map.md"],
                source_type="legacy_doc",
                claim_type="direct_observation",
                evidence_strength="strong",
                coverage_state="mapped",
                confidence="high",
                last_verified="2026-04-18",
                open_questions=[],
            )
        ],
        edges_added=[],
        candidates_raised=[],
        open_questions=[],
        compiled_into=[],
        submitted_at="2026-04-18T00:00:00Z",
    )


def test_write_claim_artifact_rejects_closed_or_non_active_wave(tmp_path: Path) -> None:
    registry_root = _seed_registry_with_open_and_closed_waves(tmp_path)
    closed_claim = _build_object_claim(
        wave_id="wave-closed",
        claim_id="claim-wave-closed-wave-guard-fixture",
    )

    with pytest.raises(ValueError, match="active open wave"):
        write_claim_artifact(registry_root, closed_claim)


def test_compile_claim_artifacts_rejects_closed_wave_inputs(tmp_path: Path) -> None:
    registry_root = _seed_registry_with_open_and_closed_waves(tmp_path)
    closed_claim = _build_object_claim(
        wave_id="wave-closed",
        claim_id="claim-wave-closed-wave-guard-fixture",
    )
    claim_path = registry_root / "claims" / "wave-closed" / "objects" / "claim-wave-closed-wave-guard-fixture.yaml"
    claim_path.parent.mkdir(parents=True, exist_ok=True)
    claim_path.write_text(
        yaml.safe_dump(closed_claim.to_payload(), sort_keys=False, allow_unicode=False),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="active open wave"):
        compile_claim_artifacts(registry_root, [claim_path])


def test_generate_reports_rejects_authoritative_current_write_when_active_wave_is_closed(
    tmp_path: Path,
) -> None:
    registry_root = _seed_registry_with_open_and_closed_waves(tmp_path)
    payload = yaml.safe_load((registry_root / "waves" / "index.yaml").read_text(encoding="utf-8"))
    payload["active_wave_id"] = "wave-closed"
    (registry_root / "waves" / "index.yaml").write_text(
        yaml.safe_dump(payload, sort_keys=False, allow_unicode=False),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="active open wave"):
        generate_reports(registry_root)


def test_pilot_uses_same_wave_guards(tmp_path: Path) -> None:
    registry_root = _seed_registry_with_open_and_closed_waves(tmp_path)
    closed_claim = _build_object_claim(
        wave_id="wave-closed",
        claim_id="claim-wave-closed-wave-guard-fixture",
    )
    claim_path = registry_root / "claims" / "wave-closed" / "objects" / "claim-wave-closed-wave-guard-fixture.yaml"
    claim_path.parent.mkdir(parents=True, exist_ok=True)
    claim_path.write_text(
        yaml.safe_dump(closed_claim.to_payload(), sort_keys=False, allow_unicode=False),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="active open wave"):
        run_first_wave_pilot(
            registry_root,
            wave_id="wave-closed",
            claim_paths=[claim_path],
        )


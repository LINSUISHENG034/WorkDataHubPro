from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest
import yaml

from scripts.legacy_semantic_map.bootstrap import bootstrap_semantic_map
from scripts.legacy_semantic_map.claims import (
    CLAIM_SCOPE_DIRECTORIES,
    ClaimArtifact,
    ClaimCandidateRecord,
    ClaimDiscoveredObjectRecord,
    ClaimEdgeRecord,
    ClaimSourceRecord,
    claim_relative_path,
    write_claim_artifact,
)
from scripts.legacy_semantic_map.models import CONFIDENCE_LEVELS


def _build_execution_claim() -> ClaimArtifact:
    return ClaimArtifact(
        claim_id="claim-wave-2026-04-16-registry-bootstrap-annuity-performance-manual-entry",
        wave_id="wave-2026-04-16-registry-bootstrap",
        claim_scope="execution",
        claim_target_id="ep-manual-cli-entrypoints-annuity-performance-manual-entry",
        sources_read=[
            ClaimSourceRecord(
                source_ref="src/work_data_hub/cli/etl/domain_validation.py",
                source_type="legacy_code",
                note="Manual domain validation entrypoint for annuity performance.",
            )
        ],
        objects_discovered=[
            ClaimDiscoveredObjectRecord(
                object_id="obj-annuity-performance-manual-entry",
                title="Annuity performance manual entry",
                summary="Manual CLI execution surface for annuity performance.",
                source_refs=[
                    "src/work_data_hub/cli/etl/domain_validation.py",
                ],
                source_type="legacy_code",
                claim_type="direct_observation",
                evidence_strength="strong",
                coverage_state="partial",
                confidence="high",
                last_verified="2026-04-16",
                open_questions=[],
            )
        ],
        edges_added=[
            ClaimEdgeRecord(
                from_id="ep-manual-cli-entrypoints-annuity-performance-manual-entry",
                to_id="obj-annuity-performance-manual-entry",
                relationship="discovers_object",
                source_refs=[
                    "src/work_data_hub/cli/etl/domain_validation.py",
                ],
                source_type="legacy_code",
                claim_type="direct_observation",
                evidence_strength="strong",
                coverage_state="partial",
                confidence="high",
                last_verified="2026-04-16",
                open_questions=[],
            )
        ],
        candidates_raised=[
            ClaimCandidateRecord(
                candidate_id="cand-subsystem-annuity-performance-manual-entry",
                candidate_type="subsystem",
                proposed_name="annuity-performance-manual-entry",
                reason="Manual entrypoint may deserve a dedicated subsystem boundary.",
                trigger_files=[
                    "src/work_data_hub/cli/etl/domain_validation.py",
                ],
                source_type="legacy_code",
                claim_type="direct_observation",
                confidence="medium",
                triage_status="new",
                first_seen_wave="wave-2026-04-16-registry-bootstrap",
                last_verified="2026-04-16",
            )
        ],
        open_questions=[],
        compiled_into=[],
        submitted_at="2026-04-16T00:00:00Z",
    )


def test_claim_artifact_contract_and_relative_path_shape() -> None:
    claim = _build_execution_claim()

    assert CONFIDENCE_LEVELS == ("high", "medium", "low")
    assert CLAIM_SCOPE_DIRECTORIES == {
        "execution": "execution",
        "subsystems": "subsystems",
        "objects": "objects",
    }

    assert claim_relative_path(claim) == Path(
        "claims"
    ) / "wave-2026-04-16-registry-bootstrap" / "execution" / (
        "claim-wave-2026-04-16-registry-bootstrap-annuity-performance-manual-entry.yaml"
    )

    payload = claim.to_payload()
    assert payload["claim_id"] == claim.claim_id
    assert payload["claim_scope"] == "execution"
    assert payload["claim_target_id"] == (
        "ep-manual-cli-entrypoints-annuity-performance-manual-entry"
    )
    assert payload["sources_read"][0]["source_type"] == "legacy_code"
    assert payload["objects_discovered"][0]["confidence"] == "high"
    assert payload["edges_added"][0]["relationship"] == "discovers_object"
    assert payload["candidates_raised"][0]["triage_status"] == "new"


def test_claim_scope_rejects_unsupported_directory_targets() -> None:
    claim = _build_execution_claim()
    invalid_claim = replace(claim, claim_scope="paths")

    with pytest.raises(ValueError, match="Unsupported claim_scope"):
        claim_relative_path(invalid_claim)


@pytest.mark.parametrize(
    ("wave_id", "message"),
    [
        ("../escape", "Malformed wave_id"),
        ("wave-2026-4-16-registry-bootstrap", "Malformed wave_id"),
    ],
)
def test_claim_relative_path_rejects_malformed_wave_ids(
    wave_id: str,
    message: str,
) -> None:
    claim = _build_execution_claim()
    invalid_claim = replace(claim, wave_id=wave_id)

    with pytest.raises(ValueError, match=message):
        claim_relative_path(invalid_claim)


@pytest.mark.parametrize("claim_id", ["../escape", "claim with spaces", "claim/escape"])
def test_claim_relative_path_rejects_malformed_claim_ids(claim_id: str) -> None:
    claim = _build_execution_claim()
    invalid_claim = replace(claim, claim_id=claim_id)

    with pytest.raises(ValueError, match="Malformed claim_id"):
        claim_relative_path(invalid_claim)


def test_claim_records_reject_invalid_constrained_vocabularies() -> None:
    claim = _build_execution_claim()

    with pytest.raises(ValueError, match="Unsupported source_type"):
        ClaimSourceRecord(
            source_ref="src/work_data_hub/cli/etl/domain_validation.py",
            source_type="made_up_source",
            note="invalid source vocabulary",
        )

    with pytest.raises(ValueError, match="Unsupported source_type"):
        replace(claim.objects_discovered[0], source_type="made_up_source")

    with pytest.raises(ValueError, match="Unsupported claim_type"):
        replace(claim.objects_discovered[0], claim_type="made_up_claim_type")

    with pytest.raises(ValueError, match="Unsupported evidence_strength"):
        replace(claim.edges_added[0], evidence_strength="certain")

    with pytest.raises(ValueError, match="Unsupported coverage_state"):
        replace(claim.objects_discovered[0], coverage_state="unknown")

    with pytest.raises(ValueError, match="Unsupported confidence"):
        replace(claim.candidates_raised[0], confidence="certain")

    with pytest.raises(ValueError, match="Unsupported triage_status"):
        replace(claim.candidates_raised[0], triage_status="queued")


def test_write_claim_artifact_writes_yaml_under_registered_wave(tmp_path: Path) -> None:
    registry_root = tmp_path / "legacy-semantic-map"
    bootstrap_semantic_map(registry_root)

    claim = _build_execution_claim()
    output_path = write_claim_artifact(registry_root, claim)

    assert output_path == (
        registry_root
        / "claims"
        / "wave-2026-04-16-registry-bootstrap"
        / "execution"
        / "claim-wave-2026-04-16-registry-bootstrap-annuity-performance-manual-entry.yaml"
    )

    payload = yaml.safe_load(output_path.read_text(encoding="utf-8"))
    assert payload["claim_id"] == claim.claim_id
    assert payload["sources_read"][0]["source_ref"] == (
        "src/work_data_hub/cli/etl/domain_validation.py"
    )
    assert payload["objects_discovered"][0]["object_id"] == (
        "obj-annuity-performance-manual-entry"
    )
    assert payload["edges_added"][0]["relationship"] == "discovers_object"
    assert payload["candidates_raised"][0]["candidate_id"] == (
        "cand-subsystem-annuity-performance-manual-entry"
    )


def test_write_claim_artifact_rejects_unregistered_wave(tmp_path: Path) -> None:
    registry_root = tmp_path / "legacy-semantic-map"
    bootstrap_semantic_map(registry_root)

    claim = _build_execution_claim()
    invalid_claim = ClaimArtifact(
        **(
            claim.to_payload()
            | {
                "wave_id": "wave-2026-04-17-unregistered",
            }
        )
    )

    with pytest.raises(ValueError, match="Unregistered wave_id"):
        write_claim_artifact(registry_root, invalid_claim)

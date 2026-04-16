from __future__ import annotations

from pathlib import Path

import pytest

from scripts.legacy_semantic_map.claims import (
    CLAIM_SCOPE_DIRECTORIES,
    ClaimArtifact,
    ClaimCandidateRecord,
    ClaimDiscoveredObjectRecord,
    ClaimEdgeRecord,
    ClaimSourceRecord,
    claim_relative_path,
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
    invalid_claim = ClaimArtifact(**(claim.to_payload() | {"claim_scope": "paths"}))

    with pytest.raises(ValueError, match="Unsupported claim_scope"):
        claim_relative_path(invalid_claim)

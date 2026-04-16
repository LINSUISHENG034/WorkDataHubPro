from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

from scripts.legacy_semantic_map.bootstrap import bootstrap_semantic_map
from scripts.legacy_semantic_map.claims import (
    ClaimArtifact,
    ClaimCandidateRecord,
    ClaimDiscoveredObjectRecord,
    ClaimEdgeRecord,
    ClaimSourceRecord,
    write_claim_artifact,
)
from scripts.legacy_semantic_map.compiler import compile_claim_artifacts


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
                note="Manual annuity-performance CLI entrypoint.",
            )
        ],
        objects_discovered=[
            ClaimDiscoveredObjectRecord(
                object_id="obj-annuity-performance-manual-entry",
                title="Annuity performance manual entry",
                summary="Manual CLI execution surface for annuity performance.",
                source_refs=["src/work_data_hub/cli/etl/domain_validation.py"],
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
                source_refs=["src/work_data_hub/cli/etl/domain_validation.py"],
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
                trigger_files=["src/work_data_hub/cli/etl/domain_validation.py"],
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


def _build_subsystem_claim() -> ClaimArtifact:
    return ClaimArtifact(
        claim_id="claim-wave-2026-04-16-registry-bootstrap-annuity-performance-subsystem",
        wave_id="wave-2026-04-16-registry-bootstrap",
        claim_scope="subsystems",
        claim_target_id="ss-annuity-performance-manual-entry",
        sources_read=[
            ClaimSourceRecord(
                source_ref="src/work_data_hub/cli/etl/domain_validation.py",
                source_type="legacy_code",
                note="Subsystem evidence for manual annuity-performance entrypoint.",
            )
        ],
        objects_discovered=[
            ClaimDiscoveredObjectRecord(
                object_id="obj-annuity-performance-manual-entry",
                title="Annuity performance manual entry",
                summary="Manual CLI execution surface for annuity performance.",
                source_refs=["src/work_data_hub/cli/etl/domain_validation.py"],
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
                from_id="ss-annuity-performance-manual-entry",
                to_id="obj-annuity-performance-manual-entry",
                relationship="owns_object",
                source_refs=["src/work_data_hub/cli/etl/domain_validation.py"],
                source_type="legacy_code",
                claim_type="direct_observation",
                evidence_strength="strong",
                coverage_state="partial",
                confidence="high",
                last_verified="2026-04-16",
                open_questions=[],
            )
        ],
        candidates_raised=[],
        open_questions=[],
        compiled_into=[],
        submitted_at="2026-04-16T00:05:00Z",
    )


def _build_object_claim() -> ClaimArtifact:
    return ClaimArtifact(
        claim_id="claim-wave-2026-04-16-registry-bootstrap-annuity-performance-object",
        wave_id="wave-2026-04-16-registry-bootstrap",
        claim_scope="objects",
        claim_target_id="obj-annuity-performance-manual-entry",
        sources_read=[
            ClaimSourceRecord(
                source_ref="src/work_data_hub/cli/etl/domain_validation.py",
                source_type="legacy_code",
                note="Object-level evidence for manual annuity-performance entrypoint.",
            )
        ],
        objects_discovered=[
            ClaimDiscoveredObjectRecord(
                object_id="obj-annuity-performance-manual-entry",
                title="Annuity performance manual entry",
                summary="Manual CLI execution surface for annuity performance.",
                source_refs=["src/work_data_hub/cli/etl/domain_validation.py"],
                source_type="legacy_code",
                claim_type="direct_observation",
                evidence_strength="strong",
                coverage_state="partial",
                confidence="high",
                last_verified="2026-04-16",
                open_questions=[],
            )
        ],
        edges_added=[],
        candidates_raised=[],
        open_questions=[],
        compiled_into=[],
        submitted_at="2026-04-16T00:10:00Z",
    )


def test_compile_claim_artifacts_writes_canonical_registry_files(tmp_path: Path) -> None:
    registry_root = tmp_path / "legacy-semantic-map"
    bootstrap_semantic_map(registry_root)

    execution_path = write_claim_artifact(registry_root, _build_execution_claim())
    subsystem_path = write_claim_artifact(registry_root, _build_subsystem_claim())
    object_path = write_claim_artifact(registry_root, _build_object_claim())

    result = compile_claim_artifacts(
        registry_root,
        [execution_path, subsystem_path, object_path],
    )

    assert result.compiled_claim_ids == [
        "claim-wave-2026-04-16-registry-bootstrap-annuity-performance-manual-entry",
        "claim-wave-2026-04-16-registry-bootstrap-annuity-performance-object",
        "claim-wave-2026-04-16-registry-bootstrap-annuity-performance-subsystem",
    ]

    path_payload = yaml.safe_load(
        (
            registry_root
            / "execution"
            / "paths"
            / "ep-manual-cli-entrypoints-annuity-performance-manual-entry.yaml"
        ).read_text(encoding="utf-8")
    )
    assert path_payload["path_id"] == "ep-manual-cli-entrypoints-annuity-performance-manual-entry"
    assert path_payload["entry_surface"] == "manual_cli_entrypoints"
    assert path_payload["domain_or_surface"] == "annuity_performance"
    assert path_payload["compiled_from_claims"] == [
        "claim-wave-2026-04-16-registry-bootstrap-annuity-performance-manual-entry"
    ]

    subsystem_payload = yaml.safe_load(
        (registry_root / "subsystems" / "ss-annuity-performance-manual-entry.yaml").read_text(
            encoding="utf-8"
        )
    )
    assert subsystem_payload["subsystem_id"] == "ss-annuity-performance-manual-entry"
    assert subsystem_payload["compiled_from_claims"] == [
        "claim-wave-2026-04-16-registry-bootstrap-annuity-performance-subsystem"
    ]

    object_payload = yaml.safe_load(
        (registry_root / "objects" / "obj-annuity-performance-manual-entry.yaml").read_text(
            encoding="utf-8"
        )
    )
    assert object_payload["object_id"] == "obj-annuity-performance-manual-entry"
    assert object_payload["compiled_from_claims"] == [
        "claim-wave-2026-04-16-registry-bootstrap-annuity-performance-object"
    ]

    edge_payload = yaml.safe_load(
        (registry_root / "edges" / "execution-to-object.yaml").read_text(encoding="utf-8")
    )
    assert edge_payload["edges"][0]["from_id"] == (
        "ep-manual-cli-entrypoints-annuity-performance-manual-entry"
    )
    assert edge_payload["edges"][0]["to_id"] == "obj-annuity-performance-manual-entry"

    candidate_payload = yaml.safe_load(
        (registry_root / "candidates" / "subsystem-candidates.yaml").read_text(
            encoding="utf-8"
        )
    )
    assert candidate_payload["subsystem_candidates"][0]["candidate_id"] == (
        "cand-subsystem-annuity-performance-manual-entry"
    )

    manifest = json.loads((registry_root / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["generated_canonical_files"] == sorted(result.written_files)
    assert manifest["compiled_claim_ids"] == result.compiled_claim_ids


def test_compile_claim_artifacts_rejects_non_claim_paths(tmp_path: Path) -> None:
    registry_root = tmp_path / "legacy-semantic-map"
    bootstrap_semantic_map(registry_root)

    rogue_claim = registry_root / "rogue.yaml"
    rogue_claim.write_text("claim_id: rogue\n", encoding="utf-8")

    with pytest.raises(ValueError, match="must live under claims/"):
        compile_claim_artifacts(registry_root, [rogue_claim])

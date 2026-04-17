from __future__ import annotations

import json
from pathlib import Path

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
from scripts.legacy_semantic_map.reporting import generate_reports


def _write_yaml(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        yaml.safe_dump(payload, sort_keys=False, allow_unicode=False),
        encoding="utf-8",
    )


def _execution_claim(wave_id: str, source_ref: str, path_id: str, domain: str) -> ClaimArtifact:
    source_type = "legacy_code" if source_ref.startswith("src/") else "legacy_doc"
    return ClaimArtifact(
        claim_id=f"claim-{wave_id}-{domain}-execution",
        wave_id=wave_id,
        claim_scope="execution",
        claim_target_id=path_id,
        sources_read=[ClaimSourceRecord(source_ref=source_ref, source_type=source_type, note=f"Execution evidence for {domain}.")],
        objects_discovered=[
            ClaimDiscoveredObjectRecord(
                object_id=f"obj-{domain}",
                title=f"{domain} object".replace("-", " ").title(),
                summary=f"Object discovered for {domain}.",
                source_refs=[source_ref],
                source_type=source_type,
                claim_type="direct_observation",
                evidence_strength="strong",
                coverage_state="mapped",
                confidence="high",
                last_verified="2026-04-17",
                open_questions=[],
            )
        ],
        edges_added=[
            ClaimEdgeRecord(
                from_id=path_id,
                to_id=f"obj-{domain}",
                relationship="discovers_object",
                source_refs=[source_ref],
                source_type=source_type,
                claim_type="direct_observation",
                evidence_strength="strong",
                coverage_state="mapped",
                confidence="high",
                last_verified="2026-04-17",
                open_questions=[],
            )
        ],
        candidates_raised=[],
        open_questions=[],
        compiled_into=[],
        submitted_at="2026-04-17T00:00:00Z",
    )


def _object_claim(wave_id: str, source_ref: str, domain: str) -> ClaimArtifact:
    source_type = "legacy_code" if source_ref.startswith("src/") else "legacy_doc"
    return ClaimArtifact(
        claim_id=f"claim-{wave_id}-{domain}-object",
        wave_id=wave_id,
        claim_scope="objects",
        claim_target_id=f"obj-{domain}",
        sources_read=[ClaimSourceRecord(source_ref=source_ref, source_type=source_type, note=f"Object evidence for {domain}.")],
        objects_discovered=[
            ClaimDiscoveredObjectRecord(
                object_id=f"obj-{domain}",
                title=f"{domain} object".replace("-", " ").title(),
                summary=f"Object discovered for {domain}.",
                source_refs=[source_ref],
                source_type=source_type,
                claim_type="direct_observation",
                evidence_strength="strong",
                coverage_state="mapped",
                confidence="high",
                last_verified="2026-04-17",
                open_questions=[],
            )
        ],
        edges_added=[],
        candidates_raised=[],
        open_questions=[],
        compiled_into=[],
        submitted_at="2026-04-17T00:10:00Z",
    )


def _runtime_candidate(wave_id: str) -> ClaimCandidateRecord:
    return ClaimCandidateRecord(
        candidate_id="cand-object-runtime-follow-up",
        candidate_type="object",
        proposed_name="runtime-follow-up",
        reason="Needs follow-up analysis.",
        trigger_files=["src/work_data_hub/cli/etl/domain_validation.py"],
        source_type="legacy_code",
        claim_type="direct_observation",
        confidence="medium",
        priority="high",
        triage_status="new",
        first_seen_wave=wave_id,
        last_verified="2026-04-17",
    )


def test_reporting_pipeline_generates_current_and_wave_reports_from_compiled_claims(tmp_path: Path) -> None:
    registry_root = tmp_path / "legacy-semantic-map"
    bootstrap_semantic_map(registry_root)

    _write_yaml(
        registry_root / "sources" / "families.yaml",
        {
            "seeded_high_priority_source_families": [
                {
                    "family_id": "legacy-domain-capability-maps",
                    "title": "Legacy domain capability maps",
                    "status": "seeded",
                    "coverage_state": "seeded",
                    "source_ref_prefixes": ["docs/domains/"],
                },
                {
                    "family_id": "legacy-operator-runtime-surfaces",
                    "title": "Legacy operator runtime surfaces",
                    "status": "seeded",
                    "coverage_state": "seeded",
                    "source_ref_prefixes": ["src/work_data_hub/cli/"],
                },
            ]
        },
    )
    _write_yaml(
        registry_root / "waves" / "index.yaml",
        {
            "active_wave_id": "wave-2026-04-17-reporting",
            "waves": [
                {
                    "wave_id": "wave-2026-04-16-registry-bootstrap",
                    "title": "Registry bootstrap",
                    "status": "closed",
                    "wave_ordinal": 1,
                    "opened_at": "2026-04-16",
                    "closed_at": "2026-04-16",
                    "seeded_entry_surfaces": ["annuity_performance"],
                    "seeded_high_priority_source_families": ["legacy-domain-capability-maps"],
                    "admitted_subsystems": [],
                    "durable_wiki_targets_accepted": True,
                    "findings_disposition_complete": True,
                    "depends_on_active_wave_working_state": False,
                },
                {
                    "wave_id": "wave-2026-04-17-reporting",
                    "title": "Reporting",
                    "status": "active",
                    "wave_ordinal": 2,
                    "opened_at": "2026-04-17",
                    "closed_at": None,
                    "seeded_entry_surfaces": ["annuity_performance", "reference_sync"],
                    "seeded_high_priority_source_families": [
                        "legacy-domain-capability-maps",
                        "legacy-operator-runtime-surfaces",
                    ],
                    "admitted_subsystems": [],
                    "durable_wiki_targets_accepted": False,
                    "findings_disposition_complete": False,
                    "depends_on_active_wave_working_state": False,
                },
            ],
        },
    )

    claims = [
        _execution_claim(
            "wave-2026-04-17-reporting",
            "docs/domains/annuity_performance-capability-map.md",
            "ep-manual-cli-entrypoints-annuity-performance-manual-entry",
            "annuity-performance",
        ),
        ClaimArtifact(
                claim_id="claim-wave-2026-04-17-reporting-reference-sync-execution",
                wave_id="wave-2026-04-17-reporting",
                claim_scope="execution",
                claim_target_id="ep-scheduled-orchestrated-entrypoints-reference-sync-manual-entry",
            sources_read=[
                ClaimSourceRecord(
                    source_ref="src/work_data_hub/cli/etl/domain_validation.py",
                    source_type="legacy_code",
                    note="Execution evidence for reference sync.",
                )
            ],
            objects_discovered=[
                ClaimDiscoveredObjectRecord(
                    object_id="obj-reference-sync",
                    title="Reference sync object",
                    summary="Object discovered for reference sync.",
                    source_refs=["src/work_data_hub/cli/etl/domain_validation.py"],
                    source_type="legacy_code",
                    claim_type="direct_observation",
                    evidence_strength="strong",
                    coverage_state="mapped",
                    confidence="high",
                    last_verified="2026-04-17",
                    open_questions=[],
                )
            ],
            edges_added=[
                    ClaimEdgeRecord(
                        from_id="ep-scheduled-orchestrated-entrypoints-reference-sync-manual-entry",
                        to_id="obj-reference-sync",
                    relationship="discovers_object",
                    source_refs=["src/work_data_hub/cli/etl/domain_validation.py"],
                    source_type="legacy_code",
                    claim_type="direct_observation",
                    evidence_strength="strong",
                    coverage_state="mapped",
                    confidence="high",
                    last_verified="2026-04-17",
                    open_questions=[],
                )
            ],
            candidates_raised=[_runtime_candidate("wave-2026-04-17-reporting")],
            open_questions=[],
            compiled_into=[],
            submitted_at="2026-04-17T00:05:00Z",
        ),
        _object_claim("wave-2026-04-17-reporting", "docs/domains/annuity_performance-capability-map.md", "annuity-performance"),
        _object_claim("wave-2026-04-17-reporting", "src/work_data_hub/cli/etl/domain_validation.py", "reference-sync"),
    ]
    claim_paths = [write_claim_artifact(registry_root, claim) for claim in claims]
    compile_claim_artifacts(registry_root, claim_paths)

    result = generate_reports(registry_root)

    coverage = json.loads(result.current_coverage_report.read_text(encoding="utf-8"))
    integrity = json.loads(result.current_integrity_report.read_text(encoding="utf-8"))
    assert coverage["wave_status"] == "green"
    assert coverage["entrypoint_coverage_pct"] == 100.0
    assert coverage["high_priority_source_family_coverage_pct"] == 100.0
    assert coverage["stale_high_priority_candidate_count"] == 0
    assert integrity["closeout_ready"] is False
    assert integrity["blocking_reasons"] == [
        "durable_wiki_targets_not_accepted",
        "findings_disposition_incomplete",
    ]
    assert result.wave_coverage_report.exists()
    assert result.wave_integrity_report.exists()

    first_payload = result.current_coverage_report.read_text(encoding="utf-8")
    second_result = generate_reports(registry_root)
    assert second_result.current_coverage_report.read_text(encoding="utf-8") == first_payload

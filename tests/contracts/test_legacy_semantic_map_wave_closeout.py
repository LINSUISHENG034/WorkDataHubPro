from __future__ import annotations

import json
from pathlib import Path

import yaml

from scripts.legacy_semantic_map.bootstrap import bootstrap_semantic_map
from scripts.legacy_semantic_map.reporting import generate_reports

from tests.contracts.test_legacy_semantic_map_reporting import _configure_registry


def test_generate_reports_detects_mutated_closed_wave_claims(tmp_path: Path) -> None:
    registry_root = tmp_path / "legacy-semantic-map"
    bootstrap_semantic_map(registry_root)
    _configure_registry(
        registry_root,
        active_wave_id="wave-2026-04-16-audit",
        active_wave_ordinal=2,
        wave_overrides=[
            {
                "wave_id": "wave-2026-04-15-bootstrap",
                "title": "Bootstrap",
                "status": "closed",
                "wave_ordinal": 1,
                "opened_at": "2026-04-15",
                "closed_at": "2026-04-15",
                "seeded_entry_surfaces": ["annuity_performance"],
                "seeded_high_priority_source_families": ["legacy-domain-capability-maps"],
                "admitted_subsystems": [],
                "durable_wiki_targets_accepted": True,
                "findings_disposition_complete": True,
                "depends_on_active_wave_working_state": False,
            },
            {
                "wave_id": "wave-2026-04-16-audit",
                "title": "Audit",
                "status": "closed",
                "wave_ordinal": 2,
                "opened_at": "2026-04-16",
                "closed_at": "2026-04-16",
                "seeded_entry_surfaces": ["annuity_performance", "reference_sync"],
                "seeded_high_priority_source_families": [
                    "legacy-domain-capability-maps",
                    "legacy-operator-runtime-surfaces",
                ],
                "admitted_subsystems": [],
                "durable_wiki_targets_accepted": True,
                "findings_disposition_complete": True,
                "depends_on_active_wave_working_state": False,
            },
        ],
    )

    first_result = generate_reports(registry_root, wave_id="wave-2026-04-16-audit")
    first_integrity = json.loads(first_result.wave_integrity_report.read_text(encoding="utf-8"))
    assert first_integrity["immutability_check_passed"] is True
    assert first_integrity["closeout_ready"] is True
    assert first_integrity["archive_ready"] is True

    claim_file = next((registry_root / "claims" / "wave-2026-04-16-audit").rglob("*.yaml"))
    claim_file.write_text(claim_file.read_text(encoding="utf-8") + "\n# rewritten\n", encoding="utf-8")

    second_result = generate_reports(registry_root, wave_id="wave-2026-04-16-audit")
    second_integrity = json.loads(second_result.wave_integrity_report.read_text(encoding="utf-8"))
    assert second_integrity["immutability_check_passed"] is False
    assert second_integrity["closeout_ready"] is False
    assert second_integrity["archive_ready"] is False
    assert second_integrity["mutable_claim_ids_detected"]
    assert "mutable_accepted_claims_detected" in second_integrity["blocking_reasons"]


def test_generate_reports_rejects_manifest_claim_mismatches(tmp_path: Path) -> None:
    registry_root = tmp_path / "legacy-semantic-map"
    bootstrap_semantic_map(registry_root)
    _configure_registry(registry_root)

    manifest_path = registry_root / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["compiled_claim_ids"] = ["claim-does-not-exist"]
    manifest["compiled_claims_by_wave"] = {
        "wave-2026-04-17-reporting": ["claim-does-not-exist"]
    }
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    result = generate_reports(registry_root)
    integrity = json.loads(result.current_integrity_report.read_text(encoding="utf-8"))
    assert integrity["closeout_ready"] is False
    assert integrity["missing_claim_ids"] == ["claim-does-not-exist"]
    assert "missing_compiled_claim_ids" in integrity["blocking_reasons"]


def test_generate_reports_ignores_late_uncompiled_draft_claims_for_immutability(tmp_path: Path) -> None:
    registry_root = tmp_path / "legacy-semantic-map"
    bootstrap_semantic_map(registry_root)
    _configure_registry(
        registry_root,
        active_wave_id="wave-2026-04-16-audit",
        active_wave_ordinal=2,
        wave_overrides=[
            {
                "wave_id": "wave-2026-04-15-bootstrap",
                "title": "Bootstrap",
                "status": "closed",
                "wave_ordinal": 1,
                "opened_at": "2026-04-15",
                "closed_at": "2026-04-15",
                "seeded_entry_surfaces": ["annuity_performance"],
                "seeded_high_priority_source_families": ["legacy-domain-capability-maps"],
                "admitted_subsystems": [],
                "durable_wiki_targets_accepted": True,
                "findings_disposition_complete": True,
                "depends_on_active_wave_working_state": False,
            },
            {
                "wave_id": "wave-2026-04-16-audit",
                "title": "Audit",
                "status": "closed",
                "wave_ordinal": 2,
                "opened_at": "2026-04-16",
                "closed_at": "2026-04-16",
                "seeded_entry_surfaces": ["annuity_performance", "reference_sync"],
                "seeded_high_priority_source_families": [
                    "legacy-domain-capability-maps",
                    "legacy-operator-runtime-surfaces",
                ],
                "admitted_subsystems": [],
                "durable_wiki_targets_accepted": True,
                "findings_disposition_complete": True,
                "depends_on_active_wave_working_state": False,
            },
        ],
    )

    first_result = generate_reports(registry_root, wave_id="wave-2026-04-16-audit")
    first_integrity = json.loads(first_result.wave_integrity_report.read_text(encoding="utf-8"))
    assert first_integrity["closeout_ready"] is True
    assert first_integrity["immutability_check_passed"] is True

    late_claim = (
        registry_root
        / "claims"
        / "wave-2026-04-16-audit"
        / "objects"
        / "late-draft-claim.yaml"
    )
    late_claim.parent.mkdir(parents=True, exist_ok=True)
    late_claim.write_text(
        """claim_id: late-draft-claim
wave_id: wave-2026-04-16-audit
claim_scope: objects
claim_target_id: obj-late-draft
sources_read: []
objects_discovered: []
edges_added: []
candidates_raised: []
open_questions: []
compiled_into: []
submitted_at: '2026-04-17T00:00:00Z'
""",
        encoding="utf-8",
    )

    second_result = generate_reports(registry_root, wave_id="wave-2026-04-16-audit")
    second_integrity = json.loads(second_result.wave_integrity_report.read_text(encoding="utf-8"))
    assert second_integrity["immutability_check_passed"] is True
    assert second_integrity["closeout_ready"] is True
    assert second_integrity["mutable_claim_ids_detected"] == []


def test_generate_reports_requires_downstream_dependencies_to_clear_before_archive(tmp_path: Path) -> None:
    registry_root = tmp_path / "legacy-semantic-map"
    bootstrap_semantic_map(registry_root)
    _configure_registry(
        registry_root,
        active_wave_id="wave-2026-04-16-audit",
        active_wave_ordinal=2,
        wave_overrides=[
            {
                "wave_id": "wave-2026-04-16-audit",
                "title": "Audit",
                "status": "closed",
                "wave_ordinal": 2,
                "opened_at": "2026-04-16",
                "closed_at": "2026-04-16",
                "seeded_entry_surfaces": ["annuity_performance", "reference_sync"],
                "seeded_high_priority_source_families": [
                    "legacy-domain-capability-maps",
                    "legacy-operator-runtime-surfaces",
                ],
                "admitted_subsystems": [],
                "durable_wiki_targets_accepted": True,
                "findings_disposition_complete": True,
                "depends_on_active_wave_working_state": True,
            },
            {
                "wave_id": "wave-2026-04-17-reporting",
                "title": "Reporting",
                "status": "active",
                "wave_ordinal": 3,
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
    )

    result = generate_reports(registry_root, wave_id="wave-2026-04-16-audit")
    integrity = json.loads(result.wave_integrity_report.read_text(encoding="utf-8"))
    assert integrity["closeout_ready"] is True
    assert integrity["archive_ready"] is False
    assert "active_wave_dependency_open" in integrity["blocking_reasons"]


def test_historical_closeout_ignores_unrelated_future_wave_manifest_gaps(tmp_path: Path) -> None:
    registry_root = tmp_path / "legacy-semantic-map"
    bootstrap_semantic_map(registry_root)
    _configure_registry(registry_root)

    historical_object_claim_id = "claim-audit-obj-domain"
    historical_execution_claim_id = "claim-audit-entry-annuity"
    missing_historical_claim_id = "claim-audit-missing-runtime"
    for claim_id, claim_scope, claim_target_id in (
        (historical_object_claim_id, "objects", "obj-domain"),
        (
            historical_execution_claim_id,
            "execution",
            "ep-manual-cli-entrypoints-annuity-performance-entry",
        ),
    ):
        claim_path = (
            registry_root / "claims" / "wave-2026-04-16-audit" / claim_scope / f"{claim_id}.yaml"
        )
        claim_path.parent.mkdir(parents=True, exist_ok=True)
        claim_path.write_text(
            f"""claim_id: {claim_id}
wave_id: wave-2026-04-16-audit
claim_scope: {claim_scope}
claim_target_id: {claim_target_id}
sources_read:
- source_ref: docs/domains/annuity_performance-capability-map.md
  source_type: legacy_doc
  note: fixture source
objects_discovered: []
edges_added: []
candidates_raised: []
open_questions: []
compiled_into: []
submitted_at: '2026-04-16T00:00:00Z'
""",
            encoding="utf-8",
        )

    object_payload = yaml.safe_load(
        (registry_root / "objects" / "obj-domain.yaml").read_text(encoding="utf-8")
    )
    object_payload["compiled_from_claims"] = [
        historical_object_claim_id,
        *object_payload["compiled_from_claims"],
    ]
    (registry_root / "objects" / "obj-domain.yaml").write_text(
        yaml.safe_dump(object_payload, sort_keys=False, allow_unicode=False),
        encoding="utf-8",
    )

    execution_payload = yaml.safe_load(
        (
            registry_root
            / "execution"
            / "paths"
            / "ep-manual-cli-entrypoints-annuity-performance-entry.yaml"
        ).read_text(encoding="utf-8")
    )
    execution_payload["compiled_from_claims"] = [
        historical_execution_claim_id,
        *execution_payload["compiled_from_claims"],
    ]
    (
        registry_root
        / "execution"
        / "paths"
        / "ep-manual-cli-entrypoints-annuity-performance-entry.yaml"
    ).write_text(
        yaml.safe_dump(execution_payload, sort_keys=False, allow_unicode=False),
        encoding="utf-8",
    )

    for edge_path in (
        registry_root / "edges" / "source-to-node.yaml",
        registry_root / "edges" / "execution-to-object.yaml",
    ):
        payload = yaml.safe_load(edge_path.read_text(encoding="utf-8"))
        payload["edges"][0]["compiled_from_claims"] = [
            historical_execution_claim_id,
            *payload["edges"][0]["compiled_from_claims"],
        ]
        edge_path.write_text(
            yaml.safe_dump(payload, sort_keys=False, allow_unicode=False),
            encoding="utf-8",
        )

    manifest_path = registry_root / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["compiled_claim_ids"] = sorted(
        [
            historical_execution_claim_id,
            historical_object_claim_id,
            missing_historical_claim_id,
            "claim-reporting-missing-future",
        ]
    )
    manifest["compiled_claims_by_wave"] = {
        "wave-2026-04-16-audit": sorted(
            [
                historical_execution_claim_id,
                historical_object_claim_id,
                missing_historical_claim_id,
            ]
        ),
        "wave-2026-04-17-reporting": ["claim-reporting-missing-future"],
    }
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    result = generate_reports(registry_root, wave_id="wave-2026-04-16-audit")
    integrity = json.loads(result.wave_integrity_report.read_text(encoding="utf-8"))
    assert integrity["required_claim_ids"] == sorted([historical_execution_claim_id, historical_object_claim_id])
    assert integrity["missing_claim_ids"] == [missing_historical_claim_id]

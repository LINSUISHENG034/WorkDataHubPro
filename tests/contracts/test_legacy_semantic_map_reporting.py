from __future__ import annotations

import json
from pathlib import Path

import yaml

from scripts.legacy_semantic_map.bootstrap import bootstrap_semantic_map
from scripts.legacy_semantic_map.reporting import generate_reports


def _write_yaml(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        yaml.safe_dump(payload, sort_keys=False, allow_unicode=False),
        encoding="utf-8",
    )


def _write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def _claim_payload(*, claim_id: str, wave_id: str, claim_scope: str, claim_target_id: str) -> dict[str, object]:
    return {
        "claim_id": claim_id,
        "wave_id": wave_id,
        "claim_scope": claim_scope,
        "claim_target_id": claim_target_id,
        "sources_read": [
            {
                "source_ref": "docs/domains/annuity_performance-capability-map.md",
                "source_type": "legacy_doc",
                "note": "fixture source",
            }
        ],
        "objects_discovered": [
            {
                "object_id": "obj-claim-backed-object",
                "title": "Claim backed object",
                "summary": "Fixture object for report generation.",
                "source_refs": ["docs/domains/annuity_performance-capability-map.md"],
                "source_type": "legacy_doc",
                "claim_type": "direct_observation",
                "evidence_strength": "strong",
                "coverage_state": "mapped",
                "confidence": "high",
                "last_verified": "2026-04-17",
                "open_questions": [],
            }
        ],
        "edges_added": [],
        "candidates_raised": [],
        "open_questions": [],
        "compiled_into": [],
        "submitted_at": "2026-04-17T00:00:00Z",
    }


def _write_claim(
    registry_root: Path,
    *,
    wave_id: str,
    claim_scope: str,
    claim_id: str,
    claim_target_id: str,
) -> None:
    directory = registry_root / "claims" / wave_id / claim_scope
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"{claim_id}.yaml"
    _write_yaml(
        path,
        _claim_payload(
            claim_id=claim_id,
            wave_id=wave_id,
            claim_scope=claim_scope,
            claim_target_id=claim_target_id,
        ),
    )


def _configure_registry(
    registry_root: Path,
    *,
    active_wave_id: str = "wave-2026-04-17-reporting",
    active_wave_ordinal: int = 3,
    execution_paths: list[dict[str, object]] | None = None,
    source_edges: list[dict[str, object]] | None = None,
    object_ids: list[str] | None = None,
    edge_pairs: list[tuple[str, str]] | None = None,
    candidates: list[dict[str, object]] | None = None,
    wave_overrides: list[dict[str, object]] | None = None,
) -> None:
    _write_yaml(
        registry_root / "execution" / "entry-surfaces.yaml",
        {
            "seeded_entry_surfaces": [
                {
                    "entry_family": "manual_cli_entrypoints",
                    "surface_id": "annuity_performance",
                    "title": "Annuity performance",
                    "status": "seeded",
                    "coverage_state": "seeded",
                },
                {
                    "entry_family": "scheduled_orchestrated_entrypoints",
                    "surface_id": "reference_sync",
                    "title": "Reference sync",
                    "status": "seeded",
                    "coverage_state": "seeded",
                },
            ]
        },
    )
    _write_yaml(
        registry_root / "sources" / "families.yaml",
        {
            "seeded_high_priority_source_families": [
                {
                    "family_id": "legacy-domain-capability-maps",
                    "title": "Legacy domain capability maps",
                    "status": "seeded",
                    "coverage_state": "seeded",
                    "source_ref_prefixes": [
                        "docs/domains/",
                        "docs/guides/domain-migration/",
                    ],
                },
                {
                    "family_id": "legacy-operator-runtime-surfaces",
                    "title": "Legacy operator runtime surfaces",
                    "status": "seeded",
                    "coverage_state": "seeded",
                    "source_ref_prefixes": [
                        "src/work_data_hub/cli/",
                        "src/work_data_hub/orchestration/",
                    ],
                },
            ]
        },
    )

    waves = wave_overrides or [
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
        {
            "wave_id": active_wave_id,
            "title": "Reporting",
            "status": "active",
            "wave_ordinal": active_wave_ordinal,
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
    ]
    _write_yaml(registry_root / "waves" / "index.yaml", {"active_wave_id": active_wave_id, "waves": waves})

    object_ids = object_ids or ["obj-domain", "obj-runtime"]
    _write_yaml(
        registry_root / "objects" / "index.yaml",
        {"objects": [{"object_id": object_id, "path": f"objects/{object_id}.yaml"} for object_id in object_ids]},
    )
    for object_id in object_ids:
        _write_yaml(
            registry_root / "objects" / f"{object_id}.yaml",
            {
                "object_id": object_id,
                "title": object_id.replace("-", " ").title(),
                "compiled_from_claims": [f"claim-{active_wave_id}-{object_id}"],
                "coverage_state": "mapped",
            },
        )
        _write_claim(
            registry_root,
            wave_id=active_wave_id,
            claim_scope="objects",
            claim_id=f"claim-{active_wave_id}-{object_id}",
            claim_target_id=object_id,
        )

    execution_paths = execution_paths or [
        {
            "path_id": "ep-manual-cli-entrypoints-annuity-performance-entry",
            "entry_surface": "manual_cli_entrypoints",
            "domain_or_surface": "annuity_performance",
            "compiled_from_claims": [f"claim-{active_wave_id}-entry-annuity"],
        },
        {
            "path_id": "ep-scheduled-orchestrated-entrypoints-reference-sync-entry",
            "entry_surface": "scheduled_orchestrated_entrypoints",
            "domain_or_surface": "reference_sync",
            "compiled_from_claims": [f"claim-{active_wave_id}-entry-reference-sync"],
        },
    ]
    execution_paths_dir = registry_root / "execution" / "paths"
    for path in execution_paths_dir.glob("*.yaml"):
        path.unlink()
    for payload in execution_paths:
        _write_yaml(execution_paths_dir / f"{payload['path_id']}.yaml", payload)
        _write_claim(
            registry_root,
            wave_id=active_wave_id,
            claim_scope="execution",
            claim_id=payload["compiled_from_claims"][0],
            claim_target_id=payload["path_id"],
        )

    source_edges = source_edges or [
        {
            "from_id": "docs/domains/annuity_performance-capability-map.md",
            "to_id": "obj-domain",
            "relationship": "supports_claim_target",
            "compiled_from_claims": [f"claim-{active_wave_id}-entry-annuity"],
        },
        {
            "from_id": "src/work_data_hub/cli/etl/domain_validation.py",
            "to_id": "obj-runtime",
            "relationship": "supports_claim_target",
            "compiled_from_claims": [f"claim-{active_wave_id}-entry-reference-sync"],
        },
    ]
    _write_yaml(registry_root / "edges" / "source-to-node.yaml", {"edges": source_edges})

    edge_pairs = edge_pairs or [
        ("ep-manual-cli-entrypoints-annuity-performance-entry", "obj-domain"),
        ("ep-scheduled-orchestrated-entrypoints-reference-sync-entry", "obj-runtime"),
        ("obj-domain", "obj-runtime"),
    ]
    execution_to_object = []
    object_to_object = []
    for from_id, to_id in edge_pairs:
        payload = {
            "from_id": from_id,
            "to_id": to_id,
            "relationship": "connected_to",
            "compiled_from_claims": [f"claim-{active_wave_id}-edge-{from_id}-{to_id}"],
        }
        if from_id.startswith("obj-"):
            object_to_object.append(payload)
        else:
            execution_to_object.append(payload)
    _write_yaml(registry_root / "edges" / "execution-to-object.yaml", {"edges": execution_to_object})
    _write_yaml(registry_root / "edges" / "object-to-object.yaml", {"edges": object_to_object})
    _write_yaml(registry_root / "edges" / "execution-to-subsystem.yaml", {"edges": []})
    _write_yaml(registry_root / "edges" / "subsystem-to-object.yaml", {"edges": []})

    candidates = candidates or []
    _write_yaml(registry_root / "candidates" / "object-candidates.yaml", {"object_candidates": candidates})
    _write_yaml(registry_root / "candidates" / "subsystem-candidates.yaml", {"subsystem_candidates": []})

    manifest_claim_ids = sorted(
        {
            claim_id
            for payload in execution_paths
            for claim_id in payload.get("compiled_from_claims", [])
        }
        | {
            claim_id
            for payload in source_edges
            for claim_id in payload.get("compiled_from_claims", [])
        }
        | {f"claim-{active_wave_id}-{object_id}" for object_id in object_ids}
    )
    generated_canonical_files = sorted(
        [f"execution/paths/{payload['path_id']}.yaml" for payload in execution_paths]
        + ["objects/index.yaml"]
        + [f"objects/{object_id}.yaml" for object_id in object_ids]
        + [
            "edges/execution-to-object.yaml",
            "edges/execution-to-subsystem.yaml",
            "edges/object-to-object.yaml",
            "edges/source-to-node.yaml",
            "edges/subsystem-to-object.yaml",
            "candidates/object-candidates.yaml",
            "candidates/subsystem-candidates.yaml",
        ]
    )
    _write_json(
        registry_root / "manifest.json",
        {
            "artifact": "legacy-semantic-map-registry",
            "canonical_seed_sources": [
                "execution/entry-surfaces.yaml",
                "sources/families.yaml",
                "waves/index.yaml",
            ],
            "generated_canonical_files": generated_canonical_files,
            "compiled_claim_ids": manifest_claim_ids,
            "compiled_claims_by_wave": {
                active_wave_id: manifest_claim_ids,
            },
        },
    )


def test_generate_reports_classifies_green_and_writes_expected_metric_fields(tmp_path: Path) -> None:
    registry_root = tmp_path / "legacy-semantic-map"
    bootstrap_semantic_map(registry_root)
    _configure_registry(registry_root)

    result = generate_reports(registry_root)

    coverage = json.loads(result.current_coverage_report.read_text(encoding="utf-8"))
    integrity = json.loads(result.current_integrity_report.read_text(encoding="utf-8"))
    assert result.wave_id == "wave-2026-04-17-reporting"
    assert coverage["wave_status"] == "green"
    assert coverage["entrypoint_coverage_pct"] == 100.0
    assert coverage["high_priority_source_family_coverage_pct"] == 100.0
    assert coverage["object_edge_coverage_pct"] == 100.0
    assert coverage["orphan_high_priority_source_count"] == 0
    assert coverage["stale_high_priority_candidate_count"] == 0
    assert coverage["untriaged_candidate_age_by_wave"] == {
        "max": 0,
        "count_gt_0": 0,
        "count_gt_1": 0,
        "by_candidate": {},
    }
    assert integrity["immutability_check_passed"] is True
    assert integrity["closeout_ready"] is False
    assert integrity["archive_ready"] is False
    assert integrity["blocking_reasons"] == [
        "durable_wiki_targets_not_accepted",
        "findings_disposition_incomplete",
    ]
    assert result.wave_coverage_report.exists()
    assert result.wave_integrity_report.exists()


def test_generate_reports_returns_yellow_when_green_thresholds_are_not_met(tmp_path: Path) -> None:
    registry_root = tmp_path / "legacy-semantic-map"
    bootstrap_semantic_map(registry_root)
    _configure_registry(
        registry_root,
        object_ids=["obj-domain", "obj-runtime", "obj-unconnected"],
        edge_pairs=[
            ("ep-manual-cli-entrypoints-annuity-performance-entry", "obj-domain"),
            ("ep-scheduled-orchestrated-entrypoints-reference-sync-entry", "obj-runtime"),
        ],
    )

    result = generate_reports(registry_root)

    coverage = json.loads(result.current_coverage_report.read_text(encoding="utf-8"))
    assert coverage["wave_status"] == "yellow"
    assert coverage["entrypoint_coverage_pct"] == 100.0
    assert coverage["high_priority_source_family_coverage_pct"] == 100.0
    assert coverage["object_edge_coverage_pct"] < 95.0


def test_generate_reports_returns_red_for_stale_candidate_and_orphaned_source_family(tmp_path: Path) -> None:
    registry_root = tmp_path / "legacy-semantic-map"
    bootstrap_semantic_map(registry_root)
    _configure_registry(
        registry_root,
        active_wave_id="wave-2026-04-18-closeout",
        active_wave_ordinal=4,
        source_edges=[
            {
                "from_id": "docs/domains/annuity_performance-capability-map.md",
                "to_id": "obj-domain",
                "relationship": "supports_claim_target",
                "compiled_from_claims": ["claim-wave-2026-04-18-closeout-entry-annuity"],
            }
        ],
        candidates=[
            {
                "candidate_id": "cand-object-stale-high-priority",
                "proposed_name": "Stale candidate",
                "candidate_type": "object",
                "reason": "still unresolved",
                "trigger_files": ["src/work_data_hub/cli/etl/domain_validation.py"],
                "source_type": "legacy_code",
                "claim_type": "compiled_summary",
                "confidence": "high",
                "priority": "high",
                "triage_status": "new",
                "first_seen_wave": "wave-2026-04-15-bootstrap",
                "last_verified": "2026-04-17",
                "compiled_from_claims": ["claim-wave-2026-04-18-closeout-entry-reference-sync"],
            }
        ],
    )

    result = generate_reports(registry_root)

    coverage = json.loads(result.current_coverage_report.read_text(encoding="utf-8"))
    assert coverage["wave_status"] == "red"
    assert coverage["orphan_high_priority_source_count"] == 1
    assert coverage["stale_high_priority_candidate_count"] == 1
    assert coverage["untriaged_candidate_age_by_wave"]["max"] == 3
    assert coverage["untriaged_candidate_age_by_wave"]["count_gt_1"] == 1
    assert coverage["untriaged_candidate_age_by_wave"]["by_candidate"] == {
        "cand-object-stale-high-priority": 3
    }


def test_generate_reports_ignores_non_high_priority_stale_candidates(tmp_path: Path) -> None:
    registry_root = tmp_path / "legacy-semantic-map"
    bootstrap_semantic_map(registry_root)
    _configure_registry(
        registry_root,
        active_wave_id="wave-2026-04-18-closeout",
        active_wave_ordinal=4,
        candidates=[
            {
                "candidate_id": "cand-object-stale-medium-priority",
                "proposed_name": "Medium priority candidate",
                "candidate_type": "object",
                "reason": "still unresolved",
                "trigger_files": ["src/work_data_hub/cli/etl/domain_validation.py"],
                "source_type": "legacy_code",
                "claim_type": "compiled_summary",
                "confidence": "high",
                "priority": "medium",
                "triage_status": "new",
                "first_seen_wave": "wave-2026-04-15-bootstrap",
                "last_verified": "2026-04-17",
                "compiled_from_claims": ["claim-wave-2026-04-18-closeout-entry-reference-sync"],
            }
        ],
    )

    result = generate_reports(registry_root)
    coverage = json.loads(result.current_coverage_report.read_text(encoding="utf-8"))
    assert coverage["stale_high_priority_candidate_count"] == 0
    assert coverage["untriaged_candidate_age_by_wave"]["by_candidate"] == {}


def test_generate_reports_uses_wave_ordinals_not_dates_for_candidate_age(tmp_path: Path) -> None:
    registry_root = tmp_path / "legacy-semantic-map"
    bootstrap_semantic_map(registry_root)
    _configure_registry(
        registry_root,
        active_wave_ordinal=7,
        candidates=[
            {
                "candidate_id": "cand-object-wave-aged",
                "proposed_name": "Wave aged candidate",
                "candidate_type": "object",
                "reason": "untriaged",
                "trigger_files": ["src/work_data_hub/cli/etl/domain_validation.py"],
                "source_type": "legacy_code",
                "claim_type": "compiled_summary",
                "confidence": "high",
                "priority": "high",
                "triage_status": "new",
                "first_seen_wave": "wave-2026-04-16-audit",
                "last_verified": "1900-01-01",
                "compiled_from_claims": ["claim-wave-2026-04-17-reporting-entry-reference-sync"],
            }
        ],
        wave_overrides=[
            {
                "wave_id": "wave-2026-04-15-bootstrap",
                "title": "Bootstrap",
                "status": "closed",
                "wave_ordinal": 1,
                "opened_at": "2020-01-01",
                "closed_at": "2020-01-01",
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
                "opened_at": "2099-12-31",
                "closed_at": "2099-12-31",
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
            {
                "wave_id": "wave-2026-04-17-reporting",
                "title": "Reporting",
                "status": "active",
                "wave_ordinal": 7,
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

    result = generate_reports(registry_root)

    coverage = json.loads(result.current_coverage_report.read_text(encoding="utf-8"))
    assert coverage["untriaged_candidate_age_by_wave"]["by_candidate"] == {
        "cand-object-wave-aged": 5
    }
    assert coverage["stale_high_priority_candidate_count"] == 1


def test_historical_wave_candidate_age_uses_current_active_wave_ordinal(tmp_path: Path) -> None:
    registry_root = tmp_path / "legacy-semantic-map"
    bootstrap_semantic_map(registry_root)
    _configure_registry(
        registry_root,
        active_wave_ordinal=7,
        candidates=[
            {
                "candidate_id": "cand-historical-wave",
                "proposed_name": "Historical candidate",
                "candidate_type": "object",
                "reason": "untriaged",
                "trigger_files": ["src/work_data_hub/cli/etl/domain_validation.py"],
                "source_type": "legacy_code",
                "claim_type": "compiled_summary",
                "confidence": "high",
                "priority": "high",
                "triage_status": "new",
                "first_seen_wave": "wave-2026-04-16-audit",
                "last_verified": "1900-01-01",
                "compiled_from_claims": ["claim-wave-2026-04-17-reporting-entry-reference-sync"],
            }
        ],
        wave_overrides=[
            {
                "wave_id": "wave-2026-04-15-bootstrap",
                "title": "Bootstrap",
                "status": "closed",
                "wave_ordinal": 1,
                "opened_at": "2020-01-01",
                "closed_at": "2020-01-01",
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
            {
                "wave_id": "wave-2026-04-17-reporting",
                "title": "Reporting",
                "status": "active",
                "wave_ordinal": 7,
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

    historical_result = generate_reports(registry_root, wave_id="wave-2026-04-16-audit")
    historical_payload = json.loads(
        historical_result.wave_coverage_report.read_text(encoding="utf-8")
    )
    assert historical_payload["untriaged_candidate_age_by_wave"]["by_candidate"] == {
        "cand-historical-wave": 5
    }


def test_historical_wave_generation_does_not_overwrite_current_reports(tmp_path: Path) -> None:
    registry_root = tmp_path / "legacy-semantic-map"
    bootstrap_semantic_map(registry_root)
    _configure_registry(registry_root)

    current_result = generate_reports(registry_root)
    current_payload = json.loads(current_result.current_coverage_report.read_text(encoding="utf-8"))
    assert current_payload["wave_id"] == "wave-2026-04-17-reporting"

    historical_result = generate_reports(registry_root, wave_id="wave-2026-04-16-audit")
    current_after_historical = json.loads(
        current_result.current_coverage_report.read_text(encoding="utf-8")
    )
    historical_payload = json.loads(
        historical_result.wave_coverage_report.read_text(encoding="utf-8")
    )

    assert current_after_historical["wave_id"] == "wave-2026-04-17-reporting"
    assert historical_payload["wave_id"] == "wave-2026-04-16-audit"


def test_historical_wave_metrics_ignore_later_wave_edges(tmp_path: Path) -> None:
    registry_root = tmp_path / "legacy-semantic-map"
    bootstrap_semantic_map(registry_root)
    _configure_registry(registry_root)

    _write_claim(
        registry_root,
        wave_id="wave-2026-04-16-audit",
        claim_scope="objects",
        claim_id="claim-wave-2026-04-16-audit-obj-domain",
        claim_target_id="obj-domain",
    )
    object_payload = yaml.safe_load(
        (registry_root / "objects" / "obj-domain.yaml").read_text(encoding="utf-8")
    )
    object_payload["compiled_from_claims"] = [
        "claim-wave-2026-04-16-audit-obj-domain",
        *object_payload["compiled_from_claims"],
    ]
    _write_yaml(registry_root / "objects" / "obj-domain.yaml", object_payload)

    historical_result = generate_reports(registry_root, wave_id="wave-2026-04-16-audit")
    historical_payload = json.loads(
        historical_result.wave_coverage_report.read_text(encoding="utf-8")
    )

    assert historical_payload["high_priority_source_family_coverage_pct"] == 0.0
    assert historical_payload["orphan_high_priority_source_count"] == 2
    assert historical_payload["object_edge_coverage_pct"] == 0.0
    assert historical_payload["untriaged_candidate_age_by_wave"]["by_candidate"] == {}
    assert historical_payload["wave_status"] == "red"

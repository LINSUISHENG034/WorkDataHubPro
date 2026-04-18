from __future__ import annotations

import json
from pathlib import Path

import yaml

from scripts.legacy_semantic_map.bootstrap import bootstrap_semantic_map
from scripts.legacy_semantic_map.claims import (
    ClaimArtifact,
    ClaimSemanticFindingRecord,
    ClaimSourceRecord,
    write_claim_artifact,
)
from scripts.legacy_semantic_map.compiler import compile_claim_artifacts
from scripts.legacy_semantic_map.reporting import generate_reports


SUCCESSOR_WAVE_ID = "wave-2026-04-17-semantic-governance-reframe"


def _seed_successor_wave(registry_root: Path) -> None:
    payload = yaml.safe_load((registry_root / "waves" / "index.yaml").read_text(encoding="utf-8"))
    payload["active_wave_id"] = SUCCESSOR_WAVE_ID
    payload["waves"] = [
        {
            "wave_id": SUCCESSOR_WAVE_ID,
            "title": "Semantic governance reframe",
            "status": "active",
            "wave_ordinal": 4,
            "opened_at": "2026-04-17",
            "seeded_entry_surfaces": [],
            "seeded_high_priority_source_families": [],
            "admitted_subsystems": [],
            "durable_wiki_targets_accepted": False,
            "findings_disposition_complete": False,
            "depends_on_active_wave_working_state": False,
            "closed_at": None,
        }
    ]
    (registry_root / "waves" / "index.yaml").write_text(
        yaml.safe_dump(payload, sort_keys=False, allow_unicode=False),
        encoding="utf-8",
    )


def _run_successor_wave_reporting(tmp_path: Path) -> dict[str, str]:
    registry_root = tmp_path / "legacy-semantic-map"
    bootstrap_semantic_map(registry_root)
    _seed_successor_wave(registry_root)

    claim = ClaimArtifact(
        claim_id="claim-wave-2026-04-17-semantic-governance-reframe-customer-status-core",
        wave_id=SUCCESSOR_WAVE_ID,
        claim_scope="semantic",
        claim_target_id="sem-concept-customer-status",
        sources_read=[
            ClaimSourceRecord(
                source_ref="docs/business-background/客户主数据回填与状态来源分析.md",
                source_type="legacy_doc",
                note="Auxiliary-view fixture source.",
                workspace_id="legacy_work_data_hub",
                relative_path="docs/business-background/客户主数据回填与状态来源分析.md",
                semantic_authority="authoritative_semantic_source",
            )
        ],
        objects_discovered=[],
        edges_added=[],
        candidates_raised=[],
        semantic_findings=[
            ClaimSemanticFindingRecord(
                semantic_id="sem-concept-customer-status",
                semantic_node_type="semantic_concept",
                title="Customer status",
                summary="Customer status is a distinct semantic layer.",
                business_conclusion="Customer status is a distinct semantic layer.",
                primary_source_refs=["docs/business-background/客户主数据回填与状态来源分析.md"],
                supporting_source_refs=["docs/wiki-bi/concepts/customer-status.md"],
                semantic_authority="authoritative_semantic_source",
                durable_target_pages=["docs/wiki-bi/concepts/customer-status.md"],
                confidence="high",
                last_verified="2026-04-18",
                open_questions=[],
            )
        ],
        open_questions=[],
        compiled_into=["docs/wiki-bi/concepts/customer-status.md"],
        submitted_at="2026-04-18T00:00:00Z",
    )
    claim_path = write_claim_artifact(registry_root, claim)
    compile_claim_artifacts(registry_root, [claim_path])
    result = generate_reports(registry_root)
    return {
        "coverage_status_path": result.current_coverage_report.as_posix(),
        "integrity_status_path": result.current_integrity_report.as_posix(),
        "semantic_discovery_status_path": (
            registry_root
            / "reports"
            / "waves"
            / SUCCESSOR_WAVE_ID
            / "semantic-discovery-status.json"
        ).as_posix(),
        "semantic_readiness_status_path": (
            registry_root
            / "reports"
            / "waves"
            / SUCCESSOR_WAVE_ID
            / "semantic-readiness-status.json"
        ).as_posix(),
    }


def test_auxiliary_views_do_not_replace_authoritative_reports(tmp_path: Path) -> None:
    reports = _run_successor_wave_reporting(tmp_path)

    assert reports["coverage_status_path"].endswith("coverage-status.json")
    assert reports["integrity_status_path"].endswith("integrity-status.json")
    assert reports["semantic_discovery_status_path"].endswith("semantic-discovery-status.json")
    assert reports["semantic_readiness_status_path"].endswith("semantic-readiness-status.json")
    assert Path(reports["semantic_discovery_status_path"]).exists()
    assert Path(reports["semantic_readiness_status_path"]).exists()


def test_auxiliary_views_surface_blocked_and_handoff_ready_semantic_ids(
    tmp_path: Path,
) -> None:
    registry_root = tmp_path / "legacy-semantic-map"
    bootstrap_semantic_map(registry_root)
    _seed_successor_wave(registry_root)

    stable_claim = ClaimArtifact(
        claim_id="claim-wave-2026-04-17-semantic-governance-reframe-customer-status-core",
        wave_id=SUCCESSOR_WAVE_ID,
        claim_scope="semantic",
        claim_target_id="sem-concept-customer-status",
        sources_read=[
            ClaimSourceRecord(
                source_ref="docs/business-background/客户主数据回填与状态来源分析.md",
                source_type="legacy_doc",
                note="Auxiliary-view fixture source.",
                workspace_id="legacy_work_data_hub",
                relative_path="docs/business-background/客户主数据回填与状态来源分析.md",
                semantic_authority="authoritative_semantic_source",
            )
        ],
        objects_discovered=[],
        edges_added=[],
        candidates_raised=[],
        semantic_findings=[
            ClaimSemanticFindingRecord(
                semantic_id="sem-concept-customer-status",
                semantic_node_type="semantic_concept",
                title="Customer status",
                summary="Customer status is a distinct semantic layer.",
                business_conclusion="Customer status is a distinct semantic layer.",
                primary_source_refs=["docs/business-background/客户主数据回填与状态来源分析.md"],
                supporting_source_refs=["docs/wiki-bi/concepts/customer-status.md"],
                semantic_authority="authoritative_semantic_source",
                durable_target_pages=["docs/wiki-bi/concepts/customer-status.md"],
                confidence="high",
                last_verified="2026-04-18",
                open_questions=[],
                proposal_governance={
                    "recommendation_status": "recommended_stable_canonical",
                    "semantic_scope_type": "semantic_object",
                    "authority_gate_passed": True,
                    "downstream_consequence_gate_passed": True,
                    "contradiction_accounting_status": "explained_scope_limited_alias",
                    "contradiction_accounting_notes": [],
                    "proxy_usage_refs": [],
                    "downstream_consequence_refs": [
                        "docs/wiki-bi/concepts/customer-status.md"
                    ],
                    "related_runtime_carriers": ["obj-customer-mdm-lifecycle"],
                    "high_priority_governance_questions": [],
                    "gate_blockers": [],
                    "governance_implications": {
                        "slice_admission": {
                            "summary": "Supports current slice admission review.",
                            "affected_surfaces": ["docs/wiki-bi/concepts/customer-status.md"],
                            "blocked_by": [],
                        },
                        "defer_candidates": {
                            "summary": "",
                            "affected_surfaces": [],
                            "blocked_by": [],
                        },
                        "retire_candidates": {
                            "summary": "",
                            "affected_surfaces": [],
                            "blocked_by": [],
                        },
                        "durable_wiki_absorption": {
                            "summary": "Ready for durable review.",
                            "target_pages": ["docs/wiki-bi/concepts/customer-status.md"],
                            "blocked_by": [],
                        },
                    },
                },
            )
        ],
        open_questions=[],
        compiled_into=["docs/wiki-bi/concepts/customer-status.md"],
        submitted_at="2026-04-18T00:00:00Z",
    )
    blocked_claim = ClaimArtifact(
        claim_id="claim-wave-2026-04-17-semantic-governance-reframe-customer-type-conflict",
        wave_id=SUCCESSOR_WAVE_ID,
        claim_scope="semantic",
        claim_target_id="sem-non-equivalence-customer-type-vs-is-new",
        sources_read=[
            ClaimSourceRecord(
                source_ref="docs/business-background/客户主数据回填与状态来源分析.md",
                source_type="legacy_doc",
                note="Auxiliary-view fixture source.",
                workspace_id="legacy_work_data_hub",
                relative_path="docs/business-background/客户主数据回填与状态来源分析.md",
                semantic_authority="authoritative_semantic_source",
            )
        ],
        objects_discovered=[],
        edges_added=[],
        candidates_raised=[],
        semantic_findings=[
            ClaimSemanticFindingRecord(
                semantic_id="sem-non-equivalence-customer-type-vs-is-new",
                semantic_node_type="semantic_non_equivalence",
                title="Customer type label vs is_new",
                summary="Customer type labels are not the same as is_new.",
                business_conclusion="Customer type labels are not the same as is_new.",
                primary_source_refs=["docs/business-background/客户主数据回填与状态来源分析.md"],
                supporting_source_refs=[
                    "docs/wiki-bi/standards/semantic-correctness/customer-status-semantics.md"
                ],
                semantic_authority="authoritative_semantic_source",
                durable_target_pages=[
                    "docs/wiki-bi/standards/semantic-correctness/customer-status-semantics.md"
                ],
                confidence="high",
                last_verified="2026-04-18",
                open_questions=[],
                proposal_governance={
                    "recommendation_status": "recommended_contested",
                    "semantic_scope_type": "semantic_object",
                    "authority_gate_passed": True,
                    "downstream_consequence_gate_passed": True,
                    "contradiction_accounting_status": "unresolved",
                    "contradiction_accounting_notes": [
                        "Legacy runtime labels still conflict.",
                    ],
                    "proxy_usage_refs": [
                        "docs/wiki-bi/standards/semantic-correctness/customer-status-semantics.md"
                    ],
                    "downstream_consequence_refs": [
                        "docs/wiki-bi/concepts/customer-status.md"
                    ],
                    "related_runtime_carriers": ["obj-customer-mdm-lifecycle"],
                    "high_priority_governance_questions": [
                        "Would this change defer or retire decisions?"
                    ],
                    "gate_blockers": [
                        "contradiction_unresolved",
                        "high_priority_governance_questions_open",
                    ],
                    "governance_implications": {
                        "slice_admission": {
                            "summary": "Blocks current slice admission review.",
                            "affected_surfaces": [
                                "docs/wiki-bi/standards/semantic-correctness/customer-status-semantics.md"
                            ],
                            "blocked_by": ["contradiction_unresolved"],
                        },
                        "defer_candidates": {
                            "summary": "",
                            "affected_surfaces": [],
                            "blocked_by": [],
                        },
                        "retire_candidates": {
                            "summary": "",
                            "affected_surfaces": [],
                            "blocked_by": [],
                        },
                        "durable_wiki_absorption": {
                            "summary": "Not ready for durable review.",
                            "target_pages": [
                                "docs/wiki-bi/standards/semantic-correctness/customer-status-semantics.md"
                            ],
                            "blocked_by": [
                                "contradiction_unresolved",
                                "high_priority_governance_questions_open",
                            ],
                        },
                    },
                },
            )
        ],
        open_questions=[],
        compiled_into=[
            "docs/wiki-bi/standards/semantic-correctness/customer-status-semantics.md"
        ],
        submitted_at="2026-04-18T00:00:00Z",
    )

    stable_path = write_claim_artifact(registry_root, stable_claim)
    blocked_path = write_claim_artifact(registry_root, blocked_claim)
    compile_claim_artifacts(registry_root, [stable_path, blocked_path])
    result = generate_reports(registry_root)

    discovery_payload = json.loads(
        Path(result.semantic_discovery_report).read_text(encoding="utf-8")
    )
    readiness_payload = json.loads(
        Path(result.semantic_readiness_report).read_text(encoding="utf-8")
    )

    assert discovery_payload["semantic_maturity_counts"]["consumption-candidate"] == 1
    assert discovery_payload["semantic_maturity_counts"]["contested"] == 1
    assert discovery_payload["contested_semantic_ids"] == [
        "sem-non-equivalence-customer-type-vs-is-new",
    ]
    assert readiness_payload["handoff_ready_semantic_ids"] == [
        "sem-concept-customer-status",
    ]
    assert readiness_payload["blocked_semantic_ids"] == [
        "sem-non-equivalence-customer-type-vs-is-new",
    ]
    assert readiness_payload["durable_target_page_count"] == 2

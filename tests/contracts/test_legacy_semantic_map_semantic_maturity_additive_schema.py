from __future__ import annotations

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


def _compile_semantic_fixture(tmp_path: Path) -> dict[str, object]:
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
                note="Semantic maturity fixture source.",
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
                    "contradiction_accounting_notes": [
                        "Legacy runtime labels are a scope-limited alias.",
                    ],
                    "proxy_usage_refs": [
                        "docs/wiki-bi/evidence/customer-mdm-lifecycle-evidence.md",
                    ],
                    "downstream_consequence_refs": [
                        "docs/wiki-bi/concepts/customer-status.md",
                    ],
                    "related_runtime_carriers": ["obj-customer-mdm-lifecycle"],
                    "high_priority_governance_questions": [],
                    "gate_blockers": ["authority_gate_failed"],
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
                            "summary": "Ready for durable absorption review.",
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
    claim_path = write_claim_artifact(registry_root, claim)
    compile_claim_artifacts(registry_root, [claim_path])
    return yaml.safe_load(
        (
            registry_root
            / "semantic"
            / "concepts"
            / "sem-concept-customer-status.yaml"
        ).read_text(encoding="utf-8")
    )


def test_compiled_semantic_nodes_keep_existing_fields_and_add_maturity_fields(
    tmp_path: Path,
) -> None:
    payload = _compile_semantic_fixture(tmp_path)

    assert "primary_semantic_sources" in payload
    assert "semantic_authority" in payload
    assert "durable_target_pages" in payload
    assert payload["proposal_governance"]["recommendation_status"] == (
        "recommended_stable_canonical"
    )
    assert payload["proposal_governance"]["semantic_scope_type"] == "semantic_object"
    assert payload["proposal_governance"]["authority_gate_passed"] is True
    assert payload["semantic_maturity_level"] in {
        "observed",
        "inferred",
        "contested",
        "consumption-candidate",
    }
    assert payload["semantic_maturity_level"] == "consumption-candidate"
    assert payload["consumption_readiness_status"] == "reviewable"
    assert payload["blocked_by"] == []
    assert payload["compiled_from_wave_id"] == SUCCESSOR_WAVE_ID


def test_compiled_semantic_node_blocks_consumption_when_authority_gate_fails(
    tmp_path: Path,
) -> None:
    registry_root = tmp_path / "legacy-semantic-map"
    bootstrap_semantic_map(registry_root)
    _seed_successor_wave(registry_root)

    claim = ClaimArtifact(
        claim_id="claim-wave-2026-04-17-semantic-governance-reframe-customer-status-contested",
        wave_id=SUCCESSOR_WAVE_ID,
        claim_scope="semantic",
        claim_target_id="sem-concept-customer-status",
        sources_read=[
            ClaimSourceRecord(
                source_ref="docs/business-background/客户主数据回填与状态来源分析.md",
                source_type="legacy_doc",
                note="Semantic maturity fixture source.",
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
                    "authority_gate_passed": False,
                    "downstream_consequence_gate_passed": True,
                    "contradiction_accounting_status": "explained_scope_limited_alias",
                    "contradiction_accounting_notes": [],
                    "proxy_usage_refs": [],
                    "downstream_consequence_refs": [
                        "docs/wiki-bi/concepts/customer-status.md"
                    ],
                    "related_runtime_carriers": ["obj-customer-mdm-lifecycle"],
                    "high_priority_governance_questions": [],
                    "gate_blockers": ["authority_gate_failed"],
                    "governance_implications": {
                        "slice_admission": {
                            "summary": "Cannot admit until authority is resolved.",
                            "affected_surfaces": ["docs/wiki-bi/concepts/customer-status.md"],
                            "blocked_by": ["authority_gate_failed"],
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
                            "summary": "",
                            "target_pages": ["docs/wiki-bi/concepts/customer-status.md"],
                            "blocked_by": ["authority_gate_failed"],
                        },
                    },
                },
            )
        ],
        open_questions=[],
        compiled_into=["docs/wiki-bi/concepts/customer-status.md"],
        submitted_at="2026-04-18T00:00:00Z",
    )
    claim_path = write_claim_artifact(registry_root, claim)
    compile_claim_artifacts(registry_root, [claim_path])

    payload = yaml.safe_load(
        (
            registry_root
            / "semantic"
            / "concepts"
            / "sem-concept-customer-status.yaml"
        ).read_text(encoding="utf-8")
    )

    assert payload["proposal_governance"]["recommendation_status"] == "recommended_contested"
    assert payload["semantic_maturity_level"] == "contested"
    assert payload["consumption_readiness_status"] == "blocked"
    assert "authority_gate_failed" in payload["blocked_by"]

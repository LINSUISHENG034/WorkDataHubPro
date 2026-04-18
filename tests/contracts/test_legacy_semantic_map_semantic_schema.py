from __future__ import annotations

from pathlib import Path

import pytest

from scripts.legacy_semantic_map.claims import (
    CLAIM_SCOPE_DIRECTORIES,
    ClaimArtifact,
    ClaimSemanticFindingRecord,
    ClaimSourceRecord,
    claim_relative_path,
)
from scripts.legacy_semantic_map.models import (
    PROPOSAL_RECOMMENDATION_STATUSES,
    PROPOSAL_SEMANTIC_SCOPE_TYPES,
    PROPOSAL_CONTRADICTION_ACCOUNTING_STATUSES,
    SEMANTIC_AUTHORITIES,
    SEMANTIC_NODE_TYPES,
)


def _build_semantic_claim() -> ClaimArtifact:
    return ClaimArtifact(
        claim_id="claim-wave-2026-04-17-customer-status-semantic-pilot-customer-status-concept",
        wave_id="wave-2026-04-17-customer-status-semantic-pilot",
        claim_scope="semantic",
        claim_target_id="sem-concept-customer-status",
        sources_read=[
            ClaimSourceRecord(
                source_ref="docs/business-background/客户主数据回填与状态来源分析.md",
                source_type="legacy_doc",
                note="Business background page defines the current customer-status semantic boundary.",
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
                summary="Customer status is a separate semantic layer from customer master backfill.",
                business_conclusion="Customer master backfill and customer status evaluation are distinct semantic concerns.",
                primary_source_refs=[
                    "docs/business-background/客户主数据回填与状态来源分析.md",
                ],
                supporting_source_refs=[
                    "docs/wiki-bi/evidence/customer-mdm-lifecycle-evidence.md",
                ],
                semantic_authority="authoritative_semantic_source",
                durable_target_pages=[
                    "docs/wiki-bi/concepts/customer-status.md",
                ],
                confidence="high",
                last_verified="2026-04-17",
                open_questions=[],
                non_equivalent_to=["sem-concept-customer-master-backfill"],
                proposal_governance={
                    "recommendation_status": "recommended_stable_canonical",
                    "semantic_scope_type": "semantic_object",
                    "authority_gate_passed": True,
                    "downstream_consequence_gate_passed": True,
                    "contradiction_accounting_status": "explained_scope_limited_alias",
                    "contradiction_accounting_notes": [
                        "Legacy operator usage mixes status and backfill labels.",
                    ],
                    "proxy_usage_refs": [
                        "docs/wiki-bi/evidence/customer-mdm-lifecycle-evidence.md",
                    ],
                    "downstream_consequence_refs": [
                        "docs/wiki-bi/concepts/customer-status.md",
                    ],
                    "related_runtime_carriers": [
                        "obj-customer-mdm-lifecycle",
                    ],
                    "high_priority_governance_questions": [],
                    "gate_blockers": [],
                    "governance_implications": {
                        "slice_admission": {
                            "summary": "Supports current customer-status slice admission.",
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
                            "summary": "Ready for durable wiki proposal review.",
                            "target_pages": ["docs/wiki-bi/concepts/customer-status.md"],
                            "blocked_by": [],
                        },
                    },
                },
            )
        ],
        open_questions=[],
        compiled_into=[],
        submitted_at="2026-04-17T12:00:00Z",
    )


def test_semantic_claim_contract_and_relative_path_shape() -> None:
    claim = _build_semantic_claim()

    assert SEMANTIC_NODE_TYPES == (
        "semantic_concept",
        "semantic_rule",
        "semantic_non_equivalence",
        "semantic_lifecycle",
        "semantic_fact_family",
        "semantic_decision_anchor",
    )
    assert SEMANTIC_AUTHORITIES == (
        "authoritative_semantic_source",
        "runtime_witness",
        "implementation_hint",
        "historical_context",
    )
    assert PROPOSAL_RECOMMENDATION_STATUSES == (
        "recommended_stable_canonical",
        "recommended_contested",
        "claim_level_only",
    )
    assert PROPOSAL_SEMANTIC_SCOPE_TYPES == (
        "semantic_object",
        "runtime_carrier",
        "witness_surface",
    )
    assert PROPOSAL_CONTRADICTION_ACCOUNTING_STATUSES == (
        "explained_operational_shortcut",
        "explained_historical_drift",
        "explained_scope_limited_alias",
        "real_contradiction",
        "unresolved",
    )
    assert CLAIM_SCOPE_DIRECTORIES == {
        "execution": "execution",
        "subsystems": "subsystems",
        "objects": "objects",
        "semantic": "semantic",
    }

    assert claim_relative_path(claim) == Path(
        "claims"
    ) / "wave-2026-04-17-customer-status-semantic-pilot" / "semantic" / (
        "claim-wave-2026-04-17-customer-status-semantic-pilot-customer-status-concept.yaml"
    )

    payload = claim.to_payload()
    assert payload["sources_read"][0]["workspace_id"] == "legacy_work_data_hub"
    assert payload["sources_read"][0]["relative_path"] == (
        "docs/business-background/客户主数据回填与状态来源分析.md"
    )
    assert payload["sources_read"][0]["semantic_authority"] == "authoritative_semantic_source"
    assert payload["semantic_findings"][0]["semantic_node_type"] == "semantic_concept"
    assert payload["semantic_findings"][0]["durable_target_pages"] == [
        "docs/wiki-bi/concepts/customer-status.md",
    ]
    assert payload["semantic_findings"][0]["proposal_governance"] == {
        "recommendation_status": "recommended_stable_canonical",
        "semantic_scope_type": "semantic_object",
        "authority_gate_passed": True,
        "downstream_consequence_gate_passed": True,
        "contradiction_accounting_status": "explained_scope_limited_alias",
        "contradiction_accounting_notes": [
            "Legacy operator usage mixes status and backfill labels.",
        ],
        "proxy_usage_refs": [
            "docs/wiki-bi/evidence/customer-mdm-lifecycle-evidence.md",
        ],
        "downstream_consequence_refs": [
            "docs/wiki-bi/concepts/customer-status.md",
        ],
        "related_runtime_carriers": ["obj-customer-mdm-lifecycle"],
        "high_priority_governance_questions": [],
        "gate_blockers": [],
        "governance_implications": {
            "slice_admission": {
                "summary": "Supports current customer-status slice admission.",
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
                "summary": "Ready for durable wiki proposal review.",
                "target_pages": ["docs/wiki-bi/concepts/customer-status.md"],
                "blocked_by": [],
            },
        },
    }


def test_semantic_schema_rejects_invalid_constrained_vocabularies() -> None:
    with pytest.raises(ValueError, match="Unsupported semantic_authority"):
        ClaimSourceRecord(
            source_ref="docs/business-background/客户主数据回填与状态来源分析.md",
            source_type="legacy_doc",
            note="invalid semantic authority",
            workspace_id="legacy_work_data_hub",
            relative_path="docs/business-background/客户主数据回填与状态来源分析.md",
            semantic_authority="wrong_authority",
        )

    with pytest.raises(ValueError, match="Unsupported semantic_node_type"):
        ClaimSemanticFindingRecord(
            semantic_id="sem-concept-customer-status",
            semantic_node_type="semantic_bad_type",
            title="Customer status",
            summary="Bad semantic node type.",
            business_conclusion="Bad semantic node type should fail validation.",
            primary_source_refs=[
                "docs/business-background/客户主数据回填与状态来源分析.md",
            ],
            supporting_source_refs=[],
            semantic_authority="authoritative_semantic_source",
            durable_target_pages=[],
            confidence="high",
            last_verified="2026-04-17",
            open_questions=[],
            non_equivalent_to=[],
        )

    with pytest.raises(ValueError, match="Unsupported recommendation_status"):
        ClaimSemanticFindingRecord(
            semantic_id="sem-concept-customer-status",
            semantic_node_type="semantic_concept",
            title="Customer status",
            summary="Bad proposal status.",
            business_conclusion="Bad proposal status should fail validation.",
            primary_source_refs=[
                "docs/business-background/客户主数据回填与状态来源分析.md",
            ],
            supporting_source_refs=[],
            semantic_authority="authoritative_semantic_source",
            durable_target_pages=[],
            confidence="high",
            last_verified="2026-04-17",
            open_questions=[],
            non_equivalent_to=[],
            proposal_governance={
                "recommendation_status": "finalized_truth",
                "semantic_scope_type": "semantic_object",
                "authority_gate_passed": False,
                "downstream_consequence_gate_passed": False,
                "contradiction_accounting_status": "unresolved",
                "contradiction_accounting_notes": [],
                "proxy_usage_refs": [],
                "downstream_consequence_refs": [],
                "related_runtime_carriers": [],
                "high_priority_governance_questions": [],
                "gate_blockers": [],
                "governance_implications": {
                    "slice_admission": {
                        "summary": "",
                        "affected_surfaces": [],
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
                        "summary": "",
                        "target_pages": [],
                        "blocked_by": [],
                    },
                },
            },
        )

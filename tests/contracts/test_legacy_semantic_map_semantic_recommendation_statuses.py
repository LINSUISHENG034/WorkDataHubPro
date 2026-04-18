from __future__ import annotations

import json
from pathlib import Path

import yaml

from scripts.legacy_semantic_map.bootstrap import bootstrap_semantic_map
from scripts.legacy_semantic_map.reporting import generate_reports


SUCCESSOR_WAVE_ID = "wave-2026-04-17-semantic-governance-reframe"


def _write_yaml(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        yaml.safe_dump(payload, sort_keys=False, allow_unicode=False),
        encoding="utf-8",
    )


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
            "closed_at": None,
            "seeded_entry_surfaces": [],
            "seeded_high_priority_source_families": [],
            "admitted_subsystems": [],
            "durable_wiki_targets_accepted": False,
            "findings_disposition_complete": False,
            "depends_on_active_wave_working_state": False,
        }
    ]
    _write_yaml(registry_root / "waves" / "index.yaml", payload)


def test_generate_reports_adds_recommendation_counts_and_gate_blockers(
    tmp_path: Path,
) -> None:
    registry_root = tmp_path / "legacy-semantic-map"
    bootstrap_semantic_map(registry_root)
    _seed_successor_wave(registry_root)

    _write_yaml(
        registry_root / "semantic" / "rules" / "sem-rule-is-new-definition.yaml",
        {
            "semantic_id": "sem-rule-is-new-definition",
            "semantic_node_type": "semantic_rule",
            "title": "is_new definition",
            "business_conclusion": "is_new is defined from winning and existing status.",
            "primary_semantic_sources": ["config/customer_status_rules.yml"],
            "supporting_witness_sources": ["docs/wiki-bi/concepts/customer-status.md"],
            "semantic_authority": "authoritative_semantic_source",
            "durable_target_pages": ["docs/wiki-bi/concepts/customer-status.md"],
            "blocked_by": [],
            "semantic_maturity_level": "consumption-candidate",
            "consumption_readiness_status": "reviewable",
            "proposal_governance": {
                "recommendation_status": "recommended_stable_canonical",
                "semantic_scope_type": "semantic_object",
                "authority_gate_passed": True,
                "downstream_consequence_gate_passed": True,
                "contradiction_accounting_status": "explained_scope_limited_alias",
                "contradiction_accounting_notes": [],
                "proxy_usage_refs": ["docs/wiki-bi/concepts/customer-status.md"],
                "downstream_consequence_refs": ["docs/wiki-bi/concepts/customer-status.md"],
                "related_runtime_carriers": ["obj-customer-mdm-lifecycle"],
                "high_priority_governance_questions": [],
                "gate_blockers": [],
                "governance_implications": {
                    "slice_admission": {
                        "summary": "Supports customer-status slice admission review.",
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
        },
    )
    _write_yaml(
        registry_root
        / "semantic"
        / "non-equivalences"
        / "sem-non-equivalence-customer-type-vs-is-new.yaml",
        {
            "semantic_id": "sem-non-equivalence-customer-type-vs-is-new",
            "semantic_node_type": "semantic_non_equivalence",
            "title": "Customer type label vs is_new",
            "business_conclusion": "Customer type labels are not the same as is_new.",
            "primary_semantic_sources": [
                "docs/business-background/客户主数据回填与状态来源分析.md",
            ],
            "supporting_witness_sources": [
                "docs/wiki-bi/standards/semantic-correctness/customer-status-semantics.md",
            ],
            "semantic_authority": "authoritative_semantic_source",
            "durable_target_pages": [
                "docs/wiki-bi/standards/semantic-correctness/customer-status-semantics.md"
            ],
            "blocked_by": ["contradiction_unresolved", "high_priority_governance_questions_open"],
            "semantic_maturity_level": "contested",
            "consumption_readiness_status": "blocked",
            "proposal_governance": {
                "recommendation_status": "recommended_contested",
                "semantic_scope_type": "semantic_object",
                "authority_gate_passed": True,
                "downstream_consequence_gate_passed": True,
                "contradiction_accounting_status": "unresolved",
                "contradiction_accounting_notes": [
                    "Legacy runtime usage still conflicts with the business semantic boundary.",
                ],
                "proxy_usage_refs": [
                    "docs/wiki-bi/standards/semantic-correctness/customer-status-semantics.md",
                ],
                "downstream_consequence_refs": [
                    "docs/wiki-bi/concepts/customer-status.md",
                ],
                "related_runtime_carriers": ["obj-customer-mdm-lifecycle"],
                "high_priority_governance_questions": [
                    "Would this conflict change defer or retire decisions?"
                ],
                "gate_blockers": [
                    "contradiction_unresolved",
                    "high_priority_governance_questions_open",
                ],
                "governance_implications": {
                    "slice_admission": {
                        "summary": "Blocks immediate slice admission closure.",
                        "affected_surfaces": [
                            "docs/wiki-bi/standards/semantic-correctness/customer-status-semantics.md"
                        ],
                        "blocked_by": [
                            "contradiction_unresolved",
                        ],
                    },
                    "defer_candidates": {
                        "summary": "Candidate for defer review until contradiction is resolved.",
                        "affected_surfaces": [
                            "docs/wiki-bi/standards/semantic-correctness/customer-status-semantics.md"
                        ],
                        "blocked_by": [
                            "contradiction_unresolved",
                        ],
                    },
                    "retire_candidates": {
                        "summary": "",
                        "affected_surfaces": [],
                        "blocked_by": [],
                    },
                    "durable_wiki_absorption": {
                        "summary": "Not ready for durable absorption.",
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
        },
    )
    _write_yaml(
        registry_root / "semantic" / "index.yaml",
        {
            "semantic_nodes": [
                {
                    "semantic_id": "sem-rule-is-new-definition",
                    "semantic_node_type": "semantic_rule",
                    "path": "semantic/rules/sem-rule-is-new-definition.yaml",
                },
                {
                    "semantic_id": "sem-non-equivalence-customer-type-vs-is-new",
                    "semantic_node_type": "semantic_non_equivalence",
                    "path": "semantic/non-equivalences/sem-non-equivalence-customer-type-vs-is-new.yaml",
                },
            ]
        },
    )

    result = generate_reports(registry_root)

    discovery_payload = json.loads(
        result.semantic_discovery_report.read_text(encoding="utf-8")
    )
    readiness_payload = json.loads(
        result.semantic_readiness_report.read_text(encoding="utf-8")
    )

    assert discovery_payload["recommendation_counts"] == {
        "recommended_stable_canonical": 1,
        "recommended_contested": 1,
        "claim_level_only": 0,
    }
    assert discovery_payload["contested_proposal_ids"] == [
        "sem-non-equivalence-customer-type-vs-is-new",
    ]
    assert readiness_payload["blocked_by_gate_reasons"] == {
        "contradiction_unresolved": 1,
        "high_priority_governance_questions_open": 1,
    }


def test_generate_reports_adds_governance_summaries_and_carrier_flags(
    tmp_path: Path,
) -> None:
    registry_root = tmp_path / "legacy-semantic-map"
    bootstrap_semantic_map(registry_root)
    _seed_successor_wave(registry_root)

    _write_yaml(
        registry_root
        / "semantic"
        / "decision-anchors"
        / "sem-decision-anchor-customer-status-rules.yaml",
        {
            "semantic_id": "sem-decision-anchor-customer-status-rules",
            "semantic_node_type": "semantic_decision_anchor",
            "title": "Customer-status rules decision anchor",
            "business_conclusion": "customer_status_rules.yml is a witness surface, not final semantic truth.",
            "primary_semantic_sources": ["config/customer_status_rules.yml"],
            "supporting_witness_sources": ["docs/wiki-bi/evidence/customer-mdm-lifecycle-evidence.md"],
            "semantic_authority": "authoritative_semantic_source",
            "durable_target_pages": ["docs/wiki-bi/evidence/customer-mdm-lifecycle-evidence.md"],
            "blocked_by": [],
            "semantic_maturity_level": "inferred",
            "consumption_readiness_status": "discovery-only",
            "proposal_governance": {
                "recommendation_status": "claim_level_only",
                "semantic_scope_type": "witness_surface",
                "authority_gate_passed": True,
                "downstream_consequence_gate_passed": True,
                "contradiction_accounting_status": "explained_operational_shortcut",
                "contradiction_accounting_notes": [],
                "proxy_usage_refs": ["docs/wiki-bi/evidence/customer-mdm-lifecycle-evidence.md"],
                "downstream_consequence_refs": [
                    "docs/wiki-bi/evidence/customer-mdm-lifecycle-evidence.md"
                ],
                "related_runtime_carriers": ["obj-customer-mdm-lifecycle"],
                "high_priority_governance_questions": [],
                "gate_blockers": [],
                "governance_implications": {
                    "slice_admission": {
                        "summary": "Useful as supporting evidence for slice admission review.",
                        "affected_surfaces": ["docs/wiki-bi/evidence/customer-mdm-lifecycle-evidence.md"],
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
                        "summary": "Witness surface only for durable review.",
                        "target_pages": ["docs/wiki-bi/evidence/customer-mdm-lifecycle-evidence.md"],
                        "blocked_by": [],
                    },
                },
            },
        },
    )
    _write_yaml(
        registry_root
        / "semantic"
        / "non-equivalences"
        / "sem-non-equivalence-customer-type-vs-is-new.yaml",
        {
            "semantic_id": "sem-non-equivalence-customer-type-vs-is-new",
            "semantic_node_type": "semantic_non_equivalence",
            "title": "Customer type label vs is_new",
            "business_conclusion": "Customer type labels are not the same as is_new.",
            "primary_semantic_sources": [
                "docs/business-background/客户主数据回填与状态来源分析.md",
            ],
            "supporting_witness_sources": [
                "docs/wiki-bi/standards/semantic-correctness/customer-status-semantics.md",
            ],
            "semantic_authority": "authoritative_semantic_source",
            "durable_target_pages": [
                "docs/wiki-bi/standards/semantic-correctness/customer-status-semantics.md"
            ],
            "blocked_by": ["contradiction_unresolved", "high_priority_governance_questions_open"],
            "semantic_maturity_level": "contested",
            "consumption_readiness_status": "blocked",
            "proposal_governance": {
                "recommendation_status": "recommended_contested",
                "semantic_scope_type": "semantic_object",
                "authority_gate_passed": True,
                "downstream_consequence_gate_passed": True,
                "contradiction_accounting_status": "unresolved",
                "contradiction_accounting_notes": [
                    "Legacy runtime usage still conflicts with the business semantic boundary.",
                ],
                "proxy_usage_refs": [
                    "docs/wiki-bi/standards/semantic-correctness/customer-status-semantics.md",
                ],
                "downstream_consequence_refs": [
                    "docs/wiki-bi/concepts/customer-status.md",
                ],
                "related_runtime_carriers": ["obj-customer-mdm-lifecycle"],
                "high_priority_governance_questions": [
                    "Would this conflict change defer or retire decisions?"
                ],
                "gate_blockers": [
                    "contradiction_unresolved",
                    "high_priority_governance_questions_open",
                ],
                "governance_implications": {
                    "slice_admission": {
                        "summary": "Blocks immediate slice admission closure.",
                        "affected_surfaces": [
                            "docs/wiki-bi/standards/semantic-correctness/customer-status-semantics.md"
                        ],
                        "blocked_by": [
                            "contradiction_unresolved",
                        ],
                    },
                    "defer_candidates": {
                        "summary": "Candidate for defer review until contradiction is resolved.",
                        "affected_surfaces": [
                            "docs/wiki-bi/standards/semantic-correctness/customer-status-semantics.md"
                        ],
                        "blocked_by": [
                            "contradiction_unresolved",
                        ],
                    },
                    "retire_candidates": {
                        "summary": "Candidate for retiring proxy-heavy customer-type usage.",
                        "affected_surfaces": [
                            "docs/wiki-bi/standards/semantic-correctness/customer-status-semantics.md"
                        ],
                        "blocked_by": [
                            "high_priority_governance_questions_open",
                        ],
                    },
                    "durable_wiki_absorption": {
                        "summary": "Not ready for durable absorption.",
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
        },
    )
    _write_yaml(
        registry_root / "semantic" / "index.yaml",
        {
            "semantic_nodes": [
                {
                    "semantic_id": "sem-decision-anchor-customer-status-rules",
                    "semantic_node_type": "semantic_decision_anchor",
                    "path": "semantic/decision-anchors/sem-decision-anchor-customer-status-rules.yaml",
                },
                {
                    "semantic_id": "sem-non-equivalence-customer-type-vs-is-new",
                    "semantic_node_type": "semantic_non_equivalence",
                    "path": "semantic/non-equivalences/sem-non-equivalence-customer-type-vs-is-new.yaml",
                },
            ]
        },
    )

    result = generate_reports(registry_root)
    discovery_payload = json.loads(
        result.semantic_discovery_report.read_text(encoding="utf-8")
    )

    assert discovery_payload["governance_implication_summaries"] == {
        "slice_admission": {
            "count": 2,
            "ids": [
                "sem-decision-anchor-customer-status-rules",
                "sem-non-equivalence-customer-type-vs-is-new",
            ],
        },
        "defer_candidates": {
            "count": 1,
            "ids": [
                "sem-non-equivalence-customer-type-vs-is-new",
            ],
        },
        "retire_candidates": {
            "count": 1,
            "ids": [
                "sem-non-equivalence-customer-type-vs-is-new",
            ],
        },
        "durable_wiki_absorption": {
            "count": 2,
            "ids": [
                "sem-decision-anchor-customer-status-rules",
                "sem-non-equivalence-customer-type-vs-is-new",
            ],
        },
    }
    assert discovery_payload["carrier_scope_mismatch_ids"] == [
        "sem-decision-anchor-customer-status-rules",
    ]
    assert discovery_payload["unresolved_proxy_conflict_ids"] == [
        "sem-non-equivalence-customer-type-vs-is-new",
    ]

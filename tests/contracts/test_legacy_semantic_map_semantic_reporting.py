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


def test_generate_reports_includes_semantic_alignment_metrics_for_question_set(
    tmp_path: Path,
) -> None:
    registry_root = tmp_path / "legacy-semantic-map"
    bootstrap_semantic_map(registry_root)

    waves_index = yaml.safe_load((registry_root / "waves" / "index.yaml").read_text(encoding="utf-8"))
    waves_index["active_wave_id"] = "wave-2026-04-17-customer-status-semantic-pilot"
    waves_index["waves"].append(
        {
            "wave_id": "wave-2026-04-17-customer-status-semantic-pilot",
            "title": "Customer status semantic pilot",
            "status": "active",
            "wave_ordinal": 2,
            "opened_at": "2026-04-17",
            "closed_at": None,
            "seeded_entry_surfaces": [],
            "seeded_high_priority_source_families": [],
            "admitted_subsystems": [],
            "durable_wiki_targets_accepted": False,
            "findings_disposition_complete": False,
            "depends_on_active_wave_working_state": False,
            "semantic_question_set_id": "customer-status-semantic-pilot",
        }
    )
    _write_yaml(registry_root / "waves" / "index.yaml", waves_index)

    _write_yaml(
        registry_root / "semantic" / "question-sets" / "customer-status-semantic-pilot.yaml",
        {
            "question_set_id": "customer-status-semantic-pilot",
            "required_question_ids": [
                "q-customer-status-concept",
                "q-customer-master-vs-status-non-equivalence",
            ],
            "required_semantic_node_ids": [
                "sem-concept-customer-status",
                "sem-non-equivalence-customer-master-vs-status",
            ],
            "required_non_equivalence_ids": [
                "sem-non-equivalence-customer-master-vs-status",
            ],
        },
    )
    _write_yaml(
        registry_root / "semantic" / "concepts" / "sem-concept-customer-status.yaml",
        {
            "semantic_id": "sem-concept-customer-status",
            "semantic_node_type": "semantic_concept",
            "business_conclusion": "Customer status is a distinct semantic layer.",
            "primary_semantic_sources": [
                "docs/business-background/客户主数据回填与状态来源分析.md",
            ],
            "supporting_witness_sources": [],
            "semantic_authority": "authoritative_semantic_source",
            "durable_target_pages": ["docs/wiki-bi/concepts/customer-status.md"],
            "blocked_by": [],
        },
    )
    _write_yaml(
        registry_root / "semantic" / "non-equivalences" / "sem-non-equivalence-customer-master-vs-status.yaml",
        {
            "semantic_id": "sem-non-equivalence-customer-master-vs-status",
            "semantic_node_type": "semantic_non_equivalence",
            "business_conclusion": "Customer master backfill is not the same as customer status evaluation.",
            "primary_semantic_sources": [
                "docs/business-background/客户主数据回填与状态来源分析.md",
            ],
            "supporting_witness_sources": [],
            "semantic_authority": "authoritative_semantic_source",
            "durable_target_pages": [
                "docs/wiki-bi/standards/semantic-correctness/customer-status-semantics.md"
            ],
            "blocked_by": [],
        },
    )
    _write_yaml(
        registry_root / "semantic" / "index.yaml",
        {
            "semantic_nodes": [
                {
                    "semantic_id": "sem-concept-customer-status",
                    "semantic_node_type": "semantic_concept",
                    "path": "semantic/concepts/sem-concept-customer-status.yaml",
                },
                {
                    "semantic_id": "sem-non-equivalence-customer-master-vs-status",
                    "semantic_node_type": "semantic_non_equivalence",
                    "path": "semantic/non-equivalences/sem-non-equivalence-customer-master-vs-status.yaml",
                },
            ]
        },
    )

    result = generate_reports(registry_root)

    coverage_payload = json.loads(result.current_coverage_report.read_text(encoding="utf-8"))
    assert coverage_payload["semantic_question_coverage_pct"] == 100.0
    assert coverage_payload["semantic_non_equivalence_coverage_pct"] == 100.0
    assert coverage_payload["stub_primary_source_count"] == 0
    assert coverage_payload["authoritative_primary_source_pct"] == 100.0
    assert coverage_payload["absorption_contract_completion_pct"] == 100.0


def test_generate_reports_turns_red_for_missing_semantic_question_and_stub_source(
    tmp_path: Path,
) -> None:
    registry_root = tmp_path / "legacy-semantic-map"
    bootstrap_semantic_map(registry_root)

    waves_index = yaml.safe_load((registry_root / "waves" / "index.yaml").read_text(encoding="utf-8"))
    waves_index["active_wave_id"] = "wave-2026-04-17-customer-status-semantic-pilot"
    waves_index["waves"].append(
        {
            "wave_id": "wave-2026-04-17-customer-status-semantic-pilot",
            "title": "Customer status semantic pilot",
            "status": "active",
            "wave_ordinal": 2,
            "opened_at": "2026-04-17",
            "closed_at": None,
            "seeded_entry_surfaces": [],
            "seeded_high_priority_source_families": [],
            "admitted_subsystems": [],
            "durable_wiki_targets_accepted": False,
            "findings_disposition_complete": False,
            "depends_on_active_wave_working_state": False,
            "semantic_question_set_id": "customer-status-semantic-pilot",
        }
    )
    _write_yaml(registry_root / "waves" / "index.yaml", waves_index)

    _write_yaml(
        registry_root / "semantic" / "question-sets" / "customer-status-semantic-pilot.yaml",
        {
            "question_set_id": "customer-status-semantic-pilot",
            "required_question_ids": [
                "q-customer-status-concept",
                "q-customer-master-vs-status-non-equivalence",
            ],
            "required_semantic_node_ids": [
                "sem-concept-customer-status",
                "sem-non-equivalence-customer-master-vs-status",
            ],
            "required_non_equivalence_ids": [
                "sem-non-equivalence-customer-master-vs-status",
            ],
        },
    )
    _write_yaml(
        registry_root / "semantic" / "concepts" / "sem-concept-customer-status.yaml",
        {
            "semantic_id": "sem-concept-customer-status",
            "semantic_node_type": "semantic_concept",
            "business_conclusion": "Customer status is a distinct semantic layer.",
            "primary_semantic_sources": [
                "src/work_data_hub/services/customer_identity.py.txt",
            ],
            "supporting_witness_sources": [],
            "semantic_authority": "implementation_hint",
            "durable_target_pages": ["docs/wiki-bi/concepts/customer-status.md"],
            "blocked_by": [],
        },
    )
    _write_yaml(
        registry_root / "semantic" / "index.yaml",
        {
            "semantic_nodes": [
                {
                    "semantic_id": "sem-concept-customer-status",
                    "semantic_node_type": "semantic_concept",
                    "path": "semantic/concepts/sem-concept-customer-status.yaml",
                }
            ]
        },
    )

    result = generate_reports(registry_root)

    coverage_payload = json.loads(result.current_coverage_report.read_text(encoding="utf-8"))
    integrity_payload = json.loads(result.current_integrity_report.read_text(encoding="utf-8"))
    assert coverage_payload["semantic_question_coverage_pct"] == 50.0
    assert coverage_payload["stub_primary_source_count"] == 1
    assert integrity_payload["wave_status"] == "red"
    assert "semantic_question_coverage_incomplete" in integrity_payload["blocking_reasons"]
    assert "stub_primary_sources_detected" in integrity_payload["blocking_reasons"]

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


def _build_semantic_claim() -> ClaimArtifact:
    return ClaimArtifact(
        claim_id="claim-wave-2026-04-16-registry-bootstrap-customer-status-concept",
        wave_id="wave-2026-04-16-registry-bootstrap",
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
            )
        ],
        open_questions=[],
        compiled_into=[],
        submitted_at="2026-04-17T12:00:00Z",
    )


def test_compile_claim_artifacts_writes_semantic_canonical_files(tmp_path: Path) -> None:
    registry_root = tmp_path / "legacy-semantic-map"
    bootstrap_semantic_map(registry_root)

    semantic_claim_path = write_claim_artifact(registry_root, _build_semantic_claim())

    result = compile_claim_artifacts(registry_root, [semantic_claim_path])

    semantic_payload = yaml.safe_load(
        (registry_root / "semantic" / "concepts" / "sem-concept-customer-status.yaml").read_text(
            encoding="utf-8"
        )
    )
    assert semantic_payload["semantic_id"] == "sem-concept-customer-status"
    assert semantic_payload["semantic_node_type"] == "semantic_concept"
    assert semantic_payload["business_conclusion"] == (
        "Customer master backfill and customer status evaluation are distinct semantic concerns."
    )
    assert semantic_payload["primary_semantic_sources"] == [
        "docs/business-background/客户主数据回填与状态来源分析.md",
    ]
    assert semantic_payload["durable_target_pages"] == [
        "docs/wiki-bi/concepts/customer-status.md",
    ]
    assert semantic_payload["compiled_from_claims"] == [
        "claim-wave-2026-04-16-registry-bootstrap-customer-status-concept",
    ]

    semantic_index = yaml.safe_load(
        (registry_root / "semantic" / "index.yaml").read_text(encoding="utf-8")
    )
    assert semantic_index["semantic_nodes"] == [
        {
            "semantic_id": "sem-concept-customer-status",
            "semantic_node_type": "semantic_concept",
            "path": "semantic/concepts/sem-concept-customer-status.yaml",
        }
    ]

    manifest = json.loads((registry_root / "manifest.json").read_text(encoding="utf-8"))
    assert "semantic/index.yaml" in result.written_files
    assert "semantic/concepts/sem-concept-customer-status.yaml" in result.written_files
    assert "semantic/index.yaml" in manifest["generated_canonical_files"]
    assert "semantic/concepts/sem-concept-customer-status.yaml" in manifest[
        "generated_canonical_files"
    ]

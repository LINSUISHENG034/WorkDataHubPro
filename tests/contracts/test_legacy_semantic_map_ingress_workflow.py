from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest
import yaml

from scripts.legacy_semantic_map.bootstrap import bootstrap_semantic_map
from scripts.legacy_semantic_map.claims import ClaimSourceRecord
from scripts.legacy_semantic_map.ingress import (
    INGRESS_KIND_DIRECTORIES,
    LEGACY_WORKSPACE_ID,
    IngressRecord,
    ingress_relative_path,
    promote_ingress_record,
    write_ingress_record,
)
from scripts.legacy_semantic_map.semantic_ingress_guard import SemanticPromotionDraft


def _legacy_source(*, source_ref: str, source_type: str = "legacy_doc") -> ClaimSourceRecord:
    return ClaimSourceRecord(
        source_ref=source_ref,
        source_type=source_type,
        note=f"Legacy semantic evidence from {source_ref}.",
        workspace_id=LEGACY_WORKSPACE_ID,
        relative_path=source_ref,
    )


def _build_finding() -> IngressRecord:
    return IngressRecord(
        ingress_id="ingress-wave-2026-04-16-registry-bootstrap-manual-entry-runtime-boundary",
        wave_id="wave-2026-04-16-registry-bootstrap",
        ingress_kind="finding",
        title="Manual entry runtime boundary",
        granularity_rationale="This conclusion is stable enough to stand alone as a single finding.",
        questions=[
            "Does annuity performance manual entry remain a separate runtime boundary from scheduled orchestration?",
        ],
        candidate_conclusions=[
            "Manual CLI entry remains a distinct operator-facing runtime boundary.",
        ],
        primary_semantic_sources=[
            _legacy_source(
                source_ref="docs/domains/annuity_performance-capability-map.md",
            )
        ],
        supporting_witness_sources=[
            _legacy_source(
                source_ref="src/work_data_hub/cli/etl/domain_validation.py",
                source_type="legacy_code",
            )
        ],
        possible_non_equivalences=[
            "manual-entry-runtime-boundary != scheduled-orchestration-runtime-boundary",
        ],
        proxy_usage_refs=[
            "docs/wiki-bi/evidence/operator-and-surface-evidence.md",
        ],
        open_points=[],
        promotion_recommendation={
            "recommended_action": "hold_ingress",
            "rationale": "This finding should remain in ingress until a promotion task evaluates semantic node typing.",
            "gate_failures": [],
            "requires_user_review": False,
        },
        promoted_claim_ids=[],
        created_at="2026-04-19T00:00:00Z",
    )


def _build_question_cluster() -> IngressRecord:
    return IngressRecord(
        ingress_id="ingress-wave-2026-04-16-registry-bootstrap-manual-entry-question-cluster",
        wave_id="wave-2026-04-16-registry-bootstrap",
        ingress_kind="question_cluster",
        title="Manual entry boundary questions",
        granularity_rationale="These two questions share the same evidence and should be reviewed together.",
        questions=[
            "Where does the manual entry runtime boundary start?",
            "Which scheduled surfaces are neighboring but not equivalent?",
        ],
        candidate_conclusions=[
            "Manual entry and scheduled orchestration should remain separate semantic boundaries.",
        ],
        primary_semantic_sources=[
            _legacy_source(
                source_ref="docs/domains/annuity_performance-capability-map.md",
            )
        ],
        supporting_witness_sources=[
            _legacy_source(
                source_ref="src/work_data_hub/orchestration/jobs/annuity_performance.py",
                source_type="legacy_code",
            )
        ],
        possible_non_equivalences=[
            "manual-entry-runtime-boundary != annuity-performance-scheduled-job-boundary",
        ],
        proxy_usage_refs=[
            "docs/wiki-bi/evidence/operator-and-surface-evidence.md",
        ],
        open_points=[
            "Confirm whether any replay helper shares state across the boundary.",
        ],
        promotion_recommendation={
            "recommended_action": "requires_user_review",
            "rationale": "This cluster still needs semantic-boundary review before promotion.",
            "gate_failures": [
                "clustered_questions_not_collapsed",
            ],
            "requires_user_review": True,
        },
        promoted_claim_ids=[],
        created_at="2026-04-19T00:00:00Z",
    )


def _promotion_ready_finding() -> IngressRecord:
    return IngressRecord(
        ingress_id="ingress-wave-2026-04-16-registry-bootstrap-status-year-anchor",
        wave_id="wave-2026-04-16-registry-bootstrap",
        ingress_kind="finding",
        title="Status year anchor",
        granularity_rationale="One stable conclusion is ready for standalone review.",
        questions=["Is status_year an annual anchor for customer-status semantics?"],
        candidate_conclusions=[
            "status_year behaves like an annual identity anchor rather than a generic timestamp label.",
        ],
        primary_semantic_sources=[
            _legacy_source(
                source_ref="docs/business-background/customer_status_rules.md",
            )
        ],
        supporting_witness_sources=[
            _legacy_source(
                source_ref="src/work_data_hub/customer_status/service.py",
                source_type="legacy_code",
            )
        ],
        possible_non_equivalences=["status_year is not snapshot_month"],
        proxy_usage_refs=["src/work_data_hub/customer_status/service.py"],
        open_points=["Manual export reuse still needs confirmation."],
        promotion_recommendation={
            "recommended_action": "hold_ingress",
            "rationale": "Not evaluated yet.",
            "gate_failures": [],
            "requires_user_review": False,
        },
        promoted_claim_ids=[],
        created_at="2026-04-19T11:00:00Z",
    )


def _promotion_draft() -> SemanticPromotionDraft:
    return SemanticPromotionDraft(
        semantic_id="sem-status-year-identity-anchor",
        semantic_node_type="semantic_rule",
        title="Status year identity anchor",
        summary="status_year is an annual semantic anchor for customer-status semantics.",
        business_conclusion=(
            "status_year is an annual identity anchor for customer-status semantics, "
            "not a generic timestamp label."
        ),
        non_equivalent_to=["sem-non-equivalence-status-year-vs-snapshot-month"],
        confidence="high",
        last_verified="2026-04-19",
        main_conclusion_stable=True,
        open_points_do_not_overturn=True,
    )


def _load_ingress_index(registry_root: Path) -> dict[str, object]:
    return yaml.safe_load(
        (
            registry_root
            / "ingress"
            / "waves"
            / "wave-2026-04-16-registry-bootstrap"
            / "index.yaml"
        ).read_text(encoding="utf-8")
    )


def test_ingress_record_relative_path_shape() -> None:
    record = _build_finding()

    assert LEGACY_WORKSPACE_ID == "legacy_work_data_hub"
    assert INGRESS_KIND_DIRECTORIES == {
        "question_cluster": "question-clusters",
        "finding": "findings",
    }
    assert ingress_relative_path(record) == Path(
        "ingress"
    ) / "waves" / "wave-2026-04-16-registry-bootstrap" / "findings" / (
        "ingress-wave-2026-04-16-registry-bootstrap-manual-entry-runtime-boundary.yaml"
    )


def test_question_cluster_relative_path_and_index_branch_shape(tmp_path: Path) -> None:
    registry_root = tmp_path / "legacy-semantic-map"
    bootstrap_semantic_map(registry_root)

    record = _build_question_cluster()

    assert ingress_relative_path(record) == Path(
        "ingress"
    ) / "waves" / "wave-2026-04-16-registry-bootstrap" / "question-clusters" / (
        "ingress-wave-2026-04-16-registry-bootstrap-manual-entry-question-cluster.yaml"
    )

    output_path = write_ingress_record(registry_root, record)

    assert output_path == (
        registry_root
        / "ingress"
        / "waves"
        / "wave-2026-04-16-registry-bootstrap"
        / "question-clusters"
        / "ingress-wave-2026-04-16-registry-bootstrap-manual-entry-question-cluster.yaml"
    )

    ingress_index = _load_ingress_index(registry_root)
    assert ingress_index["question_clusters"] == [
        {
            "ingress_id": record.ingress_id,
            "title": record.title,
            "path": (
                "ingress/waves/wave-2026-04-16-registry-bootstrap/question-clusters/"
                "ingress-wave-2026-04-16-registry-bootstrap-manual-entry-question-cluster.yaml"
            ),
            "promotion_state": "requires_user_review",
        }
    ]
    assert ingress_index["findings"] == []


def test_write_ingress_record_writes_yaml_and_updates_wave_index(tmp_path: Path) -> None:
    registry_root = tmp_path / "legacy-semantic-map"
    bootstrap_semantic_map(registry_root)

    record = _build_finding()
    output_path = write_ingress_record(registry_root, record)

    assert output_path == (
        registry_root
        / "ingress"
        / "waves"
        / "wave-2026-04-16-registry-bootstrap"
        / "findings"
        / "ingress-wave-2026-04-16-registry-bootstrap-manual-entry-runtime-boundary.yaml"
    )

    payload = yaml.safe_load(output_path.read_text(encoding="utf-8"))
    assert payload["ingress_id"] == record.ingress_id
    assert payload["primary_semantic_sources"][0]["workspace_id"] == LEGACY_WORKSPACE_ID
    assert payload["supporting_witness_sources"][0]["source_type"] == "legacy_code"
    assert payload["promotion_recommendation"]["recommended_action"] == "hold_ingress"
    assert payload["promotion_recommendation"]["gate_failures"] == []
    assert payload["promotion_recommendation"]["requires_user_review"] is False
    assert payload["promoted_claim_ids"] == []
    assert payload["created_at"] == "2026-04-19T00:00:00Z"

    ingress_index = yaml.safe_load(
        (
            registry_root
            / "ingress"
            / "waves"
            / "wave-2026-04-16-registry-bootstrap"
            / "index.yaml"
        ).read_text(encoding="utf-8")
    )
    assert ingress_index == {
        "wave_id": "wave-2026-04-16-registry-bootstrap",
        "question_clusters": [],
        "findings": [
            {
                "ingress_id": record.ingress_id,
                "title": record.title,
                "path": (
                    "ingress/waves/wave-2026-04-16-registry-bootstrap/findings/"
                    "ingress-wave-2026-04-16-registry-bootstrap-manual-entry-runtime-boundary.yaml"
                ),
                "promotion_state": "hold_ingress",
            }
        ],
    }


def test_write_ingress_record_rewrites_same_ingress_id_without_duplicate_index_entry(
    tmp_path: Path,
) -> None:
    registry_root = tmp_path / "legacy-semantic-map"
    bootstrap_semantic_map(registry_root)

    original = _build_finding()
    updated = replace(
        original,
        title="Manual entry runtime boundary updated",
        promotion_recommendation={
            "recommended_action": "requires_user_review",
            "rationale": "The finding now needs user review.",
            "gate_failures": ["updated-conclusion"],
            "requires_user_review": True,
        },
    )

    write_ingress_record(registry_root, original)
    write_ingress_record(registry_root, updated)

    ingress_index = _load_ingress_index(registry_root)
    assert ingress_index["question_clusters"] == []
    assert ingress_index["findings"] == [
        {
            "ingress_id": original.ingress_id,
            "title": "Manual entry runtime boundary updated",
            "path": (
                "ingress/waves/wave-2026-04-16-registry-bootstrap/findings/"
                "ingress-wave-2026-04-16-registry-bootstrap-manual-entry-runtime-boundary.yaml"
            ),
            "promotion_state": "requires_user_review",
        }
    ]


def test_write_ingress_record_preserves_sibling_list_when_other_branch_updates(
    tmp_path: Path,
) -> None:
    registry_root = tmp_path / "legacy-semantic-map"
    bootstrap_semantic_map(registry_root)

    cluster = _build_question_cluster()
    finding = _build_finding()

    write_ingress_record(registry_root, cluster)
    write_ingress_record(registry_root, finding)

    ingress_index = _load_ingress_index(registry_root)
    assert ingress_index == {
        "wave_id": "wave-2026-04-16-registry-bootstrap",
        "question_clusters": [
            {
                "ingress_id": cluster.ingress_id,
                "title": cluster.title,
                "path": (
                    "ingress/waves/wave-2026-04-16-registry-bootstrap/question-clusters/"
                    "ingress-wave-2026-04-16-registry-bootstrap-manual-entry-question-cluster.yaml"
                ),
                "promotion_state": "requires_user_review",
            }
        ],
        "findings": [
            {
                "ingress_id": finding.ingress_id,
                "title": finding.title,
                "path": (
                    "ingress/waves/wave-2026-04-16-registry-bootstrap/findings/"
                    "ingress-wave-2026-04-16-registry-bootstrap-manual-entry-runtime-boundary.yaml"
                ),
                "promotion_state": "hold_ingress",
            }
        ],
    }


def test_write_ingress_record_rejects_non_legacy_source_records(tmp_path: Path) -> None:
    registry_root = tmp_path / "legacy-semantic-map"
    bootstrap_semantic_map(registry_root)

    record = _build_finding()
    wrong_workspace = replace(
        record,
        primary_semantic_sources=[
            replace(
                record.primary_semantic_sources[0],
                workspace_id="work_data_hub_pro",
            )
        ],
    )
    wrong_source_type = replace(
        record,
        supporting_witness_sources=[
            replace(
                record.supporting_witness_sources[0],
                source_type="current_wiki",
            )
        ],
    )

    with pytest.raises(ValueError, match="legacy source"):
        write_ingress_record(registry_root, wrong_workspace)

    with pytest.raises(ValueError, match="legacy source"):
        write_ingress_record(registry_root, wrong_source_type)


@pytest.mark.parametrize(
    ("source_field", "bad_path"),
    [
        ("primary_semantic_sources", "..\\docs\\domains\\annuity_performance-capability-map.md"),
        (
            "supporting_witness_sources",
            "E:/Projects/Elsewhere/src/work_data_hub/cli/etl/domain_validation.py",
        ),
    ],
)
def test_write_ingress_record_rejects_legacy_paths_outside_legacy_root(
    tmp_path: Path,
    source_field: str,
    bad_path: str,
) -> None:
    registry_root = tmp_path / "legacy-semantic-map"
    bootstrap_semantic_map(registry_root)

    record = _build_finding()
    invalid_source = replace(
        getattr(record, source_field)[0],
        source_ref=bad_path,
        relative_path=bad_path,
    )
    invalid_record = replace(record, **{source_field: [invalid_source]})

    with pytest.raises(ValueError, match="legacy root"):
        write_ingress_record(registry_root, invalid_record)


def test_ingress_recommendation_and_record_plan_fields_round_trip() -> None:
    record = _build_question_cluster()

    payload = record.to_payload()

    assert payload["promotion_recommendation"] == {
        "recommended_action": "requires_user_review",
        "rationale": "This cluster still needs semantic-boundary review before promotion.",
        "gate_failures": ["clustered_questions_not_collapsed"],
        "requires_user_review": True,
    }
    assert payload["promoted_claim_ids"] == []
    assert payload["created_at"] == "2026-04-19T00:00:00Z"


def test_promote_ingress_record_writes_minimum_semantic_claim(tmp_path: Path) -> None:
    registry_root = tmp_path / "legacy-semantic-map"
    bootstrap_semantic_map(registry_root)

    record = _promotion_ready_finding()
    write_ingress_record(registry_root, record)

    claim_path = promote_ingress_record(registry_root, record, _promotion_draft())

    assert claim_path == (
        registry_root
        / "claims"
        / "wave-2026-04-16-registry-bootstrap"
        / "semantic"
        / "claim-wave-2026-04-16-registry-bootstrap-status-year-identity-anchor.yaml"
    )

    claim_payload = yaml.safe_load(claim_path.read_text(encoding="utf-8"))
    assert claim_payload == {
        "claim_id": "claim-wave-2026-04-16-registry-bootstrap-status-year-identity-anchor",
        "wave_id": "wave-2026-04-16-registry-bootstrap",
        "claim_scope": "semantic",
        "claim_target_id": "sem-status-year-identity-anchor",
        "sources_read": [
            {
                "source_ref": "docs/business-background/customer_status_rules.md",
                "source_type": "legacy_doc",
                "note": (
                    "Legacy semantic evidence from "
                    "docs/business-background/customer_status_rules.md."
                ),
                "workspace_id": "legacy_work_data_hub",
                "relative_path": "docs/business-background/customer_status_rules.md",
                "semantic_authority": None,
            },
            {
                "source_ref": "src/work_data_hub/customer_status/service.py",
                "source_type": "legacy_code",
                "note": "Legacy semantic evidence from src/work_data_hub/customer_status/service.py.",
                "workspace_id": "legacy_work_data_hub",
                "relative_path": "src/work_data_hub/customer_status/service.py",
                "semantic_authority": None,
            },
        ],
        "objects_discovered": [],
        "edges_added": [],
        "candidates_raised": [],
        "open_questions": ["Manual export reuse still needs confirmation."],
        "compiled_into": [],
        "submitted_at": "2026-04-19T11:00:00Z",
        "semantic_findings": [
            {
                "semantic_id": "sem-status-year-identity-anchor",
                "semantic_node_type": "semantic_rule",
                "title": "Status year identity anchor",
                "summary": "status_year is an annual semantic anchor for customer-status semantics.",
                "business_conclusion": (
                    "status_year is an annual identity anchor for customer-status semantics, "
                    "not a generic timestamp label."
                ),
                "primary_source_refs": [
                    "docs/business-background/customer_status_rules.md",
                ],
                "supporting_source_refs": [
                    "src/work_data_hub/customer_status/service.py",
                ],
                "semantic_authority": "authoritative_semantic_source",
                "durable_target_pages": [],
                "confidence": "high",
                "last_verified": "2026-04-19",
                "open_questions": ["Manual export reuse still needs confirmation."],
                "non_equivalent_to": ["sem-non-equivalence-status-year-vs-snapshot-month"],
                "proposal_governance": None,
            }
        ],
        "trigger_id": None,
        "orchestration_iteration": None,
    }

    ingress_payload = yaml.safe_load(
        (
            registry_root
            / "ingress"
            / "waves"
            / "wave-2026-04-16-registry-bootstrap"
            / "findings"
            / "ingress-wave-2026-04-16-registry-bootstrap-status-year-anchor.yaml"
        ).read_text(encoding="utf-8")
    )
    assert ingress_payload["promotion_recommendation"] == {
        "recommended_action": "promote_to_semantic_claim",
        "rationale": "All structural promotion gates passed.",
        "gate_failures": [],
        "requires_user_review": False,
    }
    assert ingress_payload["promoted_claim_ids"] == [
        "claim-wave-2026-04-16-registry-bootstrap-status-year-identity-anchor",
    ]


def test_promote_ingress_record_rejects_structurally_blocked_promotion(
    tmp_path: Path,
) -> None:
    registry_root = tmp_path / "legacy-semantic-map"
    bootstrap_semantic_map(registry_root)

    record = _promotion_ready_finding()
    write_ingress_record(registry_root, record)

    blocked_promotion = SemanticPromotionDraft(
        semantic_id="sem-status-year-identity-anchor",
        semantic_node_type="semantic_rule",
        title="Status year identity anchor",
        summary="status_year is an annual semantic anchor for customer-status semantics.",
        business_conclusion=(
            "status_year is an annual identity anchor for customer-status semantics, "
            "not a generic timestamp label."
        ),
        non_equivalent_to=["sem-non-equivalence-status-year-vs-snapshot-month"],
        confidence="high",
        last_verified="2026-04-19",
        main_conclusion_stable=False,
        open_points_do_not_overturn=True,
    )

    with pytest.raises(
        ValueError,
        match=r"Promotion is not structurally allowed: .+",
    ):
        promote_ingress_record(registry_root, record, blocked_promotion)


def test_promote_ingress_record_rejects_overlapping_promoted_claim_id(
    tmp_path: Path,
) -> None:
    registry_root = tmp_path / "legacy-semantic-map"
    bootstrap_semantic_map(registry_root)

    record = _promotion_ready_finding()
    promotion = _promotion_draft()
    expected_claim_path = (
        registry_root
        / "claims"
        / "wave-2026-04-16-registry-bootstrap"
        / "semantic"
        / "claim-wave-2026-04-16-registry-bootstrap-status-year-identity-anchor.yaml"
    )
    overlapping_record = replace(
        record,
        ingress_id="ingress-wave-2026-04-16-registry-bootstrap-existing-status-year-overlap",
        title="Existing status year overlap",
        promoted_claim_ids=[
            "claim-wave-2026-04-16-registry-bootstrap-status-year-identity-anchor",
        ],
    )

    write_ingress_record(registry_root, overlapping_record)
    write_ingress_record(registry_root, record)

    with pytest.raises(
        ValueError,
        match=r"Promotion is not structurally allowed: requires_user_review",
    ):
        promote_ingress_record(registry_root, record, promotion)

    assert expected_claim_path.exists() is False

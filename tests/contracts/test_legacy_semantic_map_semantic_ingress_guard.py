from __future__ import annotations

from dataclasses import asdict
from pathlib import Path

import pytest
import yaml

from scripts.legacy_semantic_map.bootstrap import bootstrap_semantic_map
from scripts.legacy_semantic_map.ingress import (
    IngressPromotionRecommendation,
    IngressRecord,
    LEGACY_WORKSPACE_ID,
    write_ingress_record,
)
from scripts.legacy_semantic_map.claims import ClaimSourceRecord
from scripts.legacy_semantic_map.semantic_ingress_guard import (
    IngressGuardResult,
    SemanticPromotionDraft,
    guard_ingress_record,
)


def _legacy_source(relative_path: str, *, authority: str) -> ClaimSourceRecord:
    return ClaimSourceRecord(
        source_ref=relative_path,
        source_type="legacy_doc" if relative_path.endswith(".md") else "legacy_code",
        note="Legacy ingress guard fixture.",
        workspace_id=LEGACY_WORKSPACE_ID,
        relative_path=relative_path,
        semantic_authority=authority,
    )


def _record() -> IngressRecord:
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
                "docs/business-background/customer_status_rules.md",
                authority="authoritative_semantic_source",
            )
        ],
        supporting_witness_sources=[
            _legacy_source(
                "src/work_data_hub/customer_status/service.py",
                authority="runtime_witness",
            )
        ],
        possible_non_equivalences=["status_year is not snapshot_month"],
        proxy_usage_refs=["src/work_data_hub/customer_status/service.py"],
        open_points=["Manual export reuse still needs confirmation."],
        promotion_recommendation=IngressPromotionRecommendation(
            recommended_action="hold_ingress",
            rationale="Not evaluated yet.",
        ),
        created_at="2026-04-19T11:00:00Z",
    )


def _promotion() -> SemanticPromotionDraft:
    return SemanticPromotionDraft(
        semantic_id="sem-rule-status-year-identity-anchor",
        semantic_node_type="semantic_rule",
        title="Status year identity anchor",
        summary="status_year is an annual semantic anchor for customer-status semantics.",
        business_conclusion="status_year is an annual identity anchor for customer-status semantics, not a generic timestamp label.",
        non_equivalent_to=["sem-non-equivalence-status-year-vs-snapshot-month"],
        confidence="high",
        last_verified="2026-04-19",
        main_conclusion_stable=True,
        open_points_do_not_overturn=True,
    )


def test_guard_resolves_active_open_wave_and_allowed_targets(tmp_path: Path) -> None:
    registry_root = tmp_path / "legacy-semantic-map"
    bootstrap_semantic_map(registry_root)

    result = guard_ingress_record(registry_root, _record(), _promotion())

    assert result.wave_id == "wave-2026-04-16-registry-bootstrap"
    assert result.allowed_write_targets == [
        "ingress/waves/wave-2026-04-16-registry-bootstrap/findings",
        "claims/wave-2026-04-16-registry-bootstrap/semantic",
    ]
    assert result.promotion_status == "ready"
    assert result.evidence_boundary_failures == []
    assert result.overlap_hits == []


def test_guard_blocks_when_record_wave_does_not_match_active_wave(tmp_path: Path) -> None:
    registry_root = tmp_path / "legacy-semantic-map"
    bootstrap_semantic_map(registry_root)
    waves_index_path = registry_root / "waves" / "index.yaml"
    waves_index = yaml.safe_load(waves_index_path.read_text(encoding="utf-8"))
    followup_wave_id = "wave-2026-04-20-semantic-followup"
    waves_index["active_wave_id"] = followup_wave_id
    waves_index["waves"].append(
        {
            "wave_id": followup_wave_id,
            "title": "Semantic follow-up",
            "status": "active",
            "wave_ordinal": 2,
            "opened_at": "2026-04-20",
            "seeded_entry_surfaces": [],
            "seeded_high_priority_source_families": [],
            "admitted_subsystems": [],
            "durable_wiki_targets_accepted": False,
            "findings_disposition_complete": False,
            "depends_on_active_wave_working_state": False,
            "closed_at": None,
        }
    )
    waves_index_path.write_text(
        yaml.safe_dump(waves_index, sort_keys=False, allow_unicode=False),
        encoding="utf-8",
    )
    followup_ingress_root = registry_root / "ingress" / "waves" / followup_wave_id
    (followup_ingress_root / "question-clusters").mkdir(parents=True)
    (followup_ingress_root / "findings").mkdir(parents=True)
    (followup_ingress_root / "index.yaml").write_text(
        yaml.safe_dump(
            {
                "wave_id": followup_wave_id,
                "question_clusters": [],
                "findings": [],
            },
            sort_keys=False,
            allow_unicode=False,
        ),
        encoding="utf-8",
    )
    (registry_root / "claims" / followup_wave_id / "semantic").mkdir(parents=True)

    result = guard_ingress_record(registry_root, _record(), _promotion())

    assert result.promotion_status == "blocked"
    assert result.promotion_gate_failures == ["record_wave_mismatch"]
    assert result.allowed_write_targets == [
        "ingress/waves/wave-2026-04-16-registry-bootstrap/findings",
        "claims/wave-2026-04-16-registry-bootstrap/semantic",
    ]


def test_guard_blocks_ready_when_active_wave_scaffolding_is_missing(tmp_path: Path) -> None:
    registry_root = tmp_path / "legacy-semantic-map"
    bootstrap_semantic_map(registry_root)
    (
        registry_root
        / "ingress"
        / "waves"
        / "wave-2026-04-16-registry-bootstrap"
        / "index.yaml"
    ).unlink()
    (
        registry_root
        / "claims"
        / "wave-2026-04-16-registry-bootstrap"
        / "semantic"
        / ".gitkeep"
    ).unlink()
    (
        registry_root
        / "claims"
        / "wave-2026-04-16-registry-bootstrap"
        / "semantic"
    ).rmdir()

    result = guard_ingress_record(registry_root, _record(), _promotion())

    assert result.promotion_status == "blocked"
    assert result.promotion_gate_failures == [
        "missing_wave_ingress_index",
        "missing_wave_semantic_claim_dir",
    ]


def test_guard_rejects_current_repo_business_evidence(tmp_path: Path) -> None:
    registry_root = tmp_path / "legacy-semantic-map"
    bootstrap_semantic_map(registry_root)
    record = _record()
    invalid = IngressRecord(
        **(
            record.to_payload()
            | {
                "primary_semantic_sources": [
                    {
                        "source_ref": "docs/wiki-bi/concepts/customer-status.md",
                        "source_type": "current_wiki",
                        "note": "Current wiki is not valid ingress evidence.",
                        "workspace_id": "work_data_hub_pro",
                        "relative_path": "docs/wiki-bi/concepts/customer-status.md",
                        "semantic_authority": "implementation_hint",
                    }
                ]
            }
        )
    )

    result = guard_ingress_record(registry_root, invalid, _promotion())

    assert result.promotion_status == "blocked"
    assert "non_legacy_primary_source" in result.evidence_boundary_failures


@pytest.mark.parametrize(
    ("source_field", "bad_path", "expected_failure"),
    [
        (
            "primary_semantic_sources",
            "..\\docs\\business-background\\customer_status_rules.md",
            "escaped_legacy_primary_source_path",
        ),
        (
            "supporting_witness_sources",
            "E:/Projects/Elsewhere/customer_status/service.py",
            "escaped_legacy_supporting_source_path",
        ),
    ],
)
def test_guard_rejects_legacy_paths_that_escape_legacy_root(
    tmp_path: Path,
    source_field: str,
    bad_path: str,
    expected_failure: str,
) -> None:
    registry_root = tmp_path / "legacy-semantic-map"
    bootstrap_semantic_map(registry_root)
    record_payload = _record().to_payload()
    original_source = list(record_payload[source_field])[0]
    record_payload[source_field] = [
        {
            **original_source,
            "source_ref": bad_path,
            "relative_path": bad_path,
        }
    ]

    result = guard_ingress_record(registry_root, record_payload, _promotion())

    assert result.promotion_status == "blocked"
    assert expected_failure in result.evidence_boundary_failures


def test_guard_requires_user_review_when_semantic_id_already_exists(tmp_path: Path) -> None:
    registry_root = tmp_path / "legacy-semantic-map"
    bootstrap_semantic_map(registry_root)
    canonical_path = (
        registry_root
        / "semantic"
        / "rules"
        / "sem-rule-status-year-identity-anchor.yaml"
    )
    canonical_path.parent.mkdir(parents=True, exist_ok=True)
    canonical_path.write_text(
        yaml.safe_dump(
            {
                "semantic_id": "sem-rule-status-year-identity-anchor",
                "semantic_node_type": "semantic_rule",
            },
            sort_keys=False,
            allow_unicode=False,
        ),
        encoding="utf-8",
    )

    result = guard_ingress_record(registry_root, _record(), _promotion())

    assert result.promotion_status == "requires_user_review"
    assert result.requires_user_review is True
    assert result.overlap_hits[0]["path"] == (
        "semantic/rules/sem-rule-status-year-identity-anchor.yaml"
    )


def test_guard_requires_user_review_when_matching_ingress_record_already_exists(
    tmp_path: Path,
) -> None:
    registry_root = tmp_path / "legacy-semantic-map"
    bootstrap_semantic_map(registry_root)
    existing_path = (
        registry_root
        / "ingress"
        / "waves"
        / "wave-2026-04-16-registry-bootstrap"
        / "findings"
        / "existing-status-year-anchor.yaml"
    )
    existing_path.parent.mkdir(parents=True, exist_ok=True)
    existing_path.write_text(
        yaml.safe_dump(
            {
                **_record().to_payload(),
                "ingress_id": "existing-status-year-anchor",
                "title": "Existing status year anchor overlap",
                "promoted_claim_ids": [
                    "claim-wave-2026-04-16-registry-bootstrap-rule-status-year-identity-anchor"
                ],
            },
            sort_keys=False,
            allow_unicode=False,
        ),
        encoding="utf-8",
    )

    result = guard_ingress_record(registry_root, _record(), _promotion())

    assert result.promotion_status == "requires_user_review"
    assert result.requires_user_review is True
    assert result.overlap_hits[0]["path"] == (
        "ingress/waves/wave-2026-04-16-registry-bootstrap/findings/existing-status-year-anchor.yaml"
    )
    assert result.overlap_hits[0]["match_type"] == "promoted_semantic_target"


def test_guard_ignores_current_record_own_ingress_path_on_recheck(tmp_path: Path) -> None:
    registry_root = tmp_path / "legacy-semantic-map"
    bootstrap_semantic_map(registry_root)
    record = _record()
    promotion = _promotion()

    write_ingress_record(registry_root, record)
    result = guard_ingress_record(registry_root, record, promotion)

    assert result.promotion_status == "ready"
    assert result.requires_user_review is False
    assert result.overlap_hits == []


def test_guard_reports_exact_structural_failures_from_raw_payloads(tmp_path: Path) -> None:
    registry_root = tmp_path / "legacy-semantic-map"
    bootstrap_semantic_map(registry_root)

    result = guard_ingress_record(
        registry_root,
        {
            "ingress_id": "ingress-wave-2026-04-16-registry-bootstrap-incomplete-status-year-anchor",
            "wave_id": "wave-2026-04-16-registry-bootstrap",
            "ingress_kind": "finding",
            "title": "Incomplete status year anchor",
            "granularity_rationale": "Fixture for raw guard validation.",
            "questions": ["Is the raw guard path mechanical?"],
            "candidate_conclusions": ["Maybe."],
            "primary_semantic_sources": [],
            "supporting_witness_sources": [],
            "possible_non_equivalences": [],
            "proxy_usage_refs": [],
            "open_points": [],
            "promotion_recommendation": {
                "recommended_action": "hold_ingress",
                "rationale": "Not evaluated yet.",
                "gate_failures": [],
                "requires_user_review": False,
            },
            "promoted_claim_ids": [],
            "created_at": "2026-04-19T11:00:00Z",
        },
        {
            "semantic_id": "sem-rule-status-year-identity-anchor",
            "semantic_node_type": "",
            "title": "Status year identity anchor",
            "summary": "Incomplete promotion fixture.",
            "business_conclusion": "",
            "non_equivalent_to": [],
            "confidence": "high",
            "last_verified": "2026-04-19",
            "main_conclusion_stable": False,
            "open_points_do_not_overturn": False,
        },
    )

    assert result.promotion_status == "blocked"
    assert result.promotion_gate_failures == [
        "main_conclusion_not_stable",
        "missing_business_conclusion",
        "missing_primary_semantic_source",
        "missing_semantic_node_type",
        "missing_supporting_witness_source",
        "open_points_may_overturn_conclusion",
    ]


def test_guard_reports_missing_promotion_draft_from_raw_record_payload(tmp_path: Path) -> None:
    registry_root = tmp_path / "legacy-semantic-map"
    bootstrap_semantic_map(registry_root)

    result = guard_ingress_record(
        registry_root,
        {
            **_record().to_payload(),
        },
        None,
    )

    assert result.promotion_status == "blocked"
    assert result.promotion_gate_failures == ["missing_promotion_draft"]


def test_guard_blocks_invalid_raw_promotion_enum_values(tmp_path: Path) -> None:
    registry_root = tmp_path / "legacy-semantic-map"
    bootstrap_semantic_map(registry_root)

    result = guard_ingress_record(
        registry_root,
        {
            **_record().to_payload(),
        },
        {
            **asdict(_promotion()),
            "semantic_node_type": "semantic_widget",
            "confidence": "certain",
        },
    )

    assert result.promotion_status == "blocked"
    assert result.promotion_gate_failures == [
        "invalid_confidence",
        "invalid_semantic_node_type",
    ]


@pytest.mark.parametrize(
    ("ingress_kind", "expected_failure"),
    [
        (None, "missing_ingress_kind"),
        ("semantic_cluster", "invalid_ingress_kind"),
    ],
)
def test_guard_blocks_malformed_raw_record_ingress_kind_without_raising(
    tmp_path: Path,
    ingress_kind: str | None,
    expected_failure: str,
) -> None:
    registry_root = tmp_path / "legacy-semantic-map"
    bootstrap_semantic_map(registry_root)
    record_payload = {
        **_record().to_payload(),
    }
    if ingress_kind is None:
        record_payload.pop("ingress_kind")
    else:
        record_payload["ingress_kind"] = ingress_kind

    result = guard_ingress_record(
        registry_root,
        record_payload,
        _promotion(),
    )

    assert result.promotion_status == "blocked"
    assert result.promotion_gate_failures == [expected_failure]
    assert result.allowed_write_targets == [
        "claims/wave-2026-04-16-registry-bootstrap/semantic",
    ]


def test_guard_blocks_malformed_raw_source_payloads_without_raising(tmp_path: Path) -> None:
    registry_root = tmp_path / "legacy-semantic-map"
    bootstrap_semantic_map(registry_root)

    result = guard_ingress_record(
        registry_root,
        {
            **_record().to_payload(),
            "primary_semantic_sources": [{"source_ref": "x"}],
            "supporting_witness_sources": [{"source_ref": "y"}],
        },
        _promotion(),
    )

    assert result.promotion_status == "blocked"
    assert result.evidence_boundary_failures == [
        "malformed_primary_source",
        "malformed_supporting_source",
    ]
    assert result.promotion_gate_failures == [
        "missing_primary_semantic_source",
        "missing_supporting_witness_source",
    ]

from __future__ import annotations

import json
from pathlib import Path

import pytest

from work_data_hub_pro.governance.adjudication.service import (
    AdjudicationError,
    AdjudicationService,
)
from work_data_hub_pro.governance.evidence_index.file_store import FileEvidenceIndex
from work_data_hub_pro.platform.contracts.models import FieldTraceEvent


def _create_case(tmp_path: Path):
    evidence_index = FileEvidenceIndex(tmp_path)
    evidence_path = evidence_index.index_trace_events(
        batch_id="annuity_performance:2026-03",
        anchor_row_no=2,
        events=[
            FieldTraceEvent(
                trace_id="trace-001",
                event_id="evt-001",
                event_seq=1,
                run_id="run-001",
                batch_id="annuity_performance:2026-03",
                record_id="record-001",
                anchor_row_no=2,
                stage_id="fact_processing",
                field_name="company_name",
                value_before="Acme",
                value_after="ACME",
                rule_id="uppercase-company-name",
                rule_version="1",
                config_release_id="2026-04-11-annuity-performance-baseline",
                action_type="cleanse",
                timestamp="2026-04-11T00:00:00Z",
                success=True,
            )
        ],
    )
    service = AdjudicationService(evidence_index)
    case = service.create_case(
        sample_locator="reference/historical_replays/annuity_performance/legacy_monthly_snapshot_2026_03.json",
        legacy_result={"period": "2026-03", "contract_state_rows": 1},
        pro_result={"period": "2026-03", "contract_state_rows": 2},
        rationale="Replay differs from accepted baseline",
        affected_rule_version="annuity-performance-core:1",
        checkpoint_name="monthly_snapshot",
        comparison_run_id="comparison-001",
        involved_anchor_row_nos=[2],
    )
    return evidence_index, evidence_path, service, case


def test_adjudication_persists_pending_case_and_indexes_trace_events(tmp_path: Path) -> None:
    evidence_index, evidence_path, _, case = _create_case(tmp_path)

    stored = evidence_index.load_case(case.case_id)

    assert evidence_path.exists()
    assert stored.severity == "block"
    assert stored.decision_status == "pending_review"
    assert stored.decision_owner is None
    assert stored.resolution_note is None
    assert stored.closure_evidence == []
    assert stored.closed_at is None
    assert stored.closed_by is None
    assert stored.resolved_outcome is None
    assert stored.decision_history == []
    assert stored.precedent_status == "none"
    assert stored.precedent_key is None
    assert stored.checkpoint_name == "monthly_snapshot"
    assert stored.comparison_run_id == "comparison-001"
    assert stored.business_rationale == "Replay differs from accepted baseline"
    assert stored.involved_anchor_row_nos == [2]


@pytest.mark.parametrize("owner", ["", "   "])
def test_transition_rejects_missing_owner(tmp_path: Path, owner: str) -> None:
    _, _, service, case = _create_case(tmp_path)

    with pytest.raises(AdjudicationError) as exc:
        service.transition_case(
            case.case_id,
            status="approved_exception",
            owner=owner,
            resolution_note="Reviewed and accepted.",
        )

    assert exc.value.code == "missing_owner"


@pytest.mark.parametrize("resolution_note", ["", "   "])
def test_transition_rejects_empty_resolution_note(
    tmp_path: Path,
    resolution_note: str,
) -> None:
    _, _, service, case = _create_case(tmp_path)

    with pytest.raises(AdjudicationError) as exc:
        service.transition_case(
            case.case_id,
            status="approved_exception",
            owner="compatibility-review",
            resolution_note=resolution_note,
        )

    assert exc.value.code == "empty_resolution_note"


@pytest.mark.parametrize("closure_evidence", [[], ["", "   "]])
def test_close_case_rejects_empty_closure_evidence(
    tmp_path: Path,
    closure_evidence: list[str],
) -> None:
    _, _, service, case = _create_case(tmp_path)
    service.transition_case(
        case.case_id,
        status="approved_exception",
        owner="compatibility-review",
        resolution_note="Reviewed and accepted.",
    )

    with pytest.raises(AdjudicationError) as exc:
        service.close_case(
            case.case_id,
            owner="compatibility-review",
            resolution_note="Closing after filing closure proof.",
            closure_evidence=closure_evidence,
        )

    assert exc.value.code == "empty_closure_evidence"


def test_transition_rejects_illegal_status_change(tmp_path: Path) -> None:
    _, _, service, case = _create_case(tmp_path)

    with pytest.raises(AdjudicationError) as exc:
        service.transition_case(
            case.case_id,
            status="closed",
            owner="compatibility-review",
            resolution_note="Skipping directly to closure.",
        )

    assert exc.value.code == "illegal_transition"


def test_compatibility_case_mirror_matches_canonical_after_transition(tmp_path: Path) -> None:
    evidence_index, _, service, case = _create_case(tmp_path)

    transitioned = service.transition_case(
        case.case_id,
        status="approved_exception",
        owner="compatibility-review",
        resolution_note="Reviewed and approved as an exception.",
    )

    canonical_path = tmp_path / "compatibility_cases" / f"{case.case_id}.json"
    mirror_path = (
        tmp_path
        / "comparison_runs"
        / transitioned.comparison_run_id
        / "compatibility-case.json"
    )

    assert json.loads(canonical_path.read_text(encoding="utf-8")) == json.loads(
        mirror_path.read_text(encoding="utf-8")
    )


def test_closed_case_retains_resolved_outcome(tmp_path: Path) -> None:
    evidence_index, _, service, case = _create_case(tmp_path)

    service.transition_case(
        case.case_id,
        status="rejected_difference",
        owner="compatibility-review",
        resolution_note="Reviewed and rejected.",
    )
    closed = service.close_case(
        case.case_id,
        owner="compatibility-review",
        resolution_note="Closed with attached evidence.",
        closure_evidence=["reference/compatibility/closure-proof.json"],
    )

    stored = evidence_index.load_case(case.case_id)
    mirrored_payload = json.loads(
        (
            tmp_path
            / "comparison_runs"
            / closed.comparison_run_id
            / "compatibility-case.json"
        ).read_text(encoding="utf-8")
    )

    assert stored.decision_status == "closed"
    assert stored.decision_owner == "compatibility-review"
    assert stored.resolution_note == "Closed with attached evidence."
    assert stored.closure_evidence == ["reference/compatibility/closure-proof.json"]
    assert stored.closed_by == "compatibility-review"
    assert stored.closed_at is not None
    assert stored.resolved_outcome == "rejected_difference"
    assert stored.decision_history == [
        {
            "status": "rejected_difference",
            "owner": "compatibility-review",
            "resolution_note": "Reviewed and rejected.",
        },
        {
            "status": "closed",
            "owner": "compatibility-review",
            "resolution_note": "Closed with attached evidence.",
            "closure_evidence": ["reference/compatibility/closure-proof.json"],
            "closed_by": "compatibility-review",
            "closed_at": stored.closed_at,
        },
    ]
    assert mirrored_payload["resolved_outcome"] == "rejected_difference"
    assert mirrored_payload["decision_status"] == "closed"

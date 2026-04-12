from work_data_hub_pro.governance.adjudication.service import AdjudicationService
from work_data_hub_pro.governance.evidence_index.file_store import FileEvidenceIndex
from work_data_hub_pro.platform.contracts.models import FieldTraceEvent


def test_adjudication_persists_pending_case_and_indexes_trace_events(tmp_path) -> None:
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

    stored = evidence_index.load_case(case.case_id)

    assert evidence_path.exists()
    assert stored.severity == "block"
    assert stored.decision_status == "pending_review"
    assert stored.precedent_status == "none"
    assert stored.precedent_key is None
    assert stored.checkpoint_name == "monthly_snapshot"
    assert stored.comparison_run_id == "comparison-001"
    assert stored.business_rationale == "Replay differs from accepted baseline"
    assert stored.approved_by is None
    assert stored.involved_anchor_row_nos == [2]

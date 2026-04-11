from work_data_hub_pro.platform.contracts.models import (
    CanonicalFactRecord,
    FieldTraceEvent,
    InputBatch,
    InputRecord,
)
from work_data_hub_pro.platform.contracts.publication import (
    PublicationMode,
    PublicationPlan,
    PublicationTarget,
)
from work_data_hub_pro.platform.execution.run_context import RunContext


def test_input_record_preserves_trace_and_anchor_fields() -> None:
    batch = InputBatch(
        batch_id="annuity_performance:2026-03",
        domain="annuity_performance",
        period="2026-03",
        source_files=["annuity_performance_2026_03.xlsx"],
        input_snapshot_id="snapshot-001",
        row_count=1,
    )
    record = InputRecord(
        run_id="run-001",
        record_id="record-001",
        batch_id=batch.batch_id,
        anchor_row_no=12,
        origin_row_nos=[12],
        parent_record_ids=[],
        stage_row_no=12,
        raw_payload={"company_name": "Acme"},
    )
    fact = CanonicalFactRecord(
        run_id="run-001",
        record_id="fact-001",
        batch_id=batch.batch_id,
        domain="annuity_performance",
        fact_type="annuity_performance",
        fields={"company_name": "ACME"},
        lineage_ref="record-001",
        trace_ref="trace-001",
    )
    event = FieldTraceEvent(
        trace_id="trace-001",
        event_id="evt-001",
        event_seq=1,
        run_id="run-001",
        batch_id=batch.batch_id,
        record_id=record.record_id,
        anchor_row_no=12,
        stage_id="fact_processing",
        field_name="company_name",
        value_before="Acme",
        value_after="ACME",
        rule_id="uppercase-company-name",
        rule_version="1",
        config_release_id="release-001",
        action_type="normalize",
        timestamp="2026-04-11T00:00:00Z",
        success=True,
    )
    target = PublicationTarget(
        target_name="fact_annuity_performance",
        target_kind="fact",
        storage_adapter="in_memory",
        write_contract="canonical_fact_record",
        transaction_scope="fact-publication",
    )
    plan = PublicationPlan(
        publication_id="publication-001",
        target_name=target.target_name,
        target_kind=target.target_kind,
        mode=PublicationMode.REFRESH,
        refresh_keys=["batch_id"],
        upsert_keys=[],
        source_batch_id=batch.batch_id,
        source_run_id="run-001",
        idempotency_scope="batch",
        transaction_group="fact-publication",
    )
    context = RunContext(
        run_id="run-001",
        domain="annuity_performance",
        period="2026-03",
        config_release_id="2026-04-11-annuity-performance-baseline",
    )

    assert record.anchor_row_no == 12
    assert record.origin_row_nos == [12]
    assert fact.trace_ref == "trace-001"
    assert event.stage_id == "fact_processing"
    assert plan.mode is PublicationMode.REFRESH
    assert plan.transaction_group == "fact-publication"
    assert context.config_release_id == "2026-04-11-annuity-performance-baseline"

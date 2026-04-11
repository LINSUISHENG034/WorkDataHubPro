from work_data_hub_pro.platform.contracts.models import FieldTraceEvent
from work_data_hub_pro.platform.lineage.models import LineageLink
from work_data_hub_pro.platform.lineage.registry import LineageRegistry
from work_data_hub_pro.platform.tracing.in_memory_trace_store import InMemoryTraceStore


def test_trace_store_queries_primary_evidence_by_batch_and_anchor() -> None:
    store = InMemoryTraceStore()
    store.record(
        FieldTraceEvent(
            trace_id="trace-001",
            event_id="evt-001",
            event_seq=2,
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
            action_type="normalize",
            timestamp="2026-04-11T00:00:01Z",
            success=True,
        )
    )
    store.record(
        FieldTraceEvent(
            trace_id="trace-001",
            event_id="evt-000",
            event_seq=1,
            run_id="run-001",
            batch_id="annuity_performance:2026-03",
            record_id="record-001",
            anchor_row_no=2,
            stage_id="source_intake",
            field_name="raw_payload",
            value_before=None,
            value_after={"company_name": "Acme"},
            rule_id="capture-input",
            rule_version="1",
            config_release_id="2026-04-11-annuity-performance-baseline",
            action_type="snapshot",
            timestamp="2026-04-11T00:00:00Z",
            success=True,
        )
    )

    result = store.find(batch_id="annuity_performance:2026-03", anchor_row_no=2)

    assert [item.event_id for item in result] == ["evt-000", "evt-001"]


def test_lineage_registry_preserves_origin_rows_and_parent_links() -> None:
    registry = LineageRegistry()
    link = LineageLink(
        record_id="fact-001",
        parent_record_ids=["record-001"],
        origin_row_nos=[2],
        anchor_row_no=2,
    )

    registry.register(link)

    stored = registry.get("fact-001")
    assert stored is not None
    assert stored.parent_record_ids == ["record-001"]
    assert stored.origin_row_nos == [2]

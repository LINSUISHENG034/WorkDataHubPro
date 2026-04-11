from time import perf_counter

from work_data_hub_pro.platform.contracts.models import FieldTraceEvent
from work_data_hub_pro.platform.tracing.in_memory_trace_store import InMemoryTraceStore


def test_trace_lookup_micro_benchmark_stays_fast_for_small_in_memory_dataset() -> None:
    store = InMemoryTraceStore()
    for index in range(1, 1001):
        store.record(
            FieldTraceEvent(
                trace_id=f"trace-{index}",
                event_id=f"evt-{index}",
                event_seq=index,
                run_id="run-001",
                batch_id="annuity_performance:2026-03",
                record_id=f"record-{index}",
                anchor_row_no=index,
                stage_id="fact_processing",
                field_name="sales_amount",
                value_before=str(index),
                value_after=float(index),
                rule_id="parse-sales-amount",
                rule_version="1",
                config_release_id="2026-04-11-annuity-performance-baseline",
                action_type="cleanse",
                timestamp="2026-04-11T00:00:00Z",
                success=True,
            )
        )

    started = perf_counter()
    result = store.find(
        batch_id="annuity_performance:2026-03",
        anchor_row_no=500,
    )
    elapsed = perf_counter() - started

    assert result[0].event_id == "evt-500"
    assert elapsed < 0.5

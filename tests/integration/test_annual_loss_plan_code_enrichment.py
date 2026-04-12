from datetime import date

from work_data_hub_pro.capabilities.fact_processing.annual_loss.plan_code_lookup import (
    AnnualLossPlanCodeEnrichmentService,
    CustomerPlanHistoryLookup,
)
from work_data_hub_pro.platform.contracts.models import CanonicalFactRecord


def test_annual_loss_plan_code_enrichment_prefers_current_contract_rows_and_plan_type_prefix() -> None:
    service = AnnualLossPlanCodeEnrichmentService(
        CustomerPlanHistoryLookup(
            [
                {
                    "company_id": "company-001",
                    "product_line_code": "PL202",
                    "plan_code": "P9999",
                    "effective_period": "2027-01",
                    "valid_to": "2027-01-31",
                },
                {
                    "company_id": "company-001",
                    "product_line_code": "PL202",
                    "plan_code": "S7999",
                    "effective_period": "2025-12",
                    "valid_to": "9999-12-31",
                },
                {
                    "company_id": "company-001",
                    "product_line_code": "PL202",
                    "plan_code": "P9001",
                    "effective_period": "2025-12",
                },
            ]
        )
    )
    fact = CanonicalFactRecord(
        run_id="run-001",
        record_id="fact-001",
        batch_id="annual_loss:2026-03",
        domain="annual_loss",
        fact_type="annual_loss",
        fields={
            "company_id": "company-001",
            "product_line_code": "PL202",
            "plan_type": "集合计划",
            "plan_code": "",
            "period": "2026-03",
        },
        lineage_ref="record-001",
        trace_ref="trace:record-001",
    )

    enriched = service.enrich(
        fact,
        anchor_row_no=2,
        config_release_id="2026-04-12-annual-loss-baseline",
    )

    assert enriched.fact.fields["plan_code"] == "P9001"
    event = enriched.trace_events[0]
    assert event.rule_id == "customer_plan_history_lookup"
    assert event.stage_id == "fact_processing.plan_code_enrichment"
    assert event.field_name == "plan_code"
    assert event.value_before == ""
    assert event.value_after == "P9001"
    assert event.config_release_id == "2026-04-12-annual-loss-baseline"
    assert event.anchor_row_no == 2


def test_annual_loss_plan_code_enrichment_treats_string_coercible_valid_to_as_current() -> None:
    service = AnnualLossPlanCodeEnrichmentService(
        CustomerPlanHistoryLookup(
            [
                {
                    "company_id": "company-010",
                    "product_line_code": "PL201",
                    "plan_code": "S3001",
                    "effective_period": "2025-12",
                    "valid_to": date(9999, 12, 31),
                }
            ]
        )
    )
    fact = CanonicalFactRecord(
        run_id="run-001",
        record_id="fact-010",
        batch_id="annual_loss:2026-03",
        domain="annual_loss",
        fact_type="annual_loss",
        fields={
            "company_id": "company-010",
            "product_line_code": "PL201",
            "plan_type": "单一计划",
            "plan_code": "",
            "period": "2026-03",
        },
        lineage_ref="record-010",
        trace_ref="trace:record-010",
    )

    enriched = service.enrich(
        fact,
        anchor_row_no=10,
        config_release_id="2026-04-12-annual-loss-baseline",
    )

    assert enriched.fact.fields["plan_code"] == "S3001"
    event = enriched.trace_events[0]
    assert event.rule_id == "customer_plan_history_lookup"
    assert event.value_before == ""
    assert event.value_after == "S3001"


def test_annual_loss_plan_code_enrichment_falls_back_to_domain_default_when_lookup_misses() -> None:
    service = AnnualLossPlanCodeEnrichmentService(CustomerPlanHistoryLookup([]))
    fact = CanonicalFactRecord(
        run_id="run-001",
        record_id="fact-002",
        batch_id="annual_loss:2026-03",
        domain="annual_loss",
        fact_type="annual_loss",
        fields={
            "company_id": "company-002",
            "product_line_code": "PL201",
            "plan_type": "单一计划",
            "plan_code": "",
            "period": "2026-03",
        },
        lineage_ref="record-002",
        trace_ref="trace:record-002",
    )

    enriched = service.enrich(
        fact,
        anchor_row_no=3,
        config_release_id="2026-04-12-annual-loss-baseline",
    )

    assert enriched.fact.fields["plan_code"] == "AN002"
    event = enriched.trace_events[0]
    assert event.rule_id == "domain_default_plan_code"
    assert event.stage_id == "fact_processing.plan_code_enrichment"
    assert event.field_name == "plan_code"
    assert event.value_before == ""
    assert event.value_after == "AN002"
    assert event.config_release_id == "2026-04-12-annual-loss-baseline"
    assert event.anchor_row_no == 3


def test_annual_loss_plan_code_enrichment_preserves_source_plan_code() -> None:
    service = AnnualLossPlanCodeEnrichmentService(
        CustomerPlanHistoryLookup(
            [
                {
                    "company_id": "company-003",
                    "product_line_code": "PL202",
                    "plan_code": "P5000",
                    "effective_period": "2025-12",
                    "valid_to": "9999-12-31",
                }
            ]
        )
    )
    fact = CanonicalFactRecord(
        run_id="run-001",
        record_id="fact-003",
        batch_id="annual_loss:2026-03",
        domain="annual_loss",
        fact_type="annual_loss",
        fields={
            "company_id": "company-003",
            "product_line_code": "PL202",
            "plan_type": "集合计划",
            "plan_code": "SRC9000",
            "period": "2026-03",
        },
        lineage_ref="record-003",
        trace_ref="trace:record-003",
    )

    enriched = service.enrich(
        fact,
        anchor_row_no=4,
        config_release_id="2026-04-12-annual-loss-baseline",
    )

    assert enriched.fact.fields["plan_code"] == "SRC9000"
    event = enriched.trace_events[0]
    assert event.rule_id == "preserve_source_plan_code"
    assert event.value_before == "SRC9000"
    assert event.value_after == "SRC9000"


def test_annual_loss_plan_code_enrichment_falls_back_to_collective_default_plan_code() -> None:
    service = AnnualLossPlanCodeEnrichmentService(CustomerPlanHistoryLookup([]))
    fact = CanonicalFactRecord(
        run_id="run-001",
        record_id="fact-004",
        batch_id="annual_loss:2026-03",
        domain="annual_loss",
        fact_type="annual_loss",
        fields={
            "company_id": "company-004",
            "product_line_code": "PL202",
            "plan_type": "集合计划",
            "plan_code": "",
            "period": "2026-03",
        },
        lineage_ref="record-004",
        trace_ref="trace:record-004",
    )

    enriched = service.enrich(
        fact,
        anchor_row_no=5,
        config_release_id="2026-04-12-annual-loss-baseline",
    )

    assert enriched.fact.fields["plan_code"] == "AN001"
    event = enriched.trace_events[0]
    assert event.rule_id == "domain_default_plan_code"
    assert event.value_before == ""
    assert event.value_after == "AN001"

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
                    "plan_code": "S7999",
                    "effective_period": "2025-12",
                    "valid_to": "9999-12-31",
                },
                {
                    "company_id": "company-001",
                    "product_line_code": "PL202",
                    "plan_code": "P9001",
                    "effective_period": "2025-12",
                    "valid_to": "9999-12-31",
                },
                {
                    "company_id": "company-001",
                    "product_line_code": "PL202",
                    "plan_code": "P7000",
                    "effective_period": "2024-12",
                    "valid_to": "2025-12-31",
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
    assert enriched.trace_events[0].rule_id == "customer_plan_history_lookup"


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
    assert enriched.trace_events[0].rule_id == "domain_default_plan_code"

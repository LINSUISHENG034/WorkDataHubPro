from work_data_hub_pro.capabilities.fact_processing.annual_award.plan_code_lookup import (
    AnnualAwardPlanCodeEnrichmentService,
    CustomerPlanHistoryLookup,
)
from work_data_hub_pro.platform.contracts.models import CanonicalFactRecord


def test_plan_code_enrichment_prefers_customer_history_for_collective_plans() -> None:
    lookup = CustomerPlanHistoryLookup(
        [
            {
                "company_id": "company-001",
                "product_line_code": "PL-RET",
                "plan_code": "P9001",
                "effective_period": "2025-12",
            },
            {
                "company_id": "company-001",
                "product_line_code": "PL-RET",
                "plan_code": "S9001",
                "effective_period": "2025-12",
            },
        ]
    )
    fact = CanonicalFactRecord(
        run_id="run-001",
        record_id="fact-001",
        batch_id="annual_award:2026-03",
        domain="annual_award",
        fact_type="annual_award",
        fields={
            "company_name": "ACME",
            "company_id": "company-001",
            "plan_code": "",
            "plan_type": "COLLECTIVE",
            "product_line_code": "PL-RET",
            "period": "2026-03",
        },
        lineage_ref="record-001",
        trace_ref="trace:record-001",
    )

    enriched = AnnualAwardPlanCodeEnrichmentService(lookup).enrich(
        fact,
        anchor_row_no=2,
        config_release_id="2026-04-11-annual-award-baseline",
    )

    assert enriched.fact.fields["plan_code"] == "P9001"
    assert enriched.trace_events[0].rule_id == "customer_plan_history_lookup"


def test_plan_code_enrichment_falls_back_to_domain_default_when_history_misses() -> None:
    fact = CanonicalFactRecord(
        run_id="run-001",
        record_id="fact-002",
        batch_id="annual_award:2026-03",
        domain="annual_award",
        fact_type="annual_award",
        fields={
            "company_name": "BETA",
            "company_id": "company-002",
            "plan_code": "",
            "plan_type": "SINGLE",
            "product_line_code": "PL-ALT",
            "period": "2026-03",
        },
        lineage_ref="record-002",
        trace_ref="trace:record-002",
    )

    enriched = AnnualAwardPlanCodeEnrichmentService(CustomerPlanHistoryLookup([])).enrich(
        fact,
        anchor_row_no=3,
        config_release_id="2026-04-11-annual-award-baseline",
    )

    assert enriched.fact.fields["plan_code"] == "AN002"
    assert enriched.trace_events[0].rule_id == "domain_default_plan_code"

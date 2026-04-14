from work_data_hub_pro.capabilities.reference_derivation.service import (
    ReferenceDerivationService,
)
from work_data_hub_pro.platform.contracts.models import CanonicalFactRecord


def test_reference_derivation_builds_company_reference_candidates() -> None:
    service = ReferenceDerivationService()
    fact = CanonicalFactRecord(
        run_id="run-001",
        record_id="fact-001",
        batch_id="annuity_performance:2026-03",
        domain="annuity_performance",
        fact_type="annuity_performance",
        fields={
            "company_name": "ACME",
            "company_id": "company-001",
            "plan_code": "PLAN-A",
            "period": "2026-03",
        },
        lineage_ref="record-001",
        trace_ref="trace:record-001",
    )

    candidates = service.derive([fact])

    assert len(candidates) == 1
    assert candidates[0].target_object == "company_reference"
    assert candidates[0].candidate_payload["company_id"] == "company-001"
    assert candidates[0].candidate_payload["company_name"] == "ACME"


def test_reference_derivation_adds_customer_master_signal_for_annual_award() -> None:
    service = ReferenceDerivationService()
    fact = CanonicalFactRecord(
        run_id="run-001",
        record_id="fact-001",
        batch_id="annual_award:2026-03",
        domain="annual_award",
        fact_type="annual_award",
        fields={
            "company_name": "ACME",
            "company_id": "company-001",
            "plan_code": "P9001",
            "period": "2026-03",
        },
        lineage_ref="record-001",
        trace_ref="trace:record-001",
    )

    candidates = service.derive([fact])

    assert [candidate.target_object for candidate in candidates] == [
        "company_reference",
        "customer_master_signal",
    ]
    assert candidates[1].candidate_payload["customer_type"] == "WINNING_CUSTOMER"
    assert candidates[1].candidate_payload["award_tag"] == "2603-AWARD"


def test_reference_derivation_adds_customer_loss_signal_for_annual_loss() -> None:
    service = ReferenceDerivationService()
    fact = CanonicalFactRecord(
        run_id="run-001",
        record_id="fact-001",
        batch_id="annual_loss:2026-03",
        domain="annual_loss",
        fact_type="annual_loss",
        fields={
            "company_name": "共享客户（流失）",
            "company_id": "company-001",
            "plan_code": "P9001",
            "period": "2026-03",
        },
        lineage_ref="record-001",
        trace_ref="trace:record-001",
    )

    candidates = service.derive([fact])

    assert [candidate.target_object for candidate in candidates] == [
        "company_reference",
        "customer_loss_signal",
    ]
    assert candidates[1].candidate_payload["customer_type"] == "LOSS_CUSTOMER"
    assert candidates[1].candidate_payload["loss_tag"] == "2603-LOSS"


def test_reference_derivation_adds_customer_master_signal_for_annuity_income() -> None:
    service = ReferenceDerivationService()
    fact = CanonicalFactRecord(
        run_id="run-001",
        record_id="fact-001",
        batch_id="annuity_income:2026-03",
        domain="annuity_income",
        fact_type="annuity_income",
        fields={
            "company_name": "示例客户",
            "company_id": "company-001",
            "plan_code": "PLAN-A",
            "period": "2026-03",
        },
        lineage_ref="record-001",
        trace_ref="trace:record-001",
    )

    candidates = service.derive([fact])

    assert [candidate.target_object for candidate in candidates] == [
        "company_reference",
        "customer_master_signal",
    ]
    assert candidates[1].candidate_payload["customer_type"] == "INCOME_CUSTOMER"
    assert candidates[1].candidate_payload["income_tag"] == "2603-INCOME"

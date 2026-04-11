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

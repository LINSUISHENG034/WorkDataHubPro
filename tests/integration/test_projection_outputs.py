from work_data_hub_pro.capabilities.projections.contract_state import (
    ContractStateProjection,
)
from work_data_hub_pro.capabilities.projections.monthly_snapshot import (
    MonthlySnapshotProjection,
)
from work_data_hub_pro.platform.storage.in_memory_tables import InMemoryTableStore


def test_projections_consume_published_annual_award_facts_with_compatibility_bridge() -> None:
    storage = InMemoryTableStore(
        seed={
            "fact_annuity_performance": [
                {
                    "record_id": "fact-perf-001",
                    "company_id": "company-001",
                    "plan_code": "P9001",
                    "period": "2026-03",
                }
            ],
            "fact_annual_award": [
                {
                    "record_id": "fact-award-001",
                    "company_id": "company-001",
                    "plan_code": "P9001",
                    "period": "2026-03",
                }
            ],
            "fixture_annual_loss": [
                {
                    "company_id": "company-001",
                    "plan_code": "PLAN-Z",
                    "period": "2026-03",
                    "loss_code": "LOSS-99",
                    "source_sheet": "LossRegister",
                    "source_record_id": "loss-001",
                }
            ],
        }
    )
    contract_state = ContractStateProjection(storage)
    contract_rows = contract_state.run(
        publication_ids=["publication-fact-001"],
        period="2026-03",
    )
    storage.refresh("contract_state", contract_rows.rows)

    monthly_snapshot = MonthlySnapshotProjection(storage)
    snapshot_rows = monthly_snapshot.run(
        publication_ids=["publication-projection-001"],
        period="2026-03",
    )

    assert contract_rows.rows == [
        {
            "company_id": "company-001",
            "plan_code": "P9001",
            "period": "2026-03",
            "has_annuity_performance": True,
            "has_annual_award_fact": True,
            "has_annual_award_fixture": True,
            "has_annual_loss_fact": False,
            "has_annual_loss_fixture": False,
        }
    ]
    assert snapshot_rows.rows == [
        {
            "period": "2026-03",
            "contract_state_rows": 1,
            "award_fixture_rows": 1,
            "loss_fixture_rows": 0,
        }
    ]


def test_projections_consume_published_annual_loss_facts_with_compatibility_bridge() -> None:
    storage = InMemoryTableStore(
        seed={
            "fact_annuity_performance": [
                {
                    "record_id": "fact-perf-001",
                    "company_id": "company-001",
                    "plan_code": "P9001",
                    "period": "2026-03",
                }
            ],
            "fixture_annual_award": [
                {
                    "company_id": "company-001",
                    "plan_code": "P9001",
                    "period": "2026-03",
                    "source_record_id": "award-001",
                }
            ],
            "fact_annual_loss": [
                {
                    "record_id": "fact-loss-001",
                    "company_id": "company-001",
                    "plan_code": "P9001",
                    "period": "2026-03",
                }
            ],
        }
    )
    contract_state = ContractStateProjection(storage)
    contract_rows = contract_state.run(
        publication_ids=["publication-loss-facts"],
        period="2026-03",
    )
    storage.refresh("contract_state", contract_rows.rows)

    monthly_snapshot = MonthlySnapshotProjection(storage)
    snapshot_rows = monthly_snapshot.run(
        publication_ids=["publication-contract-state"],
        period="2026-03",
    )

    assert contract_rows.rows == [
        {
            "company_id": "company-001",
            "plan_code": "P9001",
            "period": "2026-03",
            "has_annuity_performance": True,
            "has_annual_award_fact": False,
            "has_annual_award_fixture": True,
            "has_annual_loss_fact": True,
            "has_annual_loss_fixture": True,
        }
    ]
    assert snapshot_rows.rows == [
        {
            "period": "2026-03",
            "contract_state_rows": 1,
            "award_fixture_rows": 1,
            "loss_fixture_rows": 1,
        }
    ]

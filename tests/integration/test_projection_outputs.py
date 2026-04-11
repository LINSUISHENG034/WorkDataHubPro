from work_data_hub_pro.capabilities.projections.contract_state import (
    ContractStateProjection,
)
from work_data_hub_pro.capabilities.projections.monthly_snapshot import (
    MonthlySnapshotProjection,
)
from work_data_hub_pro.platform.storage.in_memory_tables import InMemoryTableStore


def test_projections_consume_published_fact_and_fixture_publications_only() -> None:
    storage = InMemoryTableStore(
        seed={
            "fact_annuity_performance": [
                {
                    "record_id": "fact-001",
                    "company_id": "company-001",
                    "plan_code": "PLAN-A",
                    "period": "2026-03",
                }
            ],
            "fixture_annual_award": [
                {
                    "company_id": "company-001",
                    "plan_code": "PLAN-A",
                    "period": "2026-03",
                    "award_code": "AWARD-01",
                    "source_sheet": "AwardRegister",
                    "source_record_id": "award-001",
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
            "plan_code": "PLAN-A",
            "period": "2026-03",
            "has_annuity_performance": True,
            "has_annual_award_fixture": True,
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

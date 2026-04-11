from __future__ import annotations

from work_data_hub_pro.capabilities.projections.contract_state import ProjectionRows
from work_data_hub_pro.platform.contracts.models import ProjectionResult
from work_data_hub_pro.platform.storage.in_memory_tables import InMemoryTableStore


class MonthlySnapshotProjection:
    def __init__(self, storage: InMemoryTableStore) -> None:
        self._storage = storage

    def run(self, *, publication_ids: list[str], period: str) -> ProjectionRows:
        contract_state_rows = [
            row for row in self._storage.read("contract_state") if row["period"] == period
        ]
        rows = [
            {
                "period": period,
                "contract_state_rows": len(contract_state_rows),
                "award_fixture_rows": sum(
                    1 for row in contract_state_rows if row["has_annual_award_fixture"]
                ),
                "loss_fixture_rows": sum(
                    1 for row in contract_state_rows if row["has_annual_loss_fixture"]
                ),
            }
        ]
        return ProjectionRows(
            rows=rows,
            result=ProjectionResult(
                projection_name="monthly_snapshot",
                source_publications=publication_ids,
                affected_rows=len(rows),
                success=True,
            ),
        )

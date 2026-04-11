from __future__ import annotations

from dataclasses import dataclass

from work_data_hub_pro.platform.contracts.models import ProjectionResult
from work_data_hub_pro.platform.storage.in_memory_tables import InMemoryTableStore


@dataclass(frozen=True)
class ProjectionRows:
    rows: list[dict[str, object]]
    result: ProjectionResult


class ContractStateProjection:
    def __init__(self, storage: InMemoryTableStore) -> None:
        self._storage = storage

    def run(self, *, publication_ids: list[str], period: str) -> ProjectionRows:
        performance_rows = [
            row
            for row in self._storage.read("fact_annuity_performance")
            if row["period"] == period
        ]
        award_rows = self._storage.read("fixture_annual_award")
        loss_rows = self._storage.read("fixture_annual_loss")

        rows: list[dict[str, object]] = []
        for row in performance_rows:
            company_id = row["company_id"]
            plan_code = row["plan_code"]
            rows.append(
                {
                    "company_id": company_id,
                    "plan_code": plan_code,
                    "period": period,
                    "has_annuity_performance": True,
                    "has_annual_award_fixture": any(
                        fixture["company_id"] == company_id
                        and fixture["plan_code"] == plan_code
                        and fixture["period"] == period
                        for fixture in award_rows
                    ),
                    "has_annual_loss_fixture": any(
                        fixture["company_id"] == company_id
                        and fixture["plan_code"] == plan_code
                        and fixture["period"] == period
                        for fixture in loss_rows
                    ),
                }
            )

        return ProjectionRows(
            rows=rows,
            result=ProjectionResult(
                projection_name="contract_state",
                source_publications=publication_ids,
                affected_rows=len(rows),
                success=True,
            ),
        )

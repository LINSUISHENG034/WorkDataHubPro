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

    @staticmethod
    def _has_match(
        rows: list[dict[str, object]],
        *,
        company_id: str,
        plan_code: str,
        period: str,
    ) -> bool:
        return any(
            row["company_id"] == company_id
            and row["plan_code"] == plan_code
            and row["period"] == period
            for row in rows
        )

    def run(self, *, publication_ids: list[str], period: str) -> ProjectionRows:
        performance_rows = [
            row
            for row in self._storage.read("fact_annuity_performance")
            if row["period"] == period
        ]
        award_fact_rows = self._storage.read("fact_annual_award")
        award_fixture_rows = self._storage.read("fixture_annual_award")
        loss_rows = self._storage.read("fixture_annual_loss")

        rows: list[dict[str, object]] = []
        for row in performance_rows:
            company_id = row["company_id"]
            plan_code = row["plan_code"]
            has_award_fact = self._has_match(
                award_fact_rows,
                company_id=company_id,
                plan_code=plan_code,
                period=period,
            )
            has_award_fixture = has_award_fact or self._has_match(
                award_fixture_rows,
                company_id=company_id,
                plan_code=plan_code,
                period=period,
            )
            rows.append(
                {
                    "company_id": company_id,
                    "plan_code": plan_code,
                    "period": period,
                    "has_annuity_performance": True,
                    "has_annual_award_fact": has_award_fact,
                    "has_annual_award_fixture": has_award_fixture,
                    "has_annual_loss_fixture": self._has_match(
                        loss_rows,
                        company_id=company_id,
                        plan_code=plan_code,
                        period=period,
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

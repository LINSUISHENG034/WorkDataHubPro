from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

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
    def _build_index(rows: Iterable[dict[str, object]]) -> set[tuple[str, str, str]]:
        return {
            (
                str(row["company_id"]),
                str(row["plan_code"]),
                str(row["period"]),
            )
            for row in rows
        }

    @staticmethod
    def _has_match(
        rows: set[tuple[str, str, str]],
        *,
        company_id: str,
        plan_code: str,
        period: str,
    ) -> bool:
        return (company_id, plan_code, period) in rows

    def run(self, *, publication_ids: list[str], period: str) -> ProjectionRows:
        performance_rows = [
            row
            for row in self._storage.read("fact_annuity_performance")
            if row["period"] == period
        ]
        award_fact_rows = self._storage.read("fact_annual_award")
        award_fixture_rows = self._storage.read("fixture_annual_award")
        loss_fact_rows = self._storage.read("fact_annual_loss")
        loss_fixture_rows = self._storage.read("fixture_annual_loss")
        award_fact_index = self._build_index(award_fact_rows)
        award_fixture_index = self._build_index(award_fixture_rows)
        loss_fact_index = self._build_index(loss_fact_rows)
        loss_fixture_index = self._build_index(loss_fixture_rows)

        rows: list[dict[str, object]] = []
        for row in performance_rows:
            company_id = row["company_id"]
            plan_code = row["plan_code"]
            has_award_fact = self._has_match(
                award_fact_index,
                company_id=company_id,
                plan_code=plan_code,
                period=period,
            )
            has_award_fixture = has_award_fact or self._has_match(
                award_fixture_index,
                company_id=company_id,
                plan_code=plan_code,
                period=period,
            )
            has_loss_fact = self._has_match(
                loss_fact_index,
                company_id=company_id,
                plan_code=plan_code,
                period=period,
            )
            has_loss_fixture = has_loss_fact or self._has_match(
                loss_fixture_index,
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
                    "has_annual_loss_fact": has_loss_fact,
                    "has_annual_loss_fixture": has_loss_fixture,
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

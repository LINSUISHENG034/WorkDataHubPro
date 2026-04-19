from time import perf_counter

from work_data_hub_pro.capabilities.projections.contract_state import (
    ContractStateProjection,
)
from work_data_hub_pro.platform.storage.in_memory_tables import InMemoryTableStore


BENCHMARK_THRESHOLD_SECONDS = 0.5


def test_contract_state_projection_benchmark_stays_within_threshold() -> None:
    performance_rows: list[dict[str, object]] = []
    award_fact_rows: list[dict[str, object]] = []
    award_fixture_rows: list[dict[str, object]] = []
    loss_fact_rows: list[dict[str, object]] = []
    loss_fixture_rows: list[dict[str, object]] = []

    for index in range(1, 5001):
        company_id = f"company-{index:04d}"
        plan_code = f"P{index:05d}"
        period = "2026-03"
        performance_rows.append(
            {
                "record_id": f"perf-{index}",
                "company_id": company_id,
                "plan_code": plan_code,
                "period": period,
            }
        )
        if index % 2 == 0:
            award_fact_rows.append(
                {
                    "record_id": f"award-fact-{index}",
                    "company_id": company_id,
                    "plan_code": plan_code,
                    "period": period,
                }
            )
        if index % 3 == 0:
            award_fixture_rows.append(
                {
                    "company_id": company_id,
                    "plan_code": plan_code,
                    "period": period,
                    "source_record_id": f"award-fixture-{index}",
                }
            )
        if index % 4 == 0:
            loss_fact_rows.append(
                {
                    "record_id": f"loss-fact-{index}",
                    "company_id": company_id,
                    "plan_code": plan_code,
                    "period": period,
                }
            )
        if index % 5 == 0:
            loss_fixture_rows.append(
                {
                    "company_id": company_id,
                    "plan_code": plan_code,
                    "period": period,
                    "source_record_id": f"loss-fixture-{index}",
                }
            )

    storage = InMemoryTableStore(
        seed={
            "fact_annuity_performance": performance_rows,
            "fact_annual_award": award_fact_rows,
            "fixture_annual_award": award_fixture_rows,
            "fact_annual_loss": loss_fact_rows,
            "fixture_annual_loss": loss_fixture_rows,
        }
    )

    started = perf_counter()
    result = ContractStateProjection(storage).run(
        publication_ids=["publication-benchmark"],
        period="2026-03",
    )
    elapsed = perf_counter() - started

    rows_by_key = {
        (row["company_id"], row["plan_code"], row["period"]): row
        for row in result.rows
    }

    assert rows_by_key[("company-0006", "P00006", "2026-03")] == {
        "company_id": "company-0006",
        "plan_code": "P00006",
        "period": "2026-03",
        "has_annuity_performance": True,
        "has_annual_award_fact": True,
        "has_annual_award_fixture": True,
        "has_annual_loss_fact": False,
        "has_annual_loss_fixture": False,
    }
    assert rows_by_key[("company-0012", "P00012", "2026-03")] == {
        "company_id": "company-0012",
        "plan_code": "P00012",
        "period": "2026-03",
        "has_annuity_performance": True,
        "has_annual_award_fact": True,
        "has_annual_award_fixture": True,
        "has_annual_loss_fact": True,
        "has_annual_loss_fixture": True,
    }
    assert rows_by_key[("company-0001", "P00001", "2026-03")] == {
        "company_id": "company-0001",
        "plan_code": "P00001",
        "period": "2026-03",
        "has_annuity_performance": True,
        "has_annual_award_fact": False,
        "has_annual_award_fixture": False,
        "has_annual_loss_fact": False,
        "has_annual_loss_fixture": False,
    }
    assert elapsed < BENCHMARK_THRESHOLD_SECONDS


def test_contract_state_projection_matches_fixture_expectations() -> None:
    storage = InMemoryTableStore(
        seed={
            "fact_annuity_performance": [
                {
                    "record_id": "perf-both",
                    "company_id": "company-both",
                    "plan_code": "PLAN-BOTH",
                    "period": "2026-03",
                },
                {
                    "record_id": "perf-fact-only",
                    "company_id": "company-fact-only",
                    "plan_code": "PLAN-FACT",
                    "period": "2026-03",
                },
                {
                    "record_id": "perf-no-hit",
                    "company_id": "company-no-hit",
                    "plan_code": "PLAN-NONE",
                    "period": "2026-03",
                },
            ],
            "fact_annual_award": [
                {
                    "record_id": "award-fact-both",
                    "company_id": "company-both",
                    "plan_code": "PLAN-BOTH",
                    "period": "2026-03",
                },
                {
                    "record_id": "award-fact-only",
                    "company_id": "company-fact-only",
                    "plan_code": "PLAN-FACT",
                    "period": "2026-03",
                },
            ],
            "fixture_annual_award": [
                {
                    "company_id": "company-both",
                    "plan_code": "PLAN-BOTH",
                    "period": "2026-03",
                    "source_record_id": "award-fixture-both",
                }
            ],
            "fact_annual_loss": [
                {
                    "record_id": "loss-fact-both",
                    "company_id": "company-both",
                    "plan_code": "PLAN-BOTH",
                    "period": "2026-03",
                },
                {
                    "record_id": "loss-fact-only",
                    "company_id": "company-fact-only",
                    "plan_code": "PLAN-FACT",
                    "period": "2026-03",
                },
            ],
            "fixture_annual_loss": [
                {
                    "company_id": "company-both",
                    "plan_code": "PLAN-BOTH",
                    "period": "2026-03",
                    "source_record_id": "loss-fixture-both",
                }
            ],
        }
    )

    result = ContractStateProjection(storage).run(
        publication_ids=["publication-fixture-proof"],
        period="2026-03",
    )

    assert result.rows == [
        {
            "company_id": "company-both",
            "plan_code": "PLAN-BOTH",
            "period": "2026-03",
            "has_annuity_performance": True,
            "has_annual_award_fact": True,
            "has_annual_award_fixture": True,
            "has_annual_loss_fact": True,
            "has_annual_loss_fixture": True,
        },
        {
            "company_id": "company-fact-only",
            "plan_code": "PLAN-FACT",
            "period": "2026-03",
            "has_annuity_performance": True,
            "has_annual_award_fact": True,
            "has_annual_award_fixture": True,
            "has_annual_loss_fact": True,
            "has_annual_loss_fixture": True,
        },
        {
            "company_id": "company-no-hit",
            "plan_code": "PLAN-NONE",
            "period": "2026-03",
            "has_annuity_performance": True,
            "has_annual_award_fact": False,
            "has_annual_award_fixture": False,
            "has_annual_loss_fact": False,
            "has_annual_loss_fixture": False,
        },
    ]

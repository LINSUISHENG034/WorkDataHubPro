from pathlib import Path

from work_data_hub_pro.platform.contracts.publication import (
    PublicationMode,
)
from work_data_hub_pro.platform.publication.service import (
    PublicationBundle,
    PublicationService,
    build_publication_plan,
    load_publication_policy,
)
from work_data_hub_pro.platform.storage.in_memory_tables import InMemoryTableStore


def test_publication_service_executes_visible_transaction_groups() -> None:
    storage = InMemoryTableStore()
    service = PublicationService(storage)
    policy = load_publication_policy(
        Path("config/policies/publication.json"),
        domain="annuity_performance",
    )
    results = service.execute(
        [
            PublicationBundle(
                plan=build_publication_plan(
                    policy=policy,
                    publication_id="publication-fact-001",
                    target_name="fact_annuity_performance",
                    target_kind="fact",
                    refresh_keys=["batch_id"],
                    upsert_keys=[],
                    source_batch_id="annuity_performance:2026-03",
                    source_run_id="run-001",
                ),
                rows=[
                    {
                        "record_id": "fact-001",
                        "batch_id": "annuity_performance:2026-03",
                        "company_id": "company-001",
                    }
                ],
            ),
            PublicationBundle(
                plan=build_publication_plan(
                    policy=policy,
                    publication_id="publication-ref-001",
                    target_name="company_reference",
                    target_kind="reference",
                    refresh_keys=[],
                    upsert_keys=["company_id"],
                    source_batch_id="annuity_performance:2026-03",
                    source_run_id="run-001",
                ),
                rows=[
                    {
                        "company_id": "company-001",
                        "company_name": "ACME",
                    }
                ],
            ),
        ]
    )

    assert [result.transaction_group for result in results] == [
        "fact-publication",
        "reference-publication",
    ]
    assert [result.mode for result in results] == [
        PublicationMode.REFRESH,
        PublicationMode.UPSERT,
    ]
    assert storage.read("fact_annuity_performance")[0]["record_id"] == "fact-001"
    assert storage.read("company_reference")[0]["company_name"] == "ACME"


def test_publication_service_supports_annual_award_fact_and_signal_targets() -> None:
    storage = InMemoryTableStore()
    service = PublicationService(storage)
    policy = load_publication_policy(
        Path("config/policies/publication.json"),
        domain="annual_award",
    )

    results = service.execute(
        [
            PublicationBundle(
                plan=build_publication_plan(
                    policy=policy,
                    publication_id="publication-award-facts",
                    target_name="fact_annual_award",
                    target_kind="fact",
                    refresh_keys=["batch_id"],
                    upsert_keys=[],
                    source_batch_id="annual_award:2026-03",
                    source_run_id="run-001",
                ),
                rows=[
                    {
                        "record_id": "fact-001",
                        "batch_id": "annual_award:2026-03",
                        "company_id": "company-001",
                        "plan_code": "P9001",
                        "period": "2026-03",
                    }
                ],
            ),
            PublicationBundle(
                plan=build_publication_plan(
                    policy=policy,
                    publication_id="publication-customer-signal",
                    target_name="customer_master_signal",
                    target_kind="reference",
                    refresh_keys=[],
                    upsert_keys=["company_id", "period"],
                    source_batch_id="annual_award:2026-03",
                    source_run_id="run-001",
                ),
                rows=[
                    {
                        "company_id": "company-001",
                        "period": "2026-03",
                        "customer_type": "WINNING_CUSTOMER",
                    }
                ],
            ),
        ]
    )

    assert [result.target_name for result in results] == [
        "fact_annual_award",
        "customer_master_signal",
    ]
    assert storage.read("customer_master_signal")[0]["customer_type"] == "WINNING_CUSTOMER"


def test_publication_service_supports_annual_loss_fact_and_signal_targets() -> None:
    storage = InMemoryTableStore()
    service = PublicationService(storage)
    policy = load_publication_policy(
        Path("config/policies/publication.json"),
        domain="annual_loss",
    )

    results = service.execute(
        [
            PublicationBundle(
                plan=build_publication_plan(
                    policy=policy,
                    publication_id="publication-loss-facts",
                    target_name="fact_annual_loss",
                    target_kind="fact",
                    refresh_keys=["batch_id"],
                    upsert_keys=[],
                    source_batch_id="annual_loss:2026-03",
                    source_run_id="run-001",
                ),
                rows=[
                    {
                        "record_id": "fact-001",
                        "batch_id": "annual_loss:2026-03",
                        "company_id": "company-001",
                        "plan_code": "P9001",
                        "period": "2026-03",
                    }
                ],
            ),
            PublicationBundle(
                plan=build_publication_plan(
                    policy=policy,
                    publication_id="publication-loss-signal",
                    target_name="customer_loss_signal",
                    target_kind="reference",
                    refresh_keys=[],
                    upsert_keys=["company_id", "period"],
                    source_batch_id="annual_loss:2026-03",
                    source_run_id="run-001",
                ),
                rows=[
                    {
                        "company_id": "company-001",
                        "period": "2026-03",
                        "customer_type": "LOSS_CUSTOMER",
                    }
                ],
            ),
        ]
    )

    assert [result.target_name for result in results] == [
        "fact_annual_loss",
        "customer_loss_signal",
    ]
    assert storage.read("customer_loss_signal")[0]["customer_type"] == "LOSS_CUSTOMER"

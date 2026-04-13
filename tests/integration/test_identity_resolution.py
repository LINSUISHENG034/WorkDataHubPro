import os

import pytest

from work_data_hub_pro.capabilities.identity_resolution.service import (
    CacheFirstIdentityResolutionService,
    InMemoryIdentityCache,
    StaticIdentityProvider,
)
from work_data_hub_pro.capabilities.identity_resolution.temp_identity import (
    generate_temp_identity,
    load_temp_identity_policy,
    normalize_identity_fallback_input,
    temp_identity_prefix,
)
from work_data_hub_pro.platform.contracts.models import CanonicalFactRecord


@pytest.fixture(autouse=True)
def _temp_identity_salt(monkeypatch: pytest.MonkeyPatch) -> None:
    policy = load_temp_identity_policy()
    monkeypatch.setenv(str(policy["salt_env_var"]), "phase3-test-temp-identity-salt")


def test_identity_resolution_prefers_cache_and_records_evidence() -> None:
    service = CacheFirstIdentityResolutionService(
        cache=InMemoryIdentityCache({"ACME": "company-001"}),
        provider=StaticIdentityProvider({"BETA": "company-002"}),
    )
    fact = CanonicalFactRecord(
        run_id="run-001",
        record_id="fact-001",
        batch_id="annuity_performance:2026-03",
        domain="annuity_performance",
        fact_type="annuity_performance",
        fields={"company_name": "ACME", "plan_code": "PLAN-A", "period": "2026-03"},
        lineage_ref="record-001",
        trace_ref="trace:record-001",
    )

    resolved = service.resolve(
        fact,
        anchor_row_no=2,
        config_release_id="2026-04-11-annuity-performance-baseline",
    )

    assert resolved.result.resolved_identity == "company-001"
    assert resolved.result.resolution_method == "cache_hit"
    assert resolved.fact.fields["company_id"] == "company-001"
    assert resolved.result.evidence_refs == ["identity:cache_hit:fact-001"]
    assert resolved.result.evidence_details == {}


def test_identity_resolution_falls_back_to_temp_id_when_provider_misses() -> None:
    service = CacheFirstIdentityResolutionService(
        cache=InMemoryIdentityCache({}),
        provider=StaticIdentityProvider({}),
    )
    fact = CanonicalFactRecord(
        run_id="run-001",
        record_id="fact-002",
        batch_id="annuity_performance:2026-03",
        domain="annuity_performance",
        fact_type="annuity_performance",
        fields={"company_name": "OMEGA", "plan_code": "PLAN-Z", "period": "2026-03"},
        lineage_ref="record-002",
        trace_ref="trace:record-002",
    )

    resolved = service.resolve(
        fact,
        anchor_row_no=2,
        config_release_id="2026-04-11-annuity-performance-baseline",
    )
    expected_id = generate_temp_identity(
        normalize_identity_fallback_input("OMEGA"),
        salt=os.environ[str(load_temp_identity_policy()["salt_env_var"])],
        prefix=temp_identity_prefix(),
    )

    assert resolved.result.resolution_method == "temp_id_fallback"
    assert resolved.result.fallback_level == "temporary"
    assert resolved.fact.fields["company_id"] == expected_id
    assert resolved.result.resolved_identity == expected_id
    assert resolved.result.evidence_refs == ["identity:temp_id_fallback:fact-002"]
    assert "OMEGA" not in resolved.fact.fields["company_id"]
    assert all("OMEGA" not in ref for ref in resolved.result.evidence_refs)
    assert resolved.result.evidence_details == {
        "raw_company_name": "OMEGA",
        "normalized_company_name": "OMEGA",
    }


def test_identity_resolution_returns_none_for_placeholder_names() -> None:
    service = CacheFirstIdentityResolutionService(
        cache=InMemoryIdentityCache({}),
        provider=StaticIdentityProvider({}),
    )
    fact = CanonicalFactRecord(
        run_id="run-001",
        record_id="fact-003",
        batch_id="annuity_performance:2026-03",
        domain="annuity_performance",
        fact_type="annuity_performance",
        fields={"company_name": "空白", "plan_code": "PLAN-Z", "period": "2026-03"},
        lineage_ref="record-003",
        trace_ref="trace:record-003",
    )

    resolved = service.resolve(
        fact,
        anchor_row_no=3,
        config_release_id="2026-04-11-annuity-performance-baseline",
    )

    assert resolved.result.resolution_method == "temp_id_fallback"
    assert resolved.result.fallback_level == "temporary"
    assert resolved.fact.fields["company_id"] is None
    assert resolved.result.resolved_identity is None
    assert resolved.result.evidence_refs == ["identity:temp_id_fallback:fact-003"]
    assert resolved.result.evidence_details == {
        "raw_company_name": "空白",
        "normalized_company_name": None,
    }


def test_identity_resolution_preserves_source_company_id_before_cache_lookup() -> None:
    service = CacheFirstIdentityResolutionService(
        cache=InMemoryIdentityCache({"ACME": "company-cache-999"}),
        provider=StaticIdentityProvider({"ACME": "company-provider-999"}),
    )
    fact = CanonicalFactRecord(
        run_id="run-001",
        record_id="fact-001",
        batch_id="annual_award:2026-03",
        domain="annual_award",
        fact_type="annual_award",
        fields={
            "company_name": "ACME",
            "company_id": "company-source-001",
            "plan_code": "",
            "period": "2026-03",
        },
        lineage_ref="record-001",
        trace_ref="trace:record-001",
    )

    resolved = service.resolve(
        fact,
        anchor_row_no=2,
        config_release_id="2026-04-11-annual-award-baseline",
    )

    assert resolved.fact.fields["company_id"] == "company-source-001"
    assert resolved.result.resolution_method == "source_value"
    assert resolved.result.evidence_refs == ["identity:source_value:fact-001"]
    assert resolved.result.evidence_details == {}

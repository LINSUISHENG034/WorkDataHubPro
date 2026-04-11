from work_data_hub_pro.capabilities.identity_resolution.service import (
    CacheFirstIdentityResolutionService,
    InMemoryIdentityCache,
    StaticIdentityProvider,
)
from work_data_hub_pro.platform.contracts.models import CanonicalFactRecord


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
    assert resolved.result.evidence_refs == ["identity:cache_hit:ACME"]


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

    assert resolved.result.resolution_method == "temp_id_fallback"
    assert resolved.result.fallback_level == "temporary"
    assert resolved.fact.fields["company_id"] == "TEMP-OMEGA"

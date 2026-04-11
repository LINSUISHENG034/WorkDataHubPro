from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime

from work_data_hub_pro.capabilities.identity_resolution.interfaces import (
    IdentityCache,
    IdentityProvider,
)
from work_data_hub_pro.platform.contracts.models import (
    CanonicalFactRecord,
    FieldTraceEvent,
    IdentityResolutionResult,
)


class InMemoryIdentityCache:
    def __init__(self, seed: dict[str, str] | None = None) -> None:
        self._values = dict(seed or {})

    def get(self, company_name: str) -> str | None:
        return self._values.get(company_name)

    def set(self, company_name: str, company_id: str) -> None:
        self._values[company_name] = company_id


class StaticIdentityProvider:
    def __init__(self, mapping: dict[str, str]) -> None:
        self._mapping = mapping

    def lookup(self, company_name: str) -> str | None:
        return self._mapping.get(company_name)


@dataclass(frozen=True)
class ResolvedFact:
    fact: CanonicalFactRecord
    result: IdentityResolutionResult
    trace_events: list[FieldTraceEvent]


class CacheFirstIdentityResolutionService:
    stage_id = "identity_resolution"

    def __init__(self, *, cache: IdentityCache, provider: IdentityProvider) -> None:
        self._cache = cache
        self._provider = provider

    def resolve(
        self,
        fact: CanonicalFactRecord,
        *,
        anchor_row_no: int,
        config_release_id: str,
    ) -> ResolvedFact:
        company_name = str(fact.fields["company_name"])
        cached_id = self._cache.get(company_name)

        if cached_id is not None:
            company_id = cached_id
            method = "cache_hit"
            fallback_level = "none"
        else:
            provider_id = self._provider.lookup(company_name)
            if provider_id is not None:
                company_id = provider_id
                self._cache.set(company_name, provider_id)
                method = "provider_lookup"
                fallback_level = "none"
            else:
                company_id = f"TEMP-{company_name}"
                method = "temp_id_fallback"
                fallback_level = "temporary"

        updated_fields = dict(fact.fields)
        updated_fields["company_id"] = company_id
        updated_fact = CanonicalFactRecord(
            run_id=fact.run_id,
            record_id=fact.record_id,
            batch_id=fact.batch_id,
            domain=fact.domain,
            fact_type=fact.fact_type,
            fields=updated_fields,
            lineage_ref=fact.lineage_ref,
            trace_ref=fact.trace_ref,
        )
        result = IdentityResolutionResult(
            record_id=fact.record_id,
            resolved_identity=company_id,
            resolution_method=method,
            fallback_level=fallback_level,
            evidence_refs=[f"identity:{method}:{company_name}"],
        )
        trace_event = FieldTraceEvent(
            trace_id=fact.trace_ref,
            event_id=f"{fact.record_id}:identity",
            event_seq=100,
            run_id=fact.run_id,
            batch_id=fact.batch_id,
            record_id=fact.record_id,
            anchor_row_no=anchor_row_no,
            stage_id=self.stage_id,
            field_name="company_id",
            value_before=None,
            value_after=company_id,
            rule_id=method,
            rule_version="1",
            config_release_id=config_release_id,
            action_type="resolve_identity",
            timestamp=datetime.now(UTC).isoformat(),
            success=True,
        )
        return ResolvedFact(
            fact=updated_fact,
            result=result,
            trace_events=[trace_event],
        )

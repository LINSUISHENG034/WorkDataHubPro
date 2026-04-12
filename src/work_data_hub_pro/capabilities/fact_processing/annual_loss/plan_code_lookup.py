from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime

from work_data_hub_pro.platform.contracts.models import (
    CanonicalFactRecord,
    FieldTraceEvent,
)


@dataclass(frozen=True)
class EnrichedLossFact:
    fact: CanonicalFactRecord
    trace_events: list[FieldTraceEvent]


class CustomerPlanHistoryLookup:
    def __init__(self, rows: list[dict[str, object]]) -> None:
        self._rows = rows

    def select_plan_code(
        self,
        *,
        company_id: str,
        product_line_code: str,
        plan_type: str,
    ) -> str | None:
        candidates = sorted(
            [
                row
                for row in self._rows
                if row["company_id"] == company_id
                and row["product_line_code"] == product_line_code
                and str(row.get("valid_to", "9999-12-31")) == "9999-12-31"
            ],
            key=lambda row: str(row["effective_period"]),
            reverse=True,
        )
        preferred_prefix = "P" if plan_type == "集合计划" else "S"
        for row in candidates:
            plan_code = str(row["plan_code"])
            if plan_code.startswith(preferred_prefix):
                return plan_code
        return str(candidates[0]["plan_code"]) if candidates else None


class AnnualLossPlanCodeEnrichmentService:
    stage_id = "fact_processing.plan_code_enrichment"

    def __init__(self, lookup: CustomerPlanHistoryLookup) -> None:
        self._lookup = lookup

    def enrich(
        self,
        fact: CanonicalFactRecord,
        *,
        anchor_row_no: int,
        config_release_id: str,
    ) -> EnrichedLossFact:
        before = str(fact.fields.get("plan_code") or "")

        if before:
            plan_code = before
            method = "preserve_source_plan_code"
        else:
            lookup_plan_code = self._lookup.select_plan_code(
                company_id=str(fact.fields["company_id"]),
                product_line_code=str(fact.fields["product_line_code"]),
                plan_type=str(fact.fields["plan_type"]),
            )
            if lookup_plan_code is not None:
                plan_code = lookup_plan_code
                method = "customer_plan_history_lookup"
            else:
                plan_code = (
                    "AN001" if str(fact.fields["plan_type"]) == "集合计划" else "AN002"
                )
                method = "domain_default_plan_code"

        updated_fields = dict(fact.fields)
        updated_fields["plan_code"] = plan_code
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
        trace_event = FieldTraceEvent(
            trace_id=fact.trace_ref,
            event_id=f"{fact.record_id}:plan-code",
            event_seq=150,
            run_id=fact.run_id,
            batch_id=fact.batch_id,
            record_id=fact.record_id,
            anchor_row_no=anchor_row_no,
            stage_id=self.stage_id,
            field_name="plan_code",
            value_before=before,
            value_after=plan_code,
            rule_id=method,
            rule_version="1",
            config_release_id=config_release_id,
            action_type="enrich_plan_code",
            timestamp=datetime.now(UTC).isoformat(),
            success=True,
        )
        return EnrichedLossFact(fact=updated_fact, trace_events=[trace_event])

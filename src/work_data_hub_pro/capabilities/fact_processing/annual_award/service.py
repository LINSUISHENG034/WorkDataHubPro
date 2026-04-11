from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime

from work_data_hub_pro.capabilities.fact_processing.cleansing.manifest import (
    CleansingManifest,
)
from work_data_hub_pro.platform.contracts.models import (
    CanonicalFactRecord,
    FieldTraceEvent,
    InputRecord,
)


@dataclass(frozen=True)
class ProcessingResult:
    fact: CanonicalFactRecord
    trace_events: list[FieldTraceEvent]


class AnnualAwardProcessor:
    stage_id = "fact_processing"

    def __init__(self, manifest: CleansingManifest) -> None:
        self._manifest = manifest

    def process(self, record: InputRecord) -> ProcessingResult:
        cleaned_fields = dict(record.raw_payload)
        trace_events: list[FieldTraceEvent] = []

        for event_seq, active_rule in enumerate(self._manifest.active_rules, start=1):
            before = cleaned_fields.get(active_rule.field_name)
            error_message: str | None = None
            success = True

            if active_rule.field_name not in cleaned_fields:
                after = None
                success = False
                error_message = f"missing field: {active_rule.field_name}"
            else:
                after = active_rule.rule.transform(before)
                cleaned_fields[active_rule.field_name] = after

            trace_events.append(
                FieldTraceEvent(
                    trace_id=f"trace:{record.record_id}",
                    event_id=f"{record.record_id}:{event_seq}",
                    event_seq=event_seq,
                    run_id=record.run_id,
                    batch_id=record.batch_id,
                    record_id=record.record_id,
                    anchor_row_no=record.anchor_row_no,
                    stage_id=self.stage_id,
                    field_name=active_rule.field_name,
                    value_before=before,
                    value_after=after,
                    rule_id=active_rule.rule.rule_id,
                    rule_version=f"{self._manifest.rule_pack_version}.{active_rule.rule.version}",
                    config_release_id=self._manifest.release_id,
                    action_type="cleanse",
                    timestamp=datetime.now(UTC).isoformat(),
                    success=success,
                    error_message=error_message,
                )
            )

        cleaned_fields["business_type"] = self._derive_business_type(
            cleaned_fields.get("source_sheet")
        )

        fact = CanonicalFactRecord(
            run_id=record.run_id,
            record_id=f"fact:{record.record_id}",
            batch_id=record.batch_id,
            domain="annual_award",
            fact_type="annual_award",
            fields=cleaned_fields,
            lineage_ref=record.record_id,
            trace_ref=f"trace:{record.record_id}",
        )
        return ProcessingResult(fact=fact, trace_events=trace_events)

    @staticmethod
    def _derive_business_type(source_sheet: object) -> str:
        return "trustee_award" if source_sheet == "TrusteeAwards" else "investee_award"

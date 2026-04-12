from __future__ import annotations

from typing import Iterable

from work_data_hub_pro.platform.contracts.models import (
    FieldTraceEvent,
    InputBatch,
    InputRecord,
)
from work_data_hub_pro.platform.contracts.publication import PublicationMode, PublicationPlan


def validate_input_batch(batch: InputBatch) -> None:
    missing_fields = [
        field_name
        for field_name in (
            "batch_id",
            "domain",
            "period",
            "input_snapshot_id",
        )
        if not getattr(batch, field_name)
    ]
    if missing_fields:
        raise ValueError(
            f"Input batch missing required fields: {', '.join(missing_fields)}"
        )
    if not batch.source_files:
        raise ValueError("Input batch must include at least one source file.")
    if batch.row_count < 0:
        raise ValueError("Input batch row_count must be zero or greater.")
    if batch.batch_id != f"{batch.domain}:{batch.period}":
        raise ValueError("Input batch_id must stay stable as <domain>:<period>.")


def validate_input_record(
    record: InputRecord,
    *,
    required_fields: Iterable[str] = (),
    alternative_field_groups: Iterable[Iterable[str]] = (),
) -> None:
    if not record.run_id or not record.record_id or not record.batch_id:
        raise ValueError("Input record must include run_id, record_id, and batch_id.")
    if record.anchor_row_no <= 0 or record.stage_row_no <= 0:
        raise ValueError("Input record row numbers must be positive integers.")
    if not record.origin_row_nos:
        raise ValueError("Input record must preserve origin_row_nos.")
    if not isinstance(record.raw_payload, dict):
        raise ValueError("Input record raw_payload must be a mapping.")

    missing_fields = [
        field_name
        for field_name in required_fields
        if not record.raw_payload.get(field_name)
    ]
    if missing_fields:
        raise ValueError(
            f"Input record missing required fields: {', '.join(missing_fields)}"
        )

    for field_group in alternative_field_groups:
        if not any(record.raw_payload.get(field_name) for field_name in field_group):
            rendered_group = " or ".join(field_group)
            raise ValueError(
                f"Input record must include at least one of: {rendered_group}"
            )


def validate_trace_sequence(events: list[FieldTraceEvent]) -> None:
    if not events:
        return
    expected_anchor_row = events[0].anchor_row_no
    previous_event_seq = -1
    for event in events:
        if event.anchor_row_no != expected_anchor_row:
            raise ValueError("Trace events must keep a stable anchor_row_no.")
        if event.event_seq <= previous_event_seq:
            raise ValueError("Trace events must use a strictly increasing event_seq.")
        previous_event_seq = event.event_seq


def validate_publication_plan(plan: PublicationPlan) -> None:
    if not plan.publication_id or not plan.target_name or not plan.target_kind:
        raise ValueError(
            "Publication plan must include publication_id, target_name, and target_kind."
        )
    if not plan.source_batch_id or not plan.source_run_id:
        raise ValueError("Publication plan must include source batch and run identifiers.")
    if not plan.idempotency_scope or not plan.transaction_group:
        raise ValueError(
            "Publication plan must include idempotency_scope and transaction_group."
        )
    if plan.mode is PublicationMode.REFRESH and not plan.refresh_keys:
        raise ValueError("REFRESH publication plans must define refresh_keys.")
    if plan.mode is PublicationMode.UPSERT and not plan.upsert_keys:
        raise ValueError("UPSERT publication plans must define upsert_keys.")
    if plan.mode is PublicationMode.APPEND_ONLY and (
        plan.refresh_keys or plan.upsert_keys
    ):
        raise ValueError(
            "APPEND_ONLY publication plans must not define refresh_keys or upsert_keys."
        )

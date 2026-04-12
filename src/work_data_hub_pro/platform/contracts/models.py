from __future__ import annotations

from dataclasses import dataclass
from typing import Any

JsonObject = dict[str, Any]
JsonList = list[JsonObject]


@dataclass(frozen=True)
class InputBatch:
    batch_id: str
    domain: str
    period: str
    source_files: list[str]
    input_snapshot_id: str
    row_count: int


@dataclass(frozen=True)
class InputRecord:
    run_id: str
    record_id: str
    batch_id: str
    anchor_row_no: int
    origin_row_nos: list[int]
    parent_record_ids: list[str]
    stage_row_no: int
    raw_payload: dict[str, Any]


@dataclass(frozen=True)
class CanonicalFactRecord:
    run_id: str
    record_id: str
    batch_id: str
    domain: str
    fact_type: str
    fields: dict[str, Any]
    lineage_ref: str
    trace_ref: str


@dataclass(frozen=True)
class FieldTraceEvent:
    trace_id: str
    event_id: str
    event_seq: int
    run_id: str
    batch_id: str
    record_id: str
    anchor_row_no: int
    stage_id: str
    field_name: str
    value_before: Any
    value_after: Any
    rule_id: str
    rule_version: str
    config_release_id: str
    action_type: str
    timestamp: str
    success: bool
    error_message: str | None = None


@dataclass(frozen=True)
class IdentityResolutionResult:
    record_id: str
    resolved_identity: str
    resolution_method: str
    fallback_level: str
    evidence_refs: list[str]


@dataclass(frozen=True)
class DerivationCandidate:
    target_object: str
    candidate_payload: dict[str, Any]
    source_record_ids: list[str]
    derivation_rule_id: str
    derivation_rule_version: str


@dataclass(frozen=True)
class ProjectionResult:
    projection_name: str
    source_publications: list[str]
    affected_rows: int
    success: bool
    error_message: str | None = None

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class CheckpointFingerprint:
    fingerprint: str
    row_count: int
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class CheckpointDiff:
    missing_rows: list[dict[str, Any]] = field(default_factory=list)
    extra_rows: list[dict[str, Any]] = field(default_factory=list)
    changed_rows: list[dict[str, Any]] = field(default_factory=list)
    changed_fields: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class CheckpointResult:
    comparison_run_id: str
    checkpoint_name: str
    checkpoint_type: str
    status: str
    severity: str
    legacy_fingerprint: CheckpointFingerprint
    pro_fingerprint: CheckpointFingerprint
    diff_path: str | None
    trace_anchor_rows: list[int]
    diff: CheckpointDiff | None = None
    legacy_payload: Any | None = None
    pro_payload: Any | None = None


@dataclass(frozen=True)
class GateSummary:
    comparison_run_id: str
    overall_outcome: str
    total_checkpoints: int
    blocking_count: int
    warning_count: int
    passed_count: int
    severity_counts: dict[str, int]
    status_counts: dict[str, int]
    checkpoint_statuses: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class ComparisonRunManifest:
    comparison_run_id: str
    domain: str
    period: str
    baseline_version: str
    config_release_id: str
    rule_pack_version: str
    decision_owner: str
    package_root: str
    package_paths: dict[str, str] = field(default_factory=dict)

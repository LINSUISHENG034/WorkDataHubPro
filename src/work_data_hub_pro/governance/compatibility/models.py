from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


_ALLOWED_DECISION_STATUSES = {
    "pending_review",
    "approved_exception",
    "rejected_difference",
    "closed",
}


@dataclass(frozen=True)
class CompatibilityCase:
    case_id: str
    sample_locator: str
    legacy_result: dict[str, Any]
    pro_result: dict[str, Any]
    business_rationale: str
    affected_rule_version: str
    severity: str = "block"
    decision_status: str = "pending_review"
    decision_owner: str | None = None
    resolution_note: str | None = None
    closure_evidence: list[str] = field(default_factory=list)
    closed_at: str | None = None
    closed_by: str | None = None
    resolved_outcome: str | None = None
    decision_history: list[dict[str, object]] = field(default_factory=list)
    precedent_status: str = "none"
    precedent_key: str | None = None
    expires_at: str | None = None
    checkpoint_name: str = "monthly_snapshot"
    comparison_run_id: str = "comparison-unspecified"
    involved_anchor_row_nos: list[int] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.decision_status not in _ALLOWED_DECISION_STATUSES:
            raise ValueError(f"invalid_decision_status:{self.decision_status}")
        if self.resolved_outcome is not None and self.resolved_outcome not in {
            "approved_exception",
            "rejected_difference",
        }:
            raise ValueError(f"invalid_resolved_outcome:{self.resolved_outcome}")
        if self.decision_status == "pending_review" and self.resolved_outcome is not None:
            raise ValueError("pending_review_requires_null_resolved_outcome")
        if self.decision_status in {"approved_exception", "rejected_difference"}:
            if self.resolved_outcome != self.decision_status:
                raise ValueError("non_pending_status_requires_matching_resolved_outcome")
        if self.decision_status == "closed" and self.resolved_outcome is None:
            raise ValueError("closed_requires_resolved_outcome")

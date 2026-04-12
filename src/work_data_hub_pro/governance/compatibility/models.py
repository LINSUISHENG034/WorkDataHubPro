from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


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
    approved_by: str | None = None
    precedent_status: str = "none"
    precedent_key: str | None = None
    expires_at: str | None = None
    checkpoint_name: str = "monthly_snapshot"
    comparison_run_id: str = "comparison-unspecified"
    involved_anchor_row_nos: list[int] = field(default_factory=list)

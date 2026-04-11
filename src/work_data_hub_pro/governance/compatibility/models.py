from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class CompatibilityCase:
    case_id: str
    sample_locator: str
    legacy_result: dict[str, Any]
    pro_result: dict[str, Any]
    decision_status: str
    business_rationale: str
    approved_by: str | None
    affected_rule_version: str
    involved_anchor_row_nos: list[int] = field(default_factory=list)

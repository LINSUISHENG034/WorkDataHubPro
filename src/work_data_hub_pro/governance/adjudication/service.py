from __future__ import annotations

from uuid import uuid4

from work_data_hub_pro.governance.compatibility.models import CompatibilityCase
from work_data_hub_pro.governance.evidence_index.file_store import FileEvidenceIndex


class AdjudicationService:
    def __init__(self, evidence_index: FileEvidenceIndex) -> None:
        self._evidence_index = evidence_index

    def create_case(
        self,
        *,
        sample_locator: str,
        legacy_result: dict[str, object],
        pro_result: dict[str, object],
        involved_anchor_row_nos: list[int] | None = None,
        rationale: str,
        affected_rule_version: str,
    ) -> CompatibilityCase:
        case = CompatibilityCase(
            case_id=f"compat-{uuid4().hex[:8]}",
            sample_locator=sample_locator,
            legacy_result=legacy_result,
            pro_result=pro_result,
            involved_anchor_row_nos=sorted(set(involved_anchor_row_nos or [])),
            decision_status="pending_human_review",
            business_rationale=rationale,
            approved_by=None,
            affected_rule_version=affected_rule_version,
        )
        self._evidence_index.save_case(case)
        return case

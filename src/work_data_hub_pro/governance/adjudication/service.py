from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime
from uuid import uuid4

from work_data_hub_pro.governance.compatibility.models import CompatibilityCase
from work_data_hub_pro.governance.evidence_index.file_store import FileEvidenceIndex


class AdjudicationError(ValueError):
    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


class AdjudicationService:
    allowed_transitions = {
        "pending_review": {"approved_exception", "rejected_difference"},
        "approved_exception": {"closed"},
        "rejected_difference": {"closed"},
        "closed": set(),
    }

    def __init__(self, evidence_index: FileEvidenceIndex) -> None:
        self._evidence_index = evidence_index

    def _persist_case(self, case: CompatibilityCase) -> CompatibilityCase:
        self._evidence_index.save_case(case)
        self._evidence_index.write_comparison_case(case.comparison_run_id, case)
        return case

    def _load_case(self, case_id: str) -> CompatibilityCase:
        return self._evidence_index.load_case(case_id)

    def _require_owner(self, owner: str) -> str:
        if not owner.strip():
            raise AdjudicationError("missing_owner")
        return owner

    def _require_resolution_note(self, resolution_note: str) -> str:
        if not resolution_note.strip():
            raise AdjudicationError("empty_resolution_note")
        return resolution_note

    def _append_history(
        self,
        case: CompatibilityCase,
        *,
        status: str,
        owner: str,
        resolution_note: str,
        closure_evidence: list[str] | None = None,
        closed_by: str | None = None,
        closed_at: str | None = None,
    ) -> list[dict[str, object]]:
        history_entry: dict[str, object] = {
            "status": status,
            "owner": owner,
            "resolution_note": resolution_note,
        }
        if closure_evidence is not None:
            history_entry["closure_evidence"] = closure_evidence
        if closed_by is not None:
            history_entry["closed_by"] = closed_by
        if closed_at is not None:
            history_entry["closed_at"] = closed_at
        return [*case.decision_history, history_entry]

    def create_case(
        self,
        *,
        sample_locator: str,
        legacy_result: dict[str, object],
        pro_result: dict[str, object],
        involved_anchor_row_nos: list[int] | None = None,
        rationale: str,
        affected_rule_version: str,
        checkpoint_name: str = "monthly_snapshot",
        comparison_run_id: str | None = None,
        severity: str = "block",
        decision_status: str = "pending_review",
        precedent_status: str = "none",
        precedent_key: str | None = None,
        expires_at: str | None = None,
    ) -> CompatibilityCase:
        case = CompatibilityCase(
            case_id=f"compat-{uuid4().hex[:8]}",
            sample_locator=sample_locator,
            legacy_result=legacy_result,
            pro_result=pro_result,
            involved_anchor_row_nos=sorted(set(involved_anchor_row_nos or [])),
            business_rationale=rationale,
            affected_rule_version=affected_rule_version,
            severity=severity,
            decision_status=decision_status,
            decision_owner=None,
            resolution_note=None,
            closure_evidence=[],
            closed_at=None,
            closed_by=None,
            resolved_outcome=None,
            decision_history=[],
            precedent_status=precedent_status,
            precedent_key=precedent_key,
            expires_at=expires_at,
            checkpoint_name=checkpoint_name,
            comparison_run_id=comparison_run_id or f"comparison-{uuid4().hex[:8]}",
        )
        return self._persist_case(case)

    def assign_owner(self, case_id: str, owner: str) -> CompatibilityCase:
        assigned_owner = self._require_owner(owner)
        case = self._load_case(case_id)
        return self._persist_case(replace(case, decision_owner=assigned_owner))

    def transition_case(
        self,
        case_id: str,
        *,
        status: str,
        owner: str,
        resolution_note: str,
    ) -> CompatibilityCase:
        assigned_owner = self._require_owner(owner)
        note = self._require_resolution_note(resolution_note)
        case = self._load_case(case_id)
        if status not in self.allowed_transitions.get(case.decision_status, set()):
            raise AdjudicationError("illegal_transition")
        return self._persist_case(
            replace(
                case,
                decision_status=status,
                decision_owner=assigned_owner,
                resolution_note=note,
                resolved_outcome=status,
                decision_history=self._append_history(
                    case,
                    status=status,
                    owner=assigned_owner,
                    resolution_note=note,
                ),
            )
        )

    def close_case(
        self,
        case_id: str,
        *,
        owner: str,
        resolution_note: str,
        closure_evidence: list[str],
    ) -> CompatibilityCase:
        assigned_owner = self._require_owner(owner)
        note = self._require_resolution_note(resolution_note)
        if not any(item.strip() for item in closure_evidence):
            raise AdjudicationError("empty_closure_evidence")
        case = self._load_case(case_id)
        if "closed" not in self.allowed_transitions.get(case.decision_status, set()):
            raise AdjudicationError("illegal_transition")
        closed_at = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
        normalized_evidence = [item for item in closure_evidence if item.strip()]
        return self._persist_case(
            replace(
                case,
                decision_status="closed",
                decision_owner=assigned_owner,
                resolution_note=note,
                closure_evidence=normalized_evidence,
                closed_at=closed_at,
                closed_by=assigned_owner,
                decision_history=self._append_history(
                    case,
                    status="closed",
                    owner=assigned_owner,
                    resolution_note=note,
                    closure_evidence=normalized_evidence,
                    closed_by=assigned_owner,
                    closed_at=closed_at,
                ),
            )
        )

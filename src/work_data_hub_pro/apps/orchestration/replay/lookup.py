from __future__ import annotations

from dataclasses import asdict, dataclass

from work_data_hub_pro.apps.orchestration.replay.diagnostics import (
    _validate_comparison_run_id,
    load_replay_diagnostics,
)
from work_data_hub_pro.governance.evidence_index.file_store import FileEvidenceIndex


@dataclass(frozen=True)
class ReplayLookupResult:
    comparison_run_id: str
    record_id: str
    batch_id: str
    anchor_row_no: int
    origin_row_nos: list[int]
    parent_record_ids: list[str]
    trace_path: str | None
    artifact_gaps: list[str]
    checkpoint_statuses: dict[str, str]
    compatibility_case_id: str | None

    def to_payload(self) -> dict[str, object]:
        return asdict(self)


class ReplayLookupError(Exception):
    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


_ALLOWED_ERROR_CODES = {
    "missing_selector",
    "conflicting_selectors",
    "invalid_comparison_run_id",
    "record_not_found",
    "ambiguous_anchor",
    "missing_lineage_package",
    "malformed_lineage_package",
}


def _raise_lookup_error(code: str) -> None:
    if code not in _ALLOWED_ERROR_CODES:
        raise ValueError(code)
    raise ReplayLookupError(code)


def _select_record(
    records: list[dict[str, object]],
    *,
    record_id: str | None,
    anchor_row_no: int | None,
) -> dict[str, object]:
    if record_id is not None:
        for record in records:
            if record.get("record_id") == record_id:
                return record
        _raise_lookup_error("record_not_found")

    matches = [record for record in records if record.get("anchor_row_no") == anchor_row_no]
    if not matches:
        _raise_lookup_error("record_not_found")
    if len(matches) > 1:
        _raise_lookup_error("ambiguous_anchor")
    return matches[0]


def load_replay_lookup(
    comparison_run_id: str,
    *,
    record_id: str | None = None,
    anchor_row_no: int | None = None,
) -> ReplayLookupResult:
    if record_id is None and anchor_row_no is None:
        _raise_lookup_error("missing_selector")
    if record_id is not None and anchor_row_no is not None:
        _raise_lookup_error("conflicting_selectors")

    try:
        _validate_comparison_run_id(comparison_run_id)
    except ValueError as exc:
        raise ReplayLookupError("invalid_comparison_run_id") from exc

    diagnostics = load_replay_diagnostics(comparison_run_id)
    evidence_index = FileEvidenceIndex(diagnostics.comparison_run_root.parent.parent)
    try:
        lineage_impact = evidence_index.load_lineage_impact(comparison_run_id)
    except ValueError as exc:
        code = str(exc)
        if code in {"missing_lineage_package", "malformed_lineage_package"}:
            raise ReplayLookupError(code) from exc
        raise

    selected = _select_record(
        lineage_impact["records"],
        record_id=record_id,
        anchor_row_no=anchor_row_no,
    )
    compatibility_case = diagnostics.compatibility_case
    return ReplayLookupResult(
        comparison_run_id=comparison_run_id,
        record_id=str(selected["record_id"]),
        batch_id=str(selected["batch_id"]),
        anchor_row_no=int(selected["anchor_row_no"]),
        origin_row_nos=list(selected["origin_row_nos"]),
        parent_record_ids=list(selected["parent_record_ids"]),
        trace_path=selected["trace_path"],
        artifact_gaps=list(selected["artifact_gaps"]),
        checkpoint_statuses=dict(diagnostics.gate_summary.checkpoint_statuses),
        compatibility_case_id=(
            compatibility_case.case_id if compatibility_case is not None else None
        ),
    )


__all__ = [
    "ReplayLookupError",
    "ReplayLookupResult",
    "load_replay_lookup",
]

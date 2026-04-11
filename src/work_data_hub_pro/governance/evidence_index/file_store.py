from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from work_data_hub_pro.governance.compatibility.models import CompatibilityCase
from work_data_hub_pro.platform.contracts.models import FieldTraceEvent


class FileEvidenceIndex:
    def __init__(self, root: Path) -> None:
        self._root = root
        (self._root / "trace").mkdir(parents=True, exist_ok=True)
        (self._root / "compatibility_cases").mkdir(parents=True, exist_ok=True)

    def index_trace_events(
        self,
        *,
        batch_id: str,
        anchor_row_no: int,
        events: list[FieldTraceEvent],
    ) -> Path:
        path = self._root / "trace" / f"{batch_id.replace(':', '_')}__row_{anchor_row_no}.json"
        path.write_text(
            json.dumps([asdict(event) for event in events], indent=2),
            encoding="utf-8",
        )
        return path

    def save_case(self, case: CompatibilityCase) -> Path:
        path = self._root / "compatibility_cases" / f"{case.case_id}.json"
        path.write_text(json.dumps(asdict(case), indent=2), encoding="utf-8")
        return path

    def load_case(self, case_id: str) -> CompatibilityCase:
        path = self._root / "compatibility_cases" / f"{case_id}.json"
        return CompatibilityCase(**json.loads(path.read_text(encoding="utf-8")))

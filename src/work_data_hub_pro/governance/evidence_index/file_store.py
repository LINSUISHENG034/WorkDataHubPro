from __future__ import annotations

import json
from dataclasses import asdict, is_dataclass
from enum import Enum
from pathlib import Path
from typing import Any

from work_data_hub_pro.governance.compatibility.gate_models import (
    CheckpointDiff,
    CheckpointResult,
    ComparisonRunManifest,
    GateSummary,
)
from work_data_hub_pro.governance.compatibility.models import CompatibilityCase
from work_data_hub_pro.platform.contracts.models import FieldTraceEvent
from work_data_hub_pro.platform.contracts.publication import PublicationResult


def _to_jsonable(value: Any) -> Any:
    if is_dataclass(value):
        return _to_jsonable(asdict(value))
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, dict):
        return {key: _to_jsonable(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_to_jsonable(item) for item in value]
    return value


class FileEvidenceIndex:
    def __init__(self, root: Path) -> None:
        self._root = root
        (self._root / "trace").mkdir(parents=True, exist_ok=True)
        (self._root / "compatibility_cases").mkdir(parents=True, exist_ok=True)
        (self._root / "comparison_runs").mkdir(parents=True, exist_ok=True)

    def comparison_run_root(self, comparison_run_id: str) -> Path:
        root = self._root / "comparison_runs" / comparison_run_id
        (root / "diffs").mkdir(parents=True, exist_ok=True)
        return root

    def _write_json(self, path: Path, payload: Any) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(_to_jsonable(payload), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        return path

    def _write_text(self, path: Path, contents: str) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(contents, encoding="utf-8")
        return path

    def index_trace_events(
        self,
        *,
        batch_id: str,
        anchor_row_no: int,
        events: list[FieldTraceEvent],
    ) -> Path:
        path = self._root / "trace" / f"{batch_id.replace(':', '_')}__row_{anchor_row_no}.json"
        return self._write_json(path, events)

    def save_case(self, case: CompatibilityCase) -> Path:
        path = self._root / "compatibility_cases" / f"{case.case_id}.json"
        return self._write_json(path, case)

    def load_case(self, case_id: str) -> CompatibilityCase:
        path = self._root / "compatibility_cases" / f"{case_id}.json"
        return CompatibilityCase(**json.loads(path.read_text(encoding="utf-8")))

    def write_comparison_run_manifest(self, manifest: ComparisonRunManifest) -> Path:
        root = self.comparison_run_root(manifest.comparison_run_id)
        return self._write_json(root / "manifest.json", manifest)

    def write_gate_summary(self, comparison_run_id: str, summary: GateSummary) -> Path:
        root = self.comparison_run_root(comparison_run_id)
        return self._write_json(root / "gate-summary.json", summary)

    def write_checkpoint_results(
        self,
        comparison_run_id: str,
        results: list[CheckpointResult],
    ) -> Path:
        root = self.comparison_run_root(comparison_run_id)
        return self._write_json(root / "checkpoint-results.json", results)

    def write_source_intake_adaptation(
        self,
        comparison_run_id: str,
        payload: dict[str, Any],
    ) -> Path:
        root = self.comparison_run_root(comparison_run_id)
        return self._write_json(root / "source-intake-adaptation.json", payload)

    def write_lineage_impact(
        self,
        comparison_run_id: str,
        payload: dict[str, Any],
    ) -> Path:
        root = self.comparison_run_root(comparison_run_id)
        return self._write_json(root / "lineage-impact.json", payload)

    def write_publication_results(
        self,
        comparison_run_id: str,
        results: list[PublicationResult] | list[dict[str, Any]],
    ) -> Path:
        root = self.comparison_run_root(comparison_run_id)
        return self._write_json(root / "publication-results.json", results)

    def write_comparison_case(
        self,
        comparison_run_id: str,
        case: CompatibilityCase,
    ) -> Path:
        root = self.comparison_run_root(comparison_run_id)
        return self._write_json(root / "compatibility-case.json", case)

    def write_report(self, comparison_run_id: str, report_markdown: str) -> Path:
        root = self.comparison_run_root(comparison_run_id)
        return self._write_text(root / "report.md", report_markdown)

    def write_checkpoint_diff(
        self,
        comparison_run_id: str,
        checkpoint_name: str,
        diff: CheckpointDiff | dict[str, Any],
    ) -> Path:
        root = self.comparison_run_root(comparison_run_id)
        return self._write_json(root / "diffs" / f"{checkpoint_name}.json", diff)

from __future__ import annotations

import json
from dataclasses import asdict, is_dataclass
from enum import Enum
from pathlib import Path
from typing import Any

from work_data_hub_pro.governance.compatibility.gate_models import (
    CheckpointDiff,
    CheckpointFingerprint,
    CheckpointResult,
    ComparisonRunManifest,
    GateSummary,
)
from work_data_hub_pro.governance.compatibility.models import CompatibilityCase
from work_data_hub_pro.platform.contracts.models import FieldTraceEvent
from work_data_hub_pro.platform.contracts.publication import (
    PublicationMode,
    PublicationResult,
)


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


def _checkpoint_result_from_payload(payload: dict[str, Any]) -> CheckpointResult:
    return CheckpointResult(
        comparison_run_id=payload["comparison_run_id"],
        checkpoint_name=payload["checkpoint_name"],
        checkpoint_type=payload["checkpoint_type"],
        status=payload["status"],
        severity=payload["severity"],
        legacy_fingerprint=CheckpointFingerprint(**payload["legacy_fingerprint"]),
        pro_fingerprint=CheckpointFingerprint(**payload["pro_fingerprint"]),
        diff_path=payload.get("diff_path"),
        trace_anchor_rows=payload["trace_anchor_rows"],
        diff=CheckpointDiff(**payload["diff"]) if payload.get("diff") is not None else None,
        legacy_payload=payload.get("legacy_payload"),
        pro_payload=payload.get("pro_payload"),
    )


def _publication_result_from_payload(payload: dict[str, Any]) -> PublicationResult:
    return PublicationResult(
        publication_id=payload["publication_id"],
        target_name=payload["target_name"],
        mode=PublicationMode(payload["mode"]),
        affected_rows=payload["affected_rows"],
        transaction_group=payload["transaction_group"],
        success=payload["success"],
        error_message=payload.get("error_message"),
    )


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

    def _comparison_run_root_path(self, comparison_run_id: str) -> Path:
        return self._root / "comparison_runs" / comparison_run_id

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

    def _read_json(self, path: Path) -> Any:
        return json.loads(path.read_text(encoding="utf-8"))

    def _resolve_package_path_for_run(
        self,
        comparison_run_id: str,
        package_key: str,
        default_filename: str,
    ) -> Path:
        """Resolve a manifest package_path, rejecting absolute and escaping paths."""
        manifest = self.load_comparison_run_manifest(comparison_run_id)
        relative_path = manifest.package_paths.get(
            package_key,
            f"comparison_runs/{comparison_run_id}/{default_filename}",
        )
        path = Path(relative_path)
        if path.is_absolute():
            raise ValueError(
                f"package_paths['{package_key}'] is absolute: {path}; "
                "all package files must be relative to the evidence root"
            )
        resolved = (self._root / path).resolve()
        run_root = self._comparison_run_root_path(comparison_run_id).resolve()
        if not resolved.is_relative_to(run_root):
            raise ValueError(
                f"package_paths['{package_key}'] escapes comparison run package: "
                f"{resolved} is not inside {run_root}"
            )
        return resolved

    def _resolve_package_path(
        self,
        comparison_run_id: str,
        package_key: str,
        default_filename: str,
    ) -> Path:
        return self._resolve_package_path_for_run(
            comparison_run_id, package_key, default_filename
        )

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

    def load_comparison_run_manifest(self, comparison_run_id: str) -> ComparisonRunManifest:
        path = self._comparison_run_root_path(comparison_run_id) / "manifest.json"
        return ComparisonRunManifest(**self._read_json(path))

    def load_gate_summary(self, comparison_run_id: str) -> GateSummary:
        path = self._resolve_package_path(
            comparison_run_id,
            "gate_summary",
            "gate-summary.json",
        )
        return GateSummary(**self._read_json(path))

    def load_checkpoint_results(
        self,
        comparison_run_id: str,
    ) -> list[CheckpointResult]:
        path = self._resolve_package_path(
            comparison_run_id,
            "checkpoint_results",
            "checkpoint-results.json",
        )
        payload = self._read_json(path)
        return [_checkpoint_result_from_payload(item) for item in payload]

    def load_publication_results(
        self,
        comparison_run_id: str,
    ) -> list[PublicationResult]:
        path = self._resolve_package_path(
            comparison_run_id,
            "publication_results",
            "publication-results.json",
        )
        payload = self._read_json(path)
        return [_publication_result_from_payload(item) for item in payload]

    def load_comparison_case_for_run(
        self,
        comparison_run_id: str,
    ) -> CompatibilityCase:
        path = self._resolve_package_path(
            comparison_run_id,
            "compatibility_case",
            "compatibility-case.json",
        )
        return CompatibilityCase(**self._read_json(path))

    def load_report_markdown(self, comparison_run_id: str) -> str:
        path = self._resolve_package_path(
            comparison_run_id,
            "report",
            "report.md",
        )
        return path.read_text(encoding="utf-8")

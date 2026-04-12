from __future__ import annotations

import json
from collections import Counter
from dataclasses import replace
from hashlib import sha256
from pathlib import Path
from typing import Any, Iterable

from work_data_hub_pro.governance.compatibility.gate_models import (
    CheckpointDiff,
    CheckpointFingerprint,
    CheckpointResult,
    ComparisonRunManifest,
    GateSummary,
)
from work_data_hub_pro.governance.compatibility.models import CompatibilityCase
from work_data_hub_pro.governance.evidence_index.file_store import FileEvidenceIndex
from work_data_hub_pro.platform.contracts.publication import PublicationResult


def default_package_paths(comparison_run_id: str) -> dict[str, str]:
    root = f"comparison_runs/{comparison_run_id}"
    return {
        "manifest": f"{root}/manifest.json",
        "gate_summary": f"{root}/gate-summary.json",
        "checkpoint_results": f"{root}/checkpoint-results.json",
        "source_intake_adaptation": f"{root}/source-intake-adaptation.json",
        "lineage_impact": f"{root}/lineage-impact.json",
        "publication_results": f"{root}/publication-results.json",
        "compatibility_case": f"{root}/compatibility-case.json",
        "report": f"{root}/report.md",
    }


def _to_jsonable(value: Any) -> Any:
    if hasattr(value, "__dataclass_fields__"):
        return {
            field_name: _to_jsonable(getattr(value, field_name))
            for field_name in value.__dataclass_fields__
        }
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, dict):
        return {key: _to_jsonable(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_to_jsonable(item) for item in value]
    return value


def _row_count(payload: Any) -> int:
    if isinstance(payload, list):
        return len(payload)
    if isinstance(payload, dict):
        return len(payload)
    return 0 if payload is None else 1


def _fingerprint(payload: Any) -> str:
    normalized = json.dumps(
        _to_jsonable(payload),
        sort_keys=True,
        ensure_ascii=False,
        separators=(",", ":"),
    )
    return sha256(normalized.encode("utf-8")).hexdigest()


def _build_diff(legacy_payload: Any, pro_payload: Any) -> CheckpointDiff:
    if legacy_payload == pro_payload:
        return CheckpointDiff()

    if isinstance(legacy_payload, list) and isinstance(pro_payload, list):
        legacy_counter = Counter(
            json.dumps(_to_jsonable(item), sort_keys=True, ensure_ascii=False)
            for item in legacy_payload
        )
        pro_counter = Counter(
            json.dumps(_to_jsonable(item), sort_keys=True, ensure_ascii=False)
            for item in pro_payload
        )
        missing_rows: list[dict[str, Any]] = []
        extra_rows: list[dict[str, Any]] = []
        for item in legacy_payload:
            serialized = json.dumps(_to_jsonable(item), sort_keys=True, ensure_ascii=False)
            if legacy_counter[serialized] > pro_counter[serialized]:
                missing_rows.append(item)
                pro_counter[serialized] = 0
                legacy_counter[serialized] -= 1
        for item in pro_payload:
            serialized = json.dumps(_to_jsonable(item), sort_keys=True, ensure_ascii=False)
            if pro_counter[serialized] > legacy_counter[serialized]:
                extra_rows.append(item)
                legacy_counter[serialized] = 0
                pro_counter[serialized] -= 1
        changed_rows = []
        if not missing_rows and not extra_rows:
            changed_rows = [
                {
                    "legacy": legacy_payload,
                    "pro": pro_payload,
                }
            ]
        return CheckpointDiff(
            missing_rows=missing_rows,
            extra_rows=extra_rows,
            changed_rows=changed_rows,
        )

    if isinstance(legacy_payload, dict) and isinstance(pro_payload, dict):
        changed_fields = sorted(
            key
            for key in set(legacy_payload) | set(pro_payload)
            if legacy_payload.get(key) != pro_payload.get(key)
        )
        return CheckpointDiff(
            changed_rows=[{"legacy": legacy_payload, "pro": pro_payload}],
            changed_fields=changed_fields,
        )

    return CheckpointDiff(
        changed_rows=[{"legacy": legacy_payload, "pro": pro_payload}],
    )


def build_checkpoint_result(
    *,
    comparison_run_id: str,
    checkpoint_name: str,
    checkpoint_type: str,
    legacy_payload: Any,
    pro_payload: Any,
    trace_anchor_rows: Iterable[int],
    severity: str = "block",
    diff_path: str | None = None,
    legacy_metadata: dict[str, Any] | None = None,
    pro_metadata: dict[str, Any] | None = None,
) -> CheckpointResult:
    legacy_fingerprint = CheckpointFingerprint(
        fingerprint=_fingerprint(legacy_payload),
        row_count=_row_count(legacy_payload),
        metadata=legacy_metadata or {},
    )
    pro_fingerprint = CheckpointFingerprint(
        fingerprint=_fingerprint(pro_payload),
        row_count=_row_count(pro_payload),
        metadata=pro_metadata or {},
    )
    diff = _build_diff(legacy_payload, pro_payload)
    fingerprints_match = legacy_fingerprint.fingerprint == pro_fingerprint.fingerprint
    if fingerprints_match and not any(
        (
            diff.missing_rows,
            diff.extra_rows,
            diff.changed_rows,
            diff.changed_fields,
        )
    ):
        status = "passed"
    elif severity == "warn":
        status = "warning"
    else:
        status = "failed"

    return CheckpointResult(
        comparison_run_id=comparison_run_id,
        checkpoint_name=checkpoint_name,
        checkpoint_type=checkpoint_type,
        status=status,
        severity=severity,
        legacy_fingerprint=legacy_fingerprint,
        pro_fingerprint=pro_fingerprint,
        diff_path=diff_path,
        trace_anchor_rows=sorted(set(trace_anchor_rows)),
        diff=None if status == "passed" else diff,
    )


def summarize_gate_results(
    comparison_run_id: str,
    results: list[CheckpointResult],
) -> GateSummary:
    status_counts = Counter(result.status for result in results)
    severity_counts = Counter(
        result.severity for result in results if result.status != "passed"
    )
    if status_counts["failed"]:
        overall_outcome = "failed"
    elif status_counts["warning"]:
        overall_outcome = "warning"
    else:
        overall_outcome = "passed"
    return GateSummary(
        comparison_run_id=comparison_run_id,
        overall_outcome=overall_outcome,
        total_checkpoints=len(results),
        blocking_count=severity_counts.get("block", 0),
        warning_count=severity_counts.get("warn", 0),
        passed_count=status_counts.get("passed", 0),
        severity_counts={
            "block": severity_counts.get("block", 0),
            "warn": severity_counts.get("warn", 0),
        },
        status_counts={
            "failed": status_counts.get("failed", 0),
            "warning": status_counts.get("warning", 0),
            "passed": status_counts.get("passed", 0),
        },
        checkpoint_statuses={
            result.checkpoint_name: result.status for result in results
        },
    )


def write_comparison_run_package(
    *,
    evidence_index: FileEvidenceIndex,
    manifest: ComparisonRunManifest,
    gate_summary: GateSummary,
    checkpoint_results: list[CheckpointResult],
    checkpoint_diffs: dict[str, CheckpointDiff | dict[str, Any]],
    source_intake_adaptation: dict[str, Any],
    lineage_impact: dict[str, Any],
    publication_results: list[PublicationResult] | list[dict[str, Any]],
    compatibility_case: CompatibilityCase | None,
    report_markdown: str,
) -> dict[str, Path | dict[str, Path]]:
    package_paths = manifest.package_paths or default_package_paths(
        manifest.comparison_run_id
    )
    updated_package_paths = dict(package_paths)
    updated_results: list[CheckpointResult] = []
    diff_paths: dict[str, Path] = {}
    for result in checkpoint_results:
        relative_diff_path = (
            result.diff_path
            or f"comparison_runs/{manifest.comparison_run_id}/diffs/{result.checkpoint_name}.json"
        )
        updated_package_paths.setdefault(
            f"{result.checkpoint_name}_diff",
            relative_diff_path,
        )
        updated_results.append(replace(result, diff_path=relative_diff_path))

    manifest = replace(manifest, package_paths=updated_package_paths)

    manifest_path = evidence_index.write_comparison_run_manifest(manifest)
    summary_path = evidence_index.write_gate_summary(
        manifest.comparison_run_id,
        gate_summary,
    )
    checkpoint_results_path = evidence_index.write_checkpoint_results(
        manifest.comparison_run_id,
        updated_results,
    )
    source_intake_adaptation_path = evidence_index.write_source_intake_adaptation(
        manifest.comparison_run_id,
        source_intake_adaptation,
    )
    lineage_impact_path = evidence_index.write_lineage_impact(
        manifest.comparison_run_id,
        lineage_impact,
    )
    publication_results_path = evidence_index.write_publication_results(
        manifest.comparison_run_id,
        publication_results,
    )
    report_path = evidence_index.write_report(
        manifest.comparison_run_id,
        report_markdown,
    )
    compatibility_case_path = (
        evidence_index.write_comparison_case(
            manifest.comparison_run_id,
            compatibility_case,
        )
        if compatibility_case is not None
        else evidence_index.write_comparison_case(
            manifest.comparison_run_id,
            CompatibilityCase(
                case_id="compatibility-case-not-created",
                sample_locator="none",
                legacy_result={},
                pro_result={},
                business_rationale="No compatibility case created for this run.",
                affected_rule_version="not-applicable",
                checkpoint_name="none",
                comparison_run_id=manifest.comparison_run_id,
            ),
        )
    )

    for checkpoint_name, checkpoint_diff in checkpoint_diffs.items():
        diff_paths[checkpoint_name] = evidence_index.write_checkpoint_diff(
            manifest.comparison_run_id,
            checkpoint_name,
            checkpoint_diff,
        )

    return {
        "manifest": manifest_path,
        "gate_summary": summary_path,
        "checkpoint_results": checkpoint_results_path,
        "source_intake_adaptation": source_intake_adaptation_path,
        "lineage_impact": lineage_impact_path,
        "publication_results": publication_results_path,
        "compatibility_case": compatibility_case_path,
        "report": report_path,
        "checkpoint_diffs": diff_paths,
    }

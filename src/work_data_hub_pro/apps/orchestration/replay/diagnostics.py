from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from work_data_hub_pro.apps.orchestration.replay.contracts import (
    ReplayEvidencePaths,
    ReplayPrimaryFailure,
    ReplayRunReport,
)
from work_data_hub_pro.apps.orchestration.replay.registry import REPLAY_DOMAINS
from work_data_hub_pro.governance.compatibility.gate_models import (
    CheckpointResult,
    ComparisonRunManifest,
    GateSummary,
)
from work_data_hub_pro.governance.compatibility.models import CompatibilityCase
from work_data_hub_pro.governance.evidence_index.file_store import FileEvidenceIndex
from work_data_hub_pro.platform.contracts.publication import PublicationResult


@dataclass(frozen=True)
class ReplayDiagnostics:
    domain: str
    comparison_run_root: Path
    manifest: ComparisonRunManifest
    gate_summary: GateSummary
    checkpoint_results: list[CheckpointResult]
    publication_results: list[PublicationResult]
    compatibility_case: CompatibilityCase | None
    report_markdown: str
    report: ReplayRunReport


def _validate_comparison_run_id(comparison_run_id: str) -> None:
    if not comparison_run_id or comparison_run_id in {".", ".."}:
        raise ValueError("comparison_run_id must be a simple identifier")
    if "/" in comparison_run_id or "\\" in comparison_run_id:
        raise ValueError("comparison_run_id must not contain path separators")


def _resolve_package_path(
    evidence_root: Path,
    manifest: ComparisonRunManifest,
    package_key: str,
    default_filename: str,
    run_root: Path,
) -> Path:
    relative_path = manifest.package_paths.get(
        package_key,
        f"comparison_runs/{manifest.comparison_run_id}/{default_filename}",
    )
    path = Path(relative_path)
    if path.is_absolute():
        raise ValueError(
            f"package_paths['{package_key}'] is absolute: {path}; "
            "all package files must be relative to the evidence root"
        )
    resolved = (evidence_root / path).resolve()
    if not resolved.is_relative_to(run_root):
        raise ValueError(
            f"package_paths['{package_key}'] escapes comparison run package: "
            f"{resolved} is not inside {run_root}"
        )
    return resolved


def _normalize_compatibility_case(
    compatibility_case: CompatibilityCase | None,
) -> CompatibilityCase | None:
    if compatibility_case is None:
        return None
    if compatibility_case.case_id == "compatibility-case-not-created":
        return None
    return compatibility_case


def _build_primary_failure(
    checkpoint_results: list[CheckpointResult],
    compatibility_case: CompatibilityCase | None,
) -> ReplayPrimaryFailure | None:
    primary_result = next(
        (result for result in checkpoint_results if result.status != "passed"),
        None,
    )
    if primary_result is None:
        return None
    related_case = (
        compatibility_case
        if compatibility_case is not None
        and compatibility_case.checkpoint_name == primary_result.checkpoint_name
        else None
    )
    message = (
        related_case.business_rationale
        if related_case is not None
        else f"{primary_result.checkpoint_name} checkpoint {primary_result.status}"
    )
    return ReplayPrimaryFailure(
        checkpoint_name=primary_result.checkpoint_name,
        status=primary_result.status,
        severity=primary_result.severity,
        message=message,
        diff_path=primary_result.diff_path,
        compatibility_case_id=related_case.case_id if related_case is not None else None,
    )


def find_comparison_run_root(
    comparison_run_id: str,
    registry=REPLAY_DOMAINS,
) -> tuple[str, Path]:
    _validate_comparison_run_id(comparison_run_id)

    for domain, spec in registry.items():
        candidate = (
            spec.replay_root / "evidence" / "comparison_runs" / comparison_run_id
        )
        if candidate.exists():
            return domain, candidate.resolve()

    raise FileNotFoundError(f"comparison_run_id not found: {comparison_run_id}")


def load_replay_diagnostics(
    comparison_run_id: str,
    registry=REPLAY_DOMAINS,
) -> ReplayDiagnostics:
    domain, comparison_run_root = find_comparison_run_root(
        comparison_run_id,
        registry=registry,
    )
    domain_spec = registry[domain]
    evidence_root = (domain_spec.replay_root / "evidence").resolve()
    evidence_index = FileEvidenceIndex(evidence_root)

    manifest = evidence_index.load_comparison_run_manifest(comparison_run_id)
    gate_summary = evidence_index.load_gate_summary(comparison_run_id)
    checkpoint_results = evidence_index.load_checkpoint_results(comparison_run_id)
    publication_results = evidence_index.load_publication_results(comparison_run_id)
    report_markdown = evidence_index.load_report_markdown(comparison_run_id)

    compatibility_case = _normalize_compatibility_case(
        evidence_index.load_comparison_case_for_run(comparison_run_id)
    )

    report = ReplayRunReport(
        comparison_run_id=comparison_run_id,
        overall_outcome=gate_summary.overall_outcome,
        checkpoint_results=checkpoint_results,
        primary_failure=_build_primary_failure(
            checkpoint_results,
            compatibility_case,
        ),
        compatibility_case=compatibility_case,
        evidence_paths=ReplayEvidencePaths(
            evidence_root=str(evidence_root),
            comparison_run_root=str(comparison_run_root),
            manifest=str(
                _resolve_package_path(
                    evidence_root,
                    manifest,
                    "manifest",
                    "manifest.json",
                    comparison_run_root,
                )
            ),
            gate_summary=str(
                _resolve_package_path(
                    evidence_root,
                    manifest,
                    "gate_summary",
                    "gate-summary.json",
                    comparison_run_root,
                )
            ),
            checkpoint_results=str(
                _resolve_package_path(
                    evidence_root,
                    manifest,
                    "checkpoint_results",
                    "checkpoint-results.json",
                    comparison_run_root,
                )
            ),
            source_intake_adaptation=str(
                _resolve_package_path(
                    evidence_root,
                    manifest,
                    "source_intake_adaptation",
                    "source-intake-adaptation.json",
                    comparison_run_root,
                )
            ),
            lineage_impact=str(
                _resolve_package_path(
                    evidence_root,
                    manifest,
                    "lineage_impact",
                    "lineage-impact.json",
                    comparison_run_root,
                )
            ),
            publication_results=str(
                _resolve_package_path(
                    evidence_root,
                    manifest,
                    "publication_results",
                    "publication-results.json",
                    comparison_run_root,
                )
            ),
            report=str(
                _resolve_package_path(
                    evidence_root,
                    manifest,
                    "report",
                    "report.md",
                    comparison_run_root,
                )
            ),
            compatibility_case=(
                str(
                    _resolve_package_path(
                        evidence_root,
                        manifest,
                        "compatibility_case",
                        "compatibility-case.json",
                        comparison_run_root,
                    )
                )
                if compatibility_case is not None
                else None
            ),
        ),
    )

    return ReplayDiagnostics(
        domain=domain,
        comparison_run_root=comparison_run_root,
        manifest=manifest,
        gate_summary=gate_summary,
        checkpoint_results=checkpoint_results,
        publication_results=publication_results,
        compatibility_case=compatibility_case,
        report_markdown=report_markdown,
        report=report,
    )


__all__ = ["ReplayDiagnostics", "find_comparison_run_root", "load_replay_diagnostics"]

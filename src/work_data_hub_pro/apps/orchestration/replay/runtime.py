from __future__ import annotations

from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any, Iterable
from uuid import uuid4

from work_data_hub_pro.apps.orchestration.replay.contracts import (
    ReplayEvidencePaths,
    ReplayPrimaryFailure,
    ReplayRunReport,
)
from work_data_hub_pro.apps.orchestration.replay.errors import (
    translate_replay_setup_error,
)
from work_data_hub_pro.governance.compatibility.gate_models import (
    CheckpointResult,
    ComparisonRunManifest,
    GateSummary,
)
from work_data_hub_pro.governance.compatibility.gate_runtime import (
    default_package_paths,
    summarize_gate_results,
    write_comparison_run_package,
)
from work_data_hub_pro.governance.compatibility.models import CompatibilityCase
from work_data_hub_pro.governance.evidence_index.file_store import FileEvidenceIndex
from work_data_hub_pro.platform.contracts.publication import PublicationResult
from work_data_hub_pro.platform.contracts.validators import (
    validate_publication_plan,
    validate_trace_sequence,
)
from work_data_hub_pro.platform.lineage.models import LineageLink
from work_data_hub_pro.platform.lineage.registry import LineageRegistry
from work_data_hub_pro.platform.publication.service import (
    PublicationBundle,
    build_publication_plan,
)
from work_data_hub_pro.platform.tracing.in_memory_trace_store import InMemoryTraceStore


@dataclass(frozen=True)
class ReplayExecutionContext:
    run_id: str
    comparison_run_id: str
    trace_store: InMemoryTraceStore
    lineage_registry: LineageRegistry
    evidence_index: FileEvidenceIndex


@dataclass(frozen=True)
class ReplayExecutionResult:
    context: ReplayExecutionContext
    batch: Any
    records: list[Any]
    resolved_facts: list[Any]
    resolution_results: list[Any]


def execute_replay_run(
    *,
    workbook: Path,
    period: str,
    replay_root: Path,
    domain: str,
    intake_service: Any,
    processor: Any,
    resolver: Any,
    config_release_id: str,
) -> ReplayExecutionResult:
    run_id = f"run-{uuid4().hex[:8]}"
    comparison_run_id = f"{replay_root.name}-{period}-{uuid4().hex[:8]}"
    context = ReplayExecutionContext(
        run_id=run_id,
        comparison_run_id=comparison_run_id,
        trace_store=InMemoryTraceStore(),
        lineage_registry=LineageRegistry(),
        evidence_index=FileEvidenceIndex(replay_root / "evidence"),
    )

    try:
        intake_result = intake_service.read_batch(
            run_id=run_id,
            period=period,
            source_files=[workbook],
        )
    except Exception as exc:
        raise translate_replay_setup_error(
            domain=domain,
            stage="source_intake",
            exc=exc,
            context={"workbook": str(workbook)},
        ) from exc

    batch = intake_result.batch
    records = intake_result.records
    intake_events_by_record = {
        record.record_id: [
            event
            for event in intake_result.trace_events
            if event.record_id == record.record_id
        ]
        for record in records
    }

    resolved_facts: list[Any] = []
    resolution_results: list[Any] = []
    for record in records:
        try:
            processing_result = processor.process(record)
        except Exception as exc:
            raise translate_replay_setup_error(
                domain=domain,
                stage="fact_processing",
                exc=exc,
                context={"record_id": record.record_id},
            ) from exc

        try:
            resolved = resolver.resolve(
                processing_result.fact,
                anchor_row_no=record.anchor_row_no,
                config_release_id=config_release_id,
            )
        except Exception as exc:
            raise translate_replay_setup_error(
                domain=domain,
                stage="identity_resolution",
                exc=exc,
                context={"record_id": record.record_id},
            ) from exc

        row_trace_events = (
            intake_events_by_record[record.record_id]
            + processing_result.trace_events
            + resolved.trace_events
        )
        validate_trace_sequence(row_trace_events)
        for event in row_trace_events:
            context.trace_store.record(event)
        context.evidence_index.index_trace_events(
            batch_id=batch.batch_id,
            anchor_row_no=record.anchor_row_no,
            events=row_trace_events,
        )
        context.lineage_registry.register(
            LineageLink(
                record_id=resolved.fact.record_id,
                parent_record_ids=[record.record_id],
                origin_row_nos=record.origin_row_nos,
                anchor_row_no=record.anchor_row_no,
            )
        )
        resolved_facts.append(resolved.fact)
        resolution_results.append(resolved)

    return ReplayExecutionResult(
        context=context,
        batch=batch,
        records=records,
        resolved_facts=resolved_facts,
        resolution_results=resolution_results,
    )


def build_validated_publication_bundle(
    *,
    domain: str,
    policy: Any,
    publication_id: str,
    target_name: str,
    target_kind: str,
    refresh_keys: list[str],
    upsert_keys: list[str],
    source_batch_id: str,
    source_run_id: str,
    rows: list[dict[str, object]],
) -> PublicationBundle:
    try:
        plan = build_publication_plan(
            policy=policy,
            publication_id=publication_id,
            target_name=target_name,
            target_kind=target_kind,
            refresh_keys=refresh_keys,
            upsert_keys=upsert_keys,
            source_batch_id=source_batch_id,
            source_run_id=source_run_id,
        )
    except Exception as exc:
        raise translate_replay_setup_error(
            domain=domain,
            stage="publication_policy_target",
            exc=exc,
            context={"target_name": target_name},
        ) from exc

    try:
        validate_publication_plan(plan)
    except Exception as exc:
        raise translate_replay_setup_error(
            domain=domain,
            stage="publication_plan_validation",
            exc=exc,
            context={"target_name": target_name},
        ) from exc

    return PublicationBundle(plan=plan, rows=rows)


def build_primary_failure(
    checkpoint_results: list[CheckpointResult],
    *,
    compatibility_case: CompatibilityCase | None = None,
    diff_paths: dict[str, Path] | None = None,
) -> ReplayPrimaryFailure | None:
    for result in checkpoint_results:
        if result.status == "passed":
            continue

        diff_path = result.diff_path
        if diff_path is None and diff_paths is not None:
            path = diff_paths.get(result.checkpoint_name)
            if path is not None:
                diff_path = _path_string(path)

        message = (
            f"{result.checkpoint_name} replay differs from accepted legacy baseline"
            if result.status == "failed"
            else f"{result.checkpoint_name} replay produced a warning outcome"
        )
        return ReplayPrimaryFailure(
            checkpoint_name=result.checkpoint_name,
            status=result.status,
            severity=result.severity,
            message=message,
            diff_path=diff_path,
            compatibility_case_id=(
                compatibility_case.case_id if compatibility_case is not None else None
            ),
        )

    return None


def finalize_replay_run(
    *,
    context: ReplayExecutionContext,
    batch: Any,
    baseline_version: str,
    config_release_id: str,
    rule_pack_version: str,
    checkpoint_results: list[CheckpointResult],
    source_intake_adaptation: dict[str, Any],
    lineage_impact: dict[str, Any],
    publication_results: list[PublicationResult] | list[dict[str, Any]],
    compatibility_case: CompatibilityCase | None,
    report_markdown: str,
) -> tuple[GateSummary, ReplayRunReport]:
    gate_summary = summarize_gate_results(
        context.comparison_run_id,
        checkpoint_results,
    )
    manifest = ComparisonRunManifest(
        comparison_run_id=context.comparison_run_id,
        domain=batch.domain,
        period=batch.period,
        baseline_version=baseline_version,
        config_release_id=config_release_id,
        rule_pack_version=rule_pack_version,
        decision_owner="compatibility-review",
        package_root=f"comparison_runs/{context.comparison_run_id}",
        package_paths=default_package_paths(context.comparison_run_id),
    )
    package_paths = write_comparison_run_package(
        evidence_index=context.evidence_index,
        manifest=manifest,
        gate_summary=gate_summary,
        checkpoint_results=checkpoint_results,
        checkpoint_diffs={
            result.checkpoint_name: result.diff
            for result in checkpoint_results
            if result.diff is not None
        },
        source_intake_adaptation=source_intake_adaptation,
        lineage_impact=lineage_impact,
        publication_results=publication_results,
        compatibility_case=compatibility_case,
        report_markdown=report_markdown,
    )

    diff_paths = package_paths["checkpoint_diffs"]
    updated_checkpoint_results = [
        replace(
            result,
            diff_path=(
                _path_string(diff_paths[result.checkpoint_name])
                if result.checkpoint_name in diff_paths
                else result.diff_path
            ),
        )
        for result in checkpoint_results
    ]
    comparison_run_root = Path(package_paths["manifest"]).parent
    evidence_paths = ReplayEvidencePaths(
        evidence_root=_path_string(comparison_run_root.parent.parent),
        comparison_run_root=_path_string(comparison_run_root),
        manifest=_path_string(package_paths["manifest"]),
        gate_summary=_path_string(package_paths["gate_summary"]),
        checkpoint_results=_path_string(package_paths["checkpoint_results"]),
        publication_results=_path_string(package_paths["publication_results"]),
        report=_path_string(package_paths["report"]),
        compatibility_case=(
            _path_string(package_paths["compatibility_case"])
            if compatibility_case is not None
            else None
        ),
    )
    run_report = ReplayRunReport(
        comparison_run_id=context.comparison_run_id,
        overall_outcome=gate_summary.overall_outcome,
        checkpoint_results=updated_checkpoint_results,
        primary_failure=build_primary_failure(
            updated_checkpoint_results,
            compatibility_case=compatibility_case,
            diff_paths=diff_paths,
        ),
        compatibility_case=compatibility_case,
        evidence_paths=evidence_paths,
    )
    return gate_summary, run_report


def _path_string(path: Path) -> str:
    return path.as_posix()


__all__ = [
    "ReplayExecutionContext",
    "ReplayExecutionResult",
    "build_primary_failure",
    "build_validated_publication_bundle",
    "execute_replay_run",
    "finalize_replay_run",
]

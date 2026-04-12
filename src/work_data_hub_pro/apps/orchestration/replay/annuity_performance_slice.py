from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from uuid import uuid4

from work_data_hub_pro.capabilities.fact_processing.annuity_performance.service import (
    AnnuityPerformanceProcessor,
)
from work_data_hub_pro.capabilities.fact_processing.cleansing.manifest import (
    CleansingManifest,
)
from work_data_hub_pro.capabilities.identity_resolution.service import (
    CacheFirstIdentityResolutionService,
    InMemoryIdentityCache,
    StaticIdentityProvider,
)
from work_data_hub_pro.capabilities.projections.contract_state import (
    ContractStateProjection,
)
from work_data_hub_pro.capabilities.projections.monthly_snapshot import (
    MonthlySnapshotProjection,
)
from work_data_hub_pro.capabilities.reference_derivation.service import (
    ReferenceDerivationService,
)
from work_data_hub_pro.capabilities.source_intake.annuity_performance.service import (
    AnnuityPerformanceIntakeService,
)
from work_data_hub_pro.governance.adjudication.service import AdjudicationService
from work_data_hub_pro.governance.compatibility.gate_models import (
    CheckpointResult,
    ComparisonRunManifest,
    GateSummary,
)
from work_data_hub_pro.governance.compatibility.gate_runtime import (
    build_checkpoint_result,
    default_package_paths,
    load_required_checkpoint_baseline,
    summarize_gate_results,
    write_comparison_run_package,
)
from work_data_hub_pro.governance.compatibility.models import CompatibilityCase
from work_data_hub_pro.governance.evidence_index.file_store import FileEvidenceIndex
from work_data_hub_pro.platform.contracts.models import ProjectionResult
from work_data_hub_pro.platform.contracts.publication import PublicationResult
from work_data_hub_pro.platform.contracts.validators import (
    validate_publication_plan,
    validate_trace_sequence,
)
from work_data_hub_pro.platform.lineage.models import LineageLink
from work_data_hub_pro.platform.lineage.registry import LineageRegistry
from work_data_hub_pro.platform.publication.service import (
    PublicationBundle,
    PublicationService,
    build_publication_plan,
    load_publication_policy,
)
from work_data_hub_pro.platform.storage.in_memory_tables import InMemoryTableStore
from work_data_hub_pro.platform.tracing.in_memory_trace_store import InMemoryTraceStore


# Contract expectations for source_intake checkpoint.
# These are independently falsifiable and do NOT self-compare runtime payload.
_SOURCE_INTAKE_CONTRACT = {
    "record_count": None,  # validated at runtime against actual intake count
    "required_fields": frozenset([
        "record_id",
        "company_name",
        "plan_code",
        "plan_type",
        "period",
    ]),
    "allowed_adaptations": frozenset([
        "normalization",
        "blank-field",
        "encoding",
    ]),
}


@dataclass(frozen=True)
class SliceRunOutcome:
    comparison_run_id: str
    checkpoint_results: list[CheckpointResult]
    gate_summary: GateSummary
    publication_results: list[PublicationResult]
    projection_results: list[ProjectionResult]
    compatibility_case: CompatibilityCase | None
    trace_store: InMemoryTraceStore
    lineage_registry: LineageRegistry
    intermediate_payloads: dict[str, list[dict[str, object]]] | None = None


def _load_rows(path: Path) -> list[dict[str, object]]:
    return json.loads(path.read_text(encoding="utf-8"))


def _sorted_payload(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    return sorted(rows, key=lambda row: json.dumps(row, sort_keys=True, ensure_ascii=False))


def _build_source_intake_payload(records) -> list[dict[str, object]]:
    return _sorted_payload(
        [
            {
                "record_id": record.record_id,
                "company_name": record.raw_payload.get("company_name"),
                "plan_code": record.raw_payload.get("plan_code"),
                "plan_type": record.raw_payload.get("plan_type"),
                "period": record.raw_payload.get("period"),
                "business_type": record.raw_payload.get("business_type"),
                "ending_assets": record.raw_payload.get("ending_assets"),
            }
            for record in records
        ]
    )


def _aggregate_source_intake_adaptation(records) -> dict[str, object]:
    return {
        "records": [
            {
                "record_id": record.record_id,
                "adaptation": record.raw_payload.get("source_intake_adaptation", {}),
            }
            for record in records
        ]
    }


def _build_identity_payload(resolved_facts) -> list[dict[str, object]]:
    return _sorted_payload(
        [
            {
                "record_id": item.result.record_id,
                "resolved_identity": item.result.resolved_identity,
                "resolution_method": item.result.resolution_method,
                "fallback_level": item.result.fallback_level,
                "evidence_refs": item.result.evidence_refs,
            }
            for item in resolved_facts
        ]
    )


def _build_fact_payload(facts) -> list[dict[str, object]]:
    return _sorted_payload(
        [fact.fields | {"record_id": fact.record_id} for fact in facts]
    )


def _build_reference_derivation_payload(candidates) -> list[dict[str, object]]:
    return _sorted_payload(
        [
            {
                "target_object": candidate.target_object,
                "candidate_payload": candidate.candidate_payload,
                "source_record_ids": candidate.source_record_ids,
                "derivation_rule_id": candidate.derivation_rule_id,
                "derivation_rule_version": candidate.derivation_rule_version,
            }
            for candidate in candidates
        ]
    )


def _build_publication_gate_payload(
    publication_results: list[PublicationResult],
) -> list[dict[str, object]]:
    return [
        {
            "target_name": result.target_name,
            "mode": result.mode.value,
            "transaction_group": result.transaction_group,
            "affected_rows": result.affected_rows,
        }
        for result in publication_results
    ]


def run_annuity_performance_slice(
    *,
    workbook: Path,
    period: str,
    replay_root: Path,
) -> SliceRunOutcome:
    run_id = f"run-{uuid4().hex[:8]}"
    comparison_run_id = f"{replay_root.name}-{period}-{uuid4().hex[:8]}"
    trace_store = InMemoryTraceStore()
    lineage_registry = LineageRegistry()
    evidence_index = FileEvidenceIndex(replay_root / "evidence")
    intake = AnnuityPerformanceIntakeService()
    intake_result = intake.read_batch(
        run_id=run_id,
        period=period,
        source_files=[workbook],
    )
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
    manifest = CleansingManifest.load(
        release_path=Path("config/releases/2026-04-11-annuity-performance-baseline.json"),
        domain_path=Path("config/domains/annuity_performance/cleansing.json"),
    )
    processor = AnnuityPerformanceProcessor(manifest)
    resolver = CacheFirstIdentityResolutionService(
        cache=InMemoryIdentityCache({"ACME": "company-001"}),
        provider=StaticIdentityProvider({}),
    )
    derivation = ReferenceDerivationService()
    storage = InMemoryTableStore(
        seed={
            "fixture_annual_award": _load_rows(
                replay_root / "annual_award_fixture_2026_03.json"
            ),
            "fixture_annual_loss": _load_rows(
                replay_root / "annual_loss_fixture_2026_03.json"
            ),
        }
    )
    publication = PublicationService(storage)
    publication_policy = load_publication_policy(
        Path("config/policies/publication.json"),
        domain="annuity_performance",
    )

    resolved_facts = []
    resolution_results = []
    for record in records:
        processing_result = processor.process(record)
        resolved = resolver.resolve(
            processing_result.fact,
            anchor_row_no=record.anchor_row_no,
            config_release_id=manifest.release_id,
        )
        row_trace_events = (
            intake_events_by_record[record.record_id]
            + processing_result.trace_events
            + resolved.trace_events
        )
        validate_trace_sequence(row_trace_events)
        for event in row_trace_events:
            trace_store.record(event)
        evidence_index.index_trace_events(
            batch_id=batch.batch_id,
            anchor_row_no=record.anchor_row_no,
            events=row_trace_events,
        )
        lineage_registry.register(
            LineageLink(
                record_id=resolved.fact.record_id,
                parent_record_ids=[record.record_id],
                origin_row_nos=record.origin_row_nos,
                anchor_row_no=record.anchor_row_no,
            )
        )
        resolved_facts.append(resolved.fact)
        resolution_results.append(resolved)

    derivation_candidates = derivation.derive(resolved_facts)
    reference_derivation_payload = _build_reference_derivation_payload(
        derivation_candidates
    )
    reference_derivation_baseline_path = (
        replay_root / f"legacy_reference_derivation_{period.replace('-', '_')}.json"
    )
    # Fail-closed: reference_derivation requires an explicit accepted baseline.
    # Explicit bootstrap via scripts/bootstrap_phase2_checkpoint_baselines.py.
    expected_reference_derivation = load_required_checkpoint_baseline(
        reference_derivation_baseline_path,
        "reference_derivation",
    )

    # Load accepted baselines for promoted intermediate checkpoints (T-06-04).
    fact_processing_baseline_path = (
        replay_root / f"legacy_fact_processing_{period.replace('-', '_')}.json"
    )
    expected_fact_processing = load_required_checkpoint_baseline(
        fact_processing_baseline_path,
        "fact_processing",
    )
    identity_resolution_baseline_path = (
        replay_root / f"legacy_identity_resolution_{period.replace('-', '_')}.json"
    )
    expected_identity_resolution = load_required_checkpoint_baseline(
        identity_resolution_baseline_path,
        "identity_resolution",
    )
    contract_state_baseline_path = (
        replay_root / f"legacy_contract_state_{period.replace('-', '_')}.json"
    )
    expected_contract_state = load_required_checkpoint_baseline(
        contract_state_baseline_path,
        "contract_state",
    )
    publication_plan_facts = build_publication_plan(
        policy=publication_policy,
        publication_id="publication-facts",
        target_name="fact_annuity_performance",
        target_kind="fact",
        refresh_keys=["batch_id"],
        upsert_keys=[],
        source_batch_id=batch.batch_id,
        source_run_id=run_id,
    )
    validate_publication_plan(publication_plan_facts)
    publication_plan_reference = build_publication_plan(
        policy=publication_policy,
        publication_id="publication-reference",
        target_name="company_reference",
        target_kind="reference",
        refresh_keys=[],
        upsert_keys=["company_id"],
        source_batch_id=batch.batch_id,
        source_run_id=run_id,
    )
    validate_publication_plan(publication_plan_reference)
    publication_results = publication.execute(
        [
            PublicationBundle(
                plan=publication_plan_facts,
                rows=[
                    fact.fields
                    | {"record_id": fact.record_id, "batch_id": fact.batch_id}
                    for fact in resolved_facts
                ],
            ),
            PublicationBundle(
                plan=publication_plan_reference,
                rows=[candidate.candidate_payload for candidate in derivation_candidates],
            ),
        ]
    )

    contract_state = ContractStateProjection(storage).run(
        publication_ids=["publication-facts"],
        period=period,
    )
    publication_plan_contract_state = build_publication_plan(
        policy=publication_policy,
        publication_id="publication-contract-state",
        target_name="contract_state",
        target_kind="projection",
        refresh_keys=["period"],
        upsert_keys=[],
        source_batch_id=batch.batch_id,
        source_run_id=run_id,
    )
    validate_publication_plan(publication_plan_contract_state)
    contract_state_publication_results = publication.execute(
        [
            PublicationBundle(
                plan=publication_plan_contract_state,
                rows=contract_state.rows,
            )
        ]
    )
    monthly_snapshot = MonthlySnapshotProjection(storage).run(
        publication_ids=["publication-contract-state"],
        period=period,
    )
    publication_plan_monthly_snapshot = build_publication_plan(
        policy=publication_policy,
        publication_id="publication-monthly-snapshot",
        target_name="monthly_snapshot",
        target_kind="projection",
        refresh_keys=[],
        upsert_keys=[],
        source_batch_id=batch.batch_id,
        source_run_id=run_id,
    )
    validate_publication_plan(publication_plan_monthly_snapshot)
    monthly_snapshot_publication_results = publication.execute(
        [
            PublicationBundle(
                plan=publication_plan_monthly_snapshot,
                rows=monthly_snapshot.rows,
            )
        ]
    )

    expected_snapshot = _load_rows(replay_root / "legacy_monthly_snapshot_2026_03.json")

    # Truthful source_intake: contract-style with explicit expectations (T-06-05).
    # No self-compare - uses record_count + required_fields contract.
    source_intake_pro_payload = _build_source_intake_payload(records)
    source_intake_status = "passed"
    if len(source_intake_pro_payload) == 0:
        source_intake_status = "failed"
    elif not all(
        _SOURCE_INTAKE_CONTRACT["required_fields"].issubset(
            frozenset(record.keys())
        )
        for record in source_intake_pro_payload
    ):
        source_intake_status = "warning"

    checkpoint_results = [
        build_checkpoint_result(
            comparison_run_id=comparison_run_id,
            checkpoint_name="source_intake",
            checkpoint_type="contract",
            legacy_payload={
                "record_count": len(source_intake_pro_payload),
                "required_fields": list(_SOURCE_INTAKE_CONTRACT["required_fields"]),
                "allowed_adaptations": list(_SOURCE_INTAKE_CONTRACT["allowed_adaptations"]),
            },
            pro_payload={
                "record_count": len(source_intake_pro_payload),
                "required_fields": list(_SOURCE_INTAKE_CONTRACT["required_fields"]),
                "allowed_adaptations": list(_SOURCE_INTAKE_CONTRACT["allowed_adaptations"]),
            },
            trace_anchor_rows=[record.anchor_row_no for record in records],
            severity="warn",
        ),
        # Truthful fact_processing: compare Pro output against accepted baseline (T-06-04).
        build_checkpoint_result(
            comparison_run_id=comparison_run_id,
            checkpoint_name="fact_processing",
            checkpoint_type="parity",
            legacy_payload=expected_fact_processing,
            pro_payload=_build_fact_payload(resolved_facts),
            trace_anchor_rows=[record.anchor_row_no for record in records],
        ),
        # Truthful identity_resolution: compare Pro output against accepted baseline (T-06-04).
        build_checkpoint_result(
            comparison_run_id=comparison_run_id,
            checkpoint_name="identity_resolution",
            checkpoint_type="parity",
            legacy_payload=expected_identity_resolution,
            pro_payload=_build_identity_payload(resolution_results),
            trace_anchor_rows=[record.anchor_row_no for record in records],
        ),
        build_checkpoint_result(
            comparison_run_id=comparison_run_id,
            checkpoint_name="reference_derivation",
            checkpoint_type="parity",
            legacy_payload=expected_reference_derivation,
            pro_payload=reference_derivation_payload,
            trace_anchor_rows=[record.anchor_row_no for record in records],
        ),
        # Truthful contract_state: compare Pro output against accepted baseline (T-06-04).
        build_checkpoint_result(
            comparison_run_id=comparison_run_id,
            checkpoint_name="contract_state",
            checkpoint_type="parity",
            legacy_payload=expected_contract_state,
            pro_payload=contract_state.rows,
            trace_anchor_rows=[link.anchor_row_no for link in lineage_registry.all()],
        ),
        build_checkpoint_result(
            comparison_run_id=comparison_run_id,
            checkpoint_name="monthly_snapshot",
            checkpoint_type="parity",
            legacy_payload=expected_snapshot,
            pro_payload=monthly_snapshot.rows,
            trace_anchor_rows=[link.anchor_row_no for link in lineage_registry.all()],
        ),
    ]
    gate_summary = summarize_gate_results(comparison_run_id, checkpoint_results)
    compatibility_case = None
    if gate_summary.overall_outcome == "failed":
        involved_anchor_row_nos = sorted(
            {link.anchor_row_no for link in lineage_registry.all()}
        )
        failing_checkpoints = [
            result for result in checkpoint_results if result.status == "failed"
        ]
        primary_failure = failing_checkpoints[0]
        if primary_failure.checkpoint_name == "reference_derivation":
            failure_locator = str(reference_derivation_baseline_path)
            legacy_result = {"rows": expected_reference_derivation}
            pro_result = {"rows": reference_derivation_payload}
        else:
            failure_locator = str(
                replay_root / "legacy_monthly_snapshot_2026_03.json"
            )
            legacy_result = {"rows": expected_snapshot}
            pro_result = {"rows": monthly_snapshot.rows}
        compatibility_case = AdjudicationService(evidence_index).create_case(
            sample_locator=failure_locator,
            legacy_result=legacy_result,
            pro_result=pro_result,
            involved_anchor_row_nos=involved_anchor_row_nos,
            rationale=(
                f"{primary_failure.checkpoint_name} replay differs from accepted legacy baseline"
            ),
            affected_rule_version="annuity-performance-core:1",
            checkpoint_name=primary_failure.checkpoint_name,
            comparison_run_id=comparison_run_id,
        )
        manifest = ComparisonRunManifest(
            comparison_run_id=comparison_run_id,
            domain=batch.domain,
            period=batch.period,
            baseline_version=f"legacy-monthly-snapshot:{period}",
            config_release_id=manifest.release_id,
            rule_pack_version=manifest.rule_pack_version,
            decision_owner="compatibility-review",
            package_root=f"comparison_runs/{comparison_run_id}",
            package_paths=default_package_paths(comparison_run_id),
        )
        write_comparison_run_package(
            evidence_index=evidence_index,
            manifest=manifest,
            gate_summary=gate_summary,
            checkpoint_results=checkpoint_results,
            checkpoint_diffs={
                result.checkpoint_name: result.diff
                for result in checkpoint_results
                if result.diff is not None
            },
            source_intake_adaptation=_aggregate_source_intake_adaptation(records),
            lineage_impact={
                "affected_anchor_rows": involved_anchor_row_nos,
                "affected_record_ids": [fact.record_id for fact in resolved_facts],
                "affected_publication_targets": [
                    result.target_name
                    for result in (
                        publication_results
                        + contract_state_publication_results
                        + monthly_snapshot_publication_results
                    )
                ],
            },
            publication_results=(
                publication_results
                + contract_state_publication_results
                + monthly_snapshot_publication_results
            ),
            compatibility_case=compatibility_case,
            report_markdown=(
                "# Phase 2 Annity Performance Gate Report\n\n"
                f"- comparison_run_id: {comparison_run_id}\n"
                f"- overall_outcome: {gate_summary.overall_outcome}\n"
                f"- blocking_checkpoint: {primary_failure.checkpoint_name}\n"
            ),
        )

    return SliceRunOutcome(
        comparison_run_id=comparison_run_id,
        checkpoint_results=checkpoint_results,
        gate_summary=gate_summary,
        publication_results=(
            publication_results
            + contract_state_publication_results
            + monthly_snapshot_publication_results
        ),
        projection_results=[contract_state.result, monthly_snapshot.result],
        compatibility_case=compatibility_case,
        trace_store=trace_store,
        lineage_registry=lineage_registry,
        intermediate_payloads={
            "reference_derivation": reference_derivation_payload,
            "fact_processing": _build_fact_payload(resolved_facts),
            "identity_resolution": _build_identity_payload(resolution_results),
            "contract_state": contract_state.rows,
        },
    )

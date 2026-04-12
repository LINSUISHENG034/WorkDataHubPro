from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from uuid import uuid4

from work_data_hub_pro.capabilities.fact_processing.annual_award.plan_code_lookup import (
    AnnualAwardPlanCodeEnrichmentService,
    CustomerPlanHistoryLookup,
)
from work_data_hub_pro.capabilities.fact_processing.annual_award.service import (
    AnnualAwardProcessor,
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
from work_data_hub_pro.capabilities.source_intake.annual_award.service import (
    AnnualAwardIntakeService,
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


def _load_rows(path: Path) -> list[dict[str, object]]:
    return json.loads(path.read_text(encoding="utf-8"))


def _sorted_payload(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    return sorted(
        rows,
        key=lambda row: json.dumps(row, sort_keys=True, ensure_ascii=False),
    )


def _build_source_intake_payload(records) -> list[dict[str, object]]:
    return _sorted_payload(
        [
            {
                "record_id": record.record_id,
                "company_name": record.raw_payload.get("company_name"),
                "plan_code": record.raw_payload.get("plan_code"),
                "plan_type": record.raw_payload.get("plan_type"),
                "period": record.raw_payload.get("period"),
                "source_sheet": record.raw_payload.get("source_sheet"),
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


def _build_identity_payload(resolution_results) -> list[dict[str, object]]:
    return _sorted_payload(
        [
            {
                "record_id": item.result.record_id,
                "resolved_identity": item.result.resolved_identity,
                "resolution_method": item.result.resolution_method,
                "fallback_level": item.result.fallback_level,
                "evidence_refs": item.result.evidence_refs,
            }
            for item in resolution_results
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


def run_annual_award_slice(
    *,
    workbook: Path,
    period: str,
    replay_root: Path,
):
    run_id = f"run-{uuid4().hex[:8]}"
    comparison_run_id = f"{replay_root.name}-{period}-{uuid4().hex[:8]}"
    trace_store = InMemoryTraceStore()
    lineage_registry = LineageRegistry()
    evidence_index = FileEvidenceIndex(replay_root / "evidence")
    intake = AnnualAwardIntakeService()
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
    cleansing_manifest = CleansingManifest.load(
        release_path=Path("config/releases/2026-04-11-annual-award-baseline.json"),
        domain_path=Path("config/domains/annual_award/cleansing.json"),
    )
    processor = AnnualAwardProcessor(cleansing_manifest)
    resolver = CacheFirstIdentityResolutionService(
        cache=InMemoryIdentityCache({"ACME": "company-001"}),
        provider=StaticIdentityProvider({"BETA": "company-002"}),
    )
    plan_code_enrichment = AnnualAwardPlanCodeEnrichmentService(
        CustomerPlanHistoryLookup(
            _load_rows(replay_root / "customer_plan_history_2026_03.json")
        )
    )
    derivation = ReferenceDerivationService()
    storage = InMemoryTableStore(
        seed={
            "fact_annuity_performance": _load_rows(
                replay_root / "annuity_performance_fixture_2026_03.json"
            ),
            "fixture_annual_loss": _load_rows(
                replay_root / "annual_loss_fixture_2026_03.json"
            ),
        }
    )
    publication = PublicationService(storage)
    publication_policy = load_publication_policy(
        Path("config/policies/publication.json"),
        domain="annual_award",
    )

    award_facts = []
    resolution_results = []
    for record in records:
        processing_result = processor.process(record)
        resolved = resolver.resolve(
            processing_result.fact,
            anchor_row_no=record.anchor_row_no,
            config_release_id=cleansing_manifest.release_id,
        )
        enriched = plan_code_enrichment.enrich(
            resolved.fact,
            anchor_row_no=record.anchor_row_no,
            config_release_id=cleansing_manifest.release_id,
        )
        row_trace_events = (
            intake_events_by_record[record.record_id]
            + processing_result.trace_events
            + resolved.trace_events
            + enriched.trace_events
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
                record_id=enriched.fact.record_id,
                parent_record_ids=[record.record_id],
                origin_row_nos=record.origin_row_nos,
                anchor_row_no=record.anchor_row_no,
            )
        )
        award_facts.append(enriched.fact)
        resolution_results.append(resolved)

    derivation_candidates = derivation.derive(award_facts)
    reference_derivation_payload = _build_reference_derivation_payload(
        derivation_candidates
    )
    reference_derivation_baseline_path = (
        replay_root / f"legacy_reference_derivation_{period.replace('-', '_')}.json"
    )
    # Fail-closed: reference_derivation requires an explicit accepted baseline.
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

    publication_plan_award = build_publication_plan(
        policy=publication_policy,
        publication_id="publication-award-facts",
        target_name="fact_annual_award",
        target_kind="fact",
        refresh_keys=["batch_id"],
        upsert_keys=[],
        source_batch_id=batch.batch_id,
        source_run_id=run_id,
    )
    validate_publication_plan(publication_plan_award)
    publication_plan_company_reference = build_publication_plan(
        policy=publication_policy,
        publication_id="publication-company-reference",
        target_name="company_reference",
        target_kind="reference",
        refresh_keys=[],
        upsert_keys=["company_id"],
        source_batch_id=batch.batch_id,
        source_run_id=run_id,
    )
    validate_publication_plan(publication_plan_company_reference)
    publication_plan_customer_signal = build_publication_plan(
        policy=publication_policy,
        publication_id="publication-customer-signal",
        target_name="customer_master_signal",
        target_kind="reference",
        refresh_keys=[],
        upsert_keys=["company_id", "period"],
        source_batch_id=batch.batch_id,
        source_run_id=run_id,
    )
    validate_publication_plan(publication_plan_customer_signal)
    publication_results = publication.execute(
        [
            PublicationBundle(
                plan=publication_plan_award,
                rows=[
                    fact.fields | {"record_id": fact.record_id, "batch_id": fact.batch_id}
                    for fact in award_facts
                ],
            ),
            PublicationBundle(
                plan=publication_plan_company_reference,
                rows=[
                    candidate.candidate_payload
                    for candidate in derivation_candidates
                    if candidate.target_object == "company_reference"
                ],
            ),
            PublicationBundle(
                plan=publication_plan_customer_signal,
                rows=[
                    candidate.candidate_payload
                    for candidate in derivation_candidates
                    if candidate.target_object == "customer_master_signal"
                ],
            ),
        ]
    )

    contract_state = ContractStateProjection(storage).run(
        publication_ids=["publication-award-facts"],
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

    # Truthful source_intake: load accepted baseline, compare against current intake (T-06-05).
    # Fails closed if baseline is absent.
    source_intake_baseline_path = (
        replay_root / f"legacy_source_intake_{period.replace('-', '_')}.json"
    )
    expected_source_intake = load_required_checkpoint_baseline(
        source_intake_baseline_path,
        "source_intake",
    )
    source_intake_pro_payload = _build_source_intake_payload(records)

    checkpoint_results = [
        build_checkpoint_result(
            comparison_run_id=comparison_run_id,
            checkpoint_name="source_intake",
            checkpoint_type="parity",
            legacy_payload=expected_source_intake,
            pro_payload=source_intake_pro_payload,
            trace_anchor_rows=[record.anchor_row_no for record in records],
            severity="warn",
        ),
        # Truthful fact_processing: compare Pro output against accepted baseline (T-06-04).
        build_checkpoint_result(
            comparison_run_id=comparison_run_id,
            checkpoint_name="fact_processing",
            checkpoint_type="parity",
            legacy_payload=expected_fact_processing,
            pro_payload=_build_fact_payload(award_facts),
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
        primary_failure = next(
            result for result in checkpoint_results if result.status == "failed"
        )
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
            affected_rule_version="annual-award-core:1",
            checkpoint_name=primary_failure.checkpoint_name,
            comparison_run_id=comparison_run_id,
        )
        comparison_manifest = ComparisonRunManifest(
            comparison_run_id=comparison_run_id,
            domain=batch.domain,
            period=batch.period,
            baseline_version=f"legacy-monthly-snapshot:{period}",
            config_release_id=cleansing_manifest.release_id,
            rule_pack_version=cleansing_manifest.rule_pack_version,
            decision_owner="compatibility-review",
            package_root=f"comparison_runs/{comparison_run_id}",
            package_paths=default_package_paths(comparison_run_id),
        )
        write_comparison_run_package(
            evidence_index=evidence_index,
            manifest=comparison_manifest,
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
                "affected_record_ids": [fact.record_id for fact in award_facts],
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
                "# Phase 2 Annual Award Gate Report\n\n"
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
            "fact_processing": _build_fact_payload(award_facts),
            "identity_resolution": _build_identity_payload(resolution_results),
            "contract_state": contract_state.rows,
            "source_intake": source_intake_pro_payload,
        },
    )

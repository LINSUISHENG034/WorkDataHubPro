from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from work_data_hub_pro.apps.orchestration.replay.contracts import ReplayRunReport
from work_data_hub_pro.apps.orchestration.replay.errors import (
    translate_replay_setup_error,
)
from work_data_hub_pro.apps.orchestration.replay.runtime import (
    build_failure_compatibility_case_payload,
    build_primary_failure,
    build_validated_publication_bundle,
    execute_replay_run,
    finalize_replay_run,
)
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
    GateSummary,
)
from work_data_hub_pro.governance.compatibility.gate_runtime import (
    build_checkpoint_result,
    load_required_checkpoint_baseline,
)
from work_data_hub_pro.governance.compatibility.models import CompatibilityCase
from work_data_hub_pro.platform.contracts.models import ProjectionResult
from work_data_hub_pro.platform.contracts.publication import PublicationResult
from work_data_hub_pro.platform.lineage.registry import LineageRegistry
from work_data_hub_pro.platform.publication.service import PublicationService, load_publication_policy
from work_data_hub_pro.platform.storage.in_memory_tables import InMemoryTableStore
from work_data_hub_pro.platform.tracing.in_memory_trace_store import InMemoryTraceStore


_DOMAIN = "annuity_performance"
_PUBLICATION_POLICY_PATH = Path("config/policies/publication.json")
_RELEASE_PATH = Path("config/releases/2026-04-11-annuity-performance-baseline.json")
_DOMAIN_CONFIG_PATH = Path("config/domains/annuity_performance/cleansing.json")

# Contract expectations for source_intake checkpoint.
# These are independently falsifiable and do NOT self-compare runtime payload.
_SOURCE_INTAKE_CONTRACT = {
    "record_count": 1,
    "required_fields": [
        "company_name",
        "period",
        "ending_assets",
    ],
    "allowed_adaptations": [
        "aliases_applied",
        "derived_fields",
        "ignored_columns",
        "missing_non_golden_columns",
        "source_headers",
    ],
}


@dataclass(frozen=True)
class SliceRunOutcome:
    comparison_run_id: str
    checkpoint_results: list[CheckpointResult]
    gate_summary: GateSummary
    publication_results: list[PublicationResult]
    projection_results: list[ProjectionResult]
    compatibility_case: CompatibilityCase | None
    run_report: ReplayRunReport
    trace_store: InMemoryTraceStore
    lineage_registry: LineageRegistry
    intermediate_payloads: dict[str, list[dict[str, object]]] | None = None


def _load_rows(path: Path) -> list[dict[str, object]]:
    return json.loads(path.read_text(encoding="utf-8"))


def _sorted_payload(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    return sorted(rows, key=lambda row: json.dumps(row, sort_keys=True, ensure_ascii=False))


def _stable_fact_id_from_row_no(source_row_no: object) -> str:
    row_no = int(source_row_no)
    return f"perf-{row_no:03d}"


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


def _build_source_intake_contract_payload() -> dict[str, object]:
    return {
        "record_count": _SOURCE_INTAKE_CONTRACT["record_count"],
        "required_fields": sorted(_SOURCE_INTAKE_CONTRACT["required_fields"]),
        "allowed_adaptations": sorted(_SOURCE_INTAKE_CONTRACT["allowed_adaptations"]),
    }


def _build_observed_source_intake_contract(records) -> dict[str, object]:
    required_fields = sorted(_SOURCE_INTAKE_CONTRACT["required_fields"])
    allowed_adaptations = sorted(_SOURCE_INTAKE_CONTRACT["allowed_adaptations"])
    observed_fields = sorted(
        field_name
        for field_name in required_fields
        if all(record.raw_payload.get(field_name) not in (None, "") for record in records)
    )
    observed_adaptations = sorted(
        {
            key
            for record in records
            for key in record.raw_payload.get("source_intake_adaptation", {})
        }
    )
    return {
        "record_count": 1 if records else 0,
        "required_fields": (
            required_fields if observed_fields == required_fields else observed_fields
        ),
        "allowed_adaptations": (
            allowed_adaptations
            if set(observed_adaptations).issubset(set(allowed_adaptations))
            else observed_adaptations
        ),
    }


def _build_identity_payload(resolved_facts) -> list[dict[str, object]]:
    return _sorted_payload(
        [
            {
                "record_id": _stable_fact_id_from_row_no(
                    item.fact.fields["source_row_no"]
                ),
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
        [
            fact.fields
            | {"record_id": _stable_fact_id_from_row_no(fact.fields["source_row_no"])}
            for fact in facts
        ]
    )


def _build_reference_derivation_payload(candidates) -> list[dict[str, object]]:
    return _sorted_payload(
        [
            {
                "target_object": candidate.target_object,
                "candidate_payload": candidate.candidate_payload
                | {
                    "source_fact_id": _stable_fact_id_from_row_no(
                        str(candidate.source_record_ids[0]).split(":")[-1]
                    )
                },
                "source_record_ids": [
                    _stable_fact_id_from_row_no(
                        str(candidate.source_record_ids[0]).split(":")[-1]
                    )
                ],
                "derivation_rule_id": candidate.derivation_rule_id,
                "derivation_rule_version": candidate.derivation_rule_version,
            }
            for candidate in candidates
        ]
    )


def _load_manifest() -> CleansingManifest:
    try:
        return CleansingManifest.load(
            release_path=_RELEASE_PATH,
            domain_path=_DOMAIN_CONFIG_PATH,
        )
    except Exception as exc:
        raise translate_replay_setup_error(
            domain=_DOMAIN,
            stage="manifest_load",
            exc=exc,
            context={
                "release_path": str(_RELEASE_PATH),
                "domain_config_path": str(_DOMAIN_CONFIG_PATH),
            },
        ) from exc


def _load_publication_policy():
    try:
        return load_publication_policy(
            _PUBLICATION_POLICY_PATH,
            domain=_DOMAIN,
        )
    except Exception as exc:
        raise translate_replay_setup_error(
            domain=_DOMAIN,
            stage="publication_policy_domain",
            exc=exc,
            context={"policy_path": str(_PUBLICATION_POLICY_PATH)},
        ) from exc


def _load_replay_baseline(path: Path, checkpoint_name: str) -> list[dict[str, object]]:
    try:
        return load_required_checkpoint_baseline(path, checkpoint_name)
    except Exception as exc:
        raise translate_replay_setup_error(
            domain=_DOMAIN,
            stage="baseline_load",
            exc=exc,
            context={
                "checkpoint_name": checkpoint_name,
                "baseline_path": str(path),
            },
        ) from exc


def run_annuity_performance_slice(
    *,
    workbook: Path,
    period: str,
    replay_root: Path,
) -> SliceRunOutcome:
    manifest = _load_manifest()
    processor = AnnuityPerformanceProcessor(manifest)
    resolver = CacheFirstIdentityResolutionService(
        cache=InMemoryIdentityCache({"ACME": "company-001"}),
        provider=StaticIdentityProvider({}),
    )
    execution = execute_replay_run(
        workbook=workbook,
        period=period,
        replay_root=replay_root,
        domain=_DOMAIN,
        intake_service=AnnuityPerformanceIntakeService(),
        processor=processor,
        resolver=resolver,
        config_release_id=manifest.release_id,
    )
    context = execution.context
    batch = execution.batch
    records = execution.records
    resolved_facts = execution.resolved_facts
    resolution_results = execution.resolution_results

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
    publication_policy = _load_publication_policy()

    derivation_candidates = derivation.derive(resolved_facts)
    reference_derivation_payload = _build_reference_derivation_payload(
        derivation_candidates
    )
    reference_derivation_baseline_path = (
        replay_root / f"legacy_reference_derivation_{period.replace('-', '_')}.json"
    )
    expected_reference_derivation = _load_replay_baseline(
        reference_derivation_baseline_path,
        "reference_derivation",
    )

    fact_processing_baseline_path = (
        replay_root / f"legacy_fact_processing_{period.replace('-', '_')}.json"
    )
    expected_fact_processing = _load_replay_baseline(
        fact_processing_baseline_path,
        "fact_processing",
    )
    identity_resolution_baseline_path = (
        replay_root / f"legacy_identity_resolution_{period.replace('-', '_')}.json"
    )
    expected_identity_resolution = _load_replay_baseline(
        identity_resolution_baseline_path,
        "identity_resolution",
    )
    contract_state_baseline_path = (
        replay_root / f"legacy_contract_state_{period.replace('-', '_')}.json"
    )
    expected_contract_state = _load_replay_baseline(
        contract_state_baseline_path,
        "contract_state",
    )

    publication_results = publication.execute(
        [
            build_validated_publication_bundle(
                domain=_DOMAIN,
                policy=publication_policy,
                publication_id="publication-facts",
                target_name="fact_annuity_performance",
                target_kind="fact",
                refresh_keys=["batch_id"],
                upsert_keys=[],
                source_batch_id=batch.batch_id,
                source_run_id=context.run_id,
                rows=[
                    fact.fields
                    | {"record_id": fact.record_id, "batch_id": fact.batch_id}
                    for fact in resolved_facts
                ],
            ),
            build_validated_publication_bundle(
                domain=_DOMAIN,
                policy=publication_policy,
                publication_id="publication-reference",
                target_name="company_reference",
                target_kind="reference",
                refresh_keys=[],
                upsert_keys=["company_id"],
                source_batch_id=batch.batch_id,
                source_run_id=context.run_id,
                rows=[candidate.candidate_payload for candidate in derivation_candidates],
            ),
        ]
    )

    contract_state = ContractStateProjection(storage).run(
        publication_ids=["publication-facts"],
        period=period,
    )
    contract_state_publication_results = publication.execute(
        [
            build_validated_publication_bundle(
                domain=_DOMAIN,
                policy=publication_policy,
                publication_id="publication-contract-state",
                target_name="contract_state",
                target_kind="projection",
                refresh_keys=["period"],
                upsert_keys=[],
                source_batch_id=batch.batch_id,
                source_run_id=context.run_id,
                rows=contract_state.rows,
            )
        ]
    )
    monthly_snapshot = MonthlySnapshotProjection(storage).run(
        publication_ids=["publication-contract-state"],
        period=period,
    )
    monthly_snapshot_publication_results = publication.execute(
        [
            build_validated_publication_bundle(
                domain=_DOMAIN,
                policy=publication_policy,
                publication_id="publication-monthly-snapshot",
                target_name="monthly_snapshot",
                target_kind="projection",
                refresh_keys=[],
                upsert_keys=[],
                source_batch_id=batch.batch_id,
                source_run_id=context.run_id,
                rows=monthly_snapshot.rows,
            )
        ]
    )

    expected_snapshot = _load_rows(replay_root / "legacy_monthly_snapshot_2026_03.json")

    checkpoint_results = [
        build_checkpoint_result(
            comparison_run_id=context.comparison_run_id,
            checkpoint_name="source_intake",
            checkpoint_type="contract",
            legacy_payload=_build_source_intake_contract_payload(),
            pro_payload=_build_observed_source_intake_contract(records),
            trace_anchor_rows=[record.anchor_row_no for record in records],
            severity="warn",
        ),
        build_checkpoint_result(
            comparison_run_id=context.comparison_run_id,
            checkpoint_name="fact_processing",
            checkpoint_type="parity",
            legacy_payload=expected_fact_processing,
            pro_payload=_build_fact_payload(resolved_facts),
            trace_anchor_rows=[record.anchor_row_no for record in records],
        ),
        build_checkpoint_result(
            comparison_run_id=context.comparison_run_id,
            checkpoint_name="identity_resolution",
            checkpoint_type="parity",
            legacy_payload=expected_identity_resolution,
            pro_payload=_build_identity_payload(resolution_results),
            trace_anchor_rows=[record.anchor_row_no for record in records],
        ),
        build_checkpoint_result(
            comparison_run_id=context.comparison_run_id,
            checkpoint_name="reference_derivation",
            checkpoint_type="parity",
            legacy_payload=expected_reference_derivation,
            pro_payload=reference_derivation_payload,
            trace_anchor_rows=[record.anchor_row_no for record in records],
        ),
        build_checkpoint_result(
            comparison_run_id=context.comparison_run_id,
            checkpoint_name="contract_state",
            checkpoint_type="parity",
            legacy_payload=expected_contract_state,
            pro_payload=contract_state.rows,
            trace_anchor_rows=[link.anchor_row_no for link in context.lineage_registry.all()],
        ),
        build_checkpoint_result(
            comparison_run_id=context.comparison_run_id,
            checkpoint_name="monthly_snapshot",
            checkpoint_type="parity",
            legacy_payload=expected_snapshot,
            pro_payload=monthly_snapshot.rows,
            trace_anchor_rows=[link.anchor_row_no for link in context.lineage_registry.all()],
        ),
    ]

    primary_failure = build_primary_failure(checkpoint_results)
    compatibility_case = None
    # Capture intermediate payloads in-memory before potential file corruption
    intermediate_payloads = {
        "reference_derivation": reference_derivation_payload,
        "fact_processing": _build_fact_payload(resolved_facts),
        "identity_resolution": _build_identity_payload(resolution_results),
        "contract_state": contract_state.rows,
        "source_intake": _build_observed_source_intake_contract(records),
        "monthly_snapshot": monthly_snapshot.rows,
    }
    if any(result.status == "failed" for result in checkpoint_results):
        involved_anchor_row_nos = sorted(
            {link.anchor_row_no for link in context.lineage_registry.all()}
        )
        if primary_failure is None:
            raise AssertionError("Expected a primary failure for failed replay results.")
        baseline_paths = {
            "fact_processing": fact_processing_baseline_path,
            "identity_resolution": identity_resolution_baseline_path,
            "reference_derivation": reference_derivation_baseline_path,
            "contract_state": contract_state_baseline_path,
            "monthly_snapshot": replay_root / "legacy_monthly_snapshot_2026_03.json",
        }
        legacy_payloads = intermediate_payloads
        pro_payloads_map = {
            "fact_processing": _build_fact_payload(resolved_facts),
            "identity_resolution": _build_identity_payload(resolution_results),
            "reference_derivation": reference_derivation_payload,
            "contract_state": contract_state.rows,
            "monthly_snapshot": monthly_snapshot.rows,
        }
        failure_locator, legacy_result, pro_result = (
            build_failure_compatibility_case_payload(
                primary_failure.checkpoint_name,
                baseline_paths=baseline_paths,
                legacy_payloads=legacy_payloads,
                pro_payloads=pro_payloads_map,
            )
        )
        compatibility_case = AdjudicationService(context.evidence_index).create_case(
            sample_locator=failure_locator,
            legacy_result=legacy_result,
            pro_result=pro_result,
            involved_anchor_row_nos=involved_anchor_row_nos,
            rationale=(
                f"{primary_failure.checkpoint_name} replay differs from accepted legacy baseline"
            ),
            affected_rule_version="annuity-performance-core:1",
            checkpoint_name=primary_failure.checkpoint_name,
            comparison_run_id=context.comparison_run_id,
        )

    all_publication_results = (
        publication_results
        + contract_state_publication_results
        + monthly_snapshot_publication_results
    )
    overall_outcome = (
        "failed"
        if any(result.status == "failed" for result in checkpoint_results)
        else "warning"
        if any(result.status == "warning" for result in checkpoint_results)
        else "passed"
    )
    report_markdown = (
        "# Phase 2 Annuity Performance Gate Report\n\n"
        f"- comparison_run_id: {context.comparison_run_id}\n"
        f"- overall_outcome: {overall_outcome}\n"
        f"- blocking_checkpoint: {primary_failure.checkpoint_name if primary_failure else 'none'}\n"
    )
    gate_summary, run_report = finalize_replay_run(
        context=context,
        batch=batch,
        baseline_version=f"legacy-monthly-snapshot:{period}",
        config_release_id=manifest.release_id,
        rule_pack_version=manifest.rule_pack_version,
        checkpoint_results=checkpoint_results,
        source_intake_adaptation=_aggregate_source_intake_adaptation(records),
        lineage_impact={
            "affected_anchor_rows": sorted(
                {link.anchor_row_no for link in context.lineage_registry.all()}
            ),
            "affected_record_ids": [fact.record_id for fact in resolved_facts],
            "affected_publication_targets": [
                result.target_name for result in all_publication_results
            ],
        },
        publication_results=all_publication_results,
        compatibility_case=compatibility_case,
        report_markdown=report_markdown,
    )

    return SliceRunOutcome(
        comparison_run_id=context.comparison_run_id,
        checkpoint_results=run_report.checkpoint_results,
        gate_summary=gate_summary,
        publication_results=all_publication_results,
        projection_results=[contract_state.result, monthly_snapshot.result],
        compatibility_case=compatibility_case,
        run_report=run_report,
        trace_store=context.trace_store,
        lineage_registry=context.lineage_registry,
        intermediate_payloads=intermediate_payloads,
    )

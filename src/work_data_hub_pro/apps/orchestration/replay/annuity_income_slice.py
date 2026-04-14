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
from work_data_hub_pro.capabilities.fact_processing.annuity_income.service import (
    AnnuityIncomeArtifactExporter,
    AnnuityIncomeProcessor,
)
from work_data_hub_pro.capabilities.fact_processing.cleansing.manifest import (
    CleansingManifest,
)
from work_data_hub_pro.capabilities.identity_resolution.service import (
    CacheFirstIdentityResolutionService,
    InMemoryIdentityCache,
    StaticIdentityProvider,
)
from work_data_hub_pro.capabilities.reference_derivation.service import (
    ReferenceDerivationService,
)
from work_data_hub_pro.capabilities.source_intake.annuity_income.service import (
    AnnuityIncomeIntakeService,
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
from work_data_hub_pro.platform.contracts.publication import PublicationResult
from work_data_hub_pro.platform.lineage.registry import LineageRegistry
from work_data_hub_pro.platform.publication.service import PublicationService, load_publication_policy
from work_data_hub_pro.platform.storage.in_memory_tables import InMemoryTableStore
from work_data_hub_pro.platform.tracing.in_memory_trace_store import InMemoryTraceStore


_DOMAIN = "annuity_income"
_PUBLICATION_POLICY_PATH = Path("config/policies/publication.json")
_RELEASE_PATH = Path("config/releases/2026-04-14-annuity-income-baseline.json")
_DOMAIN_CONFIG_PATH = Path("config/domains/annuity_income/cleansing.json")

_SOURCE_INTAKE_CONTRACT = {
    "record_count": 1,
    "required_fields": [
        "company_name",
        "period",
        "business_type",
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
    projection_results: list[object]
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
    return f"income-{int(source_row_no):03d}"


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


def _build_fact_payload(facts) -> list[dict[str, object]]:
    return _sorted_payload(
        [
            fact.fields | {"record_id": _stable_fact_id_from_row_no(fact.fields["source_row_no"])}
            for fact in facts
        ]
    )


def _build_identity_payload(resolution_results) -> list[dict[str, object]]:
    return _sorted_payload(
        [
            {
                "record_id": _stable_fact_id_from_row_no(item.fact.fields["source_row_no"]),
                "resolved_identity": item.result.resolved_identity,
                "resolution_method": item.result.resolution_method,
                "fallback_level": item.result.fallback_level,
                "evidence_refs": item.result.evidence_refs,
            }
            for item in resolution_results
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


def _build_operator_artifact_payload(records, artifact_results) -> list[dict[str, object]]:
    return _sorted_payload(
        [
            {
                "record_id": _stable_fact_id_from_row_no(record.anchor_row_no),
                "unknown_names_csv": result.unknown_names_csv is not None,
                "failed_records_csv": result.failed_records_csv is not None,
            }
            for record, result in zip(records, artifact_results, strict=True)
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


def run_annuity_income_slice(
    *,
    workbook: Path,
    period: str,
    replay_root: Path,
) -> SliceRunOutcome:
    manifest = _load_manifest()
    execution = execute_replay_run(
        workbook=workbook,
        period=period,
        replay_root=replay_root,
        domain=_DOMAIN,
        intake_service=AnnuityIncomeIntakeService(),
        processor=AnnuityIncomeProcessor(manifest),
        resolver=CacheFirstIdentityResolutionService(
            cache=InMemoryIdentityCache({}),
            provider=StaticIdentityProvider({}),
        ),
        config_release_id=manifest.release_id,
    )
    context = execution.context
    batch = execution.batch
    records = execution.records
    resolution_results = execution.resolution_results
    resolved_facts = execution.resolved_facts

    exporter = AnnuityIncomeArtifactExporter(replay_root / "artifacts")
    artifact_results = [
        exporter.export_for_resolution(resolved, export_unknown_names=True)
        for resolved in resolution_results
    ]

    derivation = ReferenceDerivationService()
    derivation_candidates = derivation.derive(resolved_facts)

    expected_fact_processing = _load_replay_baseline(
        replay_root / f"legacy_fact_processing_{period.replace('-', '_')}.json",
        "fact_processing",
    )
    expected_identity_resolution = _load_replay_baseline(
        replay_root / f"legacy_identity_resolution_{period.replace('-', '_')}.json",
        "identity_resolution",
    )
    expected_reference_derivation = _load_replay_baseline(
        replay_root / f"legacy_reference_derivation_{period.replace('-', '_')}.json",
        "reference_derivation",
    )
    expected_operator_artifacts = _load_replay_baseline(
        replay_root / f"legacy_operator_artifacts_{period.replace('-', '_')}.json",
        "operator_artifacts",
    )

    publication_policy = _load_publication_policy()
    storage = InMemoryTableStore()
    publication = PublicationService(storage)
    publication_results = publication.execute(
        [
            build_validated_publication_bundle(
                domain=_DOMAIN,
                policy=publication_policy,
                publication_id="publication-income-facts",
                target_name="fact_annuity_income",
                target_kind="fact",
                refresh_keys=["batch_id"],
                upsert_keys=[],
                source_batch_id=batch.batch_id,
                source_run_id=context.run_id,
                rows=[
                    fact.fields | {"record_id": fact.record_id, "batch_id": fact.batch_id}
                    for fact in resolved_facts
                ],
            ),
            build_validated_publication_bundle(
                domain=_DOMAIN,
                policy=publication_policy,
                publication_id="publication-income-company-reference",
                target_name="company_reference",
                target_kind="reference",
                refresh_keys=[],
                upsert_keys=["company_id"],
                source_batch_id=batch.batch_id,
                source_run_id=context.run_id,
                rows=[
                    candidate.candidate_payload
                    for candidate in derivation_candidates
                    if candidate.target_object == "company_reference"
                ],
            ),
            build_validated_publication_bundle(
                domain=_DOMAIN,
                policy=publication_policy,
                publication_id="publication-income-customer-signal",
                target_name="customer_master_signal",
                target_kind="reference",
                refresh_keys=[],
                upsert_keys=["company_id", "period"],
                source_batch_id=batch.batch_id,
                source_run_id=context.run_id,
                rows=[
                    candidate.candidate_payload
                    for candidate in derivation_candidates
                    if candidate.target_object == "customer_master_signal"
                ],
            ),
        ]
    )

    source_intake_payload = _build_observed_source_intake_contract(records)
    fact_processing_payload = _build_fact_payload(resolved_facts)
    identity_payload = _build_identity_payload(resolution_results)
    reference_derivation_payload = _build_reference_derivation_payload(derivation_candidates)
    operator_artifacts_payload = _build_operator_artifact_payload(records, artifact_results)

    checkpoint_results = [
        build_checkpoint_result(
            comparison_run_id=context.comparison_run_id,
            checkpoint_name="source_intake",
            checkpoint_type="contract",
            legacy_payload=_build_source_intake_contract_payload(),
            pro_payload=source_intake_payload,
            trace_anchor_rows=[record.anchor_row_no for record in records],
            severity="warn",
        ),
        build_checkpoint_result(
            comparison_run_id=context.comparison_run_id,
            checkpoint_name="fact_processing",
            checkpoint_type="parity",
            legacy_payload=expected_fact_processing,
            pro_payload=fact_processing_payload,
            trace_anchor_rows=[record.anchor_row_no for record in records],
        ),
        build_checkpoint_result(
            comparison_run_id=context.comparison_run_id,
            checkpoint_name="identity_resolution",
            checkpoint_type="parity",
            legacy_payload=expected_identity_resolution,
            pro_payload=identity_payload,
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
            checkpoint_name="operator_artifacts",
            checkpoint_type="parity",
            legacy_payload=expected_operator_artifacts,
            pro_payload=operator_artifacts_payload,
            trace_anchor_rows=[record.anchor_row_no for record in records],
        ),
    ]

    primary_failure = build_primary_failure(checkpoint_results)
    compatibility_case = None
    intermediate_payloads = {
        "fact_processing": fact_processing_payload,
        "identity_resolution": identity_payload,
        "reference_derivation": reference_derivation_payload,
        "operator_artifacts": operator_artifacts_payload,
        "source_intake": [source_intake_payload],
    }
    if any(result.status == "failed" for result in checkpoint_results):
        involved_anchor_row_nos = sorted(
            {link.anchor_row_no for link in context.lineage_registry.all()}
        )
        if primary_failure is None:
            raise AssertionError("Expected a primary failure for failed replay results.")
        baseline_paths = {
            "fact_processing": replay_root / f"legacy_fact_processing_{period.replace('-', '_')}.json",
            "identity_resolution": replay_root / f"legacy_identity_resolution_{period.replace('-', '_')}.json",
            "reference_derivation": replay_root / f"legacy_reference_derivation_{period.replace('-', '_')}.json",
            "operator_artifacts": replay_root / f"legacy_operator_artifacts_{period.replace('-', '_')}.json",
        }
        legacy_payloads = {
            "fact_processing": expected_fact_processing,
            "identity_resolution": expected_identity_resolution,
            "reference_derivation": expected_reference_derivation,
            "operator_artifacts": expected_operator_artifacts,
        }
        pro_payloads_map = {
            "fact_processing": fact_processing_payload,
            "identity_resolution": identity_payload,
            "reference_derivation": reference_derivation_payload,
            "operator_artifacts": operator_artifacts_payload,
        }
        failure_locator, legacy_result, pro_result = build_failure_compatibility_case_payload(
            primary_failure.checkpoint_name,
            baseline_paths=baseline_paths,
            legacy_payloads=legacy_payloads,
            pro_payloads=pro_payloads_map,
        )
        compatibility_case = AdjudicationService(context.evidence_index).create_case(
            sample_locator=failure_locator,
            legacy_result=legacy_result,
            pro_result=pro_result,
            involved_anchor_row_nos=involved_anchor_row_nos,
            rationale=(
                f"{primary_failure.checkpoint_name} replay differs from accepted legacy baseline"
            ),
            affected_rule_version="annuity-income-core:1",
            checkpoint_name=primary_failure.checkpoint_name,
            comparison_run_id=context.comparison_run_id,
        )

    report_markdown = (
        "# Phase 2 Annuity Income Gate Report\n\n"
        f"- comparison_run_id: {context.comparison_run_id}\n"
        f"- overall_outcome: {'failed' if primary_failure else 'passed'}\n"
        f"- blocking_checkpoint: {primary_failure.checkpoint_name if primary_failure else 'none'}\n"
    )
    gate_summary, run_report = finalize_replay_run(
        context=context,
        batch=batch,
        baseline_version=f"legacy-annuity-income:{period}",
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
                result.target_name for result in publication_results
            ],
        },
        publication_results=publication_results,
        compatibility_case=compatibility_case,
        report_markdown=report_markdown,
    )

    return SliceRunOutcome(
        comparison_run_id=context.comparison_run_id,
        checkpoint_results=run_report.checkpoint_results,
        gate_summary=gate_summary,
        publication_results=publication_results,
        projection_results=[],
        compatibility_case=compatibility_case,
        run_report=run_report,
        trace_store=context.trace_store,
        lineage_registry=context.lineage_registry,
        intermediate_payloads=intermediate_payloads,
    )

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
from work_data_hub_pro.governance.compatibility.models import CompatibilityCase
from work_data_hub_pro.governance.evidence_index.file_store import FileEvidenceIndex
from work_data_hub_pro.platform.contracts.models import ProjectionResult
from work_data_hub_pro.platform.contracts.publication import PublicationResult
from work_data_hub_pro.platform.publication.service import (
    PublicationBundle,
    PublicationService,
    build_publication_plan,
    load_publication_policy,
)
from work_data_hub_pro.platform.storage.in_memory_tables import InMemoryTableStore
from work_data_hub_pro.platform.tracing.in_memory_trace_store import InMemoryTraceStore


@dataclass(frozen=True)
class SliceRunOutcome:
    publication_results: list[PublicationResult]
    projection_results: list[ProjectionResult]
    compatibility_case: CompatibilityCase | None
    trace_store: InMemoryTraceStore


def _load_rows(path: Path) -> list[dict[str, object]]:
    return json.loads(path.read_text(encoding="utf-8"))


def run_annuity_performance_slice(
    *,
    workbook: Path,
    period: str,
    replay_root: Path,
) -> SliceRunOutcome:
    run_id = f"run-{uuid4().hex[:8]}"
    trace_store = InMemoryTraceStore()
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
        for event in row_trace_events:
            trace_store.record(event)
        evidence_index.index_trace_events(
            batch_id=batch.batch_id,
            anchor_row_no=record.anchor_row_no,
            events=row_trace_events,
        )
        resolved_facts.append(resolved.fact)

    derivation_candidates = derivation.derive(resolved_facts)
    publication_results = publication.execute(
        [
            PublicationBundle(
                plan=build_publication_plan(
                    policy=publication_policy,
                    publication_id="publication-facts",
                    target_name="fact_annuity_performance",
                    target_kind="fact",
                    refresh_keys=["batch_id"],
                    upsert_keys=[],
                    source_batch_id=batch.batch_id,
                    source_run_id=run_id,
                ),
                rows=[
                    fact.fields
                    | {"record_id": fact.record_id, "batch_id": fact.batch_id}
                    for fact in resolved_facts
                ],
            ),
            PublicationBundle(
                plan=build_publication_plan(
                    policy=publication_policy,
                    publication_id="publication-reference",
                    target_name="company_reference",
                    target_kind="reference",
                    refresh_keys=[],
                    upsert_keys=["company_id"],
                    source_batch_id=batch.batch_id,
                    source_run_id=run_id,
                ),
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
            PublicationBundle(
                plan=build_publication_plan(
                    policy=publication_policy,
                    publication_id="publication-contract-state",
                    target_name="contract_state",
                    target_kind="projection",
                    refresh_keys=["period"],
                    upsert_keys=[],
                    source_batch_id=batch.batch_id,
                    source_run_id=run_id,
                ),
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
            PublicationBundle(
                plan=build_publication_plan(
                    policy=publication_policy,
                    publication_id="publication-monthly-snapshot",
                    target_name="monthly_snapshot",
                    target_kind="projection",
                    refresh_keys=[],
                    upsert_keys=[],
                    source_batch_id=batch.batch_id,
                    source_run_id=run_id,
                ),
                rows=monthly_snapshot.rows,
            )
        ]
    )

    expected_snapshot = _load_rows(replay_root / "legacy_monthly_snapshot_2026_03.json")
    compatibility_case = None
    if monthly_snapshot.rows != expected_snapshot:
        compatibility_case = AdjudicationService(evidence_index).create_case(
            sample_locator=str(replay_root / "legacy_monthly_snapshot_2026_03.json"),
            legacy_result={"rows": expected_snapshot},
            pro_result={"rows": monthly_snapshot.rows},
            rationale="Monthly snapshot replay differs from accepted legacy baseline",
            affected_rule_version="annuity-performance-core:1",
        )

    return SliceRunOutcome(
        publication_results=(
            publication_results
            + contract_state_publication_results
            + monthly_snapshot_publication_results
        ),
        projection_results=[contract_state.result, monthly_snapshot.result],
        compatibility_case=compatibility_case,
        trace_store=trace_store,
    )

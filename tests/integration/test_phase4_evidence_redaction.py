from __future__ import annotations

import json
from pathlib import Path

from work_data_hub_pro.apps.orchestration.replay.lookup import load_replay_lookup
from work_data_hub_pro.governance.compatibility.gate_models import (
    CheckpointFingerprint,
    CheckpointResult,
    ComparisonRunManifest,
    GateSummary,
)
from work_data_hub_pro.governance.compatibility.gate_runtime import (
    default_package_paths,
    write_comparison_run_package,
)
from work_data_hub_pro.governance.compatibility.models import CompatibilityCase
from work_data_hub_pro.governance.evidence_index.file_store import FileEvidenceIndex
from work_data_hub_pro.platform.contracts.models import FieldTraceEvent
from work_data_hub_pro.platform.contracts.publication import PublicationMode, PublicationResult



def _write_lookup_ready_package(
    *,
    replay_root: Path,
    comparison_run_id: str,
    checkpoint_results: list[CheckpointResult],
    source_intake_adaptation: dict[str, object],
    lineage_impact: dict[str, object],
    compatibility_case: CompatibilityCase | None,
) -> FileEvidenceIndex:
    evidence_index = FileEvidenceIndex(replay_root / "evidence")
    manifest = ComparisonRunManifest(
        comparison_run_id=comparison_run_id,
        domain="annual_award",
        period="2026-03",
        baseline_version="baseline-001",
        config_release_id="release-001",
        rule_pack_version="rules-001",
        decision_owner="compatibility-review",
        package_root=f"comparison_runs/{comparison_run_id}",
        package_paths=default_package_paths(comparison_run_id),
    )
    gate_summary = GateSummary(
        comparison_run_id=comparison_run_id,
        overall_outcome="warning",
        total_checkpoints=len(checkpoint_results),
        blocking_count=0,
        warning_count=1,
        passed_count=0,
        severity_counts={"warn": 1},
        status_counts={"warning": 1},
        checkpoint_statuses={result.checkpoint_name: result.status for result in checkpoint_results},
    )
    write_comparison_run_package(
        evidence_index=evidence_index,
        manifest=manifest,
        gate_summary=gate_summary,
        checkpoint_results=checkpoint_results,
        checkpoint_diffs={},
        source_intake_adaptation=source_intake_adaptation,
        lineage_impact=lineage_impact,
        publication_results=[
            PublicationResult(
                publication_id="publication-001",
                target_name="monthly_snapshot",
                mode=PublicationMode.REFRESH,
                affected_rows=1,
                transaction_group="monthly-snapshot",
                success=True,
            )
        ],
        compatibility_case=compatibility_case,
        report_markdown="# Comparison Report\n",
    )
    return evidence_index



def test_trace_events_are_redacted_before_persistence(tmp_path: Path) -> None:
    evidence_index = FileEvidenceIndex(tmp_path / "evidence")

    path = evidence_index.index_trace_events(
        batch_id="annuity_performance:2026-03",
        anchor_row_no=2,
        events=[
            FieldTraceEvent(
                trace_id="trace-001",
                event_id="evt-001",
                event_seq=1,
                run_id="run-001",
                batch_id="annuity_performance:2026-03",
                record_id="record-001",
                anchor_row_no=2,
                stage_id="fact_processing",
                field_name="company_name",
                value_before="Acme Holdings",
                value_after="ACME HOLDINGS",
                rule_id="uppercase-company-name",
                rule_version="1",
                config_release_id="2026-04-11-annuity-performance-baseline",
                action_type="cleanse",
                timestamp="2026-04-11T00:00:00Z",
                success=True,
            )
        ],
    )

    payload = json.loads(path.read_text(encoding="utf-8"))

    assert payload == [
        {
            "trace_id": "trace-001",
            "event_id": "evt-001",
            "event_seq": 1,
            "run_id": "run-001",
            "batch_id": "annuity_performance:2026-03",
            "record_id": "record-001",
            "anchor_row_no": 2,
            "stage_id": "fact_processing",
            "field_name": "company_name",
            "value_before": "***REDACTED***",
            "value_after": "***REDACTED***",
            "rule_id": "uppercase-company-name",
            "rule_version": "1",
            "config_release_id": "2026-04-11-annuity-performance-baseline",
            "action_type": "cleanse",
            "timestamp": "2026-04-11T00:00:00Z",
            "success": True,
            "error_message": None,
        }
    ]



def test_checkpoint_payloads_are_redacted_before_persistence(tmp_path: Path) -> None:
    evidence_index = FileEvidenceIndex(tmp_path / "evidence")
    comparison_run_id = "comparison-redaction-001"
    checkpoint_result = CheckpointResult(
        comparison_run_id=comparison_run_id,
        checkpoint_name="monthly_snapshot",
        checkpoint_type="parity",
        status="warning",
        severity="warn",
        legacy_fingerprint=CheckpointFingerprint(fingerprint="legacy", row_count=1),
        pro_fingerprint=CheckpointFingerprint(fingerprint="pro", row_count=1),
        diff_path=None,
        trace_anchor_rows=[7],
        legacy_payload={
            "company_name": "Acme Holdings",
            "customer_name": "Ada Lovelace",
            "trace_path": "trace/batch_001__row_7.json",
            "origin_row_nos": [70, 71],
            "parent_record_ids": ["parent-001"],
            "raw_payload": {"company_name": "Acme Holdings"},
            "nested": {"normalized_company_name": "ACME HOLDINGS", "status": "legacy"},
        },
        pro_payload={
            "company_name": "Acme Holdings",
            "customer_name": "Ada Lovelace",
            "trace_path": "trace/batch_001__row_7.json",
            "origin_row_nos": [70, 71],
            "parent_record_ids": ["parent-001"],
            "raw_payload": {"customer_name": "Ada Lovelace"},
            "nested": {"raw_company_name": "Acme Holdings", "status": "pro"},
        },
    )

    path = evidence_index.write_checkpoint_results(comparison_run_id, [checkpoint_result])
    payload = json.loads(path.read_text(encoding="utf-8"))
    stored = payload[0]

    assert stored["legacy_payload"]["company_name"] == "***REDACTED***"
    assert stored["legacy_payload"]["customer_name"] == "***REDACTED***"
    assert stored["legacy_payload"]["trace_path"] == "trace/batch_001__row_7.json"
    assert stored["legacy_payload"]["origin_row_nos"] == [70, 71]
    assert stored["legacy_payload"]["parent_record_ids"] == ["parent-001"]
    assert stored["legacy_payload"]["raw_payload"] == "***REDACTED***"
    assert stored["legacy_payload"]["nested"] == {
        "normalized_company_name": "***REDACTED***",
        "status": "legacy",
    }
    assert set(stored["legacy_payload"]) == {
        "company_name",
        "customer_name",
        "trace_path",
        "origin_row_nos",
        "parent_record_ids",
        "raw_payload",
        "nested",
    }
    assert stored["pro_payload"]["company_name"] == "***REDACTED***"
    assert stored["pro_payload"]["customer_name"] == "***REDACTED***"
    assert stored["pro_payload"]["trace_path"] == "trace/batch_001__row_7.json"
    assert stored["pro_payload"]["origin_row_nos"] == [70, 71]
    assert stored["pro_payload"]["parent_record_ids"] == ["parent-001"]
    assert stored["pro_payload"]["raw_payload"] == "***REDACTED***"
    assert stored["pro_payload"]["nested"] == {
        "raw_company_name": "***REDACTED***",
        "status": "pro",
    }
    assert set(stored["pro_payload"]) == {
        "company_name",
        "customer_name",
        "trace_path",
        "origin_row_nos",
        "parent_record_ids",
        "raw_payload",
        "nested",
    }



def test_compatibility_case_payload_is_redacted_without_erasing_structure(tmp_path: Path) -> None:
    evidence_index = FileEvidenceIndex(tmp_path / "evidence")
    comparison_run_id = "comparison-redaction-compat-001"
    case = CompatibilityCase(
        case_id="compat-001",
        sample_locator="reference/historical_replays/annual_award/sample.json",
        legacy_result={
            "company_name": "Acme Holdings",
            "nested": {"status": "legacy", "customer_name": "Ada Lovelace"},
        },
        pro_result={
            "company_name": "Acme Holdings",
            "nested": {"status": "pro", "normalized_company_name": "ACME HOLDINGS"},
        },
        business_rationale="Monthly snapshot differs",
        affected_rule_version="annual-award-core:1",
        severity="warn",
        decision_status="pending_review",
        decision_owner=None,
        resolution_note=None,
        closure_evidence=[],
        closed_at=None,
        closed_by=None,
        resolved_outcome=None,
        decision_history=[],
        checkpoint_name="monthly_snapshot",
        comparison_run_id=comparison_run_id,
        involved_anchor_row_nos=[7],
    )

    path = evidence_index.write_comparison_case(comparison_run_id, case)
    payload = json.loads(path.read_text(encoding="utf-8"))

    assert payload["case_id"] == "compat-001"
    assert payload["comparison_run_id"] == comparison_run_id
    assert payload["severity"] == "warn"
    assert payload["decision_status"] == "pending_review"
    assert payload["involved_anchor_row_nos"] == [7]
    assert payload["legacy_result"] == {
        "company_name": "***REDACTED***",
        "nested": {"status": "legacy", "customer_name": "***REDACTED***"},
    }
    assert payload["pro_result"] == {
        "company_name": "***REDACTED***",
        "nested": {"status": "pro", "normalized_company_name": "***REDACTED***"},
    }



def test_replay_lookup_still_resolves_redacted_lineage(tmp_path: Path, monkeypatch) -> None:
    comparison_run_id = "annual-award-2026-03-redacted"
    replay_root = tmp_path / "annual_award"
    replay_root.mkdir(parents=True, exist_ok=True)
    trace_path = (
        FileEvidenceIndex(replay_root / "evidence")
        .index_trace_events(batch_id="batch:001", anchor_row_no=7, events=[])
        .as_posix()
    )
    checkpoint_result = CheckpointResult(
        comparison_run_id=comparison_run_id,
        checkpoint_name="monthly_snapshot",
        checkpoint_type="parity",
        status="warning",
        severity="warn",
        legacy_fingerprint=CheckpointFingerprint(fingerprint="legacy", row_count=1),
        pro_fingerprint=CheckpointFingerprint(fingerprint="pro", row_count=1),
        diff_path=None,
        trace_anchor_rows=[7],
    )
    _write_lookup_ready_package(
        replay_root=replay_root,
        comparison_run_id=comparison_run_id,
        checkpoint_results=[checkpoint_result],
        source_intake_adaptation={
            "records": [
                {
                    "record_id": "record-001",
                    "company_name": "Acme Holdings",
                    "raw_payload": {"company_name": "Acme Holdings"},
                }
            ]
        },
        lineage_impact={
            "records": [
                {
                    "record_id": "record-001",
                    "batch_id": "batch:001",
                    "anchor_row_no": 7,
                    "origin_row_nos": [70, 71],
                    "parent_record_ids": ["parent-001"],
                    "trace_path": trace_path,
                    "artifact_gaps": [],
                    "company_name": "Acme Holdings",
                    "raw_payload": {"company_name": "Acme Holdings"},
                }
            ]
        },
        compatibility_case=None,
    )

    registry = {
        "annual_award": type(
            "Spec",
            (),
            {"replay_root": replay_root},
        )()
    }
    monkeypatch.setattr(
        "work_data_hub_pro.apps.orchestration.replay.lookup.load_replay_diagnostics",
        lambda run_id: __import__(
            "work_data_hub_pro.apps.orchestration.replay.diagnostics",
            fromlist=["load_replay_diagnostics"],
        ).load_replay_diagnostics(run_id, registry=registry),
    )

    result = load_replay_lookup(comparison_run_id, record_id="record-001")
    lineage_payload = json.loads(
        (
            replay_root
            / "evidence"
            / "comparison_runs"
            / comparison_run_id
            / "lineage-impact.json"
        ).read_text(encoding="utf-8")
    )

    assert lineage_payload["records"][0]["company_name"] == "***REDACTED***"
    assert lineage_payload["records"][0]["raw_payload"] == "***REDACTED***"
    assert result.trace_path == trace_path
    assert result.origin_row_nos == [70, 71]
    assert result.parent_record_ids == ["parent-001"]
    assert result.artifact_gaps == []

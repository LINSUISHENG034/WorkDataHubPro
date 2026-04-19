from __future__ import annotations

import json
from pathlib import Path

import pytest

from work_data_hub_pro.apps.orchestration.replay.contracts import ReplayDomainSpec
from work_data_hub_pro.apps.orchestration.replay.diagnostics import (
    load_replay_diagnostics,
)
from work_data_hub_pro.apps.orchestration.replay.lookup import (
    ReplayLookupError,
    load_replay_lookup,
)
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
from work_data_hub_pro.platform.contracts.publication import (
    PublicationMode,
    PublicationResult,
)



def _registry_for(tmp_path: Path) -> dict[str, ReplayDomainSpec]:
    registry: dict[str, ReplayDomainSpec] = {}
    for domain in ("annuity_performance", "annual_award", "annual_loss", "annuity_income"):
        replay_root = tmp_path / domain
        replay_root.mkdir(parents=True, exist_ok=True)
        registry[domain] = ReplayDomainSpec(
            wrapper_command=f"replay-{domain.replace('_', '-')}",
            replay_root=replay_root,
            runbook_path=tmp_path / "docs" / f"{domain}.md",
            release_path=tmp_path / "config" / f"{domain}.json",
            domain_config_path=tmp_path / "config" / domain / "cleansing.json",
            runner_import=f"tests.fake:{domain}",
        )
    return registry



def _write_lookup_package(
    *,
    replay_root: Path,
    comparison_run_id: str,
    status: str,
    lineage_records: list[dict[str, object]],
    compatibility_case: CompatibilityCase | None = None,
) -> None:
    evidence_index = FileEvidenceIndex(replay_root / "evidence")
    manifest = ComparisonRunManifest(
        comparison_run_id=comparison_run_id,
        domain=replay_root.name,
        period="2026-03",
        baseline_version="baseline-001",
        config_release_id="release-001",
        rule_pack_version="rules-001",
        decision_owner="compatibility-review",
        package_root=f"comparison_runs/{comparison_run_id}",
        package_paths=default_package_paths(comparison_run_id),
    )
    checkpoint_result = CheckpointResult(
        comparison_run_id=comparison_run_id,
        checkpoint_name="monthly_snapshot",
        checkpoint_type="parity",
        status=status,
        severity="block" if status == "failed" else "warn" if status == "warning" else "block",
        legacy_fingerprint=CheckpointFingerprint(fingerprint="legacy-hash", row_count=1),
        pro_fingerprint=CheckpointFingerprint(
            fingerprint="legacy-hash" if status == "passed" else "pro-hash",
            row_count=1,
        ),
        diff_path=f"comparison_runs/{comparison_run_id}/diffs/monthly_snapshot.json",
        trace_anchor_rows=sorted({int(record["anchor_row_no"]) for record in lineage_records}),
    )
    gate_summary = GateSummary(
        comparison_run_id=comparison_run_id,
        overall_outcome="failed" if status == "failed" else status,
        total_checkpoints=1,
        blocking_count=1 if status == "failed" else 0,
        warning_count=1 if status == "warning" else 0,
        passed_count=1 if status == "passed" else 0,
        severity_counts={
            "block": 1 if status == "failed" else 0,
            "warn": 1 if status == "warning" else 0,
        },
        status_counts={
            "failed": 1 if status == "failed" else 0,
            "warning": 1 if status == "warning" else 0,
            "passed": 1 if status == "passed" else 0,
        },
        checkpoint_statuses={"monthly_snapshot": status},
    )
    write_comparison_run_package(
        evidence_index=evidence_index,
        manifest=manifest,
        gate_summary=gate_summary,
        checkpoint_results=[checkpoint_result],
        checkpoint_diffs={},
        source_intake_adaptation={"records": []},
        lineage_impact={"records": lineage_records},
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



def test_replay_lookup_returns_source_stage_evidence(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    registry = _registry_for(tmp_path)
    comparison_run_id = "annual-award-2026-03-passed"
    replay_root = registry["annual_award"].replay_root
    trace_path = (
        FileEvidenceIndex(replay_root / "evidence")
        .index_trace_events(batch_id="batch:001", anchor_row_no=7, events=[])
        .as_posix()
    )
    _write_lookup_package(
        replay_root=replay_root,
        comparison_run_id=comparison_run_id,
        status="passed",
        lineage_records=[
            {
                "record_id": "record-001",
                "batch_id": "batch:001",
                "anchor_row_no": 7,
                "origin_row_nos": [70, 71],
                "parent_record_ids": ["parent-001"],
                "trace_path": trace_path,
                "artifact_gaps": [],
            }
        ],
    )
    monkeypatch.setattr(
        "work_data_hub_pro.apps.orchestration.replay.lookup.load_replay_diagnostics",
        lambda run_id: load_replay_diagnostics(run_id, registry=registry),
    )

    result = load_replay_lookup(comparison_run_id, record_id="record-001")

    assert result.batch_id == "batch:001"
    assert result.anchor_row_no == 7
    assert result.origin_row_nos == [70, 71]
    assert result.parent_record_ids == ["parent-001"]
    assert result.trace_path == trace_path
    assert result.artifact_gaps == []



def test_replay_lookup_handles_failed_run_with_missing_trace_artifact(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    registry = _registry_for(tmp_path)
    comparison_run_id = "annual-loss-2026-03-failed"
    replay_root = registry["annual_loss"].replay_root
    _write_lookup_package(
        replay_root=replay_root,
        comparison_run_id=comparison_run_id,
        status="failed",
        compatibility_case=CompatibilityCase(
            case_id="compat-001",
            sample_locator="reference/historical_replays/annual_loss/sample.json",
            legacy_result={"rows": [{"record_id": "legacy-1"}]},
            pro_result={"rows": [{"record_id": "pro-1"}]},
            business_rationale="monthly_snapshot replay differs from accepted legacy baseline",
            affected_rule_version="annual-loss-core:1",
            decision_owner=None,
            resolution_note=None,
            closure_evidence=[],
            closed_at=None,
            closed_by=None,
            resolved_outcome=None,
            decision_history=[],
            checkpoint_name="monthly_snapshot",
            comparison_run_id=comparison_run_id,
            involved_anchor_row_nos=[9],
        ),
        lineage_records=[
            {
                "record_id": "record-009",
                "batch_id": "batch:009",
                "anchor_row_no": 9,
                "origin_row_nos": [90],
                "parent_record_ids": ["parent-009"],
                "trace_path": None,
                "artifact_gaps": ["trace_missing"],
            }
        ],
    )
    monkeypatch.setattr(
        "work_data_hub_pro.apps.orchestration.replay.lookup.load_replay_diagnostics",
        lambda run_id: load_replay_diagnostics(run_id, registry=registry),
    )

    result = load_replay_lookup(comparison_run_id, record_id="record-009")

    assert result.trace_path is None
    assert result.artifact_gaps == ["trace_missing"]
    assert result.checkpoint_statuses == {"monthly_snapshot": "failed"}



def test_replay_lookup_rejects_missing_selectors() -> None:
    with pytest.raises(ReplayLookupError, match="missing_selector"):
        load_replay_lookup("comparison-001")



def test_replay_lookup_rejects_both_selectors() -> None:
    with pytest.raises(ReplayLookupError, match="conflicting_selectors"):
        load_replay_lookup("comparison-001", record_id="record-001", anchor_row_no=7)



def test_replay_lookup_rejects_path_like_comparison_run_id() -> None:
    with pytest.raises(ReplayLookupError, match="invalid_comparison_run_id"):
        load_replay_lookup("../bad", record_id="record-001")



def test_replay_lookup_rejects_unknown_record_id(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    registry = _registry_for(tmp_path)
    comparison_run_id = "annual-award-2026-03-passed"
    _write_lookup_package(
        replay_root=registry["annual_award"].replay_root,
        comparison_run_id=comparison_run_id,
        status="passed",
        lineage_records=[
            {
                "record_id": "record-001",
                "batch_id": "batch:001",
                "anchor_row_no": 7,
                "origin_row_nos": [70],
                "parent_record_ids": ["parent-001"],
                "trace_path": None,
                "artifact_gaps": ["trace_missing"],
            }
        ],
    )
    monkeypatch.setattr(
        "work_data_hub_pro.apps.orchestration.replay.lookup.load_replay_diagnostics",
        lambda run_id: load_replay_diagnostics(run_id, registry=registry),
    )

    with pytest.raises(ReplayLookupError, match="record_not_found"):
        load_replay_lookup(comparison_run_id, record_id="unknown-record")



def test_replay_lookup_rejects_ambiguous_anchor_row_no(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    registry = _registry_for(tmp_path)
    comparison_run_id = "annual-award-2026-03-ambiguous"
    _write_lookup_package(
        replay_root=registry["annual_award"].replay_root,
        comparison_run_id=comparison_run_id,
        status="warning",
        lineage_records=[
            {
                "record_id": "record-001",
                "batch_id": "batch:001",
                "anchor_row_no": 7,
                "origin_row_nos": [70],
                "parent_record_ids": ["parent-001"],
                "trace_path": None,
                "artifact_gaps": ["trace_missing"],
            },
            {
                "record_id": "record-002",
                "batch_id": "batch:001",
                "anchor_row_no": 7,
                "origin_row_nos": [71],
                "parent_record_ids": ["parent-002"],
                "trace_path": None,
                "artifact_gaps": ["trace_missing"],
            },
        ],
    )
    monkeypatch.setattr(
        "work_data_hub_pro.apps.orchestration.replay.lookup.load_replay_diagnostics",
        lambda run_id: load_replay_diagnostics(run_id, registry=registry),
    )

    with pytest.raises(ReplayLookupError, match="ambiguous_anchor"):
        load_replay_lookup(comparison_run_id, anchor_row_no=7)



def test_replay_lookup_fails_closed_for_malformed_lineage_package(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    registry = _registry_for(tmp_path)
    comparison_run_id = "annual-award-2026-03-malformed"
    replay_root = registry["annual_award"].replay_root
    _write_lookup_package(
        replay_root=replay_root,
        comparison_run_id=comparison_run_id,
        status="passed",
        lineage_records=[
            {
                "record_id": "record-001",
                "batch_id": "batch:001",
                "anchor_row_no": 7,
                "origin_row_nos": [70],
                "parent_record_ids": ["parent-001"],
                "trace_path": None,
                "artifact_gaps": ["trace_missing"],
            }
        ],
    )
    monkeypatch.setattr(
        "work_data_hub_pro.apps.orchestration.replay.lookup.load_replay_diagnostics",
        lambda run_id: load_replay_diagnostics(run_id, registry=registry),
    )
    lineage_path = replay_root / "evidence" / "comparison_runs" / comparison_run_id / "lineage-impact.json"
    lineage_path.write_text(json.dumps({"affected_anchor_rows": [7]}), encoding="utf-8")

    with pytest.raises(ReplayLookupError, match="malformed_lineage_package"):
        load_replay_lookup(comparison_run_id, record_id="record-001")

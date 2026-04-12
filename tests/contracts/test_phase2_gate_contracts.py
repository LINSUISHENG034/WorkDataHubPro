from __future__ import annotations

from dataclasses import asdict

from work_data_hub_pro.governance.compatibility.gate_models import (
    CheckpointDiff,
    CheckpointFingerprint,
    CheckpointResult,
    ComparisonRunManifest,
    GateSummary,
)
from work_data_hub_pro.governance.compatibility.gate_runtime import (
    write_comparison_run_package,
)
from work_data_hub_pro.governance.compatibility.models import CompatibilityCase
from work_data_hub_pro.governance.evidence_index.file_store import FileEvidenceIndex
from work_data_hub_pro.platform.contracts.publication import (
    PublicationMode,
    PublicationResult,
)


def test_checkpoint_result_fields() -> None:
    result = CheckpointResult(
        comparison_run_id="comparison-001",
        checkpoint_name="fact_processing",
        checkpoint_type="parity",
        status="failed",
        severity="block",
        legacy_fingerprint=CheckpointFingerprint(
            fingerprint="legacy-hash",
            row_count=1,
            metadata={"stage": "legacy"},
        ),
        pro_fingerprint=CheckpointFingerprint(
            fingerprint="pro-hash",
            row_count=2,
            metadata={"stage": "pro"},
        ),
        diff_path="comparison_runs/comparison-001/diffs/fact_processing.json",
        trace_anchor_rows=[2, 3],
        diff=CheckpointDiff(
            missing_rows=[{"record_id": "legacy-1"}],
            extra_rows=[{"record_id": "pro-1"}],
        ),
    )
    payload = asdict(result)

    assert payload["comparison_run_id"] == "comparison-001"
    assert payload["checkpoint_name"] == "fact_processing"
    assert payload["checkpoint_type"] == "parity"
    assert payload["status"] == "failed"
    assert payload["severity"] == "block"
    assert payload["legacy_fingerprint"]["fingerprint"] == "legacy-hash"
    assert payload["pro_fingerprint"]["row_count"] == 2
    assert payload["diff_path"].endswith("diffs/fact_processing.json")
    assert payload["trace_anchor_rows"] == [2, 3]


def test_manifest_package_paths(tmp_path) -> None:
    evidence_index = FileEvidenceIndex(tmp_path)
    comparison_run_id = "comparison-001"
    manifest = ComparisonRunManifest(
        comparison_run_id=comparison_run_id,
        domain="annuity_performance",
        period="2026-03",
        baseline_version="baseline-001",
        config_release_id="release-001",
        rule_pack_version="rules-001",
        decision_owner="compat-owner",
        package_root="comparison_runs/comparison-001",
        package_paths={
            "manifest": "comparison_runs/comparison-001/manifest.json",
            "gate_summary": "comparison_runs/comparison-001/gate-summary.json",
            "checkpoint_results": "comparison_runs/comparison-001/checkpoint-results.json",
            "source_intake_adaptation": "comparison_runs/comparison-001/source-intake-adaptation.json",
            "lineage_impact": "comparison_runs/comparison-001/lineage-impact.json",
            "publication_results": "comparison_runs/comparison-001/publication-results.json",
            "compatibility_case": "comparison_runs/comparison-001/compatibility-case.json",
            "report": "comparison_runs/comparison-001/report.md",
            "fact_processing_diff": "comparison_runs/comparison-001/diffs/fact_processing.json",
        },
    )
    gate_summary = GateSummary(
        comparison_run_id=comparison_run_id,
        overall_outcome="failed",
        total_checkpoints=1,
        blocking_count=1,
        warning_count=0,
        passed_count=0,
        severity_counts={"block": 1, "warn": 0},
        status_counts={"failed": 1, "warning": 0, "passed": 0},
        checkpoint_statuses={"fact_processing": "failed"},
    )
    checkpoint_result = CheckpointResult(
        comparison_run_id=comparison_run_id,
        checkpoint_name="fact_processing",
        checkpoint_type="parity",
        status="failed",
        severity="block",
        legacy_fingerprint=CheckpointFingerprint(
            fingerprint="legacy-hash",
            row_count=1,
        ),
        pro_fingerprint=CheckpointFingerprint(
            fingerprint="pro-hash",
            row_count=2,
        ),
        diff_path="comparison_runs/comparison-001/diffs/fact_processing.json",
        trace_anchor_rows=[2],
    )
    compatibility_case = CompatibilityCase(
        case_id="compat-001",
        sample_locator="reference/historical_replays/annuity_performance/legacy_monthly_snapshot_2026_03.json",
        legacy_result={"rows": [{"record_id": "legacy-1"}]},
        pro_result={"rows": [{"record_id": "pro-1"}]},
        severity="block",
        decision_status="pending_review",
        precedent_status="none",
        precedent_key=None,
        expires_at=None,
        checkpoint_name="fact_processing",
        comparison_run_id=comparison_run_id,
        business_rationale="Replay differs from accepted baseline",
        approved_by=None,
        affected_rule_version="annuity-performance-core:1",
        involved_anchor_row_nos=[2],
    )

    package_paths = write_comparison_run_package(
        evidence_index=evidence_index,
        manifest=manifest,
        gate_summary=gate_summary,
        checkpoint_results=[checkpoint_result],
        checkpoint_diffs={
            "fact_processing": CheckpointDiff(
                missing_rows=[{"record_id": "legacy-1"}],
                extra_rows=[{"record_id": "pro-1"}],
            )
        },
        source_intake_adaptation={"ignored_columns": ["legacy_extra"]},
        lineage_impact={"affected_anchor_rows": [2]},
        publication_results=[
            PublicationResult(
                publication_id="publication-001",
                target_name="contract_state",
                mode=PublicationMode.REFRESH,
                affected_rows=1,
                transaction_group="contract-state",
                success=True,
            )
        ],
        compatibility_case=compatibility_case,
        report_markdown="# Comparison Report\n",
    )

    assert package_paths["manifest"].name == "manifest.json"
    assert package_paths["gate_summary"].name == "gate-summary.json"
    assert package_paths["checkpoint_results"].name == "checkpoint-results.json"
    assert package_paths["source_intake_adaptation"].name == "source-intake-adaptation.json"
    assert package_paths["lineage_impact"].name == "lineage-impact.json"
    assert package_paths["publication_results"].name == "publication-results.json"
    assert package_paths["compatibility_case"].name == "compatibility-case.json"
    assert package_paths["report"].name == "report.md"
    assert package_paths["checkpoint_diffs"]["fact_processing"].name == "fact_processing.json"
    for path in package_paths.values():
        if isinstance(path, dict):
            for nested_path in path.values():
                assert nested_path.exists()
        else:
            assert path.exists()


def test_compatibility_case_phase2_fields() -> None:
    case = CompatibilityCase(
        case_id="compat-001",
        sample_locator="reference/sample.json",
        legacy_result={"rows": []},
        pro_result={"rows": []},
        severity="warn",
        decision_status="approved_exception",
        precedent_status="candidate",
        precedent_key="fact_processing:sample",
        expires_at="2026-12-31T00:00:00Z",
        checkpoint_name="fact_processing",
        comparison_run_id="comparison-001",
        business_rationale="Reviewed mismatch",
        approved_by="qa-owner",
        affected_rule_version="rule-pack:1",
        involved_anchor_row_nos=[2, 3],
    )

    assert case.severity == "warn"
    assert case.decision_status == "approved_exception"
    assert case.precedent_status == "candidate"
    assert case.precedent_key == "fact_processing:sample"
    assert case.expires_at == "2026-12-31T00:00:00Z"
    assert case.checkpoint_name == "fact_processing"
    assert case.comparison_run_id == "comparison-001"

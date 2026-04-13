from __future__ import annotations

from pathlib import Path

import pytest

from work_data_hub_pro.apps.orchestration.replay.contracts import ReplayDomainSpec
from work_data_hub_pro.apps.orchestration.replay.diagnostics import (
    find_comparison_run_root,
    load_replay_diagnostics,
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
    for domain in ("annuity_performance", "annual_award", "annual_loss"):
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


def _write_package(
    *,
    replay_root: Path,
    comparison_run_id: str,
    status: str,
    severity: str,
    compatibility_case: CompatibilityCase | None,
) -> None:
    evidence_index = FileEvidenceIndex(replay_root / "evidence")
    checkpoint_result = CheckpointResult(
        comparison_run_id=comparison_run_id,
        checkpoint_name="monthly_snapshot",
        checkpoint_type="parity",
        status=status,
        severity=severity,
        legacy_fingerprint=CheckpointFingerprint(
            fingerprint="legacy-hash",
            row_count=1,
        ),
        pro_fingerprint=CheckpointFingerprint(
            fingerprint="pro-hash" if status != "passed" else "legacy-hash",
            row_count=1,
        ),
        diff_path=f"comparison_runs/{comparison_run_id}/diffs/monthly_snapshot.json",
        trace_anchor_rows=[1],
    )
    gate_summary = GateSummary(
        comparison_run_id=comparison_run_id,
        overall_outcome="failed" if status == "failed" else status,
        total_checkpoints=1,
        blocking_count=1 if status == "failed" else 0,
        warning_count=1 if status == "warning" else 0,
        passed_count=1 if status == "passed" else 0,
        severity_counts={
            "block": 1 if severity == "block" and status != "passed" else 0,
            "warn": 1 if severity == "warn" and status != "passed" else 0,
        },
        status_counts={
            "failed": 1 if status == "failed" else 0,
            "warning": 1 if status == "warning" else 0,
            "passed": 1 if status == "passed" else 0,
        },
        checkpoint_statuses={"monthly_snapshot": status},
    )
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

    write_comparison_run_package(
        evidence_index=evidence_index,
        manifest=manifest,
        gate_summary=gate_summary,
        checkpoint_results=[checkpoint_result],
        checkpoint_diffs={},
        source_intake_adaptation={"records": []},
        lineage_impact={"affected_anchor_rows": [1]},
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


@pytest.mark.parametrize(
    ("status", "severity", "expected_outcome", "expects_primary_failure"),
    [
        ("passed", "block", "passed", False),
        ("warning", "warn", "warning", True),
    ],
)
def test_load_replay_diagnostics_handles_completed_runs_without_real_case(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    status: str,
    severity: str,
    expected_outcome: str,
    expects_primary_failure: bool,
) -> None:
    registry = _registry_for(tmp_path)
    comparison_run_id = f"annual-award-2026-03-{status}"
    _write_package(
        replay_root=registry["annual_award"].replay_root,
        comparison_run_id=comparison_run_id,
        status=status,
        severity=severity,
        compatibility_case=None,
    )

    off_root = tmp_path / "different-cwd"
    off_root.mkdir()
    monkeypatch.chdir(off_root)

    domain, comparison_run_root = find_comparison_run_root(
        comparison_run_id,
        registry=registry,
    )
    diagnostics = load_replay_diagnostics(
        comparison_run_id,
        registry=registry,
    )

    assert domain == "annual_award"
    assert comparison_run_root == (
        registry["annual_award"].replay_root
        / "evidence"
        / "comparison_runs"
        / comparison_run_id
    )
    assert diagnostics.domain == "annual_award"
    assert diagnostics.comparison_run_root == comparison_run_root
    assert diagnostics.manifest.comparison_run_id == comparison_run_id
    assert diagnostics.gate_summary.overall_outcome == expected_outcome
    assert diagnostics.report.comparison_run_id == comparison_run_id
    assert diagnostics.report.overall_outcome == expected_outcome
    assert diagnostics.compatibility_case is None
    assert diagnostics.report.compatibility_case is None
    assert diagnostics.report.evidence_paths.compatibility_case is None
    assert diagnostics.publication_results[0].mode is PublicationMode.REFRESH
    assert diagnostics.report_markdown == "# Comparison Report\n"
    if expects_primary_failure:
        assert diagnostics.report.primary_failure is not None
        assert diagnostics.report.primary_failure.checkpoint_name == "monthly_snapshot"
        assert diagnostics.report.primary_failure.status == status
    else:
        assert diagnostics.report.primary_failure is None


def test_load_replay_diagnostics_handles_failed_run_with_real_case(
    tmp_path: Path,
) -> None:
    registry = _registry_for(tmp_path)
    comparison_run_id = "annual-loss-2026-03-failed"
    compatibility_case = CompatibilityCase(
        case_id="compat-001",
        sample_locator="reference/historical_replays/annual_loss/sample.json",
        legacy_result={"rows": [{"record_id": "legacy-1"}]},
        pro_result={"rows": [{"record_id": "pro-1"}]},
        business_rationale="monthly_snapshot replay differs from accepted legacy baseline",
        affected_rule_version="annual-loss-core:1",
        checkpoint_name="monthly_snapshot",
        comparison_run_id=comparison_run_id,
        involved_anchor_row_nos=[1],
    )
    _write_package(
        replay_root=registry["annual_loss"].replay_root,
        comparison_run_id=comparison_run_id,
        status="failed",
        severity="block",
        compatibility_case=compatibility_case,
    )

    diagnostics = load_replay_diagnostics(
        comparison_run_id,
        registry=registry,
    )

    assert diagnostics.domain == "annual_loss"
    assert diagnostics.compatibility_case is not None
    assert diagnostics.compatibility_case.case_id == "compat-001"
    assert diagnostics.report.compatibility_case is not None
    assert diagnostics.report.compatibility_case.case_id == "compat-001"
    assert diagnostics.report.primary_failure is not None
    assert diagnostics.report.primary_failure.compatibility_case_id == "compat-001"
    assert diagnostics.report.primary_failure.diff_path == (
        f"comparison_runs/{comparison_run_id}/diffs/monthly_snapshot.json"
    )
    assert diagnostics.report.evidence_paths.compatibility_case is not None


def test_find_comparison_run_root_rejects_path_separators(tmp_path: Path) -> None:
    registry = _registry_for(tmp_path)

    with pytest.raises(ValueError, match="comparison_run_id"):
        find_comparison_run_root("../escape", registry=registry)


def test_load_replay_diagnostics_raises_for_missing_run(tmp_path: Path) -> None:
    registry = _registry_for(tmp_path)

    with pytest.raises(FileNotFoundError, match="missing-run"):
        load_replay_diagnostics("missing-run", registry=registry)

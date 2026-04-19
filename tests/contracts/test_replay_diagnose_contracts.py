from __future__ import annotations

import json
from pathlib import Path

import pytest
from typer.testing import CliRunner

from work_data_hub_pro.apps.etl_cli import main as cli_main
from work_data_hub_pro.apps.orchestration.replay.contracts import ReplayDomainSpec
from work_data_hub_pro.apps.orchestration.replay.diagnostics import (
    find_comparison_run_root,
    load_replay_diagnostics,
)
from work_data_hub_pro.apps.orchestration.replay.errors import (
    ReplayDiagnosticsNotFoundError,
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
        decision_owner=None,
        resolution_note=None,
        closure_evidence=[],
        closed_at=None,
        closed_by=None,
        resolved_outcome=None,
        decision_history=[],
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


def test_replay_diagnose_cli_returns_machine_readable_output(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    runner = CliRunner()
    registry = _registry_for(tmp_path)
    comparison_run_id = "annual-award-2026-03-warning"
    _write_package(
        replay_root=registry["annual_award"].replay_root,
        comparison_run_id=comparison_run_id,
        status="warning",
        severity="warn",
        compatibility_case=None,
    )

    monkeypatch.setattr(
        cli_main,
        "load_replay_diagnostics",
        lambda run_id: load_replay_diagnostics(run_id, registry=registry),
    )

    result = runner.invoke(
        cli_main.app,
        ["replay", "diagnose", "--comparison-run-id", comparison_run_id],
    )

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["comparison_run_id"] == comparison_run_id
    assert payload["overall_outcome"] == "warning"
    assert payload["primary_failed_checkpoint"] == "monthly_snapshot"
    assert payload["compatibility_case_id"] is None
    assert payload["checkpoint_statuses"]["monthly_snapshot"] == "warning"
    assert payload["package_paths"]["manifest"].endswith("manifest.json")


def test_replay_diagnose_cli_returns_typed_missing_run_error(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    runner = CliRunner()
    registry = _registry_for(tmp_path)

    monkeypatch.setattr(
        cli_main,
        "load_replay_diagnostics",
        lambda run_id: load_replay_diagnostics(run_id, registry=registry),
    )

    result = runner.invoke(
        cli_main.app,
        ["replay", "diagnose", "--comparison-run-id", "missing-run"],
    )

    assert result.exit_code == 1
    assert "Replay diagnostics package was not found for missing-run." in result.stderr


# =============================================================================
# Path-escape and invalid-id hardening tests (03.1-02)
# =============================================================================

def _write_escaping_manifest_package(
    *,
    replay_root: Path,
    comparison_run_id: str,
    escaping_package_paths: dict[str, str],
) -> None:
    """Write a comparison-run package whose manifest contains escaping package_paths."""
    from work_data_hub_pro.governance.compatibility.gate_models import (
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
        package_paths=escaping_package_paths,
    )
    checkpoint_result = CheckpointResult(
        comparison_run_id=comparison_run_id,
        checkpoint_name="monthly_snapshot",
        checkpoint_type="parity",
        status="failed",
        severity="block",
        legacy_fingerprint=CheckpointFingerprint(
            fingerprint="legacy-hash",
            row_count=1,
        ),
        pro_fingerprint=CheckpointFingerprint(
            fingerprint="pro-hash",
            row_count=1,
        ),
        diff_path=f"comparison_runs/{comparison_run_id}/diffs/monthly_snapshot.json",
        trace_anchor_rows=[1],
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
        checkpoint_statuses={"monthly_snapshot": "failed"},
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
        compatibility_case=None,
        report_markdown="# Comparison Report\n",
    )


def test_load_replay_diagnostics_rejects_absolute_manifest_package_paths(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Diagnose loader must reject manifests whose package_paths are absolute paths."""
    registry = _registry_for(tmp_path)
    comparison_run_id = "escape-abs-2026-03"
    replay_root = registry["annual_award"].replay_root

    # Craft a manifest whose gate_summary package_path is an absolute path
    escaping_paths = {
        "manifest": f"comparison_runs/{comparison_run_id}/manifest.json",
        "gate_summary": "/tmp/evil-gate-summary.json",  # absolute — MUST be rejected
        "checkpoint_results": f"comparison_runs/{comparison_run_id}/checkpoint-results.json",
        "source_intake_adaptation": f"comparison_runs/{comparison_run_id}/source-intake-adaptation.json",
        "lineage_impact": f"comparison_runs/{comparison_run_id}/lineage-impact.json",
        "publication_results": f"comparison_runs/{comparison_run_id}/publication-results.json",
        "compatibility_case": f"comparison_runs/{comparison_run_id}/compatibility-case.json",
        "report": f"comparison_runs/{comparison_run_id}/report.md",
    }
    _write_escaping_manifest_package(
        replay_root=replay_root,
        comparison_run_id=comparison_run_id,
        escaping_package_paths=escaping_paths,
    )

    off_root = tmp_path / "different-cwd"
    off_root.mkdir()
    monkeypatch.chdir(off_root)

    with pytest.raises(ValueError, match="package_paths"):
        load_replay_diagnostics(comparison_run_id, registry=registry)


def test_load_replay_diagnostics_rejects_escaping_manifest_package_paths(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Diagnose loader must reject manifests whose package_paths escape the run package."""
    registry = _registry_for(tmp_path)
    comparison_run_id = "escape-rel-2026-03"
    replay_root = registry["annual_loss"].replay_root

    # Craft a manifest whose checkpoint_results package_path escapes via ../
    escaping_paths = {
        "manifest": f"comparison_runs/{comparison_run_id}/manifest.json",
        "gate_summary": f"comparison_runs/{comparison_run_id}/gate-summary.json",
        "checkpoint_results": f"comparison_runs/{comparison_run_id}/../../outside/checkpoint-results.json",
        "source_intake_adaptation": f"comparison_runs/{comparison_run_id}/source-intake-adaptation.json",
        "lineage_impact": f"comparison_runs/{comparison_run_id}/lineage-impact.json",
        "publication_results": f"comparison_runs/{comparison_run_id}/publication-results.json",
        "compatibility_case": f"comparison_runs/{comparison_run_id}/compatibility-case.json",
        "report": f"comparison_runs/{comparison_run_id}/report.md",
    }
    _write_escaping_manifest_package(
        replay_root=replay_root,
        comparison_run_id=comparison_run_id,
        escaping_package_paths=escaping_paths,
    )

    off_root = tmp_path / "different-cwd"
    off_root.mkdir()
    monkeypatch.chdir(off_root)

    with pytest.raises(ValueError, match="package_paths"):
        load_replay_diagnostics(comparison_run_id, registry=registry)


def test_replay_diagnose_cli_returns_typed_invalid_id_error(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """CLI must emit a typed error (no traceback) for invalid comparison_run_id values."""
    runner = CliRunner()
    registry = _registry_for(tmp_path)

    monkeypatch.setattr(
        cli_main,
        "load_replay_diagnostics",
        lambda run_id: load_replay_diagnostics(run_id, registry=registry),
    )

    result = runner.invoke(
        cli_main.app,
        ["replay", "diagnose", "--comparison-run-id", "../evil"],
    )

    assert result.exit_code == 1
    assert "Invalid comparison_run_id: ../evil" in result.stderr
    # Ensure no Python traceback leaked
    assert "Traceback" not in result.stderr
    assert "raise ValueError" not in result.stderr

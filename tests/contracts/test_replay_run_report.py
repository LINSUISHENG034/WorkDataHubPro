from __future__ import annotations

from dataclasses import asdict
from pathlib import Path

from work_data_hub_pro.apps.orchestration.replay.contracts import (
    ReplayEvidencePaths,
    ReplayPrimaryFailure,
    ReplayRunReport,
)
from work_data_hub_pro.apps.orchestration.replay.registry import REPLAY_DOMAINS, REPO_ROOT
from work_data_hub_pro.governance.compatibility.gate_models import (
    CheckpointFingerprint,
    CheckpointResult,
)


def test_replay_run_report_serializes_required_fields() -> None:
    checkpoint_result = CheckpointResult(
        comparison_run_id="annual-award-2026-03-001",
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
            row_count=2,
        ),
        diff_path="comparison_runs/annual-award-2026-03-001/diffs/monthly_snapshot.json",
        trace_anchor_rows=[1, 2],
    )
    report = ReplayRunReport(
        comparison_run_id="annual-award-2026-03-001",
        overall_outcome="failed",
        checkpoint_results=[checkpoint_result],
        primary_failure=ReplayPrimaryFailure(
            checkpoint_name="monthly_snapshot",
            status="failed",
            severity="block",
            message="monthly_snapshot replay differs from accepted legacy baseline",
            diff_path=checkpoint_result.diff_path,
            compatibility_case_id="compat-001",
        ),
        compatibility_case=None,
        evidence_paths=ReplayEvidencePaths(
            evidence_root="reference/historical_replays/annual_award/evidence",
            comparison_run_root=(
                "reference/historical_replays/annual_award/evidence/"
                "comparison_runs/annual-award-2026-03-001"
            ),
            manifest=(
                "reference/historical_replays/annual_award/evidence/"
                "comparison_runs/annual-award-2026-03-001/manifest.json"
            ),
            gate_summary=(
                "reference/historical_replays/annual_award/evidence/"
                "comparison_runs/annual-award-2026-03-001/gate-summary.json"
            ),
            checkpoint_results=(
                "reference/historical_replays/annual_award/evidence/"
                "comparison_runs/annual-award-2026-03-001/checkpoint-results.json"
            ),
            source_intake_adaptation=(
                "reference/historical_replays/annual_award/evidence/"
                "comparison_runs/annual-award-2026-03-001/source-intake-adaptation.json"
            ),
            lineage_impact=(
                "reference/historical_replays/annual_award/evidence/"
                "comparison_runs/annual-award-2026-03-001/lineage-impact.json"
            ),
            publication_results=(
                "reference/historical_replays/annual_award/evidence/"
                "comparison_runs/annual-award-2026-03-001/publication-results.json"
            ),
            report=(
                "reference/historical_replays/annual_award/evidence/"
                "comparison_runs/annual-award-2026-03-001/report.md"
            ),
            compatibility_case=None,
        ),
    )

    payload = asdict(report)

    assert set(payload) == {
        "comparison_run_id",
        "overall_outcome",
        "checkpoint_results",
        "primary_failure",
        "compatibility_case",
        "evidence_paths",
    }
    assert payload["primary_failure"]["checkpoint_name"] == "monthly_snapshot"
    assert payload["primary_failure"]["compatibility_case_id"] == "compat-001"
    assert payload["compatibility_case"] is None
    assert payload["evidence_paths"]["report"].endswith("report.md")


def test_replay_domain_registry_exposes_stable_metadata() -> None:
    expected = {
        "annuity_performance": {
            "wrapper_command": "replay-annuity-performance",
            "replay_root": Path("reference/historical_replays/annuity_performance"),
            "runbook_path": Path("docs/runbooks/annuity-performance-replay.md"),
            "release_path": Path(
                "config/releases/2026-04-11-annuity-performance-baseline.json"
            ),
            "domain_config_path": Path("config/domains/annuity_performance/cleansing.json"),
            "runner_import": (
                "work_data_hub_pro.apps.orchestration.replay."
                "annuity_performance_slice:run_annuity_performance_slice"
            ),
        },
        "annual_award": {
            "wrapper_command": "replay-annual-award",
            "replay_root": Path("reference/historical_replays/annual_award"),
            "runbook_path": Path("docs/runbooks/annual-award-replay.md"),
            "release_path": Path("config/releases/2026-04-11-annual-award-baseline.json"),
            "domain_config_path": Path("config/domains/annual_award/cleansing.json"),
            "runner_import": (
                "work_data_hub_pro.apps.orchestration.replay."
                "annual_award_slice:run_annual_award_slice"
            ),
        },
        "annual_loss": {
            "wrapper_command": "replay-annual-loss",
            "replay_root": Path("reference/historical_replays/annual_loss"),
            "runbook_path": Path("docs/runbooks/annual-loss-replay.md"),
            "release_path": Path("config/releases/2026-04-12-annual-loss-baseline.json"),
            "domain_config_path": Path("config/domains/annual_loss/cleansing.json"),
            "runner_import": (
                "work_data_hub_pro.apps.orchestration.replay."
                "annual_loss_slice:run_annual_loss_slice"
            ),
        },
        "annuity_income": {
            "wrapper_command": "replay-annuity-income",
            "replay_root": Path("reference/historical_replays/annuity_income"),
            "runbook_path": Path("docs/runbooks/annuity-income-replay.md"),
            "release_path": Path("config/releases/2026-04-14-annuity-income-baseline.json"),
            "domain_config_path": Path("config/domains/annuity_income/cleansing.json"),
            "runner_import": (
                "work_data_hub_pro.apps.orchestration.replay."
                "annuity_income_slice:run_annuity_income_slice"
            ),
        },
    }

    assert set(REPLAY_DOMAINS) == set(expected)

    for domain, expected_spec in expected.items():
        spec = REPLAY_DOMAINS[domain]

        assert spec.wrapper_command == expected_spec["wrapper_command"]
        assert spec.replay_root == REPO_ROOT / expected_spec["replay_root"]
        assert spec.runbook_path == REPO_ROOT / expected_spec["runbook_path"]
        assert spec.release_path == REPO_ROOT / expected_spec["release_path"]
        assert spec.domain_config_path == REPO_ROOT / expected_spec["domain_config_path"]
        assert spec.runner_import == expected_spec["runner_import"]
        assert spec.replay_root.is_absolute()
        assert spec.runbook_path.is_absolute()
        assert spec.release_path.is_absolute()
        assert spec.domain_config_path.is_absolute()

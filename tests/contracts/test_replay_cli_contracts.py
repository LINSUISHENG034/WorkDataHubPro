from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

from typer.testing import CliRunner

from work_data_hub_pro.apps.etl_cli import main as cli_main
from work_data_hub_pro.apps.orchestration.replay.contracts import (
    ReplayDomainSpec,
    ReplayEvidencePaths,
    ReplayRunReport,
)


def _registry_for(tmp_path: Path) -> dict[str, ReplayDomainSpec]:
    registry: dict[str, ReplayDomainSpec] = {}
    for domain in ("annuity_performance", "annual_award", "annual_loss", "annuity_income"):
        replay_root = tmp_path / "reference" / domain
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


def _fake_outcome() -> SimpleNamespace:
    return SimpleNamespace(
        run_report=ReplayRunReport(
            comparison_run_id="annual-award-2026-03-pass",
            overall_outcome="passed",
            checkpoint_results=[],
            primary_failure=None,
            compatibility_case=None,
            evidence_paths=ReplayEvidencePaths(
                evidence_root="reference/historical_replays/annual_award/evidence",
                comparison_run_root=(
                    "reference/historical_replays/annual_award/evidence/"
                    "comparison_runs/annual-award-2026-03-pass"
                ),
                manifest=(
                    "reference/historical_replays/annual_award/evidence/"
                    "comparison_runs/annual-award-2026-03-pass/manifest.json"
                ),
                gate_summary=(
                    "reference/historical_replays/annual_award/evidence/"
                    "comparison_runs/annual-award-2026-03-pass/gate-summary.json"
                ),
                checkpoint_results=(
                    "reference/historical_replays/annual_award/evidence/"
                    "comparison_runs/annual-award-2026-03-pass/checkpoint-results.json"
                ),
                source_intake_adaptation=(
                    "reference/historical_replays/annual_award/evidence/"
                    "comparison_runs/annual-award-2026-03-pass/source-intake-adaptation.json"
                ),
                lineage_impact=(
                    "reference/historical_replays/annual_award/evidence/"
                    "comparison_runs/annual-award-2026-03-pass/lineage-impact.json"
                ),
                publication_results=(
                    "reference/historical_replays/annual_award/evidence/"
                    "comparison_runs/annual-award-2026-03-pass/publication-results.json"
                ),
                report=(
                    "reference/historical_replays/annual_award/evidence/"
                    "comparison_runs/annual-award-2026-03-pass/report.md"
                ),
                compatibility_case=None,
            ),
        ),
        publication_results=[1, 2, 3, 4, 5],
        projection_results=[1, 2],
    )


def test_replay_wrapper_commands_and_nested_group_are_discoverable() -> None:
    runner = CliRunner()

    result = runner.invoke(cli_main.app, ["--help"])

    assert result.exit_code == 0
    assert "replay-annuity-performance" in result.stdout
    assert "replay-annual-award" in result.stdout
    assert "replay-annual-loss" in result.stdout
    assert "replay-annuity-income" in result.stdout
    assert "replay" in result.stdout

    replay_help = runner.invoke(cli_main.app, ["replay", "--help"])
    assert replay_help.exit_code == 0
    assert "list-domains" in replay_help.stdout
    assert "run" in replay_help.stdout


def test_replay_list_domains_contract(
    tmp_path: Path,
    monkeypatch,
) -> None:
    runner = CliRunner()
    registry = _registry_for(tmp_path)
    monkeypatch.setattr(cli_main, "REPLAY_DOMAINS", registry)

    result = runner.invoke(cli_main.app, ["replay", "list-domains"])

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert {entry["domain"] for entry in payload} == set(registry)
    assert set(payload[0]) == {
        "domain",
        "wrapper_command",
        "replay_root",
        "runbook_path",
        "release_path",
        "domain_config_path",
    }


def test_replay_run_outputs_machine_readable_summary(
    tmp_path: Path,
    monkeypatch,
) -> None:
    runner = CliRunner()
    registry = _registry_for(tmp_path)
    workbook = tmp_path / "annual_award.xlsx"
    workbook.write_text("placeholder", encoding="utf-8")

    monkeypatch.setattr(cli_main, "REPLAY_DOMAINS", registry)
    monkeypatch.setattr(cli_main, "_resolve_runner", lambda spec: lambda **kwargs: _fake_outcome())

    result = runner.invoke(
        cli_main.app,
        [
            "replay",
            "run",
            "--domain",
            "annual_award",
            "--workbook",
            str(workbook),
            "--period",
            "2026-03",
        ],
    )

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["comparison_run_id"] == "annual-award-2026-03-pass"
    assert payload["overall_outcome"] == "passed"
    assert payload["primary_failed_checkpoint"] is None
    assert payload["evidence_root"].endswith("annual_award/evidence")
    assert payload["compatibility_case_id"] is None

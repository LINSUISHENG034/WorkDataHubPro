from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from work_data_hub_pro.apps.etl_cli import main as cli_main
from work_data_hub_pro.apps.orchestration.replay.registry import REPLAY_DOMAINS, REPO_ROOT


CANONICAL_RUNBOOK = REPO_ROOT / "docs/runbooks/agent-maintenance-workflow.md"
REQUIRED_CANONICAL_STRINGS = [
    "Current bounded scope: annuity_performance, annual_award, annual_loss, annuity_income.",
    "Adding a brand-new domain is not a doc-only change; it requires updates to src/work_data_hub_pro/apps/orchestration/replay/registry.py, config/domains/<domain>/, config/releases/, reference/historical_replays/<domain>/, and docs/runbooks/<domain>-replay.md.",
    "## Add a source",
    "## Adjust a rule",
    "## Run verify",
    "## Inspect evidence",
    "## Compatibility case lifecycle",
    "## Manual verification checklist",
    "uv run python -m work_data_hub_pro.apps.etl_cli.main replay run --domain <domain> --workbook <path> --period <period>",
    "uv run python -m work_data_hub_pro.apps.etl_cli.main replay diagnose --comparison-run-id <id>",
    "uv run python -m work_data_hub_pro.apps.etl_cli.main replay lookup --comparison-run-id <id> --record-id <id>",
    "uv run python -m work_data_hub_pro.apps.etl_cli.main compatibility show-case --evidence-root <path> --case-id <id>",
    "uv run python -m work_data_hub_pro.apps.etl_cli.main compatibility transition-case --evidence-root <path> --case-id <id> --status <status> --owner <owner> --resolution-note <note>",
    "uv run python -m work_data_hub_pro.apps.etl_cli.main compatibility close-case --evidence-root <path> --case-id <id> --owner <owner> --resolution-note <note> --closure-evidence <path>",
]


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_registry_specs_reference_existing_paths() -> None:
    assert REPLAY_DOMAINS

    for domain, spec in REPLAY_DOMAINS.items():
        assert spec.runbook_path.is_file(), f"missing runbook_path for {domain}"
        assert spec.release_path.is_file(), f"missing release_path for {domain}"
        assert spec.domain_config_path.is_file(), f"missing domain_config_path for {domain}"


def test_cli_help_exposes_documented_lookup_and_compatibility_commands() -> None:
    runner = CliRunner()

    replay_help = runner.invoke(cli_main.app, ["replay", "--help"])
    compatibility_help = runner.invoke(cli_main.app, ["compatibility", "--help"])

    assert replay_help.exit_code == 0
    assert "lookup" in replay_help.stdout

    assert compatibility_help.exit_code == 0
    assert "show-case" in compatibility_help.stdout
    assert "transition-case" in compatibility_help.stdout
    assert "close-case" in compatibility_help.stdout


def test_agent_workflow_runbook_references_exact_commands() -> None:
    text = _read(CANONICAL_RUNBOOK)

    for expected in REQUIRED_CANONICAL_STRINGS:
        assert expected in text


def test_registered_domain_runbooks_reference_canonical_workflow() -> None:
    for domain, spec in REPLAY_DOMAINS.items():
        text = _read(spec.runbook_path)

        assert "agent-maintenance-workflow.md" in text, domain
        assert "replay diagnose --comparison-run-id" in text, domain
        assert "replay lookup --comparison-run-id" in text, domain
        assert "compatibility show-case" in text, domain
        assert "compatibility close-case" in text, domain

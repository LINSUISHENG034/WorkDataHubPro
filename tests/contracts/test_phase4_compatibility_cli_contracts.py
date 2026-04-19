from __future__ import annotations

import json
from pathlib import Path

import pytest
from typer.testing import CliRunner

from work_data_hub_pro.apps.etl_cli import main as cli_main
from work_data_hub_pro.governance.adjudication.service import AdjudicationError


class _StubCase:
    case_id = "compat-001"
    comparison_run_id = "comparison-001"
    severity = "warn"
    decision_owner = "compatibility-review"
    decision_status = "approved_exception"
    resolved_outcome = "approved_exception"
    closure_evidence = ["reference/compatibility/closure-proof.json"]
    closed_by = "compatibility-review"



def test_compatibility_commands_are_discoverable() -> None:
    runner = CliRunner()

    result = runner.invoke(cli_main.app, ["compatibility", "--help"])

    assert result.exit_code == 0
    assert "show-case" in result.stdout
    assert "transition-case" in result.stdout
    assert "close-case" in result.stdout



def test_compatibility_show_case_returns_machine_readable_json(monkeypatch) -> None:
    runner = CliRunner()

    class _Index:
        def __init__(self, root: Path) -> None:
            self.root = root

        def load_case(self, case_id: str):
            assert case_id == "compat-001"
            return _StubCase()

    monkeypatch.setattr(cli_main, "FileEvidenceIndex", _Index)

    result = runner.invoke(
        cli_main.app,
        [
            "compatibility",
            "show-case",
            "--evidence-root",
            "evidence-root",
            "--case-id",
            "compat-001",
        ],
    )

    assert result.exit_code == 0
    assert json.loads(result.stdout) == {
        "case_id": "compat-001",
        "comparison_run_id": "comparison-001",
        "severity": "warn",
        "decision_owner": "compatibility-review",
        "decision_status": "approved_exception",
        "resolved_outcome": "approved_exception",
        "closure_evidence": ["reference/compatibility/closure-proof.json"],
        "closed_by": "compatibility-review",
    }



def test_compatibility_show_case_returns_machine_readable_error_code_for_missing_case(
    monkeypatch,
) -> None:
    runner = CliRunner()

    class _Index:
        def __init__(self, root: Path) -> None:
            self.root = root

        def load_case(self, case_id: str):
            raise FileNotFoundError(case_id)

    monkeypatch.setattr(cli_main, "FileEvidenceIndex", _Index)

    result = runner.invoke(
        cli_main.app,
        [
            "compatibility",
            "show-case",
            "--evidence-root",
            "evidence-root",
            "--case-id",
            "missing-case",
        ],
    )

    assert result.exit_code == 1
    assert json.loads(result.stdout) == {"error": "case_not_found", "case_id": "missing-case"}



def test_compatibility_transition_case_returns_success_payload(monkeypatch) -> None:
    runner = CliRunner()

    class _Service:
        def transition_case(self, case_id: str, *, status: str, owner: str, resolution_note: str):
            assert case_id == "compat-001"
            assert status == "approved_exception"
            assert owner == "compatibility-review"
            assert resolution_note == "Reviewed and approved."
            return _StubCase()

    monkeypatch.setattr(cli_main, "_compatibility_service", lambda evidence_root: _Service())

    result = runner.invoke(
        cli_main.app,
        [
            "compatibility",
            "transition-case",
            "--evidence-root",
            "evidence-root",
            "--case-id",
            "compat-001",
            "--status",
            "approved_exception",
            "--owner",
            "compatibility-review",
            "--resolution-note",
            "Reviewed and approved.",
        ],
    )

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["case_id"] == "compat-001"
    assert payload["comparison_run_id"] == "comparison-001"
    assert payload["severity"] == "warn"
    assert payload["decision_owner"] == "compatibility-review"
    assert payload["decision_status"] == "approved_exception"
    assert payload["resolved_outcome"] == "approved_exception"
    assert payload["closure_evidence"] == ["reference/compatibility/closure-proof.json"]
    assert payload["closed_by"] == "compatibility-review"


@pytest.mark.parametrize(
    "code",
    [
        "missing_owner",
        "empty_resolution_note",
        "illegal_transition",
    ],
)
def test_compatibility_transition_case_returns_machine_readable_error_codes(
    monkeypatch,
    code: str,
) -> None:
    runner = CliRunner()

    class _Service:
        def transition_case(self, case_id: str, *, status: str, owner: str, resolution_note: str):
            raise AdjudicationError(code)

    monkeypatch.setattr(cli_main, "_compatibility_service", lambda evidence_root: _Service())

    result = runner.invoke(
        cli_main.app,
        [
            "compatibility",
            "transition-case",
            "--evidence-root",
            "evidence-root",
            "--case-id",
            "compat-001",
            "--status",
            "rejected_difference",
            "--owner",
            "compatibility-review",
            "--resolution-note",
            "Reviewed and rejected.",
        ],
    )

    assert result.exit_code == 1
    assert json.loads(result.stdout) == {"error": code, "case_id": "compat-001"}



def test_compatibility_close_case_returns_success_payload(monkeypatch) -> None:
    runner = CliRunner()

    class _Service:
        def close_case(self, case_id: str, *, owner: str, resolution_note: str, closure_evidence: list[str]):
            assert case_id == "compat-001"
            assert owner == "compatibility-review"
            assert resolution_note == "Closed with proof."
            assert closure_evidence == ["proof-a.json", "proof-b.json"]
            return _StubCase()

    monkeypatch.setattr(cli_main, "_compatibility_service", lambda evidence_root: _Service())

    result = runner.invoke(
        cli_main.app,
        [
            "compatibility",
            "close-case",
            "--evidence-root",
            "evidence-root",
            "--case-id",
            "compat-001",
            "--owner",
            "compatibility-review",
            "--resolution-note",
            "Closed with proof.",
            "--closure-evidence",
            "proof-a.json",
            "--closure-evidence",
            "proof-b.json",
        ],
    )

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["case_id"] == "compat-001"
    assert payload["resolved_outcome"] == "approved_exception"


@pytest.mark.parametrize(
    "code",
    [
        "missing_owner",
        "empty_resolution_note",
        "empty_closure_evidence",
        "illegal_transition",
    ],
)
def test_compatibility_close_case_returns_machine_readable_error_codes(
    monkeypatch,
    code: str,
) -> None:
    runner = CliRunner()

    class _Service:
        def close_case(self, case_id: str, *, owner: str, resolution_note: str, closure_evidence: list[str]):
            raise AdjudicationError(code)

    monkeypatch.setattr(cli_main, "_compatibility_service", lambda evidence_root: _Service())

    result = runner.invoke(
        cli_main.app,
        [
            "compatibility",
            "close-case",
            "--evidence-root",
            "evidence-root",
            "--case-id",
            "compat-001",
            "--owner",
            "compatibility-review",
            "--resolution-note",
            "Closed with proof.",
            "--closure-evidence",
            "proof-a.json",
        ],
    )

    assert result.exit_code == 1
    assert json.loads(result.stdout) == {"error": code, "case_id": "compat-001"}



def test_compatibility_help_exposes_expected_option_names() -> None:
    runner = CliRunner()

    show_help = runner.invoke(cli_main.app, ["compatibility", "show-case", "--help"])
    transition_help = runner.invoke(cli_main.app, ["compatibility", "transition-case", "--help"])
    close_help = runner.invoke(cli_main.app, ["compatibility", "close-case", "--help"])

    assert show_help.exit_code == 0
    assert "--evidence-root" in show_help.stdout
    assert "--case-id" in show_help.stdout

    assert transition_help.exit_code == 0
    assert "--evidence-root" in transition_help.stdout
    assert "--case-id" in transition_help.stdout
    assert "--status" in transition_help.stdout
    assert "approved_exception" in transition_help.stdout or "--status" in transition_help.stdout
    assert "--owner" in transition_help.stdout
    assert "--resolution-note" in transition_help.stdout

    assert close_help.exit_code == 0
    assert "--evidence-root" in close_help.stdout
    assert "--case-id" in close_help.stdout
    assert "--owner" in close_help.stdout
    assert "--resolution-note" in close_help.stdout
    assert "--closure-evidence" in close_help.stdout

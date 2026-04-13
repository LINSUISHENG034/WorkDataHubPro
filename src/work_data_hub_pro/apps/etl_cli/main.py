from __future__ import annotations

import json
from importlib import import_module
from pathlib import Path
from typing import Any, Callable

import typer

from work_data_hub_pro.apps.orchestration.replay.diagnostics import (
    load_replay_diagnostics,
)
from work_data_hub_pro.apps.orchestration.replay.errors import (
    ReplayDiagnosticsNotFoundError,
)
from work_data_hub_pro.apps.orchestration.replay.registry import REPLAY_DOMAINS


app = typer.Typer(help="WorkDataHubPro replay utilities")
replay_app = typer.Typer(help="Registry-backed replay commands")
app.add_typer(replay_app, name="replay")


def _domain_record(domain: str, spec) -> dict[str, str]:
    return {
        "domain": domain,
        "wrapper_command": spec.wrapper_command,
        "replay_root": str(spec.replay_root),
        "runbook_path": str(spec.runbook_path),
        "release_path": str(spec.release_path),
        "domain_config_path": str(spec.domain_config_path),
    }


def _resolve_runner(spec) -> Callable[..., Any]:
    module_name, function_name = spec.runner_import.split(":", maxsplit=1)
    module = import_module(module_name)
    return getattr(module, function_name)


def _execute_replay(
    *,
    domain: str,
    workbook: Path,
    period: str,
    replay_root: Path | None = None,
):
    spec = REPLAY_DOMAINS.get(domain)
    if spec is None:
        raise typer.BadParameter(f"Unsupported replay domain: {domain}")
    runner = _resolve_runner(spec)
    return runner(
        workbook=workbook,
        period=period,
        replay_root=replay_root or spec.replay_root,
    )


def _run_summary(outcome) -> dict[str, Any]:
    run_report = outcome.run_report
    return {
        "comparison_run_id": run_report.comparison_run_id,
        "overall_outcome": run_report.overall_outcome,
        "primary_failed_checkpoint": (
            run_report.primary_failure.checkpoint_name
            if run_report.primary_failure is not None
            else None
        ),
        "evidence_root": run_report.evidence_paths.evidence_root,
        "compatibility_case_id": (
            run_report.compatibility_case.case_id
            if run_report.compatibility_case is not None
            else None
        ),
        "publication_result_count": len(outcome.publication_results),
        "projection_result_count": len(outcome.projection_results),
    }


def _diagnostics_payload(diagnostics) -> dict[str, Any]:
    return {
        "comparison_run_id": diagnostics.report.comparison_run_id,
        "overall_outcome": diagnostics.report.overall_outcome,
        "primary_failed_checkpoint": (
            diagnostics.report.primary_failure.checkpoint_name
            if diagnostics.report.primary_failure is not None
            else None
        ),
        "evidence_root": diagnostics.report.evidence_paths.evidence_root,
        "compatibility_case_id": (
            diagnostics.compatibility_case.case_id
            if diagnostics.compatibility_case is not None
            else None
        ),
        "checkpoint_statuses": diagnostics.gate_summary.checkpoint_statuses,
        "package_paths": {
            "comparison_run_root": diagnostics.report.evidence_paths.comparison_run_root,
            "manifest": diagnostics.report.evidence_paths.manifest,
            "gate_summary": diagnostics.report.evidence_paths.gate_summary,
            "checkpoint_results": diagnostics.report.evidence_paths.checkpoint_results,
            "publication_results": diagnostics.report.evidence_paths.publication_results,
            "report": diagnostics.report.evidence_paths.report,
            "compatibility_case": diagnostics.report.evidence_paths.compatibility_case,
        },
    }


def _emit_json(payload: dict[str, Any]) -> None:
    typer.echo(json.dumps(payload, ensure_ascii=False))


def _emit_wrapper_summary(outcome) -> None:
    summary = _run_summary(outcome)
    typer.echo(f"comparison_run_id={summary['comparison_run_id']}")
    typer.echo(f"overall_outcome={summary['overall_outcome']}")
    typer.echo(f"publication_results={summary['publication_result_count']}")
    typer.echo(f"projection_results={summary['projection_result_count']}")
    typer.echo(f"compatibility_case={summary['compatibility_case_id'] is not None}")


@replay_app.command("list-domains")
def replay_list_domains() -> None:
    _emit_json(
        [
            _domain_record(domain, spec)
            for domain, spec in sorted(REPLAY_DOMAINS.items())
        ]
    )


@replay_app.command("run")
def replay_run(
    domain: str = typer.Option(..., "--domain"),
    workbook: Path = typer.Option(..., "--workbook"),
    period: str = typer.Option(..., "--period"),
    replay_root: Path | None = typer.Option(None, "--replay-root"),
) -> None:
    outcome = _execute_replay(
        domain=domain,
        workbook=workbook,
        period=period,
        replay_root=replay_root,
    )
    _emit_json(_run_summary(outcome))


@replay_app.command("diagnose")
def replay_diagnose(
    comparison_run_id: str = typer.Option(..., "--comparison-run-id"),
) -> None:
    try:
        diagnostics = load_replay_diagnostics(comparison_run_id)
    except ValueError as exc:
        typer.echo(f"Invalid comparison_run_id: {comparison_run_id}", err=True)
        raise typer.Exit(code=1) from exc
    except FileNotFoundError as exc:
        error = ReplayDiagnosticsNotFoundError(
            domain="unknown",
            stage="diagnostics_lookup",
            message=f"Replay diagnostics package was not found for {comparison_run_id}.",
            context={"comparison_run_id": comparison_run_id},
            original_exception_type=type(exc).__name__,
            original_exception_message=str(exc),
        )
        typer.echo(error.message, err=True)
        raise typer.Exit(code=1) from exc
    except ReplayDiagnosticsNotFoundError as exc:
        typer.echo(exc.message, err=True)
        raise typer.Exit(code=1)

    _emit_json(_diagnostics_payload(diagnostics))


@app.command("replay-annuity-performance")
def replay_annuity_performance(
    workbook: Path,
    period: str,
    replay_root: Path = Path("reference/historical_replays/annuity_performance"),
) -> None:
    outcome = _execute_replay(
        domain="annuity_performance",
        workbook=workbook,
        period=period,
        replay_root=replay_root,
    )
    _emit_wrapper_summary(outcome)


@app.command("replay-annual-award")
def replay_annual_award(
    workbook: Path,
    period: str,
    replay_root: Path = Path("reference/historical_replays/annual_award"),
) -> None:
    outcome = _execute_replay(
        domain="annual_award",
        workbook=workbook,
        period=period,
        replay_root=replay_root,
    )
    _emit_wrapper_summary(outcome)


@app.command("replay-annual-loss")
def replay_annual_loss(
    workbook: Path,
    period: str,
    replay_root: Path = Path("reference/historical_replays/annual_loss"),
) -> None:
    outcome = _execute_replay(
        domain="annual_loss",
        workbook=workbook,
        period=period,
        replay_root=replay_root,
    )
    _emit_wrapper_summary(outcome)


if __name__ == "__main__":
    app()

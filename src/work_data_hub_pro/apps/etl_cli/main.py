from __future__ import annotations

from pathlib import Path

import typer

from work_data_hub_pro.apps.orchestration.replay.annual_award_slice import (
    run_annual_award_slice,
)
from work_data_hub_pro.apps.orchestration.replay.annual_loss_slice import (
    run_annual_loss_slice,
)
from work_data_hub_pro.apps.orchestration.replay.annuity_performance_slice import (
    run_annuity_performance_slice,
)


app = typer.Typer(help="WorkDataHubPro replay utilities")


@app.command("replay-annuity-performance")
def replay_annuity_performance(
    workbook: Path,
    period: str,
    replay_root: Path = Path("reference/historical_replays/annuity_performance"),
) -> None:
    outcome = run_annuity_performance_slice(
        workbook=workbook,
        period=period,
        replay_root=replay_root,
    )
    typer.echo(f"publication_results={len(outcome.publication_results)}")
    typer.echo(f"projection_results={len(outcome.projection_results)}")
    typer.echo(f"compatibility_case={outcome.compatibility_case is not None}")


@app.command("replay-annual-award")
def replay_annual_award(
    workbook: Path,
    period: str,
    replay_root: Path = Path("reference/historical_replays/annual_award"),
) -> None:
    outcome = run_annual_award_slice(
        workbook=workbook,
        period=period,
        replay_root=replay_root,
    )
    typer.echo(f"publication_results={len(outcome.publication_results)}")
    typer.echo(f"projection_results={len(outcome.projection_results)}")
    typer.echo(f"compatibility_case={outcome.compatibility_case is not None}")


@app.command("replay-annual-loss")
def replay_annual_loss(
    workbook: Path,
    period: str,
    replay_root: Path = Path("reference/historical_replays/annual_loss"),
) -> None:
    outcome = run_annual_loss_slice(
        workbook=workbook,
        period=period,
        replay_root=replay_root,
    )
    typer.echo(f"publication_results={len(outcome.publication_results)}")
    typer.echo(f"projection_results={len(outcome.projection_results)}")
    typer.echo(f"compatibility_case={outcome.compatibility_case is not None}")


if __name__ == "__main__":
    app()

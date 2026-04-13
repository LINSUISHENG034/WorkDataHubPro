from __future__ import annotations

from pathlib import Path

from work_data_hub_pro.apps.orchestration.replay.contracts import ReplayDomainSpec


REPO_ROOT = Path(__file__).resolve().parents[5]

REPLAY_DOMAINS: dict[str, ReplayDomainSpec] = {
    "annuity_performance": ReplayDomainSpec(
        wrapper_command="replay-annuity-performance",
        replay_root=REPO_ROOT / "reference/historical_replays/annuity_performance",
        runbook_path=REPO_ROOT / "docs/runbooks/annuity-performance-replay.md",
        release_path=REPO_ROOT / "config/releases/2026-04-11-annuity-performance-baseline.json",
        domain_config_path=REPO_ROOT / "config/domains/annuity_performance/cleansing.json",
        runner_import=(
            "work_data_hub_pro.apps.orchestration.replay."
            "annuity_performance_slice:run_annuity_performance_slice"
        ),
    ),
    "annual_award": ReplayDomainSpec(
        wrapper_command="replay-annual-award",
        replay_root=REPO_ROOT / "reference/historical_replays/annual_award",
        runbook_path=REPO_ROOT / "docs/runbooks/annual-award-replay.md",
        release_path=REPO_ROOT / "config/releases/2026-04-11-annual-award-baseline.json",
        domain_config_path=REPO_ROOT / "config/domains/annual_award/cleansing.json",
        runner_import=(
            "work_data_hub_pro.apps.orchestration.replay."
            "annual_award_slice:run_annual_award_slice"
        ),
    ),
    "annual_loss": ReplayDomainSpec(
        wrapper_command="replay-annual-loss",
        replay_root=REPO_ROOT / "reference/historical_replays/annual_loss",
        runbook_path=REPO_ROOT / "docs/runbooks/annual-loss-replay.md",
        release_path=REPO_ROOT / "config/releases/2026-04-12-annual-loss-baseline.json",
        domain_config_path=REPO_ROOT / "config/domains/annual_loss/cleansing.json",
        runner_import=(
            "work_data_hub_pro.apps.orchestration.replay."
            "annual_loss_slice:run_annual_loss_slice"
        ),
    ),
}


__all__ = ["REPLAY_DOMAINS", "REPO_ROOT"]

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from work_data_hub_pro.governance.compatibility.gate_models import CheckpointResult
from work_data_hub_pro.governance.compatibility.models import CompatibilityCase


@dataclass(frozen=True)
class ReplayPrimaryFailure:
    checkpoint_name: str
    status: str
    severity: str
    message: str
    diff_path: str | None
    compatibility_case_id: str | None = None


@dataclass(frozen=True)
class ReplayEvidencePaths:
    evidence_root: str
    comparison_run_root: str
    manifest: str
    gate_summary: str
    checkpoint_results: str
    source_intake_adaptation: str
    lineage_impact: str
    publication_results: str
    report: str
    compatibility_case: str | None = None


@dataclass(frozen=True)
class ReplayRunReport:
    comparison_run_id: str
    overall_outcome: str
    checkpoint_results: list[CheckpointResult]
    primary_failure: ReplayPrimaryFailure | None
    compatibility_case: CompatibilityCase | None
    evidence_paths: ReplayEvidencePaths


@dataclass(frozen=True)
class ReplayDomainSpec:
    wrapper_command: str
    replay_root: Path
    runbook_path: Path
    release_path: Path
    domain_config_path: Path
    runner_import: str


__all__ = [
    "ReplayDomainSpec",
    "ReplayEvidencePaths",
    "ReplayPrimaryFailure",
    "ReplayRunReport",
]

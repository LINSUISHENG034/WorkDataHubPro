from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
RUNBOOK_PATH = REPO_ROOT / "docs/runbooks/performance-verification-matrix.md"
DISPATCHER_PATH = REPO_ROOT / "scripts/run_perf_matrix.py"
BASELINE_ROOT = REPO_ROOT / "reference/perf-baselines"


def test_perf_matrix_runbook_references_exact_tiers() -> None:
    runbook = RUNBOOK_PATH.read_text(encoding="utf-8")

    assert "smoke" in runbook
    assert "standard" in runbook
    assert "large" in runbook
    assert "PR" in runbook
    assert "protected-branch" in runbook
    assert "nightly" in runbook
    assert "reference/perf-baselines" in runbook
    assert "scripts/run_perf_matrix.py --tier" in runbook


def test_perf_dispatcher_exposes_tier_options() -> None:
    dispatcher = DISPATCHER_PATH.read_text(encoding="utf-8")

    assert "--tier smoke" in dispatcher
    assert "--tier standard" in dispatcher
    assert "--tier large" in dispatcher


def test_perf_baseline_assets_use_relative_thresholds() -> None:
    for tier_name in ("smoke", "standard", "large"):
        baseline = json.loads(
            (BASELINE_ROOT / f"{tier_name}.json").read_text(encoding="utf-8")
        )

        assert baseline["tier"] == tier_name
        assert "threshold_ratio" in baseline
        assert isinstance(baseline["threshold_ratio"], (int, float))
        assert float(baseline["threshold_ratio"]) > 1.0
        assert "metrics" in baseline
        assert set(baseline["metrics"]) == {"p50", "p95", "peak_memory"}

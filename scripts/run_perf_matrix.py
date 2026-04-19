from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from statistics import median
from time import perf_counter


BASELINE_ROOT = Path("reference/perf-baselines")
DOCUMENTED_COMMANDS = {
    "smoke": "uv run pytest tests/integration/test_publication_service.py tests/performance/test_trace_lookup_micro_benchmark.py tests/performance/test_contract_state_projection_benchmark.py tests/contracts/test_perf_matrix_contracts.py -v",
    "standard": "uv run pytest tests/replay/test_annuity_performance_slice.py tests/replay/test_annual_award_slice.py tests/replay/test_annual_loss_slice.py tests/replay/test_annuity_performance_explainability_slo.py tests/replay/test_annual_award_explainability_slo.py tests/replay/test_annual_loss_explainability_slo.py -v",
    "large": "uv run pytest -v",
}
TIER_CONFIGS: dict[str, dict[str, object]] = {
    "smoke": {
        "baseline": BASELINE_ROOT / "smoke.json",
        "command": [
            sys.executable,
            "-m",
            "pytest",
            "tests/integration/test_publication_service.py",
            "tests/performance/test_trace_lookup_micro_benchmark.py",
            "tests/performance/test_contract_state_projection_benchmark.py",
            "tests/contracts/test_perf_matrix_contracts.py",
            "-v",
        ],
    },
    "standard": {
        "baseline": BASELINE_ROOT / "standard.json",
        "command": [
            sys.executable,
            "-m",
            "pytest",
            "tests/replay/test_annuity_performance_slice.py",
            "tests/replay/test_annual_award_slice.py",
            "tests/replay/test_annual_loss_slice.py",
            "tests/replay/test_annuity_performance_explainability_slo.py",
            "tests/replay/test_annual_award_explainability_slo.py",
            "tests/replay/test_annual_loss_explainability_slo.py",
            "-v",
        ],
    },
    "large": {
        "baseline": BASELINE_ROOT / "large.json",
        "command": [sys.executable, "-m", "pytest", "-v"],
    },
}


def load_baseline(tier: str) -> dict[str, object]:
    baseline_path = TIER_CONFIGS[tier]["baseline"]
    return json.loads(Path(baseline_path).read_text(encoding="utf-8"))


def _get_peak_memory_mb() -> float:
    try:
        import resource

        value = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
        if sys.platform == "darwin":
            return float(value) / (1024 * 1024)
        return float(value) / 1024
    except ImportError:
        completed = subprocess.run(
            [
                "powershell",
                "-NoProfile",
                "-Command",
                "(Get-Process -Id $PID).PeakWorkingSet64",
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        if completed.returncode != 0:
            return 0.0
        output = completed.stdout.strip()
        if not output:
            return 0.0
        return int(output) / (1024 * 1024)


def run_tier(tier: str) -> tuple[int, dict[str, float], list[str]]:
    config = TIER_CONFIGS[tier]
    command = [str(part) for part in config["command"]]
    display_command = str(DOCUMENTED_COMMANDS[tier])

    started = perf_counter()
    completed = subprocess.run(command, check=False)
    elapsed = perf_counter() - started
    metrics = {
        "p50": median([elapsed]),
        "p95": max([elapsed]),
        "peak_memory": _get_peak_memory_mb(),
    }
    return completed.returncode, metrics, [display_command]


def enforce_thresholds(tier: str, metrics: dict[str, float]) -> None:
    baseline = load_baseline(tier)
    threshold_ratio = float(baseline["threshold_ratio"])
    baseline_metrics = baseline["metrics"]

    failures: list[str] = []
    for metric_name in ("p50", "p95", "peak_memory"):
        actual = float(metrics[metric_name])
        baseline_value = float(baseline_metrics[metric_name])
        allowed = baseline_value * threshold_ratio
        if actual > allowed:
            failures.append(
                f"{metric_name} exceeded threshold: actual={actual:.6f} allowed={allowed:.6f}"
            )

    if failures:
        raise SystemExit("\n".join(failures))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--tier",
        choices=("smoke", "standard", "large"),
        required=True,
        help="Use --tier smoke, --tier standard, or --tier large.",
    )
    args = parser.parse_args()

    return_code, metrics, commands = run_tier(args.tier)
    for command in commands:
        print(command)
    print(json.dumps({"tier": args.tier, "metrics": metrics}, indent=2, sort_keys=True))

    if return_code != 0:
        return return_code

    enforce_thresholds(args.tier, metrics)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

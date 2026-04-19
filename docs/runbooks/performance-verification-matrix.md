# Performance Verification Matrix

## Scope

This runbook is the committed Phase 05 PERF-03 workload-tier matrix.
It binds the exact tiers `smoke`, `standard`, and `large` to one authoritative dispatcher, committed baselines under `reference/perf-baselines/`, and relative-threshold enforcement.

## Matrix

| Tier | Primary scope | Command | Cadence | Baseline | Threshold rule |
| --- | --- | --- | --- | --- | --- |
| smoke | Fast local and PR verification for publication and micro-benchmark coverage. | `uv run python scripts/run_perf_matrix.py --tier smoke` | PR | `reference/perf-baselines/smoke.json` | Relative thresholds only. Measured `p50`, `p95`, and `peak_memory` must not exceed `baseline * threshold_ratio`. |
| standard | Protected-branch replay acceptance coverage for the named Phase 05 slices. | `uv run python scripts/run_perf_matrix.py --tier standard` | protected-branch | `reference/perf-baselines/standard.json` | Relative thresholds only. Measured `p50`, `p95`, and `peak_memory` must not exceed `baseline * threshold_ratio`. |
| large | Nightly full-suite stress validation for repo-wide performance drift checks. | `uv run python scripts/run_perf_matrix.py --tier large` | nightly | `reference/perf-baselines/large.json` | Relative thresholds only. Measured `p50`, `p95`, and `peak_memory` must not exceed `baseline * threshold_ratio`. |

## Dispatcher Authority

`scripts/run_perf_matrix.py` is the authoritative local and CI dispatcher for this matrix.
Pytest markers are not the primary tier mechanism for PERF-03.

## Baseline Governance

- Baselines live under `reference/perf-baselines/`.
- Each baseline stores observed metric values for `p50`, `p95`, and `peak_memory`.
- Pass/fail uses relative thresholds against the committed baseline asset, not absolute gate milliseconds.
- Updating a baseline requires rerunning the tier on the current branch and reviewing whether the captured values remain operationally credible for the target cadence.

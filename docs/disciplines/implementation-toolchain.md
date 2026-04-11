# Implementation Toolchain Discipline

## Read This When

- setting up or refreshing the development environment
- changing `pyproject.toml`, `uv.lock`, or dependency workflow
- choosing how tests or replay commands should run
- stabilizing environment-specific warnings or test noise

## Do Not Read This When

- the task is about execution ordering or slice decomposition rather than tool usage
- the task is about git workflow rather than local runtime commands

## Hard Gates

- `uv` is the required package and environment manager for this repository
- commit `pyproject.toml` and `uv.lock` together when dependency state changes
- do not mix `uv` project workflows with ad hoc `pip install`, Poetry, or shell-specific environment setup

## 1. Required Command Style

- create or refresh the local environment: `uv sync --dev`
- run the full suite: `uv run pytest -v`
- run targeted tests: `uv run pytest tests/<path> -v`
- run the replay CLI: `uv run python -m work_data_hub_pro.apps.etl_cli.main ...`

## 2. Environment Stabilization Rule

When environment-specific noise appears repeatedly, stabilize it once at the
project boundary.

- prefer project configuration over repeated per-command workarounds
- fix noisy test-environment issues early if they degrade validation signal
- treat non-correctness warnings as secondary, but do not let them drown out real failures
- document non-obvious environment choices in committed docs when they become part of normal workflow

## 3. Toolchain Change Rule

If a toolchain assumption changes during execution:

1. stop implementation
2. update the governing plan
3. update the discipline doc if the change is durable
4. only then continue implementation

Toolchain changes are not housekeeping. They alter how every later step is
executed and verified.

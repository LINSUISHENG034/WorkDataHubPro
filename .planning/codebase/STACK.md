# Technology Stack

**Analysis Date:** 2026-04-12

## Languages

**Primary:**
- Python 3.12+ - Application and CLI implementation in `src/work_data_hub_pro/` with runtime contract in `pyproject.toml`.

**Secondary:**
- JSON - Domain/rule/policy configuration in `config/domains/`, `config/releases/`, and `config/policies/publication.json`.
- Markdown - Architecture, discipline, and runbook documentation in `docs/`.

## Runtime

**Environment:**
- CPython 3.12 or newer, declared in `pyproject.toml` (`requires-python = ">=3.12"`).

**Package Manager:**
- `uv` - Required workflow manager documented in `docs/disciplines/implementation-toolchain.md`.
- Lockfile: present (`uv.lock`).

## Frameworks

**Core:**
- `openpyxl` 3.1.5 - Excel workbook intake for source slices in:
  - `src/work_data_hub_pro/capabilities/source_intake/annuity_performance/service.py`
  - `src/work_data_hub_pro/capabilities/source_intake/annual_award/service.py`
  - `src/work_data_hub_pro/capabilities/source_intake/annual_loss/service.py`
- `typer` 0.24.1 - CLI entrypoint and commands in `src/work_data_hub_pro/apps/etl_cli/main.py`.

**Testing:**
- `pytest` 8.4.2 - Test runner configured in `pyproject.toml`; tests under `tests/contracts/`, `tests/integration/`, `tests/replay/`, and `tests/performance/`.

**Build/Dev:**
- `setuptools` (build backend `setuptools.build_meta`) - Packaging defined in `pyproject.toml`.
- `uv` - Environment sync and command execution (`uv sync --dev`, `uv run pytest -v`) defined in `docs/disciplines/implementation-toolchain.md`.

## Key Dependencies

**Critical:**
- `openpyxl` (`>=3.1,<4.0`, locked 3.1.5) - Required to load Excel sheet inputs from replay workbooks in source-intake services.
- `typer` (`>=0.12,<1.0`, locked 0.24.1) - Required for exposing replay commands in `src/work_data_hub_pro/apps/etl_cli/main.py`.

**Infrastructure:**
- `pytest` (`>=8.2,<9.0`, locked 8.4.2) - Verification boundary for contracts, integration, replay, and performance tests in `tests/`.
- `click`, `rich`, `shellingham` (transitive via `typer`, locked in `uv.lock`) - CLI UX/runtime support.

## Configuration

**Environment:**
- No runtime environment variables are read in current `src/work_data_hub_pro/` code paths (no `os.environ`/`getenv` usage detected).
- `.env*` files not detected at repository root during scan.

**Build:**
- `pyproject.toml` - project metadata, dependencies, package discovery, and pytest options.
- `uv.lock` - pinned dependency graph.
- `config/releases/*.json` - release-to-domain rule mapping (for example `config/releases/2026-04-11-annuity-performance-baseline.json`).
- `config/domains/*/cleansing.json` - domain cleansing rule-pack metadata.
- `config/policies/publication.json` - publication mode/idempotency policy for output targets.

## Platform Requirements

**Development:**
- `uv` installed and usable from shell; workflows in `docs/disciplines/implementation-toolchain.md`.
- Filesystem access to `reference/historical_replays/` assets and workbook inputs for replay commands.

**Production:**
- Deployment platform: Not detected.
- CI/CD runtime: Not detected in repository automation directories (`.github/` not present).

---

*Stack analysis: 2026-04-12*

# Coding Conventions

**Analysis Date:** 2026-04-12

## Naming Patterns

**Files:**
- Use `snake_case.py` for modules across `src/work_data_hub_pro/` and `tests/` (examples: `src/work_data_hub_pro/platform/publication/service.py`, `tests/integration/test_identity_resolution.py`).
- Use `test_*.py` for tests grouped by boundary directories (examples: `tests/contracts/test_system_contracts.py`, `tests/replay/test_annual_loss_slice.py`).

**Functions:**
- Use `snake_case` for functions and methods (examples: `run_annual_loss_slice` in `src/work_data_hub_pro/apps/orchestration/replay/annual_loss_slice.py`, `select_plan_code` in `src/work_data_hub_pro/capabilities/fact_processing/annual_loss/plan_code_lookup.py`).
- Use verb-first names for behavior (`read_batch`, `process`, `enrich`, `create_case`).

**Variables:**
- Use `snake_case` for locals, parameters, and fields (`anchor_row_no`, `config_release_id`, `trace_events` in `src/work_data_hub_pro/capabilities/identity_resolution/service.py`).
- Keep domain constants uppercase with underscores (`EVENT_BUSINESS_TYPE_MAPPING`, `PRODUCT_LINE_CODE_MAPPING` in `src/work_data_hub_pro/capabilities/fact_processing/cleansing/rules.py` and `src/work_data_hub_pro/capabilities/fact_processing/annual_loss/service.py`).

**Types:**
- Use `PascalCase` for classes/dataclasses (`CanonicalFactRecord`, `PublicationPlan`, `CompatibilityCase` in `src/work_data_hub_pro/platform/contracts/models.py`, `src/work_data_hub_pro/platform/contracts/publication.py`, `src/work_data_hub_pro/governance/compatibility/models.py`).
- Use protocol names as noun roles (`IdentityProvider`, `IdentityCache` in `src/work_data_hub_pro/capabilities/identity_resolution/interfaces.py`).

## Code Style

**Formatting:**
- Tool used: No formatter config detected in `pyproject.toml` (`[tool.black]`, `[tool.ruff]`, and `[tool.isort]` are not present).
- Key settings: Follow existing style in `src/work_data_hub_pro/`:
- 4-space indentation
- type hints on public APIs and most local collections
- `from __future__ import annotations` at file top in runtime modules (examples: `src/work_data_hub_pro/platform/storage/in_memory_tables.py`, `src/work_data_hub_pro/capabilities/source_intake/annual_award/service.py`)

**Linting:**
- Tool used: Not detected (`pyproject.toml` has no lint section).
- Key rules:
- Keep imports grouped as stdlib, third-party, internal with blank lines (example: `src/work_data_hub_pro/apps/etl_cli/main.py`).
- Prefer explicit immutable domain contracts via `@dataclass(frozen=True)` (examples in `src/work_data_hub_pro/platform/contracts/models.py` and `src/work_data_hub_pro/platform/contracts/publication.py`).

## Import Organization

**Order:**
1. Python stdlib (`dataclasses`, `datetime`, `pathlib`, `json`)
2. Third-party (`openpyxl`, `typer`)
3. Internal absolute imports from `work_data_hub_pro.*`

**Path Aliases:**
- No import aliases detected.
- Use absolute package imports rooted at `work_data_hub_pro` (examples throughout `src/work_data_hub_pro/apps/orchestration/replay/*.py`).

## Error Handling

**Patterns:**
- Use explicit fallback values instead of exceptions for transform/parsing operations:
- `normalize_event_date` returns `None` on invalid date parse in `src/work_data_hub_pro/capabilities/fact_processing/cleansing/rules.py`.
- Represent per-field processing failures in trace metadata (`success=False`, `error_message=...`) instead of raising in `src/work_data_hub_pro/capabilities/fact_processing/annuity_performance/service.py`, `src/work_data_hub_pro/capabilities/fact_processing/annual_award/service.py`, and `src/work_data_hub_pro/capabilities/fact_processing/annual_loss/service.py`.
- Raise `ValueError` for strict configuration integrity mismatches (`src/work_data_hub_pro/capabilities/fact_processing/cleansing/manifest.py`).

## Logging

**Framework:** Not used (`logging` module and logger setup are not present in `src/work_data_hub_pro/`).

**Patterns:**
- CLI-facing output is emitted through `typer.echo` in `src/work_data_hub_pro/apps/etl_cli/main.py`.
- Runtime services are side-effect-light and communicate diagnostics through returned models (`FieldTraceEvent`, `PublicationResult`) rather than log calls.

## Comments

**When to Comment:**
- Keep code largely self-describing; inline comments are rarely used in `src/work_data_hub_pro/`.
- Prefer expressive domain names and typed dataclasses over explanatory comments.

**JSDoc/TSDoc:**
- Not applicable (Python codebase).
- Python docstrings are minimal/not standard in current modules (examples: `src/work_data_hub_pro/capabilities/identity_resolution/service.py`, `src/work_data_hub_pro/platform/publication/service.py`).

## Function Design

**Size:** Keep functions focused on single pipeline steps (intake, process, enrich, publish) as in:
- `AnnualLossIntakeService.read_batch` in `src/work_data_hub_pro/capabilities/source_intake/annual_loss/service.py`
- `PublicationService.execute` in `src/work_data_hub_pro/platform/publication/service.py`

**Parameters:**
- Use keyword-only arguments for domain-critical inputs (`*` markers in `read_batch`, `resolve`, `enrich`, `build_publication_plan`).
- Pass typed contract objects (`InputRecord`, `CanonicalFactRecord`) between stages.

**Return Values:**
- Return immutable typed result objects (`ProcessingResult`, `IntakeResult`, `ResolvedFact`, `EnrichedLossFact`) rather than unstructured tuples.
- Include trace/evidence artifacts in return contracts where processing occurs (examples in `src/work_data_hub_pro/capabilities/*/service.py`).

## Module Design

**Exports:**
- Modules expose concrete classes/functions directly; there is minimal package-level re-exporting.
- Package-level export is limited to version metadata in `src/work_data_hub_pro/__init__.py`.

**Barrel Files:**
- Limited usage; `src/work_data_hub_pro/__init__.py` is a minimal barrel for `__version__`.
- Use direct module imports for runtime/test code instead of broad package barrels (examples in `tests/integration/test_publication_service.py`, `tests/replay/test_annuity_performance_slice.py`).

---

*Convention analysis: 2026-04-12*

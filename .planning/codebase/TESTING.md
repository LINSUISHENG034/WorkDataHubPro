# Testing Patterns

**Analysis Date:** 2026-04-12

## Test Framework

**Runner:**
- `pytest` (from `pyproject.toml` dependency group: `pytest>=8.2,<9.0`)
- Config: `pyproject.toml` (`[tool.pytest.ini_options] addopts = "--basetemp=.pytest_tmp"`)

**Assertion Library:**
- Native `assert` statements with pytest discovery (examples across `tests/contracts/test_system_contracts.py` and `tests/integration/test_identity_resolution.py`).

**Run Commands:**
```bash
uv run pytest -v                          # Run all tests
uv run pytest tests/<path> -v             # Run a focused subset (no dedicated watch command configured)
uv run pytest --cov=src --cov-report=term # Coverage command pattern (pytest-cov not declared in pyproject.toml)
```

## Test File Organization

**Location:**
- Separate test tree under `tests/`, split by boundary:
- `tests/contracts/`
- `tests/integration/`
- `tests/replay/`
- `tests/performance/`

**Naming:**
- Use `test_*.py` filenames and `test_*` function names.
- Keep domain/topic-specific test modules (examples: `tests/integration/test_annual_loss_plan_code_enrichment.py`, `tests/replay/test_annuity_performance_explainability_slo.py`).

**Structure:**
```text
tests/
  contracts/    # contract and governance/document invariants
  integration/  # multi-component service interactions
  replay/       # end-to-end replay slice behavior + evidence/SLO checks
  performance/  # micro-benchmarks with thresholds
```

## Test Structure

**Suite Organization:**
```python
def test_<behavior_description>() -> None:
    # Arrange: construct service/models/inputs
    # Act: execute a single entrypoint
    # Assert: verify state, outputs, and trace/evidence fields
```

**Patterns:**
- Setup pattern:
- Inline object construction with dataclasses and in-memory adapters (`tests/integration/test_publication_service.py`, `tests/contracts/test_trace_lineage_runtime.py`).
- Local helper builders for larger fixtures in same file (`_write_replay_assets`, `_write_workbook` in `tests/replay/test_annual_loss_slice.py`).
- Teardown pattern:
- Prefer `tmp_path` isolation; no explicit teardown hooks needed (`tests/replay/test_annual_award_slice.py`, `tests/integration/test_compatibility_adjudication.py`).
- Assertion pattern:
- Assert full ordered lists for stage outputs and modes.
- Assert specific trace fields/rule metadata (`stage_id`, `rule_id`, `value_before`, `value_after`) in integration/replay tests.

## Mocking

**Framework:** No dedicated mocking framework used (`unittest.mock`/`pytest-mock` not detected).

**Patterns:**
```python
service = CacheFirstIdentityResolutionService(
    cache=InMemoryIdentityCache({"ACME": "company-001"}),
    provider=StaticIdentityProvider({"BETA": "company-002"}),
)
```

```python
storage = InMemoryTableStore()
service = PublicationService(storage)
```

**What to Mock:**
- Prefer constructor-injected in-memory fakes/stubs defined in production code:
- `InMemoryIdentityCache` and `StaticIdentityProvider` from `src/work_data_hub_pro/capabilities/identity_resolution/service.py`
- `InMemoryTableStore` from `src/work_data_hub_pro/platform/storage/in_memory_tables.py`
- `InMemoryTraceStore` from `src/work_data_hub_pro/platform/tracing/in_memory_trace_store.py`

**What NOT to Mock:**
- Do not mock domain contracts (`CanonicalFactRecord`, `FieldTraceEvent` in `src/work_data_hub_pro/platform/contracts/models.py`); create real instances.
- Do not mock replay artifacts; build real temporary workbooks/JSON files under `tmp_path` (`tests/replay/test_annuity_performance_slice.py`).

## Fixtures and Factories

**Test Data:**
```python
workbook_path = tmp_path / "annual_loss_2026_03.xlsx"
workbook = Workbook()
trustee = workbook.active
trustee.title = "企年受托流失(解约)"
trustee.append([...])
workbook.save(workbook_path)
```

**Location:**
- No shared `conftest.py` detected.
- Fixtures/factories are file-local helper functions inside each test module (`tests/replay/test_annual_loss_slice.py`, `tests/replay/test_annuity_performance_explainability_slo.py`).

## Coverage

**Requirements:** No explicit minimum coverage threshold detected in `pyproject.toml` or dedicated coverage config.

**View Coverage:**
```bash
uv run pytest --cov=src --cov-report=term
```

## Test Types

**Unit Tests:**
- Lightweight model/utility behavior tests live mostly in `tests/contracts/` and parts of `tests/integration/` (examples: `tests/contracts/test_project_bootstrap.py`, `tests/contracts/test_trace_lineage_runtime.py`).

**Integration Tests:**
- Primary coverage type; validates real interactions across capability/platform services and governed config files (examples: `tests/integration/test_annuity_performance_processing.py`, `tests/integration/test_publication_service.py`, `tests/integration/test_compatibility_adjudication.py`).

**E2E Tests:**
- Full replay slice tests in `tests/replay/` execute orchestration entrypoints and assert compatibility/evidence outputs.
- Browser/UI E2E framework: Not used.

## Common Patterns

**Async Testing:**
```python
# Not used in current suite.
# All tests and production paths are synchronous.
```

**Error Testing:**
```python
result = processor.process(record_without_sales_amount)
assert result.trace_events[-1].success is False
assert result.trace_events[-1].error_message == "missing field: sales_amount"
```

Additional observed error/safety checks:
- SLO timing assertions with `perf_counter` (`tests/replay/test_annual_loss_explainability_slo.py`, `tests/performance/test_trace_lookup_micro_benchmark.py`).
- Filesystem context manipulation using `monkeypatch.chdir` for CLI replay path behavior (`tests/replay/test_annual_loss_explainability_slo.py`).

---

*Testing analysis: 2026-04-12*

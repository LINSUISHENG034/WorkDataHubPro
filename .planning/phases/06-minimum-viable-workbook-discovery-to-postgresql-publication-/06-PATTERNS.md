# Phase 6: Minimum viable workbook discovery to PostgreSQL publication pilot - Pattern Map

**Mapped:** 2026-04-19
**Files analyzed:** 17
**Analogs found:** 15 / 17

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|---|---|---|---|---|
| `src/work_data_hub_pro/platform/storage/postgres_tables.py` | service | CRUD | `src/work_data_hub_pro/platform/storage/in_memory_tables.py` | exact-role / partial-flow |
| `src/work_data_hub_pro/platform/storage/protocols.py` | utility | request-response | `src/work_data_hub_pro/platform/storage/in_memory_tables.py` | partial |
| `src/work_data_hub_pro/platform/storage/errors.py` | utility | request-response | `src/work_data_hub_pro/platform/publication/service.py` | role-match |
| `src/work_data_hub_pro/platform/publication/service.py` | service | request-response | `src/work_data_hub_pro/platform/publication/service.py` | exact |
| `src/work_data_hub_pro/apps/etl_cli/main.py` | controller | request-response | `src/work_data_hub_pro/apps/etl_cli/main.py` | exact |
| `src/work_data_hub_pro/capabilities/projections/contract_state.py` | service | transform | `src/work_data_hub_pro/capabilities/projections/contract_state.py` | exact |
| `src/work_data_hub_pro/capabilities/projections/monthly_snapshot.py` | service | transform | `src/work_data_hub_pro/capabilities/projections/monthly_snapshot.py` | exact |
| `config/schemas/annuity_performance/fact_annuity_performance.sql` | config | CRUD | `config/policies/publication.json` | partial |
| `config/schemas/annuity_performance/company_reference.sql` | config | CRUD | `config/policies/publication.json` | partial |
| `config/schemas/annuity_performance/contract_state.sql` | config | CRUD | `config/policies/publication.json` | partial |
| `config/schemas/annuity_performance/monthly_snapshot.sql` | config | append-only | `config/policies/publication.json` | partial |
| `config/schemas/annuity_performance/*.schema.json` | config | request-response | `src/work_data_hub_pro/governance/compatibility/gate_runtime.py` | flow-match |
| `tests/integration/test_postgres_publication_pilot.py` | test | request-response | `tests/integration/test_publication_service.py` | exact-role / partial-flow |
| `tests/integration/test_postgres_adapter_errors.py` | test | request-response | `tests/integration/test_publication_service.py` | exact-role / partial-flow |
| `docs/runbooks/publish-annuity-performance.md` | config | request-response | `docs/runbooks/annuity-performance-replay.md` | role-match |
| `pyproject.toml` | config | request-response | `pyproject.toml` | exact |
| `.planning/REQUIREMENTS.md` | config | request-response | `.planning/REQUIREMENTS.md` | exact |

## Pattern Assignments

### `src/work_data_hub_pro/platform/storage/postgres_tables.py` (service, CRUD)

**Analog:** `src/work_data_hub_pro/platform/storage/in_memory_tables.py`

**Imports and class shape** (`src/work_data_hub_pro/platform/storage/in_memory_tables.py` lines 1-8):
```python
from __future__ import annotations

from copy import deepcopy


class InMemoryTableStore:
    def __init__(self, seed: dict[str, list[dict[str, object]]] | None = None) -> None:
        self._tables = deepcopy(seed or {})
```

**Method contract to mirror** (`src/work_data_hub_pro/platform/storage/in_memory_tables.py` lines 10-36):
```python
def refresh(self, target_name: str, rows: list[dict[str, object]]) -> int:
    self._tables[target_name] = deepcopy(rows)
    return len(rows)

def upsert(
    self,
    target_name: str,
    rows: list[dict[str, object]],
    *,
    key_fields: list[str],
) -> int:
    existing = {
        tuple(row[key] for key in key_fields): row
        for row in self._tables.get(target_name, [])
    }
    for row in rows:
        existing[tuple(row[key] for key in key_fields)] = deepcopy(row)
    self._tables[target_name] = list(existing.values())
    return len(rows)

def append(self, target_name: str, rows: list[dict[str, object]]) -> int:
    current = self._tables.setdefault(target_name, [])
    current.extend(deepcopy(rows))
    return len(rows)

def read(self, target_name: str) -> list[dict[str, object]]:
    return deepcopy(self._tables.get(target_name, []))
```

**Transaction seam to align with** (`src/work_data_hub_pro/platform/publication/service.py` lines 148-168):
```python
def execute(self, bundles: list[PublicationBundle]) -> list[PublicationResult]:
    results: list[PublicationResult] = []
    for bundle in bundles:
        try:
            if bundle.plan.mode is PublicationMode.REFRESH:
                affected_rows = self._storage.refresh(bundle.plan.target_name, bundle.rows)
            elif bundle.plan.mode is PublicationMode.UPSERT:
                affected_rows = self._storage.upsert(
                    bundle.plan.target_name,
                    bundle.rows,
                    key_fields=bundle.plan.upsert_keys,
                )
            else:
                affected_rows = self._storage.append(bundle.plan.target_name, bundle.rows)
        except Exception as exc:
            raise PublicationExecutionError(
                publication_id=bundle.plan.publication_id,
                target_name=bundle.plan.target_name,
                message=str(exc),
            ) from exc
```

**Schema-gate / fail-closed pattern to borrow** (`src/work_data_hub_pro/governance/compatibility/gate_runtime.py` lines 69-98):
```python
def load_required_checkpoint_baseline(
    path: Path, checkpoint_name: str
) -> list[dict[str, object]]:
    if not path.exists():
        raise FileNotFoundError(
            f"Missing accepted baseline for checkpoint '{checkpoint_name}': {path}"
        )
    with open(path, encoding="utf-8") as f:
        content = json.load(f)
    if not isinstance(content, list):
        raise TypeError(
            f"Baseline file for checkpoint '{checkpoint_name}' must contain a JSON array. "
            f"Got {type(content).__name__}: {path}"
        )
    return content
```

**Copy from this file:** keep the `refresh` / `upsert` / `append` / `read` public shape identical, then add PG-specific connection, SQL, schema validation, and `transaction()` context manager around that contract.

---

### `src/work_data_hub_pro/platform/storage/protocols.py` (utility, request-response)

**Analog:** `src/work_data_hub_pro/platform/storage/in_memory_tables.py`

**Interface source to abstract** (`src/work_data_hub_pro/platform/storage/in_memory_tables.py` lines 6-36):
```python
class InMemoryTableStore:
    def __init__(self, seed: dict[str, list[dict[str, object]]] | None = None) -> None:
        self._tables = deepcopy(seed or {})

    def refresh(self, target_name: str, rows: list[dict[str, object]]) -> int:
        ...

    def upsert(self, target_name: str, rows: list[dict[str, object]], *, key_fields: list[str]) -> int:
        ...

    def append(self, target_name: str, rows: list[dict[str, object]]) -> int:
        ...

    def read(self, target_name: str) -> list[dict[str, object]]:
        ...
```

**Consumer to update** (`src/work_data_hub_pro/platform/publication/service.py` lines 144-146):
```python
class PublicationService:
    def __init__(self, storage: InMemoryTableStore) -> None:
        self._storage = storage
```

**Projection consumers also currently coupled** (`src/work_data_hub_pro/capabilities/projections/contract_state.py` lines 16-18 and `src/work_data_hub_pro/capabilities/projections/monthly_snapshot.py` lines 8-10):
```python
class ContractStateProjection:
    def __init__(self, storage: InMemoryTableStore) -> None:
        self._storage = storage
```
```python
class MonthlySnapshotProjection:
    def __init__(self, storage: InMemoryTableStore) -> None:
        self._storage = storage
```

**Copy from this file:** extract only the smallest shared interface; do not introduce factory/registry machinery.

---

### `src/work_data_hub_pro/platform/storage/errors.py` (utility, request-response)

**Analog:** `src/work_data_hub_pro/platform/publication/service.py`

**Typed error hierarchy pattern** (`src/work_data_hub_pro/platform/publication/service.py` lines 17-49):
```python
class PublicationPolicyError(Exception):
    pass


class PolicyFileMissingError(PublicationPolicyError):
    pass


class PolicyParseError(PublicationPolicyError):
    pass


class UnknownDomainError(PublicationPolicyError):
    pass


class UnknownTargetError(PublicationPolicyError):
    pass


class PublicationExecutionError(Exception):
    def __init__(
        self,
        *,
        publication_id: str,
        target_name: str,
        message: str,
    ) -> None:
        super().__init__(message)
        self.publication_id = publication_id
        self.target_name = target_name
        self.message = message
```

**Copy from this file:** use one base PG adapter error plus narrow subclasses; keep constructors simple and explicit, matching existing boundary-specific typed errors.

---

### `src/work_data_hub_pro/platform/publication/service.py` (service, request-response)

**Analog:** `src/work_data_hub_pro/platform/publication/service.py`

**Imports and policy loading style** (lines 1-15, 80-109):
```python
import json
from dataclasses import dataclass
from pathlib import Path

from pydantic import BaseModel, ValidationError

from work_data_hub_pro.platform.contracts.publication import (
    PublicationMode,
    PublicationPlan,
    PublicationResult,
)
from work_data_hub_pro.platform.storage.in_memory_tables import InMemoryTableStore
```
```python
def load_publication_policy(path: Path, *, domain: str) -> PublicationPolicy:
    if not path.exists():
        raise PolicyFileMissingError(f"Publication policy file not found: {path}")

    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        validated = PublicationPolicyFileModel.model_validate({"root": payload})
    except (OSError, json.JSONDecodeError, ValidationError) as exc:
        raise PolicyParseError(
            f"Publication policy file could not be parsed: {path}"
        ) from exc
```

**Core execute pattern to preserve** (lines 144-180):
```python
class PublicationService:
    def __init__(self, storage: InMemoryTableStore) -> None:
        self._storage = storage

    def execute(self, bundles: list[PublicationBundle]) -> list[PublicationResult]:
        results: list[PublicationResult] = []
        for bundle in bundles:
            try:
                if bundle.plan.mode is PublicationMode.REFRESH:
                    affected_rows = self._storage.refresh(bundle.plan.target_name, bundle.rows)
                elif bundle.plan.mode is PublicationMode.UPSERT:
                    affected_rows = self._storage.upsert(
                        bundle.plan.target_name,
                        bundle.rows,
                        key_fields=bundle.plan.upsert_keys,
                    )
                else:
                    affected_rows = self._storage.append(bundle.plan.target_name, bundle.rows)
            except Exception as exc:
                raise PublicationExecutionError(
                    publication_id=bundle.plan.publication_id,
                    target_name=bundle.plan.target_name,
                    message=str(exc),
                ) from exc
```

**Copy from this file:** keep bundle loop, mode dispatch, and typed fail-fast wrapping unchanged; only widen constructor typing and add an outer `transaction()` boundary.

---

### `src/work_data_hub_pro/apps/etl_cli/main.py` (controller, request-response)

**Analog:** `src/work_data_hub_pro/apps/etl_cli/main.py`

**Sub-command registration pattern** (lines 28-32):
```python
app = typer.Typer(help="WorkDataHubPro replay utilities")
replay_app = typer.Typer(help="Registry-backed replay commands")
compatibility_app = typer.Typer(help="File-backed compatibility case commands")
app.add_typer(replay_app, name="replay")
app.add_typer(compatibility_app, name="compatibility")
```

**Command function style** (lines 165-179):
```python
@replay_app.command("run")
def replay_run(
    domain: str = typer.Option(..., "--domain"),
    workbook: Path = typer.Option(..., "--workbook"),
    period: str = typer.Option(..., "--period"),
    replay_root: Path | None = typer.Option(None, "--replay-root"),
) -> None:
    outcome = _execute_replay(
        domain=domain,
        workbook=workbook,
        period=period,
        replay_root=replay_root,
    )
    _emit_json(_run_summary(outcome))
```

**Wrapper command output style** (lines 146-152, 282-294):
```python
def _emit_wrapper_summary(outcome) -> None:
    summary = _run_summary(outcome)
    typer.echo(f"comparison_run_id={summary['comparison_run_id']}")
    typer.echo(f"overall_outcome={summary['overall_outcome']}")
    typer.echo(f"publication_results={summary['publication_result_count']}")
    typer.echo(f"projection_results={summary['projection_result_count']}")
    typer.echo(f"compatibility_case={summary['compatibility_case_id'] is not None}")
```
```python
@app.command("replay-annuity-performance")
def replay_annuity_performance(
    workbook: Path,
    period: str,
    replay_root: Path = Path("reference/historical_replays/annuity_performance"),
) -> None:
    outcome = _execute_replay(
        domain="annuity_performance",
        workbook=workbook,
        period=period,
        replay_root=replay_root,
    )
    _emit_wrapper_summary(outcome)
```

**Error/JSON emission pattern** (lines 121-123, 185-205):
```python
def _emit_json(payload: dict[str, Any]) -> None:
    typer.echo(json.dumps(payload, ensure_ascii=False))
```
```python
try:
    diagnostics = load_replay_diagnostics(comparison_run_id)
except ValueError as exc:
    typer.echo(f"Invalid comparison_run_id: {comparison_run_id}", err=True)
    raise typer.Exit(code=1) from exc
...
_emit_json(_diagnostics_payload(diagnostics))
```

**Copy from this file:** add `publish_app` through `app.add_typer(...)`; keep command signatures explicit and keep stable first-line stdout for operator correlation.

---

### `src/work_data_hub_pro/capabilities/projections/contract_state.py` (service, transform)

**Analog:** `src/work_data_hub_pro/capabilities/projections/contract_state.py`

**Imports and storage dependency** (lines 1-8):
```python
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from work_data_hub_pro.platform.contracts.models import ProjectionResult
from work_data_hub_pro.platform.storage.in_memory_tables import InMemoryTableStore
```

**Constructor and read pattern** (lines 16-19, 41-55):
```python
class ContractStateProjection:
    def __init__(self, storage: InMemoryTableStore) -> None:
        self._storage = storage
```
```python
def run(self, *, publication_ids: list[str], period: str) -> ProjectionRows:
    performance_rows = [
        row
        for row in self._storage.read("fact_annuity_performance")
        if row["period"] == period
    ]
    award_fact_rows = self._storage.read("fact_annual_award")
    award_fixture_rows = self._storage.read("fixture_annual_award")
    loss_fact_rows = self._storage.read("fact_annual_loss")
    loss_fixture_rows = self._storage.read("fixture_annual_loss")
```

**Projection result shape** (lines 97-105):
```python
return ProjectionRows(
    rows=rows,
    result=ProjectionResult(
        projection_name="contract_state",
        source_publications=publication_ids,
        affected_rows=len(rows),
        success=True,
    ),
)
```

**Copy from this file:** if this file is touched for protocolization, only replace the concrete storage annotation; keep business projection logic byte-for-byte.

---

### `src/work_data_hub_pro/capabilities/projections/monthly_snapshot.py` (service, transform)

**Analog:** `src/work_data_hub_pro/capabilities/projections/monthly_snapshot.py`

**Imports and constructor** (lines 1-10):
```python
from __future__ import annotations

from work_data_hub_pro.capabilities.projections.contract_state import ProjectionRows
from work_data_hub_pro.platform.contracts.models import ProjectionResult
from work_data_hub_pro.platform.storage.in_memory_tables import InMemoryTableStore


class MonthlySnapshotProjection:
    def __init__(self, storage: InMemoryTableStore) -> None:
        self._storage = storage
```

**Read/transform pattern** (lines 12-39):
```python
def run(self, *, publication_ids: list[str], period: str) -> ProjectionRows:
    contract_state_rows = [
        row for row in self._storage.read("contract_state") if row["period"] == period
    ]
    contracts_with_award_fixture = sum(
        1 for row in contract_state_rows if row["has_annual_award_fixture"]
    )
    contracts_with_loss_fixture = sum(
        1 for row in contract_state_rows if row["has_annual_loss_fixture"]
    )
    rows = [
        {
            "period": period,
            "contract_state_rows": len(contract_state_rows),
            # Keep output keys stable for accepted replay baselines.
            "award_fixture_rows": contracts_with_award_fixture,
            "loss_fixture_rows": contracts_with_loss_fixture,
        }
    ]
```

**Copy from this file:** same rule as `contract_state.py`—if touched, only loosen storage typing; do not move any counting or output-key logic into PG code.

---

### `config/schemas/annuity_performance/*.schema.json` (config, request-response)

**Analog:** `src/work_data_hub_pro/governance/compatibility/gate_runtime.py`

**Fail-closed file loading pattern** (lines 69-98):
```python
def load_required_checkpoint_baseline(
    path: Path, checkpoint_name: str
) -> list[dict[str, object]]:
    if not path.exists():
        raise FileNotFoundError(
            f"Missing accepted baseline for checkpoint '{checkpoint_name}': {path}"
        )
    with open(path, encoding="utf-8") as f:
        content = json.load(f)
    if not isinstance(content, list):
        raise TypeError(
            f"Baseline file for checkpoint '{checkpoint_name}' must contain a JSON array. "
            f"Got {type(content).__name__}: {path}"
        )
    return content
```

**Deterministic comparison pattern** (lines 101-164):
```python
if isinstance(legacy_payload, list) and isinstance(pro_payload, list):
    legacy_counter = Counter(
        json.dumps(_to_jsonable(item), sort_keys=True, ensure_ascii=False)
        for item in legacy_payload
    )
    pro_counter = Counter(
        json.dumps(_to_jsonable(item), sort_keys=True, ensure_ascii=False)
        for item in pro_payload
    )
```

**Copy from this file:** schema snapshots should be committed, explicit, and compared deterministically; missing or malformed snapshots must fail closed.

---

### `config/schemas/annuity_performance/*.sql` (config, CRUD/append-only)

**Analog:** `config/policies/publication.json`

**Target inventory / naming source** (`config/policies/publication.json` lines 2-23):
```json
"annuity_performance": {
  "fact_annuity_performance": {
    "mode": "REFRESH",
    "transaction_group": "fact-publication",
    "idempotency_scope": "batch"
  },
  "company_reference": {
    "mode": "UPSERT",
    "transaction_group": "reference-publication",
    "idempotency_scope": "company_id"
  },
  "contract_state": {
    "mode": "REFRESH",
    "transaction_group": "projection-publication",
    "idempotency_scope": "period"
  },
  "monthly_snapshot": {
    "mode": "APPEND_ONLY",
    "transaction_group": "projection-publication",
    "idempotency_scope": "run"
  }
}
```

**Copy from this file:** use the exact target names and mode semantics from policy as the DDL file naming and table intent source; keep one SQL file per target.

---

### `tests/integration/test_postgres_publication_pilot.py` (test, request-response)

**Analog:** `tests/integration/test_publication_service.py`

**Test imports / fixture-free setup style** (lines 1-20):
```python
from pathlib import Path

import pytest

from work_data_hub_pro.platform.contracts.publication import (
    PublicationMode,
)
from work_data_hub_pro.platform.publication.service import (
    PolicyFileMissingError,
    PolicyParseError,
    PublicationBundle,
    PublicationExecutionError,
    PublicationService,
    UnknownDomainError,
    UnknownTargetError,
    build_publication_plan,
    load_publication_policy,
)
from work_data_hub_pro.platform.storage.in_memory_tables import InMemoryTableStore
```

**Happy-path service assertion style** (lines 22-80):
```python
def test_publication_service_executes_visible_transaction_groups() -> None:
    storage = InMemoryTableStore()
    service = PublicationService(storage)
    policy = load_publication_policy(
        Path("config/policies/publication.json"),
        domain="annuity_performance",
    )
    results = service.execute([...])

    assert [result.transaction_group for result in results] == [
        "fact-publication",
        "reference-publication",
    ]
    assert [result.mode for result in results] == [
        PublicationMode.REFRESH,
        PublicationMode.UPSERT,
    ]
```

**Typed error assertion style** (lines 268-314):
```python
def test_load_publication_policy_raises_typed_error_for_missing_file(tmp_path: Path) -> None:
    missing_path = tmp_path / "missing-publication.json"

    with pytest.raises(PolicyFileMissingError):
        load_publication_policy(missing_path, domain="annuity_performance")
```
```python
def test_build_publication_plan_raises_typed_error_for_unknown_target() -> None:
    policy = load_publication_policy(
        Path("config/policies/publication.json"),
        domain="annuity_performance",
    )

    with pytest.raises(UnknownTargetError):
        build_publication_plan(...)
```

**Mid-run failure pattern** (lines 316-389):
```python
class FailingOnSecondWriteStore(InMemoryTableStore):
    def __init__(self) -> None:
        super().__init__()
        self.calls: list[str] = []

    def refresh(self, target_name: str, rows: list[dict[str, object]]) -> int:
        self.calls.append(target_name)
        if len(self.calls) == 2:
            raise RuntimeError("simulated second write failure")
        return super().refresh(target_name, rows)
```
```python
with pytest.raises(PublicationExecutionError) as exc_info:
    service.execute(bundles)

assert exc_info.value.publication_id == "publication-contract-state-001"
assert exc_info.value.target_name == "contract_state"
assert exc_info.value.message == "simulated second write failure"
```

**Replay parity source to reuse** (`tests/replay/test_annuity_performance_slice.py` lines 147-158):
```python
assert [result.target_name for result in outcome.publication_results] == [
    "fact_annuity_performance",
    "company_reference",
    "contract_state",
    "monthly_snapshot",
]
assert [result.projection_name for result in outcome.projection_results] == [
    "contract_state",
    "monthly_snapshot",
]
```

**Stable sort analog for read-back diff** (`src/work_data_hub_pro/apps/orchestration/replay/annuity_performance_slice.py` lines 101-103):
```python
def _sorted_payload(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    return sorted(rows, key=lambda row: json.dumps(row, sort_keys=True, ensure_ascii=False))
```

**Copy from these files:** write the new PG integration test in the same direct pytest style; expected rows should come from replay output, then be compared after deterministic sorting.

---

### `tests/integration/test_postgres_adapter_errors.py` (test, request-response)

**Analog:** `tests/integration/test_publication_service.py`

**Error-focused test style** (lines 268-389):
```python
with pytest.raises(PolicyParseError):
    load_publication_policy(malformed_path, domain="annuity_performance")
```
```python
with pytest.raises(PublicationExecutionError) as exc_info:
    service.execute(bundles)
```

**Additional fail-closed contract style** (`tests/contracts/test_phase6_gate_runtime.py` lines 88-111):
```python
with pytest.raises(FileNotFoundError) as exc_info:
    load_required_checkpoint_baseline(missing_file, "reference_derivation")

assert "Missing accepted baseline for checkpoint" in str(exc_info.value)
```

**Copy from these files:** negative PG-path tests should assert typed exceptions and explicit messages, not generic failure booleans.

---

### `docs/runbooks/publish-annuity-performance.md` (config, request-response)

**Analog:** `docs/runbooks/annuity-performance-replay.md`

**Runbook section structure** (lines 1-30):
```markdown
# Annuity Performance Replay Runbook

## Goal
...
## Inputs
...
## Wrapper Command
...
## Expected Output
...
```

**Canonical workflow / CLI examples pattern** (lines 32-69):
```markdown
## Canonical workflow
...
## Agent CLI
...
```bash
uv run python -m work_data_hub_pro.apps.etl_cli.main replay list-domains
```
```bash
uv run python -m work_data_hub_pro.apps.etl_cli.main replay run --domain annuity_performance --workbook data/annuity_performance_2026_03.xlsx --period 2026-03
```

**Copy from this file:** keep the same concise runbook structure; replace replay-specific commands with publish prerequisites, env vars, DDL application, invocation, verification, and teardown.

---

### `pyproject.toml` (config, request-response)

**Analog:** `pyproject.toml`

**Dependency layout pattern** (lines 5-20):
```toml
[project]
name = "work-data-hub-pro"
version = "0.1.0"
...
dependencies = [
  "openpyxl>=3.1,<4.0",
  "pydantic>=2,<3",
  "typer>=0.12,<1.0",
]

[dependency-groups]
dev = [
  "PyYAML>=6.0,<7.0",
  "pytest>=8.2,<9.0",
]
```

**Pytest config pattern** (lines 28-29):
```toml
[tool.pytest.ini_options]
addopts = "--basetemp=.pytest_tmp"
```

**Copy from this file:** append new runtime and dev dependencies in the existing two-list layout; if a `postgres` marker is registered here, keep it under the same `[tool.pytest.ini_options]` section.

---

### `.planning/REQUIREMENTS.md` (config, request-response)

**Analog:** `.planning/REQUIREMENTS.md`

**Requirement list style** (lines 47-58):
```markdown
## v2 Requirements

### Runtime Expansion

- **RUN-01**: Support production-grade persistent storage/tracing adapters beyond in-memory replay mode
- **RUN-02**: Add orchestrated queue/retry runtime for large replay backlogs
- **RUN-03**: Add advanced publication channels and operational policy controls beyond first-wave reconstruction scope
```

**Traceability table pattern** (lines 69-94):
```markdown
## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| ... |
| PERF-03 | Phase 5 | Pending |
| GOV-01 | Phase 4 | Validated |
```

**Copy from this file:** append `RUN-01a` in the existing requirement list and add one traceability row; do not reformat prior requirement blocks.

## Shared Patterns

### Storage contract
**Source:** `src/work_data_hub_pro/platform/storage/in_memory_tables.py` lines 6-36
**Apply to:** `postgres_tables.py`, `protocols.py`, `publication/service.py`, possibly both projection files
```python
class InMemoryTableStore:
    ...
    def refresh(...): ...
    def upsert(..., *, key_fields: list[str]) -> int: ...
    def append(...): ...
    def read(...): ...
```

### Publication fail-fast wrapping
**Source:** `src/work_data_hub_pro/platform/publication/service.py` lines 148-168
**Apply to:** `publication/service.py`, PG adapter integration tests
```python
try:
    ...
except Exception as exc:
    raise PublicationExecutionError(
        publication_id=bundle.plan.publication_id,
        target_name=bundle.plan.target_name,
        message=str(exc),
    ) from exc
```

### Typed boundary errors
**Source:** `src/work_data_hub_pro/platform/publication/service.py` lines 17-49
**Apply to:** `platform/storage/errors.py`, PG config/schema/write failures
```python
class PublicationPolicyError(Exception):
    pass
```

### CLI subgroup wiring
**Source:** `src/work_data_hub_pro/apps/etl_cli/main.py` lines 28-32
**Apply to:** `apps/etl_cli/main.py`
```python
app = typer.Typer(...)
replay_app = typer.Typer(...)
compatibility_app = typer.Typer(...)
app.add_typer(replay_app, name="replay")
app.add_typer(compatibility_app, name="compatibility")
```

### Deterministic payload comparison
**Source:** `src/work_data_hub_pro/apps/orchestration/replay/annuity_performance_slice.py` lines 101-103
**Apply to:** `test_postgres_publication_pilot.py`
```python
def _sorted_payload(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    return sorted(rows, key=lambda row: json.dumps(row, sort_keys=True, ensure_ascii=False))
```

### Fail-closed snapshot loading
**Source:** `src/work_data_hub_pro/governance/compatibility/gate_runtime.py` lines 69-98
**Apply to:** `postgres_tables.py`, `*.schema.json` loading, adapter error tests
```python
if not path.exists():
    raise FileNotFoundError(...)
```

### Test style
**Source:** `tests/integration/test_publication_service.py` lines 22-389
**Apply to:** both new PG integration modules
```python
storage = InMemoryTableStore()
service = PublicationService(storage)
...
with pytest.raises(...):
    ...
```

### Runbook structure
**Source:** `docs/runbooks/annuity-performance-replay.md` lines 1-69
**Apply to:** `docs/runbooks/publish-annuity-performance.md`
```markdown
## Goal
## Inputs
## Wrapper Command
## Expected Output
## Canonical workflow
## Agent CLI
```

## No Analog Found

Files with no close codebase analog; planner should use the nearest contract pattern above plus Phase 6 research/context constraints:

| File | Role | Data Flow | Reason |
|---|---|---|---|
| `config/schemas/annuity_performance/*.sql` | config | CRUD / append-only | Repository has governed config JSON, but no existing hand-written SQL DDL pattern yet. |
| `src/work_data_hub_pro/platform/storage/postgres_tables.py` | service | CRUD | No existing persistent database adapter exists; only in-memory contract analog exists. |

## Metadata

**Analog search scope:** `src/work_data_hub_pro/platform/`, `src/work_data_hub_pro/apps/etl_cli/`, `src/work_data_hub_pro/apps/orchestration/replay/`, `src/work_data_hub_pro/capabilities/projections/`, `tests/integration/`, `tests/replay/`, `docs/runbooks/`, `config/`, `.planning/`

**Files scanned:** 14

**Pattern extraction date:** 2026-04-19

# Phase 6: Minimum viable workbook discovery to PostgreSQL publication pilot - Research

**Researched:** 2026-04-19
**Domain:** workbook-driven ETL publication to PostgreSQL in a capability-first Python runtime [VERIFIED: local file]
**Confidence:** HIGH

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

### A. Pilot slice boundary

- **D-01:** Pilot is locked to `annuity_performance` as the single domain. Architecture blueprint §7.3 names this as the first validation slice; it is also the domain with the richest existing capability coverage and the most stable replay baseline. No other domain gains a PG write path in Phase 6.
- **D-02:** All four publication targets for `annuity_performance` go through PostgreSQL: `fact_annuity_performance`, `company_reference`, `contract_state`, `monthly_snapshot`. This covers all three publication modes already modeled — `REFRESH`, `UPSERT`, `APPEND_ONLY` — so the adapter is proven against every mode the platform contracts describe.
- **D-03:** Upstream stages are byte-unchanged: `source_intake`, `fact_processing`, `identity_resolution`, `reference_derivation`, `tracing`, and `governance/evidence_index/*`. The pilot is purely a publication-layer adapter insertion. Trace events remain in `platform/tracing/in_memory_trace_store.py`; evidence remains in the file-backed evidence index. Any temptation to "tidy up" adjacent modules is out of scope.

### B. PostgreSQL adapter shape

- **D-04:** Driver is **psycopg v3** (synchronous API). Rationale: lightweight, pydantic v2-compatible, same sync call style as the existing `PublicationService.execute` loop, no API-level changes elsewhere. No `asyncpg`, no SQLAlchemy, no psycopg2. Add `psycopg[binary]>=3.2,<4` as a runtime dependency in `pyproject.toml` and refresh `uv.lock`.
- **D-05:** New `PostgresTableStore` lives at `src/work_data_hub_pro/platform/storage/postgres_tables.py`. It mirrors the `InMemoryTableStore` public contract: `refresh(target_name, rows) -> int`, `upsert(target_name, rows, *, key_fields) -> int`, `append(target_name, rows) -> int`, plus a `read(target_name) -> list[dict]` helper used only by tests / read-back diffs.
- **D-06:** `PublicationService` is made storage-agnostic via a **minimum Protocol** (or equivalent `typing.Protocol`) in `platform/storage/` describing the three write operations. `PublicationService.__init__` accepts any object satisfying the protocol. Current `InMemoryTableStore` usage continues to work unchanged. This is a surgical seam — no refactor of publication, no new factory system, no "storage registry".
- **D-07:** Connection configuration is read **only from environment variables**. Primary: `WDH_PG_DSN` (explicit, project-scoped). Fallback: `DATABASE_URL` (industry standard). If both are absent, the adapter raises a typed `PostgresAdapterConfigError` at construction time (never silently falls back to in-memory). Optional `WDH_PG_SCHEMA` env var (default `public`) prefixes all table lookups. No secrets in `config/`, no `.env` loader inside the adapter.
- **D-08:** Schema management: hand-written **idempotent DDL scripts** under `config/schemas/annuity_performance/`. One file per target table (e.g. `fact_annuity_performance.sql`, `company_reference.sql`, `contract_state.sql`, `monthly_snapshot.sql`). Operators apply these scripts before first run (documented runbook step); the adapter does **not** auto-create tables. Legacy `E:\Projects\WorkDataHub\io\schema\migrations\versions/*` is a **reference for column shapes and indexes only** — do not copy Alembic infrastructure.
- **D-09:** Fail-closed startup schema validation: on first use of a target, `PostgresTableStore` queries `information_schema.columns` for the configured schema + table, compares the result against a per-target expected-column snapshot committed under `config/schemas/annuity_performance/<target>.schema.json`, and raises a typed `PostgresSchemaMismatchError` (subclass of `PostgresAdapterError`) on any mismatch. This is the agent-operable gate: the adapter never runs DDL, it only asserts preconditions.
- **D-10:** Transaction boundary: **one PostgreSQL transaction covers the whole publish run** (all four targets). `PostgresTableStore` exposes `transaction()` as a context manager; `PublicationService.execute` wraps its per-bundle loop inside one `transaction()` when the injected store supports it. Any target failure inside the loop raises the existing fail-fast `PublicationExecutionError` (Phase 5 D-12) and rolls back every write. This matches the "one run = one atomic state transition" operator mental model and removes partial-write residue.
- **D-11:** Typed error hierarchy under `src/work_data_hub_pro/platform/storage/errors.py` (or inline in `postgres_tables.py` — Claude's discretion): base `PostgresAdapterError` + `PostgresAdapterConfigError`, `PostgresConnectionError`, `PostgresSchemaMismatchError`, `PostgresWriteError`. Mirrors Phase 3 / Phase 5 typed-diagnostic style.

### C. Workbook discovery + operator entrypoint

- **D-12:** Operator invocation style mirrors the existing `replay` CLI — **explicit workbook path + explicit period** as positional arguments. No directory scanning, no filename convention parser, no manifest file. Pilot stays reproducible and boring.
- **D-13:** CLI surface: extend `src/work_data_hub_pro/apps/etl_cli/main.py` with a new `publish_app = typer.Typer(...)` sub-group and mount it via `app.add_typer(publish_app, name="publish")`. First command: `publish annuity-performance <workbook> <period>`. The command signature and help style must match existing `replay` sub-group conventions.
- **D-14:** Identifiers (`run_id`, `batch_id`, `publication_id`) are **auto-generated inside the command**. Convention: `run_id = f"pub-{domain}-{period}-{utc_iso_timestamp}"`; `batch_id` and `publication_id` derive from `run_id` with stable suffixes (e.g. `{run_id}-batch`, `{run_id}-{target_name}`). The generated `run_id` is printed on stdout as the first line of successful command output so an operator can trace it back to PG rows. No `--run-id` override in Phase 6.
- **D-15:** The pilot command is **read-only against the workbook** and **write-only against PG** — it never writes to `evidence_index/`, `tracing/in_memory_trace_store.py`, or any file-backed artifact outside PG. (Evidence persistence for PG runs belongs in a future phase that pairs with a PG-backed evidence adapter.) The replay CLI remains the only path that materializes evidence + trace bundles.

### D. Acceptance axis + Requirements mapping

- **D-16:** Phase 6 opens a **new pilot-scoped requirement** `RUN-01a` in `REQUIREMENTS.md`. Definition: *"Single-domain (`annuity_performance`) PostgreSQL publication adapter can publish all four domain targets from one real workbook, under a single transaction, with a fail-closed schema gate and a typed error surface."* The broader v2 `RUN-01` ("production-grade persistent storage / tracing adapters beyond in-memory replay mode") stays open and unresolved — `RUN-01a` is listed as a predecessor pilot, not a replacement. Traceability table adds a row: `RUN-01a → Phase 6 → Pending`.
- **D-17:** Acceptance evidence is a **read-back diff against replay output**. For the same `annuity_performance` workbook + period:
  1. Run the existing replay CLI → produce the in-memory publication bundles and the replay run report.
  2. Run the new `publish annuity-performance` CLI → write to PG.
  3. A new integration test at `tests/integration/test_postgres_publication_pilot.py` loads PG rows via `PostgresTableStore.read(target_name)` for each of the four targets and asserts row-for-row, field-for-field equality with the replay bundle rows (with a documented, minimal normalization for row ordering where `APPEND_ONLY` semantics allow it). This is the pilot's truth gate.
- **D-18:** Parity guarantee is **delegated to replay**: the replay acceptance suite under `tests/replay/annuity_performance/*` is the source of truth for business-semantic correctness. Phase 6 does **not** add a second parity harness. If the read-back diff disagrees with replay, the PG adapter or the publish command is wrong — replay is never re-derived to match PG output. (Phase 5 D-05 / D-08 pattern.)
- **D-19:** Test infrastructure is **testcontainers-python** with a module-scoped PostgreSQL container fixture. Pytest marker: `@pytest.mark.postgres`. The marker lets the existing CI tiering (Phase 2 / Phase 5 D-15) decide where this runs: local + protected-branch + nightly; PR tier stays fast by skipping `postgres`-marked tests by default. Add `testcontainers[postgresql]` and `pytest-docker` (or equivalent) only to the `dev` dependency group in `pyproject.toml`. If Docker is unavailable on the host, tests using the marker are **skipped**, not failed.
- **D-20:** Negative-path coverage (also under `tests/integration/test_postgres_publication_pilot.py` or a sibling module): missing `WDH_PG_DSN` → `PostgresAdapterConfigError`; schema mismatch on first use → `PostgresSchemaMismatchError`; mid-run target failure → whole transaction rolls back (post-condition assertion: all four tables are empty after a seeded failure). Aligns with Phase 5 D-13 "negative-path coverage lives in integration tests" pattern.
- **D-21:** Verification artifacts: Phase 6 produces a standard `06-VERIFICATION.md` and a new runbook entry at `docs/runbooks/publish-annuity-performance.md` (setup steps: env var, DDL apply, testcontainers / local PG, sample invocation, teardown). The runbook is a required plan output, not an afterthought — Phase 4 OPS-02 pattern.

### Claude's Discretion
- Exact file layout for typed errors (`platform/storage/errors.py` vs inline in `postgres_tables.py`), provided the listed typed errors exist and are importable.
- Whether the `Protocol` describing the storage contract lives in `platform/storage/protocols.py` or inline in `postgres_tables.py` — as long as it is a single source of truth used by both stores.
- Exact SQL shape in `config/schemas/annuity_performance/*.sql` (column types, nullability, primary keys) — must be consistent with the row dicts produced by the existing publication pipeline and with the legacy reference tables' observable shape (no business-semantics drift).
- Normalization strategy for `APPEND_ONLY` row ordering in the read-back diff (sort by source-row anchor or by a stable composite key) — provided the diff remains deterministic and documented in the test docstring.
- Whether the `transaction()` context manager lives on `PostgresTableStore` itself or on a tiny sibling helper, provided the whole-run-one-txn invariant (D-10) holds.
- Exact CLI output format (JSON vs human-friendly) for `publish annuity-performance` — must include `run_id` as the first stable field either way.

### Deferred Ideas (OUT OF SCOPE)

- PostgreSQL-backed tracing adapter (`platform/tracing/postgres_trace_store.py`) — deferred to a later phase; pilot keeps the current trace runtime unchanged.
- PostgreSQL-backed evidence adapter (`governance/evidence_index/postgres_store.py`) — deferred; pilot uses file-backed evidence only.
- Schema migration framework (Alembic or equivalent) — deferred; DDL in Phase 6 is hand-rolled idempotent SQL, applied by the operator.
- Auto-creation of tables / auto-migration on version bump — deferred; fail-closed schema snapshot is the pilot's gate.
- PG adapters for other domains (`annuity_income`, `annual_award`, `annual_loss`) — deferred; their publication policy entries already exist and will be picked up in follow-on phases that expand `RUN-01a` toward the full `RUN-01`.
- Batch / manifest-driven publish command — deferred; pilot is one-workbook-per-invocation.
- `--run-id` override for publish command — deferred; auto-generated is sufficient for pilot.
- Per-transaction-group rollback granularity (one PG txn per `transaction_group`) — evaluated and explicitly rejected for the pilot (see D-10); can be revisited if a future phase needs partial-snapshot semantics.
- Operator dashboards / self-service UI — v2 UX-01.
- Queue / retry runtime for large publish backlogs — v2 RUN-02.
- Additional publication channels (S3, object store, external warehouse) — v2 RUN-03.
- Profile-driven hot-path scanning on the PG write path — future phase, own discuss/plan cycle.
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| RUN-01a | Single-domain (`annuity_performance`) PostgreSQL publication adapter can publish all four domain targets from one real workbook, under a single transaction, with a fail-closed schema gate and a typed error surface. [VERIFIED: local file] | Standard Stack, Architecture Patterns, Common Pitfalls, Validation Architecture, Security Domain all specify the adapter seam, transaction model, schema validation, typed errors, and test path. [VERIFIED: local file] |
| RUN-01 | Support production-grade persistent storage/tracing adapters beyond in-memory replay mode. [VERIFIED: local file] | This phase only pilots publication storage for one domain and leaves tracing/evidence adapters open; planner should map this as partial predecessor coverage, not closure. [VERIFIED: local file] |
</phase_requirements>

## Summary

本阶段不是“做一个通用数据库层”，而是要在既有 `annuity_performance` 真实工作簿链路上，证明一条最小但真实的“工作簿输入 -> 既有 capability 流水线 -> PostgreSQL 发布”运行路径，且不触碰上游业务语义实现。现有代码已经把 Phase 6 最重要的复用点准备好了：`PublicationService` 负责 bundle 执行、`InMemoryTableStore` 定义了最小写接口、`replay` CLI 已经有 Typer 子组模式、`tests/integration/test_publication_service.py` 已经把 typed error 与 fail-fast 的风格固定下来了。 [VERIFIED: codebase grep] [VERIFIED: local file]

从规划角度，最关键的不是“怎么把 SQL 写出来”，而是把边界收窄并保持一致：PG 适配器只能落在 `platform/storage/`；`PublicationService` 只能做一个最小 Protocol 抽象；`publish` CLI 只能做 orchestration，不承载业务规则；回放（replay）仍然是真相源，PG 只接受 replay 结果对账。这个边界与架构蓝图中“publication/storage 属于 platform runtime、business semantics 不能落到 apps/platform helper”完全一致。 [CITED: https://www.postgresql.org/docs/current/infoschema-columns.html] [CITED: https://typer.tiangolo.com/tutorial/subcommands/add-typer/] [VERIFIED: local file]

真正需要提前在计划里锁死的风险有五类：psycopg v3 默认隐式事务、长连接 `idle in transaction`、schema 校验只靠 `information_schema.columns` 时的比较维度、`APPEND_ONLY` 对读回 diff 的稳定排序、以及 Docker 不可用时 testcontainers 集成测试必须 skip 而不是 fail。若计划不先把这些点变成任务与验收条件，执行阶段很容易出现“代码能跑，但语义边界、事务边界或 CI 期望不真实”的返工。 [CITED: https://www.psycopg.org/psycopg3/docs/basic/transactions.html] [CITED: https://www.postgresql.org/docs/current/infoschema-columns.html] [CITED: https://docs.pytest.org/en/stable/how-to/skipping.html] [CITED: https://testcontainers-python.readthedocs.io/]

**Primary recommendation:** 以“最小 Protocol + `PostgresTableStore` + `publish` 子命令 + PG 读回对 replay diff 的单一集成测试”为主线规划，避免任何超出 pilot 的抽象扩张。 [VERIFIED: local file]

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Workbook path intake and operator CLI invocation | Execution adapters | Business capabilities | `apps/etl_cli/main.py` 已经承载 CLI 入口；工作簿读取仍委托 `source_intake` 服务。 [VERIFIED: local file] |
| Workbook parsing and input contract enforcement | Business capabilities | Platform runtime | `AnnuityPerformanceIntakeService.read_batch()` 读取 workbook 并调用 `validate_input_batch` / `validate_input_record`。 [VERIFIED: local file] |
| Publication policy resolution | Platform runtime | Governance control plane | `load_publication_policy()` 位于 `platform/publication/service.py`，读取 `config/policies/publication.json`。 [VERIFIED: local file] |
| PostgreSQL write execution | Platform runtime | Database / Storage | PostgreSQL adapter 属于 `platform/storage/`，是技术存储职责，不是 capability 业务规则。 [VERIFIED: local file] [CITED: https://www.psycopg.org/psycopg3/docs/basic/transactions.html] |
| Transaction scoping across four targets | Platform runtime | Database / Storage | `PublicationService.execute()` 是单一 bundle 循环注入点，最适合包裹 whole-run transaction。 [VERIFIED: local file] |
| Schema preflight validation | Platform runtime | Database / Storage | 这是 adapter 边界上的 fail-closed contract check，应查询 `information_schema.columns` 而不是下沉到 capability。 [CITED: https://www.postgresql.org/docs/current/infoschema-columns.html] [VERIFIED: local file] |
| Contract-state and monthly-snapshot derivation | Business capabilities | Platform runtime | `ContractStateProjection` / `MonthlySnapshotProjection` 属于 `capabilities/projections/`，不能迁入 PG adapter。 [VERIFIED: local file] |
| Replay parity truth and diff evidence | Governance control plane | Execution adapters | replay acceptance suite 是语义真相源；Phase 6 只做 PG 读回对账，不重建第二真相源。 [VERIFIED: local file] |
| PostgreSQL integration test orchestration | Tests / Execution adapters | Platform runtime | testcontainers + pytest fixture 属于测试编排，不属于生产 runtime。 [CITED: https://testcontainers-python.readthedocs.io/] [CITED: https://docs.pytest.org/en/stable/how-to/skipping.html] |

## Project Constraints (from CLAUDE.md)

- 保持 capability-first 边界，不要退回 stage-first、hook-centric 或 generic helper 中心结构。 [VERIFIED: local file]
- 业务语义必须留在 `capabilities/`，不要放进 CLI、publication helper、storage adapter 或 governance code。 [VERIFIED: local file]
- `uv` 是仓库唯一要求的环境/依赖/命令管理方式；依赖变更时 `pyproject.toml` 与 `uv.lock` 必须一起提交。 [VERIFIED: local file]
- 代码和计划应追求最小可行变更，不做未要求的可配置化、工厂、注册表或预留抽象。 [VERIFIED: local file]
- 测试开发期间跑最窄相关集，声称完成前必须跑 `uv run pytest -v` 全量。 [VERIFIED: local file]
- Phase / slice 工作要优先走单一明确验证切片；如果跨边界，必须能解释其 slice 合理性。 [VERIFIED: local file]
- 本阶段不应碰 `platform/tracing/*`、`governance/evidence_index/*` 等已被上游上下文明确排除的边界。 [VERIFIED: local file]

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| psycopg | 3.3.3 (released 2026-02-18) [VERIFIED: PyPI] | PostgreSQL sync driver for `PostgresTableStore` | 官方文档明确支持 connection context manager、`conn.transaction()` 与同步事务控制，最贴近当前同步 `PublicationService.execute()` 形态。 [VERIFIED: PyPI] [CITED: https://www.psycopg.org/psycopg3/docs/basic/transactions.html] |
| typer | 0.24.1 (released 2026-02-21) [VERIFIED: PyPI] | `publish` 子命令组 | 当前仓库已依赖 Typer，且官方文档给出 `app.add_typer(...)` 子组模式，适合与现有 `replay` / `compatibility` 保持一致。 [VERIFIED: PyPI] [CITED: https://typer.tiangolo.com/tutorial/subcommands/add-typer/] [VERIFIED: local file] |
| pytest | 8.2,<9 pinned in repo; latest PyPI is 9.0.2 (2025-12-06) [VERIFIED: local file] [VERIFIED: PyPI] | Test runner | 仓库当前已用 pytest，Phase 6 只需沿用现有测试边界与 marker/skip 模式，不需要更换框架。 [VERIFIED: local file] [CITED: https://docs.pytest.org/en/stable/how-to/skipping.html] |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| testcontainers | 4.14.2 stable (released 2026-03-18) [VERIFIED: PyPI] | 启动隔离 PostgreSQL 容器做集成测试 | 用于 `tests/integration/test_postgres_publication_pilot.py` 的模块级 PG fixture。 [VERIFIED: PyPI] [CITED: https://testcontainers-python.readthedocs.io/] |
| openpyxl | `>=3.1,<4.0` in repo [VERIFIED: local file] | 真实 workbook 读取 | 现有 intake 服务已依赖它；Phase 6 不需要新增 workbook stack。 [VERIFIED: local file] |
| pydantic | `>=2,<3` in repo [VERIFIED: local file] | 现有 publication policy / contract validation style | 新 PG adapter 不需改 schema framework，但错误/配置风格应延续当前 typed contract 习惯。 [VERIFIED: local file] |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| psycopg sync API | SQLAlchemy / ORM | 与当前最小同步写接口不匹配，会引入不必要的 session/ORM 抽象，超出 pilot 目标。 [VERIFIED: local file] [ASSUMED] |
| `PostgresTableStore` + minimal Protocol | storage registry / factory | 当前只有一个新 adapter，工厂/注册表会违反项目“最小改动、无 speculative abstraction”约束。 [VERIFIED: local file] |
| testcontainers integration test | 手工依赖本地 PG 实例 | testcontainers 更容易复制一致环境；本地 PG 可留作 runbook 手工验证，不应成为自动化主路径。 [CITED: https://testcontainers-python.readthedocs.io/] [VERIFIED: local file] |

**Installation:**
```bash
uv add "psycopg[binary]>=3.2,<4"
uv add --dev "testcontainers[postgresql]"
uv add --dev pytest-docker
```
[VERIFIED: local file] [CITED: https://testcontainers.com/modules/postgresql/]

> Planning note: D-19 in `06-CONTEXT.md` is the locked source of truth for admitted test tooling, so Phase 6 plans preserve `testcontainers[postgresql]` plus `pytest-docker` (or equivalent) wording. If the actual package extra resolves as `testcontainers[postgres]` during execution, treat that as the implementation-time equivalent only after explicit verification.

**Version verification:**
- `psycopg` current PyPI release is `3.3.3` on 2026-02-18. [VERIFIED: PyPI]
- `testcontainers` current stable PyPI release is `4.14.2` on 2026-03-18. [VERIFIED: PyPI]
- `typer` current PyPI release is `0.24.1` on 2026-02-21. [VERIFIED: PyPI]
- Repo pins `pytest>=8.2,<9.0`, so planner should not silently upgrade to latest `9.0.2` inside this phase. [VERIFIED: local file] [VERIFIED: PyPI]

## Architecture Patterns

### System Architecture Diagram

```text
operator CLI: uv run python -m work_data_hub_pro.apps.etl_cli.main publish annuity-performance <workbook> <period>
  -> publish_app command parses positional args and generates run_id [VERIFIED: local file] [CITED: https://typer.tiangolo.com/tutorial/subcommands/add-typer/]
  -> AnnuityPerformanceIntakeService.read_batch() loads workbook rows [VERIFIED: local file]
  -> existing fact_processing / identity_resolution / reference_derivation pipeline runs unchanged [VERIFIED: local file]
  -> PublicationService builds/executes 4 publication bundles from config/policies/publication.json [VERIFIED: local file]
  -> PostgresTableStore.transaction() opens one transaction for whole run [CITED: https://www.psycopg.org/psycopg3/docs/basic/transactions.html] [VERIFIED: local file]
      -> first target use validates schema via information_schema.columns + committed *.schema.json snapshot [CITED: https://www.postgresql.org/docs/current/infoschema-columns.html] [VERIFIED: local file]
      -> refresh fact_annuity_performance
      -> upsert company_reference
      -> refresh contract_state
      -> append monthly_snapshot
  -> commit on success / rollback on first failure [CITED: https://www.psycopg.org/psycopg3/docs/basic/transactions.html]
  -> print run_id first in stdout output [VERIFIED: local file]
  -> integration test reads back four tables and diffs rows against replay output [VERIFIED: local file]
```

### Recommended Project Structure
```text
src/work_data_hub_pro/
├── platform/
│   ├── publication/
│   │   └── service.py                 # change ctor annotation + optional transaction seam
│   └── storage/
│       ├── in_memory_tables.py        # unchanged contract reference
│       ├── protocols.py               # minimal store protocol
│       ├── errors.py                  # typed PG adapter errors
│       └── postgres_tables.py         # new psycopg-backed adapter
├── apps/
│   └── etl_cli/
│       └── main.py                    # mount publish_app and command
config/
├── policies/
│   └── publication.json               # existing authoritative target policy
└── schemas/
    └── annuity_performance/
        ├── fact_annuity_performance.sql
        ├── fact_annuity_performance.schema.json
        ├── company_reference.sql
        ├── company_reference.schema.json
        ├── contract_state.sql
        ├── contract_state.schema.json
        ├── monthly_snapshot.sql
        └── monthly_snapshot.schema.json
tests/
├── integration/
│   ├── test_publication_service.py    # existing pattern anchor
│   └── test_postgres_publication_pilot.py
└── contracts/
    └── test_phase6_pytest_markers.py  # optional marker registration / docs contract check [ASSUMED]
docs/
└── runbooks/
    └── publish-annuity-performance.md
```
[VERIFIED: local file] [ASSUMED]

### Pattern 1: 最小存储协议注入到 `PublicationService`
**What:** 用 `typing.Protocol` 把 `refresh` / `upsert` / `append` / `read` 和可选 `transaction()` 抽成最小接口。 [VERIFIED: local file]
**When to use:** 当 `PublicationService` 需要继续服务 in-memory replay 与新 PG adapter，但又不引入工厂/注册表时。 [VERIFIED: local file]
**Example:**
```python
from contextlib import nullcontext
from typing import Protocol

class TableStore(Protocol):
    def refresh(self, target_name: str, rows: list[dict[str, object]]) -> int: ...
    def upsert(self, target_name: str, rows: list[dict[str, object]], *, key_fields: list[str]) -> int: ...
    def append(self, target_name: str, rows: list[dict[str, object]]) -> int: ...
    def read(self, target_name: str) -> list[dict[str, object]]: ...
    def transaction(self): ...

class PublicationService:
    def __init__(self, storage: TableStore) -> None:
        self._storage = storage

    def execute(self, bundles: list[PublicationBundle]) -> list[PublicationResult]:
        tx = getattr(self._storage, "transaction", None)
        with tx() if tx is not None else nullcontext():
            ...
```
// Source: current `PublicationService` and `InMemoryTableStore` seam [VERIFIED: local file]
```

### Pattern 2: Typer 子组挂载 `publish`
**What:** 复用当前 `app.add_typer(subapp, name=...)` 模式添加 `publish` 子组。 [VERIFIED: local file] [CITED: https://typer.tiangolo.com/tutorial/subcommands/add-typer/]
**When to use:** 当 Phase 6 需要增加一个 operator-facing 子命令且保持 CLI 风格统一时。 [VERIFIED: local file]
**Example:**
```python
app = typer.Typer(help="WorkDataHubPro replay utilities")
publish_app = typer.Typer(help="PostgreSQL publication commands")
app.add_typer(publish_app, name="publish")

@publish_app.command("annuity-performance")
def publish_annuity_performance(workbook: Path, period: str) -> None:
    ...
```
// Source: Typer add_typer docs + current `apps/etl_cli/main.py` [CITED: https://typer.tiangolo.com/tutorial/subcommands/add-typer/] [VERIFIED: local file]
```

### Pattern 3: PG adapter 只做技术写入与 schema gate
**What:** `PostgresTableStore` 负责连接、事务、DDL 预条件验证、SQL 写入；它不负责业务投影、不负责补字段、不负责 evidence。 [VERIFIED: local file] [CITED: https://www.postgresql.org/docs/current/infoschema-columns.html]
**When to use:** 所有 PostgreSQL 交互都经由 adapter，不要在 CLI 或 projection 里散落 SQL。 [VERIFIED: local file]
**Example:**
```python
with psycopg.connect(dsn) as conn:
    with conn.transaction():
        validate_table_schema(conn, schema="public", table="fact_annuity_performance")
        ...
```
// Source: psycopg transaction docs + PostgreSQL information_schema docs [CITED: https://www.psycopg.org/psycopg3/docs/basic/transactions.html] [CITED: https://www.postgresql.org/docs/current/infoschema-columns.html]
```

### Pattern 4: replay 仍然是真相源，PG 只做 read-back parity
**What:** 用 replay slice 产生的 publication rows 作为 expected，再从 PG 读回四张表做 deterministic diff。 [VERIFIED: local file]
**When to use:** 需要证明 PG adapter 没改变业务语义，但又不想复制第二套业务判定逻辑时。 [VERIFIED: local file]
**Example:**
```python
replay_outcome = run_annuity_performance_slice(...)
publish_cli(...)
assert stable_sort(pg_store.read("fact_annuity_performance")) == stable_sort(expected_rows)
```
// Source: current replay slice and Phase 6 context decision D-17/D-18 [VERIFIED: local file]
```

### Anti-Patterns to Avoid
- **在 `PublicationService` 上加工厂/registry/plugin system：** 当前只新增一个 adapter，工厂会制造无收益抽象。 [VERIFIED: local file]
- **在 PG adapter 中自动跑 DDL：** Phase 6 已锁定为 operator-applied DDL + fail-closed schema validation。 [VERIFIED: local file]
- **在 CLI 中直接写 SQL：** 这会把 platform storage 职责错放进 execution adapter。 [VERIFIED: local file]
- **把 projection 逻辑搬到数据库视图/SQL 中：** 蓝图要求业务语义留在 capability 层，Phase 6 也明确上游/投影语义不改。 [VERIFIED: local file]
- **让 PG 测试依赖开发者本机已有数据库：** 自动化基线路径应是 testcontainers；本地 PG 只适合手工 runbook。 [CITED: https://testcontainers-python.readthedocs.io/] [VERIFIED: local file]

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| PostgreSQL driver abstraction | 自己封装 DB-API mini driver | psycopg v3 sync API | 官方已提供连接/事务/错误语义；自封装只会重复踩事务坑。 [CITED: https://www.psycopg.org/psycopg3/docs/basic/transactions.html] |
| CLI subcommand framework | 自写 argparse hierarchy | Typer subgroup via `add_typer()` | 仓库已在用 Typer，风格和帮助输出已稳定。 [VERIFIED: local file] [CITED: https://typer.tiangolo.com/tutorial/subcommands/add-typer/] |
| PostgreSQL integration environment | 手工脚本起停本地 DB | testcontainers PostgreSQL module | 官方文档就是为 Docker-based integration testing 设计。 [CITED: https://testcontainers-python.readthedocs.io/] |
| Skip logic when Docker unavailable | 自己吞异常伪装通过 | pytest `skipif` / `pytest.skip()` | 官方 pytest 已定义标准跳过模式。 [CITED: https://docs.pytest.org/en/stable/how-to/skipping.html] |
| Schema shape discovery | ad hoc `SELECT * LIMIT 0` 解析列 | `information_schema.columns` | 官方 schema metadata 视图更适合按 schema/table 校验列快照。 [CITED: https://www.postgresql.org/docs/current/infoschema-columns.html] |

**Key insight:** 这一 phase 真正复杂的不是“写入 PostgreSQL”，而是“在不破坏现有 replay truth 和 capability 边界的前提下，让事务、schema gate、CLI、测试都可操作且可验证”；这些都已有成熟机制，不值得手写替代。 [VERIFIED: local file] [CITED: https://www.psycopg.org/psycopg3/docs/basic/transactions.html] [CITED: https://docs.pytest.org/en/stable/how-to/skipping.html]

## Common Pitfalls

### Pitfall 1: psycopg 默认隐式开启事务
**What goes wrong:** 执行第一条 SQL 后连接已进入事务，但代码没有明确 commit/rollback 语义，最终出现长事务或异常后连接卡在 failed transaction state。 [CITED: https://www.psycopg.org/psycopg3/docs/basic/transactions.html]
**Why it happens:** psycopg 文档明确说明“any database operation will start a new transaction”。 [CITED: https://www.psycopg.org/psycopg3/docs/basic/transactions.html]
**How to avoid:** 把 whole-run 包在一个显式 transaction context 内，并在 adapter 内集中处理 rollback。 [CITED: https://www.psycopg.org/psycopg3/docs/basic/transactions.html] [VERIFIED: local file]
**Warning signs:** SELECT-only preflight 后连接长时间 idle；一次写失败后后续 SQL 全报 transaction aborted。 [CITED: https://www.psycopg.org/psycopg3/docs/basic/transactions.html] [ASSUMED]

### Pitfall 2: 把 whole-run transaction 错做成每个 target 一次提交
**What goes wrong:** 第一个或第二个 target 已落库，后续 target 失败时出现部分写入残留。 [VERIFIED: local file]
**Why it happens:** 现有 `PublicationService.execute()` 是逐 bundle 执行；如果不在外围加 transaction seam，就只能得到 fail-fast 而非 rollback。 [VERIFIED: local file]
**How to avoid:** 在 `PublicationService.execute()` 的 bundle loop 外层统一包 transaction。 [VERIFIED: local file]
**Warning signs:** 回滚测试后四张表里仍有 `fact_annuity_performance` 或 `company_reference` 数据。 [VERIFIED: local file]

### Pitfall 3: schema 校验只比较列名，不比较顺序/空值/类型
**What goes wrong:** 表存在但形状漂移，写入或读回 diff 在运行时才暴露。 [CITED: https://www.postgresql.org/docs/current/infoschema-columns.html]
**Why it happens:** `information_schema.columns` 返回的不只是 `column_name`，还包含 `ordinal_position`、`is_nullable`、`data_type`、`udt_name` 等；若 planner 只要求列名集合，校验会太弱。 [CITED: https://www.postgresql.org/docs/current/infoschema-columns.html]
**How to avoid:** schema snapshot 至少比较 `column_name`、`ordinal_position`、`is_nullable`，必要时再比较 `data_type` / `udt_name`。 [CITED: https://www.postgresql.org/docs/current/infoschema-columns.html] [ASSUMED]
**Warning signs:** DDL 改过但 `.schema.json` 没同步，或 snapshot diff 只能看出“列数相同”。 [VERIFIED: local file] [ASSUMED]

### Pitfall 4: `APPEND_ONLY` 读回 diff 因行序不稳定而假失败
**What goes wrong:** 数据语义相同，但 PG `SELECT` 默认无排序保证，导致与 replay 结果逐行比较失败。 [VERIFIED: local file] [ASSUMED]
**Why it happens:** 当前 replay slice 已经用 `_sorted_payload()` 通过 JSON key 排序做 deterministic payload 比较。 [VERIFIED: local file]
**How to avoid:** 对 `monthly_snapshot` 读回结果做文档化稳定排序，再比较。 [VERIFIED: local file]
**Warning signs:** 同一测试重复跑时 diff 顺序变化，但字段值集合不变。 [ASSUMED]

### Pitfall 5: projection 仍然硬耦合 `InMemoryTableStore`
**What goes wrong:** planner 误以为只改 `PublicationService` 就足够，但 `ContractStateProjection` 和 `MonthlySnapshotProjection` 构造函数也直接依赖 `InMemoryTableStore`。 [VERIFIED: local file]
**Why it happens:** 两个 projection 当前都从 `platform.storage.in_memory_tables.InMemoryTableStore` 导入并注解。 [VERIFIED: local file]
**How to avoid:** planner 必须显式决定：要么把 projection 构造参数也切到同一 Protocol，要么保证 PG publish command 只在 publication 阶段使用 PG 而投影仍通过 in-memory intermediate store 再发布。基于 D-02/D-10，前者更一致。 [VERIFIED: local file] [ASSUMED]
**Warning signs:** publish command 无法把 `contract_state` / `monthly_snapshot` 从 PG 路径跑通，或需要额外复制投影输入。 [VERIFIED: local file] [ASSUMED]

### Pitfall 6: Docker 不可用时把集成测试当失败而非跳过
**What goes wrong:** 开发机或 CI 某层没有 Docker，Phase 6 自动化测试全红，阻塞非 PG 相关工作。 [CITED: https://testcontainers-python.readthedocs.io/] [CITED: https://docs.pytest.org/en/stable/how-to/skipping.html]
**Why it happens:** testcontainers 依赖 Docker daemon；pytest 官方推荐在外部依赖缺失时 skip。 [CITED: https://testcontainers-python.readthedocs.io/] [CITED: https://docs.pytest.org/en/stable/how-to/skipping.html]
**How to avoid:** fixture 启动前探测 Docker，不可用则 `pytest.skip()`；并为 Phase 6 增加 `postgres` marker。 [CITED: https://docs.pytest.org/en/stable/how-to/skipping.html] [VERIFIED: local file]
**Warning signs:** 本机无 Docker 时测试报 import/connection error，而不是 clean skip。 [ASSUMED]

## Code Examples

Verified patterns from official sources and current codebase:

### Typer subgroup mounting
```python
app = typer.Typer(help="WorkDataHubPro replay utilities")
publish_app = typer.Typer(help="PostgreSQL publication commands")
app.add_typer(publish_app, name="publish")
```
// Source: current `src/work_data_hub_pro/apps/etl_cli/main.py` + Typer docs [VERIFIED: local file] [CITED: https://typer.tiangolo.com/tutorial/subcommands/add-typer/]
```

### Existing in-memory store contract to mirror
```python
class InMemoryTableStore:
    def refresh(self, target_name: str, rows: list[dict[str, object]]) -> int: ...
    def upsert(self, target_name: str, rows: list[dict[str, object]], *, key_fields: list[str]) -> int: ...
    def append(self, target_name: str, rows: list[dict[str, object]]) -> int: ...
    def read(self, target_name: str) -> list[dict[str, object]]: ...
```
// Source: `src/work_data_hub_pro/platform/storage/in_memory_tables.py` [VERIFIED: local file]
```

### Existing fail-fast publication execution seam
```python
for bundle in bundles:
    try:
        if bundle.plan.mode is PublicationMode.REFRESH:
            affected_rows = self._storage.refresh(...)
        elif bundle.plan.mode is PublicationMode.UPSERT:
            affected_rows = self._storage.upsert(...)
        else:
            affected_rows = self._storage.append(...)
    except Exception as exc:
        raise PublicationExecutionError(...)
```
// Source: `src/work_data_hub_pro/platform/publication/service.py` [VERIFIED: local file]
```

### PostgreSQL schema validation query shape
```sql
SELECT table_schema, table_name, column_name, ordinal_position,
       is_nullable, data_type, udt_name, column_default
FROM information_schema.columns
WHERE table_schema = %s
  AND table_name = %s
ORDER BY ordinal_position;
```
-- Source: PostgreSQL official docs for `information_schema.columns` [CITED: https://www.postgresql.org/docs/current/infoschema-columns.html]
```

### psycopg transaction context pattern
```python
with psycopg.connect(dsn) as conn:
    with conn.transaction():
        ...
```
// Source: Psycopg 3 transactions docs [CITED: https://www.psycopg.org/psycopg3/docs/basic/transactions.html]
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| `PublicationService` constructor typed to `InMemoryTableStore` only [VERIFIED: local file] | minimal Protocol seam for multiple store implementations [VERIFIED: local file] | Phase 6 plan target [VERIFIED: local file] | enables PG pilot without refactoring publication semantics. [VERIFIED: local file] |
| in-memory only publication writes during replay [VERIFIED: local file] | pilot PostgreSQL publication path for one domain [VERIFIED: local file] | Phase 6 admission on 2026-04-19 [VERIFIED: local file] | proves RUN-01a while leaving RUN-01 open. [VERIFIED: local file] |
| no DB-backed integration path in tests [VERIFIED: local file] | testcontainers-backed PostgreSQL integration test [VERIFIED: local file] | Phase 6 scope decision [VERIFIED: local file] | gives a realistic operator-visible write path. [VERIFIED: local file] |

**Deprecated/outdated:**
- Treating `InMemoryTableStore` as the only publication-store contract is outdated for this phase because `PublicationService` is currently the narrowest reusable seam and PG pilot must flow through it. [VERIFIED: local file]
- Relying on local developer PostgreSQL as the primary automated test substrate is outdated for this phase; testcontainers is the planned authoritative automation path. [CITED: https://testcontainers-python.readthedocs.io/] [VERIFIED: local file]

## Pattern Analogs in the Codebase

| Need in Phase 6 | Existing Analog | Why It Matters |
|-----------------|----------------|----------------|
| Typed runtime errors | `PublicationPolicyError` and `PublicationExecutionError` in `platform/publication/service.py` [VERIFIED: local file] | PG adapter errors should mirror this boundary-specific typed style. [VERIFIED: local file] |
| Minimal in-memory storage seam | `InMemoryTableStore` [VERIFIED: local file] | PG adapter should mirror its public shape, not invent a new write contract. [VERIFIED: local file] |
| CLI subgroup wiring | `replay_app` / `compatibility_app` in `apps/etl_cli/main.py` [VERIFIED: local file] | `publish_app` should match this exact style. [VERIFIED: local file] |
| Deterministic payload normalization | `_sorted_payload()` in `annuity_performance_slice.py` [VERIFIED: local file] | reuse same idea for PG read-back parity, especially `APPEND_ONLY`. [VERIFIED: local file] |
| Fail-closed baseline loading | `_load_replay_baseline()` and `load_required_checkpoint_baseline()` [VERIFIED: local file] | Phase 6 schema snapshot gate should be similarly fail-closed. [VERIFIED: local file] |
| Integration-test negative path style | `tests/integration/test_publication_service.py` [VERIFIED: local file] | planner should model config error / mid-run failure / rollback assertions in the same file style. [VERIFIED: local file] |
| Projection storage read pattern | `ContractStateProjection.run()` / `MonthlySnapshotProjection.run()` [VERIFIED: local file] | planner must account for their current hard dependency on store `.read()` and likely protocolization need. [VERIFIED: local file] |

## Open Questions (RESOLVED)

1. **`ContractStateProjection` 和 `MonthlySnapshotProjection` 是否一并切到同一 storage Protocol？**
   - Resolution: **Yes.** Phase 6 的最小可执行 seam 不只覆盖 `PublicationService`，还覆盖这两个 projection 的构造参数类型；但改动严格限制在类型注解和导入，不改任何 projection 业务逻辑。这样可以避免 publish command 在 PG 路径里额外维护一套双存储搬运。 [VERIFIED: local file]

2. **`testcontainers[postgresql]` 还是 `testcontainers[postgres]`？**
   - Resolution: **Plans stay aligned to locked D-19 wording: `testcontainers[postgresql]` plus `pytest-docker` (or equivalent).** 官方模块页展示的 Python 安装写法是 `testcontainers[postgres]`，因此执行阶段可以把它当成待核验的实现等价物，但在 planning artifacts 里仍以 D-19 的 admitted tooling 名称为准，避免与锁定上下文冲突。 [CITED: https://testcontainers.com/modules/postgresql/]

3. **schema snapshot 要比较到什么粒度？**
   - Resolution: **Lock the comparison fields to `column_name`, `ordinal_position`, `is_nullable`, `data_type`, and `udt_name`.** 这组字段既能覆盖列名、顺序、可空性和具体类型，又能避开对环境差异更敏感的默认值细节；Phase 6 计划和实现都应按这五个字段做 fail-closed 比较。 [CITED: https://www.postgresql.org/docs/current/infoschema-columns.html]

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| `uv` | dependency sync, test execution | ✗ [VERIFIED: local env] | — | none; planner must treat local execution as blocked until installed. [VERIFIED: local env] |
| `python` | runtime + pytest + CLI | ✗ [VERIFIED: local env] | — | none; planner must not assume local test execution here. [VERIFIED: local env] |
| `docker` | testcontainers PostgreSQL integration tests | ✗ [VERIFIED: local env] | — | skip `postgres`-marked tests via pytest when unavailable. [VERIFIED: local env] [CITED: https://docs.pytest.org/en/stable/how-to/skipping.html] |
| `psql` | optional manual DB inspection / runbook smoke checks | ✗ [VERIFIED: local env] | — | use adapter `read()` in tests; psql remains optional for operators. [VERIFIED: local env] |
| `node` / `npm` | not required by Phase 6 runtime path | ✗ [VERIFIED: local env] | — | none needed. [VERIFIED: local env] |
| `gsd-sdk` | optional orchestration helper in agent docs | ✗ [VERIFIED: local env] | — | phase research and planning can proceed without it; do not depend on it in implementation tasks. [VERIFIED: local env] |

**Missing dependencies with no fallback:**
- `uv` for repo-standard dependency/test workflow. [VERIFIED: local env] [VERIFIED: local file]
- `python` for any local execution in this agent environment. [VERIFIED: local env]

**Missing dependencies with fallback:**
- `docker` for PG integration tests; automated tests should skip when unavailable, and planner can still specify the path truthfully. [VERIFIED: local env] [CITED: https://docs.pytest.org/en/stable/how-to/skipping.html]
- `psql` for manual inspection; integration assertions can rely on `PostgresTableStore.read()`. [VERIFIED: local env] [VERIFIED: local file]

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest `>=8.2,<9.0` in repo; latest PyPI is `9.0.2` but repo pin stays `<9`. [VERIFIED: local file] [VERIFIED: PyPI] |
| Config file | `E:\Projects\WorkDataHubPro\pyproject.toml` with `[tool.pytest.ini_options] addopts = "--basetemp=.pytest_tmp"`. [VERIFIED: local file] |
| Quick run command | `uv run pytest tests/integration/test_postgres_publication_pilot.py -v -m postgres` [VERIFIED: local file] [ASSUMED] |
| Full suite command | `uv run pytest -v` [VERIFIED: local file] |

### Phase Requirements → Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| RUN-01a | publish all four annuity targets to PG with one transaction | integration | `uv run pytest tests/integration/test_postgres_publication_pilot.py::test_publish_annuity_performance_writes_all_four_targets -v -m postgres` [ASSUMED] | ❌ Wave 0 |
| RUN-01a | fail when DSN missing | integration | `uv run pytest tests/integration/test_postgres_publication_pilot.py::test_postgres_store_requires_dsn -v -m postgres` [ASSUMED] | ❌ Wave 0 |
| RUN-01a | fail-closed on schema mismatch | integration | `uv run pytest tests/integration/test_postgres_publication_pilot.py::test_postgres_store_rejects_schema_mismatch -v -m postgres` [ASSUMED] | ❌ Wave 0 |
| RUN-01a | rollback whole run after seeded target failure | integration | `uv run pytest tests/integration/test_postgres_publication_pilot.py::test_publish_rolls_back_all_targets_on_mid_run_failure -v -m postgres` [ASSUMED] | ❌ Wave 0 |
| RUN-01 partial predecessor | replay remains parity truth | replay + integration | `uv run pytest tests/replay/test_annuity_performance_slice.py -v && uv run pytest tests/integration/test_postgres_publication_pilot.py -v -m postgres` [ASSUMED] | replay ✅ / pg ❌ Wave 0 |

### Sampling Rate
- **Per task commit:** 最窄相关集；例如 `uv run pytest tests/integration/test_publication_service.py -v` 或新的 PG pilot 集成模块。 [VERIFIED: local file] [ASSUMED]
- **Per wave merge:** `uv run pytest -v`。 [VERIFIED: local file]
- **Phase gate:** 全量 suite 绿色，且在有 Docker 的环境中 `postgres` 标记测试实际执行通过。 [VERIFIED: local file] [ASSUMED]

### Wave 0 Gaps
- [ ] `tests/integration/test_postgres_publication_pilot.py` — 覆盖 RUN-01a 主路径与负路径。 [VERIFIED: local file]
- [ ] pytest marker registration for `postgres` in repo config or `conftest.py` — 当前检索未发现现成 `postgres` marker。 [VERIFIED: codebase grep]
- [ ] testcontainers PostgreSQL fixture helper — 当前仓库暂无相关 fixture。 [VERIFIED: codebase grep]
- [ ] `config/schemas/annuity_performance/*.sql` 与 `*.schema.json` — 当前仓库无该目录。 [VERIFIED: local file] [ASSUMED]
- [ ] runbook `docs/runbooks/publish-annuity-performance.md`。 [VERIFIED: local file]

## Security Domain

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|-----------------|
| V2 Authentication | no | 本 phase 不实现应用级用户认证；数据库连接凭证仅从环境变量读取。 [VERIFIED: local file] |
| V3 Session Management | no | 不是会话型 Web 系统；关注点是 DB transaction 而非 user session。 [VERIFIED: local file] [ASSUMED] |
| V4 Access Control | yes | 使用最小数据库权限账户，只授予 Phase 6 目标 schema/table 所需权限。 [ASSUMED] |
| V5 Input Validation | yes | workbook 输入沿用现有 intake validators；schema gate 验证 DB 端前提。 [VERIFIED: local file] [CITED: https://www.postgresql.org/docs/current/infoschema-columns.html] |
| V6 Cryptography | yes | 不手写加密；凭证通过环境变量注入，TLS/连接加密交由 PostgreSQL/driver 配置。 [CITED: https://www.psycopg.org/psycopg3/docs/basic/usage.html] [ASSUMED] |

### Known Threat Patterns for Python + PostgreSQL publication path

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| SQL injection through dynamic table/column interpolation | Tampering | 表名来自受控 publication policy / schema snapshot，值参数一律走参数化 SQL。 [VERIFIED: local file] [ASSUMED] |
| Partial write residue after mid-run failure | Tampering | whole-run single transaction + fail-fast `PublicationExecutionError`. [VERIFIED: local file] [CITED: https://www.psycopg.org/psycopg3/docs/basic/transactions.html] |
| Writing into wrong schema/table | Tampering | `WDH_PG_SCHEMA` default `public` + explicit schema snapshot validation before first write. [VERIFIED: local file] [CITED: https://www.postgresql.org/docs/current/infoschema-columns.html] |
| Secret leakage via committed config | Information Disclosure | DSN only from env vars; never store in `config/`. [VERIFIED: local file] |
| Silent drift after operator DDL change | Repudiation / Tampering | committed `*.schema.json` snapshot + fail-closed mismatch error. [VERIFIED: local file] [CITED: https://www.postgresql.org/docs/current/infoschema-columns.html] |

## Assumptions Log

> List all claims tagged `[ASSUMED]` in this research. The planner and discuss-phase use this section to identify decisions that need user confirmation before execution.

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | ORM/SQLAlchemy would add unnecessary session/abstraction overhead for this pilot. | Standard Stack | Low — may affect rationale wording, not the locked decision to avoid ORM. |
| A2 | `uv add --dev "testcontainers[postgresql]"` is the exact install command shape to use. | Standard Stack | Medium — wrong extras name would break dependency install plan. |
| A3 | `PublicationExecutionError` after a failed transaction will commonly surface as aborted transaction / failed transaction state on subsequent SQL. | Common Pitfalls | Low — the mitigation still stands: rollback immediately. |
| A4 | Schema snapshot should at least compare `column_name`, `ordinal_position`, and `is_nullable`. | Common Pitfalls / Open Questions | Medium — too-weak or too-strong snapshot may create false pass/fail behavior. |
| A5 | `APPEND_ONLY` PG read-back ordering is unstable enough that explicit normalization is required. | Common Pitfalls | Low — planner can still include deterministic sort as a harmless safeguard. |
| A6 | The best Phase 6 shape is to protocolize projection constructor dependencies too, not just `PublicationService`. | Common Pitfalls / Open Questions | Medium — if false, planner may over-scope the seam. |
| A7 | `tests/contracts/test_phase6_pytest_markers.py` could be a useful optional contract test. | Recommended Project Structure | Low — optional only. |
| A8 | Suggested targeted pytest node names in Validation Architecture match the eventual test module structure. | Validation Architecture | Low — command strings may need adjustment when files are created. |
| A9 | V3 session management is not applicable because this is not a session-oriented web system. | Security Domain | Low — security section wording only. |
| A10 | Database least-privilege and parameterized SQL should be explicit Phase 6 controls even though current context does not state them verbatim. | Security Domain | Medium — if omitted, planner may under-specify DB hardening. |
| A11 | TLS/connection encryption should be handled by PostgreSQL/driver configuration rather than custom code. | Security Domain | Low — standard posture, but environment-specific. |
| A12 | Dynamic table/column interpolation can be fully constrained by publication policy and schema snapshots. | Security Domain | Medium — if planner allows arbitrary identifiers, SQL safety weakens. |

## Sources

### Primary (HIGH confidence)
- Current repository files under `E:\Projects\WorkDataHubPro\src\work_data_hub_pro\platform\publication\service.py`, `platform/storage/in_memory_tables.py`, `apps/etl_cli/main.py`, `capabilities/source_intake/annuity_performance/service.py`, `capabilities/projections/contract_state.py`, `capabilities/projections/monthly_snapshot.py`, `tests/integration/test_publication_service.py`, `tests/replay/test_annuity_performance_slice.py`, `config/policies/publication.json`, `pyproject.toml`. [VERIFIED: local file]
- [Psycopg 3 transactions docs](https://www.psycopg.org/psycopg3/docs/basic/transactions.html) - transaction behavior, context managers, autocommit caveats, idle-in-transaction warning. [CITED: https://www.psycopg.org/psycopg3/docs/basic/transactions.html]
- [PostgreSQL `information_schema.columns` docs](https://www.postgresql.org/docs/current/infoschema-columns.html) - schema validation metadata available per schema/table. [CITED: https://www.postgresql.org/docs/current/infoschema-columns.html]
- [Typer `add_typer()` docs](https://typer.tiangolo.com/tutorial/subcommands/add-typer/) - command subgroup pattern. [CITED: https://typer.tiangolo.com/tutorial/subcommands/add-typer/]
- [Pytest skipping docs](https://docs.pytest.org/en/stable/how-to/skipping.html) - canonical skip/skipif guidance for unavailable external dependencies. [CITED: https://docs.pytest.org/en/stable/how-to/skipping.html]
- [testcontainers-python docs](https://testcontainers-python.readthedocs.io/) - Docker-based integration testing requirement. [CITED: https://testcontainers-python.readthedocs.io/]
- PyPI project pages for `psycopg`, `testcontainers`, `typer`, and `pytest` used to verify current package versions and release dates. [VERIFIED: PyPI]

### Secondary (MEDIUM confidence)
- [Testcontainers PostgreSQL module page](https://testcontainers.com/modules/postgresql/) - confirms PostgreSQL module exists and shows Python install naming. [CITED: https://testcontainers.com/modules/postgresql/]

### Tertiary (LOW confidence)
- None. All unverified reasoning is called out as `[ASSUMED]`. [VERIFIED: local file]

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - core library choices are locked by context and verified against official docs / PyPI. [VERIFIED: local file] [VERIFIED: PyPI]
- Architecture: HIGH - reuse points and seam locations are visible in current codebase and align with the blueprint. [VERIFIED: local file]
- Pitfalls: MEDIUM - transaction and schema pitfalls are well documented, but exact SQL / snapshot granularity still needs implementation-time confirmation. [CITED: https://www.psycopg.org/psycopg3/docs/basic/transactions.html] [CITED: https://www.postgresql.org/docs/current/infoschema-columns.html]

**Research date:** 2026-04-19
**Valid until:** 2026-05-19 for codebase anchors; re-verify package versions and official docs if implementation starts later than 30 days. [VERIFIED: local file] [VERIFIED: PyPI]
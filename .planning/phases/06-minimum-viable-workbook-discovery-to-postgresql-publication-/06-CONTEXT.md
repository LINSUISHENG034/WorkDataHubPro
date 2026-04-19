# Phase 6: Minimum viable workbook discovery to PostgreSQL publication pilot - Context

**Gathered:** 2026-04-19
**Status:** Ready for planning

<domain>
## Phase Boundary

Phase 6 delivers the **minimum viable production runtime path** for a single domain: take one real `annuity_performance` Excel workbook from the operator, run it through the existing capability pipeline unchanged (`source_intake → fact_processing → identity_resolution → reference_derivation → projections → publication`), and persist the published rows into a real PostgreSQL database via a new storage adapter. This is a narrowly scoped pilot of the v2 runtime deferral recorded in Phase 5 (`Persistent / pluggable storage, tracing, evidence adapters beyond in-memory and file-backed — v2 RUN-01`).

**In scope:**
- One domain: `annuity_performance`
- All four publication targets for that domain: `fact_annuity_performance` (REFRESH), `company_reference` (UPSERT), `contract_state` (REFRESH), `monthly_snapshot` (APPEND_ONLY)
- New PostgreSQL storage adapter mirroring the existing `InMemoryTableStore` contract
- New `publish` Typer sub-group under `apps/etl_cli/main.py` with an `annuity-performance <workbook> <period>` command
- Hand-rolled DDL scripts under `config/schemas/annuity_performance/` with fail-closed startup validation
- Single-transaction semantics for a whole run (all four targets commit or rollback together)
- Acceptance evidence through a new integration test that reads PG contents back and diffs against replay output for the same workbook
- A new pilot-scoped requirement ID (`RUN-01a`) appended to `REQUIREMENTS.md` with traceability

**Out of scope (deferred to later phases or explicitly blocked):**
- Any change to `capabilities/source_intake/*`, `identity_resolution/*`, `reference_derivation/*`, `projections/*`, `fact_processing/*` implementations — intake and projections stay byte-identical
- PostgreSQL adapters for `platform/tracing/*` or `governance/evidence_index/*` — tracing keeps its current in-memory/file-artifact path and evidence stays file-backed (Phase 4 D-06 remains authoritative)
- Other domains (`annuity_income`, `annual_award`, `annual_loss`) — their policy entries already exist in `config/policies/publication.json` but are not exercised in Phase 6
- Operator dashboards or self-service UI (v2 UX-01)
- Queue / retry runtime or batch orchestration of multiple workbooks (v2 RUN-02)
- Additional publication channels beyond PostgreSQL (v2 RUN-03)
- Full v2 RUN-01 completion across all domains / all targets / all adapters — RUN-01 remains the broad v2 requirement; Phase 6 delivers only the scoped subset `RUN-01a`
- Any change to the replay CLI, replay acceptance suite, or `InMemoryTableStore`
- Secret management infrastructure (vault, secret store, etc.) — DSN is read from process env only
- Transactional rollback semantics for `InMemoryTableStore` (explicitly out of Phase 5; still out here)
- Alembic / SQLAlchemy / asyncpg or any ORM layer
- Schema migration / drift-recovery tooling beyond "schema snapshot matches, else fail-closed"
- Profile-driven hot-path scanning or additional performance baselines

</domain>

<decisions>
## Implementation Decisions

### A. Pilot slice boundary

- **D-01:** Pilot is locked to `annuity_performance` as the single domain. Architecture blueprint §7.3 names this as the first validation slice; it is also the domain with the richest existing capability coverage and the most stable replay baseline. No other domain gains a PG write path in Phase 6.
- **D-02:** All four publication targets for `annuity_performance` go through PostgreSQL: `fact_annuity_performance`, `company_reference`, `contract_state`, `monthly_snapshot`. This covers all three publication modes already modeled — `REFRESH`, `UPSERT`, `APPEND_ONLY` — so the adapter is proven against every mode the platform contracts describe.
- **D-03:** Upstream stages are byte-unchanged: `source_intake`, `fact_processing`, `identity_resolution`, `reference_derivation`, `projections`, `tracing`, and `governance/evidence_index/*`. The pilot is purely a publication-layer adapter insertion. Trace events remain in `platform/tracing/in_memory_trace_store.py`; evidence remains in the file-backed evidence index. Any temptation to "tidy up" adjacent modules is out of scope.

### B. PostgreSQL adapter shape

- **D-04:** Driver is **psycopg v3** (synchronous API). Rationale: lightweight, pydantic v2-compatible, same sync call style as the existing `PublicationService.execute` loop, no API-level changes elsewhere. No `asyncpg`, no SQLAlchemy, no psycopg2. Add `psycopg[binary]>=3.2,<4` as a runtime dependency in `pyproject.toml` and refresh `uv.lock`.
- **D-05:** New `PostgresTableStore` lives at `src/work_data_hub_pro/platform/storage/postgres_tables.py`. It mirrors the `InMemoryTableStore` public contract: `refresh(target_name, rows) -> int`, `upsert(target_name, rows, *, key_fields) -> int`, `append(target_name, rows) -> int`, plus a `read(target_name) -> list[dict]` helper used only by tests / read-back diffs.
- **D-06:** `PublicationService` is made storage-agnostic via a **minimum Protocol** (or equivalent `typing.Protocol`) in `platform/storage/` describing the three write operations. `PublicationService.__init__` accepts any object satisfying the protocol. Current `InMemoryTableStore` usage continues to work unchanged. This is a surgical seam — no refactor of publication, no new factory system, no "storage registry".
- **D-07:** Connection configuration is read **only from environment variables**. Primary: `WDH_PG_DSN` (explicit, project-scoped). Fallback: `DATABASE_URL` (industry standard). If both are absent, the adapter raises a typed `PostgresAdapterConfigError` at construction time (never silently falls back to in-memory). Optional `WDH_PG_SCHEMA` env var (default `public`) prefixes all table lookups. No secrets in `config/`, no `.env` loader inside the adapter.
- **D-08:** Schema management: hand-written **idempotent DDL scripts** under `config/schemas/annuity_performance/`. One file per target table (e.g. `fact_annuity_performance.sql`, `company_reference.sql`, `contract_state.sql`, `monthly_snapshot.sql`). Operators apply these scripts before first run (documented runbook step); the adapter does **not** auto-create tables. Legacy `E:\Projects\WorkDataHub\io\schema\migrations/versions/*` is a **reference for column shapes and indexes only** — do not copy Alembic infrastructure.
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

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Phase scope and acceptance

- `.planning/ROADMAP.md` — Phase 6 row and the overall phase sequencing that makes this a pilot, not a full adapter roll-out.
- `.planning/REQUIREMENTS.md` — v1/v2 requirements boundary; `RUN-01` (v2) is the broad requirement this pilot narrows; Phase 6 appends `RUN-01a`.
- `.planning/PROJECT.md` — constraints (parity, transparency, incremental delivery, agent operability, performance safety, brownfield reality), current-state notes, and the deferred-carry-forward list.
- `.planning/STATE.md` — admission note for Phase 6 and current workflow state.

### Prior phase decisions that constrain Phase 6

- `.planning/phases/05-performance-reliability-optimization-with-drift-safeguards/05-CONTEXT.md` — Phase 5 D-09/D-10/D-11/D-12 (Pydantic policy load + typed publication errors + fail-fast execute) define the style the PG adapter must match; D-14/D-15 define the CI tiers the new `postgres` marker plugs into; the deferred-ideas block names RUN-01 as the v2 requirement this phase pilot-answers.
- `.planning/phases/04-agent-operations-governance-hardening/04-CONTEXT.md` — file-backed evidence + lineage baseline (D-06) that Phase 6 must not disturb; runbook-alignment pattern (OPS-02) that shapes D-21.
- `.planning/phases/03-orchestration-refactor-failure-explainability/03-CONTEXT.md` — typed-diagnostic and CLI-subcommand conventions that `publish` must follow.
- `.planning/phases/02-transparent-pipeline-contracts-parity-gates/02-CONTEXT.md` — explicit publication contracts and CI tiering that the pilot reuses.
- `.planning/phases/02.1-phase-2-governance-remediation-truthful-gates-and-status-sync/02.1-CONTEXT.md` — truthful baseline contracts the replay acceptance suite relies on; Phase 6 must not weaken.

### Architecture and concerns

- `docs/superpowers/specs/2026-04-11-workdatahubpro-rebuild-architecture-draft.md` — §4.3 capability-first boundaries, §4.4 `publication`/`storage` as platform runtime services, §5.1 explicit publication/storage responsibilities, §6.3 publication-mode/transaction-scope contracts, §7.3 `annuity_performance` first-validation-slice anchor, §10 open question 1 (storage location for compatibility/evidence) that Phase 6 partially answers for publication output.
- `docs/superpowers/specs/2026-04-11-workdatahubpro-refactor-program.md` — refactor-wave ordering; confirms pilot-style incremental delivery over big-bang.
- `docs/superpowers/specs/2026-04-11-workdatahubpro-first-wave-legacy-coverage-matrix.md` — coverage expectations for the first-wave slice.
- `.planning/codebase/CONCERNS.md` — current structural concerns; specifically the publication-fragility surface that Phase 5 already addressed (do not re-open).
- `.planning/codebase/STRUCTURE.md` — current source tree; informs where `PostgresTableStore`, the storage Protocol, and the publish sub-command fit.
- `.planning/codebase/TESTING.md` — existing contract / integration / replay / performance tier layout that the new `postgres` marker extends.

### Code anchors

- `src/work_data_hub_pro/platform/publication/service.py` — `PublicationService.execute` is the single injection point; must accept any store satisfying the new storage Protocol.
- `src/work_data_hub_pro/platform/storage/in_memory_tables.py` — reference contract for `refresh` / `upsert` / `append` / `read`; the new `PostgresTableStore` mirrors this public shape.
- `src/work_data_hub_pro/platform/contracts/publication.py` — `PublicationMode`, `PublicationPlan`, `PublicationResult` — not modified in Phase 6; adapter must round-trip rows without altering these contracts.
- `src/work_data_hub_pro/apps/etl_cli/main.py` — the CLI root where the `publish` Typer sub-group is mounted; `replay_app` / `compatibility_app` are the structural precedents to mirror.
- `src/work_data_hub_pro/capabilities/source_intake/annuity_performance/service.py` — entry-point for workbook reads; not modified, but the `publish` command's workbook argument flows into this service.
- `config/policies/publication.json` — authoritative source for `annuity_performance` target names, modes, transaction groups, and idempotency scopes.
- `config/releases/` — existing release config directory; `config/schemas/` (new in Phase 6) follows the same "governed config under `config/`" convention.
- `tests/integration/test_publication_service.py` — reference style for publication-service integration tests (Phase 5 D-13 landed it).
- `tests/replay/annuity_performance/` — replay acceptance suite that defines parity truth for the pilot's read-back diff.
- `pyproject.toml` / `uv.lock` — Phase 6 adds `psycopg[binary]` runtime dep and `testcontainers[postgresql]` dev dep.

### Legacy reference (not source of truth)

- `E:\Projects\WorkDataHub\io\schema\migrations\versions\*.py` — Alembic migrations under the legacy repo. **Reference only** for column shapes / index choices / PK layout of the four target tables. Do **not** import Alembic, do not replicate the migration framework in Pro. DDL in Phase 6 is hand-rolled idempotent SQL, not migration scripts.

### Discipline references

- `docs/disciplines/implementation-execution.md` — execution rules for Phase 6 implementation tasks.
- `docs/disciplines/implementation-toolchain.md` — `uv` usage, lockfile updates for the new dependencies, command-style expectations for the new CLI sub-group.
- `docs/disciplines/implementation-slice-workflow.md` — contract-first slice discipline that Phase 6 (as a single-domain pilot) must respect.
- `docs/disciplines/implementation-verification.md` — full-suite verification expectations; the new `postgres` marker opts into the existing tiering.
- `docs/disciplines/git-workflow.md` — branch/commit discipline for the plan/execute cycle.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets

- `platform/publication/service.py::PublicationService` already loops over bundles and dispatches on `PublicationMode` — this is the seam where a `transaction()` context wraps the whole run with zero business-logic change.
- `platform/storage/in_memory_tables.py::InMemoryTableStore` is the functional template for `PostgresTableStore`; the method signatures (`refresh`, `upsert(key_fields=...)`, `append`, `read`) are stable and ported directly.
- `platform/contracts/publication.py::{PublicationMode, PublicationPlan, PublicationResult}` already encode what the adapter needs to honor — no new platform contracts required.
- `apps/etl_cli/main.py` already uses Typer sub-groups (`replay_app`, `compatibility_app`) mounted via `app.add_typer(...)` — the new `publish_app` follows the same pattern with zero scaffold work.
- `config/policies/publication.json` is already authoritative for target names / modes / transaction groups / idempotency scopes for `annuity_performance`; the PG adapter consumes the same policy without change.
- `tests/replay/annuity_performance/` is already the parity truth; the new integration test reuses replay bundles as the comparison source.

### Established Patterns

- Typed exception hierarchies at each platform boundary (Phase 3 / Phase 5 D-10) — the new `PostgresAdapterError` family follows this.
- Validate-at-boundary, never inside domain logic (Phase 4 / Phase 5 D-11) — schema-snapshot validation at `PostgresTableStore` startup matches.
- File-backed evidence / reference assets as the operational baseline (Phase 4 D-06) — evidence stays file-backed, tracing keeps its current in-memory/file-artifact flow, and PG is publication-only.
- Typer sub-group CLI style with per-domain commands (Phase 3) — `publish annuity-performance <workbook> <period>` mirrors `replay run <domain> <workbook> <period>` idioms.
- Replay acceptance suite as the single parity arbiter (Phase 5 D-08) — the pilot's read-back diff defers to it.
- Per-phase runbook under `docs/runbooks/` (Phase 4 OPS-02) — `publish-annuity-performance.md` follows this shape.
- Relative-threshold / deterministic comparison in test assertions (Phase 5 D-16) — the read-back diff is row-exact, not approximate.

### Integration Points

- `platform/publication/service.py` — accept the new storage Protocol; wrap the bundle loop in a store-provided `transaction()` context.
- `platform/storage/postgres_tables.py` — **new** file, `PostgresTableStore` implementation, `psycopg` connection lifecycle, schema snapshot validation, `transaction()` context manager.
- `platform/storage/protocols.py` (or inline) — **new** `StorageTableStore` Protocol with the four methods and an optional `transaction()` hook.
- `platform/storage/errors.py` — **new** typed-error module (or inline if kept minimal).
- `apps/etl_cli/main.py` — wire `publish_app` sub-group; add `annuity-performance` command with path + period args and auto-generated run_id.
- `apps/etl_cli/publish/` (optional helper package) — if the publish command's wiring grows past ~100 lines, extract to a sibling package under `etl_cli/` the way replay is structured. Claude's discretion.
- `config/schemas/annuity_performance/` — **new** directory holding the four DDL files and four `*.schema.json` column snapshots the adapter asserts against.
- `docs/runbooks/publish-annuity-performance.md` — **new** operator runbook (env var, DDL apply, testcontainers setup, sample invocation, teardown).
- `tests/integration/test_postgres_publication_pilot.py` — **new** integration test that runs the CLI against a testcontainers PG, reads the rows back, and diffs against replay bundles.
- `tests/integration/test_postgres_adapter_errors.py` — **new** negative-path coverage (missing DSN, schema mismatch, mid-run failure rolls back).
- `pyproject.toml` + `uv.lock` — add `psycopg[binary]>=3.2,<4` to runtime deps; add `testcontainers[postgresql]` to `dev`.

### Seams and constraints

- `PublicationService` currently type-annotates its constructor parameter as `InMemoryTableStore`. The Phase 6 seam is narrow: introduce a Protocol, change the annotation, no behavior change. Do **not** add a factory, registry, or plugin system.
- `platform/tracing/*` and `governance/evidence_index/*` must not be touched. If a plan task starts naming those paths, it is drifting from Phase 6 scope.
- `InMemoryTableStore` does not expose a `transaction()` hook; the new `Protocol` makes `transaction()` optional, and `PublicationService` only wraps the loop in a context when the injected store provides one (or unconditionally provides a no-op for in-memory). Either shape is acceptable; Claude's discretion between them.
- The four `schema.json` snapshots must stay in lock-step with the `*.sql` DDL — update both in the same commit when a column changes, enforced by the plan's acceptance criteria.

</code_context>

<specifics>
## Specific Ideas

- Phase 6 reads as "one new adapter file + one new CLI sub-group + one new test + four DDL files + one runbook" — five narrow strands, no scope creep. If a plan grows past that shape, something has drifted.
- The read-back diff against replay is the pilot's **only** business-semantics gate. Replay is the arbiter; PG output is the candidate. No second parity harness, no separate baseline.
- Transactional whole-run semantics are the operator mental model ("one publish = one atomic state transition"). Partial writes are a bug, not a mode.
- The adapter asserts preconditions on a real DB schema; it never mutates DDL. An operator (or the runbook) applies DDL first. This is the agent-operable contract.
- Secrets live in process env, never in `config/`. This is consistent with the project's "config/ is governed, not private" discipline.
- Typecontainers is the default for both local dev and CI — same test path in both places, no "works on my machine" drift.
- `RUN-01a` is explicitly **not** `RUN-01`. Broader v2 RUN-01 (multi-domain, multi-adapter, tracing + evidence + publication) stays open as the true v2 production-runtime goal.

</specifics>

<deferred>
## Deferred Ideas

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

</deferred>

---

*Phase: 06-minimum-viable-workbook-discovery-to-postgresql-publication*
*Context gathered: 2026-04-19*

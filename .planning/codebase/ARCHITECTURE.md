# Architecture

**Analysis Date:** 2026-04-12

## Pattern Overview

**Overall:** Capability-first layered architecture with explicit replay orchestration.

**Key Characteristics:**
- Keep business semantics in `src/work_data_hub_pro/capabilities/` services, not in adapters.
- Keep runtime contracts and write mechanics in `src/work_data_hub_pro/platform/`.
- Keep evidence indexing and compatibility adjudication in `src/work_data_hub_pro/governance/` and invoke them from orchestration after pipeline execution.

## Layers

**Execution Adapters Layer:**
- Purpose: Accept operator inputs and orchestrate end-to-end slice runs.
- Location: `src/work_data_hub_pro/apps/etl_cli/main.py`, `src/work_data_hub_pro/apps/orchestration/replay/*.py`
- Contains: Typer CLI commands, slice outcomes, orchestration sequence code.
- Depends on: All capability modules, platform services, governance services, config JSON, replay fixtures.
- Used by: CLI operators and replay tests in `tests/replay/`.

**Business Capabilities Layer:**
- Purpose: Implement intake, fact processing, identity resolution, derivation, and projections.
- Location: `src/work_data_hub_pro/capabilities/`
- Contains: Domain intake services, processors, enrichment logic, projections, capability protocols.
- Depends on: Platform contracts/models and selected platform storage in projections.
- Used by: Replay orchestration in `src/work_data_hub_pro/apps/orchestration/replay/*.py`.

**Platform Runtime Layer:**
- Purpose: Define contracts and run generic runtime services for publication, storage, tracing, lineage, and run context.
- Location: `src/work_data_hub_pro/platform/`
- Contains: Dataclass contracts, publication planning/execution, in-memory stores, lineage registry, trace store.
- Depends on: Standard library only.
- Used by: Capabilities and orchestration modules.

**Governance Control Layer:**
- Purpose: Persist evidence and emit compatibility adjudication cases when replay output diverges from accepted baseline.
- Location: `src/work_data_hub_pro/governance/`
- Contains: Compatibility case model, file-backed evidence index, adjudication service.
- Depends on: Platform trace contracts and standard library JSON/path handling.
- Used by: Replay orchestration modules.

**Configuration And Reference Assets Layer:**
- Purpose: Provide governed rule-pack activation, publication modes, and replay baseline/fixture assets.
- Location: `config/domains/`, `config/releases/`, `config/policies/`, `reference/historical_replays/`
- Contains: Cleansing configs, release bindings, publication policy map, expected replay snapshots, fixture rows.
- Depends on: Consumed by orchestration and manifest loaders.
- Used by: `CleansingManifest.load(...)` and replay slice runners.

## Data Flow

**Replay Slice Flow (`annuity_performance` / `annual_award` / `annual_loss`):**

1. CLI command in `src/work_data_hub_pro/apps/etl_cli/main.py` calls a replay function in `src/work_data_hub_pro/apps/orchestration/replay/`.
2. Orchestration runs intake (`capabilities/source_intake/*/service.py`) and builds `InputBatch` + `InputRecord` + intake trace events.
3. Orchestration loads cleansing manifest from `config/releases/*.json` + `config/domains/*/cleansing.json`, runs processor (`capabilities/fact_processing/*/service.py`), then identity resolution (`capabilities/identity_resolution/service.py`), and optional plan-code enrichment for event domains.
4. Orchestration records trace events in `platform/tracing/in_memory_trace_store.py` and writes per-row evidence via `governance/evidence_index/file_store.py`.
5. Orchestration registers lineage links in `platform/lineage/registry.py`, derives reference candidates (`capabilities/reference_derivation/service.py`), then publishes via `platform/publication/service.py` using `config/policies/publication.json`.
6. Orchestration runs projections (`capabilities/projections/contract_state.py`, `capabilities/projections/monthly_snapshot.py`), publishes projection outputs, compares monthly snapshot to `reference/historical_replays/<domain>/legacy_monthly_snapshot_2026_03.json`, and creates a compatibility case through `governance/adjudication/service.py` when mismatched.

**State Management:**
- Use explicit immutable dataclass contracts (`platform/contracts/models.py`, `platform/contracts/publication.py`) for flow payloads.
- Keep runtime mutable state in memory stores (`platform/storage/in_memory_tables.py`, `platform/tracing/in_memory_trace_store.py`, `platform/lineage/registry.py`).
- Persist replay evidence and adjudication artifacts as files under `reference/historical_replays/<domain>/evidence/`.

## Key Abstractions

**Core Contracts:**
- Purpose: Define stable runtime interfaces and handoff shapes between layers.
- Examples: `src/work_data_hub_pro/platform/contracts/models.py`, `src/work_data_hub_pro/platform/contracts/publication.py`
- Pattern: Frozen dataclasses for domain/runtime records.

**Replay Slice Runner (`run_<domain>_slice`):**
- Purpose: Compose end-to-end execution chain for each domain.
- Examples: `src/work_data_hub_pro/apps/orchestration/replay/annuity_performance_slice.py`, `src/work_data_hub_pro/apps/orchestration/replay/annual_award_slice.py`, `src/work_data_hub_pro/apps/orchestration/replay/annual_loss_slice.py`
- Pattern: Orchestrator function returning `SliceRunOutcome` dataclass.

**Cleansing Manifest:**
- Purpose: Bind code-defined rule packs to governed release/domain configs.
- Examples: `src/work_data_hub_pro/capabilities/fact_processing/cleansing/manifest.py`, `src/work_data_hub_pro/capabilities/fact_processing/cleansing/rules.py`
- Pattern: Code-owned rule semantics + config-driven activation order.

**Publication Planning + Execution:**
- Purpose: Enforce explicit mode, transaction group, and idempotency scope per target.
- Examples: `src/work_data_hub_pro/platform/publication/service.py`, `config/policies/publication.json`
- Pattern: Build `PublicationPlan` from policy, then execute `PublicationBundle` list.

## Entry Points

**Typer CLI App:**
- Location: `src/work_data_hub_pro/apps/etl_cli/main.py`
- Triggers: `uv run python -m work_data_hub_pro.apps.etl_cli.main replay-...`
- Responsibilities: Parse command args and dispatch to replay slice runners.

**Replay Orchestrators:**
- Location: `src/work_data_hub_pro/apps/orchestration/replay/annuity_performance_slice.py`, `src/work_data_hub_pro/apps/orchestration/replay/annual_award_slice.py`, `src/work_data_hub_pro/apps/orchestration/replay/annual_loss_slice.py`
- Triggers: CLI calls and replay tests in `tests/replay/`.
- Responsibilities: Execute ordered capability chain, publish outputs, create governance evidence/cases.

**Automated Verification Entry Points:**
- Location: `tests/contracts/`, `tests/integration/`, `tests/replay/`, `tests/performance/`
- Triggers: `uv run pytest -v` or targeted `uv run pytest tests/<path> -v`.
- Responsibilities: Enforce contract integrity, capability behavior, replay parity, and trace lookup SLO.

## Error Handling

**Strategy:** Fail fast for contract/config mismatches; persist evidence and open a compatibility case for output divergence.

**Patterns:**
- Raise `ValueError` during manifest load when domain rule-pack version does not match release (`src/work_data_hub_pro/capabilities/fact_processing/cleansing/manifest.py`).
- Treat replay baseline differences as adjudication events using `AdjudicationService.create_case(...)` instead of suppressing differences (`src/work_data_hub_pro/governance/adjudication/service.py`).

## Cross-Cutting Concerns

**Logging:** Not detected as a dedicated logging framework; runtime evidence relies on trace events plus file-backed evidence (`src/work_data_hub_pro/platform/tracing/in_memory_trace_store.py`, `src/work_data_hub_pro/governance/evidence_index/file_store.py`).
**Validation:** Enforce through dataclass contracts, config/release checks, and automated tests in `tests/contracts/` and `tests/replay/`.
**Authentication:** No active external auth flow in runtime; identity provider abstraction exists as protocol and static/in-memory implementations in `src/work_data_hub_pro/capabilities/identity_resolution/interfaces.py` and `src/work_data_hub_pro/capabilities/identity_resolution/service.py`.

---

*Architecture analysis: 2026-04-12*

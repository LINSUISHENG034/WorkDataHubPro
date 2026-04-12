# Codebase Structure

**Analysis Date:** 2026-04-12

## Directory Layout

```text
WorkDataHubPro/
|-- docs/                     # Architecture/spec/program/runbook/governance documentation
|-- config/                   # Domain cleansing config, release bindings, publication policy
|-- reference/                # Replay baselines, fixtures, and generated evidence artifacts
|-- src/work_data_hub_pro/    # Runtime package split by capabilities/platform/governance/apps
|-- tests/                    # Contract, integration, replay, and performance test suites
|-- pyproject.toml            # Python package/test/tool configuration
`-- uv.lock                   # Dependency lockfile for uv-managed environment
```

## Directory Purposes

**`docs/`:**
- Purpose: Hold active architecture baseline, refactor governance, discipline rules, slice plans/reviews, and replay runbooks.
- Contains: Markdown specs and process artifacts.
- Key files: `docs/superpowers/specs/2026-04-11-workdatahubpro-rebuild-architecture-draft.md`, `docs/superpowers/specs/2026-04-11-workdatahubpro-refactor-program.md`, `docs/runbooks/annuity-performance-replay.md`

**`config/`:**
- Purpose: Govern runtime behavior selection without embedding business logic in orchestration.
- Contains: Domain cleansing JSON, release JSON, publication policy JSON.
- Key files: `config/domains/annuity_performance/cleansing.json`, `config/domains/annual_award/cleansing.json`, `config/domains/annual_loss/cleansing.json`, `config/releases/2026-04-11-annuity-performance-baseline.json`, `config/policies/publication.json`

**`reference/`:**
- Purpose: Store accepted replay assets and generated evidence for explainability/adjudication.
- Contains: Historical replay fixtures, expected snapshots, `evidence/trace/`, `evidence/compatibility_cases/`.
- Key files: `reference/historical_replays/annuity_performance/legacy_monthly_snapshot_2026_03.json`, `reference/historical_replays/annual_award/customer_plan_history_2026_03.json`, `reference/historical_replays/annual_loss/annuity_performance_fixture_2026_03.json`

**`src/work_data_hub_pro/`:**
- Purpose: Application runtime package.
- Contains: `capabilities/`, `platform/`, `governance/`, `apps/` boundaries.
- Key files: `src/work_data_hub_pro/apps/etl_cli/main.py`, `src/work_data_hub_pro/platform/contracts/models.py`, `src/work_data_hub_pro/capabilities/fact_processing/cleansing/manifest.py`

**`tests/`:**
- Purpose: Enforce architecture and behavior through boundary-aligned automated tests.
- Contains: `contracts/`, `integration/`, `replay/`, `performance/`.
- Key files: `tests/contracts/test_system_contracts.py`, `tests/replay/test_annuity_performance_slice.py`, `tests/integration/test_publication_service.py`

## Key File Locations

**Entry Points:**
- `src/work_data_hub_pro/apps/etl_cli/main.py`: CLI command surface for replay execution.
- `src/work_data_hub_pro/apps/orchestration/replay/annuity_performance_slice.py`: Annuity-performance orchestrator.
- `src/work_data_hub_pro/apps/orchestration/replay/annual_award_slice.py`: Annual-award orchestrator.
- `src/work_data_hub_pro/apps/orchestration/replay/annual_loss_slice.py`: Annual-loss orchestrator.

**Configuration:**
- `config/policies/publication.json`: Publication mode and transaction group per target.
- `config/releases/*.json`: Release-level rule-pack version bindings.
- `config/domains/*/cleansing.json`: Domain activation order and enabled cleansing fields.

**Core Logic:**
- `src/work_data_hub_pro/capabilities/source_intake/*/service.py`: Workbook-to-record intake.
- `src/work_data_hub_pro/capabilities/fact_processing/*/service.py`: Domain fact transformations.
- `src/work_data_hub_pro/capabilities/identity_resolution/service.py`: Company ID resolution.
- `src/work_data_hub_pro/capabilities/reference_derivation/service.py`: Reference candidate derivation.
- `src/work_data_hub_pro/capabilities/projections/`: Contract-state and monthly-snapshot projections.
- `src/work_data_hub_pro/platform/publication/service.py`: Publication planning/execution.
- `src/work_data_hub_pro/governance/evidence_index/file_store.py`: File-backed evidence index.

**Testing:**
- `tests/contracts/`: Contract and governance doc/replay asset checks.
- `tests/integration/`: Capability and platform service integration tests.
- `tests/replay/`: End-to-end slice replay and explainability SLO validation.
- `tests/performance/test_trace_lookup_micro_benchmark.py`: Trace retrieval performance micro-benchmark.

## Naming Conventions

**Files:**
- Use `snake_case.py` for Python modules.
- Name domain processors/intake as `service.py` inside domain folders, e.g., `src/work_data_hub_pro/capabilities/source_intake/annual_loss/service.py`.
- Name orchestration modules as `<domain>_slice.py`, e.g., `src/work_data_hub_pro/apps/orchestration/replay/annual_award_slice.py`.

**Directories:**
- Keep top runtime boundaries fixed as `capabilities/`, `platform/`, `governance/`, `apps/` under `src/work_data_hub_pro/`.
- Keep domain-specific code nested one level below capability type when behavior is domain-bound, e.g., `src/work_data_hub_pro/capabilities/fact_processing/annual_award/`.
- Keep tests boundary-first (`tests/contracts`, `tests/integration`, `tests/replay`, `tests/performance`).

## Where to Add New Code

**New Feature:**
- Primary code: Add capability logic under `src/work_data_hub_pro/capabilities/<capability>/<domain>/` when domain-specific, or `src/work_data_hub_pro/capabilities/<capability>/` when cross-domain.
- Orchestration wiring: Add or extend replay runner in `src/work_data_hub_pro/apps/orchestration/replay/`.
- CLI exposure: Add command in `src/work_data_hub_pro/apps/etl_cli/main.py`.
- Tests: Add boundary-matching tests under `tests/integration/` and `tests/replay/`; add contract tests under `tests/contracts/` when data contracts/config policies change.

**New Component/Module:**
- Implementation: Use existing boundary directory first (`src/work_data_hub_pro/platform/` for runtime mechanics, `src/work_data_hub_pro/governance/` for evidence/adjudication, `src/work_data_hub_pro/capabilities/` for business semantics).

**Utilities:**
- Shared helpers: Place capability-scoped helpers beside the owning capability (example pattern: `src/work_data_hub_pro/capabilities/fact_processing/annual_loss/plan_code_lookup.py`).
- Avoid introducing generic catch-all utility folders; follow boundary ownership from `docs/superpowers/specs/2026-04-11-workdatahubpro-rebuild-architecture-draft.md`.

## Special Directories

**`.planning/codebase/`:**
- Purpose: Generated codebase mapping docs used by planning/execution workflows.
- Generated: Yes.
- Committed: Yes (project workflow artifact).

**`.pytest_tmp/`:**
- Purpose: Temporary pytest base temp directory configured in `pyproject.toml`.
- Generated: Yes.
- Committed: No.

**`.serena/`:**
- Purpose: Local Serena state and memories.
- Generated: Yes.
- Committed: No by default policy in `AGENTS.md`.

**`.worktrees/`:**
- Purpose: Local project worktree root for isolated branches.
- Generated: Yes.
- Committed: No.

---

*Structure analysis: 2026-04-12*

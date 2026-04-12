# External Integrations

**Analysis Date:** 2026-04-12

## APIs & External Services

**Third-party APIs:**
- Not detected in current runtime code under `src/work_data_hub_pro/`.
  - SDK/Client: Not applicable
  - Auth: Not applicable

**CLI-facing local interfaces:**
- Local workbook ingestion via CLI commands in `src/work_data_hub_pro/apps/etl_cli/main.py`.
  - SDK/Client: `typer` CLI command surface (`replay-annuity-performance`, `replay-annual-award`, `replay-annual-loss`)
  - Auth: Not applicable

## Data Storage

**Databases:**
- In-memory table storage only via `InMemoryTableStore` in:
  - `src/work_data_hub_pro/platform/storage/in_memory_tables.py`
  - consumers in replay slices under `src/work_data_hub_pro/apps/orchestration/replay/`
  - Connection: Not applicable
  - Client: Internal in-memory adapter (not external DB/ORM)

**File Storage:**
- Local filesystem only.
- Excel source files read using `openpyxl.load_workbook(...)` in:
  - `src/work_data_hub_pro/capabilities/source_intake/annuity_performance/service.py`
  - `src/work_data_hub_pro/capabilities/source_intake/annual_award/service.py`
  - `src/work_data_hub_pro/capabilities/source_intake/annual_loss/service.py`
- JSON replay fixtures loaded from `reference/historical_replays/...` in:
  - `src/work_data_hub_pro/apps/orchestration/replay/annuity_performance_slice.py`
  - `src/work_data_hub_pro/apps/orchestration/replay/annual_award_slice.py`
  - `src/work_data_hub_pro/apps/orchestration/replay/annual_loss_slice.py`
- Governance evidence and compatibility cases written to local files by `FileEvidenceIndex` in `src/work_data_hub_pro/governance/evidence_index/file_store.py`.

**Caching:**
- In-process memory cache only (`InMemoryIdentityCache`) in `src/work_data_hub_pro/capabilities/identity_resolution/service.py`.

## Authentication & Identity

**Auth Provider:**
- Custom internal identity resolution strategy, no external identity provider integration.
  - Implementation: `CacheFirstIdentityResolutionService` with `InMemoryIdentityCache` and `StaticIdentityProvider` in `src/work_data_hub_pro/capabilities/identity_resolution/service.py`.

## Monitoring & Observability

**Error Tracking:**
- None detected (no external error tracking SDK in `src/work_data_hub_pro/`).

**Logs:**
- CLI summary output via `typer.echo(...)` in `src/work_data_hub_pro/apps/etl_cli/main.py`.
- Trace/event evidence persisted as JSON via `FileEvidenceIndex` in `src/work_data_hub_pro/governance/evidence_index/file_store.py`.

## CI/CD & Deployment

**Hosting:**
- Not detected.

**CI Pipeline:**
- Not detected (`.github/workflows/` absent).

## Environment Configuration

**Required env vars:**
- None detected for current runtime path (`src/work_data_hub_pro/` has no `os.environ` or `getenv` access).

**Secrets location:**
- Not applicable for current runtime integration surface.

## Webhooks & Callbacks

**Incoming:**
- None.

**Outgoing:**
- None.

---

*Integration audit: 2026-04-12*

---
phase: 06
slug: minimum-viable-workbook-discovery-to-postgresql-publication
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-04-19
---

# Phase 06 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | `pytest >=8.2,<9` via `uv run pytest` |
| **Config file** | `pyproject.toml` |
| **Quick run command** | `uv run pytest tests/integration/test_postgres_publication_pilot.py -v -m postgres` |
| **Full suite command** | `uv run pytest -v` |
| **Estimated runtime** | ~240 seconds when Docker-backed PostgreSQL tests run |

---

## Sampling Rate

- **After every task commit:** Run the narrowest plan-specific command from the table below.
- **After every plan wave:** Run `uv run pytest tests/integration/test_postgres_publication_pilot.py -v -m postgres`.
- **Before `/gsd-verify-work`:** Run `uv run pytest -v`.
- **Max feedback latency:** 240 seconds.

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 06-01-01 | 01 | 1 | RUN-01a | T-06-01 / T-06-02 | Storage contract seams stay minimal and publication execution can wrap all four target writes in one transaction-capable store boundary without changing business semantics. | integration | `uv run pytest tests/integration/test_publication_service.py -v` | ✅ | ⬜ pending |
| 06-02-01 | 02 | 1 | RUN-01a | T-06-03 / T-06-04 | PostgreSQL adapter fails closed on missing DSN or schema mismatch and executes REFRESH / UPSERT / APPEND_ONLY writes through one typed adapter. | integration | `uv run pytest tests/integration/test_postgres_publication_pilot.py -v -m postgres` | ❌ W0 | ⬜ pending |
| 06-03-01 | 03 | 2 | RUN-01a | T-06-05 / T-06-06 | `publish annuity-performance` generates stable run identifiers, writes all four targets, and rolls back the whole run on seeded mid-run failure. | integration + cli | `uv run pytest tests/integration/test_postgres_publication_pilot.py -v -m postgres` | ❌ W0 | ⬜ pending |
| 06-04-01 | 04 | 2 | RUN-01a / RUN-01 | T-06-07 | Runbook, DDL snapshots, and replay-vs-PG read-back parity stay aligned and operator-usable without hidden setup. | integration + replay + contract | `uv run pytest tests/integration/test_postgres_publication_pilot.py tests/replay/test_annuity_performance_slice.py -v -m "postgres or not postgres"` | replay ✅ / pg ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `tests/integration/test_postgres_publication_pilot.py` — PostgreSQL pilot mainline and negative-path coverage
- [ ] PostgreSQL test fixture and `postgres` marker registration — Docker-aware skip behavior for unavailable hosts
- [ ] `config/schemas/annuity_performance/*.sql` — operator-applied idempotent DDL for all four targets
- [ ] `config/schemas/annuity_performance/*.schema.json` — committed schema snapshots used by fail-closed validation
- [ ] `docs/runbooks/publish-annuity-performance.md` — operator setup / run / teardown workflow

*Existing infrastructure covers the framework and runner requirements; Wave 0 is primarily new PostgreSQL test, schema, and runbook artifacts.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| A local operator can follow the runbook to apply DDL, export DSN env vars, run `publish annuity-performance`, and inspect the generated `run_id` without hidden setup. | RUN-01a | Automated tests can prove CLI behavior and DB writes, but not whether the documented operator sequence is coherent from a clean shell. | From a clean shell with Docker or a local PostgreSQL instance, follow `docs/runbooks/publish-annuity-performance.md`: apply all four SQL files, set `WDH_PG_DSN` (and optional `WDH_PG_SCHEMA`), run `uv run python -m work_data_hub_pro.apps.etl_cli.main publish annuity-performance <workbook> <period>`, confirm `run_id` is printed first, then inspect rows through the documented verification step. |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or existing test infrastructure support
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all missing verification references
- [ ] No watch-mode flags
- [ ] Feedback latency < 240s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending

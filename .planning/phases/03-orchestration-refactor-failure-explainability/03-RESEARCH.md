# Phase 3: Orchestration Refactor & Failure Explainability - Research

**Researched:** 2026-04-13 [VERIFIED: research session date]
**Domain:** Replay orchestration, typed failure contracts, agent CLI surface, and deterministic temporary identity fallback. [VERIFIED: `.planning/phases/03-orchestration-refactor-failure-explainability/03-CONTEXT.md`]
**Confidence:** MEDIUM [VERIFIED: research assessment]

<user_constraints>
## User Constraints (from CONTEXT.md)

Verbatim copy from `.planning/phases/03-orchestration-refactor-failure-explainability/03-CONTEXT.md`. [VERIFIED: `.planning/phases/03-orchestration-refactor-failure-explainability/03-CONTEXT.md`]

### Locked Decisions

### Shared replay composition
- **D-01:** Extract shared replay primitives, but keep explicit per-domain replay runners.
- **D-02:** The shared primitive boundary includes trace and lineage scaffolding, checkpoint construction, gate summarization, evidence package assembly, publication-plan helper usage, and the orchestration loop skeleton for intake, processing, and identity resolution.
- **D-03:** Domain-specific runner contracts remain explicit for intake service selection, processor selection, enrichment steps, replay asset loading, publication target wiring, rule manifests, and hook-sensitive behavior.
- **D-04:** Phase 3 explicitly rejects a single fully generic replay runner with domain adapters as the primary abstraction target.

### Failure contract
- **D-05:** Adopt a split failure contract: typed exceptions for preflight, config, and setup failures; typed run reports for completed runs that reach replay outcome evaluation.
- **D-06:** The minimum typed run-report fields are `comparison_run_id`, `overall_outcome`, `checkpoint_results`, `primary_failure`, `compatibility_case`, and `evidence_paths`.
- **D-07:** Replay mismatch outcomes must remain distinct from setup failures; Phase 3 must not collapse governed parity differences and invalid-run failures into one undifferentiated object.

### Agent entrypoints
- **D-08:** Keep the current human-facing domain wrappers: `replay-annuity-performance`, `replay-annual-award`, and `replay-annual-loss`.
- **D-09:** Add a unified agent-facing replay CLI v1 surface: `replay run --domain <domain> --workbook <path> --period <period>`, `replay diagnose --comparison-run-id <id>`, and `replay list-domains`.
- **D-10:** The minimum agent-facing output contract is `comparison_run_id`, `overall_outcome`, `primary_failed_checkpoint`, `evidence_root`, and `compatibility_case_id`.

### Temporary identity policy
- **D-11:** Replace `TEMP-{company_name}` with a deterministic opaque temp-identity contract.
- **D-12:** Use the legacy deterministic generation model as the reference: normalize before hashing, use HMAC-based deterministic generation with governed salt, and keep the generated `company_id` opaque.
- **D-13:** Allow one governed global temp-id prefix setting, default it to `IN`, and treat the prefix as a config-release compatibility parameter rather than a runtime convenience toggle.
- **D-14:** Empty or placeholder names return `None` instead of generating a shared fake temp id.
- **D-15:** Raw company names remain in sidecar evidence only; they must not appear in `company_id`.
- **D-16:** Recommended helper boundary for fallback identity is `generate_temp_identity(...)`, `is_temp_identity(...)`, `normalize_identity_fallback_input(...)`, and `temp_identity_prefix()`.

### the agent's Discretion
- Exact names and module locations for extracted replay primitive helpers, provided the shared-versus-explicit boundary above remains visible.
- Final typed exception class names and final CLI presentation formatting, provided the locked failure and output contracts above are preserved.
- Exact sequencing for updating tests, runbooks, and config wiring during implementation, provided compatibility-sensitive temp-id and replay-entrypoint behavior remain governed.

### Deferred Ideas (OUT OF SCOPE)
- Legacy-style replay/ETL execution parity such as `--all-domains`, file discovery controls, and DB diagnostics.
- Full `etl`, `operator`, and `adjudication` command trees beyond the replay CLI v1 surface.
- Final retain-or-replace decisions for `company_lookup_queue`, `reference_sync`, and manual `customer-mdm` surfaces.
- Broader future-domain generalization beyond first-wave needs, including treating `annuity_income` as a proof point for a fully generic replay runner.
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| PIPE-03 | System can surface failure paths with typed error categories and actionable diagnostics. [VERIFIED: `.planning/REQUIREMENTS.md`] | Freeze replay-specific setup exceptions, a serializable run-report, and a diagnose read path before refactoring slice bodies. [VERIFIED: `03-CONTEXT.md`][VERIFIED: repo code] |
| PIPE-04 | System can reduce duplicated replay orchestration by extracting reusable pipeline composition primitives. [VERIFIED: `.planning/REQUIREMENTS.md`] | Extract only invariant replay mechanics after the contract is fixed; keep domain wiring explicit. [VERIFIED: `03-CONTEXT.md`][VERIFIED: replay slice code] |
| OPS-01 | Agent can discover stable task entrypoints for replay execution, diagnostics, and rule updates without relying on hidden context. [VERIFIED: `.planning/REQUIREMENTS.md`] | Add one registry-backed replay command group plus evidence readers for `run`, `diagnose`, and `list-domains`. [VERIFIED: `03-CONTEXT.md`][VERIFIED: current CLI][CITED: https://typer.tiangolo.com/tutorial/subcommands/nested-subcommands/] |
| GOV-02 | Identity fallback behavior can avoid leaking raw business identifiers in generated temporary IDs. [VERIFIED: `.planning/REQUIREMENTS.md`] | Replace raw-name `TEMP-*` IDs with legacy-style normalized deterministic opaque IDs and placeholder-to-`None`. [VERIFIED: `03-CONTEXT.md`][VERIFIED: current repo code][VERIFIED: legacy repo code] |
</phase_requirements>

## Summary

Phase 3 should lock the replay-facing contracts before extracting helpers, because the current slice files duplicate one orchestration skeleton while also mixing public outcome fields, debug stores, evidence writing, and setup failure behavior in the same functions. [VERIFIED: `src/work_data_hub_pro/apps/orchestration/replay/annuity_performance_slice.py`][VERIFIED: `src/work_data_hub_pro/apps/orchestration/replay/annual_award_slice.py`][VERIFIED: `src/work_data_hub_pro/apps/orchestration/replay/annual_loss_slice.py`]

The correct refactor target is still "shared primitives, explicit runners": the loop shape is shared, but intake choice, enrichment, replay fixtures, release paths, and publication targets are materially different across the three accepted slices. [VERIFIED: `03-CONTEXT.md`][VERIFIED: replay slice code]

The biggest contract gap is explainability on the read side. Phase 2 already standardized comparison-run packages, but `FileEvidenceIndex` currently exposes only `load_case()`, so `replay diagnose --comparison-run-id <id>` cannot exist yet without new reader APIs. [VERIFIED: `src/work_data_hub_pro/governance/compatibility/gate_runtime.py`][VERIFIED: `src/work_data_hub_pro/governance/evidence_index/file_store.py`]

The temp-ID change is parity-sensitive, not cleanup. `WorkDataHubPro` still emits `TEMP-{company_name}` and raw-name evidence refs, while legacy current code normalizes names, uses HMAC-SHA1 plus Base32 for deterministic `IN...` IDs, and returns `None` for empty or placeholder names before temp-id assignment. [VERIFIED: `src/work_data_hub_pro/capabilities/identity_resolution/service.py`][VERIFIED: `E:\Projects\WorkDataHub\src\work_data_hub\infrastructure\enrichment\normalizer.py`][VERIFIED: `E:\Projects\WorkDataHub\src\work_data_hub\infrastructure\enrichment\resolver\backflow.py`]

**Primary recommendation:** Freeze `ReplayRunReport`, typed setup exceptions, a replay domain registry, and temp-id helper semantics first; then extract only the invariant replay mechanics; then add unified replay CLI commands on top of the same explicit runners. [VERIFIED: `03-CONTEXT.md`][VERIFIED: repo code]

## Project Constraints

- Preserve capability-first boundaries and keep business logic out of generic orchestration helpers. [VERIFIED: `AGENTS.md`][CITED: `docs/superpowers/specs/2026-04-11-workdatahubpro-rebuild-architecture-draft.md`]
- Use `uv` for runtime commands; current machine has `uv` and `uv`-managed Python, but plain `python` is not on PATH. [VERIFIED: `docs/disciplines/implementation-toolchain.md`][VERIFIED: local environment probe]
- Keep replay assets and runbooks aligned with behavior changes, and require `uv run pytest -v` before any completion claim. [VERIFIED: `AGENTS.md`][VERIFIED: `docs/disciplines/implementation-verification.md`]
- Plan cross-boundary work explicitly when it touches `apps`, `capabilities`, and `governance`. [VERIFIED: `docs/disciplines/implementation-slice-workflow.md`][VERIFIED: `docs/disciplines/git-workflow.md`]

## Standard Stack

### Core

| Component | Version | Purpose | Why Standard |
|-----------|---------|---------|--------------|
| Typer | `0.24.1` locked and installed. [VERIFIED: `uv.lock`][VERIFIED: `uv run python -c ...`] | Existing CLI surface in `src/work_data_hub_pro/apps/etl_cli/main.py`. [VERIFIED: repo code] | The repo already uses Typer, and official docs support nested command groups through `add_typer()`, which matches the locked `replay run/diagnose/list-domains` shape. [VERIFIED: current CLI][CITED: https://typer.tiangolo.com/tutorial/subcommands/nested-subcommands/] |
| `gate_models` + `gate_runtime` | Current repo modules. [VERIFIED: repo code] | Canonical checkpoint, gate summary, and comparison-run package schema. [VERIFIED: `src/work_data_hub_pro/governance/compatibility/gate_models.py`][VERIFIED: `src/work_data_hub_pro/governance/compatibility/gate_runtime.py`] | Phase 3 should reuse the accepted Phase 2 evidence package instead of inventing a second diagnostics schema. [VERIFIED: `.planning/phases/02-transparent-pipeline-contracts-parity-gates/02-CONTEXT.md`][VERIFIED: repo code] |
| `FileEvidenceIndex` | Current repo module. [VERIFIED: repo code] | File-backed evidence writer and the natural read-side extension point for `replay diagnose`. [VERIFIED: `src/work_data_hub_pro/governance/evidence_index/file_store.py`] | The current gap is missing readers, not missing storage. [VERIFIED: repo code] |
| Python stdlib `hmac` + `hashlib` + `base64` | Python `3.12` stdlib in the repo runtime. [VERIFIED: `pyproject.toml`][VERIFIED: local environment probe] | Deterministic opaque temp-id generation without new dependencies. [VERIFIED: legacy repo code] | Legacy current code already uses HMAC-SHA1 plus Base32 for `IN...` IDs, and Python documents `hmac` as the standard keyed-hash module. [VERIFIED: legacy repo code][CITED: https://docs.python.org/3/library/hmac.html] |

### Supporting

| Component | Version | Purpose | When to Use |
|-----------|---------|---------|-------------|
| `pytest` | `8.4.2` locked and installed. [VERIFIED: `uv.lock`][VERIFIED: `uv run pytest --version`] | Contract, integration, replay, and performance verification. [VERIFIED: `pyproject.toml`][VERIFIED: `tests/`] | Use for contract freezing first, then refactor parity regression across all accepted slices. [VERIFIED: repo test layout] |
| `openpyxl` | `3.1.5` locked and installed. [VERIFIED: `uv.lock`][VERIFIED: `uv run python -c ...`] | Workbook intake remains the live replay input boundary. [VERIFIED: source-intake services] | Keep workbook-backed tests in the plan so CLI and replay changes are not fixture-blind. [VERIFIED: replay tests] |
| `platform.contracts.validators` | Current repo module. [VERIFIED: repo code] | Existing structural validation for batch, record, trace, and publication-plan setup. [VERIFIED: `src/work_data_hub_pro/platform/contracts/validators.py`] | Wrap its current `ValueError` outputs into replay-specific setup exceptions instead of duplicating validation logic. [VERIFIED: repo code] |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Typer subcommand group under the existing app. [VERIFIED: current CLI][CITED: https://typer.tiangolo.com/tutorial/subcommands/nested-subcommands/] | Custom `sys.argv` or `argparse` routing. [ASSUMED] | That would duplicate plumbing the repo already has and bypass Typer's first-party CLI testing pattern. [VERIFIED: current CLI][CITED: https://typer.tiangolo.com/tutorial/testing/] |
| Reusing `gate_models` and `FileEvidenceIndex` as the replay-diagnostics contract. [VERIFIED: repo code] | A second agent-only JSON schema. [ASSUMED] | A second schema would fork the accepted Phase 2 evidence shape and create drift risk. [VERIFIED: Phase 2 context][VERIFIED: repo code] |
| Legacy-style normalized HMAC temp IDs with `IN` prefix. [VERIFIED: `03-CONTEXT.md`][VERIFIED: legacy repo code] | Raw-name `TEMP-*` IDs or a non-keyed ad hoc hash. [VERIFIED: current repo code][ASSUMED] | The current raw-name fallback leaks identifiers and does not match the verified legacy reference behavior. [VERIFIED: current repo code][VERIFIED: legacy repo code] |

**Installation:** No new dependency is required for the recommended plan; refresh the governed environment with `uv sync --dev`. [VERIFIED: `pyproject.toml`][VERIFIED: `docs/disciplines/implementation-toolchain.md`]

**Version verification:** `typer 0.24.1`, `openpyxl 3.1.5`, and `pytest 8.4.2` were verified from both `uv.lock` and the active `uv` environment; this research does not claim they are the newest upstream releases. [VERIFIED: `uv.lock`][VERIFIED: local environment probe]

## Architecture Patterns

### Recommended Project Structure

```text
src/work_data_hub_pro/
├── apps/
│   ├── etl_cli/main.py                  # keep wrappers and add replay subcommands
│   └── orchestration/replay/
│       ├── contracts.py                 # typed run-report + domain registry contracts
│       ├── errors.py                    # typed preflight/config/setup exceptions
│       ├── diagnostics.py               # comparison-run read-side helpers
│       ├── runtime.py                   # shared replay primitives only
│       ├── annuity_performance_slice.py # explicit runner remains
│       ├── annual_award_slice.py        # explicit runner remains
│       └── annual_loss_slice.py         # explicit runner remains
├── capabilities/identity_resolution/service.py  # temp-id helper integration point
└── governance/evidence_index/file_store.py      # extend with package readers
```

This keeps replay public contracts in `apps`, keeps evidence package formats in `governance`, and avoids turning `platform` into a generic dumping ground for slice-specific abstractions. [ASSUMED][VERIFIED: repo structure]

### Pattern 1: Shared Primitives, Explicit Runners

**What:** Extract only invariant replay mechanics: run/comparison ID creation, checkpoint assembly, gate summarization, evidence writing, common publication-plan helper wiring, and the intake -> processing -> identity loop skeleton. [VERIFIED: `03-CONTEXT.md`][VERIFIED: replay slice code]

**When to use:** After public replay contracts are frozen and before CLI unification. [VERIFIED: `03-CONTEXT.md`]

**Why this boundary works:** Current slices are near-duplicates in structure, but still differ materially in processor choice, enrichment, fixture loads, release paths, and publication targets. [VERIFIED: replay slice code]

### Pattern 2: Typed Setup Exceptions + Typed Run Report

**What:** Keep preflight/config/setup failures as typed exceptions, and keep run-completed parity outcomes as a serializable `ReplayRunReport` that reuses `CheckpointResult`, `GateSummary`, and `CompatibilityCase` instead of exposing raw trace stores and lineage registries. [VERIFIED: `03-CONTEXT.md`][VERIFIED: repo code]

**When to use:** At the boundary for `run_*_slice(...)`, `replay run`, and `replay diagnose`. [VERIFIED: `03-CONTEXT.md`]

**Current gap:** Current code leaks `FileNotFoundError`, `TypeError`, `ValueError`, and `KeyError` from baseline loading, validators, and publication policy lookup; current `SliceRunOutcome` also contains debug-only stores and intermediate payloads. [VERIFIED: `src/work_data_hub_pro/governance/compatibility/gate_runtime.py`][VERIFIED: `src/work_data_hub_pro/platform/contracts/validators.py`][VERIFIED: `src/work_data_hub_pro/platform/publication/service.py`][VERIFIED: replay slice code]

### Pattern 3: One Replay Domain Registry, Two CLI Layers

**What:** Add one registry that maps domain key -> explicit runner, replay root, wrapper command, and diagnose root; keep wrapper commands, and make both wrappers and `replay run` call the same registry-backed path. [ASSUMED][VERIFIED: current CLI]

**When to use:** Before implementing `replay list-domains` and `replay diagnose`. [VERIFIED: `03-CONTEXT.md`]

**Current gap:** There is no domain registry today; `apps/etl_cli/main.py` imports three slice functions directly and exposes only flat wrapper commands. [VERIFIED: `src/work_data_hub_pro/apps/etl_cli/main.py`]

### Pattern 4: Dedicated Temp-Identity Helper Boundary

**What:** Move fallback generation behind `generate_temp_identity(...)`, `is_temp_identity(...)`, `normalize_identity_fallback_input(...)`, and `temp_identity_prefix()`, and make `CacheFirstIdentityResolutionService.resolve(...)` call those helpers instead of embedding string formatting. [VERIFIED: `03-CONTEXT.md`][VERIFIED: `src/work_data_hub_pro/capabilities/identity_resolution/service.py`]

**When to use:** Before replay baseline refresh and before shared-runtime extraction, because fallback IDs flow into fact payloads, reference derivation payloads, and replay baselines. [VERIFIED: replay slice code][VERIFIED: tests and reference assets]

### Plan Decomposition

1. Lock the public replay contracts first: `ReplayRunReport`, typed setup exceptions, `primary_failure` semantics, and the replay domain registry. [VERIFIED: `03-CONTEXT.md`][VERIFIED: repo code]
2. Lock the temp-id contract second: normalization source, HMAC format, prefix handling, placeholder-to-`None`, and evidence-side raw-name placement. [VERIFIED: `03-CONTEXT.md`][VERIFIED: legacy repo code]
3. Add read-side evidence APIs third: manifest/gate-summary/checkpoint-results/report readers in the evidence layer so `replay diagnose` has a real backend. [VERIFIED: current evidence layout][ASSUMED]
4. Extract shared replay primitives fourth, but leave domain-specific runners explicit. [VERIFIED: `03-CONTEXT.md`]
5. Add unified replay CLI subcommands fifth, keeping current wrapper names as stable shims. [VERIFIED: `03-CONTEXT.md`]
6. Refresh tests, runbooks, and replay fixtures last, with all three accepted slice replay suites in the gate. [VERIFIED: roadmap success criteria][VERIFIED: replay tests]

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Nested replay CLI routing | Manual `sys.argv` parsing or a second parser library. [ASSUMED] | Typer subcommands via `Typer()` + `add_typer()`. [CITED: https://typer.tiangolo.com/tutorial/subcommands/nested-subcommands/] | The repo already uses Typer, and Typer documents CLI testing with `CliRunner`. [VERIFIED: current CLI][CITED: https://typer.tiangolo.com/tutorial/testing/] |
| Temp-id hashing | Raw-name prefixes, string concatenation, or a custom non-keyed hash helper. [VERIFIED: current repo code][ASSUMED] | Python stdlib `hmac` + `hashlib` + `base64`, following the verified legacy format. [VERIFIED: legacy repo code][CITED: https://docs.python.org/3/library/hmac.html] | This preserves deterministic parity and avoids leaking raw names into `company_id`. [VERIFIED: `03-CONTEXT.md`][VERIFIED: legacy repo code] |
| Replay evidence schema | A new JSON package format just for agents. [ASSUMED] | Existing `ComparisonRunManifest`, `GateSummary`, `CheckpointResult`, and `FileEvidenceIndex` package layout. [VERIFIED: repo code] | Phase 2 already standardized the package; Phase 3 should add readers and summaries, not a competing format. [VERIFIED: Phase 2 context][VERIFIED: repo code] |
| Setup validation logic | New ad hoc validation branches in every slice runner. [ASSUMED] | Existing `platform.contracts.validators` plus typed exception translation. [VERIFIED: `src/work_data_hub_pro/platform/contracts/validators.py`] | Reusing validators keeps structural enforcement centralized while improving failure categorization. [VERIFIED: repo code] |

## Runtime State Inventory

| Category | Items Found | Action Required |
|----------|-------------|-----------------|
| Stored data | Committed replay baselines under `reference/historical_replays/*/legacy_identity_resolution_2026_03.json` do not contain `TEMP-*`; committed tests and planning/docs still do. [VERIFIED: replay baseline files][VERIFIED: `tests/integration/test_identity_resolution.py`][VERIFIED: `tests/replay/test_annual_loss_slice.py`] | Code edit plus fixture/test refresh; no committed repo data migration was identified. [VERIFIED: repo scan] |
| Live service config | None detected in the current Pro runtime: integrations are file-backed only, and broader operator surfaces remain deferred. [VERIFIED: `.planning/codebase/INTEGRATIONS.md`][VERIFIED: refactor program spec] | None for Phase 3. [VERIFIED: repo scan] |
| OS-registered state | None detected in the repo scan; no systemd, launchd, pm2, or Task Scheduler registration files were found. [VERIFIED: repo grep for service/task-manager terms] | None. [VERIFIED: repo scan] |
| Secrets / env vars | Current Pro runtime reads no env vars, while legacy temp-id generation reads `WDH_ALIAS_SALT`; Phase 3 adds a new governed salt source instead of migrating an existing Pro secret name. [VERIFIED: repo grep for env vars][VERIFIED: `E:\Projects\WorkDataHub\src\work_data_hub\domain\company_enrichment\lookup_queue.py`] | Code/config addition only; lock the salt source before implementation. [VERIFIED: current repo][VERIFIED: legacy repo] |
| Build artifacts | Phase 3 does not rename the package, module root, or CLI module path. [VERIFIED: `src/work_data_hub_pro/apps/etl_cli/main.py`][VERIFIED: repo scan] | No migration; rerun tests and replay commands after changes to refresh local evidence. [VERIFIED: repo workflow] |

## Common Pitfalls

### Pitfall 1: Freezing the Wrong Abstraction First

**What goes wrong:** A shared runtime is extracted before the run-report and temp-id contracts are fixed, so the new helper layer bakes in today's mixed `SliceRunOutcome` and raw-name fallback behavior. [VERIFIED: replay slice code][VERIFIED: current identity service]

**Why it happens:** The code duplication is obvious, so it is tempting to extract the loop immediately. [VERIFIED: `.planning/codebase/CONCERNS.md`]

**How to avoid:** Lock the exception classes, run-report schema, temp-id helper boundary, and CLI v1 outputs first. [VERIFIED: `03-CONTEXT.md`]

### Pitfall 2: Treating `replay diagnose` as Just Another Print Command

**What goes wrong:** The CLI adds a `diagnose` command, but there is no stable way to load manifests, gate summaries, and checkpoint results by `comparison_run_id`. [VERIFIED: `03-CONTEXT.md`][VERIFIED: `src/work_data_hub_pro/governance/evidence_index/file_store.py`]

**Why it happens:** The current runtime already writes the files, so the missing read-side API is easy to overlook. [VERIFIED: `src/work_data_hub_pro/governance/compatibility/gate_runtime.py`]

**How to avoid:** Extend `FileEvidenceIndex` with package readers or add a dedicated replay-diagnostics reader rooted to known replay directories. [ASSUMED][VERIFIED: current evidence layout]

### Pitfall 3: Relative-Path Hidden Context in the CLI

**What goes wrong:** A command only works when launched from a workspace whose current directory already contains the expected `reference/historical_replays/...` and `config/...` trees. [VERIFIED: current CLI defaults][VERIFIED: `tests/replay/test_annual_loss_explainability_slo.py`]

**Why it happens:** The current wrapper commands use relative `Path(...)` defaults for replay roots. [VERIFIED: `src/work_data_hub_pro/apps/etl_cli/main.py`]

**How to avoid:** Resolve replay roots through a registry or shared resolver anchored to the repo structure, not the caller's CWD. [ASSUMED][VERIFIED: repo structure]

### Pitfall 4: Temp-ID Normalization Drift

**What goes wrong:** New temp IDs are deterministic but do not match legacy normalization rules, so replay outputs drift and unresolved-name behavior becomes inconsistent. [VERIFIED: `03-CONTEXT.md`][VERIFIED: legacy repo code]

**Why it happens:** Legacy normalization is more complex than a trivial `strip()` or `upper()` operation. [VERIFIED: `E:\Projects\WorkDataHub\src\work_data_hub\infrastructure\cleansing\normalizers\customer_name.py`]

**How to avoid:** Port or faithfully emulate the legacy normalization semantics behind `normalize_identity_fallback_input(...)`, and pin them with replay/integration tests before refreshing baselines. [VERIFIED: `03-CONTEXT.md`][VERIFIED: legacy repo code]

## Code Examples

Verified patterns from official and primary sources:

### Typer Nested Replay Command Group

```python
import typer

app = typer.Typer()
replay_app = typer.Typer()
app.add_typer(replay_app, name="replay")
```

Source: Typer nested subcommands tutorial. [CITED: https://typer.tiangolo.com/tutorial/subcommands/nested-subcommands/]

### Typer CLI Contract Test

```python
from typer.testing import CliRunner
from .main import app

runner = CliRunner()

def test_app():
    result = runner.invoke(app, ["replay", "list-domains"])
    assert result.exit_code == 0
```

Source: Typer testing tutorial. [CITED: https://typer.tiangolo.com/tutorial/testing/]

### Current Comparison-Run Package Write Pattern

```python
comparison_manifest = ComparisonRunManifest(
    comparison_run_id=comparison_run_id,
    domain=batch.domain,
    period=batch.period,
    baseline_version=f"legacy-monthly-snapshot:{period}",
    config_release_id=manifest.release_id,
    rule_pack_version=manifest.rule_pack_version,
    decision_owner="compatibility-review",
    package_root=f"comparison_runs/{comparison_run_id}",
    package_paths=default_package_paths(comparison_run_id),
)
write_comparison_run_package(...)
```

Source: Current replay slices plus shared gate runtime. [VERIFIED: `src/work_data_hub_pro/apps/orchestration/replay/annuity_performance_slice.py`][VERIFIED: `src/work_data_hub_pro/governance/compatibility/gate_runtime.py`]

### Legacy Deterministic Temp-ID Pattern

```python
normalized = normalize_for_temp_id(customer_name)
digest = hmac.new(
    salt.encode("utf-8"),
    normalized.encode("utf-8"),
    hashlib.sha1,
).digest()
encoded = base64.b32encode(digest[:10]).decode("ascii")
return f"IN{encoded}"
```

Source: Legacy current normalization/temp-id generator. [VERIFIED: `E:\Projects\WorkDataHub\src\work_data_hub\infrastructure\enrichment\normalizer.py`]

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Flat wrapper-only CLI commands. [VERIFIED: current CLI] | Typer-documented nested command groups via `add_typer()` for `replay run`, `replay diagnose`, and `replay list-domains`. [CITED: https://typer.tiangolo.com/tutorial/subcommands/nested-subcommands/] | Supported in current Typer docs. [CITED: https://typer.tiangolo.com/tutorial/subcommands/nested-subcommands/] | Lets Phase 3 add agent-facing commands without removing human-facing wrappers. [VERIFIED: `03-CONTEXT.md`] |
| Raw-name `TEMP-{company_name}` fallback in Pro. [VERIFIED: current repo code] | Legacy normalized HMAC-SHA1 Base32 `IN...` temp IDs plus `None` for empty placeholders. [VERIFIED: legacy repo code] | Legacy current implementation documented in code and comments from 2026-01-05 and Story 7.5-3. [VERIFIED: legacy repo code] | Reduces raw-identifier leakage and preserves deterministic replay behavior. [VERIFIED: `03-CONTEXT.md`] |
| Write-only evidence package APIs. [VERIFIED: current repo code] | Read/write package boundary with manifest, gate summary, checkpoint results, report, and case readers. [ASSUMED] | Phase 3 target. [VERIFIED: `03-CONTEXT.md`] | Required to make `replay diagnose --comparison-run-id` real instead of implicit. [VERIFIED: current evidence layout] |

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | New replay public contracts and setup exceptions should live under `src/work_data_hub_pro/apps/orchestration/replay/` instead of `platform/execution/`. [ASSUMED] | Architecture Patterns | Boundary churn or review friction if the project prefers a different owner. |
| A2 | One shared replay domain registry should resolve both wrapper commands and `replay run/diagnose/list-domains`. [ASSUMED] | Architecture Patterns | CLI work may fragment into duplicate routing logic if the project wants separate registries. |
| A3 | Phase 3 can implement `replay diagnose` by scanning known replay roots from a registry rather than changing `comparison_run_id` format or introducing a global index. [ASSUMED] | Open Questions / Architecture Patterns | Diagnose lookup could become slower or more brittle if domain count grows faster than expected. |

## Open Questions (RESOLVED)

1. **Where does the governed temp-id salt live in `WorkDataHubPro`?** [VERIFIED: `03-CONTEXT.md`][VERIFIED: repo grep][VERIFIED: legacy repo code]
   **Resolution:** Phase 3 uses one governed env-var contract, `WDHP_TEMP_ID_SALT`, referenced by `config/releases/temp_identity_policy.json` rather than a committed salt value. This keeps the secret out of source while still giving the temp-id policy one explicit configuration boundary. [VERIFIED: `03-02-PLAN.md`]

2. **How should `replay diagnose` resolve `comparison_run_id` without hidden domain context?** [VERIFIED: `03-CONTEXT.md`][VERIFIED: current evidence layout]
   **Resolution:** `replay diagnose` resolves runs by scanning only the registry-declared replay roots and then using explicit comparison-run package readers. Phase 3 does not introduce a global run index. [VERIFIED: `03-01-PLAN.md`]

3. **Should existing wrapper commands keep CWD-relative replay-root behavior?** [VERIFIED: current CLI][VERIFIED: `tests/replay/test_annual_loss_explainability_slo.py`]
   **Resolution:** Keep the wrapper command names, but move default replay-root resolution to repo-root-anchored registry metadata so agents and humans get deterministic behavior without depending on shell CWD. [VERIFIED: `03-01-PLAN.md`][VERIFIED: `03-05-PLAN.md`]

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|-------------|-----------|---------|----------|
| `uv` | All repo-standard commands and the supported runtime entry path. [VERIFIED: toolchain discipline] | ✓ [VERIFIED: local environment probe] | `0.8.14` [VERIFIED: local environment probe] | None. [VERIFIED: repo workflow] |
| `uv`-managed Python runtime | Replay CLI, tests, and stdlib temp-id helpers. [VERIFIED: `pyproject.toml`] | ✓ [VERIFIED: local environment probe] | `3.12.11` [VERIFIED: `uv run python --version`] | None. [VERIFIED: repo workflow] |
| Plain `python` on PATH | Ad hoc shell commands that ignore repo workflow. [VERIFIED: local environment probe] | ✗ [VERIFIED: local environment probe] | — [VERIFIED: local environment probe] | Use `uv run python ...`. [VERIFIED: toolchain discipline] |
| `pytest` via `uv run` | Contract, integration, replay, and full-suite verification. [VERIFIED: `pyproject.toml`][VERIFIED: tests tree] | ✓ [VERIFIED: local environment probe] | `8.4.2` [VERIFIED: local environment probe] | None. [VERIFIED: repo workflow] |

## Validation Architecture

### Test Framework

| Property | Value |
|----------|-------|
| Framework | `pytest 8.4.2` via `uv run pytest`. [VERIFIED: `pyproject.toml`][VERIFIED: local environment probe] |
| Config file | `pyproject.toml` with `addopts = "--basetemp=.pytest_tmp"`. [VERIFIED: `pyproject.toml`] |
| Quick run command | `uv run pytest tests/contracts/test_phase2_gate_contracts.py tests/integration/test_identity_resolution.py tests/integration/test_publication_service.py -v`. [VERIFIED: test files exist] |
| Full suite command | `uv run pytest -v`. [VERIFIED: `AGENTS.md`][VERIFIED: verification discipline] |

### Phase Requirements → Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| PIPE-03 | Typed setup failures and typed run-report outputs. [VERIFIED: `.planning/REQUIREMENTS.md`][VERIFIED: `03-CONTEXT.md`] | contract + integration | `uv run pytest tests/contracts/test_replay_run_report.py tests/integration/test_replay_setup_failures.py -v` [ASSUMED] | ❌ Wave 0 [VERIFIED: repo scan] |
| PIPE-04 | Shared replay primitives adopted without parity drift across all accepted slices. [VERIFIED: `.planning/REQUIREMENTS.md`][VERIFIED: roadmap] | replay | `uv run pytest tests/replay/test_annuity_performance_slice.py tests/replay/test_annual_award_slice.py tests/replay/test_annual_loss_slice.py -v` [VERIFIED: test files exist] | ✅ [VERIFIED: repo scan] |
| OPS-01 | Stable `replay run`, `replay diagnose`, and `replay list-domains` entrypoints with machine-readable outputs. [VERIFIED: `.planning/REQUIREMENTS.md`][VERIFIED: `03-CONTEXT.md`] | CLI contract | `uv run pytest tests/contracts/test_replay_cli_contracts.py tests/contracts/test_replay_diagnose_contracts.py -v` [ASSUMED] | ❌ Wave 0 [VERIFIED: repo scan] |
| GOV-02 | Opaque deterministic temp IDs and placeholder-to-`None` semantics. [VERIFIED: `.planning/REQUIREMENTS.md`][VERIFIED: `03-CONTEXT.md`] | integration + replay | `uv run pytest tests/integration/test_temp_identity_policy.py tests/integration/test_identity_resolution.py -v` [ASSUMED] | ❌ Wave 0 [VERIFIED: repo scan] |

### Wave 0 Gaps

- `tests/contracts/test_replay_cli_contracts.py` — lock `replay run`, `replay diagnose`, and `replay list-domains` output and exit-code contracts. [ASSUMED][VERIFIED: current repo lacks CLI tests]
- `tests/contracts/test_replay_run_report.py` — freeze the serializable run-report schema and `primary_failure` derivation. [ASSUMED][VERIFIED: current repo lacks this contract]
- `tests/integration/test_replay_setup_failures.py` — translate current `FileNotFoundError`, `TypeError`, `ValueError`, and `KeyError` sources into typed setup exceptions. [ASSUMED][VERIFIED: current failure sources]
- `tests/integration/test_temp_identity_policy.py` — cover deterministic `IN...` IDs, placeholder-to-`None`, and raw-name-free `company_id`. [ASSUMED][VERIFIED: current repo lacks this coverage]
- `tests/replay/test_annual_loss_slice.py` — strengthen or replace the weaker annual-loss replay assertions before trusting refactor parity gates. [VERIFIED: current test file]

## Security Domain

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|-----------------|
| V2 Authentication | No; the current replay runtime has no auth boundary. [VERIFIED: `.planning/codebase/INTEGRATIONS.md`] | None in Phase 3 scope. [VERIFIED: repo scan] |
| V3 Session Management | No; the current replay runtime is synchronous CLI execution without sessions. [VERIFIED: current repo code] | None in Phase 3 scope. [VERIFIED: repo scan] |
| V4 Access Control | Partially; `replay diagnose` will be a local file reader and must stay rooted to known evidence directories. [ASSUMED][VERIFIED: current evidence layout] | Validate `comparison_run_id`, resolve through registry-backed roots, and never concatenate untrusted paths directly. [ASSUMED] |
| V5 Input Validation | Yes. [VERIFIED: current validators][VERIFIED: replay CLI inputs] | Reuse `platform.contracts.validators`, validate domain keys at the registry boundary, and treat config/baseline/path drift as typed setup failures. [VERIFIED: repo code][ASSUMED] |
| V6 Cryptography | Yes; temp-ID generation is explicitly HMAC-based in the locked contract. [VERIFIED: `03-CONTEXT.md`][VERIFIED: legacy repo code] | Use stdlib `hmac`/`hashlib`/`base64`; never hand-roll crypto or embed raw names in identifiers. [VERIFIED: legacy repo code][CITED: https://docs.python.org/3/library/hmac.html] |

## Sources

### Primary (HIGH confidence)

- `.planning/phases/03-orchestration-refactor-failure-explainability/03-CONTEXT.md` — locked Phase 3 decisions and boundaries. [VERIFIED: repo file]
- `.planning/REQUIREMENTS.md`, `.planning/ROADMAP.md`, `.planning/PROJECT.md` — requirement targets, success criteria, and project constraints. [VERIFIED: repo files]
- `src/work_data_hub_pro/apps/orchestration/replay/*.py` and `src/work_data_hub_pro/apps/etl_cli/main.py` — current orchestration duplication and CLI surface. [VERIFIED: repo code]
- `src/work_data_hub_pro/governance/compatibility/gate_models.py`, `gate_runtime.py`, and `governance/evidence_index/file_store.py` — current evidence package schema and read/write gap. [VERIFIED: repo code]
- `src/work_data_hub_pro/capabilities/identity_resolution/service.py` — current raw-name temp-id behavior. [VERIFIED: repo code]
- `E:\Projects\WorkDataHub\src\work_data_hub\infrastructure\enrichment\normalizer.py`, `resolver/backflow.py`, and `domain/company_enrichment/lookup_queue.py` — legacy current temp-id format, placeholder handling, and salt source. [VERIFIED: local legacy repo code]

### Secondary (MEDIUM confidence)

- `https://typer.tiangolo.com/tutorial/subcommands/nested-subcommands/` — official Typer nested subcommand pattern. [CITED: https://typer.tiangolo.com/tutorial/subcommands/nested-subcommands/]
- `https://typer.tiangolo.com/tutorial/testing/` — official Typer CLI testing pattern. [CITED: https://typer.tiangolo.com/tutorial/testing/]
- `https://docs.python.org/3/library/hmac.html` — official Python `hmac` reference. [CITED: https://docs.python.org/3/library/hmac.html]

## Metadata

**Confidence breakdown:**

- Standard stack: HIGH — the project stack, locked versions, and official Typer/Python docs were verified directly. [VERIFIED: `uv.lock`][VERIFIED: local environment probe][CITED: official docs above]
- Architecture: MEDIUM — the shared-vs-explicit boundary is locked and the code duplication is verified, but exact new module placement and diagnose lookup strategy are still planning recommendations. [VERIFIED: `03-CONTEXT.md`][VERIFIED: repo code][ASSUMED]
- Pitfalls: HIGH — the major failure surfaces are visible in current code, tests, and legacy temp-id behavior. [VERIFIED: repo code][VERIFIED: legacy repo code]

**Research date:** 2026-04-13 [VERIFIED: research session date]
**Valid until:** 2026-04-20, because this phase is an active planning surface and the codebase is changing quickly. [VERIFIED: `.planning/STATE.md`][ASSUMED]

# Phase 4: Agent Operations & Governance Hardening - Research

**Researched:** 2026-04-13
**Domain:** Agent-operable maintenance workflow, output-to-source lineage lookup, evidence redaction, and file-backed compatibility lifecycle hardening.
**Confidence:** MEDIUM

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

### Operator workflow contract
- **D-01:** Phase 4 should center on one explicit repo-native workflow: add a source or adjust a rule through committed config/runbook surfaces, run verification, and inspect evidence using documented commands.
- **D-02:** Prefer extending the existing CLI and runbook surfaces over inventing a separate operator UI or hidden local-only scripts.
- **D-03:** Configuration changes that affect semantics must stay release-governed under `config/` and be paired with verification instructions in committed docs.

### Lineage and evidence lookup
- **D-04:** Lineage lookup should use query helpers over the existing `trace`, `lineage`, and comparison-run evidence structures rather than relying on humans or agents to browse JSON folders manually.
- **D-05:** The primary lookup anchors remain `comparison_run_id`, `batch_id`, `anchor_row_no`, and output identifiers; Phase 4 should make those lookups explicit and test-covered.
- **D-06:** Preserve file-backed evidence as the operational baseline for now; persistent storage/query adapters are deferred.

### Evidence redaction
- **D-07:** Redaction belongs at the evidence persistence boundary, not inside domain business logic.
- **D-08:** Default behavior should preserve auditability while redacting or masking raw business-identifying values such as names and other sensitive payload fields in persisted evidence artifacts.
- **D-09:** Redaction policy should be explicit and governed, not ad hoc per writer call.

### Adjudication lifecycle
- **D-10:** `CompatibilityCase` should become a fuller operational record with explicit severity, decision owner, closure evidence, and lifecycle status transitions.
- **D-11:** Phase 4 should formalize how a pending case becomes approved, rejected, or closed, and that lifecycle should be visible in committed artifacts/tests.
- **D-12:** Keep the control-plane model file-backed and repository-auditable for now instead of adding a new adjudication service backend.

### the agent's Discretion
- Exact CLI command names and file/module placement for lineage and governance helpers, provided they stay discoverable from committed runbooks and existing app boundaries.
- Exact redaction field list and masking representation, provided sensitive identifiers do not persist in plaintext evidence and audit anchors remain intact.
- Exact closure-proof schema for compatibility cases, provided severity, owner, status, and proof-of-closure are all explicit.

### Deferred Ideas (OUT OF SCOPE)
- Persistent trace/evidence storage adapters and large-run operability remain later work.
- Operator dashboards and richer self-service interfaces remain out of scope for this phase.
- Full multi-surface rule-update UX beyond one documented add-source / adjust-rule / run-verify path is deferred.
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| OPS-02 | Agent can use standardized runbook + config contracts to add a new data source with bounded change surface. | The plan should end with one canonical maintenance workflow runbook plus contract tests that freeze the exact repo surfaces an agent must touch: replay registry metadata, domain config under `config/domains/`, release bindings under `config/releases/`, replay assets under `reference/historical_replays/`, and verification commands under `uv run pytest` plus CLI entrypoints. |
| OPS-03 | Agent can trace a produced output row back to its source and stage decisions through queryable lineage/evidence references. | The current replay runtime already writes per-row trace files and a comparison-run package, but there is no persisted lookup surface that resolves `comparison_run_id` plus `record_id` or `anchor_row_no` into source-stage evidence. Phase 4 should add package readers, a typed lookup payload, and a CLI command so agents stop browsing raw JSON by hand. |
| OPS-04 | Project can provide explicit observability contracts that support operations and incident response. | Observability should be expressed as a governed package contract: manifest, gate summary, checkpoint results, source-intake adaptation, lineage impact, trace evidence, and typed compatibility case files with stable CLI/read APIs and runbooks. |
| GOV-01 | Evidence artifacts can apply redaction policy for sensitive fields before persistence. | The evidence writer currently persists raw trace values, payload fragments, and compatibility payloads without redaction. Phase 4 should add one governed policy file and one persistence-boundary redaction helper that masks configured business-identifying fields while preserving anchors such as `comparison_run_id`, `batch_id`, `record_id`, `anchor_row_no`, `stage_id`, and `rule_id`. |
| GOV-03 | Compatibility adjudication can record mismatch severity, decision owner, and closure evidence for auditability. | `CompatibilityCase` already has `severity`, `decision_status`, and `approved_by`, but it lacks a full lifecycle contract, decision owner, history, and closure-proof fields. Phase 4 should harden both the model and the file-backed operational surface. |
</phase_requirements>

## Summary

Phase 4 should not be planned as a broad runtime expansion. The repo already has the essential replay and diagnostics skeleton from Phase 3, and the active context explicitly defers persistent storage, queue/runtime closure, dashboards, and operator-UI work. The right target is a file-backed operational hardening slice: make replay evidence queryable, make persisted evidence safe by default, make compatibility cases auditable, and then document one stable maintenance workflow around those surfaces.

The codebase reality supports that decomposition. `src/work_data_hub_pro/apps/etl_cli/main.py` already exposes `replay run`, `replay diagnose`, and `replay list-domains`, `src/work_data_hub_pro/apps/orchestration/replay/runtime.py` already writes comparison-run packages, and `src/work_data_hub_pro/governance/evidence_index/file_store.py` is the obvious persistence choke point. The missing pieces are not new architectures; they are missing query/read contracts, missing redaction at write time, and missing lifecycle structure in compatibility records.

The strongest risk area is that Phase 4 could drift into doc-only work or, in the opposite direction, into a new backend. The roadmap and context reject both extremes. A good plan must keep the evidence model file-backed, add explicit CLI/read helpers instead of generic data services, and tie every operational promise to executable tests and runbooks.

**Primary recommendation:** decompose Phase 4 into four plans across three waves:
1. lineaged evidence lookup and CLI contracts;
2. evidence redaction policy at the file-writer boundary;
3. compatibility lifecycle hardening with explicit owner and closure-proof fields;
4. one canonical agent maintenance workflow runbook plus contract tests that bind docs to the real code/config/CLI surfaces.

## Project Constraints

- Preserve capability-first boundaries. Query/read helpers belong under `apps/` or `governance/`, not inside business capability modules.
- Keep evidence file-backed and repo-auditable for this phase; do not add a database, queue, or long-running service.
- Keep redaction at persistence boundaries, not in `source_intake`, `fact_processing`, or `identity_resolution`.
- Keep runbooks and verification commands committed and repo-native; local scratch notes do not satisfy OPS-02 or OPS-04.
- Require boundary-matching tests: contract/integration coverage for new CLI and evidence contracts, then `uv run pytest -v` before completion claims.

## Standard Stack

### Core

| Component | Version / State | Purpose | Why Standard |
|-----------|-----------------|---------|--------------|
| Typer CLI | current repo standard | Extend `replay` and add compatibility/lookup commands without inventing a second command layer. | Existing Phase 3 surfaces already depend on Typer and are contract-tested. |
| `FileEvidenceIndex` | current repo module | Central file-backed evidence read/write boundary. | Redaction and query helpers belong here or immediately adjacent to it. |
| replay runtime + diagnostics modules | current repo modules | Canonical comparison-run package assembly and read-side lookup. | Phase 4 should extend these contracts instead of introducing a new backend or hidden path logic. |
| `pytest` via `uv run pytest` | current repo standard | Contract, integration, replay, and full-suite verification. | Matches the repository toolchain discipline and existing test layout. |

### Supporting

| Component | Purpose | When to Use |
|-----------|---------|-------------|
| `platform/tracing/in_memory_trace_store.py` | Current trace query seam. | Extend only enough to support stable lookup helpers and testable contract behavior. |
| `platform/lineage/registry.py` | Current lineage query seam. | Reuse for persisted lookup packaging and record-to-source linkage. |
| `governance/adjudication/service.py` | Existing compatibility-case creation path. | Extend to support explicit owner, lifecycle transition, and closure-proof recording. |
| `docs/runbooks/*.md` | Human/agent operational baseline. | Use as the stable handoff layer after code contracts exist. |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| File-backed evidence lookup and redaction hardening | A new persistent store or indexed service | Violates the locked Phase 4 scope and creates runtime/ops work deferred to later phases. |
| CLI/read helpers rooted in replay registry metadata | Manual path browsing under `reference/historical_replays/**/evidence` | Keeps OPS-03 implicit and brittle; still depends on human memory of file layout. |
| One governed redaction policy file | Inline field masking decisions per writer call | Produces drift across trace, checkpoint, lineage, and compatibility artifacts. |
| Explicit compatibility-case lifecycle commands or service methods | Editing case JSON by hand | Not operationally credible and too easy to bypass owner/proof requirements. |

## Architecture Patterns

### Pattern 1: Comparison-Run Lookup Contract

**What:** extend the comparison-run package so a run can be queried by `comparison_run_id` plus either `record_id` or `anchor_row_no`, returning stable paths and typed linkage to source/stage evidence.

**Why:** the current repo can diagnose a run at the run level, but not at the output-row level. Phase 4 success depends on lookup being explicit and test-covered rather than manual.

**Likely shape:**
- add package readers for `source-intake-adaptation.json` and `lineage-impact.json`
- persist lineage entries with exact keys `record_id`, `batch_id`, `anchor_row_no`, `origin_row_nos`, `parent_record_ids`, and `trace_path`
- expose a CLI such as `replay lookup --comparison-run-id <id> --record-id <id>` with machine-readable JSON output

### Pattern 2: Persistence-Boundary Redaction

**What:** introduce one governed evidence-redaction policy file and one helper that is applied by the evidence writer before JSON is written.

**Why:** current evidence writes raw names and payload values directly to disk. The phase context explicitly says this redaction belongs at the persistence boundary, not in domain logic.

**Recommended contract:**
- config file under `config/policies/evidence_redaction.json`
- exact keys: `policy_id`, `mask_token`, `sensitive_trace_fields`, `sensitive_payload_keys`, `preserve_exact_fields`
- default mask token such as `***REDACTED***`
- preserve anchors and rule metadata intact

### Pattern 3: File-Backed Compatibility Lifecycle

**What:** evolve `CompatibilityCase` from a mismatch snapshot to an auditable lifecycle record.

**Why:** the current model cannot prove who owns a case, how it moved through review, or what evidence closed it. That is the direct gap behind GOV-03.

**Recommended fields and transitions:**
- required fields: `severity`, `decision_owner`, `decision_status`, `resolution_note`, `closure_evidence`, `closed_at`, `closed_by`
- allowed statuses: `pending_review`, `approved_exception`, `rejected_difference`, `closed`
- add service/CLI support for assignment, transition, and show-case operations

### Pattern 4: One Canonical Agent Workflow Runbook

**What:** add one canonical workflow runbook that binds code, config, evidence, and verification commands into a stable add-source / adjust-rule / run-verify path.

**Why:** OPS-02 is not satisfied by scattered domain runbooks. The workflow must point to exact repo surfaces and command forms.

**Recommended content:**
- add source: replay registry + domain config + release binding + replay asset locations
- adjust rule: exact config files and verification commands
- run verify: `replay run`, `replay diagnose`, `replay lookup`, targeted `uv run pytest ...`, and `uv run pytest -v`
- adjudicate/close case: compatibility CLI commands and closure-proof expectations

## Recommended Plan Decomposition

### Plan 04-01: Output-to-Source Lookup Contract and CLI

Purpose:
- satisfy OPS-03 and part of OPS-04 by making comparison-run lineage/evidence queryable

Key outputs:
- package readers for source-intake adaptation and lineage impact
- persisted lineage lookup shape with stable keys
- `replay lookup` CLI and contract/integration tests
- updated evidence path/report contract where needed

### Plan 04-02: Evidence Redaction Policy and Writer Hardening

Purpose:
- satisfy GOV-01 and part of OPS-04 by ensuring persisted evidence applies one governed masking policy

Key outputs:
- `config/policies/evidence_redaction.json`
- persistence-boundary redaction helper
- evidence writer updates for trace, checkpoint, lineage, and compatibility payloads
- contract/integration tests proving sensitive values are masked while anchors remain intact

### Plan 04-03: Compatibility Lifecycle and Closure-Proof Hardening

Purpose:
- satisfy GOV-03 and part of OPS-04 by making file-backed cases auditable records instead of shallow snapshots

Key outputs:
- expanded `CompatibilityCase` fields and lifecycle rules
- adjudication service methods for owner assignment and lifecycle transitions
- compatibility CLI commands for show/transition/close behavior
- tests covering required owner, status, and closure-proof semantics

### Plan 04-04: Agent Maintenance Workflow and Incident Runbooks

Purpose:
- satisfy OPS-02 and tie together the operational surfaces from Plans 01-03 into one bounded workflow

Key outputs:
- `docs/runbooks/agent-maintenance-workflow.md`
- updates to domain replay runbooks with the new lookup and compatibility command surfaces
- contract tests that freeze exact file paths and command strings referenced in the workflow

## Key Risks And How Plans Should Address Them

### Risk 1: Queryability Stops at Run Level
- **Failure mode:** `replay diagnose` works, but agents still cannot get from an output record to the original row and trace path.
- **Plan response:** persist stable lineage lookup entries and expose a dedicated lookup command.

### Risk 2: Redaction Breaks Auditability
- **Failure mode:** masking removes names but also destroys anchors, stage metadata, or rule references.
- **Plan response:** preserve `comparison_run_id`, `batch_id`, `record_id`, `anchor_row_no`, `stage_id`, `rule_id`, and `rule_version`; redact only configured sensitive values.

### Risk 3: Compatibility Lifecycle Remains Informal
- **Failure mode:** the repo keeps severity but still cannot show owner, transition history, or closure proof.
- **Plan response:** require explicit owner and closure evidence in the model, service, CLI, and tests.

### Risk 4: Workflow Docs Drift from Real Commands
- **Failure mode:** Phase 4 claims an agent workflow, but the runbook references commands or paths that no longer exist.
- **Plan response:** add contract tests that grep the runbook for exact CLI forms and repo paths and fail when docs drift.

## Validation Architecture

### Test Framework

| Property | Value |
|----------|-------|
| Framework | `pytest` via `uv run pytest` |
| Config file | `pyproject.toml` |
| Quick run command | `uv run pytest tests/contracts/test_phase4_lookup_contracts.py tests/contracts/test_phase4_evidence_redaction_contracts.py tests/contracts/test_phase4_compatibility_cli_contracts.py tests/contracts/test_phase4_runbook_contracts.py tests/integration/test_phase4_lineage_lookup.py tests/integration/test_phase4_evidence_redaction.py tests/integration/test_compatibility_adjudication.py -v` |
| Full suite command | `uv run pytest -v` |

### Phase Requirements → Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| OPS-02 | Canonical agent maintenance workflow references exact code/config/test surfaces. | contract | `uv run pytest tests/contracts/test_phase4_runbook_contracts.py -v` | ❌ Wave 0 |
| OPS-03 | `comparison_run_id` plus `record_id` or `anchor_row_no` resolves to source/stage evidence. | contract + integration | `uv run pytest tests/contracts/test_phase4_lookup_contracts.py tests/integration/test_phase4_lineage_lookup.py -v` | ❌ Wave 0 |
| OPS-04 | Observability contracts stay explicit across replay diagnostics, lookup, redaction, and case lifecycle. | contract + integration | `uv run pytest tests/contracts/test_phase4_lookup_contracts.py tests/contracts/test_phase4_evidence_redaction_contracts.py tests/contracts/test_phase4_compatibility_cli_contracts.py tests/contracts/test_phase4_runbook_contracts.py tests/integration/test_phase4_lineage_lookup.py tests/integration/test_phase4_evidence_redaction.py tests/integration/test_compatibility_adjudication.py -v` | ❌ Wave 0 |
| GOV-01 | Evidence artifacts redact configured sensitive fields before persistence. | contract + integration | `uv run pytest tests/contracts/test_phase4_evidence_redaction_contracts.py tests/integration/test_phase4_evidence_redaction.py -v` | ❌ Wave 0 |
| GOV-03 | Compatibility cases record severity, owner, lifecycle status, and closure evidence. | integration + CLI contract | `uv run pytest tests/contracts/test_phase4_compatibility_cli_contracts.py tests/integration/test_compatibility_adjudication.py -v` | ❌ Wave 0 |

### Wave 0 Gaps

- `tests/contracts/test_phase4_lookup_contracts.py` — freeze the lookup CLI contract and evidence-path expectations.
- `tests/integration/test_phase4_lineage_lookup.py` — prove output-to-source lookup works for passed and failed/warning runs.
- `tests/contracts/test_phase4_evidence_redaction_contracts.py` — freeze the governed redaction policy keys and masked package shape.
- `tests/integration/test_phase4_evidence_redaction.py` — prove sensitive values are masked while anchors survive.
- `tests/contracts/test_phase4_compatibility_cli_contracts.py` — freeze compatibility CLI show/transition/close commands.
- `tests/contracts/test_phase4_runbook_contracts.py` — fail when the maintenance workflow docs drift from real command/path surfaces.

## Assumptions Log

| # | Claim | Risk if Wrong |
|---|-------|---------------|
| A1 | A dedicated `replay lookup` command is the most direct OPS-03 surface. | If the project prefers lookup only through `replay diagnose`, plan 04-01 may need a smaller CLI shape but the same underlying lookup contract. |
| A2 | File-backed compatibility cases remain the accepted storage model for this phase. | If a new backing store is required, Phase 4 scope would expand into deferred runtime work and should be re-planned. |
| A3 | A single canonical workflow runbook plus domain runbook references is enough for OPS-02. | If a machine-readable workflow artifact is also required, Plan 04-04 will need a small companion JSON/contract file. |

## Sources

### Primary

- `.planning/phases/04-agent-operations-governance-hardening/04-CONTEXT.md`
- `.planning/ROADMAP.md`
- `.planning/REQUIREMENTS.md`
- `.planning/PROJECT.md`
- `.planning/STATE.md`
- `.planning/phases/03-orchestration-refactor-failure-explainability/03-CONTEXT.md`
- `.planning/phases/03-orchestration-refactor-failure-explainability/03-VERIFICATION.md`
- `.planning/phases/02.1-phase-2-governance-remediation-truthful-gates-and-status-sync/02.1-CONTEXT.md`
- `.planning/codebase/CONCERNS.md`
- `.planning/codebase/STRUCTURE.md`
- `.planning/codebase/TESTING.md`
- `docs/superpowers/specs/2026-04-11-workdatahubpro-rebuild-architecture-draft.md`
- `docs/superpowers/specs/2026-04-11-workdatahubpro-refactor-program.md`
- `docs/superpowers/specs/2026-04-11-workdatahubpro-first-wave-legacy-coverage-matrix.md`
- `src/work_data_hub_pro/governance/evidence_index/file_store.py`
- `src/work_data_hub_pro/apps/orchestration/replay/runtime.py`
- `src/work_data_hub_pro/apps/orchestration/replay/diagnostics.py`
- `src/work_data_hub_pro/platform/tracing/in_memory_trace_store.py`
- `src/work_data_hub_pro/platform/lineage/registry.py`
- `src/work_data_hub_pro/governance/compatibility/models.py`
- `src/work_data_hub_pro/governance/adjudication/service.py`
- `src/work_data_hub_pro/apps/etl_cli/main.py`
- `tests/integration/test_compatibility_adjudication.py`
- `tests/contracts/test_replay_diagnose_contracts.py`

## Metadata

- Confidence in scope boundaries: HIGH
- Confidence in exact module/file placement: MEDIUM
- Confidence in required test boundaries: HIGH

**Research date:** 2026-04-13
**Valid until:** 2026-04-20, because this phase is an active planning surface and the codebase is changing quickly.

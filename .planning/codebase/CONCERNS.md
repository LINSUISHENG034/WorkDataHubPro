# Codebase Concerns

**Analysis Date:** 2026-04-12

## Tech Debt

**Replay Slice Orchestration Duplication:**
- Issue: The three replay orchestrators implement near-identical end-to-end flow with domain-specific literals inline, which increases change drift risk.
- Files: `src/work_data_hub_pro/apps/orchestration/replay/annuity_performance_slice.py`, `src/work_data_hub_pro/apps/orchestration/replay/annual_award_slice.py`, `src/work_data_hub_pro/apps/orchestration/replay/annual_loss_slice.py`
- Impact: Bug fixes in one slice can be missed in the other two; behavioral consistency across domains is fragile.
- Fix approach: Extract a shared orchestration template/helper for invariant stages (intake, processing, identity, derivation, publication, projections, adjudication), then inject domain-specific adapters/config.

**Validation Runtime Embedded As Primary Adapter:**
- Issue: Core execution is hard-wired to in-memory stores and file-backed evidence in hot paths.
- Files: `src/work_data_hub_pro/platform/storage/in_memory_tables.py`, `src/work_data_hub_pro/platform/tracing/in_memory_trace_store.py`, `src/work_data_hub_pro/governance/evidence_index/file_store.py`, `src/work_data_hub_pro/apps/orchestration/replay/*.py`
- Impact: Limits operability and reliability for larger runs; runtime behavior differs from production persistence expectations.
- Fix approach: Add pluggable storage/tracing/evidence interfaces and keep current in-memory/file implementations as test/replay adapters.

**Hard-Coded Release and Fixture Paths in Runtime Code:**
- Issue: Release ids, policy paths, and replay fixture names are embedded directly in orchestration functions.
- Files: `src/work_data_hub_pro/apps/orchestration/replay/annuity_performance_slice.py`, `src/work_data_hub_pro/apps/orchestration/replay/annual_award_slice.py`, `src/work_data_hub_pro/apps/orchestration/replay/annual_loss_slice.py`
- Impact: Configuration rollout requires code edits; misalignment risk between `config/releases/` and runtime path literals.
- Fix approach: Resolve release/policy/fixture locations from explicit run configuration (`RunContext` + domain config mapping) instead of inline `Path(...)` constants.

## Known Bugs

**Annual Award Intake Includes Empty Rows As Records:**
- Symptoms: Blank worksheet rows are emitted as facts with empty/`None` payload fields.
- Files: `src/work_data_hub_pro/capabilities/source_intake/annual_award/service.py`
- Trigger: Any trailing or intermediate fully empty row in `TrusteeAwards` or `InvesteeAwards`.
- Workaround: Pre-clean source workbooks or add explicit empty-row skip logic (pattern already present in `src/work_data_hub_pro/capabilities/source_intake/annual_loss/service.py`).

**Annual Award Plan-Code Lookup Can Return Literal `'None'`:**
- Symptoms: Enrichment may write `plan_code="None"` (string) when history row has null plan code.
- Files: `src/work_data_hub_pro/capabilities/fact_processing/annual_award/plan_code_lookup.py`
- Trigger: Matching lookup candidate with `plan_code` null/empty.
- Workaround: Normalize candidate plan codes before selection (same null-guard pattern used in `src/work_data_hub_pro/capabilities/fact_processing/annual_loss/plan_code_lookup.py`).

## Security Considerations

**Unredacted Trace Evidence Written To Disk:**
- Risk: Raw payloads and field-level before/after values are persisted as plaintext JSON, including business identifiers and names.
- Files: `src/work_data_hub_pro/governance/evidence_index/file_store.py`, `src/work_data_hub_pro/capabilities/source_intake/*/service.py`, `src/work_data_hub_pro/platform/contracts/models.py`
- Current mitigation: Not detected in code (no redaction, encryption, or access control enforcement in writer path).
- Recommendations: Add field-level redaction policy, optional at-rest encryption for evidence artifacts, and path/ACL governance for evidence roots.

**Deterministic Temp Identity Construction:**
- Risk: Fallback IDs embed raw company names (`TEMP-{company_name}`), which can leak business-identifying values into downstream tables and logs.
- Files: `src/work_data_hub_pro/capabilities/identity_resolution/service.py`
- Current mitigation: Fallback level is explicitly marked as temporary in `IdentityResolutionResult`.
- Recommendations: Use opaque generated IDs plus a secured mapping table for unresolved identities.

## Performance Bottlenecks

**Contract State Projection Performs Repeated Linear Scans:**
- Problem: `_has_match` executes `any(...)` scans for each performance row across award/loss fact+fixture arrays.
- Files: `src/work_data_hub_pro/capabilities/projections/contract_state.py`
- Cause: Nested repeated filtering and per-row membership checks create O(n*m) behavior.
- Improvement path: Pre-index rows by `(company_id, plan_code, period)` sets/dicts before looping performance rows.

**Trace Lookup Is Linear Over Entire Event Store:**
- Problem: `find()` scans all events each query, then sorts matches.
- Files: `src/work_data_hub_pro/platform/tracing/in_memory_trace_store.py`
- Cause: Single list-backed store without batch/anchor index.
- Improvement path: Maintain a keyed index by `(batch_id, anchor_row_no)` and append events in sequence order.

## Fragile Areas

**Publication Policy Access Is Not Defensive:**
- Files: `src/work_data_hub_pro/platform/publication/service.py`, `config/policies/publication.json`
- Why fragile: `payload[domain]` and `policy.targets[target_name]` raise immediate `KeyError` on config drift or typo; execution has no structured failure object.
- Safe modification: Add schema validation for policy file and convert lookup failures to typed domain errors before execution starts.
- Test coverage: Gaps in negative-path tests for invalid domain/target policy keys under `tests/integration/`.

**Annual Award Business Type Derivation Uses Binary Else Default:**
- Files: `src/work_data_hub_pro/capabilities/fact_processing/annual_award/service.py`
- Why fragile: Any unexpected `source_sheet` value is treated as `investee_award`, silently misclassifying data.
- Safe modification: Replace ternary with explicit mapping and emit trace error on unknown sheet names.
- Test coverage: No explicit unknown-sheet behavior test in `tests/integration/test_annual_award_processing.py`.

## Scaling Limits

**Validation-Only Storage and Evidence Footprint:**
- Current capacity: Works for test/replay-sized batches with in-memory table and trace lists plus JSON evidence files.
- Limit: Memory growth and filesystem artifact growth become dominant as row counts and domains increase.
- Scaling path: Move tables/traces/evidence to persistent adapters with bounded retention and query indexes.

**Single-Process Replay Execution:**
- Current capacity: CLI drives one replay run synchronously per command.
- Limit: No built-in parallel run coordination, queueing, or failure recovery semantics for large replay backlogs.
- Scaling path: Introduce orchestrated runtime adapter under `src/work_data_hub_pro/apps/orchestration/` with explicit run state and retry policies.

## Dependencies at Risk

**`openpyxl` Runtime Parsing Dependency:**
- Risk: Workbook schema/header variance directly affects ingestion behavior; parser assumptions are strict and domain-specific.
- Impact: Input-format drift can hard-fail ingestion or create malformed payload records.
- Migration plan: Add explicit workbook schema validators and versioned intake contracts before row conversion.

## Missing Critical Features

**First-Wave Runtime/Operator Surfaces Still Deferred:**
- Problem: Program-critical operational surfaces are documented as pending/deferred and are not implemented in `src/work_data_hub_pro/`.
- Blocks: Production-grade rollout for queue runtime, reference sync runtime, enterprise persistence surfaces, and manual operator command parity.
- Files: `docs/superpowers/specs/2026-04-11-workdatahubpro-first-wave-legacy-coverage-matrix.md`, `docs/superpowers/specs/2026-04-11-workdatahubpro-refactor-program.md`

## Test Coverage Gaps

**Negative Intake Contract Handling:**
- What's not tested: Missing sheet names, header mismatch, and malformed workbook column counts for all intake services.
- Files: `src/work_data_hub_pro/capabilities/source_intake/annuity_performance/service.py`, `src/work_data_hub_pro/capabilities/source_intake/annual_award/service.py`, `src/work_data_hub_pro/capabilities/source_intake/annual_loss/service.py`, `tests/integration/test_*_intake.py`
- Risk: Production workbooks with schema drift fail unpredictably or produce silent data-quality issues.
- Priority: High

**Publication Policy and Failure-Path Validation:**
- What's not tested: Unknown policy domain/target handling and partial-write behavior when a bundle fails mid-execution.
- Files: `src/work_data_hub_pro/platform/publication/service.py`, `tests/integration/test_publication_service.py`
- Risk: Runtime config defects surface as abrupt exceptions without controlled rollback/reporting.
- Priority: High

**Sensitive Evidence Handling:**
- What's not tested: Redaction, retention, and access control expectations for evidence artifacts.
- Files: `src/work_data_hub_pro/governance/evidence_index/file_store.py`, `tests/contracts/`
- Risk: Compliance and data exposure risk grows with real replay payloads.
- Priority: Medium

---

*Concerns audit: 2026-04-12*

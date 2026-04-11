# WorkDataHubPro Rebuild Architecture Blueprint

Date: 2026-04-11
Status: Reviewed Draft
Target Workspace: `E:\Projects\WorkDataHubPro`
Legacy Behavioral Reference: `E:\Projects\WorkDataHub`

Validated against legacy evidence:

- `E:\Projects\WorkDataHub\docs\guides\domain-migration\workflow.md`
- `E:\Projects\WorkDataHub\docs\domains\annuity_performance-capability-map.md`
- `E:\Projects\WorkDataHub\docs\domains\annual_award-capability-map.md`

## 1. Executive Summary

1. `WorkDataHubPro` is a behavioral rebuild, not a structural lift-and-shift.
2. The top-level structure should remain capability-first, but publication and orchestration must be modeled explicitly instead of staying hidden in generic hooks or loaders.
3. Governance should not be a hot-path business module. Runtime evidence capture and control-plane adjudication must be separated.
4. The first executable validation slice remains `annuity_performance`, but multi-sheet event domains are part of the system blueprint from day one because `annual_award` already proves that single-sheet assumptions are insufficient.
5. Legacy parity is evidence for adjudication, not permanent architectural supremacy.

### 1.1 Goals

- preserve legacy-equivalent business outcomes while removing black-box rule execution
- make the system agent-friendly for maintenance, operations, and investigation
- improve architecture clarity, runtime observability, and execution efficiency

When these goals conflict, the invariants in Section 3 take precedence over convenience.

### 1.2 Corrections Applied In This Review

- `publish` is promoted from an implicit stage to an explicit platform publication layer.
- `governance` is split into runtime evidence responsibilities and control-plane responsibilities.
- the explainability requirement is anchored to a measurable reference workload: one full monthly `annuity_performance` replay until broader benchmarks exist
- trace contracts are strengthened with `run_id`, `trace_id`, `event_id`, `event_seq`, and `stage_id`
- legacy-to-rebuild mapping rules and acceptance gates are added so the document is executable as a design baseline instead of remaining a narrative draft

## 2. Validation Findings From Legacy

### 2.1 Confirmed By Existing WorkDataHub Behavior

- `annuity_performance` currently spans file discovery, transform, `company_id` resolution, reference backfill, fact publication, post-ETL hooks, and downstream snapshot consequences. The rebuild must decompose this without losing chain closure.
- `annual_award` already depends on multi-sheet merged read, conditional identity handling, optional plan-code enrichment, and downstream snapshot consumption. This means multi-sheet event domains are not edge cases.
- the current migration workflow is domain-folder and registry centric. It is useful for behavior capture and parity discipline, but it must not be copied as the `WorkDataHubPro` structural template.
- `GenericBackfillService` and `cli/etl/hooks.py` are strong behavior references but weak structural references. Their responsibilities need to be redistributed into explicit capabilities and adapters.
- snapshot/status behavior already depends on cross-domain facts such as `annuity_performance`, `annual_award`, and `annual_loss`, so projection boundaries must be explicit from the start.

### 2.2 Architectural Consequences

- single-sheet assumptions are invalid at system level
- post-load hooks should be redesigned as explicit projection use cases
- identity resolution must remain isolated from domain derivation logic
- reference/master derivation must not stay a hidden generic side effect
- publication semantics and transaction scopes must be first-class design objects

## 3. Non-Negotiable Invariants

- business semantics must live in capabilities, not in orchestration adapters, hook registries, or generic utilities
- `fact_processing` must not call external identity services directly
- `reference_derivation` may derive master/reference candidates, but it must not own projection behavior
- `projections` must consume published facts or published reference/master outputs only, never raw intake payloads
- configuration may tune approved parameters and enablement, but it must not silently change transformation semantics or module boundaries
- every material write path must declare `PublicationMode`, idempotency scope, and transaction scope
- every unexpected output must be explainable by `batch_id + anchor_row_no` with rule-hit evidence and before/after field deltas
- until broader baselines exist, the explainability SLO is: for one full monthly `annuity_performance` replay, an operator can retrieve primary evidence within 5 minutes

## 4. Corrected Reference Architecture

### 4.1 Layer Model

| Layer | Owns | Must Not Own |
|------|------|---------------|
| Business capabilities | business semantics, domain contracts, domain rule execution | orchestration policy, hidden shared side effects |
| Platform runtime | contract enforcement, tracing, lineage, publication, storage, execution helpers | business rules, domain meaning |
| Governance control plane | config release, compatibility adjudication, shadow runs, evidence indexing | hot-path rule execution, field derivation |
| Execution adapters | CLI, Dagster, replay, scheduling, operator entry points | transformation semantics, adjudication logic |

### 4.2 Primary Flow

```text
Execution adapters
  -> source_intake
  -> fact_processing
  -> identity_resolution
  -> reference_derivation
  -> publication
  -> projections

Platform runtime services wrap each stage:
  contracts, tracing, lineage, storage, execution helpers

Governance control plane consumes runtime evidence:
  config release, compatibility cases, shadow runs, evidence index, adjudication
```

### 4.3 Business Capability Modules

1. `source_intake`
2. `fact_processing`
3. `identity_resolution`
4. `reference_derivation`
5. `projections`

`publication` is intentionally not a business capability. It is a platform runtime service used by multiple capabilities with explicit contracts.

### 4.4 Platform Runtime Services

- `contracts`
- `tracing`
- `lineage`
- `publication`
- `storage`
- `execution`

### 4.5 Governance Control Plane

- `compatibility`
- `config_release`
- `shadow_run`
- `evidence_index`
- `adjudication`

### 4.6 Execution Adapters

- `etl_cli`
- `dagster`
- `replay_runner`
- `adjudication_cli`
- `operator_tools`

## 5. Capability Boundaries And System Contracts

### 5.1 Capability Responsibilities

`source_intake`

- batch definition
- file discovery
- workbook reading
- input snapshotting
- original row anchoring

`fact_processing`

- domain-specific normalization
- cleansing rule execution
- field derivation into canonical facts

`identity_resolution`

- `company_id` resolution
- cache lookup
- provider integration
- temp-id fallback
- identity evidence capture

`reference_derivation`

- candidate generation for master/reference updates
- derived master/reference decisions
- publication planning inputs for reference/master targets

`projections`

- downstream contract state
- monthly snapshots
- status views
- projection-only read models derived from published facts

### 5.2 Platform Runtime Responsibilities

`publication`

- execute explicit publication plans
- expose transaction groups and idempotency scopes
- separate fact publication, reference publication, and projection publication into visible write scopes

`tracing` and `lineage`

- record field-level change events
- preserve row anchors across split, merge, and reorder operations
- expose queryable trace views for humans and agents

`contracts`

- validate stage inputs and outputs
- prevent boundary drift between capabilities

### 5.3 Minimum System Contracts

`InputBatch`

- `batch_id`
- `domain`
- `period`
- `source_files`
- `input_snapshot_id`
- `row_count`

`InputRecord`

- `run_id`
- `record_id`
- `batch_id`
- `anchor_row_no`
- `origin_row_nos[]`
- `parent_record_ids[]`
- `stage_row_no`
- `raw_payload`

`CanonicalFactRecord`

- `run_id`
- `record_id`
- `batch_id`
- `domain`
- `fact_type`
- `fields`
- `lineage_ref`
- `trace_ref`

`FieldTraceEvent`

- `trace_id`
- `event_id`
- `event_seq`
- `run_id`
- `batch_id`
- `record_id`
- `anchor_row_no`
- `stage_id`
- `field_name`
- `value_before`
- `value_after`
- `rule_id`
- `rule_version`
- `config_release_id`
- `action_type`
- `timestamp`
- `success`
- `error_message` when failed

`IdentityResolutionResult`

- `record_id`
- `resolved_identity`
- `resolution_method`
- `fallback_level`
- `evidence_refs`

`DerivationCandidate`

- `target_object`
- `candidate_payload`
- `source_record_ids`
- `derivation_rule_id`
- `derivation_rule_version`

`PublicationTarget`

- `target_name`
- `target_kind`
- `storage_adapter`
- `write_contract`
- `transaction_scope`

`PublicationPlan`

- `publication_id`
- `target_name`
- `target_kind`
- `mode`
- `refresh_keys`
- `upsert_keys`
- `source_batch_id`
- `source_run_id`
- `idempotency_scope`
- `transaction_group`

`PublicationResult`

- `publication_id`
- `target_name`
- `mode`
- `affected_rows`
- `transaction_group`
- `success`
- `error_message`

`ProjectionResult`

- `projection_name`
- `source_publications`
- `affected_rows`
- `success`
- `error_message`

`CompatibilityCase`

- `case_id`
- `sample_locator`
- `legacy_result`
- `pro_result`
- `decision_status`
- `business_rationale`
- `approved_by`
- `affected_rule_version`

### 5.4 Lineage Rules

- field-level change events are the single source of truth for explainability
- row-level payloads are retained as context, not as a competing truth model
- `anchor_row_no` is the primary accountability anchor
- `origin_row_nos[]` and `parent_record_ids[]` are required whenever split, merge, or reorder changes the local row context
- merged records default to the minimum original source row as the primary displayed anchor, while still exposing all source rows

## 6. Governed Subsystems

### 6.1 Cleansing Architecture

Cleansing is a governed subsystem, not an implementation detail inside `fact_processing`.

Cleansing consists of:

- rule packs defined in code
- domain-scoped rule configuration
- a constrained runtime manifest
- traceable rule execution events

Code owns:

- cleansing rule semantics
- normalization functions
- parser/formatter logic
- category implementations such as date, numeric, and string cleansing

Configuration owns:

- enablement
- thresholds and literals
- ordered activation within approved domain scope
- domain-specific parameter values

Each cleansing effect must be attributable to:

- `rule_pack_id`
- `rule_pack_version`
- `config_release_id`
- `domain`

Registry rule:

- the runtime manifest may answer which rule pack and config release are active
- it must not become a hidden singleton that owns business logic through mutable runtime state

### 6.2 External Identity Integration Contract

External lookup integration, including EQC-like providers, belongs inside `identity_resolution`.

Required interfaces:

- `IdentityProvider`
- `IdentityCache`
- `AuthTokenProvider`
- `DeferredLookupQueue` when asynchronous lookup is introduced

Guardrails:

- `fact_processing` never calls external services directly
- authentication and token refresh logic are forbidden inside domain rule code
- cache hit, external lookup, and temp-id fallback must each emit explicit evidence
- provider unavailability must degrade to governed fallback behavior, not silent rule skipping

Phase strategy:

- early validation may run in cache-first mode
- replay mode is acceptable in early phases
- provider-disabled mode is acceptable only if the interface contract already exists and evidence still records the chosen fallback path

### 6.3 Publication And Loading Modes

Publication semantics are first-class and must be explicit in the architecture.

Required publication objects:

- `PublicationPlan`
- `PublicationTarget`
- `PublicationMode`
- `PublicationResult`

Supported modes:

- `REFRESH`: delete + insert for detail-style fact targets
- `UPSERT`: conflict-aware write for aggregate/master targets
- `APPEND_ONLY`: immutable evidence and governance logs

Transaction rule:

- fact publication, derivation publication, and projection publication must be separately visible transaction scopes
- the system must not hide all writes inside one opaque loader path

### 6.4 Configuration Governance And Compatibility

Configuration governance should use one asset model with increasing gate strength.

Layers:

- local experimental layer
- shared rebuild layer
- formal baseline layer

Hard rule:

- local experimental configuration must never affect shared batch results

Compatibility strategy:

- use golden samples for fast protection
- use historical batch replay for final acceptance
- adjudicate differences case by case against business semantics and explicit rules

Compatibility precedent rule:

- every adjudicated difference becomes a queryable `CompatibilityCase`
- agents may propose adjudications
- human approval is required before precedent admission

## 7. First Validation Slice

### 7.1 Selected Slice

`annuity_performance` remains the first validation slice because the legacy evidence shows it already exercises the most coupled path: intake, cleansing, identity, reference derivation, fact publication, and downstream snapshot consequences.

### 7.2 Required End-To-End Chain

The slice is only considered closed when this chain is explicit:

`source_intake -> fact_processing -> identity_resolution -> reference_derivation -> publication -> contract_state projection -> monthly_snapshot projection -> runtime evidence -> governance adjudication`

### 7.3 Fixtures, Dependencies, And Exclusions

- `annual_award` and `annual_loss` remain read-only fixtures or replayed fact dependencies in the first phase
- multi-sheet event domains must still be represented in the blueprint as first-class archetypes from day one
- GUI and manual EQC tooling are out of scope for the first validation slice
- live external provider integration may remain behind cache/replay mode in the first phase
- `sandbox_trustee_performance` is excluded unless later promoted into a real business target

### 7.4 Validation-Slice Execution Order

1. lock the reference baseline
2. close intake and trace root
3. close fact processing and cleansing trace
4. connect identity resolution
5. close reference derivation
6. make publication explicit
7. close projections
8. run replay and adjudication loop
9. admit approved compatibility cases

### 7.5 Slice Completion Standard

- the full chain closes without hidden hook-only business logic
- rule-hit evidence is queryable by `batch_id + anchor_row_no`
- publication modes are explicit and visible
- projection outputs are validated with cross-domain fixtures
- compatibility decisions are stored as explicit cases instead of informal notes

## 8. Legacy-To-Rebuild Mapping Rules

| Legacy Behavior Source | Rebuild Target | Carry Forward | Do Not Carry Forward |
|------|------|------|------|
| `src/work_data_hub/domain/*/pipeline_builder.py` | `capabilities/fact_processing/*` | rule behavior, field semantics, protected tests | monolithic domain folder as universal architecture pattern |
| `src/work_data_hub/domain/reference_backfill/generic_service.py` | `capabilities/reference_derivation/*` plus `platform/publication` | derivation behavior, aggregation rules, validation assets | hidden generic side effects and oversized shared-service abstraction |
| `src/work_data_hub/cli/etl/hooks.py` | `apps/orchestration/*` plus `capabilities/projections/*` | orchestration order evidence and projection triggering needs | hooks as architectural center |
| `src/work_data_hub/customer_mdm/*` | `capabilities/projections/*` | projection semantics, status definitions, protected tests | cross-module mutation through opaque side effects |
| `src/work_data_hub/infrastructure/enrichment/*` | `capabilities/identity_resolution/*` | resolver behavior, cache strategy, provider contracts | direct domain-to-provider coupling |
| `config/*.yml` and verified rule files | `config/domains/`, `config/policies/`, `config/releases/` | approved parameters, mappings, releaseable config assets | mutable runtime state that silently changes semantics |
| `docs/guides/domain-migration/workflow.md` | migration playbook only | parity discipline, documentation discipline | old architecture template and 8-file domain folder as the target end state |

Migration rule:

- carry forward behavior, rules, and verification assets
- do not carry forward high-coupling shared-service structures, implicit hook chains, or oversized pipeline-builder files as architecture patterns

## 9. Repository Layout

Recommended top-level layout:

```text
WorkDataHubPro/
├── docs/
│   ├── architecture/
│   ├── adr/
│   ├── domains/
│   ├── runbooks/
│   └── superpowers/specs/
├── config/
│   ├── domains/
│   ├── policies/
│   └── releases/
├── data_contracts/
├── reference/
│   ├── golden_samples/
│   ├── historical_replays/
│   └── compatibility_cases/
├── scripts/
├── src/work_data_hub_pro/
│   ├── capabilities/
│   ├── platform/
│   ├── governance/
│   └── apps/
├── tests/
│   ├── contracts/
│   ├── golden/
│   ├── replay/
│   ├── integration/
│   └── performance/
└── pyproject.toml
```

Recommended source layout:

```text
src/work_data_hub_pro/
├── capabilities/
│   ├── source_intake/
│   ├── fact_processing/
│   │   ├── annuity_performance/
│   │   ├── annuity_income/
│   │   ├── annual_award/
│   │   └── annual_loss/
│   ├── identity_resolution/
│   ├── reference_derivation/
│   └── projections/
├── platform/
│   ├── contracts/
│   ├── execution/
│   ├── tracing/
│   ├── lineage/
│   ├── publication/
│   └── storage/
├── governance/
│   ├── adjudication/
│   ├── compatibility/
│   ├── config_release/
│   ├── shadow_run/
│   └── evidence_index/
└── apps/
    ├── etl_cli/
    ├── orchestration/
    │   ├── dagster/
    │   ├── replay/
    │   └── scheduling/
    ├── adjudication_cli/
    └── operator_tools/
```

Directory rules:

- `platform/` may contain technical capabilities, but it must not own business semantics
- `apps/` may orchestrate calls, but must not contain business rules
- `governance/` may evaluate evidence and control releases, but must not be required to calculate hot-path field values
- `shared/`, `common/`, `misc/`, and unlimited top-level `utils/` are anti-patterns and should be avoided

### 9.1 Intake Archetypes

The blueprint must support multiple intake archetypes explicitly.

Required archetypes:

- single-sheet workbook domains
- multi-sheet merged workbook domains

Current mapping from legacy evidence:

- single-sheet: `annuity_performance`, `annuity_income`
- multi-sheet merged: `annual_award`, `annual_loss`

## 10. Acceptance Gates And Open Questions

### 10.1 Blueprint Readiness Gate

The blueprint is ready for execution only when all of the following are true:

- publication is modeled explicitly in both contracts and repository layout
- governance responsibilities are split cleanly between runtime evidence and control-plane decisions
- the first-slice chain is defined end to end
- capability boundaries and anti-boundaries are documented
- config governance and compatibility precedent rules are explicit

### 10.2 Slice Readiness Gate

The first validation slice is ready to start only when:

- the reference baseline and replay assets are locked
- `annuity_performance` scope and cross-domain fixtures are confirmed
- trace and publication contracts are accepted
- the projection success criteria are agreed before implementation begins

### 10.3 Open Questions

These questions do not invalidate the blueprint, but they should be resolved before broad domain rollout:

1. Where will `CompatibilityCase` and evidence-index storage live physically: repository-managed artifacts, database tables, or both?
2. Will publication execution remain fully synchronous inside the ETL run, or will some targets use deferred execution behind explicit transaction groups?
3. After `annuity_performance`, should the second executable slice be `annual_award` or `annual_loss` to validate the multi-sheet archetype sooner?
4. What is the long-term explainability benchmark beyond the initial monthly `annuity_performance` replay reference workload?

## 11. Final Position

`WorkDataHubPro` should be rebuilt as a capability-first system with an explicit runtime publication layer, explicit projection boundaries, and a separated governance control plane. The architecture is only successful if it can make the most opaque legacy flows explainable, queryable, and governable without recreating shared black-box layers under new names.

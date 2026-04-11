# First-Wave Legacy Coverage Risk Register For WorkDataHubPro Rebuild

**Date:** 2026-04-11
**Author:** Codex
**Purpose:** Maintain one governance-aligned first-wave risk register that merges the earlier direct legacy-mismatch review with the supplemental structural coverage review.

---

## Current Governance Position

- `annuity_performance` remains an accepted validation slice.
- `annual_award` remains an accepted multi-sheet validation slice.
- `annual_loss` and `annuity_income` remain unclosed first-wave executable slices.
- This register does **not** roll back accepted validation evidence by itself.
- This register exists to prevent first-wave legacy behavior from remaining implicit, overstated, or split across competing review documents.

---

## Status Vocabulary Used Here

Each risk uses one governance-aligned position:

- `accepted but narrowed`: current validation slice is accepted, but the validated runtime is intentionally narrower than the full legacy behavior surface
- `pending first-wave gap`: behavior is in first-wave scope and still needs explicit coverage work or an explicit retirement decision
- `planned follow-on`: the gap is admitted and expected to be handled by an approved or clearly identified follow-on plan
- `deferred runtime/operator gap`: valid concern, but intentionally postponed behind current validation priorities
- `invalid or outdated claim`: the earlier review wording no longer reflects the current repository state or used the wrong architectural boundary

---

## Canonical Risk Register

| Risk ID | Canonical Risk | Merged From | Current Position | Matrix Mapping |
|------|----------------|-------------|------------------|----------------|
| `CR-001` | legacy identity-source lineage, override mapping, and post-load backfill parity | original risks 1, 4, 11 | `pending first-wave gap` | `AP-003`, `CT-006` |
| `CR-002` | pre-load reference bootstrap and missing-code creation semantics outside the explicit publication chain | original risk 2 | `pending first-wave gap` | `CT-007` |
| `CR-003` | multi-slice execution ordering and cross-domain dependency closure for downstream projection correctness | original risk 3 | `pending first-wave gap` | `XD-001`, `XD-002`, `CT-010` |
| `CR-004` | reference/master semantic breadth and governed aggregation parity | supplemental `SFR-001`, original risk 9 | `pending first-wave gap` | `AP-004`, `AA-005`, `CT-002` |
| `CR-005` | publication key/delete-scope and sink write-contract parity | supplemental `SFR-002` | `planned follow-on` | `AP-005`, `CT-003` |
| `CR-006` | customer-contract and snapshot projection semantic-width parity | supplemental `SFR-003`, original risk 5 | `pending first-wave gap` | `AP-006`, `CT-004` |
| `CR-007` | governed string normalization and plan-code correction parity across first-wave domains | original risks 6, 7 | `pending first-wave gap` | `AP-002`, `AI-002`, `CT-008` |
| `CR-008` | history-aware event-domain lookup and temporal enrichment semantics | supplemental `SFR-004` | `pending first-wave gap` | `AA-004`, `AL-003`, `CT-005` |
| `CR-009` | `annuity_income` operator-facing artifact contract | supplemental `SFR-005` | `pending first-wave gap` | `AI-004` |
| `CR-010` | `annuity_income` service-delegation and explicit no-hook runtime contract | supplemental `SFR-006` | `pending first-wave gap` | `AI-005` |
| `CR-011` | directory-based discovery and workbook version arbitration beyond replay-only CLI input | supplemental `SFR-007` | `deferred runtime/operator gap` | `CT-001` |
| `CR-012` | annual lifecycle and January-only status initialization semantics | original risk 10 | `pending first-wave gap` | `CT-009` |
| `CR-013` | dynamic FK creation as a legacy operational mechanism | original risk 8 | `invalid or outdated claim` | no new row; covered indirectly by production storage/publication design follow-on |

---

## Detailed Risks

### `CR-001` Legacy Identity-Source Lineage, Override Mapping, And Post-Load Backfill Parity

This risk combines the earlier review's strongest identity-related warnings:

- hardcoded plan-to-company override mappings
- former-name lineage sourced through Mongo-to-MySQL sync
- post-load SQL-template backfill that repairs `company_id` after ETL

Current `WorkDataHubPro` proves a cache-first validation resolver with explicit evidence, but it does **not** yet prove parity for the broader identity-source surface described by the legacy first-wave domains.

Repository evidence:

- [identity_resolution/service.py](/E:/Projects/WorkDataHubPro/src/work_data_hub_pro/capabilities/identity_resolution/service.py#L43)
- [annuity_performance-capability-map.md](/E:/Projects/WorkDataHub/docs/domains/annuity_performance-capability-map.md#L139)

Why this remains open:

- the accepted slice proves stage isolation and evidence capture
- it does not yet prove parity for legacy override catalogs, former-name lineage, or downstream repair/update paths

Governance action:

- keep `AP-003` accepted as the validation baseline
- track the parity gap explicitly through `CT-006`

### `CR-002` Pre-Load Reference Bootstrap And Missing-Code Creation Semantics

Legacy `prefix_processing()` creates or updates required reference rows before the main ETL loop. That is not the same concern as generic reference derivation after canonical fact processing.

Why this matters:

- if the legacy flow depends on those rows existing before downstream processing, a purely post-processing derivation model can still miss valid behavior

Why this remains open:

- current validation slices prove explicit reference derivation and publication
- they do not yet prove equivalence for pre-load reference bootstrap semantics

Governance action:

- register the behavior explicitly through `CT-007`
- decide later whether the behavior should be rebuilt, absorbed into a cleaner explicit pre-publication contract, or retired

### `CR-003` Multi-Slice Execution Ordering And Cross-Domain Dependency Closure

Legacy downstream status correctness depends on ordered cross-domain execution:

- `annuity_performance` hook behavior must complete in order
- `annual_award` and `annual_loss` facts must be available when snapshot/status logic needs them

Current `WorkDataHubPro` state:

- accepted slices prove fixture-backed dependencies
- the full multi-slice execution contract is still not closed

Repository evidence:

- [annuity_performance-capability-map.md](/E:/Projects/WorkDataHub/docs/domains/annuity_performance-capability-map.md#L75)
- [contract_state.py](/E:/Projects/WorkDataHubPro/src/work_data_hub_pro/capabilities/projections/contract_state.py#L34)

Governance action:

- preserve `XD-001` and `XD-002` as active dependencies
- add `CT-010` so ordering closure becomes a tracked asset instead of a note buried in dependency prose

### `CR-004` Reference/Master Semantic Breadth And Governed Aggregation Parity

Legacy first-wave coverage includes more than a generic company-reference write path. It includes:

- customer tags
- customer-type derivation
- weighted selection behavior such as `max_by(order_column="固费")`
- aggregation semantics that were previously expressed through config plus code, including unsafe lambda-based aggregation in legacy config

Current `WorkDataHubPro` state:

- derivation plumbing is proven
- full aggregation/semantic breadth is not

Repository evidence:

- [reference_derivation/service.py](/E:/Projects/WorkDataHubPro/src/work_data_hub_pro/capabilities/reference_derivation/service.py#L9)
- [annuity_income-capability-map.md](/E:/Projects/WorkDataHub/docs/domains/annuity_income-capability-map.md#L137)

Governance action:

- keep accepted derivation rows accepted
- use `CT-002` to track remaining semantic breadth
- do **not** treat legacy `lambda` config execution as a required feature to carry forward unchanged

### `CR-005` Publication Key/Delete-Scope And Sink Write-Contract Parity

Current publication runtime proves explicit visibility:

- mode
- transaction group
- idempotency scope

It does **not** yet prove parity for:

- legacy table-specific delete scopes
- sink-specific PK semantics
- final storage adapter contracts

Repository evidence:

- [publication.json](/E:/Projects/WorkDataHubPro/config/policies/publication.json#L2)
- [platform/publication/service.py](/E:/Projects/WorkDataHubPro/src/work_data_hub_pro/platform/publication/service.py#L76)

Governance action:

- track through `CT-003`
- keep this as `planned follow-on`, not as an immediate rollback of accepted validation slices

### `CR-006` Customer-Contract And Snapshot Projection Semantic-Width Parity

The earlier review claimed a P0 SCD2 discrepancy, but that claim used the wrong current-path evidence and overstated the present repository state.

What remains valid:

- legacy customer-contract and snapshot semantics are much richer than the current validation bridge projections

What is invalid in the earlier wording:

- the cited "new implementation" path did not exist in this repository as written
- the issue is broader than one SCD2 function; it is a projection semantic-width question

Repository evidence:

- [contract_state.py](/E:/Projects/WorkDataHubPro/src/work_data_hub_pro/capabilities/projections/contract_state.py#L15)
- [monthly_snapshot.py](/E:/Projects/WorkDataHubPro/src/work_data_hub_pro/capabilities/projections/monthly_snapshot.py#L8)

Governance action:

- retire the earlier P0 wording as stated
- track the real remaining work through `CT-004`

### `CR-007` Governed String Normalization And Plan-Code Correction Parity

This combines the earlier review's cleansing warnings:

- silent plan-code corrections
- broad company-name normalization and regex cleanup

Current `WorkDataHubPro` state:

- current cleansing runtime is explicit and governed
- the semantic breadth is still much narrower than legacy

Repository evidence:

- [rules.py](/E:/Projects/WorkDataHubPro/src/work_data_hub_pro/capabilities/fact_processing/cleansing/rules.py#L15)
- [annuity_performance-capability-map.md](/E:/Projects/WorkDataHub/docs/domains/annuity_performance-capability-map.md#L137)

Governance action:

- track the parity gap through `CT-008`
- keep current accepted processing rows accepted as the validated baseline, not as the final parity statement

### `CR-008` History-Aware Event-Domain Lookup And Temporal Enrichment Semantics

Current event-domain slices prove:

- source-aware identity handling
- replay-backed contract-history lookup
- fallback defaults

They do **not** yet prove a full temporal contract for historical/current contract selection or broader event-domain replay semantics needed by `annual_loss`.

Repository evidence:

- [plan_code_lookup.py](/E:/Projects/WorkDataHubPro/src/work_data_hub_pro/capabilities/fact_processing/annual_award/plan_code_lookup.py#L22)
- [annual_loss-capability-map.md](/E:/Projects/WorkDataHub/docs/domains/annual_loss-capability-map.md#L148)

Governance action:

- track through `CT-005`
- use `AA-004` as accepted validation evidence, not as proof of full temporal parity

### `CR-009` `annuity_income` Operator-Facing Artifact Contract

Legacy `annuity_income` includes operator-facing artifacts such as unresolved-name export and failed-record export. Those are runtime outputs that matter operationally even though they are not fact-table fields.

Repository evidence:

- [annuity_income-capability-map.md](/E:/Projects/WorkDataHub/docs/domains/annuity_income-capability-map.md#L64)

Governance action:

- track explicitly through `AI-004`

### `CR-010` `annuity_income` Service-Delegation And No-Hook Runtime Contract

Legacy `annuity_income` has a distinct execution shape:

- service-delegation rather than the same adapter/replay shape used elsewhere
- explicit absence of post-ETL hooks as part of the runtime contract

Repository evidence:

- [annuity_income-capability-map.md](/E:/Projects/WorkDataHub/docs/domains/annuity_income-capability-map.md#L62)
- [annuity_income-capability-map.md](/E:/Projects/WorkDataHub/docs/domains/annuity_income-capability-map.md#L76)

Governance action:

- track explicitly through `AI-005`

### `CR-011` Directory-Based Discovery And Workbook Version Arbitration Beyond Replay-Only CLI Input

Current `WorkDataHubPro` replay CLI accepts an explicit workbook path. That is suitable for validation, but it is narrower than the operator-facing discovery/version selection behavior present in legacy ETL workflows.

Repository evidence:

- [apps/etl_cli/main.py](/E:/Projects/WorkDataHubPro/src/work_data_hub_pro/apps/etl_cli/main.py#L18)

Governance action:

- track through `CT-001`
- keep the item `deferred` until Phase E runtime/operator closure work is admitted

### `CR-012` Annual Lifecycle And January-Only Status Initialization Semantics

The earlier review correctly identified that legacy has January-specific annual initialization behavior. That concern remains valid, but it is not yet represented explicitly in the active first-wave matrix.

Governance action:

- register through `CT-009`

### `CR-013` Dynamic FK Creation As A Legacy Operational Mechanism

The earlier review treated runtime FK creation as a low-risk operational difference. That remains the right overall direction, but it should not be treated as a core first-wave behavior gap by itself.

Why this is `invalid or outdated` as a standalone first-wave coverage claim:

- current repository runtime is still validation-mode in-memory/file-backed
- the old wording assumed a concrete new production schema/runtime that is not yet the active implementation baseline

Governance action:

- no dedicated new matrix row
- treat future physical FK enforcement as part of broader production storage/publication design

---

## Earlier Claims Retired Or Corrected During Merge

The merged register intentionally retires or rewrites several earlier claims:

1. The earlier P0 statement that no identity-resolution coverage existed was too strong.
Current position:
`AP-003` is accepted as a validation baseline, but broader identity-source parity remains open through `CT-006`.

2. The earlier SCD2 risk cited the wrong current-path evidence.
Current position:
the real open concern is projection semantic width, tracked through `CT-004`.

3. The earlier recommendation to model dependency ordering inside the governance layer used the wrong boundary.
Current position:
ordering closure belongs in explicit runtime/orchestration and projection behavior, tracked through `CT-010`.

4. The earlier runtime assumptions about PostgreSQL/FK behavior were ahead of the current repository baseline.
Current position:
production storage concerns remain follow-on runtime work, not proof that the present validation architecture has already failed.

---

## Coverage Matrix Registration Decision

This merged register requires the active first-wave matrix to track:

- `AI-004`
- `AI-005`
- `CT-001`
- `CT-002`
- `CT-003`
- `CT-004`
- `CT-005`
- `CT-006`
- `CT-007`
- `CT-008`
- `CT-009`
- `CT-010`

These rows are intentionally additive. They make unclosed first-wave behavior explicit without invalidating already accepted validation-slice evidence.

---

## Final Position

The earlier review and the supplemental review are now superseded by this single register.

The central conclusion is unchanged:

- `WorkDataHubPro` has proven that the corrected capability-first architecture can close validation slices
- it has **not** yet proven full first-wave legacy coverage

What changes in this merged version is the governance precision:

- accepted validation evidence stays accepted
- still-open first-wave gaps are made explicit
- outdated or over-broad claims are corrected instead of repeated

That gives the program one canonical risk source to use when admitting new slices, planning follow-on runtime work, or deciding what can be deferred or retired.

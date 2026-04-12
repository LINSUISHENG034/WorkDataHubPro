# WorkDataHubPro First-Wave Legacy Coverage Matrix

Date: 2026-04-11
Status: Active Coverage Baseline
Scope: First-Wave Domains Only

## 1. Purpose

This document tracks whether the first-wave legacy behaviors and operational
assets from `WorkDataHub` have been:

- rebuilt and accepted in `WorkDataHubPro`
- explicitly deferred
- explicitly retired

It is not a narrative design document. Each row should represent one behavior,
asset, or operational responsibility that can be judged independently.

## 2. Usage Rules

- No new slice should start unless its target legacy behavior already appears in this matrix.
- No row may move to `accepted` without explicit validation evidence.
- No row may move to `retired` without an explicit retirement decision.
- `Deferred` is allowed only with a reason and a future trigger to revisit.
- This matrix is the first-wave coverage tracker for:
  - `annuity_performance`
  - `annual_award`
  - `annual_loss`
  - `annuity_income`

## 3. Status Model

| Status | Meaning |
|------|---------|
| `pending` | known legacy behavior not yet scheduled into an approved execution path |
| `planned` | behavior is in scope of an approved or clearly identified follow-on plan |
| `in_progress` | active implementation is underway |
| `accepted` | rebuilt with committed validation evidence |
| `deferred` | intentionally postponed with written reason |
| `retired` | intentionally removed or superseded with written rationale |

## 4. Column Definitions

| Column | Meaning |
|------|---------|
| `Legacy Source` | actual legacy code, config, docs, or runbook path |
| `Behavior / Asset` | smallest reviewable behavior or operational artifact |
| `Category` | capability / mechanism / config / projection / operator / replay / integration |
| `Rebuild Target` | expected replacement or governance target in `WorkDataHubPro` |
| `Target Boundary` | `capabilities` / `platform` / `governance` / `apps` / `docs` / `reference` |
| `Owning Spec / Plan` | current governing spec or follow-on plan placeholder |
| `Validation Evidence` | proof required to move the row to `accepted` |
| `Retirement Decision` | replacement or removal outcome when the row is retired |

## 5. Coverage Summary

| Domain | Current Position | Highest-Risk Gap |
|------|-------------------|------------------|
| `annuity_performance` | first executable slice accepted | production runtime and operator follow-on work still deferred |
| `annual_award` | accepted multi-sheet slice | `annuity_income` remains the only unclosed first-wave breadth work |
| `annual_loss` | accepted breadth-closure slice | `annuity_income` remains the only unclosed first-wave domain |
| `annuity_income` | next recommended single-sheet breadth slice | no accepted executable slice yet |

## 6. Domain Coverage

### 6.1 `annuity_performance`

| Row ID | Behavior / Asset | Category | Legacy Source | Rebuild Target | Target Boundary | Owning Spec / Plan | Status | Validation Evidence | Retirement Decision | Notes / Risks |
|------|-------------------|----------|---------------|----------------|-----------------|--------------------|--------|---------------------|--------------------|---------------|
| AP-001 | single-sheet workbook intake and anchor-preserving row capture | capability | `docs/domains/annuity_performance-capability-map.md`, legacy file discovery/read path | `capabilities/source_intake/annuity_performance/service.py` | `capabilities` | architecture blueprint + annuity performance slice plan | `accepted` | `tests/integration/test_annuity_performance_intake.py`, replay tests | N/A | accepted in first slice |
| AP-002 | governed cleansing and canonical fact processing | capability | `docs/domains/annuity_performance-capability-map.md`, legacy pipeline builder behavior | `capabilities/fact_processing/annuity_performance/`, `config/domains/annuity_performance/cleansing.json` | `capabilities` + `config` | architecture blueprint + annuity performance slice plan | `accepted` | `tests/integration/test_annuity_performance_processing.py`, replay tests | N/A | rule-pack versioning now explicit |
| AP-003 | `company_id` resolution chain with fallback evidence | mechanism | legacy enrichment / resolver chain documented in capability map | `capabilities/identity_resolution/` | `capabilities` | architecture blueprint + annuity performance slice plan | `accepted` | `tests/integration/test_identity_resolution.py`, replay evidence | N/A | current mode is cache-first validation implementation |
| AP-004 | reference/master candidate derivation from normalized facts | mechanism | legacy reference backfill behavior documented in capability map | `capabilities/reference_derivation/` plus explicit publication | `capabilities` + `platform` | architecture blueprint + annuity performance slice plan | `accepted` | `tests/integration/test_reference_derivation.py`, publication tests | N/A | hidden generic side effect removed from hot path |
| AP-005 | explicit fact/reference/projection publication scopes | mechanism | legacy load + hidden write ordering from loader/hook chain | `platform/publication/`, `platform/storage/`, `config/policies/publication.json` | `platform` + `config` | architecture blueprint + annuity performance slice plan | `accepted` | `tests/integration/test_publication_service.py`, replay tests | N/A | production storage still deferred |
| AP-006 | downstream contract-state and monthly snapshot consequences | projection | legacy customer MDM hook and snapshot consequences described in capability map | `capabilities/projections/` | `capabilities` | architecture blueprint + annuity performance slice plan | `accepted` | `tests/integration/test_projection_outputs.py`, replay tests | N/A | first slice uses fixture-backed cross-domain dependencies |
| AP-007 | replay evidence, compatibility adjudication, and explainability retrieval | replay | legacy parity / operator verification references | `governance/evidence_index/`, `governance/adjudication/`, replay assets, runbook | `governance` + `reference` + `docs` | architecture blueprint + annuity performance slice plan | `accepted` | `tests/replay/test_annuity_performance_slice.py`, `tests/replay/test_annuity_performance_explainability_slo.py`, runbook | N/A | accepted for validation runtime only |
| AP-008 | production storage and deferred publication runtime for this domain | operator | legacy runtime and DB-backed execution expectations | follow-on production storage/publication design | `platform` + `apps` | follow-on production storage/publication plan | `deferred` | future production runtime plan and acceptance evidence | to be decided after production design | current validation runtime is intentionally in-memory/file-backed; revisit when Phase E is admitted or before any first-wave domain is promoted beyond validation-only runtime |

### 6.2 `annual_award`

| Row ID | Behavior / Asset | Category | Legacy Source | Rebuild Target | Target Boundary | Owning Spec / Plan | Status | Validation Evidence | Retirement Decision | Notes / Risks |
|------|-------------------|----------|---------------|----------------|-----------------|--------------------|--------|---------------------|--------------------|---------------|
| AA-001 | multi-sheet workbook merge intake | capability | `docs/domains/annual_award-capability-map.md`, legacy migration workflow | `capabilities/source_intake/annual_award/service.py` | `capabilities` | architecture blueprint + annual award slice plan | `accepted` | `tests/integration/test_annual_award_intake.py`, `tests/replay/test_annual_award_slice.py` | N/A | merged anchors stay queryable by batch + anchor row |
| AA-002 | canonical award event transformation | capability | `docs/domains/annual_award-capability-map.md` | `capabilities/fact_processing/annual_award/` | `capabilities` | architecture blueprint + annual award slice plan | `accepted` | `tests/integration/test_annual_award_processing.py`, `tests/replay/test_annual_award_slice.py` | N/A | governed rule-pack binding is explicit |
| AA-003 | optional `company_id` resolution path for award rows | mechanism | annual award capability map, legacy enrichment behavior | shared `identity_resolution` contract plus award-specific wiring | `capabilities` | architecture blueprint + annual award slice plan | `accepted` | `tests/integration/test_identity_resolution.py`, replay evidence | N/A | source company id now wins before cache/provider fallback |
| AA-004 | conditional plan-code enrichment from customer contract history | mechanism | annual award capability map | `capabilities/fact_processing/annual_award/plan_code_lookup.py` | `capabilities` | annual award slice plan | `accepted` | `tests/integration/test_annual_award_plan_code_enrichment.py`, replay evidence | N/A | replay fixture keeps lookup behavior explicit before production storage exists |
| AA-005 | customer-master backfill signals from award events | mechanism | annual award capability map and legacy backfill behavior | explicit derivation/publication path | `capabilities` + `platform` | annual award slice plan | `accepted` | `tests/integration/test_reference_derivation.py`, `tests/integration/test_publication_service.py` | N/A | hidden side effects remain out of the hot path |
| AA-006 | award fact publication used by downstream status logic | projection | annual award capability map, downstream snapshot dependency | explicit publication and replay fixture coverage | `platform` + `reference` | annual award slice plan | `accepted` | `tests/integration/test_projection_outputs.py`, `tests/replay/test_annual_award_slice.py`, `tests/replay/test_annual_award_explainability_slo.py` | N/A | projection keeps compatibility field shape while reading published award facts |

### 6.3 `annual_loss`

| Row ID | Behavior / Asset | Category | Legacy Source | Rebuild Target | Target Boundary | Owning Spec / Plan | Status | Validation Evidence | Retirement Decision | Notes / Risks |
|------|-------------------|----------|---------------|----------------|-----------------|--------------------|--------|---------------------|--------------------|---------------|
| AL-001 | multi-sheet loss-domain intake contract | capability | legacy migration workflow and paired event-domain references | `capabilities/source_intake/annual_loss/service.py` | `capabilities` | architecture blueprint + annual loss slice plan | `accepted` | `tests/integration/test_annual_loss_intake.py`, `tests/replay/test_annual_loss_slice.py` | N/A | merged anchors stay queryable by batch + anchor row |
| AL-002 | canonical loss event transformation | capability | legacy domain behavior and capability-map-equivalent references | `capabilities/fact_processing/annual_loss/` | `capabilities` | architecture blueprint + annual loss slice plan | `accepted` | `tests/integration/test_annual_loss_processing.py`, `tests/replay/test_annual_loss_slice.py` | N/A | governed rule-pack binding and date parsing are explicit |
| AL-003 | identity / plan-code handling for loss rows | mechanism | legacy event-domain behavior | shared identity contract plus loss-specific current-contract lookup | `capabilities` | annual loss slice plan | `accepted` | `tests/integration/test_identity_resolution.py`, `tests/integration/test_annual_loss_plan_code_enrichment.py`, replay evidence | N/A | source company id now wins before cache/provider fallback and current-row lookup keeps `valid_to` filtering explicit |
| AL-004 | loss fact publication consumed by downstream status rules | projection | downstream snapshot dependency implied by current fixtures and blueprint | explicit publication plus projection evidence | `platform` + `capabilities` | annual loss slice plan | `accepted` | `tests/integration/test_projection_outputs.py`, `tests/replay/test_annual_loss_slice.py`, `tests/replay/test_annual_loss_explainability_slo.py` | N/A | the slice replaces fixture-only loss dependency with published fact coverage |

### 6.4 `annuity_income`

| Row ID | Behavior / Asset | Category | Legacy Source | Rebuild Target | Target Boundary | Owning Spec / Plan | Status | Validation Evidence | Retirement Decision | Notes / Risks |
|------|-------------------|----------|---------------|----------------|-----------------|--------------------|--------|---------------------|--------------------|---------------|
| AI-001 | single-sheet workbook intake | capability | legacy domain migration workflow and current blueprint archetype mapping | future `capabilities/source_intake/annuity_income/` | `capabilities` | future annuity income slice plan | `pending` | future intake tests and replay evidence | N/A | lower architectural novelty than event domains |
| AI-002 | canonical cleansing and fact processing | capability | legacy domain workflow and cleansing-rule references | future `capabilities/fact_processing/annuity_income/` plus domain config | `capabilities` + `config` | future annuity income slice plan | `pending` | future processing tests and replay evidence | N/A | should follow governed rule-pack pattern already proven |
| AI-003 | identity/reference/publication path | mechanism | legacy enrichment/backfill/load expectations | shared contracts plus annuity-income-specific derivation/publication | `capabilities` + `platform` | future annuity income slice plan | `pending` | future identity/derivation/publication tests | N/A | reuse explicit publication boundary, not old hook-centric patterns |
| AI-004 | unresolved-name and failed-record operator artifacts | operator | `docs/domains/annuity_income-capability-map.md`, legacy service export behavior | future annuity-income operator artifact flow and runbook coverage | `capabilities` + `apps` + `docs` | merged first-wave legacy coverage risk register + future annuity income slice plan | `pending` | future artifact tests, replay/slice evidence, and runbook coverage | N/A | legacy income execution returns operator-facing diagnostics such as `unknown_names_csv`; this contract is not yet registered in `WorkDataHubPro` |
| AI-005 | service-delegation execution path and explicit no-hook contract | mechanism | `docs/domains/annuity_income-capability-map.md`, legacy service path and hook-registry absence | future annuity-income slice wiring plus no-hook guard coverage | `capabilities` + `apps` | merged first-wave legacy coverage risk register + future annuity income slice plan | `pending` | future slice tests plus explicit no-hook integration evidence | N/A | legacy `annuity_income` behavior includes runtime-shape constraints, not only fact transformation |

### 6.5 Cross-Cutting First-Wave Assets

| Row ID | Behavior / Asset | Category | Legacy Source | Rebuild Target | Target Boundary | Owning Spec / Plan | Status | Validation Evidence | Retirement Decision | Notes / Risks |
|------|-------------------|----------|---------------|----------------|-----------------|--------------------|--------|---------------------|--------------------|---------------|
| CT-001 | directory-based file discovery and workbook version arbitration for operator runs | operator | first-wave domain capability maps and legacy discovery/read paths | follow-on operator discovery/runtime path beyond replay CLI | `apps` + `capabilities` | merged first-wave legacy coverage risk register + follow-on operator tooling/runtime plan | `deferred` | future discovery integration tests, operator commands, and runbook evidence | N/A | current validation runtime intentionally takes explicit workbook paths; revisit during Phase E operator/runtime closure |
| CT-002 | reference/master semantic parity beyond current derivation stubs | mechanism | `docs/domains/annuity_performance-capability-map.md`, `docs/domains/annual_award-capability-map.md`, `docs/domains/annual_loss-capability-map.md`, `docs/domains/annuity_income-capability-map.md` | future expansion of `capabilities/reference_derivation/` and explicit publication targets | `capabilities` + `platform` | merged first-wave legacy coverage risk register + future derivation parity follow-on plan | `pending` | future derivation/publication tests and replay evidence for customer/reference outputs | N/A | accepted slices prove derivation plumbing, but not the full legacy breadth of tags, weighted customer selection, or multi-table master/reference outputs |
| CT-003 | publication key/delete-scope and sink write-contract parity across first-wave fact targets | mechanism | first-wave capability maps and legacy load semantics | follow-on production publication/storage design with table-specific contracts | `platform` + `config` | merged first-wave legacy coverage risk register + follow-on production storage/publication plan | `planned` | future publication contract tests, replay evidence, and storage adapter validation | N/A | validation runtime proves visible publication groups, not legacy table-specific delete scopes or sink schema contracts |
| CT-004 | projection semantic-width parity for customer contract and monthly snapshot outputs | projection | `docs/domains/annuity_performance-capability-map.md`, `docs/domains/annual_loss-capability-map.md`, legacy customer status references | future projection parity work after first-wave breadth closure | `capabilities` + `platform` | merged first-wave legacy coverage risk register + future projection parity follow-on plan | `pending` | future projection contract tests plus replay/golden evidence for customer MDM output shape | N/A | current projections are validation bridges and counters, not the full legacy customer contract/snapshot output surface |
| CT-005 | history-aware event-domain contract lookup and temporal enrichment semantics | mechanism | `docs/domains/annual_award-capability-map.md`, `docs/domains/annual_loss-capability-map.md`, legacy contract lookup behavior | future temporal lookup contract for event-domain plan-code enrichment | `capabilities` + `reference` | merged first-wave legacy coverage risk register + future annual loss / event-domain parity follow-on plan | `pending` | future lookup contract tests, historical replay evidence, and event-domain slice validation | N/A | current accepted event-domain slice proves replay-backed lookup, not a full repository-wide temporal selection contract for historical/current contract rows |
| CT-006 | legacy identity-source lineage, override mapping, and post-load `company_id` backfill parity | mechanism | `docs/domains/annuity_performance-capability-map.md`, legacy mapping/sync/update behavior, identity-related follow-on sources | future identity parity work beyond cache-first validation resolver | `capabilities` + `reference` + `platform` | merged first-wave legacy coverage risk register + future identity parity follow-on plan | `pending` | future identity parity tests, replay evidence, and explicit adjudication for retained or retired legacy sources | N/A | accepted identity resolution proves the validation chain, not full parity for override catalogs, former-name lineage, or downstream repair/update paths |
| CT-007 | pre-load reference bootstrap and missing-code creation semantics outside the explicit publication chain | mechanism | legacy pre-ETL bootstrap behavior for first-wave reference creation | future explicit pre-publication or bootstrap design | `capabilities` + `platform` | merged first-wave legacy coverage risk register + future derivation/publication follow-on plan | `pending` | future bootstrap tests, replay evidence, and explicit migrate-or-retire decision | N/A | legacy behavior may require reference objects before the main ETL publication chain runs; current validation slices do not yet prove parity here |
| CT-008 | governed string normalization and plan-code correction parity across first-wave domains | config | first-wave domain capability maps and legacy cleansing/correction behavior | future rule-pack expansion and compatibility adjudication for retained normalization semantics | `capabilities` + `config` | merged first-wave legacy coverage risk register + future cleansing parity follow-on plan | `pending` | future cleansing tests, replay/golden evidence, and explicit adjudication for retained or retired legacy rules | N/A | current governed cleansing baseline is narrower than legacy string-cleanup and plan-code correction behavior |
| CT-009 | annual lifecycle and January-only status initialization semantics | projection | legacy hook-chain yearly initialization behavior | future annual lifecycle projection/runtime design | `capabilities` + `apps` | merged first-wave legacy coverage risk register + future projection/runtime follow-on plan | `pending` | future lifecycle tests, replay evidence, and explicit retention-or-retirement decision | N/A | January-only yearly initialization remains outside the currently accepted validation projection bridge |
| CT-010 | multi-slice projection execution ordering and dependency closure | projection | first-wave domain capability maps, legacy hook-chain ordering, and downstream status dependencies | future multi-slice orchestration/runtime closure | `apps` + `capabilities` + `platform` | merged first-wave legacy coverage risk register + future multi-slice dependency closure plan | `pending` | future multi-slice replay evidence and ordering contract tests | N/A | current accepted slices prove fixture-backed dependencies, not fully closed multi-slice execution ordering |

## 7. Cross-Domain Dependencies

| Row ID | Dependency | Why It Matters | Governing Status | Notes |
|------|------------|----------------|------------------|-------|
| XD-001 | `annual_award` facts influence downstream snapshot status triggered by `annuity_performance` | first-wave slices are not fully independent at projection level | active dependency | already represented as fixture dependency in the accepted first slice |
| XD-002 | `annual_loss` facts influence downstream snapshot status triggered by `annuity_performance` | event-domain closure matters for customer status correctness | active dependency | closed by the accepted `annual_loss` slice with published-fact projection coverage |
| XD-003 | shared identity/provider integration affects all first-wave domains | domain rollout may outrun runtime/provider readiness | deferred cross-cutting track | governed by refactor program, not a single domain slice |
| XD-004 | production publication/storage decisions affect all first-wave domains | validation runtime is not the final production runtime | deferred cross-cutting track | governed by follow-on production storage/publication plan |

## 8. Update Rules

Update this matrix when:

- a new slice spec or plan is created
- a row changes status
- validation evidence changes materially
- a compatibility case alters the acceptance story for a row
- a legacy behavior is retired or reclassified as deferred

This matrix is a governance asset. It is not optional documentation.

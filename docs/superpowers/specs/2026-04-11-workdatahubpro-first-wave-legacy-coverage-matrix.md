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
| `annual_award` | accepted multi-sheet slice | `annual_loss` and `annuity_income` remain unclosed first-wave breadth work |
| `annual_loss` | next recommended event-domain slice | no accepted executable slice yet |
| `annuity_income` | identified first-wave single-sheet domain | no accepted executable slice yet |

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
| AL-001 | multi-sheet loss-domain intake contract | capability | legacy migration workflow and paired event-domain references | future `capabilities/source_intake/annual_loss/` | `capabilities` | follow-on multi-sheet validation plan after annual_award | `pending` | future intake tests and replay evidence | N/A | should reuse archetype lessons from accepted award slice |
| AL-002 | canonical loss event transformation | capability | legacy domain behavior and capability-map-equivalent references | future `capabilities/fact_processing/annual_loss/` | `capabilities` | future annual loss slice plan | `pending` | future transform tests and replay evidence | N/A | not yet designed in detail |
| AL-003 | identity / plan-code handling for loss rows | mechanism | legacy event-domain behavior | shared contracts plus domain-specific wiring | `capabilities` | future annual loss slice plan | `pending` | future replay evidence | N/A | exact priority chain to be documented before implementation |
| AL-004 | loss fact publication consumed by downstream status rules | projection | downstream snapshot dependency implied by current fixtures and blueprint | explicit publication plus projection evidence | `platform` + `capabilities` | future annual loss slice plan | `pending` | future replay and projection evidence | N/A | currently represented only as fixture dependency |

### 6.4 `annuity_income`

| Row ID | Behavior / Asset | Category | Legacy Source | Rebuild Target | Target Boundary | Owning Spec / Plan | Status | Validation Evidence | Retirement Decision | Notes / Risks |
|------|-------------------|----------|---------------|----------------|-----------------|--------------------|--------|---------------------|--------------------|---------------|
| AI-001 | single-sheet workbook intake | capability | legacy domain migration workflow and current blueprint archetype mapping | future `capabilities/source_intake/annuity_income/` | `capabilities` | future annuity income slice plan | `pending` | future intake tests and replay evidence | N/A | lower architectural novelty than event domains |
| AI-002 | canonical cleansing and fact processing | capability | legacy domain workflow and cleansing-rule references | future `capabilities/fact_processing/annuity_income/` plus domain config | `capabilities` + `config` | future annuity income slice plan | `pending` | future processing tests and replay evidence | N/A | should follow governed rule-pack pattern already proven |
| AI-003 | identity/reference/publication path | mechanism | legacy enrichment/backfill/load expectations | shared contracts plus annuity-income-specific derivation/publication | `capabilities` + `platform` | future annuity income slice plan | `pending` | future identity/derivation/publication tests | N/A | reuse explicit publication boundary, not old hook-centric patterns |

## 7. Cross-Domain Dependencies

| Row ID | Dependency | Why It Matters | Governing Status | Notes |
|------|------------|----------------|------------------|-------|
| XD-001 | `annual_award` facts influence downstream snapshot status triggered by `annuity_performance` | first-wave slices are not fully independent at projection level | active dependency | already represented as fixture dependency in the accepted first slice |
| XD-002 | `annual_loss` facts influence downstream snapshot status triggered by `annuity_performance` | event-domain closure matters for customer status correctness | active dependency | still fixture-only in current accepted slice |
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

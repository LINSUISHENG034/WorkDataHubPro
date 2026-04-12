# WorkDataHubPro Refactor Program

Date: 2026-04-11
Status: Active Governance Baseline
Target Workspace: `E:\Projects\WorkDataHubPro`
Legacy Reference Workspace: `E:\Projects\WorkDataHub`

## 1. Purpose And Scope

This document governs the first-wave refactor program from `WorkDataHub` to
`WorkDataHubPro`.

It is not:

- a single-slice implementation plan
- a narrative architecture draft
- a replacement for the coverage matrix

It defines how first-wave refactor work is allowed to advance, what counts as
coverage, what blocks new slice work, and what must be true before the program
may claim first-wave completion.

### 1.1 In Scope

This program baseline covers the first-wave domains only:

- `annuity_performance`
- `annual_award`
- `annual_loss`
- `annuity_income`

It also governs the cross-cutting tracks required to make those domains
operationally credible in `WorkDataHubPro`:

- publication/runtime storage decisions
- compatibility and evidence handling
- operator entrypoints and replay tooling
- external identity/provider integration strategy
- deferred lookup queue and special orchestration runtime surfaces
- reference bootstrap / reference-sync runtime decisions
- enterprise persistence surfaces used by identity and EQC integration
- cross-domain operator artifacts and manual customer-status command surfaces

### 1.2 Out Of Scope

This document does not define:

- the detailed steps of a single slice implementation
- the final full-program rollout for all legacy domains
- production infrastructure decisions beyond the gates needed to schedule follow-on plans

## 2. Governing Inputs

This program is constrained by:

- `docs/superpowers/specs/2026-04-11-workdatahubpro-rebuild-architecture-draft.md`
- `docs/superpowers/specs/2026-04-11-workdatahubpro-first-wave-legacy-coverage-matrix.md`
- `docs/disciplines/git-workflow.md`
- `docs/disciplines/implementation-execution.md`
- `docs/disciplines/implementation-slice-workflow.md`

Legacy behavior references for first-wave domains include:

- `E:\Projects\WorkDataHub\docs\guides\domain-migration\workflow.md`
- `E:\Projects\WorkDataHub\docs\domains\annuity_performance-capability-map.md`
- `E:\Projects\WorkDataHub\docs\domains\annual_award-capability-map.md`

## 3. Current Position

The program has completed:

- the first executable validation slice for `annuity_performance`
- the default Phase C multi-sheet slice for `annual_award`
- the first Phase D breadth slice for `annual_loss`

What is already true:

- a capability-first package exists under `src/work_data_hub_pro/`
- explicit platform contracts, tracing, lineage, publication, and replay flow exist
- compatibility adjudication and evidence indexing exist for the first three accepted slices
- replay assets and runbooks exist for `annuity_performance`, `annual_award`, and `annual_loss`
- the paired event-domain dependency path is accepted with committed coverage updates

What is not yet true:

- `annuity_income` does not have an accepted executable slice yet
- production storage/publication and operator tooling remain deferred
- special orchestration surfaces such as `company_lookup_queue` and `reference_sync` are now explicitly registered, but not yet closed
- enterprise persistence surfaces and manual `customer-mdm` operator paths are now explicitly registered, but not yet closed
- first-wave legacy retirement decisions are not yet recorded

## 4. Success Definition

The first-wave refactor is only successful when every first-wave legacy behavior
and operational asset is in one of these states:

- `accepted`: rebuilt in `WorkDataHubPro` with committed validation evidence
- `deferred`: explicitly postponed with an owner reason and trigger to revisit
- `retired`: explicitly declared unnecessary or replaced, with rationale

The program is not successful if any first-wave legacy behavior remains in an
implicit state such as:

- unknown
- assumed handled
- probably covered
- to be checked later

## 5. Hard Rules

- No new executable slice may start unless its target legacy behavior is already registered in the first-wave coverage matrix.
- No implementation may start without an approved governing spec and an executable implementation plan.
- No legacy behavior may be considered covered without a defined validation evidence path.
- Cross-boundary implementation must proceed as an explicit slice, not as a quiet accumulation of unrelated boundary changes.
- Semantic config changes must be paired with rule/version governance, replay evidence, and compatibility handling.
- A legacy behavior may only move to `retired` if the replacement path or removal rationale is written down explicitly.

## 6. Program Phases

### 6.1 Phase A: Governance Baseline

Purpose:

- establish program governance before broad rollout

Required outputs:

- active architecture blueprint
- refactor program spec
- first-wave legacy coverage matrix
- discipline router and implementation discipline docs

Exit gate:

- all first-wave work can be evaluated against a committed governance baseline

### 6.2 Phase B: First Executable Slice Baseline

Purpose:

- prove the corrected architecture works end to end in code

Current status:

- complete via `annuity_performance`

Required outputs:

- closed executable slice
- replay evidence
- compatibility adjudication path
- operator runbook

Exit gate:

- first slice accepted with executable validation and explainability evidence

### 6.3 Phase C: Multi-Sheet Archetype Closure

Purpose:

- validate the second intake archetype before broad first-wave rollout

Default next domain:

- `annual_award`

Why `annual_award` first:

- it validates multi-sheet merged intake
- it exercises optional `company_id` resolution and conditional plan-code enrichment
- its outputs already affect downstream status behavior consumed by the current first slice

Exit gate:

- one multi-sheet slice is accepted with replay evidence and committed coverage updates

### 6.4 Phase D: First-Wave Breadth Closure

Purpose:

- extend accepted coverage across the remaining first-wave domains

Targets after multi-sheet closure:

- `annual_loss`
- `annuity_income`

Exit gate:

- every first-wave domain coverage row in Sections 6.1 through 6.4 of the first-wave coverage matrix is `accepted`, `deferred`, or `retired`

### 6.5 Phase E: Production Runtime And Operator Closure

Purpose:

- replace validation-only runtime choices where first-wave rollout requires it

Cross-cutting areas:

- production storage and deferred publication design
- physical location for compatibility/evidence storage
- operator tooling, Dagster wiring, and manual command-surface decisions
- live identity/provider integration strategy
- deferred lookup queue runtime and retry orchestration
- reference bootstrap / reference-sync runtime design
- enterprise identity/EQC persistence-surface retention or retirement decisions
- shared operator artifact retention or retirement decisions

Exit gate:

- first-wave operational paths are no longer blocked by unresolved runtime decisions

### 6.6 Phase F: Legacy Retirement Review

Purpose:

- decide what may be retired, what remains deferred, and what must still be rebuilt

Exit gate:

- first-wave retirement decisions are explicit and queryable

## 7. Domain Sequencing

| Order | Domain | Program Status | Rationale |
|------|--------|----------------|-----------|
| 1 | `annuity_performance` | accepted baseline slice | proves the corrected architecture in code |
| 2 | `annual_award` | accepted multi-sheet slice | closes the second intake archetype and downstream award-status dependency |
| 3 | `annual_loss` | accepted breadth-closure slice | closes the paired event-domain dependency path before the final single-sheet breadth slice |
| 4 | `annuity_income` | next recommended single-sheet breadth slice | extends first-wave coverage after event-domain breadth risk is reduced |

Historical pre-closure sequence reference:
| 3 | `annual_loss` | next recommended slice | validates the paired event-domain dependency path |

This order may only change if the program governance review writes down:

- why the new order reduces risk
- which blocked matrix rows it clears sooner
- which new risks it introduces

## 8. Slice Admission Rules

Before writing or executing a new slice plan, all of the following must be true:

- the target legacy behavior exists in the first-wave coverage matrix
- the source legacy code/docs/config references are known
- the target boundary in `WorkDataHubPro` is known
- the expected validation evidence type is known
- replay/golden/fixture strategy is known when legacy parity matters
- cross-domain dependencies are known if the slice affects projections, operator flow, or compatibility posture

If any of the above is unknown, the work is not ready for implementation. It is
still in governance or design discovery.

## 9. Slice Exit Rules

A slice may only move to `accepted` when all of the following are true:

- the target chain closes without hidden hook-only business logic
- runtime evidence is queryable for the behavior the slice claims to cover
- the validation command and result are committed or explicitly recorded
- runbooks and replay assets are updated when the slice depends on them
- the coverage matrix row(s) are updated with current status and evidence
- any legacy difference is adjudicated or explicitly marked as deferred

## 10. Cross-Cutting Tracks

These tracks are governed separately from domain slices, but they are mandatory
program concerns:

Current status values for these tracks should reuse the active governance
vocabulary where it fits:

- `planned`: the decision or follow-on design is admitted but not yet executed
- `deferred`: the work is intentionally postponed behind current validation priorities

| Track | Why It Matters | Current Status | Follow-On Need |
|------|----------------|----------------|----------------|
| production storage and publication runtime | current slice uses in-memory and file-backed validation adapters | deferred | separate production storage/publication plan |
| external identity/provider integration | first slice runs cache-first with provider-disabled behavior | deferred | separate provider-integration plan |
| deferred lookup queue runtime | legacy supports queued provider processing, retries, and recovery outside the main fact run | deferred | separate queue/runtime plan |
| reference bootstrap / reference-sync runtime | legacy uses an explicit `reference_sync` orchestration surface plus incremental state | deferred | separate reference bootstrap/runtime plan |
| enterprise identity / EQC persistence surfaces | legacy persists cache, queue, and raw/cleansed EQC data beyond fact-domain outputs | deferred | separate identity persistence plan |
| manual customer-status command surfaces and shared operator artifacts | legacy supports `customer-mdm` manual commands and cross-domain unresolved-name / failed-record artifacts | deferred | separate operator-tools / artifact-governance plan |
| evidence and compatibility storage location | current artifacts are repository/file-backed in validation mode | planned | physical storage decision |
| operator tooling and Dagster | replay CLI exists; broader operator flow does not | deferred | separate operator-tools and Dagster plan |

## 11. Legacy Retirement Model

Every first-wave matrix row must end in one of these states:

- `accepted`
- `deferred`
- `retired`

Retirement requires:

- a written rationale
- a replacement path or explicit removal decision
- identified risk ownership

Deferred requires:

- why the work is deferred
- what blocks acceptance now
- what future plan or trigger should reactivate it

## 12. Governance Loop

The program must be updated at these moments:

- when a new slice is admitted
- when a slice becomes accepted
- when a compatibility decision changes precedent
- when a legacy behavior is moved to `retired`
- when cross-cutting runtime decisions move from `planned` or `deferred` to committed

At minimum, these assets must be updated when relevant:

- this refactor program spec
- the first-wave coverage matrix
- the active slice plan
- replay assets and runbooks
- compatibility cases / adjudication evidence

## 13. Current Decision Backlog

The following decisions still block broad first-wave rollout:

1. physical storage location for `CompatibilityCase` and evidence index
2. whether publication remains fully synchronous or gains deferred execution groups
3. exact production design for external identity/provider integration
4. whether queued provider processing via `company_lookup_queue` is retained, replaced, or retired for first-wave production closure
5. whether `reference_sync` remains a retained runtime surface or is replaced by an explicit bootstrap/publication flow
6. which enterprise persistence surfaces remain in scope for retained runtime behavior: queue/cache only, raw EQC persistence, cleansed EQC persistence, or none
7. which manual `customer-mdm` commands remain supported in the rebuild and in what form
8. whether unresolved-name and failed-record artifacts remain mandatory operator outputs across first-wave runs
9. operator-tooling and Dagster rollout order after replay-only validation

## 14. Final Program Position

`WorkDataHubPro` should not expand through opportunistic domain-by-domain
coding. It should expand through governed slice admission, explicit legacy
coverage tracking, and explicit retirement or deferral of every first-wave
legacy behavior.

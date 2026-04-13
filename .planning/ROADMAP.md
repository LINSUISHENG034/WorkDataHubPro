# Roadmap: WorkDataHubPro

**Generated:** 2026-04-12
**Mode:** Brownfield rebuild / reconstruction
**Core acceptance axis:** Legacy-result parity + explicit, agent-operable architecture

## Phase Overview

| # | Phase | Goal | Requirements | Success Criteria |
|---|-------|------|--------------|------------------|
| 1 | Legacy Capability Mapping & Parity Harness | Build authoritative mapping between legacy and pro capabilities, and establish parity baseline verification assets | MAP-01, MAP-02, MAP-03, PAR-01 | 5 |
| 2 | Transparent Pipeline Contracts & Parity Gates | Define non-black-box stage contracts and enforce deterministic parity adjudication in replay verification | PAR-02, PAR-03, PAR-04, PIPE-01, PIPE-02 | 5 |
| 3 | Orchestration Refactor & Failure Explainability | Remove replay orchestration duplication and standardize typed diagnostics/failure paths | PIPE-03, PIPE-04, OPS-01, GOV-02 | 5 |
| 4 | Agent Operations & Governance Hardening | Deliver agent-runbook-ready operations model with lineage, observability, and evidence governance | OPS-02, OPS-03, OPS-04, GOV-01, GOV-03 | 5 |
| 5 | Performance Reliability Optimization with Drift Safeguards | Improve bottlenecks and policy safety while preserving parity behavior | PERF-01, PERF-02, PERF-03 | 5 |

## Phase Details

### Phase 1: Legacy Capability Mapping & Parity Harness

**Goal**
Create a verifiable source of truth describing what legacy does, what Pro currently does, and what parity must be proven first.

**Scope**
- Map legacy capability surfaces to Pro module boundaries and status
- Build source-recognition mapping for critical data intake paths
- Define parity datasets, expected outputs, and comparison rules
- Define mismatch severity matrix and escalation path
- Establish first “must-pass” parity checkpoint for scoped domains

**Requirements**
- MAP-01, MAP-02, MAP-03, PAR-01

**High-Risk Focus**
- Data source recognition drift
- Incomplete legacy rule migration inventory
- Hidden intermediate transformation mismatch

**Dependencies**
- Access to legacy project `E:\Projects\WorkDataHub` and representative input/output samples
- Stable replay fixtures and baseline assets under `reference/historical_replays/`
- Agreed mismatch severity taxonomy and adjudication owner
- Availability of current Pro codebase map artifacts for capability ownership mapping

**Success Criteria**
1. Capability map artifact exists and links each parity-critical legacy behavior to Pro ownership and migration status.
2. Intake/source-recognition mapping covers all scoped replay sources and identifies unresolved ambiguities.
3. Parity dataset and golden output set are reproducible and versioned for replay use.
4. Mismatch severity taxonomy is documented and operationally usable.
5. Phase report identifies top migration risks with explicit next-phase mitigation ownership.

**UI hint**: no

---

### Phase 2: Transparent Pipeline Contracts & Parity Gates

**Goal**
Turn replay flow into explicit stage contracts with deterministic parity and adjudication gates.

**Scope**
- Define stage boundary contracts for input, transformations, intermediates, and outputs
- Attach rule/rationale evidence contract to each major stage
- Implement deterministic compare+adjudication gate for replay outputs
- Add CI/pass criteria hooks for parity-critical requirements

**Requirements**
- PAR-02, PAR-03, PAR-04, PIPE-01, PIPE-02

**High-Risk Focus**
- False positive/negative parity comparisons
- Ambiguous acceptable-difference policy
- Stage contract overfitting that blocks evolvability

**Success Criteria**
1. Replay stage contracts are explicit and machine-checkable.
2. Rule decision evidence is queryable at stage granularity.
3. Parity comparator emits deterministic structured results.
4. Adjudication policy distinguishes acceptable and blocking differences.
5. CI gate fails reliably when parity-critical checks regress.

**UI hint**: no

---

### Phase 3: Orchestration Refactor & Failure Explainability

**Goal**
Refactor duplicated orchestration into reusable pipeline composition while making failures diagnosable by developers and agents.

**Scope**
- Extract shared orchestration template/primitives from domain slice runners
- Standardize typed error categories and failure-path reporting
- Upgrade operational entrypoint conventions for agent execution and diagnostics
- Fix identified fragile fallback identity behaviors

**Requirements**
- PIPE-03, PIPE-04, OPS-01, GOV-02

**High-Risk Focus**
- Refactor-induced behavior drift across domains
- Error taxonomy inconsistency
- Hidden coupling between orchestration and domain specifics

**Success Criteria**
1. Shared orchestration primitives are adopted by all scoped replay slices.
2. Domain-specific behavior remains parity-stable after refactor.
3. Failure diagnostics return actionable typed categories and context.
4. Agent can trigger replay and diagnostics through stable documented entrypoints.
5. Temporary identity fallback no longer leaks raw business identifiers.

**UI hint**: no

---

### Phase 4: Agent Operations & Governance Hardening

**Goal**
Make system operationally handoff-ready for agent-driven maintenance and governed evidence handling.

**Scope**
- Define runbook + configuration contract for adding sources and flows
- Strengthen lineage queryability from output back to source/stage
- Harden evidence redaction and governance metadata conventions
- Formalize compatibility adjudication lifecycle and closure evidence

**Requirements**
- OPS-02, OPS-03, OPS-04, GOV-01, GOV-03

**High-Risk Focus**
- Insufficient evidence redaction in persisted artifacts
- Incomplete lineage links under failure conditions
- Operational runbooks diverging from real execution

**Success Criteria**
1. Agent can complete a documented “add source / adjust rule / run verify” workflow end-to-end.
2. Output-to-source lineage lookup is reliable and test-covered.
3. Evidence artifacts enforce redaction policy for sensitive fields.
4. Adjudication records include severity, decision owner, and closure proof.
5. Incident diagnostics flow is documented and executable by non-authors.

**UI hint**: no

---

### Phase 5: Performance Reliability Optimization with Drift Safeguards

**Goal**
Address confirmed performance and reliability bottlenecks without semantic regression.

**Scope**
- Optimize projection and trace-query hotspots identified in concerns map
- Add defensive policy validation and fail-safe publication behavior
- Add verification matrix for perf gains vs parity stability

**Requirements**
- PERF-01, PERF-02, PERF-03

**High-Risk Focus**
- Performance optimization causing subtle behavioral drift
- Partial-write and config-failure paths lacking robust handling
- Benchmarking without representative workload

**Success Criteria**
1. Performance hotspots show measurable improvement with reproducible benchmark evidence.
2. Policy/config errors return typed, actionable failures.
3. Full verification matrix runs at required checkpoints.
4. No parity-critical regression introduced by optimization changes.
5. Rollback strategy exists for each high-impact optimization.

**UI hint**: no

## Suggested First Execution Phase

**Recommended start:** Phase 1 - Legacy Capability Mapping & Parity Harness

**Why first**
- It creates the acceptance and risk baseline that every subsequent architecture change depends on.
- It prevents “refactor by assumption” and reduces parity break risk.
- It makes high-risk zones visible before implementation pressure increases.

## Validation Model

Each phase completion requires:
1. Requirement-level verification evidence
2. Parity checkpoint outcome and adjudication status
3. High-risk checklist closure or explicit carry-over
4. Regression test evidence for touched boundaries

### Phase 6: Phase 2 governance remediation - truthful gates and status sync

**Goal:** Restore truthful Phase 2 intermediate gates and synchronize governance status with the actual remediation state.
**Requirements**: PAR-02, PAR-03, PIPE-01, PIPE-02
**Depends on:** Phase 5
**Status:** Complete (verified 2026-04-13)
**Plans:** 3 plans

Plans:
- [x] 06-01 - shared fail-closed baseline runtime, explicit bootstrap path, and duplicate-row diff fix
- [x] 06-02 - truthful intermediate checkpoint wiring and accepted replay baseline assets for all accepted slices
- [x] 06-03 - governance and planning status synchronization plus contract coverage

---
*Roadmap created: 2026-04-12*
*Last updated: 2026-04-13 after Phase 03.1 closure*

### Phase 03.1: Phase 3 governance remediation - truthful failure evidence and diagnose hardening

**Goal:** Remove stale Phase 3 closure wording and ensure repository-facing status docs reflect executed remediation evidence before treating Phase 3 governance sign-off as closed.
**Requirements**: PAR-02, PIPE-03, OPS-01
**Depends on:** 03.1-01, 03.1-02
**Status:** Gap closure in progress (verified 2026-04-13)
**Plans:** 5/5 plans complete

Plans:
- [x] 03.1-01 - truthful failed-checkpoint compatibility-case payload selection across all replay slices
- [x] 03.1-02 - fail-closed diagnose package-path enforcement and typed invalid-id CLI handling
- [x] 03.1-03 - governance and planning artifact synchronization plus Phase 3 governance-status contract coverage
- [x] 03.1-05 - use outcome.intermediate_payloads for compatibility-case legacy_payloads (gap-closure)

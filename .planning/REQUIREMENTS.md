# Requirements: WorkDataHubPro

**Defined:** 2026-04-12
**Core Value:** 在不牺牲旧项目业务结果一致性的前提下，把数据处理流程重构为可解释、可验证、可维护、可由 agent 接管的系统。

## v1 Requirements

### Legacy Capability Mapping

- [x] **MAP-01**: Team can produce a capability inventory that maps each legacy `E:\Projects\WorkDataHub` business processing capability to WorkDataHubPro target modules and status (existing/missing/partial)
- [x] **MAP-02**: Team can map each critical legacy data source recognition path to explicit Pro intake contracts and validation checks
- [x] **MAP-03**: Team can identify and classify parity-critical legacy rules as must-keep / replace-with-equivalent / retire-with-proof

### Result Parity Validation

- [x] **PAR-01**: Team can define domain-specific parity datasets and golden outputs for annuity performance, annual award, and annual loss
- [x] **PAR-02**: Replay verification can compare Pro outputs against legacy baselines with deterministic pass/fail evidence
- [x] **PAR-03**: Team can distinguish acceptable structural differences from unacceptable business-semantic mismatches using explicit adjudication rules
- [x] **PAR-04**: CI can block phase completion when parity-critical checks fail

### Non-Black-Box Processing Architecture

- [x] **PIPE-01**: System can express processing lifecycle as explicit stage contracts (input -> stage transform -> intermediate product -> output)
- [x] **PIPE-02**: System can expose per-stage rule application evidence and decision rationale for debugging
- [x] **PIPE-03**: System can surface failure paths with typed error categories and actionable diagnostics
- [x] **PIPE-04**: System can reduce duplicated replay orchestration by extracting reusable pipeline composition primitives

### Agent-Friendly Operability

- [x] **OPS-01**: Agent can discover stable task entrypoints for replay execution, diagnostics, and rule updates without relying on hidden context
- [x] **OPS-02**: Agent can use standardized runbook + config contracts to add a new data source with bounded change surface
- [x] **OPS-03**: Agent can trace a produced output row back to its source and stage decisions through queryable lineage/evidence references
- [x] **OPS-04**: Project can provide explicit observability contracts (logs/traces/evidence structure) that support operations and incident response

### Performance and Reliability

- [ ] **PERF-01**: System can improve projection and trace-query hotspots identified in `.planning/codebase/CONCERNS.md` without parity drift
- [ ] **PERF-02**: Publication policy handling can fail safely with typed validation errors instead of unstructured key errors
- [ ] **PERF-03**: System can enforce workload-scaled verification (contract/integration/replay/performance) before phase completion

### Governance and Security

- [x] **GOV-01**: Evidence artifacts can apply redaction policy for sensitive fields before persistence
- [x] **GOV-02**: Identity fallback behavior can avoid leaking raw business identifiers in generated temporary IDs
- [x] **GOV-03**: Compatibility adjudication can record mismatch severity, decision owner, and closure evidence for auditability

## v2 Requirements

### Runtime Expansion

- **RUN-01**: Support production-grade persistent storage/tracing adapters beyond in-memory replay mode
- **RUN-02**: Add orchestrated queue/retry runtime for large replay backlogs
- **RUN-03**: Add advanced publication channels and operational policy controls beyond first-wave reconstruction scope

### Experience Expansion

- **UX-01**: Add operator-facing dashboards for replay status, parity trend, and bottleneck diagnostics
- **UX-02**: Add self-service scenario configuration for non-developer analysts

## Out of Scope

| Feature | Reason |
|---------|--------|
| Full functional redesign of legacy business semantics | Rebuild goal is semantic preservation + architecture upgrade, not product reinvention |
| Simultaneous all-domain migration in one phase | Too risky for parity validation and rollback |
| Unverified performance-only optimization | Performance improvements must pass parity gates |
| Ad-hoc undocumented manual operations | Violates agent-friendly operability objective |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| MAP-01 | Phase 1 | Validated |
| MAP-02 | Phase 1 | Validated |
| MAP-03 | Phase 1 | Validated |
| PAR-01 | Phase 1 | Validated |
| PAR-02 | Phase 2 | Validated |
| PAR-03 | Phase 2 | Validated |
| PAR-04 | Phase 2 | Validated |
| PIPE-01 | Phase 2 | Validated |
| PIPE-02 | Phase 2 | Validated |
| PIPE-03 | Phase 3 | Validated |
| PIPE-04 | Phase 3 | Validated |
| OPS-01 | Phase 3 | Validated |
| OPS-02 | Phase 4 | Validated |
| OPS-03 | Phase 4 | Validated |
| OPS-04 | Phase 4 | Validated |
| PERF-01 | Phase 5 | Pending |
| PERF-02 | Phase 5 | Pending |
| PERF-03 | Phase 5 | Pending |
| GOV-01 | Phase 4 | Validated |
| GOV-02 | Phase 3 | Validated |
| GOV-03 | Phase 4 | Validated |

**Coverage:**
- v1 requirements: 21 total
- Mapped to phases: 21
- Unmapped: 0 ✓

## Phase 6 Re-Verification Note

- 2026-04-13: Phase 6 re-verified `PAR-02`, `PAR-03`, `PIPE-01`, and `PIPE-02` with the required replay acceptance suite and governance status-sync contract suite after the completion audit findings were fixed.

---
*Requirements defined: 2026-04-12*
*Last updated: 2026-04-19 after Phase 04 Plan 03 execution*

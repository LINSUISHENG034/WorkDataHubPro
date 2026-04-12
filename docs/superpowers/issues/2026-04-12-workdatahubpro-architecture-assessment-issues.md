# WorkDataHubPro Architecture Assessment Issues

> Review date: 2026-04-12
> Basis: architecture blueprint + refactor program + first-wave coverage matrix + source review + full-suite validation

---

## Main Issues By Priority

---

### P1 - Production Closure Gap

#### 1. Projection Layer Still Depends On Compatibility Bridges Instead Of Fully Closed Runtime Inputs

**Location:**

- `src/work_data_hub_pro/capabilities/projections/contract_state.py`
- `src/work_data_hub_pro/apps/orchestration/replay/annuity_performance_slice.py`
- `docs/superpowers/specs/2026-04-11-workdatahubpro-first-wave-legacy-coverage-matrix.md`

**Issue:** `ContractStateProjection` still reads both published fact tables and fixture-backed compatibility inputs such as `fixture_annual_award` and `fixture_annual_loss`. The replay slice also seeds those fixture tables directly into storage for validation runs.

**Impact:** The architecture has proven that projection boundaries are explicit, but it has not yet proven that cross-slice dependencies are fully closed through the real runtime publication chain. Current projection behavior is still partly a validation bridge.

**Why it matters:** This is acceptable for validation slices, but not for claiming full runtime closure or production replacement of the legacy downstream path.

**Suggested follow-on:** Replace fixture-backed projection dependencies with published-fact dependencies across accepted slices, then add multi-slice ordering and dependency-closure validation.

---

### P1 - Production Runtime Gap

#### 2. Publication, Storage, And Evidence Handling Are Still Validation-Grade Implementations

**Location:**

- `src/work_data_hub_pro/platform/publication/service.py`
- `src/work_data_hub_pro/platform/storage/in_memory_tables.py`
- `src/work_data_hub_pro/governance/evidence_index/file_store.py`
- `docs/superpowers/specs/2026-04-11-workdatahubpro-first-wave-legacy-coverage-matrix.md`

**Issue:** The explicit publication architecture is in place, but the current runtime still uses in-memory storage and file-backed evidence indexing for accepted slices. The coverage matrix also records production storage, sink-contract parity, queue/runtime closure, and evidence-storage decisions as deferred or planned.

**Impact:** The rebuilt architecture is valid for replay-driven adjudication and slice validation, but it is not yet a production-ready replacement for the legacy runtime surface.

**Why it matters:** Without closing physical storage, sink contracts, transaction behavior, and evidence persistence decisions, the architecture remains a verified prototype rather than an operational platform.

**Suggested follow-on:** Admit a dedicated production runtime closure plan covering storage adapters, publication contracts, evidence persistence, and transaction/execution semantics.

---

### P2 - First-Wave Coverage Gap

#### 3. The Architecture Has Not Yet Been Proven Across The Full First-Wave Domain Set

**Location:**

- `docs/superpowers/specs/2026-04-11-workdatahubpro-first-wave-legacy-coverage-matrix.md`
- `docs/superpowers/specs/2026-04-11-workdatahubpro-refactor-program.md`

**Issue:** `annuity_income` remains fully unaccepted. Its intake, processing, publication path, operator artifacts, and explicit no-hook runtime contract are still `pending` in the first-wave coverage matrix.

**Impact:** The architecture has been proven on the first executable slice and on both accepted multi-sheet event domains, but it has not yet demonstrated that the same boundary model cleanly absorbs the last first-wave single-sheet domain with its operator-facing runtime shape.

**Why it matters:** Until `annuity_income` is closed, the project cannot claim first-wave architectural breadth closure.

**Suggested follow-on:** Prioritize the `annuity_income` slice before broader architecture success claims, and include operator artifact and no-hook guard coverage in its acceptance path.

---

### P2 - Operator Surface Gap

#### 4. Major Legacy Operator And Special Runtime Surfaces Are Registered But Still Unclosed

**Location:**

- `docs/superpowers/specs/2026-04-11-workdatahubpro-first-wave-legacy-coverage-matrix.md`
- `docs/superpowers/specs/2026-04-11-workdatahubpro-refactor-program.md`

**Issue:** Several high-value legacy runtime surfaces are now explicitly tracked, but still deferred or pending:

- `company_lookup_queue`
- `reference_sync`
- enterprise identity cache and EQC persistence surfaces
- manual `customer-mdm` command surfaces
- unresolved-name and failed-record operator artifacts

**Impact:** This is a governance strength, because the gaps are visible instead of hidden. But it is also an architectural limitation: the rebuilt system currently centers on the core ETL validation chain, not the full operating model that surrounded the legacy system.

**Why it matters:** A rebuild can appear structurally successful while still omitting the runtime surfaces operators rely on to recover failures, bootstrap references, or execute manual lifecycle flows.

**Suggested follow-on:** Treat operator/runtime closure as a first-class architecture stream, not as residual tooling. Each retained surface should end in one of three states: accepted, deferred with trigger, or retired with rationale.

---

## Assessment Summary

`WorkDataHubPro` has a valid capability-first architecture for rebuild and validation purposes. Its strongest design decisions are the explicit publication layer, explicit projection boundaries, governed compatibility handling, and system-level explainability contracts.

The current limitation is not architectural incoherence. The limitation is closure. The rebuild has proven the corrected model on accepted validation slices, but it has not yet closed the production runtime, full first-wave breadth, or the legacy operator surface area required for complete replacement of `WorkDataHub`.

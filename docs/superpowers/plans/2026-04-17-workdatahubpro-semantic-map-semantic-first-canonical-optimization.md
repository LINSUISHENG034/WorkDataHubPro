# WorkDataHubPro Semantic-First Canonical Optimization Deliberate Consensus Plan

> **Status:** Proposed
>
> **Plan file:** `docs/superpowers/plans/2026-04-17-workdatahubpro-semantic-map-semantic-first-canonical-optimization.md`
>
> **Target branch:** `slice/semantic-map-semantic-first-canonical-pilot`
>
> **Integration baseline:** branch from the current `slice/semantic-map-integration` head (`002f4f7 docs(docs.architecture): close semantic-map first-wave pilot`) and merge back into `slice/semantic-map-integration` after verification. Do not start from `main`.

## 1) Requirements Summary

### Task intent
Optimize the legacy semantic-map model using **Option B: dual-layer architecture**:

- discovery remains **execution-first**
- canonical outputs become **semantic-first**

The optimization must improve alignment with the **real business semantics** of
`E:\Projects\WorkDataHub`, not merely mirror implementation structure. The
semantic map remains an **internal discovery ledger** whose job is to improve
`docs/wiki-bi/` completeness and correctness. `docs/wiki-bi/` remains the only
durable human-facing knowledge layer.

### Chosen design stance
This plan adopts:

1. **execution-first discovery claims**
   - keep execution paths, subsystem clustering, and witness-oriented discovery
   - continue to support parallel source analysis and provenance capture
2. **semantic-first canonical compilation**
   - compile accepted claims into semantic nodes centered on business meaning
   - treat execution/subsystem/object outputs as witness/support layers, not the final semantic target
3. **small semantic pilot slice**
   - validate the optimization on one bounded semantic theme before broad rollout
   - prove that the new model improves business-semantic alignment without turning the semantic map into a second durable wiki

### Grounded facts from current repository state
- The current semantic-map toolchain under `scripts/legacy_semantic_map/` is executable and its checked-in suite currently passes on `slice/semantic-map-integration`.
- The current reporting model can classify the active wave as `green`, but many compiled canonical fields that should carry semantic structure remain empty across execution, subsystem, and object files.
- Current semantic-map canonical outputs are still biased toward execution surfaces and provenance capture, not toward business-semantic conclusions and semantic non-equivalence.
- Some current `legacy_code` supporting artifacts use simplified `.txt` snapshots or surface aliases that do not correspond to real current legacy-repo paths; this weakens semantic fidelity even when the registry is mechanically valid.
- `WorkDataHub` already contains business-semantic material that is stronger than raw implementation hints for some themes, for example:
  - `docs/business-background/客户主数据回填与状态来源分析.md`
  - `docs/business-background/年金计划类型与客户名称业务背景.md`
- `WorkDataHubPro` already contains durable `wiki-bi` evidence pages that express business-semantic conclusions, for example:
  - `docs/wiki-bi/evidence/customer-mdm-lifecycle-evidence.md`
  - related status/snapshot and identity evidence pages

### Core optimization goals
1. Make canonical semantic-map outputs answer **business-semantic questions** directly.
2. Distinguish **business equivalence** from **business non-equivalence** explicitly.
3. Rank sources by **semantic authority**, so implementation hints cannot silently outweigh stronger business-semantic evidence.
4. Preserve traceability from semantic conclusions back to legacy and current sources.
5. Make downstream `wiki-bi` absorption easier by attaching explicit absorption targets and readiness metadata.

### Explicit non-goals
This optimization must not:
- replace `docs/wiki-bi/` as the durable knowledge layer
- force automatic wiki absorption
- become a general parser of all legacy code structure before semantic usefulness is proven
- require broad reclassification of every existing first-wave semantic-map artifact in one slice
- silently weaken current claim provenance or current regression guarantees

## 2) Architecture Decision

### Option A - execution-first discovery and execution-first canonical outputs
**Pros**
- lowest implementation change
- reuses current compiler/reporting model almost unchanged

**Cons**
- preserves the current over-bias toward runtime surfaces and implementation adjacency
- keeps `green` vulnerable to meaningfully shallow semantic outputs
- does not solve the strongest business-semantic alignment problem

### Option B - execution-first discovery and semantic-first canonical outputs **(chosen)**
**Pros**
- preserves current discovery ergonomics and parallelism
- gives canonical outputs a business-semantic center of gravity
- supports stronger wiki absorption and anti-drift checks
- lets execution/subsystem outputs remain available as witnesses rather than pretending they are the knowledge product

**Cons**
- requires schema, compiler, reporting, and pilot-wave changes
- requires an explicit source-authority model and migration path

### Option C - semantic-first discovery and semantic-first canonical outputs
**Pros**
- the purest semantic model

**Cons**
- weakens early discovery ergonomics and parallel work partitioning
- makes provenance harder to accumulate incrementally
- is too large a departure for one bounded optimization slice

### Decision
Adopt **Option B** and validate it with one bounded semantic pilot theme before
changing wider semantic-map practice.

## 3) Acceptance Criteria

1. A checked-in plan exists at `docs/superpowers/plans/2026-04-17-workdatahubpro-semantic-map-semantic-first-canonical-optimization.md`.
2. A new narrow branch `slice/semantic-map-semantic-first-canonical-pilot` is cut from `slice/semantic-map-integration@002f4f7`.
3. The refactor program and first-wave coverage matrix are updated so this optimization is explicitly admitted as a planned cross-cutting semantic-map support slice before implementation begins.
4. The semantic-map schema supports semantic-first canonical nodes with at least these node families:
   - `semantic_concept`
   - `semantic_rule`
   - `semantic_non_equivalence`
   - `semantic_lifecycle`
   - `semantic_fact_family`
   - `semantic_decision_anchor`
5. The source model supports semantic-authority ranking with at least these roles:
   - `authoritative_semantic_source`
   - `runtime_witness`
   - `implementation_hint`
   - `historical_context`
6. Accepted semantic claims can point to real legacy-repo sources through a workspace-relative source model; accepted semantic canonical outputs must not rely on stub-only `.txt` aliases as primary semantic sources.
7. The compiler can generate semantic-first canonical outputs while preserving execution-first witness outputs.
8. Reporting adds semantic-alignment metrics, including at minimum:
   - semantic-question coverage
   - stub/virtual primary-source detection
   - semantic non-equivalence coverage
   - absorption-contract completeness
9. A small semantic pilot slice proves the optimization on a bounded business theme:
   - **customer status semantics**
   - using real legacy/current sources
   - producing semantic-first canonical outputs
   - producing a semantic report that is informative rather than structure-only
10. The pilot can be rerun deterministically from the semantic-map worktree and its targeted semantic suite passes before merge-back into `slice/semantic-map-integration`.
11. Full-suite verification (`uv run pytest -v`) passes before the optimization slice is considered merge-ready.

## 4) Chosen Small Validation Slice

### Slice name
`customer-status-semantic-pilot`

### Why this slice
This is the smallest high-value semantic theme that exercises the new model:

- it contains stable business concepts
- it contains explicit business rules
- it contains important non-equivalence boundaries
- it contains lifecycle semantics
- it has durable wiki targets already present
- it has both stronger business-background evidence and lower-authority implementation hints

### Required semantic conclusions for the pilot
The pilot must be able to represent, compile, and report at least the following:

1. **Concept**
   - customer master data
   - customer status
2. **Rule**
   - `is_new = is_winning_this_year AND NOT is_existing`
   - status sources are split across different fact families
3. **Non-equivalence**
   - customer master backfill ≠ customer status evaluation
   - `年金客户类型 = 新客` ≠ snapshot field `is_new`
4. **Lifecycle**
   - `yearly-init`, `sync`, `snapshot` are distinct lifecycle actions
5. **Fact family**
   - `规模明细`
   - `中标客户明细`
   - `流失客户明细`
   - customer snapshot tables
6. **Decision anchor**
   - `config/customer_status_rules.yml`

### Minimum real source set for the pilot
Legacy-side or source-of-truth inputs must include at least:
- `E:/Projects/WorkDataHub/docs/business-background/客户主数据回填与状态来源分析.md`
- `E:/Projects/WorkDataHub/config/customer_status_rules.yml`
- `E:/Projects/WorkDataHub/src/work_data_hub/customer_mdm/contract_sync.py`
- `E:/Projects/WorkDataHub/src/work_data_hub/customer_mdm/snapshot_refresh.py`
- `E:/Projects/WorkDataHub/src/work_data_hub/cli/etl/hooks.py`

Current-side supporting targets may include:
- `docs/wiki-bi/evidence/customer-mdm-lifecycle-evidence.md`
- the durable `wiki-bi` concept / standard / surface pages already covering customer-status semantics

### Pilot success condition
The pilot is successful when the semantic-first canonical layer makes the above
business conclusions explicit and reviewable **without** requiring a reviewer to
reconstruct them from execution-path files or raw implementation modules.

## 5) Proposed File And Directory Changes

### Governance and admission
- Modify: `docs/superpowers/specs/2026-04-11-workdatahubpro-refactor-program.md`
- Modify: `docs/superpowers/specs/2026-04-11-workdatahubpro-first-wave-legacy-coverage-matrix.md`
- Modify: `docs/superpowers/specs/2026-04-16-workdatahub-legacy-semantic-map-design.md`

### Semantic registry
- Create: `docs/wiki-bi/_meta/legacy-semantic-map/semantic/index.yaml`
- Create: `docs/wiki-bi/_meta/legacy-semantic-map/semantic/concepts/`
- Create: `docs/wiki-bi/_meta/legacy-semantic-map/semantic/rules/`
- Create: `docs/wiki-bi/_meta/legacy-semantic-map/semantic/non-equivalences/`
- Create: `docs/wiki-bi/_meta/legacy-semantic-map/semantic/lifecycles/`
- Create: `docs/wiki-bi/_meta/legacy-semantic-map/semantic/fact-families/`
- Create: `docs/wiki-bi/_meta/legacy-semantic-map/semantic/decision-anchors/`
- Create: `docs/wiki-bi/_meta/legacy-semantic-map/semantic/question-sets/`

### Claim and compiler tooling
- Modify: `scripts/legacy_semantic_map/models.py`
- Modify: `scripts/legacy_semantic_map/claims.py`
- Modify: `scripts/legacy_semantic_map/compiler.py`
- Modify: `scripts/legacy_semantic_map/reporting.py`
- Modify: `scripts/legacy_semantic_map/pilot.py`
- Prefer create: `scripts/legacy_semantic_map/semantic.py`

### Pilot-wave state
- Modify: `docs/wiki-bi/_meta/legacy-semantic-map/waves/index.yaml`
- Create: `docs/wiki-bi/_meta/legacy-semantic-map/claims/<semantic-pilot-wave-id>/semantic/*.yaml`
- Create or modify: `docs/wiki-bi/_meta/legacy-semantic-map/reports/waves/<semantic-pilot-wave-id>/`

### Tests
- Create: `tests/contracts/test_legacy_semantic_map_semantic_schema.py`
- Create: `tests/contracts/test_legacy_semantic_map_semantic_compiler.py`
- Create: `tests/contracts/test_legacy_semantic_map_semantic_reporting.py`
- Create: `tests/integration/test_legacy_semantic_map_customer_status_semantic_pilot.py`
- Modify: existing semantic-map contract/integration tests only where shared manifest or report expectations must expand

## 6) Implementation Steps

### Step 0 - Admit the optimization slice through governance first
**Files**
- Modify: `docs/superpowers/specs/2026-04-11-workdatahubpro-refactor-program.md`
- Modify: `docs/superpowers/specs/2026-04-11-workdatahubpro-first-wave-legacy-coverage-matrix.md`

**Actions**
- Add one explicit cross-cutting planned row for semantic-map semantic-first canonical alignment and wiki-absorption support.
- Record that this slice is a semantic-map support slice, not a new first-wave runtime rebuild slice.
- Name the new slice branch and integration baseline in the governance docs so later work does not start from `main`.

**Acceptance checkpoint**
- The optimization slice is no longer an implicit or local-only effort.
- Governance documents admit the work before any code/schema change begins.

### Step 1 - Extend the semantic-map design spec for the dual-layer model
**Files**
- Modify: `docs/superpowers/specs/2026-04-16-workdatahub-legacy-semantic-map-design.md`

**Actions**
- Add an explicit design delta section that states:
  - discovery remains execution-first
  - canonical outputs are semantic-first
  - execution/subsystem/object become witness-oriented support layers
- Define the semantic node families and semantic-authority roles.
- Define the no-stub primary-source rule for accepted semantic canonical outputs.
- Define the absorption-contract model that links semantic nodes to durable `wiki-bi` targets.

**Acceptance checkpoint**
- The optimization is governed by a checked-in spec delta, not only by plan text.

### Step 2 - Bootstrap the semantic-first canonical directory and vocabulary
**Files**
- Create: `docs/wiki-bi/_meta/legacy-semantic-map/semantic/index.yaml`
- Create: `docs/wiki-bi/_meta/legacy-semantic-map/semantic/question-sets/customer-status-semantic-pilot.yaml`
- Modify: `scripts/legacy_semantic_map/models.py`

**Actions**
- Add semantic-node vocabulary and stable IDs.
- Add question-set vocabulary so semantic coverage can be measured against explicit business questions rather than only entry surfaces.
- Keep this additive: do not remove current execution/subsystem/object directories in this slice.

**Acceptance checkpoint**
- The repository contains a canonical place for semantic-first outputs and semantic question sets.
- The schema stays additive and migration-safe for one bounded slice.

### Step 3 - Upgrade claim records to carry semantic findings and source authority
**Files**
- Modify: `scripts/legacy_semantic_map/claims.py`
- Modify: `scripts/legacy_semantic_map/models.py`
- Create or modify: `tests/contracts/test_legacy_semantic_map_semantic_schema.py`

**Actions**
- Extend claim schema to support semantic findings or semantic claim payloads.
- Add source records with:
  - `workspace_id`
  - `relative_path`
  - `semantic_authority`
  - optional local mirror/supporting `source_ref`
- Enforce that accepted semantic claims cannot use stub-only or virtualized aliases as their highest-authority primary semantic source.
- Preserve backward compatibility for current execution/subsystem/object claims where possible.

**Acceptance checkpoint**
- Claims can now express business-semantic discoveries directly.
- Source authority is explicit and machine-checkable.

### Step 4 - Implement semantic-first compilation while preserving witness outputs
**Files**
- Modify: `scripts/legacy_semantic_map/compiler.py`
- Prefer create: `scripts/legacy_semantic_map/semantic.py`
- Create or modify: `tests/contracts/test_legacy_semantic_map_semantic_compiler.py`

**Actions**
- Add compilation from accepted claims into semantic canonical nodes under `semantic/`.
- Preserve current execution/subsystem/object compilation for witness/provenance continuity.
- Add absorption-contract fields to compiled semantic nodes, for example:
  - `durable_target_pages`
  - `durable_summary_ready`
  - `requires_human_judgement`
  - `blocked_by`
  - `archive_after_absorption`
- Ensure compiled semantic nodes expose business-semantic conclusions directly rather than only source lists.

**Acceptance checkpoint**
- The compiler now produces a semantic-first canonical layer that is reviewable on its own.
- Existing witness outputs still compile.

### Step 5 - Add semantic-alignment reporting and fail-loud quality gates
**Files**
- Modify: `scripts/legacy_semantic_map/reporting.py`
- Create or modify: `tests/contracts/test_legacy_semantic_map_semantic_reporting.py`

**Actions**
- Add semantic metrics at minimum:
  - `semantic_question_coverage_pct`
  - `semantic_non_equivalence_coverage_pct`
  - `stub_primary_source_count`
  - `authoritative_primary_source_pct`
  - `absorption_contract_completion_pct`
- Add report blockers for:
  - missing required semantic questions in the pilot question set
  - accepted semantic nodes with stub-only highest-authority sources
  - semantic non-equivalence gaps where the question set requires them
- Keep current wave and coverage reporting, but distinguish structural coverage from semantic coverage.

**Acceptance checkpoint**
- A wave can no longer look semantically healthy merely because entry surfaces are covered.
- Reports directly surface semantic-quality defects.

### Step 6 - Implement the small customer-status semantic pilot
**Files**
- Modify: `docs/wiki-bi/_meta/legacy-semantic-map/waves/index.yaml`
- Create: `docs/wiki-bi/_meta/legacy-semantic-map/claims/<semantic-pilot-wave-id>/semantic/*.yaml`
- Create: semantic canonical files under:
  - `semantic/concepts/`
  - `semantic/rules/`
  - `semantic/non-equivalences/`
  - `semantic/lifecycles/`
  - `semantic/fact-families/`
  - `semantic/decision-anchors/`
- Create or modify: `tests/integration/test_legacy_semantic_map_customer_status_semantic_pilot.py`

**Actions**
- Open a dedicated semantic pilot wave, for example `wave-2026-04-17-customer-status-semantic-pilot`.
- Create accepted semantic claims for the customer-status theme using the minimum real source set listed in Section 4.
- Compile and report on the pilot wave.
- Verify that the pilot can answer the required semantic questions directly from semantic canonical outputs.

**Acceptance checkpoint**
- The pilot produces semantic-first outputs for one bounded business theme.
- Reviewers can validate business conclusions without reverse-engineering execution files.

### Step 7 - Rerun, inspect, and verify end-to-end behavior
**Files**
- Generated reports and manifest under `docs/wiki-bi/_meta/legacy-semantic-map/`

**Actions**
- Rerun the pilot flow from the semantic-map worktree.
- Inspect semantic canonical files, manifest, and reports.
- Run targeted semantic-map tests first, then full-suite verification.
- Merge back into `slice/semantic-map-integration` only after the feature branch is verified.

**Acceptance checkpoint**
- The optimization is proven by actual generated artifacts plus tests.
- Full-suite regression confidence is gathered before merge-back.

## 7) Small Slice Validation Scheme

### Validation question set
The small slice is valid only if the semantic report can answer all of these:

1. Are customer master backfill and customer status evaluation distinct concepts?
2. Is `is_new` defined as a status rule rather than a customer-master label?
3. Are the fact sources for status fields explicitly separated?
4. Are `yearly-init`, `sync`, and `snapshot` represented as distinct lifecycle actions?
5. Is `config/customer_status_rules.yml` represented as a decision anchor?
6. Are durable wiki targets named for each compiled semantic node?

### Minimum semantic outputs required
- 2 concept nodes
- 2 rule nodes
- 2 non-equivalence nodes
- 1 lifecycle node
- 1 fact-family node
- 1 decision-anchor node

### Failure conditions
The pilot fails if any of the following are true:
- a required question is unanswered
- a required non-equivalence is absent
- a primary semantic node depends on stub-only highest-authority sources
- semantic outputs only restate implementation paths without expressing business conclusions
- no durable absorption targets are attached

### Success criteria
The pilot succeeds when:
- semantic question coverage is `100`
- stub primary-source count is `0`
- all required non-equivalences are present
- all semantic nodes point to durable `wiki-bi` targets
- targeted tests pass

## 8) Risks And Mitigations

### Risk 1 - The semantic-first layer becomes a second durable wiki
**Mitigation**
- keep all semantic outputs under `docs/wiki-bi/_meta/legacy-semantic-map/semantic/`
- require absorption contracts instead of writing durable pages in this slice

### Risk 2 - Source-authority ranking becomes subjective and unstable
**Mitigation**
- use explicit enumerated authority roles
- lock the customer-status pilot against a real fixed source set

### Risk 3 - Backward compatibility breaks current semantic-map tooling
**Mitigation**
- keep the change additive
- preserve witness-layer compilation and existing core report behavior

### Risk 4 - The pilot theme is too narrow to prove the model
**Mitigation**
- choose a theme that includes concepts, rules, non-equivalences, lifecycle, fact families, and decision anchors in one bounded slice

### Risk 5 - The plan drifts into implementation-detail indexing again
**Mitigation**
- require business question coverage in reporting
- require direct semantic conclusions in canonical nodes

## 9) Verification Steps

### Branch setup
```powershell
git fetch --all --prune
git worktree add .worktrees/slice-semantic-map-semantic-first-canonical-pilot slice/semantic-map-integration
git -C .worktrees/slice-semantic-map-semantic-first-canonical-pilot switch -c slice/semantic-map-semantic-first-canonical-pilot
```

### Targeted semantic-map contract tests during development
```powershell
cd .worktrees/slice-semantic-map-semantic-first-canonical-pilot
uv run pytest tests/contracts/test_legacy_semantic_map_semantic_schema.py -v
uv run pytest tests/contracts/test_legacy_semantic_map_semantic_compiler.py -v
uv run pytest tests/contracts/test_legacy_semantic_map_semantic_reporting.py -v
```

### Small pilot integration check
```powershell
cd .worktrees/slice-semantic-map-semantic-first-canonical-pilot
uv run pytest tests/integration/test_legacy_semantic_map_customer_status_semantic_pilot.py -v
```

### Pilot-flow execution check
```powershell
cd .worktrees/slice-semantic-map-semantic-first-canonical-pilot
uv run python -m scripts.legacy_semantic_map.pilot --registry-root docs/wiki-bi/_meta/legacy-semantic-map --wave-id wave-2026-04-17-customer-status-semantic-pilot --legacy-root E:/Projects/WorkDataHub
```

### Inspect semantic outputs and reports
```powershell
Get-Content docs/wiki-bi/_meta/legacy-semantic-map/semantic/question-sets/customer-status-semantic-pilot.yaml
Get-Content docs/wiki-bi/_meta/legacy-semantic-map/reports/current/coverage-status.json
Get-Content docs/wiki-bi/_meta/legacy-semantic-map/reports/waves/wave-2026-04-17-customer-status-semantic-pilot/integrity-status.json
Get-ChildItem -Recurse docs/wiki-bi/_meta/legacy-semantic-map/semantic
```

### Full semantic-map regression before merge-back
```powershell
cd .worktrees/slice-semantic-map-semantic-first-canonical-pilot
uv run pytest tests/contracts/test_legacy_semantic_map_*.py tests/integration/test_legacy_semantic_map_reporting_pipeline.py tests/integration/test_legacy_semantic_map_first_wave_pilot_flow.py tests/integration/test_legacy_semantic_map_customer_status_semantic_pilot.py -v
```

### Required full-suite verification before claiming merge readiness
```powershell
cd .worktrees/slice-semantic-map-semantic-first-canonical-pilot
uv run pytest -v
```

## 10) Executable Checklist

- [ ] Create branch `slice/semantic-map-semantic-first-canonical-pilot` from `slice/semantic-map-integration@002f4f7`
- [ ] Update the refactor program to admit the semantic-map optimization slice
- [ ] Update the first-wave coverage matrix with an explicit planned cross-cutting row
- [ ] Check in the design-spec delta for the dual-layer model
- [ ] Add semantic node vocabulary and semantic question-set registry
- [ ] Extend claim schema with semantic authority and workspace-relative legacy source references
- [ ] Implement semantic-first canonical compilation
- [ ] Add semantic-alignment report metrics and blockers
- [ ] Add the `customer-status-semantic-pilot` wave and question set
- [ ] Check in accepted semantic claims for the customer-status pilot
- [ ] Compile semantic canonical outputs for the pilot
- [ ] Generate reports and inspect semantic quality gates
- [ ] Run targeted semantic-map tests
- [ ] Run full-suite verification
- [ ] Merge back into `slice/semantic-map-integration` after verification

## 11) RALPLAN-DR Deliberate Summary

### Principles
1. Discovery remains execution-first because it is still the best way to find hidden semantics.
2. Canonical outputs must be semantic-first because that is what downstream wiki absorption actually needs.
3. Source authority must be explicit so stronger business-semantic evidence outranks weaker implementation hints.
4. Non-equivalence is a first-class semantic output, not just an open question.
5. A small semantic pilot must prove the model before broad rollout.

### Top drivers
1. Align the semantic map to real business meaning rather than structural coverage alone.
2. Preserve current provenance and execution discovery strengths.
3. Make semantic-map outputs easier to absorb into durable `wiki-bi`.

### Why the small pilot is enough
- It is bounded enough to keep the slice mergeable.
- It stresses the exact semantic features the new model claims to improve.
- It proves whether the new compiler/reporting model is useful before broad adoption.

## 12) ADR

### Decision
Implement a bounded semantic-map optimization slice that preserves
execution-first discovery but changes canonical outputs to semantic-first,
validated through one small pilot wave focused on customer-status semantics.

### Drivers
- Current semantic-map outputs are mechanically valid but semantically shallow.
- The durable target is `wiki-bi`, not the execution graph itself.
- Real business semantics already exist in stronger legacy/current sources and should be modeled directly.

### Alternatives considered
- Keep execution-first canonical outputs.
- Rebuild the semantic map as semantic-first at both discovery and canonical layers.

### Why chosen
- It gives the best balance of continuity, semantic usefulness, and bounded implementation risk.

### Consequences
- The registry becomes more complex, but also more faithful to the actual knowledge-absorption goal.
- Reporting must now distinguish structural health from semantic health.
- Future semantic waves can expand theme by theme once the pilot proves useful.

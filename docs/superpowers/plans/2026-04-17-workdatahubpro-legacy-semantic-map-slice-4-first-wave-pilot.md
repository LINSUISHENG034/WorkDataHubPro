# WorkDataHubPro Legacy Semantic Map Slice 4 First-Wave Pilot Deliberate Consensus Plan

> **Status:** Proposed
>
> **Plan file:** `docs/superpowers/plans/2026-04-17-workdatahubpro-legacy-semantic-map-slice-4-first-wave-pilot.md`
>
> **Target branch:** `slice/semantic-map-first-wave-pilot`
>
> **Integration baseline:** branch from the current `slice/semantic-map-integration` head (`485f3a4 merge(slice.semantic-map): close reporting wave closeout`) and merge back into `slice/semantic-map-integration` after Slice 4 verification. Do not start from `main`.

## 1) Requirements Summary

### Slice intent
Implement `Slice 4: First-Wave Pilot` from `docs/superpowers/specs/2026-04-16-workdatahub-legacy-semantic-map-design.md`.

### Governing requirements
- Run the semantic-map model on a **first-wave-biased subset** of real legacy surfaces.
- Prove that **claim output**, **canonical compilation**, and **reporting/wave-closeout** work together on non-placeholder data.
- Preserve the semantic map as an **internal discovery ledger**, not durable wiki content.
- Keep helper logic under `scripts/legacy_semantic_map/`, not under `src/work_data_hub_pro/`.
- Use the current head of `slice/semantic-map-integration` as the integration baseline, then execute Slice 4 on its own branch `slice/semantic-map-first-wave-pilot`.
- Keep Slice 4 scoped to pilot execution and only make the **minimum** contract/tooling refinements needed to run a trustworthy pilot.

### Grounding facts from spec and repository inspection
- The semantic-map design orders slices as: registry bootstrap -> claim workflow -> canonical compilation -> reporting/wave closeout -> first-wave pilot.
- The integration baseline already contains `scripts/legacy_semantic_map/bootstrap.py`, `claims.py`, `compiler.py`, `reporting.py`, `closeout.py`, and `models.py`.
- The integration baseline already contains semantic-map contract tests plus `tests/integration/test_legacy_semantic_map_reporting_pipeline.py`.
- The checked-in semantic-map tree exists under `docs/wiki-bi/_meta/legacy-semantic-map/`.
- The checked-in registry still contains **placeholder-only** claim/report payloads:
  - `claims/` contains only `.gitkeep` placeholders.
  - `reports/` contains only `.gitkeep` placeholders.
  - `manifest.json` still shows `generated_canonical_files = []` and `compiled_claim_ids = []`.
- The active checked-in wave is still `wave-2026-04-16-registry-bootstrap`; Slice 4 therefore needs an explicit pilot-wave transition instead of pretending the bootstrap wave is the live discovery wave.
- Seeded entry surfaces currently include:
  - `annuity_performance`
  - `annual_award`
  - `annual_loss`
  - `annuity_income`
  - `customer_mdm`
  - `company_lookup_queue`
  - `reference_sync`
- Seeded high-priority source families currently include:
  - legacy domain capability maps and migration workflow guides
  - legacy operator CLI / orchestration runtime surfaces
  - legacy identity / reference runtime surfaces
  - current governance specs
  - current wiki-bi surfaces
  - current replay / reference assets
- The refactor program and first-wave coverage matrix already register the relevant first-wave and cross-cutting surfaces needed for pilot admission, including accepted domain rows and deferred operator/runtime rows such as:
  - `CT-011 company_lookup_queue`
  - `CT-012 reference_sync`
  - `CT-015 customer-mdm`
  - `CT-016 shared operator artifacts`

### Chosen pilot stance
This plan adopts a **breadth-balanced pilot with tiered depth**:
- all 7 seeded entry surfaces stay inside the pilot-wave denominator so Slice 4 proves the model across the admitted first-wave governance scope
- the 4 fact-domain surfaces receive deeper mapping and richer claim evidence
- the 3 operator/runtime-adjacent surfaces receive representative mapping depth, explicit candidates, and open-question handling where full semantic closure would exceed Slice 4

### Proposed admitted pilot denominator and depth tiers
Unless baseline inspection on the feature branch reveals a stronger already-accepted denominator contract, start the pilot wave with **all 7 seeded entry surfaces** admitted:
- `annuity_performance`
- `annual_award`
- `annual_loss`
- `annuity_income`
- `customer_mdm`
- `company_lookup_queue`
- `reference_sync`

Use tiered depth inside that denominator:

**Tier A — deep pilot coverage**
- `annuity_performance`
- `annual_award`
- `annual_loss`
- `annuity_income`

**Tier B — representative pilot coverage**
- `customer_mdm`
- `company_lookup_queue`
- `reference_sync`

Rationale:
- Tier A proves discovery usefulness on the 4 accepted first-wave fact domains.
- Tier B proves the map can register and route operator/runtime-adjacent surfaces without prematurely deciding retain/defer/retire or full runtime closure.

### Admitted high-priority source-family denominator
Slice 4 should use the exact seeded high-priority source-family denominator already defined in:

`docs/wiki-bi/_meta/legacy-semantic-map/sources/families.yaml`

The admitted family IDs for this pilot are:
- `legacy-domain-capability-maps`
- `legacy-operator-runtime-surfaces`
- `legacy-identity-and-reference-runtime`
- `current-first-wave-governance-specs`
- `current-wiki-bi-surfaces`
- `current-replay-and-reference-assets`

If Slice 4 changes this denominator, it must update `sources/families.yaml` explicitly and add matching contract coverage so reporting is provably using the same family set.

### Real-evidence policy for Slice 4
Slice 4 must be grounded in **actual legacy source files and current governance assets**.

Allowed use of synthetic or test-only fixtures:
- to extend automated test coverage
- to simulate edge cases that are difficult to trigger deterministically in tests
- to validate helper orchestration code around the pilot flow

Not allowed as the primary pilot evidence:
- synthetic claims that stand in for the actual chosen pilot surfaces
- fake wave data used to claim the pilot proved discovery usefulness

### Explicit “not Slice 4” guardrails
Slice 4 must **not**:
- close production/runtime decisions for `company_lookup_queue`, `reference_sync`, or manual `customer_mdm` command retention
- absorb discoveries into durable `docs/wiki-bi/` pages
- claim overall semantic-map closure beyond the admitted pilot-wave denominator
- redesign Slice 1-3 claim/compiler/report contracts except for prerequisite-only repairs that are explicitly documented as pilot blockers

## 2) Acceptance Criteria

1. A new plan file is created at `docs/superpowers/plans/2026-04-17-workdatahubpro-legacy-semantic-map-slice-4-first-wave-pilot.md`.
2. Execution starts on a new branch `slice/semantic-map-first-wave-pilot` cut from the current `slice/semantic-map-integration` head, not from `main`.
3. The registry transitions from the bootstrap wave to a dedicated pilot wave, with wave metadata updated explicitly rather than reusing `wave-2026-04-16-registry-bootstrap` as the active discovery wave.
4. Slice 4 admits all 7 seeded entry surfaces into one explicit pilot wave and records tiered mapping depth explicitly in `waves/index.yaml` and/or a closely paired pilot execution note.
5. The pilot produces **real checked-in claim artifacts** under `claims/<pilot-wave-id>/` for the admitted surfaces, and each mapping task records all required outputs:
   - `sources_read`
   - `objects_discovered`
   - `edges_added`
   - `candidates_raised`
6. At least one accepted real-evidence pilot mapping exists for every admitted entry surface, and at least one accepted real-evidence mapping exists for every admitted high-priority source family.
7. The main thread compiles accepted pilot claims into canonical registry files and the manifest is no longer empty:
   - `generated_canonical_files` is populated
   - `compiled_claim_ids` is populated
   - per-wave claim provenance stays visible
8. Slice 4 generates current and per-wave reports from the real pilot wave, not only from synthetic integration-test data.
9. The pilot proves end-to-end semantic-map usefulness by showing at least:
   - one compiled execution-path canonical file
   - one compiled subsystem canonical file
   - one compiled object canonical file
   - non-empty edge and/or candidate registries derived from real claims
10. The pilot wave must be mechanically reportable for its admitted denominator. Preferred closure is `green`. `yellow` is acceptable **only** when all spec-defined red conditions are absent:
   - `entrypoint_coverage_pct = 100`
   - `high_priority_source_family_coverage_pct = 100`
   - `orphan_high_priority_source_count = 0`
   - `stale_high_priority_candidate_count = 0`
   and any remaining non-green state is limited to incomplete connectivity or intentional closeout blockers such as durable wiki disposition still being open. Slice 4 must not close on a spec-defined `red` state.
11. Slice 4 does **not** absorb findings into durable `docs/wiki-bi/` pages and does **not** claim broad semantic-map closure beyond the admitted pilot denominator.
12. The semantic-map subtree remains excluded from durable wiki cataloging/lint expectations and no code under `src/work_data_hub_pro/` depends on pilot tooling.
13. Tests and verification cover the pilot runner/flow, real-claim compilation, report generation, and wave transition semantics.
14. After feature-branch verification, the slice is merged back into `slice/semantic-map-integration`, and the targeted semantic-map suite is rerun there before any later consideration of merge to `main`.

## 3) Implementation Steps Sized To Scope

### Step 0 - Baseline verification and slice branch setup
**Files:** none changed until baseline is verified.

**Actions**
- Verify that `slice/semantic-map-integration` at commit `485f3a4` contains the expected Slice 1-3 semantic-map tooling, tests, and checked-in registry tree.
- Create or reuse a linked worktree from that integration baseline.
- Create `slice/semantic-map-first-wave-pilot` from the verified integration head.
- Confirm the pilot branch starts from a clean working tree.

**Acceptance checkpoint**
- The new slice branch points to the current `slice/semantic-map-integration` head.
- Work is isolated from `main` and from future semantic-map slices.
- Any baseline drift is documented before code changes begin.

### Step 1 - Lock the pilot-wave admission and transition contracts first
**Files**
- Create: `tests/contracts/test_legacy_semantic_map_first_wave_pilot.py`
- Modify: `tests/contracts/test_legacy_semantic_map_reporting.py`
- Modify: `tests/contracts/test_legacy_semantic_map_wave_closeout.py`
- Modify: `tests/contracts/test_legacy_semantic_map_repo_docs.py` only if checked-in wave metadata expectations change

**Actions**
- Add failing contract tests for:
  - transitioning the active wave from bootstrap to a dedicated pilot wave
  - bounded pilot-wave denominators in `waves/index.yaml`
  - pilot source-family coverage denominators anchored to `sources/families.yaml`
  - rejecting pilot success when only placeholder claim/report surfaces exist
  - manifest/report population from real checked-in claim paths
  - preserving the non-durable semantic-map boundary during pilot execution
- Lock the all-7-surface pilot denominator and tiered-depth rule so the slice cannot silently shrink to a smaller proof target or expand to equal-depth mapping everywhere.
- If a thin pilot runner is introduced, lock its inputs/outputs here as well.

**Acceptance checkpoint**
- Tests fail for the intended missing Slice 4 behavior before implementation.
- Pilot scope, wave transition, tiered-depth policy, and real-evidence requirements are testable rather than aspirational.

### Step 2 - Introduce the dedicated pilot wave and denominator updates
**Files**
- Modify: `docs/wiki-bi/_meta/legacy-semantic-map/waves/index.yaml`
- Verify or modify: `docs/wiki-bi/_meta/legacy-semantic-map/sources/families.yaml`
- Modify: `docs/wiki-bi/_meta/legacy-semantic-map/README.md` if active-owner/wave wording needs to mention the pilot wave
- Modify: `scripts/legacy_semantic_map/models.py`
- Modify: `scripts/legacy_semantic_map/bootstrap.py` only if bootstrap defaults must support the new pilot-wave state deterministically

**Actions**
- Add a new wave, for example `wave-2026-04-17-first-wave-pilot`, with a higher ordinal than the bootstrap wave.
- Mark the bootstrap wave closed if that is required for deterministic staleness and closeout behavior.
- Set the pilot wave as `active_wave_id`.
- Seed the pilot wave with all 7 admitted entry surfaces and the admitted high-priority source families needed for a credible first-wave pilot denominator.
- Treat `sources/families.yaml` as the authoritative source-family denominator file for this slice and verify that the pilot tests/reporting use those exact family IDs.
- Record the tiered-depth rule clearly so the wave denominator is broad while evidence depth remains intentionally uneven.
- Keep denominator changes narrow: Slice 4 should refine pilot-wave scope, not redefine the global semantic-map vocabulary.

**Acceptance checkpoint**
- The registry has one explicit active pilot wave.
- Coverage and staleness math now reflect the pilot denominator instead of the bootstrap denominator.
- The tiered-depth rule keeps all admitted surfaces visible without forcing equal semantic depth.

### Step 3 - Capture real legacy-backed claims for the admitted denominator
**Files**
- Create: `docs/wiki-bi/_meta/legacy-semantic-map/claims/<pilot-wave-id>/execution/*.yaml`
- Create: `docs/wiki-bi/_meta/legacy-semantic-map/claims/<pilot-wave-id>/subsystems/*.yaml`
- Create: `docs/wiki-bi/_meta/legacy-semantic-map/claims/<pilot-wave-id>/objects/*.yaml`
- Optionally create a narrow pilot assignment/runbook note if task coordination needs a tracked artifact

**Actions**
- Read actual legacy sources for each admitted surface, including both code and relevant current governance/wiki artifacts where helpful.
- Author execution claims tied to all admitted entry surfaces.
- Author deeper subsystem and object claims for Tier A surfaces.
- Author representative subsystem/object/candidate outputs for Tier B surfaces without forcing premature runtime-closure semantics.
- Promote only the **smallest stable set** of semantic objects needed to prove the object graph and downstream reporting path.
- Raise candidate subsystem/object records instead of over-forcing unstable boundaries.
- Keep discovery-first posture: record what is real and traceable without deciding wiki absorption, retain/defer/retire outcomes, or final durable page taxonomy.

**Acceptance checkpoint**
- The pilot wave contains real claims with traceable source references.
- Claim files prove the map can record execution paths, subsystem boundaries, objects, edges, and candidates without placeholder-only data.
- All admitted surfaces appear in accepted pilot outputs, even when Tier B depth stops at representative mapping plus candidates/open questions.

### Step 4 - Add the thinnest reproducible pilot orchestration path
**Files**
- Preferred create: `scripts/legacy_semantic_map/pilot.py`
- Modify: `scripts/legacy_semantic_map/__init__.py`
- Create or modify: `tests/integration/test_legacy_semantic_map_first_wave_pilot.py`

**Actions**
- Add a thin main-thread-only pilot runner that:
  - selects explicit accepted claim paths for the pilot wave
  - compiles them through the canonical compiler
  - generates current and per-wave reports
  - evaluates closeout/archive readiness for the pilot wave
- Keep the runner under `scripts/legacy_semantic_map/` and scoped to orchestration only.
- Do **not** turn this into application runtime behavior or a second durable governance system.

**Acceptance checkpoint**
- The pilot can be rerun deterministically without hand-editing canonical files.
- Execution remains main-thread-controlled and traceable.

### Step 5 - Compile accepted claims and validate real report outputs
**Files**
- Modify: canonical registry files under `docs/wiki-bi/_meta/legacy-semantic-map/` as generated output
- Modify: `docs/wiki-bi/_meta/legacy-semantic-map/manifest.json`
- Generate: `reports/current/*.json`
- Generate: `reports/waves/<pilot-wave-id>/*.json`

**Actions**
- Compile the accepted pilot claims into canonical execution/subsystem/object/edge/candidate outputs.
- Confirm the manifest lists generated canonical files and compiled claim IDs.
- Generate current and per-wave reports from the real pilot data.
- Evaluate closeout readiness for the pilot wave, but treat a non-green or non-closeout-ready result as a legitimate pilot outcome if blockers are explicit and grounded.
- Require concrete checked-in outputs at minimum:
  - bootstrap-to-pilot wave transition in `waves/index.yaml`
  - real claim files under `claims/<pilot-wave-id>/`
  - non-empty canonical files under `execution/paths/`, `subsystems/`, `objects/`, `edges/`, and/or `candidates/`
  - populated `manifest.json`
  - current and per-wave report JSONs

**Acceptance checkpoint**
- The registry is no longer an empty shell.
- Reports and closeout logic run against real pilot content.
- Any blockers are mechanical and informative, not silent gaps.

### Step 6 - Record pilot findings without creating a second knowledge layer
**Files**
- Prefer create: `docs/runbooks/legacy-semantic-map-first-wave-pilot.md` or a similarly narrow execution record, if the command sequence and interpretation need durable operator guidance
- Modify: `docs/superpowers/plans/2026-04-17-workdatahubpro-legacy-semantic-map-slice-4-first-wave-pilot.md` only for final status links if needed

**Actions**
- Record the command sequence, expected outputs, and interpretation rules needed to rerun or review the pilot.
- Summarize what the pilot proved:
  - which Tier A surfaces mapped deeply and cleanly
  - which Tier B surfaces remained representative-only or candidate-heavy
  - whether the current denominator was too broad or too narrow
  - what should become the next absorption-adjacent or second-wave semantic-map follow-on
- Keep this summary operational; do not convert it into durable wiki-bi knowledge content.

**Acceptance checkpoint**
- Future maintainers can understand and rerun the pilot.
- The pilot produces actionable follow-on decisions without becoming a permanent second knowledge layer.

## 4) RALPLAN-DR Summary

### Principles
1. **Real evidence over synthetic comfort.** The pilot must prove the semantic-map model on actual legacy surfaces, not just on fixtures.
2. **Breadth with honest depth.** The pilot denominator should match the seeded first-wave governance scope, while evidence depth varies intentionally by surface class.
3. **Discovery before absorption.** Slice 4 records semantics and boundary issues; it does not decide durable wiki placement.
4. **Main-thread compilation and reporting discipline.** Distributed work may create claims, but canonical writes and pilot closeout stay centrally controlled.
5. **Minimal contract repair only.** Slice 4 may refine upstream tooling only when a real pilot blocker requires it.

### Top 3 decision drivers
1. Prove end-to-end semantic-map usefulness on non-placeholder data.
2. Keep the pilot denominator credible without letting the slice turn into a full legacy audit.
3. Exercise both domain and operator/orchestration surfaces so the pilot does not overfit to one class of legacy semantics.

### Viable options

#### Option A - Equal-depth breadth-first pilot across all seeded entry surfaces
**Pros**
- Maximizes early coverage denominator pressure.
- Quickly exposes missing schema or reporting assumptions.

**Cons**
- High risk of shallow claims, noisy subsystem/object boundaries, and scope blowout.
- More likely to cause schema churn, candidate sprawl, and merge conflict risk.
- Harder to prove discovery usefulness before the slice balloons.

#### Option B - Depth-first pilot on a single first-wave domain only
**Pros**
- Best semantic quality per mapped surface.
- Lowest immediate slice complexity.

**Cons**
- Risks overfitting the model to one domain archetype.
- Does not prove the operator/orchestration surfaces that motivated seeded cross-cutting runtime entries.
- Weak evidence for whether the semantic map can coordinate multi-surface discovery.

#### Option C - Breadth-balanced pilot across all 7 seeded surfaces with tiered depth (**Chosen**)
**Pros**
- Keeps the pilot denominator aligned with the already-seeded first-wave governance scope.
- Exercises all admitted surface families while preserving deeper work where it matters most.
- Stronger evidence that the map can guide future absorption and follow-on waves.

**Cons**
- Requires careful control to avoid breadth collapsing into shallow semantics.
- Increases curation and review load versus a smaller pilot.
- Requires explicit messaging so stakeholders do not mistake the pilot for global closure or runtime/operator closure.

### Why alternatives were not chosen
- Option A is invalid for Slice 4 if it implies equal depth across all surfaces; that would likely convert the pilot into a de facto full-wave mapping effort before the model has proven its operational usefulness.
- Option B is too narrow because it would not pressure-test the seeded operator/orchestration surfaces that were explicitly admitted into the semantic-map design.

## 5) Pre-Mortem

### Scenario 1 - The pilot claims success but only proves synthetic plumbing
**How it happens**
- The slice leans on fixture-generated claim payloads or test-only data instead of real legacy inspection.

**Impact**
- Reporting and compilation appear healthy, but the semantic map still has not demonstrated discovery value.

**Mitigation**
- Require real checked-in pilot claims sourced from actual legacy files.
- Keep fixtures limited to tests and edge-case validation.

### Scenario 2 - The pilot expands into shallow equal-depth breadth and becomes noisy
**How it happens**
- The team treats every admitted surface as requiring the same depth of semantic decomposition.

**Impact**
- Claims become thin, candidate volume explodes, and the slice loses its bounded purpose.

**Mitigation**
- Lock the all-7-surface denominator but also lock the tiered-depth rule in tests and wave metadata.
- Treat additional depth beyond the chosen tiers as later-wave follow-on work unless a blocker forces it.

### Scenario 3 - Wave bookkeeping stays bootstrap-shaped and corrupts report meaning
**How it happens**
- Slice 4 writes real claims while leaving the bootstrap wave active, so denominators, staleness, and closeout semantics refer to the wrong wave.

**Impact**
- Reports look machine-generated but are semantically misleading.

**Mitigation**
- Require an explicit pilot-wave transition before real pilot claims are compiled.
- Add tests for wave-ordinal correctness and manifest/report alignment.

## 6) Expanded Test Plan

### Unit / contract
- `tests/contracts/test_legacy_semantic_map_first_wave_pilot.py`
  - pilot-wave admission rules
  - active-wave transition from bootstrap to pilot
  - rejection of placeholder-only pilot success
  - tiered-depth denominator expectations
  - pilot runner argument/path validation if a runner is added
- Extend reporting/wave-closeout contract tests as needed to ensure the pilot wave drives denominators and report interpretation.

### Integration
- `tests/integration/test_legacy_semantic_map_first_wave_pilot.py`
  - compile real-style pilot claims through the end-to-end flow
  - generate current and per-wave reports for the pilot wave
  - verify manifest/report population and deterministic reruns
- Keep `tests/integration/test_legacy_semantic_map_reporting_pipeline.py` green as the baseline synthetic pipeline guardrail.

### End-to-end / workflow
- Branch from `slice/semantic-map-integration`.
- Create or update pilot-wave claims.
- Run the pilot runner (or explicit main-thread orchestration path) to compile claims and generate reports.
- Inspect the resulting canonical files, manifest, and report outputs.
- Run `uv run pytest -v` before claiming the slice complete or merge-ready.
- Merge back into `slice/semantic-map-integration` only after targeted verification passes.

### Observability / artifact checks
- Inspect `manifest.json` for non-empty `generated_canonical_files`, `compiled_claim_ids`, and per-wave claim provenance.
- Inspect `reports/current/coverage-status.json` and `reports/current/integrity-status.json` for the pilot wave.
- Inspect `reports/waves/<pilot-wave-id>/...` for stable snapshot output.
- Verify that newly generated canonical files and reports correspond only to the accepted pilot claims.

## 7) Risks And Mitigations

### Risk 1 - The pilot turns into implicit Phase B wiki absorption
- **Risk:** engineers start classifying final wiki destinations or creating durable wiki pages while mapping.
- **Mitigation:** keep Slice 4 outputs inside the semantic-map subtree and operational docs only; no durable wiki page creation is in scope.

### Risk 2 - Too many objects get promoted too early
- **Risk:** to prove object compilation, the slice promotes every discovered semantic object.
- **Mitigation:** promote only the minimum stable set needed to prove the object graph and downstream reporting path; leave the rest inline or as candidates.

### Risk 3 - Pilot runner scope creeps into permanent runtime tooling
- **Risk:** a helper under `scripts/legacy_semantic_map/` grows into a generalized runtime surface.
- **Mitigation:** keep the runner thin, main-thread-only, and explicitly tied to semantic-map orchestration.

### Risk 4 - Report status is misread as runtime/operator closure or overall semantic-map closure
- **Risk:** a `green` pilot wave is mistaken for full runtime/operator closure or full semantic-map completion.
- **Mitigation:** bind the pilot denominator and tiered-depth rule explicitly in `waves/index.yaml` and in the plan/runbook wording, and keep the explicit “not Slice 4” guardrail section.

### Risk 5 - Shared contract churn reopens Slice 1-3 boundaries
- **Risk:** pilot implementation starts redesigning claim schema, compiler layout, or report semantics unnecessarily.
- **Mitigation:** limit upstream edits to the smallest repair required for real pilot execution, and document any such repair explicitly.

## 8) Verification Steps

### Branch and baseline setup
```bash
git fetch --all --prune
git branch --list slice/semantic-map-integration
git worktree add .worktrees/slice-semantic-map-first-wave-pilot slice/semantic-map-integration
git -C .worktrees/slice-semantic-map-first-wave-pilot switch -c slice/semantic-map-first-wave-pilot
```

### Targeted contract and integration runs during development
```bash
uv run pytest tests/contracts/test_legacy_semantic_map_first_wave_pilot.py -v
uv run pytest tests/contracts/test_legacy_semantic_map_reporting.py tests/contracts/test_legacy_semantic_map_wave_closeout.py -v
uv run pytest tests/integration/test_legacy_semantic_map_first_wave_pilot.py -v
```

### Targeted semantic-map suite before merge back to integration
```bash
uv run pytest tests/contracts/test_legacy_semantic_map_*.py tests/integration/test_legacy_semantic_map_reporting_pipeline.py tests/integration/test_legacy_semantic_map_first_wave_pilot.py -v
```

### Pilot-flow execution check
If Slice 4 adds a thin runner:
```bash
uv run python -m scripts.legacy_semantic_map.pilot --registry-root docs/wiki-bi/_meta/legacy-semantic-map --wave-id <pilot-wave-id> --claim <accepted-claim-path> --claim <accepted-claim-path>
```

If Slice 4 intentionally keeps orchestration as a documented inline flow instead of a runner, the runbook must provide the exact `uv run python` sequence and the same sequence must be exercised in integration coverage.

### Integration-branch verification after merge
```bash
git switch slice/semantic-map-integration
git merge --no-ff slice/semantic-map-first-wave-pilot
uv run pytest tests/contracts/test_legacy_semantic_map_*.py tests/integration/test_legacy_semantic_map_reporting_pipeline.py tests/integration/test_legacy_semantic_map_first_wave_pilot.py -v
```

### Required full-suite verification before claiming Slice 4 complete / merge-ready
```bash
uv run pytest -v
```

## 9) ADR Section

### Decision
Implement Slice 4 as a **breadth-balanced first-wave pilot** on a new branch `slice/semantic-map-first-wave-pilot`, cut from `slice/semantic-map-integration`, using a dedicated pilot wave with all 7 seeded entry surfaces admitted and tiered mapping depth so the pilot proves the model across the seeded governance scope without forcing equal semantic depth everywhere.

### Drivers
- Need to prove the semantic-map stack on real non-placeholder data.
- Need a credible pilot denominator that still stays mergeable as one slice branch.
- Need to preserve the semantic map as a temporary discovery ledger instead of a second durable wiki layer.

### Alternatives considered
- Equal-depth breadth-first pilot across all seeded surfaces.
- Depth-first pilot on a single domain only.
- Breadth-balanced multi-surface pilot with all 7 seeded surfaces admitted and tiered depth.

### Why chosen
- It provides stronger real-world evidence than a smaller subset pilot because the denominator matches the seeded first-wave governance scope.
- It keeps scope bounded enough to remain one slice branch by varying evidence depth rather than expanding to equal-depth mapping everywhere.
- It tests the parts of the design that matter most for future waves: admission, claim creation, canonical compilation, reporting, and boundary/candidate handling.

### Consequences
- Some surfaces will remain representative-only in this pilot even though they are inside the denominator.
- The slice must explicitly communicate denominator scope and tiered depth to avoid misleading coverage claims.
- Minimal upstream contract/tooling repairs may be required if real pilot execution exposes gaps in the current Slice 1-3 baseline.

### Follow-ups
- Decide the next semantic-map wave or absorption-adjacent follow-on based on pilot findings.
- Revisit whether `company_lookup_queue` or another deferred runtime surface should anchor the next wave.
- Archive or retire semantic-map tooling only after the later absorption wave closes and durable wiki updates are accepted.

## 10) Available-Agent-Types Roster And Follow-Up Staffing Guidance

### Available agent types relevant to this slice
- `architect` - wave-boundary design, pilot denominator rules, anti-drift review
- `planner` - sequencing, slice scoping, and merge choreography
- `executor` - claim authoring support, pilot runner implementation, registry/report integration
- `test-engineer` - contract and integration coverage for pilot flow
- `verifier` - manifest/report evidence validation and merge-readiness checks
- `critic` - challenge pilot scope creep and false-proof risks
- `writer` - runbook or pilot-operations documentation if needed
- `code-reviewer` - post-implementation review before merge

### Ralph follow-up guidance
Use Ralph when one persistent owner should drive Slice 4 from wave setup through pilot evidence capture.

**Recommended Ralph lane mix**
- `architect` - **high** reasoning
  - owns pilot-wave admission, denominator, and minimal-contract-repair decisions
- `executor` - **high** reasoning
  - owns pilot claims, pilot orchestration helper, and canonical/report flow
- `test-engineer` - **medium** reasoning
  - owns contract/integration tests for the pilot flow
- `verifier` - **high** reasoning
  - owns manifest/report validation and post-merge semantic-map suite evidence

**Suggested Ralph use**
- Best when pilot execution is expected to reveal a few sequential contract adjustments and you want one loop to keep reconciling them without multi-lane coordination overhead.

### Team follow-up guidance
For actual execution, prefer team mode when you want parallel claim-authoring and verification lanes.

**Recommended headcount:** 4 workers
- 2 discovery/delivery lanes
- 1 test lane
- 1 verification/merge-prep lane

**Role allocation guidance**
- **Lane 1 - fact-domain discovery**
  - effective role: `executor`
  - reasoning: **high**
  - owns Tier A pilot claims for the fact-domain surfaces
- **Lane 2 - operator/runtime discovery + pilot runner**
  - effective role: `executor`
  - reasoning: **high**
  - owns Tier B pilot claims plus the thin pilot orchestration helper and any minimal script wiring
- **Lane 3 - contract/integration tests**
  - effective role: `test-engineer`
  - reasoning: **medium**
  - owns pilot-wave contract tests and end-to-end pilot integration coverage
- **Lane 4 - verification and merge-prep**
  - effective role: `verifier`
  - reasoning: **high**
  - owns manifest/report inspection, targeted suite reruns, and post-merge verification on `slice/semantic-map-integration`

**Explicit launch hint**
```bash
$team 4:executor "Execute Slice 4 legacy semantic map first-wave pilot from slice/semantic-map-first-wave-pilot; keep one worker on tests and one on verification; do not merge to main"
```

**Alternative launch hint with reasoning args**
```bash
OMX_TEAM_WORKER_LAUNCH_ARGS="-c model_reasoning_effort=high" omx team 4:executor "Execute Slice 4 legacy semantic map first-wave pilot from slice/semantic-map-first-wave-pilot; keep one worker on tests and one on verification; do not merge to main"
```

**Team verification path**
1. Leader confirms the worktree is branched from `slice/semantic-map-integration`.
2. Discovery lanes author bounded pilot claims from real legacy sources.
3. Test lane proves pilot-wave contracts and end-to-end flow deterministically.
4. Verification lane checks that canonical files, manifest, and reports are populated from accepted pilot claims only.
5. Leader merges `slice/semantic-map-first-wave-pilot` back into `slice/semantic-map-integration`.
6. Verification lane or leader reruns the targeted semantic-map suite on `slice/semantic-map-integration`.
7. No `main` merge occurs as part of Slice 4 closure.

## Proposed Merge Strategy

1. Keep the repository root worktree clean on `main`.
2. Create or reuse a linked worktree for `slice/semantic-map-integration`.
3. Branch `slice/semantic-map-first-wave-pilot` from the verified integration baseline head.
4. Complete Slice 4 and run targeted semantic-map verification on the feature branch.
5. Merge `slice/semantic-map-first-wave-pilot` back into `slice/semantic-map-integration` with an explicit slice-closure reason.
6. Rerun the targeted semantic-map suite on `slice/semantic-map-integration`.
7. Do not merge to `main` until the larger semantic-map package completes its later acceptance path.

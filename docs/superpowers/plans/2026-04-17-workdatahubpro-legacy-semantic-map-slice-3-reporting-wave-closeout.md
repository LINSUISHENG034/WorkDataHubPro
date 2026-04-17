# WorkDataHubPro Legacy Semantic Map Slice 3 Reporting And Wave Closeout Deliberate Consensus Plan

> **Status:** Proposed
>
> **Plan file:** `docs/superpowers/plans/2026-04-17-workdatahubpro-legacy-semantic-map-slice-3-reporting-wave-closeout.md`
>
> **Target branch:** `slice/semantic-map-reporting-wave-closeout`
>
> **Integration baseline:** branch from the current `slice/semantic-map-integration` head, then merge back into `slice/semantic-map-integration` after Slice 3 verification. Do not start from `main`.

## 1) Requirements Summary

### Slice intent
Implement `Slice 3: Reporting And Wave Closure` from `docs/superpowers/specs/2026-04-16-workdatahub-legacy-semantic-map-design.md`.

### Governing requirements
- Implement integrity and coverage reporting.
- Implement candidate staleness calculation using wave ordinals, not wall-clock age.
- Implement wave closeout and archive-readiness checks.
- Preserve claim immutability once a claim artifact is accepted into a wave closeout.
- Make wave status mechanically classifiable as `red`, `yellow`, or `green`.
- Keep semantic-map helper logic under `scripts/legacy_semantic_map/`, not under `src/work_data_hub_pro/`.
- Keep implementation-plan artifacts under `docs/superpowers/plans/`.
- Follow slice discipline: use one explicit slice branch and merge back to `slice/semantic-map-integration`, not directly to `main`.

### Grounding facts from spec and repo inspection
- Spec scope for Slice 3 is the reporting, staleness, and closeout slice.
- Spec requires immutable accepted claim artifacts at closeout.
- Spec defines wave responsibilities to include staleness measurement, closeout reporting, and archive eligibility.
- Spec recommends the branch name `slice/semantic-map-reporting-wave-closeout`.
- Spec defines required status outputs `red`, `yellow`, and `green` and the minimum mechanical metrics:
  - `entrypoint_coverage_pct`
  - `high_priority_source_family_coverage_pct`
  - `object_edge_coverage_pct`
  - `orphan_high_priority_source_count`
  - `stale_high_priority_candidate_count`
  - `untriaged_candidate_age_by_wave`
- Spec defines thresholds:
  - `green`: `entrypoint_coverage_pct = 100`, `high_priority_source_family_coverage_pct = 100`, `orphan_high_priority_source_count = 0`, `object_edge_coverage_pct >= 95`, `stale_high_priority_candidate_count = 0`
  - `yellow`: mostly mapped, but not green; no critical high-priority unmapped surface is being ignored
  - `red`: any high-priority entry surface unmapped, any high-priority source family unmapped, orphan high-priority sources exist, or a high-priority candidate is untriaged for more than one audit wave
- Spec tree already reserves:
  - `docs/wiki-bi/_meta/legacy-semantic-map/reports/current/coverage-status.json`
  - `docs/wiki-bi/_meta/legacy-semantic-map/reports/current/integrity-status.json`
  - `docs/wiki-bi/_meta/legacy-semantic-map/reports/waves/<wave_id>/...`
- Current checked-out root worktree inspection does **not** match all supplied grounding facts:
  - current branch here is `main`, not `slice/semantic-map-integration`
  - current root checkout does not currently contain `scripts/legacy_semantic_map/` or `docs/wiki-bi/_meta/legacy-semantic-map/`
- Therefore execution must begin by switching to, or creating a linked worktree from, the real `slice/semantic-map-integration` baseline before any code work starts. If that baseline still lacks the expected Slice 1 and Slice 2 artifacts, stop and reconcile baseline drift before implementation.

### Recommended metric and closeout definitions for this slice
These should be locked in this plan unless baseline inspection reveals a stronger already-accepted contract on `slice/semantic-map-integration`.

#### Reporting metrics
- `entrypoint_coverage_pct`
  - numerator: seeded high-priority entry surfaces for the target wave that compile to at least one accepted canonical route into the semantic map
  - denominator: seeded high-priority entry surfaces assigned to the target wave in `waves/index.yaml` and `execution/entry-surfaces.yaml`
- `high_priority_source_family_coverage_pct`
  - numerator: seeded high-priority source families for the target wave that attach to at least one accepted canonical node or routed edge
  - denominator: seeded high-priority source families assigned to the target wave in `sources/families.yaml` and `waves/index.yaml`
- `object_edge_coverage_pct`
  - numerator: canonical objects in the target wave that participate in at least one accepted edge in `edges/subsystem-to-object.yaml`, `edges/object-to-object.yaml`, or `edges/source-to-node.yaml`
  - denominator: canonical objects compiled for the target wave into `objects/index.yaml`
  - note: this denominator is derived from canonical compile output rather than a separately seeded object catalog; that is acceptable for Slice 3 because the metric is measuring connectivity quality, not discovery entitlement
- `orphan_high_priority_source_count`
  - count of high-priority seeded source families with no accepted routed edge to any canonical node
- `stale_high_priority_candidate_count`
  - count of high-priority candidates whose `triage_status` remains unresolved and whose age-by-wave is greater than `1`
- `untriaged_candidate_age_by_wave`
  - `current_active_wave_ordinal - first_seen_wave_ordinal`
  - calculated per candidate and surfaced in aggregate summaries as at least `max`, `count_gt_0`, and `count_gt_1`

#### Wave closeout inputs
- `docs/wiki-bi/_meta/legacy-semantic-map/waves/index.yaml`
- `docs/wiki-bi/_meta/legacy-semantic-map/manifest.json`
- canonical registry outputs under `execution/`, `subsystems/`, `objects/`, `edges/`, `sources/`, `candidates/`
- claim artifacts for the target wave under `claims/<wave_id>/`
- current and per-wave reporting outputs under `reports/`
- target-wave durable absorption disposition evidence recorded in wave metadata or closeout metadata

#### Wave closeout outputs
Keep the spec's reserved report-file shape rather than introducing extra top-level report files.
- `reports/current/coverage-status.json`
- `reports/current/integrity-status.json`
- `reports/waves/<wave_id>/coverage-status.json`
- `reports/waves/<wave_id>/integrity-status.json`
- manifest updates that accurately record:
  - `generated_canonical_files`
  - `compiled_claim_ids`
  - report file references for the current generation, if the existing manifest contract allows extension without breaking earlier slices

#### Wave closeout decision fields
Recommended JSON fields to add to `integrity-status.json`:
- `wave_id`
- `wave_status`
- `closeout_ready`
- `archive_ready`
- `immutability_check_passed`
- `required_claim_ids`
- `compiled_claim_ids`
- `missing_claim_ids`
- `mutable_claim_ids_detected`
- `blocking_reasons`
- `generated_at`

#### Archive readiness rule
A wave is `archive_ready = true` only when all are true:
- `closeout_ready = true`
- durable wiki targets for the wave are accepted
- remaining findings are explicitly marked as absorbed, deferred, or retired for that wave
- no mutable accepted claim artifact was rewritten after closeout acceptance
- no active wave remains that still depends on the target wave's semantic-map working state

## 2) Acceptance Criteria

1. A new plan file is created at `docs/superpowers/plans/2026-04-17-workdatahubpro-legacy-semantic-map-slice-3-reporting-wave-closeout.md`.
2. Execution starts from a new branch `slice/semantic-map-reporting-wave-closeout` cut from the current `slice/semantic-map-integration` head, not from `main`.
3. Slice 3 adds deterministic reporting logic under `scripts/legacy_semantic_map/` that produces the reserved `coverage-status.json` and `integrity-status.json` outputs for current and per-wave locations.
4. Reporting calculates all six required metrics and classifies each target wave as `red`, `yellow`, or `green` using the spec thresholds.
5. Candidate staleness is calculated from wave ordinals only; no wall-clock-only staleness rule is used.
6. Closeout logic mechanically decides:
   - whether a wave is closeout-ready
   - whether a wave is archive-ready
   - why it is blocked when not ready
7. Accepted claim artifacts are treated as immutable once included in a wave closeout decision; the slice includes a check that detects rewritten accepted claim artifacts instead of silently tolerating mutation.
8. Manifest generation is trustworthy enough for closeout review:
   - `generated_canonical_files` is populated from actual compile output
   - `compiled_claim_ids` is populated from the claims that fed the current canonical state
   - if current baseline still leaves these empty, Slice 3 includes the minimum contract repair required to make closeout reporting credible
9. Targeted semantic-map contract and integration tests cover reporting, staleness, closeout, and manifest/report consistency.
10. After slice verification on the feature branch, the branch is merged back into `slice/semantic-map-integration`, and the full semantic-map targeted suite is rerun there before any later consideration of merge to `main`.

## 3) Implementation Steps Sized To Scope

### Step 0 - Baseline reconciliation and branch setup
**Files:** none changed until baseline is verified.

**Actions**
- Verify that `slice/semantic-map-integration` exists and contains the expected Slice 1 and Slice 2 surfaces:
  - `scripts/legacy_semantic_map/bootstrap.py`
  - `scripts/legacy_semantic_map/claims.py`
  - `scripts/legacy_semantic_map/compiler.py`
  - `scripts/legacy_semantic_map/models.py`
  - `docs/wiki-bi/_meta/legacy-semantic-map/...`
  - semantic-map contract tests
- Create a linked worktree from `slice/semantic-map-integration` if the repository root remains on `main`.
- Create `slice/semantic-map-reporting-wave-closeout` from that verified integration baseline.

**Acceptance checkpoint**
- The new slice branch points to the current `slice/semantic-map-integration` head.
- The implementation workspace is isolated from `main`.
- Any mismatch between the asserted baseline and the actual baseline is documented before coding begins.

### Step 1 - Lock report and closeout contracts in tests first
**Files**
- Create: `tests/contracts/test_legacy_semantic_map_reporting.py`
- Create: `tests/contracts/test_legacy_semantic_map_wave_closeout.py`
- Modify: existing semantic-map contract test files on the integration baseline if they already cover manifest/compiler contracts

**Actions**
- Add failing contract tests for:
  - metric formulas and required keys in `coverage-status.json`
  - status classification to `red` / `yellow` / `green`
  - candidate staleness age-by-wave calculation
  - required keys in `integrity-status.json`
  - claim immutability detection after closeout acceptance
  - manifest/report consistency for `generated_canonical_files` and `compiled_claim_ids`
- Use fixed fixture data for at least three waves:
  - a clearly `red` wave
  - a `yellow` wave with incomplete connectivity or stale candidates
  - a `green` wave that meets all thresholds

**Acceptance checkpoint**
- Tests fail for the intended missing Slice 3 behavior before implementation.
- Tests encode the non-negotiable Slice 3 rules, especially closeout immutability and wave-ordinal staleness.

### Step 2 - Add reporting domain models and report writer logic
**Files**
- Modify: `scripts/legacy_semantic_map/models.py`
- Create: `scripts/legacy_semantic_map/reporting.py`
- Modify: `scripts/legacy_semantic_map/__init__.py`

**Actions**
- Add explicit dataclasses or typed structures for:
  - coverage metrics
  - integrity metrics
  - closeout decision
  - archive readiness result
- Implement deterministic report assembly in `reporting.py`.
- Keep the reserved two-file report surface:
  - coverage metrics and wave status in `coverage-status.json`
  - integrity, immutability, closeout, and archive-readiness detail in `integrity-status.json`
- Ensure writer logic can generate both:
  - `reports/current/*.json`
  - `reports/waves/<wave_id>/*.json`

**Acceptance checkpoint**
- Report builders accept canonical registry inputs and wave metadata without requiring manual edits.
- Report JSON schemas are stable and deterministic.

### Step 3 - Refine compiler and manifest integration only where Slice 3 depends on it
**Files**
- Modify: `scripts/legacy_semantic_map/compiler.py`
- Modify: `scripts/legacy_semantic_map/claims.py` if claim metadata exposure is needed for closeout checks
- Modify: `scripts/legacy_semantic_map/bootstrap.py` only if report directory seeding or manifest defaults must be corrected
- Modify: `docs/wiki-bi/_meta/legacy-semantic-map/manifest.json` fixture/check-in on the slice baseline

**Actions**
- Populate manifest fields required for trustworthy reporting:
  - `generated_canonical_files`
  - `compiled_claim_ids`
- Ensure compiler exposes enough trace data for reporting to tie canonical state back to accepted claims.
- Seed reserved report directories and minimal placeholder files only if the integration baseline does not already do so.
- Do **not** redesign claim format or canonical schema beyond what reporting and closeout require.

**Acceptance checkpoint**
- Running compiler + reporting can produce a manifest that supports closeout review.
- Manifest data is generated from compile inputs, not handwritten.

### Step 4 - Implement candidate staleness and closeout decisioning
**Files**
- Modify: `scripts/legacy_semantic_map/reporting.py`
- Create: `scripts/legacy_semantic_map/closeout.py`
- Modify: `scripts/legacy_semantic_map/models.py`
- Modify: `scripts/legacy_semantic_map/__init__.py`

**Actions**
- Implement `untriaged_candidate_age_by_wave` based on wave ordinals.
- Compute `stale_high_priority_candidate_count` with the explicit stale rule: unresolved high-priority candidate and age-by-wave greater than `1`.
- Implement closeout gating:
  - required reports present
  - no missing compiled accepted claim IDs
  - no mutable accepted claim artifacts detected
  - durable absorption dispositions complete
  - thresholds satisfied for target status
- Implement archive-readiness gating on top of closeout readiness rather than as an independent shortcut.

**Acceptance checkpoint**
- The slice can mechanically explain why a wave is blocked.
- Closeout and archive readiness are deterministic for the same input tree.

### Step 5 - Add end-to-end semantic-map reporting flow coverage
**Files**
- Create: `tests/integration/test_legacy_semantic_map_reporting_pipeline.py`
- Modify: existing semantic-map integration fixtures if present on the baseline
- Modify checked-in sample tree under `docs/wiki-bi/_meta/legacy-semantic-map/` only as needed for deterministic fixture realism

**Actions**
- Build an integration test that runs the semantic-map flow in order:
  - bootstrap or load seeded tree
  - compile accepted claims
  - generate current reports
  - generate per-wave reports
  - evaluate closeout and archive readiness
- Verify that `red`, `yellow`, and `green` outcomes match the fixture scenarios.
- Verify immutability detection by simulating a post-closeout rewrite attempt of an accepted claim artifact in test fixtures.

**Acceptance checkpoint**
- The feature is proven end-to-end on deterministic fixtures, not only by unit math tests.

### Step 6 - Documentation, merge prep, and slice integration
**Files**
- Create: `docs/superpowers/plans/2026-04-17-workdatahubpro-legacy-semantic-map-slice-3-reporting-wave-closeout.md`
- Modify: any semantic-map README or plan cross-reference files only if needed for discoverability

**Actions**
- Keep this plan checked in.
- Document any manifest-contract refinement that Slice 3 had to absorb from baseline drift.
- Merge the verified branch back into `slice/semantic-map-integration`.
- Rerun the full semantic-map targeted suite on `slice/semantic-map-integration` after merge.

**Acceptance checkpoint**
- Slice 3 closes as one explicit slice branch.
- Integration branch remains the only semantic-map staging branch ahead of any future `main` merge.

## 4) Risks And Mitigations

### Risk 1 - Baseline drift between supplied facts and actual repo state
- **Risk:** the current root checkout does not show the expected semantic-map files or branch, so Slice 3 could be planned against a nonexistent baseline.
- **Mitigation:** make baseline verification Step 0 and block coding until `slice/semantic-map-integration` is materially verified in a dedicated worktree.

### Risk 2 - Manifest remains non-authoritative
- **Risk:** if `generated_canonical_files` and `compiled_claim_ids` stay empty, closeout status can look mechanical while still being untrustworthy.
- **Mitigation:** explicitly include minimal manifest-contract repair in Slice 3 scope if the integration baseline still leaves those fields empty.

### Risk 3 - Status logic becomes hand-wavy instead of mechanical
- **Risk:** `yellow` especially can degrade into human judgment.
- **Mitigation:** encode deterministic classification in tests with explicit ordered predicates and blocking reasons.

### Risk 4 - Object edge coverage becomes gameable
- **Risk:** if the denominator is defined too loosely, `object_edge_coverage_pct` can look healthy while hiding discovery gaps.
- **Mitigation:** tie the denominator to canonical objects compiled for the target wave and document this as a quality metric, with a follow-up to seed expected-object denominators only if pilot evidence shows gaming risk.

### Risk 5 - Closeout logic mutates or rewrites accepted claims
- **Risk:** an implementation might "fix" accepted claim files during closeout generation, violating provenance.
- **Mitigation:** keep closeout checks read-only over claim artifacts; detect mutation and fail integrity instead of rewriting accepted claims.

### Risk 6 - Slice 3 scope expands into Slice 4 pilot work
- **Risk:** attempts to validate real first-wave discovery flows can turn this into an execution pilot.
- **Mitigation:** keep fixtures deterministic and synthetic enough for reporting semantics; defer live first-wave discovery execution to Slice 4.

## 5) Verification Steps

### Branch and baseline verification
```bash
git fetch --all --prune
git branch --list slice/semantic-map-integration
git worktree add .worktrees/slice-semantic-map-reporting-wave-closeout slice/semantic-map-integration
git -C .worktrees/slice-semantic-map-reporting-wave-closeout switch -c slice/semantic-map-reporting-wave-closeout
```

### Targeted contract runs during development
```bash
uv run pytest tests/contracts/test_legacy_semantic_map_reporting.py -v
uv run pytest tests/contracts/test_legacy_semantic_map_wave_closeout.py -v
```

### Targeted semantic-map suite before merge back to integration
```bash
uv run pytest tests/contracts/test_legacy_semantic_map_*.py -v
uv run pytest tests/integration/test_legacy_semantic_map_reporting_pipeline.py -v
```

### Integration-branch verification after merge
```bash
git switch slice/semantic-map-integration
git merge --no-ff slice/semantic-map-reporting-wave-closeout
uv run pytest tests/contracts/test_legacy_semantic_map_*.py tests/integration/test_legacy_semantic_map_reporting_pipeline.py -v
```

### Optional broader safety run if the semantic-map slice touches shared tooling contracts
```bash
uv run pytest -v
```

## 6) RALPLAN-DR Summary

### Principles
1. **Mechanical over narrative:** wave status must come from deterministic rules, not reviewer interpretation.
2. **Immutable provenance:** accepted claims are evidence, not mutable working files.
3. **Minimal contract repair:** fix only the upstream manifest/compiler gaps required to make Slice 3 trustworthy.
4. **Reserved surface discipline:** prefer the spec's existing `reports/current` and `reports/waves/<wave_id>` structure over introducing extra report sprawl.
5. **Slice isolation:** close Slice 3 on its own branch from `slice/semantic-map-integration`, then merge back deliberately.

### Top 3 drivers
1. Make the semantic-map wave mechanically classifiable as `red`, `yellow`, or `green`.
2. Preserve provenance and archiveability by keeping accepted claims immutable.
3. Produce closeout evidence that is credible enough to support later Slice 4 pilot work and eventual integration-branch acceptance.

### Options considered

#### Option A - Keep the spec's two reserved report files and place closeout/archive fields inside `integrity-status.json`
**Pros**
- Matches the spec's reserved tree exactly.
- Minimizes file proliferation and schema sprawl.
- Keeps consumers focused on one coverage artifact and one integrity/closeout artifact.

**Cons**
- `integrity-status.json` becomes broader and needs careful schema discipline.
- Closeout-specific readers must parse a mixed integrity plus closeout payload.

#### Option B - Introduce a third `closeout-status.json` file beside coverage and integrity reports
**Pros**
- Separates closeout/archive decisions from lower-level integrity checks.
- Easier to evolve closeout detail independently.

**Cons**
- Deviates from the spec's reserved report tree.
- Increases schema and file-surface complexity.
- Adds another artifact to current and per-wave report directories with limited incremental value for Slice 3.

#### Option C - Only compute current-wave status and defer per-wave snapshots to Slice 4
**Pros**
- Smaller immediate implementation surface.
- Simplifies report writing.

**Cons**
- Undercuts closeout traceability for archived waves.
- Conflicts with the spec's reserved per-wave report structure.
- Makes historical closeout review weaker exactly where immutability and archiveability matter.

### Chosen direction
Choose **Option A**.

It best fits the spec, keeps the surface area controlled, and still provides enough room to store closeout and archive-readiness evidence. Per-wave snapshot generation remains in scope because historical review is part of the point of closeout.

## 7) Pre-Mortem

### Scenario 1 - Slice merges with green reports that are mathematically wrong
- **How it happens:** thresholds are encoded incompletely, especially for `yellow`, and tests only assert happy paths.
- **Impact:** wave status appears reliable but misclassifies blocking conditions.
- **Prevention:** lock explicit red/yellow/green fixtures and ordered predicate tests before implementation.

### Scenario 2 - Closeout readiness is reported from stale or empty manifest data
- **How it happens:** Slice 3 trusts the existing manifest even though `generated_canonical_files` and `compiled_claim_ids` were never populated.
- **Impact:** closeout reports look complete while provenance is actually missing.
- **Prevention:** treat manifest-population repair as mandatory if baseline inspection confirms the gap.

### Scenario 3 - Team broadens Slice 3 into live discovery or wiki absorption execution
- **How it happens:** to prove reporting works, implementation starts mutating real wave content or durable wiki targets.
- **Impact:** slice scope balloons, merge risk rises, and provenance lines blur.
- **Prevention:** keep Slice 3 fixture-driven and contract-focused; defer live pilot execution to Slice 4.

## 8) Expanded Test Plan

### Unit
- `tests/contracts/test_legacy_semantic_map_reporting.py`
  - metric numerators and denominators
  - red/yellow/green classification predicates
  - age-by-wave calculation
  - stale candidate counting
- `tests/contracts/test_legacy_semantic_map_wave_closeout.py`
  - closeout-ready gating
  - archive-ready gating
  - immutable accepted-claim detection
  - blocking-reason ordering and completeness

### Integration
- `tests/integration/test_legacy_semantic_map_reporting_pipeline.py`
  - bootstrap/load seeded tree
  - compile accepted claims
  - write current reports
  - write per-wave reports
  - evaluate closeout and archive readiness
  - verify manifest/report alignment

### End-to-end slice verification
- branch creation from `slice/semantic-map-integration`
- targeted semantic-map contract suite on the slice branch
- merge to `slice/semantic-map-integration`
- rerun targeted semantic-map suite on integration branch
- optional full `uv run pytest -v` if shared tooling surfaces were touched

### Observability and artifact checks
- inspect generated `reports/current/coverage-status.json`
- inspect generated `reports/current/integrity-status.json`
- inspect generated `reports/waves/<wave_id>/...`
- inspect `manifest.json` for populated `generated_canonical_files` and `compiled_claim_ids`
- verify closeout failure explains blockers in a machine-readable `blocking_reasons` list

## 9) ADR Section

### Decision
Implement Slice 3 as a deterministic reporting and closeout layer under `scripts/legacy_semantic_map/`, using the spec's two reserved report files (`coverage-status.json` and `integrity-status.json`) for both current and per-wave outputs, and add only the minimum compiler/manifest refinements required to make closeout reporting trustworthy.

### Drivers
- Need mechanical `red` / `yellow` / `green` wave classification.
- Need immutable accepted claims for provenance and archive review.
- Need credible closeout evidence before Slice 4 pilot work can rely on this ledger.

### Alternatives considered
- Add a separate `closeout-status.json` file.
- Defer per-wave snapshots until Slice 4.
- Leave manifest gaps for a later cleanup slice.

### Why chosen
- The chosen design aligns most closely with the spec's reserved filesystem contract.
- It limits scope creep while still solving the actual closeout problem.
- It avoids a fake-mechanical solution that would rely on empty manifest data.

### Consequences
- `integrity-status.json` must carry a broader, carefully versioned schema.
- Slice 3 may need a small amount of retroactive baseline repair in `compiler.py` and manifest generation.
- Consumers of closeout readiness will have a stable per-wave historical record instead of only a current snapshot.

### Follow-ups
- If Slice 4 reveals that `object_edge_coverage_pct` is too easy to game, add a seeded expected-object denominator strategy in a later refinement.
- If closeout consumers become more complex, revisit whether a dedicated `closeout-status.json` file is warranted after the pilot.
- If all semantic-map waves are completed, archive or remove both the semantic-map subtree and `scripts/legacy_semantic_map/` tooling together.

## 10) Available-Agent-Types Roster And Follow-Up Staffing Guidance

### Available agent types relevant to this slice
- `architect` - contract boundaries, schema shape, tradeoff review
- `planner` - execution sequencing, risk control, merge choreography
- `executor` - implementation lane for reporting and closeout logic
- `test-engineer` - contract, integration, and regression test design
- `verifier` - completion evidence and claim validation
- `critic` - challenge ambiguous thresholds and hidden scope creep
- `code-reviewer` - post-implementation review
- `build-fixer` - resolve failing test or toolchain issues if they arise
- `writer` - documentation or plan maintenance if plan/docs drift occurs

### Ralph follow-up guidance
Use Ralph only if you want a persistent single-owner execution loop after this plan is approved.

**Recommended Ralph lane mix**
- `architect` - **high** reasoning
  - own contract decisions around report schema, manifest refinement boundaries, and closeout semantics
- `executor` - **high** reasoning
  - own `reporting.py`, `closeout.py`, and compiler/manifest refinements
- `test-engineer` - **medium** reasoning
  - own contract and integration tests for red/yellow/green, staleness, and immutability
- `verifier` - **high** reasoning
  - own merge-readiness evidence and post-merge integration verification

**Suggested Ralph use**
- Best when one operator wants a disciplined single loop across implementation, correction, and verification.
- Escalate to Ralph if Slice 3 reveals baseline drift that needs iterative reconciliation across compiler and manifest contracts.

### Team follow-up guidance
For actual execution, prefer team mode when you want durable parallel lanes and one dedicated verification lane.

**Recommended headcount:** 4 workers
- 2 delivery lanes
- 1 test lane
- 1 verification/merge-prep lane

**Role allocation guidance**
- **Lane 1 - reporting implementation**
  - effective role: `executor`
  - reasoning: **high**
  - owns `scripts/legacy_semantic_map/reporting.py`, related `models.py` updates, and report schemas
- **Lane 2 - closeout + manifest integration**
  - effective role: `executor`
  - reasoning: **high**
  - owns `scripts/legacy_semantic_map/closeout.py`, `compiler.py`, and any minimal `claims.py` or `bootstrap.py` refinements
- **Lane 3 - contract/integration tests**
  - effective role: `test-engineer`
  - reasoning: **medium**
  - owns `tests/contracts/test_legacy_semantic_map_reporting.py`, `tests/contracts/test_legacy_semantic_map_wave_closeout.py`, and `tests/integration/test_legacy_semantic_map_reporting_pipeline.py`
- **Lane 4 - verification and merge-prep audit**
  - effective role: `verifier`
  - reasoning: **high**
  - owns branch/baseline validation, evidence capture, post-merge semantic-map suite rerun, and merge checklist

**Closest-role fallback for tmux team runtime**
- If the team runtime is launched with one shared worker prompt such as `$team 4:executor`, keep all workers as `executor` workers but assign them the four lanes above explicitly in the leader dispatch.
- Preserve at least one worker as the verification owner; do not let all four lanes become delivery-only.

**Explicit launch hint**
```bash
$team 4:executor "Execute Slice 3 legacy semantic map reporting and wave closeout from slice/semantic-map-reporting-wave-closeout; keep one worker on tests and one on verification; do not merge to main"
```

**Alternative launch hint with environment-pinned reasoning args**
```bash
OMX_TEAM_WORKER_LAUNCH_ARGS="-c model_reasoning_effort=high" omx team 4:executor "Execute Slice 3 legacy semantic map reporting and wave closeout from slice/semantic-map-reporting-wave-closeout; keep one worker on tests and one on verification; do not merge to main"
```

**Team verification path**
1. Leader confirms the team is operating from a worktree branched off `slice/semantic-map-integration`.
2. Delivery lanes implement reporting and closeout logic.
3. Test lane proves red/yellow/green, staleness, and immutability with targeted tests.
4. Verification lane checks manifest/report consistency and ensures `generated_canonical_files` plus `compiled_claim_ids` are populated.
5. Leader waits for terminal team status, then merges the slice branch back into `slice/semantic-map-integration`.
6. Verification lane or leader reruns the full semantic-map targeted suite on `slice/semantic-map-integration`.
7. Only after that evidence is captured does the team shut down; no direct `main` merge is part of Slice 3 closeout.

## Proposed Merge Strategy

1. Keep repository root worktree clean on `main`.
2. Create or reuse a linked worktree for `slice/semantic-map-integration`.
3. Branch `slice/semantic-map-reporting-wave-closeout` from that integration baseline.
4. Complete Slice 3 and run targeted semantic-map verification on the slice branch.
5. Merge `slice/semantic-map-reporting-wave-closeout` back into `slice/semantic-map-integration` with an explicit slice-closure reason.
6. Rerun the targeted semantic-map suite on `slice/semantic-map-integration`.
7. Do not merge to `main` until the semantic-map package completes its later acceptance path.

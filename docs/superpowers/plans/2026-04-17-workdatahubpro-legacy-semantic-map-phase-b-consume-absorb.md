# WorkDataHubPro Legacy Semantic Map Phase B Consume/Absorb Deliberate Consensus Plan

> **Status:** Approved / checked in for execution
>
> **Intended checked-in plan path:** `docs/superpowers/plans/2026-04-17-workdatahubpro-legacy-semantic-map-phase-b-consume-absorb.md`
>
> **Planner save path:** `.omx/plans/2026-04-17-workdatahubpro-legacy-semantic-map-phase-b-consume-absorb.md`
>
> **Recommended narrow slice branch:** `slice/semantic-map-phase-b-absorb`
>
> **Integration baseline:** branch from `slice/semantic-map-integration` at verified head `a2872ab` in `.worktrees/slice-semantic-map-integration`; merge back into `slice/semantic-map-integration`, not `main`.

## 1) Requirements Summary

### Task intent
Create a narrow Phase B plan that clears the active wave's remaining closeout blockers by:
- consuming already-proven semantic-map findings into durable `docs/wiki-bi/` targets where durable deltas are actually needed
- normalizing candidate disposition state to the repo/design vocabulary
- updating wave metadata and regenerated report artifacts so the current wave can truthfully move past the two known blocker conditions

This Phase B is **blocker-clearing consume/absorb + disposition normalization**. It is **not** a mandate to force architectural closure of deferred Tier B runtime/governance decisions that the current durable pages already preserve honestly.

### Grounded facts
- Governing architecture and refactor inputs are already verified from:
  - `docs/superpowers/specs/2026-04-11-workdatahubpro-rebuild-architecture-draft.md`
  - `docs/superpowers/specs/2026-04-11-workdatahubpro-refactor-program.md`
  - `docs/superpowers/specs/2026-04-11-workdatahubpro-first-wave-legacy-coverage-matrix.md`
  - `docs/disciplines/implementation-slice-workflow.md`
  - `docs/disciplines/implementation-verification.md`
  - `docs/disciplines/git-workflow.md`
  - `.worktrees/slice-semantic-map-integration/docs/superpowers/specs/2026-04-16-workdatahub-legacy-semantic-map-design.md`
- Verified execution baseline is `.worktrees/slice-semantic-map-integration` on branch `slice/semantic-map-integration` at commit `a2872ab`.
- Active wave metadata in `.worktrees/slice-semantic-map-integration/docs/wiki-bi/_meta/legacy-semantic-map/waves/index.yaml` shows:
  - active wave `wave-2026-04-17-first-wave-pilot`
  - Tier A: `annuity_performance`, `annual_award`, `annual_loss`, `annuity_income`
  - Tier B: `customer_mdm`, `company_lookup_queue`, `reference_sync`
  - `durable_wiki_targets_accepted: false`
  - `findings_disposition_complete: false`
- Current reports are mechanically green but blocked from closeout:
  - `.worktrees/slice-semantic-map-integration/docs/wiki-bi/_meta/legacy-semantic-map/reports/current/coverage-status.json`
  - `.worktrees/slice-semantic-map-integration/docs/wiki-bi/_meta/legacy-semantic-map/reports/waves/wave-2026-04-17-first-wave-pilot/integrity-status.json`
- Verified closeout logic in `.worktrees/slice-semantic-map-integration/scripts/legacy_semantic_map/reporting.py` and `models.py` requires:
  - `closeout_ready=true` only when status is green, missing-claim checks pass, immutability and manifest conditions pass, and both wave booleans are true
  - `archive_ready=true` only when `closeout_ready=true`, `depends_on_active_wave_working_state=false`, and wave `status == "closed"`
- Current unresolved candidate files are:
  - `.worktrees/slice-semantic-map-integration/docs/wiki-bi/_meta/legacy-semantic-map/candidates/subsystem-candidates.yaml`
    - `cand-company-lookup-queue-publication-boundary`
    - `cand-customer-mdm-manual-runtime-boundary`
  - `.worktrees/slice-semantic-map-integration/docs/wiki-bi/_meta/legacy-semantic-map/candidates/object-candidates.yaml`
    - `cand-reference-sync-governance-bridge`
- Additional verified grounding for Phase B:
  - `company_lookup_queue`, `reference_sync`, and `customer-mdm` durable pages already preserve deferred runtime reality and must not be forced into false closure
  - integration-worktree tests live under `.worktrees/slice-semantic-map-integration/tests/...`
  - existing pilot regeneration entrypoint is `uv run python -m scripts.legacy_semantic_map.pilot --registry-root docs/wiki-bi/_meta/legacy-semantic-map` when run from the semantic-map worktree
- Durable wiki targets already exist for all required absorption areas under `.worktrees/slice-semantic-map-integration/docs/wiki-bi/`; Tier B object files already state they remain representative-only until durable absorption/disposition is accepted.

### Design-aligned disposition vocabulary
Phase B must bind narrative outcomes to the semantic-map and design vocabulary instead of inventing new closure language:
- **candidate status vocabulary:** `accepted`, `rejected`, `deferred`, `merged`
- **closeout rule vocabulary:** absorbed / deferred / retired

Required alignment:
- **absorbed** -> reflected in durable wiki and candidate metadata normalized to `accepted` or `merged`
- **deferred** -> explicitly preserved as deferred runtime/governance reality and candidate metadata normalized to `deferred`
- **retired** -> explicitly not carried forward and candidate metadata normalized to `rejected`

### In scope
- Write a checked-in Phase B plan under `docs/superpowers/plans/`
- Produce a **review-aid** delta mapping for active-wave findings to existing durable `docs/wiki-bi/` targets
- Absorb Tier A deltas where needed, including allowing `no durable edit needed` when current durable pages already fully absorb a finding
- Normalize disposition for:
  - `cand-company-lookup-queue-publication-boundary`
  - `cand-customer-mdm-manual-runtime-boundary`
  - `cand-reference-sync-governance-bridge`
- Update wave metadata and closeout evidence
- Regenerate registry/report artifacts through the existing pilot entrypoint and verify blocker clearance from the correct worktree

### Out of scope
- Redesigning Slice 1-4 tooling/contracts under `scripts/legacy_semantic_map/`
- Opening a new broad discovery wave
- Turning `docs/wiki-bi/_meta/legacy-semantic-map/` into a second durable knowledge layer
- Forcing Tier B deferred runtime decisions into `accepted` merely to obtain cleaner closure language

## 2) Branch Strategy Tradeoffs And Decision

### Option A - Work directly on `slice/semantic-map-integration`
**Pros**
- No branch handoff overhead
- Simplest ancestry

**Cons**
- Violates the requested narrow-slice isolation
- Makes closeout/doc/reporting changes harder to review separately from baseline integration work
- Increases risk of mutating the shared integration baseline before Phase B is accepted

### Option B - Branch from `main`
**Pros**
- Cleanest repository-default branch point

**Cons**
- Drops the verified semantic-map baseline at `a2872ab`
- Would require replaying or cherry-picking integration-only Slice 1-4 work
- Conflicts with the user's explicit baseline constraint

### Option C - Create a new narrow slice branch from `slice/semantic-map-integration@a2872ab` **(chosen)**
**Pros**
- Preserves the verified integration baseline and current green reporting state
- Isolates Phase B consume/absorb work into one reviewable slice
- Supports merge-back into `slice/semantic-map-integration` after validation without contaminating `main`

**Cons**
- Requires explicit branch cut and later merge-back discipline
- Any further integration-branch drift must be consciously rebased or merged

### Decision
Use `slice/semantic-map-phase-b-absorb`, cut from `.worktrees/slice-semantic-map-integration` at `a2872ab`, then merge back into `slice/semantic-map-integration` only after Phase B regeneration and closeout validation pass.

## 3) Acceptance Criteria

1. A checked-in plan exists at `docs/superpowers/plans/2026-04-17-workdatahubpro-legacy-semantic-map-phase-b-consume-absorb.md` and execution occurs from `slice/semantic-map-phase-b-absorb` branched from `slice/semantic-map-integration@a2872ab`.
2. Phase B includes a **claim/source-to-durable-target delta table** for all Tier A findings and the three named candidates; the table is explicitly a review aid only, not a third source of truth.
3. For each Tier A finding, the execution result is one of:
   - durable delta absorbed into existing durable pages, or
   - `no durable edit needed` because the current durable page already fully absorbs the finding.
4. The three current candidates are each normalized to semantic-map candidate status vocabulary: `accepted`, `rejected`, `deferred`, or `merged`, with closeout interpretation aligned to absorbed / deferred / retired.
5. Phase B does **not** require Tier B `company_lookup_queue`, `reference_sync`, or `customer-mdm` durable pages to be forced into false finality; truthful deferred runtime reality is allowed and must map to `deferred` where appropriate.
6. The authoritative post-execution state is visible in the combination of:
   - durable wiki pages under `.worktrees/slice-semantic-map-integration/docs/wiki-bi/`
   - candidate metadata under `.worktrees/slice-semantic-map-integration/docs/wiki-bi/_meta/legacy-semantic-map/candidates/`
   - wave metadata and regenerated report artifacts under `.worktrees/slice-semantic-map-integration/docs/wiki-bi/_meta/legacy-semantic-map/`
7. Wave metadata in `.worktrees/slice-semantic-map-integration/docs/wiki-bi/_meta/legacy-semantic-map/waves/index.yaml` is updated so `durable_wiki_targets_accepted` and `findings_disposition_complete` become `true` only if the underlying durable/candidate/report state supports that claim.
8. Verification is run from the correct derived worktree using the existing pilot entrypoint, and regenerated report artifacts remove the two known blockers without relying on tests alone.
9. Any remaining inability to archive is only due to conditions outside the two stated blockers, such as `status != closed` or `depends_on_active_wave_working_state=true`, and is documented rather than hidden.

## 4) Claim/Source-To-Durable-Target Delta Table (Review Aid Only)

> This table is a planning and review aid only. It is **not** authoritative post-execution truth. After execution, the authoritative state must live in updated durable wiki pages, candidate metadata, wave metadata, and regenerated report artifacts under `.worktrees/slice-semantic-map-integration/docs/wiki-bi/_meta/legacy-semantic-map/`.

| Area | Current semantic-map source / claim focus | Candidate or finding intent | Existing durable target(s) | Expected Phase B delta | Expected normalized disposition |
|---|---|---|---|---|---|
| `annuity_performance` | Tier A active-wave object/edge findings already linked to domain/contract/evidence pages | confirm whether current durable pages fully absorb accepted finding set | `docs/wiki-bi/domains/annuity-performance.md`; `docs/wiki-bi/standards/input-reality/annuity-performance-input-contract.md`; `docs/wiki-bi/standards/output-correctness/annuity-performance-output-contract.md`; `docs/wiki-bi/evidence/annuity-performance-field-processing-evidence.md` | targeted delta only; or `no durable edit needed` if already fully absorbed | absorbed via durable page state |
| `annual_award` | Tier A active-wave object/edge findings | same | `docs/wiki-bi/domains/annual-award.md`; `docs/wiki-bi/standards/input-reality/annual-award-input-contract.md`; `docs/wiki-bi/standards/output-correctness/annual-award-output-contract.md`; `docs/wiki-bi/evidence/annual-award-field-processing-evidence.md` | targeted delta only; or `no durable edit needed` | absorbed via durable page state |
| `annual_loss` | Tier A active-wave object/edge findings | same | `docs/wiki-bi/domains/annual-loss.md`; `docs/wiki-bi/standards/input-reality/annual-loss-input-contract.md`; `docs/wiki-bi/standards/output-correctness/annual-loss-output-contract.md`; `docs/wiki-bi/evidence/annual-loss-field-processing-evidence.md` | targeted delta only; or `no durable edit needed` | absorbed via durable page state |
| `annuity_income` | Tier A active-wave object/edge findings | same | `docs/wiki-bi/domains/annuity-income.md`; `docs/wiki-bi/standards/input-reality/annuity-income-input-contract.md`; `docs/wiki-bi/standards/output-correctness/annuity-income-output-contract.md`; `docs/wiki-bi/evidence/annuity-income-field-processing-evidence.md` | targeted delta only; or `no durable edit needed` | absorbed via durable page state |
| `cand-company-lookup-queue-publication-boundary` | `candidates/subsystem-candidates.yaml` | publication boundary may remain runtime-truthfully deferred | `docs/wiki-bi/surfaces/company-lookup-queue.md`; `docs/wiki-bi/evidence/operator-and-surface-evidence.md` | only edit if durable clarification is missing; otherwise normalize metadata to match existing deferred/absorbed reality | `accepted`, `merged`, `deferred`, or `rejected` depending on actual durable/candidate outcome |
| `cand-customer-mdm-manual-runtime-boundary` | `candidates/subsystem-candidates.yaml` | manual/runtime boundary may remain deferred | `docs/wiki-bi/surfaces/customer-mdm-commands.md`; `docs/wiki-bi/evidence/customer-mdm-lifecycle-evidence.md` | only edit if durable clarification is missing; otherwise normalize metadata to existing deferred runtime reality | `accepted`, `merged`, `deferred`, or `rejected` |
| `cand-reference-sync-governance-bridge` | `candidates/object-candidates.yaml` | governance bridge may remain deferred | `docs/wiki-bi/surfaces/reference-sync.md`; `docs/wiki-bi/evidence/reference-and-backfill-evidence.md` | only edit if durable clarification is missing; otherwise normalize metadata to existing deferred runtime reality | `accepted`, `merged`, `deferred`, or `rejected` |

## 5) Implementation Steps

### Step 1 - Cut the Phase B slice and check in the planning contract
**Primary paths**
- New checked-in plan: `docs/superpowers/plans/2026-04-17-workdatahubpro-legacy-semantic-map-phase-b-consume-absorb.md`
- Baseline worktree: `.worktrees/slice-semantic-map-integration`

**Actions**
- Create `slice/semantic-map-phase-b-absorb` from verified baseline `a2872ab`.
- Check in the Phase B plan with explicit scope, delta-table review aid, disposition vocabulary, closeout obligations, and regeneration commands.
- Record that Phase B is a blocker-clearing consume/absorb follow-on to the active wave, not a new discovery wave and not a mandate to settle all Tier B architectural questions.

**Acceptance checkpoint**
- Branch ancestry is explicit.
- The checked-in plan reflects blocker-clearing and disposition normalization rather than forced closure.

### Step 2 - Build the delta review aid against current durable reality
**Primary paths**
- `.worktrees/slice-semantic-map-integration/docs/wiki-bi/_meta/legacy-semantic-map/objects/*.yaml`
- `.worktrees/slice-semantic-map-integration/docs/wiki-bi/_meta/legacy-semantic-map/edges/*.yaml`
- `.worktrees/slice-semantic-map-integration/docs/wiki-bi/_meta/legacy-semantic-map/candidates/*.yaml`
- Durable targets under `.worktrees/slice-semantic-map-integration/docs/wiki-bi/`

**Actions**
- For each Tier A finding, compare active-wave claim/source reality against the already-existing durable target pages.
- Mark each row as either:
  - targeted durable delta needed, or
  - `no durable edit needed` because the durable page already fully absorbs the finding.
- For each named candidate, determine whether current durable pages already encode absorbed/deferred/retired reality and only schedule durable edits where a real clarity gap remains.
- Keep the table explicitly secondary to the repo artifacts it summarizes.

**Acceptance checkpoint**
- No in-scope finding lacks a planned delta/no-delta decision.
- The plan does not become a third truth source.

### Step 3 - Apply only the needed Tier A durable deltas
**Primary paths**
- `docs/wiki-bi/domains/annuity-performance.md`
- `docs/wiki-bi/domains/annual-award.md`
- `docs/wiki-bi/domains/annual-loss.md`
- `docs/wiki-bi/domains/annuity-income.md`
- corresponding `docs/wiki-bi/standards/input-reality/*`, `docs/wiki-bi/standards/output-correctness/*`, `docs/wiki-bi/evidence/*`

**Actions**
- Update only the specific durable pages whose current content does not yet fully absorb the accepted Tier A finding set.
- Preserve the durable wiki role as synthesis, not a restatement of semantic-map internals.
- Where the durable page already fully absorbs the finding, make no content change and record that the finding is already absorbed.

**Acceptance checkpoint**
- Tier A work is explicitly delta-based rather than blanket page churn.
- Every Tier A finding ends in either absorbed-by-delta or already-absorbed/no-edit-needed state.

### Step 4 - Normalize candidate disposition without forcing false Tier B closure
**Primary paths**
- `.worktrees/slice-semantic-map-integration/docs/wiki-bi/_meta/legacy-semantic-map/candidates/subsystem-candidates.yaml`
- `.worktrees/slice-semantic-map-integration/docs/wiki-bi/_meta/legacy-semantic-map/candidates/object-candidates.yaml`
- `docs/wiki-bi/surfaces/company-lookup-queue.md`
- `docs/wiki-bi/surfaces/customer-mdm-commands.md`
- `docs/wiki-bi/surfaces/reference-sync.md`
- `docs/wiki-bi/evidence/operator-and-surface-evidence.md`
- `docs/wiki-bi/evidence/customer-mdm-lifecycle-evidence.md`
- `docs/wiki-bi/evidence/reference-and-backfill-evidence.md`

**Actions**
- For each named candidate, select the truthful semantic-map status: `accepted`, `rejected`, `deferred`, or `merged`.
- Align that status to the design closeout interpretation: absorbed / deferred / retired.
- Preserve truthful deferred runtime/governance reality where the existing durable pages already do so; do not promote such cases to `accepted` unless the durable and candidate evidence really support absorption.
- Make durable page edits only where needed to remove ambiguity between durable narrative and candidate metadata.

**Acceptance checkpoint**
- None of the three named candidates remain in ambiguous limbo.
- Deferred Tier B reality is allowed and explicit rather than treated as planning failure.

### Step 5 - Update wave metadata and closeout evidence from the normalized state
**Primary paths**
- `.worktrees/slice-semantic-map-integration/docs/wiki-bi/_meta/legacy-semantic-map/waves/index.yaml`
- `.worktrees/slice-semantic-map-integration/docs/wiki-bi/_meta/legacy-semantic-map/reports/waves/wave-2026-04-17-first-wave-pilot/`
- related closeout/readme notes under `.worktrees/slice-semantic-map-integration/docs/wiki-bi/_meta/legacy-semantic-map/` if needed

**Actions**
- Flip `durable_wiki_targets_accepted` only after Tier A absorbed/already-absorbed review and necessary durable deltas are complete.
- Flip `findings_disposition_complete` only after each named candidate is normalized to `accepted`, `rejected`, `deferred`, or `merged` and the durable/candidate evidence no longer conflicts.
- Add or refresh closeout evidence notes only where reviewer traceability is otherwise weak.

**Acceptance checkpoint**
- Wave booleans follow the normalized artifact state; they do not lead it.
- Closeout evidence is sufficient to explain blocker clearance to a reviewer without relying on the plan text.

### Step 6 - Regenerate through the existing pilot entrypoint and verify from the correct worktree
**Primary paths**
- `.worktrees/slice-semantic-map-integration/scripts/legacy_semantic_map/pilot.py`
- `.worktrees/slice-semantic-map-integration/docs/wiki-bi/_meta/legacy-semantic-map/reports/current/coverage-status.json`
- `.worktrees/slice-semantic-map-integration/docs/wiki-bi/_meta/legacy-semantic-map/reports/waves/wave-2026-04-17-first-wave-pilot/integrity-status.json`
- `.worktrees/slice-semantic-map-integration/tests/...`

**Actions**
- Run regeneration from the derived semantic-map worktree on the Phase B slice branch using the existing pilot entrypoint.
- Inspect the regenerated registry/report artifacts first.
- Then run targeted contract/integration tests from the same derived worktree as regression support, not as a substitute for regeneration.
- If `archive_ready` remains false, document the exact remaining cause and keep Phase B scoped to blocker-clearing completion.

**Acceptance checkpoint**
- The two known blockers disappear in regenerated outputs.
- Verification evidence is anchored to the correct worktree and actual regenerated artifacts.

## 6) Risks And Mitigations

| Risk | Why it matters here | Mitigation |
|---|---|---|
| Premature closure by metadata toggle | The current blockers are booleans; it is easy to flip them before artifacts support them | Gate booleans behind durable-page review + candidate normalization + regenerated report inspection |
| False finality on Tier B runtime reality | `company_lookup_queue`, `reference_sync`, and `customer-mdm` durable pages already preserve deferred truth | Treat `deferred` as first-class; require justification before any promotion to `accepted` or `merged` |
| Wrong-workspace verification | Running commands from repo root or wrong checkout can validate stale or unrelated artifacts | Require all regeneration and targeted tests from the derived worktree branch created off `.worktrees/slice-semantic-map-integration` |
| Third-truth-source drift | The plan's mapping table could diverge from durable pages/candidate metadata/report artifacts | Mark the table as review-only and require final truth to live only in durable pages + candidate metadata + wave/report artifacts |
| Blanket durable-page churn | Reviewing all Tier A pages without delta discipline risks noise and hard-to-audit edits | Use claim/source-to-durable-target delta review and allow `no durable edit needed` |
| Closeout/archive confusion | Clearing the two blockers may still not satisfy `archive_ready` | Explicitly verify and report `closeout_ready` vs `archive_ready` separately per `reporting.py` / `models.py` |

## 7) Verification Steps

### Branch setup from the verified integration worktree
```powershell
git -C .worktrees/slice-semantic-map-integration status -sb
git -C .worktrees/slice-semantic-map-integration switch -c slice/semantic-map-phase-b-absorb
```

### Regenerate the registry/report artifacts from the correct worktree
```powershell
cd .worktrees/slice-semantic-map-integration
uv run python -m scripts.legacy_semantic_map.pilot --registry-root docs/wiki-bi/_meta/legacy-semantic-map
```

### Inspect regenerated artifacts first
```powershell
Get-Content .worktrees/slice-semantic-map-integration/docs/wiki-bi/_meta/legacy-semantic-map/reports/current/coverage-status.json
Get-Content .worktrees/slice-semantic-map-integration/docs/wiki-bi/_meta/legacy-semantic-map/reports/waves/wave-2026-04-17-first-wave-pilot/integrity-status.json
rg -n "cand-company-lookup-queue-publication-boundary|cand-customer-mdm-manual-runtime-boundary|cand-reference-sync-governance-bridge" .worktrees/slice-semantic-map-integration/docs/wiki-bi/_meta/legacy-semantic-map
```

### Run targeted regression tests from the same worktree
```powershell
cd .worktrees/slice-semantic-map-integration
uv run pytest tests/contracts/test_legacy_semantic_map_reporting.py -v
uv run pytest tests/contracts/test_legacy_semantic_map_wave_closeout.py -v
uv run pytest tests/integration/test_legacy_semantic_map_reporting_pipeline.py -v
```

### Manual artifact review gates
- Inspect `.worktrees/slice-semantic-map-integration/docs/wiki-bi/_meta/legacy-semantic-map/waves/index.yaml` for truthful blocker clearance.
- Inspect updated durable pages under `.worktrees/slice-semantic-map-integration/docs/wiki-bi/domains/`, `.../standards/`, `.../surfaces/`, and `.../evidence/` to confirm only required deltas were applied.
- Confirm the post-execution truth is readable from durable pages + candidate metadata + wave/report artifacts without consulting the plan.
- Confirm any remaining `archive_ready=false` cause is explicitly documented and is outside the two cleared blockers.

## 8) Executable Checklist

- [ ] Create branch `slice/semantic-map-phase-b-absorb` from `.worktrees/slice-semantic-map-integration` at `a2872ab`
- [ ] Check in `docs/superpowers/plans/2026-04-17-workdatahubpro-legacy-semantic-map-phase-b-consume-absorb.md`
- [ ] Build the claim/source-to-durable-target delta review aid for four Tier A surfaces and three named candidates
- [ ] For each Tier A finding, mark `durable delta needed` or `no durable edit needed`
- [ ] Apply only the needed durable deltas for `annuity_performance`
- [ ] Apply only the needed durable deltas for `annual_award`
- [ ] Apply only the needed durable deltas for `annual_loss`
- [ ] Apply only the needed durable deltas for `annuity_income`
- [ ] Normalize `cand-company-lookup-queue-publication-boundary` to `accepted`, `rejected`, `deferred`, or `merged`
- [ ] Normalize `cand-customer-mdm-manual-runtime-boundary` to `accepted`, `rejected`, `deferred`, or `merged`
- [ ] Normalize `cand-reference-sync-governance-bridge` to `accepted`, `rejected`, `deferred`, or `merged`
- [ ] Update `waves/index.yaml` booleans only after durable/candidate state supports them
- [ ] Regenerate via `uv run python -m scripts.legacy_semantic_map.pilot --registry-root docs/wiki-bi/_meta/legacy-semantic-map` from `.worktrees/slice-semantic-map-integration`
- [ ] Inspect regenerated `coverage-status.json` and `integrity-status.json` for blocker removal
- [ ] Run targeted tests from `.worktrees/slice-semantic-map-integration/tests/...`
- [ ] Document any remaining `archive_ready=false` cause if blocker clearance is complete but archival closure is still pending
- [ ] Merge `slice/semantic-map-phase-b-absorb` back into `slice/semantic-map-integration` after verification

## 9) RALPLAN-DR Deliberate Summary

### Principles
1. Preserve the semantic map as a discovery ledger and the durable wiki as the accepted knowledge layer.
2. Clear closeout blockers through artifact-backed absorb/disposition normalization, not metadata toggles.
3. Keep Phase B narrow: consume the active wave and normalize its disposition state; do not force unresolved Tier B runtime reality into false closure.
4. Prefer existing durable targets and delta edits over new documentation sprawl or blanket page churn.
5. Verify from the correct derived worktree using real regeneration paths, not test-only proxies.

### Top drivers
1. Clear the two verified closeout blockers in `waves/index.yaml` and regenerated integrity output.
2. Normalize active-wave findings into durable wiki pages and candidate metadata without creating a third truth source.
3. Keep the work mergeable as one narrow slice on top of `slice/semantic-map-integration@a2872ab`.

### Viable options

#### Option 1 - Narrow blocker-clearing consume/absorb + disposition-normalization slice from integration baseline **(chosen)**
- Apply only needed Tier A deltas, allow already-absorbed/no-edit-needed outcomes, normalize Tier B candidates to accepted/rejected/deferred/merged, update wave metadata, regenerate artifacts.
- Best fit for the current blocker state and the existing deferred-runtime durable pages.

#### Option 2 - Metadata-first closure patch
- Flip booleans and make minimal edits without disciplined delta review or candidate normalization.
- Rejected because it invites premature closure and contradicts the verified closeout logic in `reporting.py` / `models.py`.

#### Option 3 - Force Tier B runtime decisions to `accepted`
- Rewrite `company_lookup_queue`, `reference_sync`, and `customer-mdm` durable pages toward finality so every candidate looks resolved as absorbed.
- Rejected because current durable pages already preserve deferred runtime reality and false closure would lower fidelity.

### Pre-mortem
1. **Premature closure:** wave booleans are flipped before durable pages and candidate metadata actually support blocker clearance.
2. **Wrong-worktree proof:** regeneration or tests run outside `.worktrees/slice-semantic-map-integration`, producing misleading green results.
3. **Third-truth drift:** the plan's review table says one thing while durable pages/candidate metadata/report artifacts say another.

### Expanded test plan
- **Regeneration first:** run `uv run python -m scripts.legacy_semantic_map.pilot --registry-root docs/wiki-bi/_meta/legacy-semantic-map` from `.worktrees/slice-semantic-map-integration` and inspect regenerated registry/report artifacts.
- **Contract regression:** rerun `.worktrees/slice-semantic-map-integration/tests/contracts/test_legacy_semantic_map_reporting.py` and `.../test_legacy_semantic_map_wave_closeout.py`.
- **Integration regression:** rerun `.worktrees/slice-semantic-map-integration/tests/integration/test_legacy_semantic_map_reporting_pipeline.py`.
- **Observability:** inspect `waves/index.yaml`, candidate files, durable pages, `coverage-status.json`, and `integrity-status.json` together to confirm blocker clearance and any remaining non-archive condition.

## 10) ADR

### Decision
Execute Phase B as a narrow blocker-clearing consume/absorb + disposition-normalization slice on branch `slice/semantic-map-phase-b-absorb` from `slice/semantic-map-integration@a2872ab`, with the checked-in plan at `docs/superpowers/plans/2026-04-17-workdatahubpro-legacy-semantic-map-phase-b-consume-absorb.md`.

### Drivers
- The active wave is already mechanically green; only durable-target acceptance and findings disposition block closeout.
- Durable targets already exist for Tier A and the three candidate-related Tier B areas.
- Tier B durable pages already preserve deferred runtime reality and should not be forced into false architectural closure.
- The user explicitly requires a narrow new slice branch, not `main` and not the integration branch itself.

### Alternatives considered
- Edit `slice/semantic-map-integration` directly.
- Branch from `main`.
- Use metadata-only closure.
- Force Tier B deferred runtime/governance cases into absorbed/final form.

### Why chosen
- It preserves the verified baseline, keeps review scope tight, and directly addresses the only two known closeout blockers while respecting existing deferred-runtime truth.

### Consequences
- Reviewers must validate three artifact surfaces together: durable pages, candidate metadata, and wave/report artifacts.
- Some Tier B outcomes may correctly remain `deferred`; Phase B success does not require architectural closure of those runtime decisions.
- A later archive/closure micro-slice may still be needed if wave status/working-state conditions remain after blocker clearance.

### Follow-ups
- If `archive_ready` remains false for non-blocker reasons, open a separate archive/closure micro-slice rather than enlarging Phase B.
- If any Tier A finding is already fully absorbed, preserve the no-edit-needed result instead of manufacturing churn.
- If any candidate remains deferred, ensure the durable page and candidate metadata say so consistently, then treat that as a valid closed Phase B outcome rather than a defect.

## 11) Proposed Checked-In Plan Document Structure

1. Title + status + target branch/baseline
2. Requirements Summary
3. Branch Strategy Decision
4. Claim/source-to-durable-target delta table (review aid only)
5. Acceptance Criteria
6. Implementation Steps
7. Risks / Mitigations
8. Verification Steps
9. Executable Checklist
10. RALPLAN-DR Deliberate Summary
11. ADR


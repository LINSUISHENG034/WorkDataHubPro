# WorkDataHubPro Legacy Semantic Map Key Semantics Governance Consensus Plan

> **Status:** Approved
>
> **Source spec:** `.omx/specs/deep-interview-legacy-semantic-map-key-semantics.md`
>
> **Intended checked-in plan path:** `docs/superpowers/plans/2026-04-18-workdatahubpro-legacy-semantic-map-key-semantics-governance.md`
>
> **Planner save path:** `.omx/plans/2026-04-18-workdatahubpro-legacy-semantic-map-key-semantics-governance.md`
>
> **Recommended narrow slice branch:** `slice/semantic-map-key-semantics-governance`
>
> **Integration baseline:** branch from `slice/semantic-map-integration` at verified head `a2e96a0`; merge back into `slice/semantic-map-integration`, not `main`.

## 1) Requirements Summary

### Task intent
Convert the current semantic-governance wave from a permissive semantic compilation pass into a proposal-grade semantic governance workflow that can:

- keep discovery broad and execution-first
- promote only business-meaningful semantic objects
- preserve runtime carriers as evidence instead of semantic truth
- treat semantic non-equivalence as a first-class output
- emit governance implications for slice admission, defer, retire, and durable wiki absorption
- validate semantic proposals in temporary registry copies before any shared-truth promotion

This work is not about reopening the whole repository or creating more semantic nodes by breadth alone. It is about hardening promotion discipline and proposal semantics around the already-admitted CT-018 lane.

### Grounded facts

- The rebuild governance baseline requires slice admission and retirement work to remain governed by the architecture blueprint, the refactor program, and the coverage matrix, not by local tool state alone.
- The refactor program already identifies semantic-map follow-on work as CT-018 and frames the open question as how semantic discovery should compile into semantic-first outputs that align to business semantics and durable wiki targets.
- The semantic-map design already establishes execution-first discovery, semantic-first compilation, main-thread canonical management, and wave-scoped reporting under `docs/wiki-bi/_meta/legacy-semantic-map/`.
- The semantic-map subtree guidance explicitly forbids top-down key-semantic checklisting as the discovery driver and requires any key semantic inventory to be a derived view from accepted execution-first findings.
- The current registry and scripts already contain:
  - an active successor wave `wave-2026-04-17-semantic-governance-reframe`
  - compiled semantic nodes under `docs/wiki-bi/_meta/legacy-semantic-map/semantic/`
  - additive semantic discovery/readiness reports under `docs/wiki-bi/_meta/legacy-semantic-map/reports/waves/wave-2026-04-17-semantic-governance-reframe/`
  - compiler/reporting entrypoints under `scripts/legacy_semantic_map/`
- The current compiler/reporting implementation is still too permissive for the new spec:
  - `ClaimSemanticFindingRecord` captures source refs, durable targets, and open questions, but not contradiction accounting, proxy-usage explanation, downstream consequence evidence, semantic-object vs runtime-carrier separation, or governance implications.
  - semantic maturity currently becomes `consumption-candidate` whenever a finding has durable target pages and no open questions.
  - reporting can show readiness and maturity counts, but it cannot explain why a proposal is blocked, contested, or governance-relevant in the way the direct spec now requires.
- Existing compiled example semantics already prove the customer-status family is the right seed set for this follow-on:
  - `sem-rule-is-new-definition`
  - `sem-non-equivalence-customer-type-vs-is-new`
  - `sem-non-equivalence-customer-master-vs-status`

### In scope

- Add explicit semantic-promotion gates and recommendation statuses to the semantic claim/compiler/reporting flow.
- Distinguish semantic objects from runtime carriers and witness surfaces in machine-readable artifacts.
- Add contradiction-accounting and proxy-usage explanation to semantic proposals.
- Add governance-implication fields for:
  - slice admission
  - defer candidates
  - retire candidates
  - durable wiki absorption implications
- Produce proposal-grade outputs that can say `recommended stable canonical`, `recommended contested`, or `claim-level only` without pretending to finalize shared governance truth.
- Validate the new rules against the `is_new` / customer-type non-equivalence family and at least one additional rule/non-equivalence pair in temporary registry copies plus checked-in regression tests.

### Out of scope

- reopening broad first-wave discovery or replacing execution-first discovery with a top-down semantic checklist
- redesigning the entire semantic-map package structure or moving it out of `docs/wiki-bi/_meta/legacy-semantic-map/`
- treating runtime carriers such as CLI names, hook order, YAML shape, SQL shape, or operator commands as canonical semantic objects by default
- directly mutating refactor-program states, coverage-matrix states, or durable wiki truth as part of proposal compilation
- merging semantic-map integration work directly to `main`

## 2) Branch Strategy Tradeoffs And Decision

### Option A - Tighten only the review guidance and keep the current compiler logic
**Pros**
- Smallest patch surface
- Minimal regression risk

**Cons**
- Leaves promotion discipline manual and unverified
- Cannot express contested-vs-stable recommendations mechanically
- Does not satisfy the direct spec's gates or governance-implication requirements

### Option B - Introduce a separate proposal registry tree and stop compiling into `semantic/`
**Pros**
- Strongest proposal-vs-final boundary
- Makes it visually obvious that proposal output is not final shared truth

**Cons**
- Larger contract break across compiler, reporting, tests, and existing semantic outputs
- Risks duplicating the current semantic layer during CT-018 rather than extending it additively
- Harder to land as a narrow follow-on slice

### Option C - Keep the current semantic registry paths, but make the compiled nodes explicitly recommendation-grade and gate-driven **(chosen)**
**Pros**
- Preserves the current CT-018 registry/reporting surface and wave structure
- Lets the compiler add missing semantic-governance rigor without a path-level rewrite
- Keeps the follow-on narrow and additive while still enforcing proposal-vs-final wording

**Cons**
- Requires careful naming so reviewers do not mistake recommendation-grade outputs for finalized governance truth
- Needs stronger docs/report language to offset the existing `semantic/` path's canonical-sounding name

### Decision
Execute a narrow additive follow-on on top of `slice/semantic-map-integration@a2e96a0`. Keep the current semantic registry paths, preserve current top-level CT-018 semantic/report keys, and add one exact nested `proposal_governance` block so compiled semantic outputs become gate-driven recommendation artifacts rather than permissive quasi-final canon.

## 3) Acceptance Criteria

1. A checked-in plan exists at `docs/superpowers/plans/2026-04-18-workdatahubpro-legacy-semantic-map-key-semantics-governance.md`, and execution occurs on `slice/semantic-map-key-semantics-governance` branched from `slice/semantic-map-integration@a2e96a0`.
2. Semantic claims can express, at minimum:
   - authoritative semantic sources
   - downstream consequence witnesses
   - proxy-usage evidence
   - contradiction-accounting status
   - governance implications
   - recommendation status: `recommended_stable_canonical`, `recommended_contested`, or `claim_level_only`
3. Compiled semantic outputs explicitly distinguish:
   - semantic objects and rules
   - runtime carriers or witness surfaces
   - non-equivalent objects
4. The compiler enforces the direct spec's gates so a semantic node cannot become `recommended_stable_canonical` unless:
   - an authority gate passes
   - a downstream consequence gate passes
   - contradiction accounting is resolved
   - no open high-priority governance question remains
5. The `is_new` / `customer_type=新客` family is compiled through the new workflow and proves:
   - one semantic rule
   - one semantic non-equivalence
   - contradiction/proxy accounting
   - governance implications
6. Reporting adds proposal-grade visibility without replacing existing coverage/integrity contracts:
   - proposal recommendation counts
   - contested proposal IDs
   - blocked-by-gate reasons
   - governance-implication summaries
   - unresolved non-equivalence/proxy-conflict blockers
7. Temporary-registry validation is part of the plan's required proof, and the verified loop confirms repeated compile/report runs stabilize before any checked-in promotion is claimed.
8. No part of the implementation automatically finalizes:
   - shared canonical truth
   - matrix/refactor-program status
   - durable absorption closure
   - retire/defer/admit decisions
9. One exact additive nested block name and schema is used consistently in claim artifacts, compiled semantic outputs, and tests:
   - block name: `proposal_governance`
   - required fields:
     - `recommendation_status`
     - `semantic_scope_type`
     - `authority_gate_passed`
     - `downstream_consequence_gate_passed`
     - `contradiction_accounting_status`
     - `contradiction_accounting_notes`
     - `proxy_usage_refs`
     - `downstream_consequence_refs`
     - `related_runtime_carriers`
     - `high_priority_governance_questions`
     - `gate_blockers`
     - `governance_implications`
10. The plan defines and tests the deterministic compatibility mapping from `proposal_governance.recommendation_status` into the existing top-level fields `semantic_maturity_level`, `consumption_readiness_status`, and `blocked_by`.

## 3A) Additive Schema Freeze

Use one exact nested block name in both claim fixtures and compiled semantic outputs:

```yaml
proposal_governance:
  recommendation_status: recommended_stable_canonical | recommended_contested | claim_level_only
  semantic_scope_type: semantic_object | runtime_carrier | witness_surface
  authority_gate_passed: true | false
  downstream_consequence_gate_passed: true | false
  contradiction_accounting_status: explained_operational_shortcut | explained_historical_drift | explained_scope_limited_alias | real_contradiction | unresolved
  contradiction_accounting_notes: []
  proxy_usage_refs: []
  downstream_consequence_refs: []
  related_runtime_carriers: []
  high_priority_governance_questions: []
  gate_blockers: []
  governance_implications:
    slice_admission:
      summary: ""
      affected_surfaces: []
      blocked_by: []
    defer_candidates:
      summary: ""
      affected_surfaces: []
      blocked_by: []
    retire_candidates:
      summary: ""
      affected_surfaces: []
      blocked_by: []
    durable_wiki_absorption:
      summary: ""
      target_pages: []
      blocked_by: []
```

This block is additive. Existing top-level semantic fields remain in place.

## 3B) Compatibility Mapping

Use this deterministic mapping from `proposal_governance` into the current top-level fields and report aggregates:

| Nested result | `semantic_maturity_level` | `consumption_readiness_status` | `blocked_by` | Report treatment |
|---|---|---|---|---|
| `recommended_stable_canonical` with durable targets and no blockers | `consumption-candidate` | `reviewable` | `[]` | count as recommendation-stable and handoff-ready |
| `recommended_stable_canonical` without durable targets | `inferred` | `discovery-only` | `[]` | count as recommendation-stable but not handoff-ready |
| `recommended_contested` | `contested` | `blocked` | copy `gate_blockers` | count as contested; include in blocked and contested report lists |
| `claim_level_only` with multiple distinct source refs | `inferred` | `discovery-only` | copy `gate_blockers` | count as claim-level only |
| `claim_level_only` with one distinct source ref | `observed` | `discovery-only` | copy `gate_blockers` | count as claim-level only |

If `contradiction_accounting_status` is `real_contradiction` or `unresolved`, or if `high_priority_governance_questions` is non-empty, the finding must not map to `recommended_stable_canonical`.
For this table, `multiple distinct source refs` means the deduplicated union of `primary_source_refs` and `supporting_source_refs`.

## 4) Implementation Steps

### Step 1 - Check in the governing plan and restate the proposal-vs-final boundary
**Primary paths**
- New plan: `docs/superpowers/plans/2026-04-18-workdatahubpro-legacy-semantic-map-key-semantics-governance.md`
- Docs boundary surfaces:
  - `docs/wiki-bi/_meta/legacy-semantic-map/README.md`
  - `docs/wiki-bi/_meta/legacy-semantic-map/AGENTS.md`
- Optional CT-018 plan note update:
  - `docs/superpowers/plans/2026-04-18-workdatahubpro-semantic-map-agent-governance-reframe.md`

**Actions**
- Check in the plan and state clearly that this slice is a CT-018 follow-on for promotion discipline, not a new discovery wave.
- Update semantic-map local guidance only where needed so reviewers can see that compiled semantic outputs are recommendation-grade proposal artifacts until main-thread acceptance.
- If the broader CT-018 plan remains the umbrella plan, add a short note or follow-on reference instead of replacing it.
- Treat the checked-in plan under `docs/superpowers/plans/` as the execution gate. Do not start implementation from the local `.omx` draft alone.

**Acceptance checkpoint**
- The plan and local guidance tell one story: proposal-making is automatic enough to review, but final governance truth is still main-thread-controlled.

### Step 2 - Extend semantic claim schema for promotion gates, governance implications, and the current orchestration source path
**Primary paths**
- `scripts/legacy_semantic_map/claims.py`
- `scripts/legacy_semantic_map/models.py`
- `scripts/legacy_semantic_map/orchestrate_wave.py`
- Claim fixtures under:
  - `docs/wiki-bi/_meta/legacy-semantic-map/claims/wave-2026-04-17-customer-status-semantic-pilot/semantic/`
  - `docs/wiki-bi/_meta/legacy-semantic-map/claims/wave-2026-04-17-semantic-governance-reframe/semantic/`

**Actions**
- Extend `ClaimSemanticFindingRecord` and supporting vocabularies so a semantic proposal can capture:
  - one exact additive nested block named `proposal_governance`
  - the exact required fields defined in `3A`
- Keep the new fields additive and compatible with the current claim workflow.
- Preserve the current source-wave-to-successor-wave orchestration contract explicitly:
  - either extend the closed source-wave semantic pilot claims that `build_successor_wave_claims()` clones, or
  - change orchestration in the same slice so successor-wave claims become the maintained source of truth
- For this slice, the required path is to extend the existing source-wave claim fixtures and ensure the orchestrator preserves the new fields into successor-wave claims.
- Update or add claim fixtures so the seed customer-status family exercises the new fields instead of leaving them empty.

**Acceptance checkpoint**
- A semantic proposal can carry enough structure to explain why it is stable, contested, or claim-level without relying on prose-only reviewer inference.
- The exact same `proposal_governance` block name and required fields exist in both claim artifacts and compiled semantic outputs.

### Step 3 - Add a dedicated semantic-governance gate evaluator in the compiler layer
**Primary paths**
- `scripts/legacy_semantic_map/compiler.py`
- New helper if needed:
  - `scripts/legacy_semantic_map/semantic_governance.py`
- Potential supporting vocab in `scripts/legacy_semantic_map/models.py`

**Actions**
- Implement a gate evaluator that turns each semantic claim into a recommendation outcome using the direct spec's rules:
  - authority gate
  - downstream consequence gate
  - contradiction-accounting gate
  - no-open-high-priority-question gate
- Compile explicit proposal-level fields into semantic outputs, including:
  - the exact nested `proposal_governance` block
  - recommendation status
  - gate pass/fail details
  - related runtime carriers and witness surfaces
  - governance-implication sections
  - contradiction/proxy explanation
- Ensure semantic non-equivalence remains first-class and can block stable-canonical recommendation when conflicts are unresolved.
- Keep `semantic/` outputs additive:
  - do not rename or repurpose the current top-level CT-018 semantic/report keys
  - add the new gate/recommendation data under a dedicated nested block so existing additive-schema tests remain valid
- Apply the exact compatibility mapping from `3B` so the current top-level fields and report counts stay deterministic.
- Add an explicit rule that unresolved non-equivalence or unresolved proxy conflict blocks `recommended_stable_canonical`.

**Acceptance checkpoint**
- The compiler no longer upgrades a semantic node to ready/reviewable merely because it has durable target pages and no open questions.
- The compiler produces the same deterministic top-level compatibility fields for the same nested recommendation outcome every run.

### Step 4 - Add proposal-grade reporting and review surfaces
**Primary paths**
- `scripts/legacy_semantic_map/reporting.py`
- Generated reports under:
  - `docs/wiki-bi/_meta/legacy-semantic-map/reports/current/`
  - `docs/wiki-bi/_meta/legacy-semantic-map/reports/waves/wave-2026-04-17-semantic-governance-reframe/`

**Actions**
- Add generated views for:
  - `recommendation_counts` keyed by `recommended_stable_canonical`, `recommended_contested`, and `claim_level_only`
  - contested proposal IDs
  - blocked-by-gate reasons
  - governance-implication summaries
  - carrier-vs-semantic-object mismatches or over-promotion flags
- Add explicit reporting for unresolved non-equivalence/proxy conflicts so reviewers can see why a finding is blocked or contested.
- Preserve existing coverage/integrity reports; add new proposal-grade views rather than replacing them.
- Make the reports explain why a proposal is blocked or contested, not only that it exists.
- Keep the existing `semantic_maturity_counts` and auxiliary-view contracts valid by deriving them through the fixed compatibility table rather than by ad hoc logic.

**Acceptance checkpoint**
- A reviewer can inspect wave reports and understand which findings are stable recommendations, which are contested, and which remain claim-level only, plus why.

### Step 5 - Prove the model on the seed semantic family and a temporary-registry loop
**Primary paths**
- Existing seed semantics:
  - `docs/wiki-bi/_meta/legacy-semantic-map/semantic/rules/sem-rule-is-new-definition.yaml`
  - `docs/wiki-bi/_meta/legacy-semantic-map/semantic/rules/sem-rule-status-source-splitting.yaml`
  - `docs/wiki-bi/_meta/legacy-semantic-map/semantic/non-equivalences/sem-non-equivalence-customer-type-vs-is-new.yaml`
  - `docs/wiki-bi/_meta/legacy-semantic-map/semantic/non-equivalences/sem-non-equivalence-customer-master-vs-status.yaml`
- Existing wave claims:
  - `docs/wiki-bi/_meta/legacy-semantic-map/claims/wave-2026-04-17-semantic-governance-reframe/semantic/*.yaml`
- Validation tooling:
  - `scripts/legacy_semantic_map/compiler.py`
  - `scripts/legacy_semantic_map/reporting.py`
  - `scripts/legacy_semantic_map/pilot.py`

**Actions**
- Rework the current seed semantic claims so they include the new gate evidence and governance implications.
- Run the minimal verified loop in a temporary copy of the semantic-map registry:
  1. copy the registry to a temp directory
  2. run `uv run python -m scripts.legacy_semantic_map.orchestrate_wave --registry-root <temp_copy> --wave-id wave-2026-04-17-semantic-governance-reframe --trigger-id trigger-key-semantics-001`
  3. inspect the generated reports
  4. rerun the exact same orchestration command against the same temp copy to prove stabilization and field preservation across cloning + compile + report
- Use these exact proof cases:
  - mandatory rule/non-equivalence pair A: `sem-rule-is-new-definition` + `sem-non-equivalence-customer-type-vs-is-new`
  - mandatory rule/non-equivalence pair B: `sem-rule-status-source-splitting` + `sem-non-equivalence-customer-master-vs-status`

**Acceptance checkpoint**
- The seed family demonstrates the exact distinction the direct spec cares about: authoritative business meaning can coexist with proxy-heavy runtime usage, and unresolved conflict produces `recommended_contested` instead of silent promotion.

### Step 6 - Add regression tests and controlled verification commands
**Primary paths**
- New or updated tests under:
  - `tests/contracts/test_legacy_semantic_map_semantic_promotion_gates.py`
  - `tests/contracts/test_legacy_semantic_map_semantic_recommendation_statuses.py`
  - `tests/contracts/test_legacy_semantic_map_semantic_governance_implications.py`
  - `tests/contracts/test_legacy_semantic_map_semantic_carrier_boundary.py`
  - `tests/contracts/test_legacy_semantic_map_semantic_non_equivalence_gate_blocking.py`
  - `tests/contracts/test_legacy_semantic_map_orchestrate_wave_governance_field_passthrough.py`
  - `tests/integration/test_legacy_semantic_map_key_semantics_proposal_flow.py`
  - `tests/integration/test_legacy_semantic_map_temp_registry_stability.py`
- Existing regression guards:
  - `tests/contracts/test_legacy_semantic_map_semantic_compiler.py`
  - `tests/contracts/test_legacy_semantic_map_semantic_reporting.py`
  - `tests/contracts/test_legacy_semantic_map_semantic_maturity_additive_schema.py`
  - `tests/contracts/test_legacy_semantic_map_semantic_auxiliary_views.py`
  - `tests/contracts/test_legacy_semantic_map_orchestrate_wave_adapter.py`
  - `tests/integration/test_legacy_semantic_map_semantic_governance_reframe_flow.py`

**Actions**
- Write contract tests for every gate and for the proposal-vs-final boundary language.
- Write a contract test that successor-wave orchestration preserves the new `proposal_governance` fields across source-wave cloning and rerun.
- Add an integration test that uses a temporary registry copy and verifies repeated compile/report runs stabilize.
- Re-run the existing semantic compiler/reporting integration tests so the slice proves it extended CT-018 rather than breaking it.

**Acceptance checkpoint**
- The direct spec's gates are enforced by tests, and the temporary-registry stability loop is no longer just a convention.
- The orchestration path proves the new fields survive from source-wave claims into successor-wave claims across reruns.

## 5) Risks And Mitigations

| Risk | Why it matters here | Mitigation |
|---|---|---|
| Additive wording is too weak and reviewers still read `semantic/` as final truth | The chosen option preserves current paths | Add a nested proposal-governance block, preserve top-level compatibility, and update README/AGENTS guidance |
| Promotion gates stay shallow and only rename the old permissive behavior | Current compiler already over-promotes durable-target findings | Require explicit gate evidence fields and write failing tests for each gate before implementation |
| Runtime carriers get over-promoted because they are operationally important | The direct spec explicitly rejects this | Add carrier-vs-semantic-object markers and reporting flags for carrier-only proposals |
| Governance implications become free-form prose and cannot drive later decisions | The whole purpose of this slice is governance usefulness | Give governance implications structured fields and require them in contract tests |
| Temporary-copy validation is documented but not actually stable | The semantic-map guidance already warns about warm-up and stabilization behavior | Add an integration test that reruns compile/report on the same temp registry and checks for stabilized output |
| Source-wave cloning overwrites or bypasses the new semantic-governance fields | Current successor-wave orchestration still clones from the closed pilot wave | Make the source-of-truth choice explicit in the slice and cover it with orchestrator regression tests |
| The slice expands into broad semantic discovery | The direct spec warns against treating more discovery as success by itself | Keep the proof set bounded to the current successor-wave seed family and one adjacent example only if required |

## 6) Verification Steps

### Branch setup
```powershell
git status -sb
git switch slice/semantic-map-integration
git switch -c slice/semantic-map-key-semantics-governance
```

### Targeted contract tests during implementation
```powershell
uv run pytest tests/contracts/test_legacy_semantic_map_semantic_promotion_gates.py -v
uv run pytest tests/contracts/test_legacy_semantic_map_semantic_recommendation_statuses.py -v
uv run pytest tests/contracts/test_legacy_semantic_map_semantic_governance_implications.py -v
uv run pytest tests/contracts/test_legacy_semantic_map_semantic_carrier_boundary.py -v
uv run pytest tests/contracts/test_legacy_semantic_map_semantic_non_equivalence_gate_blocking.py -v
uv run pytest tests/contracts/test_legacy_semantic_map_orchestrate_wave_governance_field_passthrough.py -v
```

### Temporary-registry validation loop
```powershell
uv run python -m scripts.legacy_semantic_map.orchestrate_wave --registry-root <temp_copy> --wave-id wave-2026-04-17-semantic-governance-reframe --trigger-id trigger-key-semantics-001
uv run python -m scripts.legacy_semantic_map.orchestrate_wave --registry-root <temp_copy> --wave-id wave-2026-04-17-semantic-governance-reframe --trigger-id trigger-key-semantics-001
uv run pytest tests/integration/test_legacy_semantic_map_temp_registry_stability.py -v
uv run pytest tests/integration/test_legacy_semantic_map_key_semantics_proposal_flow.py -v
```

### Regression support
```powershell
uv run pytest tests/contracts/test_legacy_semantic_map_semantic_compiler.py -v
uv run pytest tests/contracts/test_legacy_semantic_map_semantic_reporting.py -v
uv run pytest tests/contracts/test_legacy_semantic_map_semantic_maturity_additive_schema.py -v
uv run pytest tests/contracts/test_legacy_semantic_map_semantic_auxiliary_views.py -v
uv run pytest tests/contracts/test_legacy_semantic_map_orchestrate_wave_adapter.py -v
uv run pytest tests/integration/test_legacy_semantic_map_semantic_governance_reframe_flow.py -v
```

### Full-suite gate before completion
```powershell
uv run pytest -v
```

### Manual review gates
- Confirm the generated wave reports distinguish `recommended_stable_canonical`, `recommended_contested`, and `claim_level_only`.
- Confirm at least one semantic rule and one semantic non-equivalence include contradiction-accounting and governance-implication output.
- Confirm no report or compiled field claims the shared registry has been finally accepted, deferred, retired, or absorbed.
- Confirm runtime-carrier evidence remains linked as witness material rather than silently promoted as semantic truth.

## 7) Executable Checklist

- [ ] Create branch `slice/semantic-map-key-semantics-governance` from `slice/semantic-map-integration@a2e96a0`
- [ ] Check in `docs/superpowers/plans/2026-04-18-workdatahubpro-legacy-semantic-map-key-semantics-governance.md`
- [ ] Update semantic-map README / local guidance for proposal-vs-final wording where needed
- [ ] Extend semantic claim schema with gate evidence, contradiction accounting, governance implications, and source-wave cloning compatibility
- [ ] Add gate evaluator logic in compiler support code with a nested proposal-governance block
- [ ] Freeze the exact `proposal_governance` schema and the top-level compatibility mapping in code and tests
- [ ] Replace permissive semantic-maturity promotion with gate-driven recommendation status
- [ ] Add proposal-grade reporting outputs without replacing coverage/integrity reports
- [ ] Resolve whether source-wave pilot claims or successor-wave claims are the maintained semantic input, and cover that path in orchestration tests
- [ ] Update the maintained seed semantic claim fixtures and ensure cloned successor-wave claims carry the new fields
- [ ] Prove the `is_new` / customer-type non-equivalence family through the new workflow
- [ ] Prove the `status-source-splitting` / customer-master-vs-status pair through the new workflow
- [ ] Prove unresolved non-equivalence/proxy conflict blocks stable recommendation
- [ ] Run temporary-registry compile/report stabilization loop
- [ ] Add contract tests for gates, statuses, governance implications, carrier boundaries, and non-equivalence blocking
- [ ] Run semantic compiler/reporting regression tests
- [ ] Run `uv run pytest -v`
- [ ] Merge `slice/semantic-map-key-semantics-governance` back into `slice/semantic-map-integration` after verification

## 8) RALPLAN-DR Summary

### Principles
1. Keep discovery execution-first; key semantics must remain a derived review surface, not the discovery driver.
2. Promote only business-meaningful semantic objects; preserve runtime carriers as evidence.
3. Separate recommendation-grade semantic proposals from final shared governance truth.
4. Treat contradiction accounting and non-equivalence as mandatory, not optional reviewer polish.
5. Require temporary-registry validation before checked-in promotion claims.

### Decision Drivers
1. The direct spec's core gap is promotion discipline, not discovery breadth.
2. CT-018 already exists and should be extended additively rather than replaced by a new semantic-map architecture.
3. The seed `is_new` family already exposes the exact proxy-vs-authority conflict the new workflow must govern correctly.

### Viable Options

#### Option 1 - Guidance-only tightening
- Keep the current compiler and rely on reviewer judgment to decide stable vs contested.
- Rejected because the direct spec requires machine-supported gates and governance implications.

#### Option 2 - Separate proposal registry tree
- Move proposal outputs away from the existing `semantic/` path entirely.
- Not chosen because it is a larger refactor than this narrow follow-on needs and would duplicate the current CT-018 surfaces.

#### Option 3 - Add gate-driven recommendation semantics to the existing registry **(chosen)**
- Preserve current paths and reports, keep current top-level schema stable, and add a nested proposal-governance block so semantic outputs become explicitly recommendation-grade and evidence-gated.
- Chosen because it best balances correctness, additive delivery, and branch-sized scope.

## 9) ADR

### Decision
Implement a narrow CT-018 follow-on that adds gate-driven semantic recommendation logic, contradiction accounting, carrier-vs-semantic separation, and governance implications to the current semantic claim/compiler/reporting flow.

### Drivers
- The direct spec requires stronger promotion discipline than the current implementation provides.
- The current semantic-map package already has the right wave, example seed set, and reporting skeleton.
- A narrow additive slice is lower-risk than a path-level registry redesign.

### Alternatives considered
- leave the current permissive compiler in place and rely on review guidance
- create a separate proposal registry tree
- broaden discovery instead of tightening promotion discipline

### Why chosen
It fixes the real gap the interview exposed while preserving the current CT-018 structure and avoiding unnecessary churn in the semantic-map package.

### Consequences
- Compiled semantic nodes will carry more governance and evidence structure.
- Existing semantic tests and reports will need updates because the meaning of readiness becomes stricter.
- Reviewers will need to read recommendation-grade outputs carefully; the docs must make the boundary explicit.
- Orchestration/source-wave assumptions must be made explicit so future re-orchestration does not silently discard the new fields.
- The plan now intentionally locks one nested additive schema and one compatibility mapping, which reduces executor ambiguity but increases up-front contract specificity.

### Follow-ups
- If the additive wording still proves too ambiguous in practice, open a later micro-slice to split proposal outputs into a separate registry tree.
- If the seed family is not enough to prove all gates, admit one adjacent bounded semantic example rather than reopening broad discovery.
- After this slice lands, use the strengthened proposal outputs to decide whether a later durable absorption or governance-adoption slice is warranted.

## 10) Available-Agent-Types Roster

- `planner`: convert the checked-in plan into execution sequencing and risk checkpoints
- `architect`: challenge boundary decisions around proposal-vs-final semantics
- `critic`: enforce gate completeness, verification clarity, and testability
- `executor`: implement bounded code and doc changes across scripts/tests/docs
- `test-engineer`: strengthen contract/integration test coverage for gates and stabilization loops
- `verifier`: confirm generated outputs and commands support the completion claim
- `writer`: tighten checked-in plan text, README guidance, and review-facing summaries

## 11) Follow-up Staffing Guidance

### Ralph lane
- Recommended mode: `$ralph` with one primary execution lane and verifier checkpoints
- Suggested reasoning levels by lane:
  - planning/doc boundary lane: `medium`
  - compiler/reporting logic lane: `high`
  - verification lane: `medium`
- Best fit when one owner should keep the gate logic, doc wording, and test adjustments tightly synchronized.

### Team lane
- Recommended staffing:
  - 1 `architect` or boundary-focused lead for proposal-vs-final semantics
  - 1 `executor` for claim/compiler/model changes
  - 1 `executor` for reporting plus docs/readme updates
  - 1 `test-engineer` or `verifier` for regression and temp-registry stabilization proof
- Suggested reasoning levels by lane:
  - boundary/design lane: `high`
  - implementation lanes: `high`
  - verification lane: `medium`
- Best fit when the code/write surfaces stay separated:
  - lane 1 owns `claims.py`, `models.py`, `compiler.py`
  - lane 2 owns `reporting.py`, docs, plan text
  - lane 3 owns new contract/integration tests and validation commands

## 12) Launch Hints

### Ralph handoff hint
```text
$ralph docs/superpowers/plans/2026-04-18-workdatahubpro-legacy-semantic-map-key-semantics-governance.md
```

### Team handoff hints
```text
$team docs/superpowers/plans/2026-04-18-workdatahubpro-legacy-semantic-map-key-semantics-governance.md
```

```powershell
omx team run docs/superpowers/plans/2026-04-18-workdatahubpro-legacy-semantic-map-key-semantics-governance.md
```

## 13) Team Verification Path

- Team proves the new gate fields exist in claims and compiled semantic outputs.
- Team proves reporting distinguishes recommendation statuses and blocked reasons without replacing coverage/integrity outputs.
- Team proves the temporary-registry stabilization loop passes on repeated runs.
- Ralph or the final verifier then reruns the targeted semantic regressions plus `uv run pytest -v` and checks the generated wave reports before any completion claim.

## 14) Consensus Changelog

- Preserved CT-018 additive compatibility by freezing one exact nested `proposal_governance` block instead of changing existing top-level semantic/report fields.
- Added a deterministic compatibility mapping from nested recommendation outcomes into `semantic_maturity_level`, `consumption_readiness_status`, and `blocked_by`.
- Made the current source-wave-to-successor-wave orchestration path explicit and added a required passthrough regression for cloned governance fields.
- Fixed the proof set to two concrete semantic pairs: `is_new` vs customer type and status-source-splitting vs customer-master-vs-status.
- Fixed the temp-registry proof path to the real orchestration front door and required a rerun-stability check.

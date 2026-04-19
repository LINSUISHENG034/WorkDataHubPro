# WorkDataHubPro Legacy Semantic Map Accuracy Repair Plan

**Goal:** repair the checked-in `legacy-semantic-map` nodes whose source provenance or semantic-layer classification currently weakens the claim that the map accurately records legacy `WorkDataHub` business semantics.

**Scope:** `docs/wiki-bi/_meta/legacy-semantic-map/`, its active-wave claim artifacts, generated semantic outputs, generated reports, and the semantic-map contract/integration tests that should prevent the same drift from recurring.

**Non-Goals:**

- reopening closed waves as active implementation lanes
- rewriting durable `docs/wiki-bi/` concept / standard / evidence pages in this plan
- expanding the semantic inventory beyond the nodes already checked in

---

## Audit Summary

The 2026-04-19 audit established four stable findings:

1. Core sample business-semantics nodes such as `is_new`, `company_id` multi-signal resolution, and `reference_sync vs backfill` are materially aligned with legacy docs/config/code.
2. No broken source paths were found in checked-in `semantic/` outputs or claim artifacts.
3. Two active semantic nodes still cite current `docs/wiki-bi/` content as primary semantic authority, which is not acceptable for a registry that claims to record legacy source truth.
4. A runtime/operator cluster is currently presented as `recommended_stable_canonical` semantic output even though local subtree guidance says runtime/operator surfaces should normally stay in `surfaces/`, `evidence/`, or claim-level discovery unless they directly encode business meaning rather than engineering/runtime behavior.

The repair set below is therefore a correction of provenance and semantic-layer classification, not a broad semantic rewrite.

---

## Complete Repair Inventory

### A. Provenance Corrections

These nodes currently overstate their authority because `primary_semantic_sources` point to current wiki output instead of legacy raw sources.

| Node | Current problem | Required correction | Primary file(s) to change |
|---|---|---|---|
| `sem-lifecycle-customer-status-yearly-cycle` | `primary_semantic_sources` points to `docs/wiki-bi/evidence/customer-mdm-lifecycle-evidence.md` instead of legacy raw sources | replace primary source with legacy business-background / runtime witnesses; keep current wiki only as supporting witness or durable target | `docs/wiki-bi/_meta/legacy-semantic-map/semantic/lifecycles/sem-lifecycle-customer-status-yearly-cycle.yaml` |
| `sem-non-equivalence-temp-id-vs-company-id` | `primary_semantic_sources` includes `docs/wiki-bi/concepts/temp-id.md` | keep `docs/guides/infrastructure/company-enrichment-service.md` as the authoritative primary source and move current wiki references to supporting/downstream witness only | `docs/wiki-bi/_meta/legacy-semantic-map/semantic/non-equivalences/sem-non-equivalence-temp-id-vs-company-id.yaml` |

### B. Runtime / Operator Scope Demotions

These nodes are not being flagged as factually false. The problem is that they are currently presented as `recommended_stable_canonical` semantic outputs even though they primarily describe runtime/operator/persistence behavior rather than durable business semantics.

The repair action for this cluster is to demote them from absorption-ready semantic canon to claim-level discovery or runtime-governance memory.

| Node | Current problem | Required correction | Primary file(s) to change |
|---|---|---|---|
| `sem-rule-annuity-performance-post-hook-chain` | default post-hook trigger chain is a runtime orchestration rule, not a standalone business-semantic object | change from `recommended_stable_canonical` to `claim_level_only` and `discovery-only`; keep it as surface/evidence support, not semantic canon | `docs/wiki-bi/_meta/legacy-semantic-map/semantic/rules/sem-rule-annuity-performance-post-hook-chain.yaml` |
| `sem-rule-company-lookup-queue-single-domain-boundary` | CLI single-domain boundary is orchestration behavior | demote to claim-level runtime-governance note | `docs/wiki-bi/_meta/legacy-semantic-map/semantic/rules/sem-rule-company-lookup-queue-single-domain-boundary.yaml` |
| `sem-lifecycle-company-lookup-queue-recovery-cycle` | retry/backoff/reset loop is queue runtime behavior | demote to claim-level runtime-governance note | `docs/wiki-bi/_meta/legacy-semantic-map/semantic/lifecycles/sem-lifecycle-company-lookup-queue-recovery-cycle.yaml` |
| `sem-lifecycle-reference-sync-preload-cycle` | pre-load job/schedule/state-control description is runtime lifecycle, not business-semantic canon | demote to claim-level runtime-governance note | `docs/wiki-bi/_meta/legacy-semantic-map/semantic/lifecycles/sem-lifecycle-reference-sync-preload-cycle.yaml` |
| `sem-fact-family-reference-sync-target-inventory` | target inventory is a governed surface contract, but not a business-semantic fact family | demote to claim-level inventory note tied to `reference_sync` surface governance | `docs/wiki-bi/_meta/legacy-semantic-map/semantic/fact-families/sem-fact-family-reference-sync-target-inventory.yaml` |
| `sem-rule-reference-sync-incremental-state` | `last_synced_at` / `force_full_sync` is runtime state behavior | demote to claim-level runtime-governance note | `docs/wiki-bi/_meta/legacy-semantic-map/semantic/rules/sem-rule-reference-sync-incremental-state.yaml` |
| `sem-rule-enrichment-index-cache-boundary` | cache-boundary rule is runtime/persistence behavior rather than business-semantic canon | demote to claim-level cache-governance note | `docs/wiki-bi/_meta/legacy-semantic-map/semantic/rules/sem-rule-enrichment-index-cache-boundary.yaml` |
| `sem-rule-first-wave-artifact-operator-evidence` | unresolved-name / failed-record artifact handling is operator-evidence classification, not business-semantic canon | demote to claim-level operator-evidence note | `docs/wiki-bi/_meta/legacy-semantic-map/semantic/rules/sem-rule-first-wave-artifact-operator-evidence.yaml` |

### C. Historical Audit-Only Provenance Debt

This artifact should not be reopened as an active-wave mutation unless a later contract test proves historical-wave repair is required. It still needs to be recorded in the repair plan so the debt is not forgotten.

| Artifact | Current problem | Planned treatment |
|---|---|---|
| `claim-wave-2026-04-17-customer-status-semantic-pilot-lifecycle` | historical closed-wave claim still marks current wiki lifecycle evidence as `authoritative_semantic_source` | keep closed-wave artifact immutable unless verification proves otherwise; document it as historical provenance debt and ensure current canonical output no longer depends on the same mistake |

### D. Active-Wave Claim Artifacts That Must Move With The Node Fixes

Every active semantic-node correction above has to be applied at the claim layer first, then recompiled. The following active-wave claims therefore belong to the execution set:

- `claim-wave-2026-04-17-semantic-governance-reframe-lifecycle`
- `claim-wave-2026-04-17-semantic-governance-reframe-temp-id-non-equivalence`
- `claim-wave-2026-04-17-semantic-governance-reframe-annuity-performance-hook-chain`
- `claim-wave-2026-04-17-semantic-governance-reframe-company-lookup-queue-recovery-cycle`
- `claim-wave-2026-04-17-semantic-governance-reframe-reference-sync-preload-cycle`
- `claim-wave-2026-04-17-semantic-governance-reframe-reference-sync-inventory`
- `claim-wave-2026-04-17-semantic-governance-reframe-reference-sync-state`
- `claim-wave-2026-04-17-semantic-governance-reframe-enrichment-index-cache-boundary`
- `claim-wave-2026-04-17-semantic-governance-reframe-first-wave-artifact-operator-evidence`
- `claim-wave-2026-04-17-semantic-governance-reframe-company-lookup-queue-recovery-cycle`

---

## File Scope

### Semantic-map claims and compiled semantic outputs

- `docs/wiki-bi/_meta/legacy-semantic-map/claims/wave-2026-04-17-semantic-governance-reframe/semantic/*.yaml`
- `docs/wiki-bi/_meta/legacy-semantic-map/semantic/lifecycles/sem-lifecycle-customer-status-yearly-cycle.yaml`
- `docs/wiki-bi/_meta/legacy-semantic-map/semantic/non-equivalences/sem-non-equivalence-temp-id-vs-company-id.yaml`
- `docs/wiki-bi/_meta/legacy-semantic-map/semantic/rules/sem-rule-annuity-performance-post-hook-chain.yaml`
- `docs/wiki-bi/_meta/legacy-semantic-map/semantic/rules/sem-rule-company-lookup-queue-single-domain-boundary.yaml`
- `docs/wiki-bi/_meta/legacy-semantic-map/semantic/lifecycles/sem-lifecycle-company-lookup-queue-recovery-cycle.yaml`
- `docs/wiki-bi/_meta/legacy-semantic-map/semantic/lifecycles/sem-lifecycle-reference-sync-preload-cycle.yaml`
- `docs/wiki-bi/_meta/legacy-semantic-map/semantic/fact-families/sem-fact-family-reference-sync-target-inventory.yaml`
- `docs/wiki-bi/_meta/legacy-semantic-map/semantic/rules/sem-rule-reference-sync-incremental-state.yaml`
- `docs/wiki-bi/_meta/legacy-semantic-map/semantic/rules/sem-rule-enrichment-index-cache-boundary.yaml`
- `docs/wiki-bi/_meta/legacy-semantic-map/semantic/rules/sem-rule-first-wave-artifact-operator-evidence.yaml`

### Generated report surfaces

- `docs/wiki-bi/_meta/legacy-semantic-map/reports/current/*.json`
- `docs/wiki-bi/_meta/legacy-semantic-map/reports/waves/wave-2026-04-17-semantic-governance-reframe/*.json`
- `docs/wiki-bi/_meta/legacy-semantic-map/reports/waves/wave-2026-04-17-semantic-governance-reframe/*.md`

### Guardrails and tests

- `docs/wiki-bi/_meta/legacy-semantic-map/AGENTS.md`
- `tests/contracts/test_legacy_semantic_map_semantic_source_provenance.py` (new)
- `tests/contracts/test_legacy_semantic_map_runtime_scope_boundary.py` (new)
- `tests/contracts/test_legacy_semantic_map_semantic_compiler.py`
- `tests/contracts/test_legacy_semantic_map_semantic_reporting.py`
- `tests/contracts/test_legacy_semantic_map_semantic_recommendation_statuses.py`
- `tests/integration/test_legacy_semantic_map_semantic_governance_reframe_flow.py`

---

## Repair Strategy

### Task 1: Add Regression Guards Before Editing Claims

**Goal:** make the audit findings mechanically enforceable before any node edits happen.

- [ ] Create `tests/contracts/test_legacy_semantic_map_semantic_source_provenance.py`
  - assert no active compiled semantic node under `docs/wiki-bi/_meta/legacy-semantic-map/semantic/` uses `docs/wiki-bi/` as a `primary_semantic_sources` entry
  - explicitly allow `docs/wiki-bi/` only in `supporting_witness_sources`, `durable_target_pages`, `proxy_usage_refs`, and downstream consequence refs
- [ ] Create `tests/contracts/test_legacy_semantic_map_runtime_scope_boundary.py`
  - maintain an explicit denylist of the runtime/operator cluster above
  - assert those nodes do not carry `recommendation_status: recommended_stable_canonical`
  - assert their `consumption_readiness_status` is `discovery-only`
- [ ] Reuse existing schema/reporting tests so the new guard does not break the compiler contract by accident

**Verification:**

```powershell
uv run pytest tests/contracts/test_legacy_semantic_map_semantic_source_provenance.py -v
uv run pytest tests/contracts/test_legacy_semantic_map_runtime_scope_boundary.py -v
```

### Task 2: Repair Provenance At The Claim Layer

**Goal:** remove current wiki pages from primary semantic authority for the two affected active nodes.

- [ ] Update `claim-wave-2026-04-17-semantic-governance-reframe-lifecycle`
  - replace `docs/wiki-bi/evidence/customer-mdm-lifecycle-evidence.md` as `authoritative_semantic_source`
  - prefer legacy raw sources such as:
    - `docs/business-background/战客身份定义与更新逻辑.md`
    - `src/work_data_hub/customer_mdm/contract_sync.py`
    - `src/work_data_hub/customer_mdm/snapshot_refresh.py`
    - `src/work_data_hub/cli/etl/hooks.py`
- [ ] Update `claim-wave-2026-04-17-semantic-governance-reframe-temp-id-non-equivalence`
  - keep `docs/guides/infrastructure/company-enrichment-service.md` as the only authoritative primary source unless a second legacy raw source proves necessary
  - move `docs/wiki-bi/concepts/temp-id.md` out of `primary_source_refs`
  - use legacy runtime witnesses if an additional supporting witness is needed:
    - `src/work_data_hub/domain/company_enrichment/lookup_queue.py`
    - `src/work_data_hub/infrastructure/enrichment/resolver/core.py`
- [ ] Do not mutate the closed-wave `claim-wave-2026-04-17-customer-status-semantic-pilot-lifecycle` in the first repair pass
  - record it as historical provenance debt only
  - verify that no current compiled semantic output depends on that closed-wave artifact

**Verification:**

```powershell
uv run pytest tests/contracts/test_legacy_semantic_map_semantic_source_provenance.py -v
```

### Task 3: Demote Runtime / Operator Nodes Out Of Absorption-Ready Semantic Canon

**Goal:** keep runtime/operator discovery visible without presenting it as business-semantic stable canon.

For each node in the runtime/operator demotion cluster:

- [ ] update the active-wave claim artifact first
- [ ] then regenerate the compiled semantic node
- [ ] apply the same metadata shape unless a compiler/test contract forces a different field set:

```yaml
proposal_governance:
  recommendation_status: claim_level_only
consumption_readiness_status: discovery-only
readiness_notes:
  - runtime/operator governance memory; not stable business-semantic canon
```

Additional per-node intent:

- `sem-rule-annuity-performance-post-hook-chain`
  - preserve the legacy behavior statement
  - stop presenting it as a semantic absorption-ready object
- `sem-rule-company-lookup-queue-single-domain-boundary`
  - preserve CLI/runtime boundary memory
  - classify it as runtime-governance only
- `sem-lifecycle-company-lookup-queue-recovery-cycle`
  - preserve retry/backoff/reset memory
  - classify it as queue runtime lifecycle memory
- `sem-lifecycle-reference-sync-preload-cycle`
  - preserve pre-load-cycle memory
  - classify it as `reference_sync` runtime lifecycle memory
- `sem-fact-family-reference-sync-target-inventory`
  - preserve inventory contract memory
  - classify it as governed surface inventory, not business fact family canon
- `sem-rule-reference-sync-incremental-state`
  - preserve `last_synced_at` / `force_full_sync` memory
  - classify it as runtime state control, not business-semantic canon
- `sem-rule-enrichment-index-cache-boundary`
  - preserve cache subordination to `company_id` semantics
  - classify it as cache-governance memory
- `sem-rule-first-wave-artifact-operator-evidence`
  - preserve operator-artifact classification
  - classify it as operator-evidence memory only

**Verification:**

```powershell
uv run pytest tests/contracts/test_legacy_semantic_map_runtime_scope_boundary.py -v
uv run pytest tests/contracts/test_legacy_semantic_map_semantic_recommendation_statuses.py -v
```

### Task 4: Regenerate Compiled Semantic Outputs And Reports

**Goal:** ensure checked-in `semantic/` outputs and report surfaces are regenerated from the corrected active-wave claims instead of being hand-edited into drift.

- [ ] use the existing semantic-map regeneration path; do not hand-edit generated report files
- [ ] regenerate the active successor wave after claim edits
- [ ] verify that current and wave-local report artifacts reflect the demotions and provenance fixes

**Preferred commands:**

```powershell
uv run python -m scripts.legacy_semantic_map.orchestrate_wave --registry-root docs/wiki-bi/_meta/legacy-semantic-map --wave-id wave-2026-04-17-semantic-governance-reframe
uv run python -m scripts.legacy_semantic_map.pilot --registry-root docs/wiki-bi/_meta/legacy-semantic-map --wave-id wave-2026-04-17-semantic-governance-reframe
```

**Expected result:**

- no active semantic node keeps `docs/wiki-bi/` under `primary_semantic_sources`
- the runtime/operator denylist no longer appears as `recommended_stable_canonical`
- current/wave-local semantic summary views stay mechanically healthy

### Task 5: Run The Semantic-Map Contract And Integration Stack

**Goal:** prove the repair is consistent with the existing semantic-map workflow rather than a one-off doc edit.

- [ ] run the new provenance and scope-boundary tests
- [ ] run the existing semantic compiler/reporting/recommendation tests
- [ ] run the successor-wave integration flow

**Verification:**

```powershell
uv run pytest tests/contracts/test_legacy_semantic_map_semantic_source_provenance.py -v
uv run pytest tests/contracts/test_legacy_semantic_map_runtime_scope_boundary.py -v
uv run pytest tests/contracts/test_legacy_semantic_map_semantic_compiler.py -v
uv run pytest tests/contracts/test_legacy_semantic_map_semantic_reporting.py -v
uv run pytest tests/contracts/test_legacy_semantic_map_semantic_recommendation_statuses.py -v
uv run pytest tests/integration/test_legacy_semantic_map_semantic_governance_reframe_flow.py -v
```

Optional final confidence gate if the repair touches compiler logic:

```powershell
uv run pytest -v
```

---

## Completion Criteria

This repair plan is complete only when all of the following are true:

- the 10 active nodes in the repair inventory have been addressed
- the 2 provenance nodes no longer use current wiki pages as primary semantic authority
- the 8 runtime/operator nodes no longer present as absorption-ready business-semantic canon
- the closed-wave lifecycle claim is explicitly treated as historical audit debt rather than silently ignored
- reports are regenerated through existing semantic-map entrypoints, not hand-edited
- new regression tests prevent the same provenance and scope drift from reappearing

---

## Notes

- This plan intentionally does **not** call for `docs/wiki-bi/index.md` or `docs/wiki-bi/log.md` changes because `legacy-semantic-map` remains a non-durable subtree.
- The audit found no need to repair validated core nodes such as:
  - `sem-rule-is-new-definition`
  - `sem-rule-company-id-multi-signal-resolution`
  - `sem-non-equivalence-reference-sync-vs-backfill`
- The repair target is therefore precision and governance, not wholesale semantic-map redesign.

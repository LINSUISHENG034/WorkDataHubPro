# WorkDataHub Legacy Semantic Deep Dig Round 2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Distributed workers may write only under `docs/wiki-bi/_meta/legacy-semantic-map/claims/wave-2026-04-17-semantic-governance-reframe/`. Canonical compile, manifest, and report writes remain main-thread-only.

**Goal:** Extend the active successor wave with four additional high-value semantic claims rooted in `E:\Projects\WorkDataHub`: publication refresh/delete-scope semantics, event-domain temporal contract lookup, customer-master derived signal provenance, and directory-based workbook discovery/version arbitration.

**Architecture:** Keep discovery execution-first and bounded to the active wave `wave-2026-04-17-semantic-governance-reframe`. Each mined subdomain becomes one proposal-grade semantic claim under the active wave, with legacy docs/config/code as primary evidence and current wiki pages only as supporting witnesses or durable targets. The main thread reviews the claims, then reruns probe/pilot and semantic-map tests so canonical semantic outputs and authoritative reports are regenerated in one place.

**Tech Stack:** Markdown plans, YAML claim artifacts, Python semantic-map tooling under `scripts/legacy_semantic_map/`, `uv`, `pytest`, legacy repo evidence under `E:\Projects\WorkDataHub`

---

## File Structure

### Planning
- Create: `docs/superpowers/plans/2026-04-19-workdatahubpro-legacy-semantic-deep-dig-round-2.md`

### New active-wave claim files
- Create: `docs/wiki-bi/_meta/legacy-semantic-map/claims/wave-2026-04-17-semantic-governance-reframe/semantic/claim-wave-2026-04-17-semantic-governance-reframe-fact-publication-refresh-scope-boundary.yaml`
- Create: `docs/wiki-bi/_meta/legacy-semantic-map/claims/wave-2026-04-17-semantic-governance-reframe/semantic/claim-wave-2026-04-17-semantic-governance-reframe-event-domain-current-row-contract-lookup.yaml`
- Create: `docs/wiki-bi/_meta/legacy-semantic-map/claims/wave-2026-04-17-semantic-governance-reframe/semantic/claim-wave-2026-04-17-semantic-governance-reframe-customer-master-derived-signal-provenance.yaml`
- Create: `docs/wiki-bi/_meta/legacy-semantic-map/claims/wave-2026-04-17-semantic-governance-reframe/semantic/claim-wave-2026-04-17-semantic-governance-reframe-workbook-discovery-version-arbitration.yaml`

### Main-thread-generated outputs
- Modify via compile/report only: `docs/wiki-bi/_meta/legacy-semantic-map/manifest.json`
- Modify via compile/report only: `docs/wiki-bi/_meta/legacy-semantic-map/semantic/index.yaml`
- Modify via compile/report only: `docs/wiki-bi/_meta/legacy-semantic-map/semantic/rules/*.yaml`
- Modify via compile/report only: `docs/wiki-bi/_meta/legacy-semantic-map/reports/current/*.json`
- Modify via compile/report only: `docs/wiki-bi/_meta/legacy-semantic-map/reports/waves/wave-2026-04-17-semantic-governance-reframe/*`

---

## Targeted Subdomains

### 1. Publication refresh/delete-scope contract

Why it is worth mining:
- maps directly to `CT-003`
- has strong legacy config/doc/code evidence
- not yet expressed as a dedicated active-wave semantic node

Primary evidence family:
- `E:\Projects\WorkDataHub\config\data_sources.yml`
- `E:\Projects\WorkDataHub\docs\guides\domain-migration\development-guide.md`
- four legacy capability maps under `docs/domains/*capability-map.md`
- `E:\Projects\WorkDataHub\src\work_data_hub\orchestration\ops\loading.py`
- `E:\Projects\WorkDataHub\src\work_data_hub\io\loader\operations.py`
- `E:\Projects\WorkDataHub\src\work_data_hub\infrastructure\schema\definitions\*.py`

Durable target pages:
- `docs/wiki-bi/standards/output-correctness/output-correctness.md`
- `docs/wiki-bi/standards/output-correctness/annuity-performance-output-contract.md`
- `docs/wiki-bi/standards/output-correctness/annuity-income-output-contract.md`
- `docs/wiki-bi/standards/output-correctness/annual-award-output-contract.md`
- `docs/wiki-bi/standards/output-correctness/annual-loss-output-contract.md`

Core conclusion to mine:
- legacy delete-scope / refresh-key semantics are output-publication contracts, not business identity grain or snapshot grain
- fact refresh scope and semantic identity must not be collapsed into one notion of “primary key”

### 2. Event-domain temporal contract lookup

Why it is worth mining:
- maps directly to `CT-005`
- evidence already exists in legacy capability maps and current output/evidence pages
- high leverage for interpreting `annual_award` / `annual_loss` enrichment correctness

Primary evidence family:
- `E:\Projects\WorkDataHub\docs\domains\annual_award-capability-map.md`
- `E:\Projects\WorkDataHub\docs\domains\annual_loss-capability-map.md`
- `E:\Projects\WorkDataHub\tests\slice_tests\test_j_real_effect_guards.py`
- `E:\Projects\WorkDataHub\src\work_data_hub\customer_mdm\contract_sync.py`
- current pages under `docs/wiki-bi/evidence/annual-award-field-processing-evidence.md` and `docs/wiki-bi/evidence/annual-loss-field-processing-evidence.md`

Durable target pages:
- `docs/wiki-bi/standards/output-correctness/annual-award-output-contract.md`
- `docs/wiki-bi/standards/output-correctness/annual-loss-output-contract.md`
- `docs/wiki-bi/evidence/identity-and-lookup-evidence.md`

Core conclusion to mine:
- event-domain plan-code enrichment uses a current-row temporal contract lookup boundary rather than a general historical contract replay
- preserving source value, current-row lookup, and domain default fallback are three distinct stages of one output contract

### 3. Customer-master derived signal provenance

Why it is worth mining:
- maps directly to `CT-002` and partially to `CT-007`
- evidence is dense and business-semantic rather than purely runtime
- current active wave has reference-layering claims, but no direct semantic claim for weighted signal provenance

Primary evidence family:
- `E:\Projects\WorkDataHub\config\foreign_keys.yml`
- `E:\Projects\WorkDataHub\docs\business-background\客户主数据回填与状态来源分析.md`
- `E:\Projects\WorkDataHub\docs\verification_guide_real_data.md`
- `E:\Projects\WorkDataHub\docs\domains\annuity_performance-capability-map.md`
- `E:\Projects\WorkDataHub\docs\domains\annuity_income-capability-map.md`
- current page `docs/wiki-bi/evidence/customer-master-signals-evidence.md`

Durable target pages:
- `docs/wiki-bi/evidence/customer-master-signals-evidence.md`
- `docs/wiki-bi/standards/output-correctness/output-correctness.md`
- `docs/wiki-bi/evidence/reference-and-backfill-evidence.md`

Core conclusion to mine:
- customer-master signals are derived output objects with explicit provenance classes such as dominant-value, breadth-count, breadth-list, classification, and timeline-tag
- these derived signals must not be reduced to raw fact publication or snapshot status

### 4. Directory-based workbook discovery and version arbitration

Why it is worth mining:
- maps directly to `CT-001`
- strong evidence in discovery service, version scanner, capability maps, and sample/fixture docs
- complements the current workbook-family evidence without repeating row-level contracts

Primary evidence family:
- `E:\Projects\WorkDataHub\config\data_sources.yml`
- `E:\Projects\WorkDataHub\src\work_data_hub\io\connectors\version_scanner.py`
- `E:\Projects\WorkDataHub\src\work_data_hub\io\connectors\discovery\service.py`
- `E:\Projects\WorkDataHub\tests\integration\io\test_version_detection.py`
- `E:\Projects\WorkDataHub\docs\domains\annuity_performance-capability-map.md`
- `E:\Projects\WorkDataHub\docs\domains\annuity_income-capability-map.md`
- `E:\Projects\WorkDataHub\docs\domains\annual_award-capability-map.md`
- `E:\Projects\WorkDataHub\docs\domains\annual_loss-capability-map.md`

Durable target pages:
- `docs/wiki-bi/evidence/annuity-workbook-family-evidence.md`
- `docs/wiki-bi/evidence/business-collection-workbook-variants-evidence.md`
- `docs/wiki-bi/standards/input-reality/input-reality-contracts.md`

Core conclusion to mine:
- directory scan plus version arbitration is an operator/runtime admission boundary, not just I/O plumbing
- shared folder or workbook family does not by itself collapse domain contracts into one domain

---

### Task 1: Freeze the round-2 excavation scope

**Files:**
- Create: `docs/superpowers/plans/2026-04-19-workdatahubpro-legacy-semantic-deep-dig-round-2.md`
- Read: `docs/superpowers/specs/2026-04-11-workdatahubpro-first-wave-legacy-coverage-matrix.md`
- Read: `docs/wiki-bi/_meta/legacy-semantic-map/claims/wave-2026-04-17-semantic-governance-reframe/semantic/*.yaml`
- Read: `docs/wiki-bi/_meta/legacy-semantic-map/reports/waves/wave-2026-04-17-semantic-governance-reframe/*.json`

- [ ] **Step 1: Confirm these targets are still open and non-duplicated**

Run:

```powershell
rg -n "CT-001|CT-002|CT-003|CT-005" docs/superpowers/specs/2026-04-11-workdatahubpro-first-wave-legacy-coverage-matrix.md
rg -n "refresh-scope|current-row-contract|derived-signal-provenance|version-arbitration" docs/wiki-bi/_meta/legacy-semantic-map/claims/wave-2026-04-17-semantic-governance-reframe/semantic
```

Expected:
- the CT rows remain non-accepted follow-on work
- no existing active-wave claim already owns these exact semantic targets

- [ ] **Step 2: Freeze the round-2 ownership map**

Ownership map:

- Worker A owns `claim-wave-2026-04-17-semantic-governance-reframe-fact-publication-refresh-scope-boundary.yaml`
- Worker B owns `claim-wave-2026-04-17-semantic-governance-reframe-event-domain-current-row-contract-lookup.yaml`
- Worker C owns `claim-wave-2026-04-17-semantic-governance-reframe-customer-master-derived-signal-provenance.yaml`
- Worker D owns `claim-wave-2026-04-17-semantic-governance-reframe-workbook-discovery-version-arbitration.yaml`

- [ ] **Step 3: Freeze the verification stack**

Run after the four new claim files exist:

```powershell
uv run python -m scripts.legacy_semantic_map.probe --registry-root docs/wiki-bi/_meta/legacy-semantic-map --wave-id wave-2026-04-17-semantic-governance-reframe --reruns 2
uv run python -m scripts.legacy_semantic_map.pilot --registry-root docs/wiki-bi/_meta/legacy-semantic-map --wave-id wave-2026-04-17-semantic-governance-reframe
uv run pytest tests/contracts tests/integration -k legacy_semantic_map -v
```

Expected:
- probe stabilizes after the final rerun
- pilot compiles the full active-wave set
- semantic-map suite stays green

---

### Task 2: Mine fact publication refresh-scope boundary

**Files:**
- Create: `docs/wiki-bi/_meta/legacy-semantic-map/claims/wave-2026-04-17-semantic-governance-reframe/semantic/claim-wave-2026-04-17-semantic-governance-reframe-fact-publication-refresh-scope-boundary.yaml`
- Read: `E:\Projects\WorkDataHub\config\data_sources.yml`
- Read: `E:\Projects\WorkDataHub\docs\guides\domain-migration\development-guide.md`
- Read: `E:\Projects\WorkDataHub\docs\domains\annuity_performance-capability-map.md`
- Read: `E:\Projects\WorkDataHub\docs\domains\annuity_income-capability-map.md`
- Read: `E:\Projects\WorkDataHub\docs\domains\annual_award-capability-map.md`
- Read: `E:\Projects\WorkDataHub\docs\domains\annual_loss-capability-map.md`
- Read: `E:\Projects\WorkDataHub\src\work_data_hub\orchestration\ops\loading.py`
- Read: `E:\Projects\WorkDataHub\src\work_data_hub\io\loader\operations.py`
- Read: `E:\Projects\WorkDataHub\src\work_data_hub\infrastructure\schema\definitions\*.py`

- [ ] **Step 1: Gather legacy primary evidence**

Minimum evidence:
- one `legacy_config` source from `config/data_sources.yml`
- one `legacy_doc` source from `development-guide.md`
- at least two `legacy_doc` capability-map sources spanning both annuity and event domains
- one `legacy_code` source from load or schema layers

- [ ] **Step 2: Author the claim with this exact target**

Required claim shape:

- `claim_scope: semantic`
- `claim_target_id: sem-rule-fact-publication-refresh-scope-boundary`
- `compiled_into` must include:
  - `docs/wiki-bi/standards/output-correctness/output-correctness.md`
  - `docs/wiki-bi/standards/output-correctness/annuity-performance-output-contract.md`
  - `docs/wiki-bi/standards/output-correctness/annuity-income-output-contract.md`
  - `docs/wiki-bi/standards/output-correctness/annual-award-output-contract.md`
  - `docs/wiki-bi/standards/output-correctness/annual-loss-output-contract.md`

Required conclusion:
- delete-scope / refresh-key semantics are fact-publication replacement contracts, not business-identity grain
- refresh keys decide overwrite boundary, not the full semantic meaning of the published record family

Required governance posture:
- `recommendation_status: claim_level_only`
- `semantic_scope_type: runtime_carrier`

---

### Task 3: Mine event-domain current-row contract lookup

**Files:**
- Create: `docs/wiki-bi/_meta/legacy-semantic-map/claims/wave-2026-04-17-semantic-governance-reframe/semantic/claim-wave-2026-04-17-semantic-governance-reframe-event-domain-current-row-contract-lookup.yaml`
- Read: `E:\Projects\WorkDataHub\docs\domains\annual_award-capability-map.md`
- Read: `E:\Projects\WorkDataHub\docs\domains\annual_loss-capability-map.md`
- Read: `E:\Projects\WorkDataHub\tests\slice_tests\test_j_real_effect_guards.py`
- Read: `docs/wiki-bi/standards/output-correctness/annual-award-output-contract.md`
- Read: `docs/wiki-bi/standards/output-correctness/annual-loss-output-contract.md`
- Read: `docs/wiki-bi/evidence/annual-award-field-processing-evidence.md`
- Read: `docs/wiki-bi/evidence/annual-loss-field-processing-evidence.md`
- Read: `docs/wiki-bi/evidence/identity-and-lookup-evidence.md`

- [ ] **Step 1: Gather temporal lookup evidence**

Minimum evidence:
- one `legacy_doc` source from each event-domain capability map
- one `legacy_test` or `legacy_code` source proving current-row filtering or ordered lookup
- current supporting pages from both output contracts

- [ ] **Step 2: Author the claim with this exact target**

Required claim shape:

- `claim_scope: semantic`
- `claim_target_id: sem-rule-event-domain-current-row-contract-lookup`
- `compiled_into` must include:
  - `docs/wiki-bi/standards/output-correctness/annual-award-output-contract.md`
  - `docs/wiki-bi/standards/output-correctness/annual-loss-output-contract.md`
  - `docs/wiki-bi/evidence/identity-and-lookup-evidence.md`

Required conclusion:
- event-domain plan-code enrichment is a current-row temporal lookup contract, not a general replay of historical contract versions
- preserving source value, current-row lookup, and domain default fallback are distinct enrichment stages

Required governance posture:
- `recommendation_status: claim_level_only`
- `semantic_scope_type: runtime_carrier`

---

### Task 4: Mine customer-master derived signal provenance

**Files:**
- Create: `docs/wiki-bi/_meta/legacy-semantic-map/claims/wave-2026-04-17-semantic-governance-reframe/semantic/claim-wave-2026-04-17-semantic-governance-reframe-customer-master-derived-signal-provenance.yaml`
- Read: `E:\Projects\WorkDataHub\config\foreign_keys.yml`
- Read: `E:\Projects\WorkDataHub\docs\business-background\客户主数据回填与状态来源分析.md`
- Read: `E:\Projects\WorkDataHub\docs\verification_guide_real_data.md`
- Read: `E:\Projects\WorkDataHub\docs\domains\annuity_performance-capability-map.md`
- Read: `E:\Projects\WorkDataHub\docs\domains\annuity_income-capability-map.md`
- Read: `docs/wiki-bi/evidence/customer-master-signals-evidence.md`
- Read: `docs/wiki-bi/evidence/reference-and-backfill-evidence.md`
- Read: `docs/wiki-bi/standards/output-correctness/output-correctness.md`

- [ ] **Step 1: Gather derived-signal evidence**

Minimum evidence:
- one `legacy_config` source from `foreign_keys.yml`
- one `legacy_doc` business-background source
- one `legacy_doc` verification source
- one annuity-performance and one annuity-income capability-map source

- [ ] **Step 2: Author the claim with this exact target**

Required claim shape:

- `claim_scope: semantic`
- `claim_target_id: sem-rule-customer-master-derived-signal-provenance`
- `compiled_into` must include:
  - `docs/wiki-bi/evidence/customer-master-signals-evidence.md`
  - `docs/wiki-bi/evidence/reference-and-backfill-evidence.md`
  - `docs/wiki-bi/standards/output-correctness/output-correctness.md`

Required conclusion:
- customer-master signals are derived outputs with distinct provenance families such as dominant-value, breadth-count, breadth-list, classification, and timeline-tag
- these signals must not be collapsed into raw fact publication or snapshot status

Required governance posture:
- `recommendation_status: claim_level_only`
- `semantic_scope_type: semantic_object`

---

### Task 5: Mine workbook discovery and version arbitration

**Files:**
- Create: `docs/wiki-bi/_meta/legacy-semantic-map/claims/wave-2026-04-17-semantic-governance-reframe/semantic/claim-wave-2026-04-17-semantic-governance-reframe-workbook-discovery-version-arbitration.yaml`
- Read: `E:\Projects\WorkDataHub\config\data_sources.yml`
- Read: `E:\Projects\WorkDataHub\src\work_data_hub\io\connectors\version_scanner.py`
- Read: `E:\Projects\WorkDataHub\src\work_data_hub\io\connectors\discovery\service.py`
- Read: `E:\Projects\WorkDataHub\tests\integration\io\test_version_detection.py`
- Read: `E:\Projects\WorkDataHub\docs\domains\annuity_performance-capability-map.md`
- Read: `E:\Projects\WorkDataHub\docs\domains\annuity_income-capability-map.md`
- Read: `E:\Projects\WorkDataHub\docs\domains\annual_award-capability-map.md`
- Read: `E:\Projects\WorkDataHub\docs\domains\annual_loss-capability-map.md`
- Read: `docs/wiki-bi/evidence/annuity-workbook-family-evidence.md`
- Read: `docs/wiki-bi/evidence/business-collection-workbook-variants-evidence.md`
- Read: `docs/wiki-bi/standards/input-reality/input-reality-contracts.md`

- [ ] **Step 1: Gather discovery evidence**

Minimum evidence:
- one `legacy_config` source from `data_sources.yml`
- one `legacy_code` source from `version_scanner.py`
- one `legacy_code` source from `discovery/service.py`
- one `legacy_test` source from `test_version_detection.py`
- one annuity-family and one business-collection capability-map source

- [ ] **Step 2: Author the claim with this exact target**

Required claim shape:

- `claim_scope: semantic`
- `claim_target_id: sem-rule-workbook-discovery-version-arbitration`
- `compiled_into` must include:
  - `docs/wiki-bi/evidence/annuity-workbook-family-evidence.md`
  - `docs/wiki-bi/evidence/business-collection-workbook-variants-evidence.md`
  - `docs/wiki-bi/standards/input-reality/input-reality-contracts.md`

Required conclusion:
- directory scanning and highest-version arbitration are operator/runtime admission contracts, not low-level plumbing
- shared workbook family or folder ancestry does not collapse separate domain sheet contracts into one domain

Required governance posture:
- `recommendation_status: claim_level_only`
- `semantic_scope_type: runtime_carrier`

---

### Task 6: Main-thread review, compile, and verification

**Files:**
- Review: `docs/wiki-bi/_meta/legacy-semantic-map/claims/wave-2026-04-17-semantic-governance-reframe/semantic/*.yaml`
- Modify via compile/report only: `docs/wiki-bi/_meta/legacy-semantic-map/manifest.json`
- Modify via compile/report only: `docs/wiki-bi/_meta/legacy-semantic-map/semantic/index.yaml`
- Modify via compile/report only: `docs/wiki-bi/_meta/legacy-semantic-map/reports/current/*.json`
- Modify via compile/report only: `docs/wiki-bi/_meta/legacy-semantic-map/reports/waves/wave-2026-04-17-semantic-governance-reframe/*`

- [ ] **Step 1: Validate each new claim**

Each claim must satisfy:
- path under the active-wave `semantic/` claim directory
- no canonical registry writes by workers
- durable pages are existing wiki pages
- current wiki is used only as a witness or `compiled_into` target

- [ ] **Step 2: Run the temp-copy probe loop**

Run:

```powershell
uv run python -m scripts.legacy_semantic_map.probe --registry-root docs/wiki-bi/_meta/legacy-semantic-map --wave-id wave-2026-04-17-semantic-governance-reframe --reruns 2
```

Expected:
- `stable_after_final_rerun` is `true`

- [ ] **Step 3: Run authoritative pilot twice if immutability warm-up appears**

Run:

```powershell
uv run python -m scripts.legacy_semantic_map.pilot --registry-root docs/wiki-bi/_meta/legacy-semantic-map --wave-id wave-2026-04-17-semantic-governance-reframe
```

If `reports/current/integrity-status.json` shows `mutable_accepted_claims_detected`, rerun the same command once more.

- [ ] **Step 4: Run semantic-map regression coverage**

Run:

```powershell
uv run pytest tests/contracts tests/integration -k legacy_semantic_map -v
```

Expected:
- PASS

---

## Self-Review

### 1. Scope coverage
- This round targets one input/discovery boundary, one publication/output boundary, one temporal lookup boundary, and one derived-signal semantic boundary.
- Each target maps to a still-open first-wave coverage gap.

### 2. Placeholder scan
- Exact claim files are named.
- Exact legacy evidence families are named.
- Exact verification commands are named.

### 3. Overlap control
- No task duplicates the previous round's four claims.
- Existing `reference_sync`, queue recovery, manual customer-mdm boundary, and standalone-tooling adjacency claims remain untouched.

---

Plan complete and saved to `docs/superpowers/plans/2026-04-19-workdatahubpro-legacy-semantic-deep-dig-round-2.md`.

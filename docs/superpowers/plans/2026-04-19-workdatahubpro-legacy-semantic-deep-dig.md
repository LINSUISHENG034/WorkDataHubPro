# WorkDataHub Legacy Semantic Deep Dig Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development. Steps use checkbox (`- [ ]`) syntax for tracking. Subagents may write only under `docs/wiki-bi/_meta/legacy-semantic-map/claims/wave-2026-04-17-semantic-governance-reframe/`. Main-thread-only steps own canonical compile, manifest, and report writes.

**Goal:** Use `docs/wiki-bi/_meta/legacy-semantic-map` to dig deeper into `E:\Projects\WorkDataHub`, add four new successor-wave semantic claims, and regenerate the active-wave semantic-map outputs without violating the single-writer rules.

**Architecture:** Keep the active wave `wave-2026-04-17-semantic-governance-reframe` as the only writable semantic-map wave. Subagents do bounded legacy evidence mining and author one claim file each under the active wave. The main thread reviews those proposal-grade claims, then runs the probe/pilot compile loop so canonical registry files and reports are regenerated in one place.

**Tech Stack:** Markdown plan docs, YAML claim artifacts, Python semantic-map scripts under `scripts/legacy_semantic_map/`, `uv`, `pytest`, legacy repo evidence under `E:\Projects\WorkDataHub`

---

## File Structure

### Planning and coordination
- Create: `docs/superpowers/plans/2026-04-19-workdatahubpro-legacy-semantic-deep-dig.md`

### Subagent-owned active-wave claim files
- Create: `docs/wiki-bi/_meta/legacy-semantic-map/claims/wave-2026-04-17-semantic-governance-reframe/semantic/claim-wave-2026-04-17-semantic-governance-reframe-customer-mdm-manual-runtime-boundary.yaml`
- Create: `docs/wiki-bi/_meta/legacy-semantic-map/claims/wave-2026-04-17-semantic-governance-reframe/semantic/claim-wave-2026-04-17-semantic-governance-reframe-reference-sync-governance-bridge.yaml`
- Create: `docs/wiki-bi/_meta/legacy-semantic-map/claims/wave-2026-04-17-semantic-governance-reframe/semantic/claim-wave-2026-04-17-semantic-governance-reframe-company-lookup-queue-publication-boundary.yaml`
- Create: `docs/wiki-bi/_meta/legacy-semantic-map/claims/wave-2026-04-17-semantic-governance-reframe/semantic/claim-wave-2026-04-17-semantic-governance-reframe-standalone-tooling-operator-adjacency.yaml`

### Main-thread-generated canonical outputs
- Modify via compile/report only: `docs/wiki-bi/_meta/legacy-semantic-map/manifest.json`
- Modify via compile/report only: `docs/wiki-bi/_meta/legacy-semantic-map/semantic/index.yaml`
- Modify via compile/report only: `docs/wiki-bi/_meta/legacy-semantic-map/semantic/rules/*.yaml`
- Modify via compile/report only: `docs/wiki-bi/_meta/legacy-semantic-map/semantic/lifecycles/*.yaml`
- Modify via compile/report only: `docs/wiki-bi/_meta/legacy-semantic-map/reports/current/coverage-status.json`
- Modify via compile/report only: `docs/wiki-bi/_meta/legacy-semantic-map/reports/current/integrity-status.json`
- Modify via compile/report only: `docs/wiki-bi/_meta/legacy-semantic-map/reports/waves/wave-2026-04-17-semantic-governance-reframe/*.json`
- Modify via compile/report only: `docs/wiki-bi/_meta/legacy-semantic-map/reports/waves/wave-2026-04-17-semantic-governance-reframe/*.md`

---

## Excavation Checklist

- [ ] Lock the writable denominator to `wave-2026-04-17-semantic-governance-reframe`; do not reopen any closed wave.
- [ ] Keep subagent writes inside `claims/wave-2026-04-17-semantic-governance-reframe/semantic/`.
- [ ] Use legacy repo primary evidence first: `legacy_doc`, `legacy_config`, `legacy_code`, `legacy_test`.
- [ ] Treat current wiki pages only as durable targets or supporting witnesses, not authoritative primary semantics.
- [ ] Mine only areas that are still candidate-grade or under-evidenced in the active successor wave.
- [ ] Avoid duplicating existing successor-wave claims:
  - `company-lookup-queue-recovery-cycle`
  - `reference-sync-preload-cycle`
  - `reference-sync-state`
  - `reference-sync-inventory`
  - `first-wave-artifact-operator-evidence`
  - `enrichment-index-cache-boundary`
  - `eqc-persistence-layering`
- [ ] For each new claim, make the business/runtime conclusion explicit and map it to existing durable pages.
- [ ] Compile new claims together with the full active-wave accepted set, not in isolation.
- [ ] Validate with both a temp-copy probe loop and an authoritative pilot run before closing the task.

---

### Task 1: Freeze the dig targets and ownership

**Files:**
- Create: `docs/superpowers/plans/2026-04-19-workdatahubpro-legacy-semantic-deep-dig.md`
- Read: `docs/wiki-bi/_meta/legacy-semantic-map/waves/index.yaml`
- Read: `docs/wiki-bi/_meta/legacy-semantic-map/candidates/subsystem-candidates.yaml`
- Read: `docs/wiki-bi/_meta/legacy-semantic-map/candidates/object-candidates.yaml`
- Read: `docs/superpowers/specs/2026-04-11-workdatahubpro-first-wave-legacy-coverage-matrix.md`

- [ ] **Step 1: Confirm the active-wave and candidate baseline**

Run:

```powershell
Get-Content docs/wiki-bi/_meta/legacy-semantic-map/waves/index.yaml
Get-Content docs/wiki-bi/_meta/legacy-semantic-map/candidates/subsystem-candidates.yaml
Get-Content docs/wiki-bi/_meta/legacy-semantic-map/candidates/object-candidates.yaml
```

Expected:
- active wave is `wave-2026-04-17-semantic-governance-reframe`
- deferred candidates include:
  - `cand-customer-mdm-manual-runtime-boundary`
  - `cand-company-lookup-queue-publication-boundary`
  - `cand-reference-sync-governance-bridge`

- [ ] **Step 2: Freeze this round's four dig targets**

Use exactly these four bounded targets:

1. `customer-mdm` manual runtime boundary
2. `reference_sync` governance bridge
3. `company_lookup_queue` publication boundary
4. `standalone tooling` operator adjacency

Do not add a fifth target in the same round unless one of the four proves invalid.

- [ ] **Step 3: Assign disjoint subagent write ownership**

Ownership map:

- Worker A owns `claim-wave-2026-04-17-semantic-governance-reframe-customer-mdm-manual-runtime-boundary.yaml`
- Worker B owns `claim-wave-2026-04-17-semantic-governance-reframe-reference-sync-governance-bridge.yaml`
- Worker C owns `claim-wave-2026-04-17-semantic-governance-reframe-company-lookup-queue-publication-boundary.yaml`
- Worker D owns `claim-wave-2026-04-17-semantic-governance-reframe-standalone-tooling-operator-adjacency.yaml`

- [ ] **Step 4: Freeze the verification stack**

Use these exact commands after the four claim files exist:

```powershell
uv run python -m scripts.legacy_semantic_map.probe --registry-root docs/wiki-bi/_meta/legacy-semantic-map --wave-id wave-2026-04-17-semantic-governance-reframe --reruns 2
uv run python -m scripts.legacy_semantic_map.pilot --registry-root docs/wiki-bi/_meta/legacy-semantic-map --wave-id wave-2026-04-17-semantic-governance-reframe
uv run pytest tests/contracts tests/integration -k legacy_semantic_map -v
```

Expected:
- probe loop reports `stable_after_final_rerun = true`
- pilot emits compiled claim ids for the active successor wave
- semantic-map contract and integration suite passes

---

### Task 2: Mine `customer-mdm` manual runtime boundary

**Files:**
- Create: `docs/wiki-bi/_meta/legacy-semantic-map/claims/wave-2026-04-17-semantic-governance-reframe/semantic/claim-wave-2026-04-17-semantic-governance-reframe-customer-mdm-manual-runtime-boundary.yaml`
- Read: `E:\Projects\WorkDataHub\src\work_data_hub\cli\__main__.py`
- Read: `E:\Projects\WorkDataHub\src\work_data_hub\cli\customer_mdm\*.py`
- Read: `E:\Projects\WorkDataHub\src\work_data_hub\customer_mdm\*.py`
- Read: `E:\Projects\WorkDataHub\docs\deployment_run_guide.md`
- Read: `docs/wiki-bi/surfaces/customer-mdm-commands.md`
- Read: `docs/wiki-bi/evidence/customer-mdm-lifecycle-evidence.md`

- [ ] **Step 1: Gather the legacy primary evidence**

Required evidence minimum:
- at least one `legacy_doc` source from `docs/deployment_run_guide.md`
- at least two `legacy_code` sources spanning both:
  - CLI dispatch under `src/work_data_hub/cli/`
  - lifecycle implementation under `src/work_data_hub/customer_mdm/`

- [ ] **Step 2: Author the claim with this exact semantic target**

Claim requirements:

- `claim_scope: semantic`
- `claim_target_id: sem-lifecycle-customer-mdm-manual-runtime-boundary`
- include `compiled_into`:
  - `docs/wiki-bi/surfaces/customer-mdm-commands.md`
  - `docs/wiki-bi/evidence/customer-mdm-lifecycle-evidence.md`

Required conclusion:
- `customer-mdm` commands are a manual operator/runtime boundary outside hook-only execution.
- `sync`, `snapshot`, `init-year`, `validate`, and `cutover` must be described as distinct operator controls, not aliases for one hidden hook chain.

Required governance posture:
- `recommendation_status: claim_level_only`
- `semantic_scope_type: runtime_carrier`

- [ ] **Step 3: Reject overlap with existing successor-wave lifecycle claims**

The new claim must not restate:
- yearly customer-status formula meaning
- `status_year` identity anchor definition
- strategic ratchet semantics

It should focus on manual runtime boundary and command-surface separation only.

---

### Task 3: Mine `reference_sync` governance bridge

**Files:**
- Create: `docs/wiki-bi/_meta/legacy-semantic-map/claims/wave-2026-04-17-semantic-governance-reframe/semantic/claim-wave-2026-04-17-semantic-governance-reframe-reference-sync-governance-bridge.yaml`
- Read: `E:\Projects\WorkDataHub\config\reference_sync.yml`
- Read: `E:\Projects\WorkDataHub\src\work_data_hub\orchestration\reference_sync_ops.py`
- Read: `E:\Projects\WorkDataHub\src\work_data_hub\io\repositories\sync_state_repository.py`
- Read: `E:\Projects\WorkDataHub\src\work_data_hub\domain\reference_backfill\sync_models.py`
- Read: `docs/wiki-bi/surfaces/reference-sync.md`
- Read: `docs/wiki-bi/evidence/reference-sync-runtime-and-state-evidence.md`

- [ ] **Step 1: Gather the legacy and replacement evidence**

Required evidence minimum:
- `legacy_config` source: `config/reference_sync.yml`
- `legacy_code` sources:
  - `src/work_data_hub/orchestration/reference_sync_ops.py`
  - `src/work_data_hub/io/repositories/sync_state_repository.py`
- one current supporting witness from existing durable pages

- [ ] **Step 2: Author the claim with this exact semantic target**

Claim requirements:

- `claim_scope: semantic`
- `claim_target_id: sem-rule-reference-sync-governance-bridge`
- include `compiled_into`:
  - `docs/wiki-bi/surfaces/reference-sync.md`
  - `docs/wiki-bi/evidence/reference-sync-runtime-and-state-evidence.md`

Required conclusion:
- legacy `reference_sync` carries a governance bridge between authoritative target inventory / sync contract memory and the current explicit `reference_derivation -> publication` replacement path.
- replacement of the repo-native runtime must not erase the legacy target inventory and sync-contract semantics from governance memory.

Required governance posture:
- `recommendation_status: claim_level_only`
- `semantic_scope_type: runtime_carrier`

- [ ] **Step 3: Reject overlap with existing `reference_sync` claims**

Do not restate these already-covered points as the main conclusion:
- pre-load scheduling
- target inventory membership
- incremental `last_synced_at` state itself

This new claim should focus on the bridge between retained governance truth and replaced/deferred runtime.

---

### Task 4: Mine `company_lookup_queue` publication boundary

**Files:**
- Create: `docs/wiki-bi/_meta/legacy-semantic-map/claims/wave-2026-04-17-semantic-governance-reframe/semantic/claim-wave-2026-04-17-semantic-governance-reframe-company-lookup-queue-publication-boundary.yaml`
- Read: `E:\Projects\WorkDataHub\docs\guides\infrastructure\company-enrichment-service.md`
- Read: `E:\Projects\WorkDataHub\src\work_data_hub\domain\company_enrichment\lookup_queue.py`
- Read: `E:\Projects\WorkDataHub\src\work_data_hub\io\loader\company_enrichment_loader.py`
- Read: `E:\Projects\WorkDataHub\src\work_data_hub\infrastructure\enrichment\repository\enrichment_index_ops.py`
- Read: `docs/wiki-bi/surfaces/company-lookup-queue.md`
- Read: `docs/wiki-bi/evidence/operator-and-surface-evidence.md`

- [ ] **Step 1: Gather queue and persistence evidence**

Required evidence minimum:
- one `legacy_doc` source from `company-enrichment-service.md`
- at least three `legacy_code` sources spanning:
  - queue runtime
  - enrichment loader / persistence writes
  - enrichment index repository behavior

- [ ] **Step 2: Author the claim with this exact semantic target**

Claim requirements:

- `claim_scope: semantic`
- `claim_target_id: sem-rule-company-lookup-queue-publication-boundary`
- include `compiled_into`:
  - `docs/wiki-bi/surfaces/company-lookup-queue.md`
  - `docs/wiki-bi/evidence/operator-and-surface-evidence.md`

Required conclusion:
- `company_lookup_queue` and its persistence writes are identity-runtime publication carriers, not equivalents of first-wave fact publication or accepted `publication` groups.
- queue persistence and enrichment index updates must stay separated from business fact publication semantics.

Required governance posture:
- `recommendation_status: claim_level_only`
- `semantic_scope_type: runtime_carrier`

- [ ] **Step 3: Reject overlap with existing queue claims**

Do not make retry cadence, stale reset, or single-domain execution the primary output.
Those are already covered by:
- `company-lookup-queue-recovery-cycle`
- `company-lookup-queue-single-domain-boundary`

This claim must stay focused on publication/persistence boundary semantics.

---

### Task 5: Mine `standalone tooling` operator adjacency

**Files:**
- Create: `docs/wiki-bi/_meta/legacy-semantic-map/claims/wave-2026-04-17-semantic-governance-reframe/semantic/claim-wave-2026-04-17-semantic-governance-reframe-standalone-tooling-operator-adjacency.yaml`
- Read: `E:\Projects\WorkDataHub\src\work_data_hub\cli\__main__.py`
- Read: `E:\Projects\WorkDataHub\docs\deployment_run_guide.md`
- Read: `E:\Projects\WorkDataHub\src\work_data_hub\gui\eqc_query\app.py`
- Read: `E:\Projects\WorkDataHub\src\work_data_hub\gui\eqc_query\controller.py`
- Read: `docs/wiki-bi/surfaces/standalone-tooling.md`
- Read: `docs/wiki-bi/evidence/operator-and-surface-evidence.md`

- [ ] **Step 1: Gather explicit entry-surface evidence**

Required evidence minimum:
- one CLI dispatch source from `src/work_data_hub/cli/__main__.py`
- one deployment/runbook source from `docs/deployment_run_guide.md`
- one GUI implementation source under `src/work_data_hub/gui/eqc_query/`

- [ ] **Step 2: Author the claim with this exact semantic target**

Claim requirements:

- `claim_scope: semantic`
- `claim_target_id: sem-rule-standalone-tooling-operator-adjacency`
- include `compiled_into`:
  - `docs/wiki-bi/surfaces/standalone-tooling.md`
  - `docs/wiki-bi/evidence/operator-and-surface-evidence.md`

Required conclusion:
- standalone tooling surfaces are explicit operator-adjacent entrypoints, not hidden helpers and not automatic members of the rebuild core runtime.
- CLI or GUI adjacency is enough to preserve them as governance surfaces, but not enough to promote them to business-semantic canon.

Required governance posture:
- `recommendation_status: claim_level_only`
- `semantic_scope_type: runtime_carrier`

- [ ] **Step 3: Reject improper elevation**

The claim must not imply:
- all standalone tools should be rebuilt
- GUI tooling is business truth
- operator convenience surfaces are equivalent to domain ETL admission

---

### Task 6: Main-thread review, compile, and verification

**Files:**
- Review: `docs/wiki-bi/_meta/legacy-semantic-map/claims/wave-2026-04-17-semantic-governance-reframe/semantic/*.yaml`
- Modify via compile/report only: `docs/wiki-bi/_meta/legacy-semantic-map/manifest.json`
- Modify via compile/report only: `docs/wiki-bi/_meta/legacy-semantic-map/semantic/index.yaml`
- Modify via compile/report only: `docs/wiki-bi/_meta/legacy-semantic-map/reports/current/*.json`
- Modify via compile/report only: `docs/wiki-bi/_meta/legacy-semantic-map/reports/waves/wave-2026-04-17-semantic-governance-reframe/*`

- [ ] **Step 1: Review each new claim for wave/path/schema correctness**

Each new claim must satisfy:
- path under `claims/wave-2026-04-17-semantic-governance-reframe/semantic/`
- `claim_scope: semantic`
- no canonical file edits by subagents
- current wiki pages used only as supporting witnesses or `compiled_into` targets

- [ ] **Step 2: Run the temp-copy probe loop with the full active-wave set**

Run:

```powershell
uv run python -m scripts.legacy_semantic_map.probe --registry-root docs/wiki-bi/_meta/legacy-semantic-map --wave-id wave-2026-04-17-semantic-governance-reframe --reruns 2
```

Expected:
- the temp registry compiles the full active-wave claim set including the four new claims
- `stable_after_final_rerun` is `true`
- no changed files remain after the final rerun

- [ ] **Step 3: Run the authoritative active-wave compile/report**

Run:

```powershell
uv run python -m scripts.legacy_semantic_map.pilot --registry-root docs/wiki-bi/_meta/legacy-semantic-map --wave-id wave-2026-04-17-semantic-governance-reframe
```

Expected:
- `compiled_claim_ids` includes the new four claim ids
- `generated_canonical_files` includes refreshed `semantic/index.yaml`
- current and wave report paths are emitted

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
- This round covers four still-open or still-candidate semantic areas rooted in real legacy runtime/operator flow.
- Each task writes proposal-grade active-wave claims only.
- Canonical compile and reporting remain main-thread-only.

### 2. Placeholder scan
- The plan names exact claim files.
- The plan names exact legacy evidence paths.
- The plan names exact validation commands.

### 3. Overlap control
- Each task is scoped to a different surface family.
- Existing successor-wave claims are explicitly named so this round does not re-author them under new filenames.

---

Plan complete and saved to `docs/superpowers/plans/2026-04-19-workdatahubpro-legacy-semantic-deep-dig.md`.

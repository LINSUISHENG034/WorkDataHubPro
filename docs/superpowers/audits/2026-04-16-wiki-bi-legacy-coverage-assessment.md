# WorkDataHubPro Wiki BI Legacy Coverage Assessment

Date: 2026-04-16
Auditor: Codex
Purpose: Assess how completely the `docs/wiki-bi/` content in `.worktrees/docs-wiki-bi-legacy-semantic-absorption/` absorbs business semantics from `E:\Projects\WorkDataHub`.
Scope: First-wave domains plus legacy operator/runtime/config/verification surfaces that materially affect semantic understanding.

---

## 0. Executive Summary

This assessment reviewed the wiki worktree structure, the legacy repository structure, the current wiki durable pages, and the legacy source families that still carry business meaning.

Overall judgment:

- domain-semantic coverage for the four first-wave domains is high
- full legacy-semantic coverage including runtime, operator, schema, and verification surfaces is medium

Working estimate:

- first-wave domain semantics: about 75% to 85% covered
- full legacy semantic surface: about 55% to 65% covered

These percentages are qualitative module-level judgments, not line-by-line counts.

Two rounds of subagent dispatch were attempted for independent cross-checks. The first failed due to model routing errors, and the second hit usage limits before stable final findings were returned. The final report therefore relies on the main-session audit, not delegated outputs.

---

## 1. Audit Method

### 1.1 Sources Reviewed

Wiki worktree:

- `E:\Projects\WorkDataHubPro\.worktrees\docs-wiki-bi-legacy-semantic-absorption\docs\wiki-bi\`
- `E:\Projects\WorkDataHubPro\.worktrees\docs-wiki-bi-legacy-semantic-absorption\docs\superpowers\plans\2026-04-16-workdatahubpro-wiki-bi-legacy-semantic-absorption-plan.md`
- `E:\Projects\WorkDataHubPro\.worktrees\docs-wiki-bi-legacy-semantic-absorption\docs\superpowers\audits\2026-04-12-legacy-code-audit.md`
- `E:\Projects\WorkDataHubPro\.worktrees\docs-wiki-bi-legacy-semantic-absorption\docs\superpowers\audits\2026-04-12-verification-assets-search-findings.md`

Legacy repository:

- `E:\Projects\WorkDataHub\docs\domains\*`
- `E:\Projects\WorkDataHub\docs\verification_guide_real_data.md`
- `E:\Projects\WorkDataHub\docs\guides\validation\legacy-parity-validation.md`
- `E:\Projects\WorkDataHub\tests\fixtures\golden_dataset\curated\dataset_requirements.md`
- `E:\Projects\WorkDataHub\tests\slice_tests\traceability_matrix.md`
- `E:\Projects\WorkDataHub\config\*.yml`
- `E:\Projects\WorkDataHub\src\work_data_hub\domain\*`
- `E:\Projects\WorkDataHub\src\work_data_hub\customer_mdm\*`
- `E:\Projects\WorkDataHub\src\work_data_hub\orchestration\*`
- `E:\Projects\WorkDataHub\src\work_data_hub\infrastructure\enrichment\*`
- `E:\Projects\WorkDataHub\io\schema\migrations\versions\*`

### 1.2 Assessment Lens

The review used three coverage lenses:

1. domain business semantics
2. operator/runtime/persistence surfaces
3. config, schema, and verification assets that encode business meaning

Coverage was judged against the wiki's own design rule:

- domains stay thin
- stable semantics should live in concepts, standards, surfaces, and evidence pages

---

## 2. Structural Coverage Position

### 2.1 Wiki Structure Already In Place

The wiki structure is coherent and durable. It is no longer acting like a mirror of execution planning and is instead operating as a semantic synthesis layer.

Main durable buckets:

- `concepts/`
- `domains/`
- `surfaces/`
- `standards/`
- `evidence/`

This matches the intended model described in:

- `docs/wiki-bi/index.md`
- `docs/wiki-bi/_meta/wiki-design.md`

### 2.2 Legacy Structure Still Carrying Business Meaning

Meaningful legacy source families are spread across:

- `src/work_data_hub/domain/`
- `src/work_data_hub/customer_mdm/`
- `src/work_data_hub/orchestration/`
- `src/work_data_hub/infrastructure/enrichment/`
- `src/work_data_hub/cli/`
- `config/`
- `io/schema/migrations/versions/`
- `tests/slice_tests/`
- `tests/fixtures/`

The wiki now covers the domain-heavy part of that surface well, but the runtime, schema, and verification-heavy part only partially.

---

## 3. Areas Covered Well

### 3.1 First-Wave Domain Semantics

Coverage is strong for:

- `annuity_performance`
- `annuity_income`
- `annual_award`
- `annual_loss`

Each domain now has:

- a thin navigation page
- an input contract page
- an output contract page
- a field-processing evidence page

This is the strongest-covered zone in the current wiki.

### 3.2 Identity Governance

The wiki has substantially closed the gap around:

- `company_id`
- `temp_id`
- identity fallback layering
- queue and persistence being separate surfaces, not implementation noise

The identity cluster is materially stronger than a generic "lookup" summary and now captures retained, replaced, and deferred semantics.

### 3.3 Reference Sync vs Backfill

The wiki clearly distinguishes:

- authoritative pre-load via `reference_sync`
- fact-derived writeback via `backfill`

This is one of the best examples of genuine semantic absorption rather than implementation paraphrase.

### 3.4 Customer Status and Lifecycle Semantics

The wiki now has durable treatment of:

- `is_new`
- `is_winning_this_year`
- `is_loss_reported`
- `status_year`
- customer contract state vs snapshot state vs command surface

The separation between concept, lifecycle evidence, and command surface is materially improved.

### 3.5 Surface Registration

The wiki has already surfaced several important legacy objects that would otherwise stay hidden:

- `company_lookup_queue`
- `reference_sync`
- `customer-mdm` commands
- failed-record export
- unknown-names CSV
- enterprise enrichment persistence
- standalone tooling

This is a major improvement over domain-only coverage.

---

## 4. Missing Or Weak Coverage

The most important remaining gaps are not in the four headline domains. They are in the layers that define output shape, operator verification, and runtime breadth.

### 4.1 Output Entity And Schema Semantics

Coverage is weak for the business meaning encoded in legacy physical outputs and migrations.

Primary sources:

- `io/schema/migrations/versions/007_create_customer_plan_contract.py`
- `io/schema/migrations/versions/008_create_fct_customer_monthly_status.py`
- `io/schema/migrations/versions/011_create_fct_customer_plan_monthly.py`
- `io/schema/migrations/versions/009_create_bi_star_schema.py`
- `io/schema/migrations/versions/010_create_sync_product_line_trigger.py`

Current state:

- the wiki explains many status and snapshot semantics
- the wiki does not yet elevate the output entities themselves into stable semantic objects

Why this matters:

- a large part of legacy business meaning lives in output table boundaries, grain, and write-side contracts
- current pages discuss those results, but not yet as first-class governed output objects

Best next wiki targets:

- extend `standards/output-correctness/output-correctness.md`
- create or extend evidence pages focused on contract-state and snapshot output entities
- optionally add a surface or evidence page for output-schema semantics

### 4.2 Real-Data Validation And Parity Execution Semantics

Coverage is only medium for the full verification chain.

Primary sources:

- `docs/verification_guide_real_data.md`
- `docs/guides/validation/legacy-parity-validation.md`
- `tests/slice_tests/traceability_matrix.md`
- `tests/fixtures/golden_dataset/curated/dataset_requirements.md`
- `tests/fixtures/validation_results/`

Current state:

- the wiki has `real-data-validation`, `verification-assets-evidence`, and `validation-result-history-evidence`
- but it still underrepresents the full legacy validation flow: stage ordering, SQL verification path, parity artifacts, result-package semantics, and operator review expectations

Why this matters:

- legacy verification is not just "replay exists"
- it encodes what counts as proof, what reports are produced, and how operators inspect success or mismatch

Best next wiki targets:

- extend `standards/verification-method/real-data-validation.md`
- extend `evidence/verification-assets-evidence.md`
- extend `evidence/validation-result-history-evidence.md`

### 4.3 Orchestration Control-Surface Semantics

Coverage is partial for the special runtime/control surfaces beyond the fact domains.

Primary sources:

- `src/work_data_hub/orchestration/jobs.py`
- `src/work_data_hub/orchestration/schedules.py`
- `src/work_data_hub/orchestration/sensors.py`
- `src/work_data_hub/orchestration/repository.py`
- `src/work_data_hub/orchestration/reference_sync_jobs.py`
- `src/work_data_hub/cli/etl/*`

Current state:

- the wiki recognizes queue and reference sync as surfaces
- the wiki does not yet fully absorb schedule, sensor, job dispatch, recovery, and operator flow semantics as stable surface knowledge

Why this matters:

- these files carry more than execution plumbing
- they define retained runtime breadth, recovery assumptions, and operational boundaries

Best next wiki targets:

- refine `surfaces/company-lookup-queue.md`
- refine `surfaces/reference-sync.md`
- extend `evidence/operator-and-surface-evidence.md`

### 4.4 Enrichment Persistence Object-Level Semantics

Coverage is medium at the cluster level but weak at object level.

Primary sources:

- `src/work_data_hub/infrastructure/enrichment/data_refresh_service.py`
- `src/work_data_hub/infrastructure/enrichment/refresh_checkpoint.py`
- `src/work_data_hub/infrastructure/enrichment/domain_learning_service.py`
- `src/work_data_hub/infrastructure/enrichment/business_info_repository.py`
- `src/work_data_hub/infrastructure/enrichment/biz_label_repository.py`
- `src/work_data_hub/infrastructure/enrichment/repository/other_ops.py`

Current state:

- the wiki has one good persistence-surface page
- but the internal objects are still grouped more coarsely than the legacy code justifies

Why this matters:

- cache persistence, queue persistence, provider raw persistence, provider cleansed persistence, and refresh checkpoints are not the same semantic object

Best next wiki targets:

- refine `surfaces/enterprise-enrichment-persistence.md`
- extend `evidence/operator-and-surface-evidence.md`

### 4.5 Config-Driven Semantic Objects

Coverage is uneven for config families whose business meaning is currently expressed mostly through downstream effects.

Primary sources:

- `config/mappings/business_type_code.yml`
- `config/mappings/default_portfolio_code.yml`
- `config/mappings/default_plan_institution_code.yml`
- `config/domain_sources.yaml`

Current state:

- some mapping consequences are already reflected in field-processing evidence
- the config families themselves are not yet treated as stable semantic objects

Why this matters:

- these files encode classification and fallback rules that are easy to forget once only their output consequences are documented

Best next wiki targets:

- extend field-processing evidence pages where the mappings materially drive semantics
- add targeted evidence sections for config-family governance

### 4.6 Explicit Legacy Retirement Or Deferral For Non-Core Domains

Coverage is weak for legacy non-core modules that are not part of the accepted first-wave set.

Primary source:

- `config/domain_sources.yaml`

Specific example:

- `sandbox_trustee_performance`

Current state:

- the wiki correctly focuses on four confirmed domains
- but this leaves some legacy modules in an implicit state rather than an explicit `deferred` or `retired` state

Best next wiki targets:

- a governance note in evidence or meta pages
- or a dedicated deferred/retired registry page if this pattern expands

### 4.7 Evidence Strength Drift

Some current wiki pages still claim that certain legacy assets are not directly readable from the current repository context, even though the raw files were directly accessible during this assessment.

Directly re-opened in this audit:

- `E:\Projects\WorkDataHub\docs\guides\validation\legacy-parity-validation.md`
- `E:\Projects\WorkDataHub\tests\fixtures\golden_dataset\curated\dataset_requirements.md`
- `E:\Projects\WorkDataHub\tests\fixtures\validation_results\`

Why this matters:

- some findings currently classified as audit-derived or indirectly supported can be upgraded to direct source-backed findings

Best next wiki targets:

- `evidence/verification-assets-evidence.md`
- `evidence/validation-result-history-evidence.md`
- `standards/verification-method/real-data-validation.md`

---

## 5. Module-Level Judgment

| Module | Focus | Coverage Judgment |
|------|------|-------------------|
| `M1` | `annuity_performance` hidden field semantics and downstream meaning | high |
| `M2` | `annuity_income` hidden field semantics and operator-visible differences | high |
| `M3` | `annual_award` hidden multi-sheet and enrichment semantics | high |
| `M4` | `annual_loss` hidden multi-sheet and temporal lookup semantics | high |
| `M5` | identity resolution, overrides, branch mapping, enrichment persistence boundaries | medium-high |
| `M6` | reference derivation, backfill, master-data propagation, publication-facing meaning | medium-high |
| `M7` | customer status, yearly lifecycle, strategic/existing semantics, snapshot consequences | medium-high |
| `M8` | operator/runtime/verification governance | medium |

---

## 6. Priority Order For Next Coverage Work

### Priority 1

Close output-entity and schema semantics.

Reason:

- too much customer contract and snapshot meaning still floats above the physical output layer

### Priority 2

Close verification and parity execution semantics.

Reason:

- legacy verification expresses business acceptance logic, not just tooling

### Priority 3

Deepen orchestration control-surface coverage.

Reason:

- schedule, sensor, queue, sync, and recovery breadth remain under-described

### Priority 4

Split enrichment persistence objects more finely.

Reason:

- current clustering is acceptable for discovery, not yet for full semantic closure

### Priority 5

Upgrade config-family coverage and explicit retirement/defer decisions for legacy non-core modules.

Reason:

- several legacy semantic objects are visible but not yet durably adjudicated

---

## 7. Final Assessment

The current wiki has already crossed the threshold from "navigation notes" into a genuine semantic knowledge layer for the first-wave domains. It now captures the most important domain-level business semantics, identity boundaries, reference-vs-backfill distinction, and status lifecycle meaning.

The remaining gap is not mainly "more domain pages." It is the legacy semantic surface that lives in verification assets, runtime control surfaces, schema outputs, and persistence objects. Those areas are visible in the current wiki, but they are not yet absorbed with the same depth and stability as the four first-wave domains.

That means the wiki is already strong enough to support first-wave semantic reasoning, but not yet complete enough to claim broad legacy-semantic closure.

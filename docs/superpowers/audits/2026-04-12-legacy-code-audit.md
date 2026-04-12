# WorkDataHub Legacy Code Audit

Date: 2026-04-12
Auditor: Codex (Claude Code)
Purpose: Independent audit of WorkDataHub (E:\Projects\WorkDataHub) based on code analysis, not relying on legacy documentation.
Scope: All domains except sandbox_trustee_performance (explicitly excluded).

---

## 0. Executive Summary

### 0.1 CLI Command Surface (from `src/work_data_hub/cli/__main__.py` and delegated modules)

| Command | Subcommands / Modes | Purpose |
|---------|--------------------|---------|
| `etl` | configured domains: `annuity_performance`, `annuity_income`, `annual_award`, `annual_loss`, `sandbox_trustee_performance`; single-domain orchestration targets: `company_lookup_queue`, `reference_sync`; supports discovery, execution, backfill, enrichment, diagnostics, and post-hook control flags | Run fact-domain ETL and orchestration jobs |
| `auth` | `refresh` | Authentication operations |
| `eqc-refresh` | `--status` | EQC data refresh |
| `eqc-gui` | (standalone) | EQC quick query GUI (Tkinter) |
| `eqc-gui-fluent` | (standalone) | EQC quick query GUI (Modern) |
| `intranet-deploy-gui` | (standalone) | Deployment packaging GUI |
| `cleanse` | `--table`, `--domain` | Data cleansing |
| `customer-mdm sync` | | Sync contract status |
| `customer-mdm snapshot` | | Refresh monthly snapshots |
| `customer-mdm init-year` | | Initialize annual status |
| `customer-mdm validate` | | Validate status distributions |
| `customer-mdm cutover` | | Annual cutover |

**Important completeness note:** `etl` is not only a fact-domain runner. It is also the operator entrypoint for the special orchestration domains `company_lookup_queue` and `reference_sync`, which are validated in `src/work_data_hub/cli/etl/domain_validation.py` and dispatched in `src/work_data_hub/cli/etl/executors.py`.

### 0.2 Discovered Runtime / Infrastructure Systems

| System | Files | Purpose |
|--------|-------|---------|
| **Company Enrichment / Identity** | `domain/company_enrichment/`, `infrastructure/enrichment/` | `company_id` resolution, cache lookup, EQC-backed enrichment |
| **EQC Integration** | `io/connectors/eqc/`, `infrastructure/enrichment/eqc_provider.py`, `io/auth/` | External Query Cache access, auth, result persistence |
| **Lookup Queue** | `domain/company_enrichment/lookup_queue.py`, `orchestration/ops/company_enrichment.py` | Async enrichment queue and retry processing |
| **Reference Sync** | `orchestration/reference_sync_ops.py`, `domain/reference_backfill/sync_service.py`, `config/reference_sync.yml` | Sync authoritative reference data into business schema targets |
| **Customer MDM** | `customer_mdm/`, `cli/customer_mdm/`, `cli/etl/hooks.py` | Contract state, snapshots, year initialization, cutover, validation |
| **Cleansing** | `infrastructure/cleansing/`, `cli/cleanse_data.py` | Data cleansing rules and standalone cleansing operations |
| **Validation Export** | `infrastructure/validation/` | Failed-row export and validation artifacts |
| **Dagster Scheduling / Sensors** | `orchestration/schedules.py`, `orchestration/sensors.py` | Scheduled trustee runs, async enrichment, reference sync |
| **GUI Apps** | `gui/eqc_query/`, `gui/eqc_query_fluent/`, `gui/intranet_deploy/` | Standalone GUI tools |

### 0.3 Key Operations (from `orchestration/ops/`)

| Operation | File | Purpose |
|-----------|------|---------|
| `discover_files_op` | `file_processing.py` | File discovery |
| `read_data_op` | `file_processing.py` | Excel reading |
| `process_domain_op_v2` | `generic_ops.py` | Domain pipeline execution |
| `generic_backfill_refs_op` | `generic_backfill.py` | FK backfill |
| `load_op` | `loading.py` | Database write |
| `process_company_lookup_queue_op` | `company_enrichment.py` | Enrichment queue processing |
| `reference_sync_op` | `reference_sync_ops.py` | Reference table sync |

### 0.4 Post-ETL Hooks (from `cli/etl/hooks.py`)

| Order | Hook | Trigger Domain | Tables Affected |
|------|------|---------------|-----------------|
| 1 | `contract_status_sync` | `annuity_performance` | `customer.客户年金计划` |
| 2 | `year_init` | `annuity_performance` (January only) | `customer.客户年金计划` |
| 3 | `snapshot_refresh` | `annuity_performance` | `customer.客户业务月度快照`, `customer.客户计划月度快照` |

Hook order matters in code: the runtime sequence is `contract_status_sync` → `year_init` (January only) → `snapshot_refresh`, and `year_init` is a separate write path that updates `customer.客户年金计划` directly rather than acting through snapshot refresh.

---

## 1. Audit Methodology

### 1.1 Data Sources Analyzed

| Source | Purpose |
|--------|---------|
| `config/data_sources.yml` | Domain file discovery + output table definitions |
| `config/foreign_keys.yml` | FK backfill rules and target tables |
| `config/reference_sync.yml` | Reference table sync configuration |
| `config/customer_status_rules.yml` | Customer MDM status evaluation rules |
| `src/work_data_hub/domain/*/` | Domain implementation code |
| `src/work_data_hub/customer_mdm/` | Post-ETL hooks and MDM logic |
| `src/work_data_hub/orchestration/` | ETL orchestration and loading |

### 1.2 Audit Principles

- **Code is source of truth**, not documentation
- **Every table write must be traced** from config to code to DB
- **No assumption is trusted** without code evidence
- **Side effects are documented** separately from main data flows

---

## 2. Domain Inventory

### 2.1 Domains Confirmed in Code

| Domain | Directory | Status |
|--------|----------|--------|
| `annuity_performance` | `src/work_data_hub/domain/annuity_performance/` | Active |
| `annual_award` | `src/work_data_hub/domain/annual_award/` | Active |
| `annual_loss` | `src/work_data_hub/domain/annual_loss/` | Active |
| `annuity_income` | `src/work_data_hub/domain/annuity_income/` | Active |
| `company_enrichment` | `src/work_data_hub/domain/company_enrichment/` | Infrastructure (not standalone domain) |
| `reference_backfill` | `src/work_data_hub/domain/reference_backfill/` | Shared service |
| `pipelines` | `src/work_data_hub/domain/pipelines/` | Shared framework |

**Note**: `sandbox_trustee_performance` excluded per user instruction.

**Special orchestration domains outside `src/work_data_hub/domain/*` business folders:** `company_lookup_queue`, `reference_sync`.

---

## 3. Database Tables Written

### 3.1 Summary by Schema

#### `business` Schema (Fact Tables)

| Table | Source Domain | Write Mechanism | Config Location |
|-------|-------------|-----------------|-----------------|
| `规模明细` | `annuity_performance` | `load_op` (delete-insert) | `data_sources.yml` |
| `收入明细` | `annuity_income` | `load_op` (delete-insert) | `data_sources.yml` |

#### `customer` Schema

| Table | Source | Write Mechanism | Trigger |
|-------|--------|-----------------|---------|
| `中标客户明细` | `annual_award` | `load_op` | ETL |
| `流失客户明细` | `annual_loss` | `load_op` | ETL |
| `客户明细` | All domains | FK backfill (`fk_customer`) | ETL (via `generic_backfill_refs_op`) |
| `客户年金计划` | `annuity_performance` | Post-ETL hook (`contract_status_sync`) | Post-ETL |
| `客户业务月度快照` | `annuity_performance` | Post-ETL hook (`snapshot_refresh`) | Post-ETL |
| `客户计划月度快照` | `annuity_performance` | Post-ETL hook (`snapshot_refresh`) | Post-ETL |

#### `business` Schema (Reference Sync Targets)

| Table | Source | Sync Mode | Config Location |
|-------|--------|-----------|-----------------|
| `年金计划` | Legacy PostgreSQL `enterprise.annuity_plan` | upsert | `reference_sync.yml` |
| `组合计划` | Legacy PostgreSQL `enterprise.portfolio_plan` | upsert | `reference_sync.yml` |
| `组织架构` | Legacy PostgreSQL `enterprise.organization` | upsert | `reference_sync.yml` |
| `产品线` | Config file `config/reference_data/product_lines.yml` | delete-insert | `reference_sync.yml` |

#### `mapping` Schema (Reference Tables via FK Backfill)

| Table | Source Domains | FK Rule | Aggregation |
|-------|---------------|---------|-------------|
| `年金计划` | `annuity_performance`, `annuity_income` | `fk_plan` | insert-missing |
| `组合计划` | `annuity_performance`, `annuity_income` | `fk_portfolio` | insert-missing |
| `产品线` | `annuity_performance`, `annuity_income` | `fk_product_line` | insert-missing |
| `组织架构` | `annuity_performance`, `annuity_income` | `fk_organization` | insert-missing |

#### `enterprise` Schema (Enrichment / Operational Persistence)

| Table | Source / Writer | Write Mechanism |
|-------|-----------------|-----------------|
| `enrichment_requests` | lookup queue DAO, async enrichment, queue backflow | insert, status update, retry update |
| `enrichment_index` | EQC cache, domain learning, former-name handling | upsert, hit-count update, conflict delete |
| `company_name_index` | enrichment repository cache write | insert-ignore |
| `base_info` | EQC provider / refresh service | upsert |
| `business_info` | cleansing / refresh integration | upsert, best-effort update |
| `biz_label` | biz-label repository | delete + insert |

These `enterprise` tables are not first-wave fact outputs, but they are persistent legacy surfaces and cannot stay implicit in rebuild governance.

---

## 4. Complete Table Write Map

### 4.1 By Domain

#### `annuity_performance`

| Order | Table | Schema | Mechanism | PK |
|-------|-------|--------|-----------|-----|
| 1 | `规模明细` | `business` | `load_op` | `月度`, `业务类型`, `计划类型` |
| 2 | `年金计划` | `mapping` | `fk_plan` | `年金计划号` |
| 3 | `组合计划` | `mapping` | `fk_portfolio` | `组合代码` |
| 4 | `产品线` | `mapping` | `fk_product_line` | `产品线代码` |
| 5 | `组织架构` | `mapping` | `fk_organization` | `机构代码` |
| 6 | `客户明细` | `customer` | `fk_customer` | `company_id` |
| 7 | `客户年金计划` | `customer` | `contract_status_sync` hook | SCD2 |
| 8 | `客户业务月度快照` | `customer` | `snapshot_refresh` hook | `company_id`, `产品线代码`, `月度` |
| 9 | `客户计划月度快照` | `customer` | `snapshot_refresh` hook | `company_id`, `计划代码`, `月度` |

#### `annual_award`

| Order | Table | Schema | Mechanism | PK |
|-------|-------|--------|-----------|-----|
| 1 | `中标客户明细` | `customer` | `load_op` | `上报月份`, `业务类型` |
| 2 | `客户明细` | `customer` | `fk_customer` | `company_id` |

#### `annual_loss`

| Order | Table | Schema | Mechanism | PK |
|-------|-------|--------|-----------|-----|
| 1 | `流失客户明细` | `customer` | `load_op` | `上报月份`, `业务类型` |
| 2 | `客户明细` | `customer` | `fk_customer` | `company_id` |

#### `annuity_income`

| Order | Table | Schema | Mechanism | PK |
|-------|-------|--------|-----------|-----|
| 1 | `收入明细` | `business` | `load_op` | `月度`, `业务类型`, `计划类型` |
| 2 | `年金计划` | `mapping` | `fk_plan` | `年金计划号` |
| 3 | `组合计划` | `mapping` | `fk_portfolio` | `组合代码` |
| 4 | `产品线` | `mapping` | `fk_product_line` | `产品线代码` |
| 5 | `组织架构` | `mapping` | `fk_organization` | `机构代码` |
| 6 | `客户明细` | `customer` | `fk_customer` | `company_id` |

### 4.2 Special Orchestration And Manual Operator Write Paths

| Entry Point | Write Surface | Notes |
|-------------|---------------|-------|
| `etl --domains reference_sync` | `business.年金计划`, `business.组合计划`, `business.组织架构`, `business.产品线` | Special single-domain orchestration target, not a normal fact domain |
| `etl --domains company_lookup_queue` | `enterprise.enrichment_requests` plus enrichment persistence surfaces on successful lookup | Queue status is always updated; successful EQC paths may also write `base_info`, `enrichment_index`, and cache tables |
| `customer-mdm sync` | `customer.客户年金计划` | Manual operator entrypoint for contract-state sync |
| `customer-mdm snapshot` | `customer.客户业务月度快照`, `customer.客户计划月度快照` | Manual operator entrypoint for snapshot refresh |
| `customer-mdm init-year` | `customer.客户年金计划` | January lifecycle / annual status initialization |
| `customer-mdm cutover` | `customer.客户年金计划` | Annual close + insert cutover path distinct from ETL hooks |
| `customer-mdm validate` | read-only | Validation command; important operator surface but not a write path |

---

## 5. Side Effects and Artifacts

### 5.1 File-Based Outputs

| Artifact | Source Domain | Location | Trigger |
|----------|--------------|----------|---------|
| `unknown_names_csv` | `annuity_performance` | Domain helper export path | When unresolved names exist + `export_unknown_names=True` |
| `unknown_names_csv` | `annuity_income` | Domain helper export path | When unresolved names exist + `export_unknown_names=True` |
| failed-record CSV (`FailureExporter`) | `annuity_performance` | Validation output directory | When pipeline drops rows and a session ID is active |
| failed-record CSV (`FailureExporter`) | `annuity_income` | Validation output directory | When pipeline drops rows and a session ID is active |

### 5.2 Post-ETL Hook Chains (annuity_performance only)

| Order | Hook | Purpose | Tables Affected |
|------|------|---------|-----------------|
| 1 | `contract_status_sync` | SCD2 contract status tracking | `客户年金计划` |
| 2 | `year_init` | January-specific lifecycle initialization | `客户年金计划` |
| 3 | `snapshot_refresh` | Monthly snapshot refresh | `客户业务月度快照`, `客户计划月度快照` |

### 5.3 Manual Operator Commands Outside ETL Hook Execution

| Command | Purpose | Primary Tables |
|---------|---------|----------------|
| `customer-mdm sync` | Re-run contract sync manually | `customer.客户年金计划` |
| `customer-mdm snapshot` | Re-run monthly snapshots manually | `customer.客户业务月度快照`, `customer.客户计划月度快照` |
| `customer-mdm init-year` | Re-run year initialization manually | `customer.客户年金计划` |
| `customer-mdm cutover` | Perform annual cutover | `customer.客户年金计划` |
| `customer-mdm validate` | Validate status distribution | read-only |

---

## 6. Cross-Domain Dependencies

| Dependency | Direction | Impact |
|------------|-----------|--------|
| `annual_award` → `annuity_performance` | Downstream | Award facts populate `is_winning_this_year` via snapshot |
| `annual_loss` → `annuity_performance` | Downstream | Loss facts populate `is_loss_reported` via snapshot |
| `annuity_income` → `annuity_performance` | Indirect | Both use same file pattern, different sheets |
| `annuity_performance` / `customer-mdm` → `annual_award` | Upstream lookup dependency | Award rows query `customer.客户年金计划` to enrich missing `年金计划号` |
| `annuity_performance` / `customer-mdm` → `annual_loss` | Upstream lookup dependency | Loss rows query `customer.客户年金计划` to enrich missing `年金计划号` |
| identity / EQC runtime → all first-wave domains | Shared runtime dependency | `company_id` resolution behavior, cache state, and fallback semantics are cross-domain rather than per-domain |

---

## 7. Findings: Documentation vs Code Discrepancies

### 7.1 Undocumented Or Under-Modeled In Legacy Capability Maps

| Item | Evidence | Severity |
|------|----------|----------|
| `company_lookup_queue` special ETL domain | Exists in CLI validation and executor dispatch, but not as a normal domain capability map | High |
| `reference_sync` as an operator domain with its own schedule/state | Exists in CLI dispatch, Dagster schedule, and sync-state persistence | High |
| enterprise enrichment persistence (`base_info`, `business_info`, `biz_label`, `enrichment_index`, `enrichment_requests`, `company_name_index`) | Real write paths exist in enrichment and refresh code, but are not represented as first-class legacy surfaces | High |
| manual `customer-mdm` operator commands | CLI subcommands execute writes outside the ETL hook path | Medium |
| `unknown_names_csv` and failed-record CSV artifacts | Real operator artifacts exist in `annuity_performance` and `annuity_income` | Medium |
| event-domain plan-code lookup from `customer.客户年金计划` | Real cross-domain query path in `annual_award` and `annual_loss` pipelines | Medium |
| Multi-domain FK backfill ordering | FK rules have `depends_on`, not documented | Low |

### 7.2 Legacy Surfaces Only Partially Represented In Current WorkDataHubPro Coverage Matrix

| Surface | Current Matrix Position | Why Partial |
|---------|------------------------|-------------|
| customer MDM output semantics | covered semantically by `AP-006`, `CT-004`, `CT-009` | output tables exist in the matrix, but manual operator entrypoints are not registered as separate assets |
| async lookup queue | implied by deferred identity/provider work | queue runtime and `enterprise.enrichment_requests` surface do not have an explicit row |
| reference sync | implied by cross-cutting follow-on work | `business` schema reference-sync targets and sync-state/runtime are not registered as an explicit row |
| enterprise enrichment persistence | partially implied by identity parity follow-on work | persistent EQC/cache tables are not enumerated as separate accept/defer/retire surfaces |
| operator artifacts (`unknown_names_csv`, failed-record CSV) | `AI-004` covers only part of the artifact story | `annuity_performance` artifact parity and failure-export behavior are not explicitly registered |
| GUI / standalone cleansing surfaces | not registered | these must be explicitly deferred or retired instead of remaining implied |

---

## 8. Complete System Inventory

### 8.1 Company Enrichment System (company_id Resolution)

| Component | File | Purpose |
|-----------|------|---------|
| `CompanyEnrichmentService` | `domain/company_enrichment/service.py` | Main enrichment orchestration |
| `CompanyIdResolver` | `infrastructure/enrichment/company_id_resolver.py` | Resolution strategy chain |
| `EnrichmentContext` | `infrastructure/enrichment/factory.py` | Context factory |
| `EnrichmentIndex` | `infrastructure/enrichment/repository/enrichment_index_ops.py` | DB cache |
| `EqcProvider` | `infrastructure/enrichment/eqc_provider.py` | External EQC API |
| `LookupQueue` | `domain/company_enrichment/lookup_queue.py` | Async queue processing |
| `CsvExporter` | `infrastructure/enrichment/csv_exporter.py` | Export enrichment results |
| `DomainLearningService` | `infrastructure/enrichment/domain_learning_service.py` | Pattern learning |

**Resolution Strategy Chain (per domain capability maps):**
1. YAML override → 2. DB cache (enrichment_index) → 3. EQC provider → 4. Temp ID generation

### 8.2 EQC Integration System

| Component | File | Purpose |
|-----------|------|---------|
| `EqcClient` | `io/connectors/eqc_client.py` | HTTP client |
| `EqcAuthHandler` | `io/auth/eqc_auth_handler.py` | Authentication |
| `AutoEqcAuth` | `io/auth/auto_eqc_auth.py` | Auto login via browser |
| `EqcParsers` | `io/connectors/eqc/parsers.py` | Response parsing |
| `DataRefreshService` | `infrastructure/enrichment/data_refresh_service.py` | Refresh operations |

### 8.3 Cleansing System

| Component | File | Purpose |
|-----------|------|---------|
| `BusinessInfoCleanser` | `infrastructure/cleansing/business_info_cleanser.py` | Business info cleansing |
| `BizLabelParser` | `infrastructure/cleansing/biz_label_parser.py` | Biz label parsing |
| `RuleEngine` | `infrastructure/cleansing/rule_engine.py` | Cleansing rule execution |
| `StringRules` | `infrastructure/cleansing/rules/string_rules.py` | String normalization |
| `NumericRules` | `infrastructure/cleansing/rules/numeric_rules.py` | Numeric validation |
| `DateRules` | `infrastructure/cleansing/rules/date_rules.py` | Date parsing |

**CLI Command:** `python -m work_data_hub.cli cleanse --table <business_info|biz_label|all>`

### 8.4 Validation and Failure Export System

| Component | File | Purpose |
|-----------|------|---------|
| `FailureExporter` | `infrastructure/validation/failure_exporter.py` | Export failures to CSV |
| `FailedRecord` | `infrastructure/validation/failed_record.py` | Record model |
| `export_error_csv` | `infrastructure/validation/report_generator.py` | Error CSV export |
| `export_failed_records` | `infrastructure/validation/error_handler.py` | Failure record export |

### 8.5 GUI Applications

| Application | Directory | Purpose |
|-------------|-----------|---------|
| EQC Query (Tkinter) | `gui/eqc_query/` | Quick EQC lookup GUI |
| EQC Query Fluent | `gui/eqc_query_fluent/` | Modern EQC lookup GUI |
| Intranet Deploy | `gui/intranet_deploy/` | Deployment packaging |

### 8.6 Reference Sync System

| Component | File | Purpose |
|-----------|------|---------|
| `reference_sync_ops` | `orchestration/reference_sync_ops.py` | Sync orchestration |
| `SyncService` | `domain/reference_backfill/sync_service.py` | Sync execution |
| `HybridService` | `domain/reference_backfill/hybrid_service.py` | Hybrid backfill |
| `LegacyMySqlConnector` | `io/connectors/legacy_mysql_connector.py` | Legacy DB |
| `PostgresSourceAdapter` | `io/connectors/postgres_source_adapter.py` | PostgreSQL source adapter |

**Current config truth:** `reference_sync.yml` now points at PostgreSQL-backed sources and writes to `business` schema targets, not `enterprise` schema targets.

### 8.7 Customer MDM Operator System

| Component | File | Purpose |
|-----------|------|---------|
| `sync_contract_status` | `customer_mdm/contract_sync.py` | Build and maintain `customer.客户年金计划` |
| `refresh_monthly_snapshot` | `customer_mdm/snapshot_refresh.py` | Refresh business and plan monthly snapshots |
| `initialize_year_status` | `customer_mdm/year_init.py` | January lifecycle initialization for contract status |
| `annual_cutover` | `customer_mdm/year_init.py` | Annual close + insert cutover for contract records |
| `validate_status_distribution` | `customer_mdm/validation.py` | Read-only validation of customer status outputs |

### 8.8 Scheduling And Sensor System

| Component | File | Purpose |
|-----------|------|---------|
| `async_enrichment_schedule` | `orchestration/schedules.py` | Hourly queue processing schedule |
| `reference_sync_schedule` | `orchestration/schedules.py` | Daily reference sync schedule |
| trustee daily schedule | `orchestration/schedules.py` | Daily sandbox trustee processing |
| enrichment queue sensors | `orchestration/sensors.py` | Trigger queue processing based on pending workload |

---

## 9. Coverage Assessment for WorkDataHubPro

### 9.1 Tables That Must Be Covered

Based on this audit, `WorkDataHubPro` must explicitly account for the following first-wave data outputs. "Account for" means: rebuild, defer with reason, or retire with rationale. It does not always mean "rebuild immediately in Phase B/C."

**Fact Tables:**
- `business.规模明细`
- `business.收入明细`
- `customer.中标客户明细`
- `customer.流失客户明细`

**Reference Tables (via FK Backfill):**
- `mapping.年金计划`
- `mapping.组合计划`
- `mapping.产品线`
- `mapping.组织架构`
- `customer.客户明细`

**MDM Tables (Post-ETL Hooks):**
- `customer.客户年金计划`
- `customer.客户业务月度快照`
- `customer.客户计划月度快照`

**Baseline first-wave output surface: 12 tables across 3 active output schemas (`business`, `customer`, `mapping`)**

Separate from that first-wave output surface, the legacy system also owns persistent operational tables under `enterprise` and authoritative reference-sync targets under `business`. Those are governed legacy surfaces, not ignorable implementation detail.

### 9.2 Legacy Persistence / Operator Surfaces Requiring Explicit Governance Decisions

These surfaces are not fully closed by the currently accepted first-wave slices and should be registered explicitly in coverage or retirement decisions:

| Surface | Current Position In WorkDataHubPro Governance | Impact |
|--------|----------------------------------------------|--------|
| identity resolution core chain | partially accepted (`AP-003`) | High |
| live EQC/provider mode, provider auth, and cache persistence breadth | deferred / partial via `CT-006`, refactor-program cross-cutting track | High |
| async lookup queue runtime (`enterprise.enrichment_requests`) | not explicitly registered as its own row | High |
| reference sync runtime and `business`-schema authoritative targets | not explicitly registered as its own row | High |
| enterprise enrichment persistence (`base_info`, `business_info`, `biz_label`, `enrichment_index`, `company_name_index`) | partially implied by identity parity follow-on work | High |
| manual `customer-mdm` operator commands | semantics partially covered, operator surfaces not explicitly registered | High |
| validation-export / failed-row artifact parity | partially represented by `AI-004`; not closed for all domains | Medium |
| standalone `cleanse` command | not explicitly registered | Medium |
| GUI applications | not explicitly registered | Low |

### 9.3 Critical Gaps in New Project Coverage

Based on the active blueprint and first-wave coverage matrix:
1. Projection semantic-width parity for `customer.客户年金计划`, `customer.客户业务月度快照`, and `customer.客户计划月度快照` remains open under `CT-004` and `CT-009`.
2. Identity parity remains only partially closed. Accepted slices prove the validation chain, but not the full legacy persistence/catalog breadth tracked by `CT-006`.
3. `annuity_income` operator artifacts and runtime-shape constraints remain open under `AI-004` and `AI-005`.
4. Special orchestration surfaces (`company_lookup_queue`, `reference_sync`) are still missing explicit first-wave matrix rows.
5. Enterprise persistence surfaces used by enrichment and refresh flows are still missing explicit accept/defer/retire decisions.

---

## 10. Audit Evidence Files

### 10.1 Config Files Analyzed

| File | Key Findings |
|------|-------------|
| `config/data_sources.yml` | 4 active domains, output tables, file patterns |
| `config/foreign_keys.yml` | FK rules with aggregations, target schemas |
| `config/reference_sync.yml` | Legacy postgres sync, 4 reference tables |
| `config/customer_status_rules.yml` | Status evaluation rules for snapshots |

### 10.2 Code Directories Analyzed

| Directory | Purpose |
|-----------|---------|
| `src/work_data_hub/cli/` | unified CLI entry, ETL dispatch, customer-mdm commands |
| `src/work_data_hub/domain/annuity_performance/` | annuity performance processing and operator artifacts |
| `src/work_data_hub/domain/annual_award/` | annual award processing and plan-code lookup |
| `src/work_data_hub/domain/annual_loss/` | annual loss processing and plan-code lookup |
| `src/work_data_hub/domain/annuity_income/` | annuity income processing and operator artifacts |
| `src/work_data_hub/domain/company_enrichment/` | queue DAO and enrichment orchestration |
| `src/work_data_hub/domain/reference_backfill/` | generic backfill, hybrid service, reference sync |
| `src/work_data_hub/customer_mdm/` | contract sync, snapshot refresh, year init, cutover, validation |
| `src/work_data_hub/orchestration/` | Dagster ops, jobs, schedules, sensors |
| `src/work_data_hub/infrastructure/enrichment/` | EQC provider, persistence, identity cache logic |
| `src/work_data_hub/infrastructure/validation/` | failed-row export and validation artifacts |
| `src/work_data_hub/io/connectors/` | EQC, postgres, and legacy connector adapters |

---

## 11. Open Questions

1. Which enterprise enrichment persistence surfaces are first-wave rebuild targets versus explicit retirement candidates?
2. Should `reference_sync` remain a retained operator/runtime surface, or be replaced by a new explicit bootstrap/publication design in `WorkDataHubPro`?
3. Are `company_lookup_queue` and live-provider EQC processing required before first-wave production closure, or can they remain Phase E deferred runtime work?
4. Which manual operator commands must remain supported in the rebuild: `customer-mdm sync`, `snapshot`, `init-year`, `validate`, `cutover`?
5. Should `unknown_names_csv` and failed-record CSV remain mandatory operator artifacts across first-wave domains?
6. Which standalone tools should be retired explicitly: EQC GUIs, intranet deploy GUI, standalone `cleanse` CLI?

---

## 12. Database Verification Results

### 12.1 Verified Tables (2026-04-12)

Connected to: `postgresql://root:Post.169828@192.168.0.200:5432/postgres`

**✅ All 12 required tables CONFIRMED:**

| Table | Schema | Verified | Row Count |
|-------|--------|----------|-----------|
| `规模明细` | business | ✅ | (fact table) |
| `收入明细` | business | ✅ | (fact table) |
| `中标客户明细` | customer | ✅ | (fact table) |
| `流失客户明细` | customer | ✅ | (fact table) |
| `客户明细` | customer | ✅ | (FK backfill) |
| `客户年金计划` | customer | ✅ | (SCD2 contract) |
| `客户业务月度快照` | customer | ✅ | (monthly snapshot) |
| `客户计划月度快照` | customer | ✅ | (monthly snapshot) |
| `年金计划` | mapping | ✅ | (reference) |
| `组合计划` | mapping | ✅ | (reference) |
| `产品线` | mapping | ✅ | (reference) |
| `组织架构` | mapping | ✅ | (reference) |

**Scope note:** this verification set confirms the first-wave fact/reference/projection output surface captured in Section 9.1. It does **not** prove the separate `business`-schema reference-sync targets or every `enterprise` operational table listed elsewhere in this audit.

### 12.2 Additional Operational Tables And Views Found

| Table | Schema | Rows | Notes |
|-------|--------|------|-------|
| `产品明细` | mapping | 18 | Product details reference |
| `利润指标` | mapping | 12 | Profit indicator reference |
| `计划层规模` | mapping | 7 | Plan-level scale reference |
| `客户明细` | mapping | - | **VIEW** (joins from customer schema) |
| `v_customer_business_monthly_status_by_type` | customer | - | VIEW |
| `enrichment_index` | enterprise | 0 | EQC cache (empty) |
| `enrichment_requests` | enterprise | 0 | EQC queue (empty) |
| `base_info`, `biz_label`, `business_info` | enterprise | 0 | EQC enrichment tables |
| `company_types_classification` | enterprise | - | Classification ref |
| `industrial_classification` | enterprise | - | Industry classification ref |
| `validation_results` | enterprise | - | Validation tracking |

### 12.3 Verification SQL Used

```sql
-- List all tables in target schemas
SELECT table_schema, table_name 
FROM information_schema.tables 
WHERE table_schema IN ('business', 'customer', 'mapping', 'enterprise')
ORDER BY table_schema, table_name;

-- Check specific tables
\d business.规模明细
\d customer.客户明细
\d mapping.年金计划
```

---

## 13. Architecture Verification Framework

This section defines how to use this audit document to verify WorkDataHubPro architecture coverage.

### 13.1 Verification Principles

1. **Audit is source of truth for legacy behavior** - if legacy does X, new project must either implement X or explicitly retire it
2. **Every table write must be traced to a capability** - no orphaned table operations
3. **Every system must be either: implemented, deferred (with reason), or retired (with rationale)**
4. **Cross-domain dependencies must be explicitly modeled**

---

### 13.2 Path A: Domain-by-Domain Verification

**Approach**: For each domain, trace every capability to table writes and verify coverage.

#### Process

1. **List domain's tables from audit (Section 4.1)**
2. **For each table, verify:**
   - Which WorkDataHubPro capability writes to it?
   - Is that capability implemented?
   - What is the status in coverage matrix?
3. **Check cross-domain dependencies (Section 6)**
4. **Identify gaps**

#### Domain Verification Checklist

```
Domain: [annuity_performance | annual_award | annual_loss | annuity_income]

□ Fact Table Write
  ├─ Table: [table_name]
  ├─ WorkDataHubPro Capability: [capability name]
  ├─ Status: [pending | planned | accepted]
  └─ Gap: [none | partial | missing]

□ FK Backfill Writes
  ├─ Target: [table_name]
  ├─ WorkDataHubPro Capability: [capability name]
  ├─ Status: [pending | planned | accepted]
  └─ Gap: [none | partial | missing]

□ Post-ETL Hooks
  ├─ Hook: [hook_name]
  ├─ Tables Affected: [table list]
  ├─ WorkDataHubPro Equivalent: [capability name]
  └─ Gap: [none | missing]

□ Side Effects / Artifacts
  ├─ Artifact: [file/artifact type]
  ├─ WorkDataHubPro Handling: [implement | retire | deferred]
  └─ Gap: [none | missing]
```

#### Example for `annuity_performance`

| Audit Table | Type | WorkDataHubPro Capability | Status | Gap |
|-------------|------|--------------------------|--------|-----|
| `business.规模明细` | Fact | `capabilities/fact_processing/annuity_performance` + `platform/publication` | accepted | none for validation slice |
| `mapping.年金计划` | Reference | `capabilities/reference_derivation` + `platform/publication` | accepted | semantic breadth still limited by `CT-002` |
| `customer.客户明细` | Reference | `capabilities/reference_derivation` + `platform/publication` | accepted | semantic breadth still limited by `CT-002` |
| `customer.客户年金计划` | Projection | `capabilities/projections/contract_state` | pending semantic-width parity | `CT-004`, `CT-009`, and manual operator-command surface not yet fully registered |
| `customer.客户业务月度快照` | Projection | `capabilities/projections/monthly_snapshot` | pending semantic-width parity | `CT-004` |
| `customer.客户计划月度快照` | Projection | `capabilities/projections/monthly_snapshot` | pending semantic-width parity | `CT-004` |

---

### 13.3 Path B: System-by-System Verification

**Approach**: For each infrastructure system, verify whether it is implemented, deferred, or retired.

#### Process

1. **List system components from audit (Section 8)**
2. **For each component, verify:**
   - Is it needed for production?
   - Is it implemented in WorkDataHubPro?
   - What is the status?
3. **Check dependencies between systems**
4. **Identify blocking gaps**

#### System Verification Checklist

```
System: [company_enrichment | eqc_integration | cleansing | validation_export | reference_sync | gui]

□ Component Inventory
  ├─ Component: [name]
  ├─ Legacy File: [path]
  ├─ Purpose: [what it does]
  ├─ WorkDataHubPro Status: [implemented | deferred | retired | missing]
  └─ Blocker: [yes | no]

□ Integration Points
  ├─ Input From: [system/table]
  ├─ Output To: [system/table]
  └─ Dependency Covered: [yes | no]

□ Production Readiness
  ├─ Required for Year 1: [yes | no | unclear]
  ├─ Current Status: [ready | needs_work | deferred]
  └─ Action Required: [description]
```

#### System Coverage Matrix

| System | Components | WorkDataHubPro Status | Production Ready | Gap Severity |
|--------|-----------|----------------------|-----------------|--------------|
| Company Enrichment core resolution chain | shared identity capability + cache-first validation mode | partial / validation-only accepted | no | High |
| EQC Integration live-provider breadth | provider contract partly represented, full persistence/runtime not closed | deferred / partial | no | High |
| Lookup Queue | queue runtime not explicitly registered in first-wave matrix | missing explicit governance row | no | High |
| Reference Sync | follow-on need is known, but row-level coverage is not explicit | missing explicit governance row | no | High |
| Cleansing CLI | standalone tool not registered | unknown | no | Medium |
| Validation Export | artifact parity only partially represented | partial | no | Medium |
| Customer MDM hooks and manual commands | semantic projection coverage is partial, operator surface incomplete | partial | no | High |
| GUI Applications | no explicit retain/retire decision | unknown | no | Low |

---

### 13.4 Cross-Cutting Concerns Verification

These items span multiple domains and must be verified holistically:

| Item | Source | Impact | Verification Method |
|------|--------|--------|---------------------|
| Cross-domain FK ordering | `foreign_keys.yml` `depends_on` | Backfill sequence matters | Verify `depends_on` chains preserved |
| Hook execution order | `hooks.py` | Contract/snapshot correctness | Verify `contract_status_sync` → `year_init` (January only) → `snapshot_refresh` order |
| January `year_init` | `year_init.py` | Annual status init | Verify January-only trigger logic |
| EQC rate limiting | `.wdh_env` | API quota | Verify rate limit config carried forward |

---

### 13.5 Verification Workflow

```
Step 1: Run Path A for each domain
         └─ Output: Per-domain gap list

Step 2: Run Path B for each system
         └─ Output: Per-system gap list

Step 3: Merge findings
         └─ Output: Consolidated gap list with priorities

Step 4: Identify blocking gaps
         └─ Output: Critical path items for production

Step 5: Update coverage matrix
         └─ Action: Mark items as deferred/retired with rationale

Step 6: Create follow-on plans
         └─ Output: Plans for deferred items
```

---

## 14. Follow-On Governance Actions

This audit is now a usable legacy baseline. The remaining work is not "finish the audit"; it is to apply the audit to governance assets:

1. Keep the newly registered first-wave coverage-matrix rows for `company_lookup_queue`, `reference_sync`, enterprise enrichment persistence surfaces, manual `customer-mdm` operator commands, and cross-domain operator artifacts current as decisions move from `pending` / `deferred` to explicit outcomes.
2. Decide which standalone tools are retained, deferred, or retired: GUI apps, standalone `cleanse` CLI, validation-export surfaces.
3. Decide whether `reference_sync` remains a retained legacy surface or is replaced by a new explicit bootstrap/publication design.
4. Decide whether live EQC/provider mode and async queue processing are required before first-wave production closure or remain Phase E deferred runtime concerns.
5. Align future implementation plans with the audit's corrected write-map: `business`-schema reference sync, `mapping`-schema FK backfill, `customer`-schema projections, and `enterprise` operational persistence.

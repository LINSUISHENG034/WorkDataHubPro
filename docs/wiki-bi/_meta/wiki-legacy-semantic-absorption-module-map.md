# wiki legacy semantic absorption module map

> 状态：Active
> 日期：2026-04-16
> 目标：把 `E:\Projects\WorkDataHub` 中仍藏在实现里的业务语义按可并行吸收的模块固定下来。

## Coverage Intent

- 先覆盖 legacy source families，再安排 subagent 执行顺序
- 每个模块都必须能回答“读哪些 raw sources、更新哪些 wiki pages、怎样验收”
- 模块边界优先服务 reviewability，而不是复制 legacy 目录结构
- 除非特别说明，下表与后续提到的 legacy source paths 均以 legacy WorkDataHub repo 为相对根路径（例如 `E:\Projects\WorkDataHub`）
- 模块表中的 `parallel-wave` 表示“在 pilots 通过后可被纳入并行波次”，不是立即执行授权

## Modules

| Module | Coverage Focus | Primary Legacy Sources | Primary Wiki Targets | Pilot Status |
|------|------|------|------|------|
| `M1` | `annuity_performance` hidden field semantics and downstream meaning | `docs/domains/annuity_performance*.md`, runbook, `pipeline_builder.py`, `service.py`, `schemas.py`, `helpers.py` | domain page, input contract, output contract, field-processing evidence | `wave-01` |
| `M2` | `annuity_income` hidden field semantics and operator-visible differences | `docs/domains/annuity_income*.md`, runbook, `pipeline_builder.py`, `service.py`, `schemas.py`, `helpers.py` | domain page, input contract, output contract, field-processing evidence | `wave-01` |
| `M3` | `annual_award` hidden multi-sheet and enrichment semantics | `docs/domains/annual_award*.md`, runbook, `pipeline_builder.py`, `service.py`, `schemas.py`, `helpers.py` | domain page, input contract, output contract, field-processing evidence | `wave-01` |
| `M4` | `annual_loss` hidden multi-sheet and temporal lookup semantics | `docs/domains/annual_loss*.md`, runbook, `pipeline_builder.py`, `service.py`, `schemas.py`, `helpers.py` | domain page, input contract, output contract, field-processing evidence | `wave-01` |
| `M5` | identity resolution, `temp_id`, override mappings, branch mappings, enrichment persistence boundaries | `config/mappings/company_id/*`, `config/mappings/company_branch.yml`, `config/eqc_confidence.yml`, `infrastructure/enrichment/*`, `domain/company_enrichment/*`, business-background docs | concept pages, identity standard, identity evidence, queue and persistence surfaces | `accepted-pilot` |
| `M6` | reference derivation, backfill, master-data propagation, publication-facing meaning | `config/foreign_keys.yml`, `config/reference_sync.yml`, `domain/reference_backfill/*`, `orchestration/reference_sync_ops.py`, `io/loader/*`, customer-master background docs | `backfill.md`, `reference-sync.md`, new reference/backfill evidence page, output correctness, domain links | `accepted-pilot` |
| `M7` | customer status, yearly lifecycle, strategic/existing semantics, snapshot consequences | `config/customer_status_rules.yml`, `config/customer_mdm.yaml`, `customer_mdm/*`, `cli/customer_mdm/*`, `cli/etl/hooks.py`, status background docs | customer-status concepts, status standard, new customer-MDM lifecycle evidence page, customer-MDM surface | `accepted-pilot` |
| `M8` | operator/runtime/verification governance including CLI surfaces, failed artifacts, replay and parity memory | `docs/guides/validation/*`, `docs/reference/data_processing_guide.md`, runbooks, `cli/etl/*`, `orchestration/jobs.py`, `orchestration/ops/*`, `infrastructure/validation/*` | operator/surface evidence, verification evidence, validation-result-history evidence, tooling surfaces, domain links | `wave-01` |

## Coverage Gaps Closed By Review

- review confirmed the exact eight-module model; no `M9` was added
- discovery and input-contract family was originally under-covered; ownership: `M8`
- shared cleansing and transform substrate was originally under-covered; ownership: `M8` for cross-domain execution semantics, domain-specific semantic effects stay with `M1-M4` when cited by their pages
- load/write-contract schema family was originally under-covered; ownership: `M6`
- reference-sync state family was originally under-covered; ownership: `M6`
- enrichment-index learning/conflict semantics were originally under-covered; ownership: `M5`
- scheduled/operator runtime surfaces were originally under-covered; ownership: `M8`

## Guardrails Added After Review

- M1-M4 treat code as a second-pass/audit source after the minimal non-code/raw-doc source set, so “domain semantics” does not silently collapse into “whatever the current implementation does”
- `pilot-*` and `parallel-wave` labels are scoping markers, not permission to bypass the canonical domain-upgrade framework or round workflow
- assigned write sets are frozen per round note before dispatch, not inferred from the module label alone
- module acceptance requires same-change closure artifacts, reachability, evidence-template preservation, stable-finding separation, assigned write-set checks, and explicit gap disposition (plus current-implementation writeback when applicable)
- parallel-wave execution is only acceptable with collision guardrails for controller-owned integration files (notably `index.md`/`log.md`/round notes), so module reviews complete before integration edits land

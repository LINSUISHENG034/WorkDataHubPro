# 状态与快照证据

## 结论主题

本页聚合客户状态、snapshot granularity、customer MDM、`is_new` 与客户类型边界相关证据。

## 证据记录

| evidence_id | source_type | evidence_strength | coverage_state | supported_pages | last_verified | notes |
|---|---|---|---|---|---|---|
| E-ST-001 | legacy_doc | strong | legacy_only | `customer-status`, `is-new`, `customer-type` | 2026-04-14 | `E:\Projects\WorkDataHub\docs\business-background\客户主数据回填与状态来源分析.md` 说明状态来源分层与 `is_new` 语义。 |
| E-ST-002 | legacy_doc | strong | legacy_only | `customer-status`, `snapshot-granularity` | 2026-04-14 | `E:\Projects\WorkDataHub\docs\business-background\战客身份定义与更新逻辑.md` 说明年度身份、SCD2 与快照关系。 |
| E-ST-003 | legacy_config | strong | legacy_only | `customer-status-semantics`, `output-correctness` | 2026-04-14 | `E:\Projects\WorkDataHub\config\customer_status_rules.yml` 是状态语义与 SQL generation 的直接合同。 |
| E-ST-004 | legacy_doc | supporting | legacy_only | `real-data-validation`, `output-correctness` | 2026-04-14 | `verification_guide_real_data.md` 提供对 snapshot 与 contract 输出的 operator 验证路径。 |
| E-ST-005 | audit | supporting | absorbed | `customer-mdm-commands`, `snapshot-granularity` | 2026-04-14 | `2026-04-12-legacy-code-audit.md` 识别了 customer MDM manual command surface 与 hook-linked outputs。 |

## 哪些来源是强证

- 客户状态业务背景文档
- `customer_status_rules.yml`

## 哪些来源只是旁证

- audit synthesis
- verification guide 中的操作说明

## 当前证据缺口

- 还未把 `is_winning_this_year`、`is_loss_reported`、`is_churned_this_year` 拆成对象级 evidence pages

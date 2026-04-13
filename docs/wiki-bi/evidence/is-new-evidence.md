# `is_new` 对象级证据

## 结论主题

本页聚合 `is_new` 这一状态对象的直接证据，包括其公式、粒度边界、非例和 operator 验证路径。

## 证据记录

| evidence_id | source_type | evidence_strength | coverage_state | supported_pages | last_verified | notes |
|---|---|---|---|---|---|---|
| E-ISNEW-001 | legacy_doc | strong | absorbed | `is-new`, `customer-status-semantics`, `output-correctness` | 2026-04-14 | `客户主数据回填与状态来源分析.md` 明确 `is_new` = `is_winning_this_year AND NOT is_existing`，且只定义在客户 / 产品线粒度。 |
| E-ISNEW-002 | legacy_config | strong | absorbed | `is-new`, `customer-status-semantics` | 2026-04-14 | `customer_status_rules.yml` 将 `is_new` 定义为 derived status，使用 `status_reference + negation + BOOL_OR(is_existing)`。 |
| E-ISNEW-003 | legacy_doc | supporting | absorbed | `is-new`, `real-data-validation` | 2026-04-14 | `verification_guide_real_data.md` 提供 `is_new` 与 `is_winning_this_year` / `is_existing` 一致性检查 SQL。 |
| E-ISNEW-004 | audit | supporting | absorbed | `is-new`, `customer-type` | 2026-04-14 | 首轮状态与快照吸收已确认 `is_new` 与 `年金客户类型` 的语义边界，并保留审查痕迹。 |

## 本轮已吸收的稳定结论

- `is_new` 是 derived status，不是 event 原生字段
- `is_new` 当前只存在于客户 / 产品线粒度，不存在计划层版本
- `is_new` 与 `年金客户类型` 不是同一层语义
- 对 `is_new` 的验证至少应同时检查 `is_winning_this_year` 与 `is_existing`

## 哪些来源是强证

- `客户主数据回填与状态来源分析.md`
- `customer_status_rules.yml`

## 哪些来源只是旁证

- operator verification guide
- 先前轮次吸收沉淀

## 当前证据缺口

- 还没有把 `is_winning_this_year`、`is_loss_reported`、`is_churned_this_year` 拆成各自对象级 evidence page

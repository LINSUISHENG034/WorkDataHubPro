# `is_loss_reported` 对象级证据

## 结论主题

本页聚合 `is_loss_reported` 这一状态对象的直接证据，包括其事实来源、粒度边界与验证路径。

## 证据记录

| evidence_id | source_type | evidence_strength | coverage_state | supported_pages | last_verified | notes |
|---|---|---|---|---|---|---|
| E-ILOSS-001 | legacy_config | strong | absorbed | `customer-status`, `customer-status-semantics`, `annual-loss` | 2026-04-14 | `customer_status_rules.yml` 明确 `is_loss_reported` 的 source 是 `annual_loss`，采用 `exists_in_year` 规则，并在客户 / 产品线粒度匹配 `company_id + product_line_code`。 |
| E-ILOSS-002 | legacy_doc | supporting | absorbed | `real-data-validation`, `annual-loss` | 2026-04-14 | `verification_guide_real_data.md` 提供 `is_loss_reported` 与 `customer."流失客户明细"` 的交叉核验 SQL，并把它接回客户明细 tags 与快照结果。 |
| E-ILOSS-003 | legacy_doc | supporting | absorbed | `annual-loss`, `customer-status` | 2026-04-14 | `annual_loss` 相关 domain / capability 文档把年度流失申报事实定义为客户状态判断的上游来源。 |

## 本轮已吸收的稳定结论

- `is_loss_reported` 是年度流失申报事实在客户 / 产品线粒度上的状态表达
- 它的直接事实来源是 `annual_loss`，而不是规模下降或其他推断
- 它与 `is_churned_this_year` 不是同一层判断：一个是申报事实，一个是规模表现判断

## 哪些来源是强证

- `customer_status_rules.yml`

## 哪些来源只是旁证

- `verification_guide_real_data.md`
- `annual_loss` 相关 domain 文档

## 当前证据缺口

- current project 还没有为 `is_loss_reported` 建立独立对象级 replay / evidence page
- 当前 wiki 仍主要通过 shared status pages 承接这条状态的 current implementation evidence

# `is_winning_this_year` 对象级证据

## 结论主题

本页聚合 `is_winning_this_year` 这一状态对象的直接证据，包括其事实来源、粒度边界与验证路径。

## 证据记录

| evidence_id | source_type | evidence_strength | coverage_state | supported_pages | last_verified | notes |
|---|---|---|---|---|---|---|
| E-IWIN-001 | legacy_config | strong | absorbed | `customer-status`, `customer-status-semantics`, `annual-award` | 2026-04-14 | `customer_status_rules.yml` 明确 `is_winning_this_year` 的 source 是 `annual_award`，采用 `exists_in_year` 规则，并在客户 / 产品线粒度匹配 `company_id + product_line_code`。 |
| E-IWIN-002 | legacy_doc | supporting | absorbed | `real-data-validation`, `annual-award`, `is-new` | 2026-04-14 | `verification_guide_real_data.md` 提供 `is_winning_this_year` 与 `customer."中标客户明细"` 的交叉核验 SQL，并把它接到 `is_new` 的验证路径。 |
| E-IWIN-003 | legacy_doc | supporting | absorbed | `annual-award`, `customer-status` | 2026-04-14 | `annual_award` 相关 domain / capability 文档把年度中标事实定义为客户状态判断的上游来源。 |

## 本轮已吸收的稳定结论

- `is_winning_this_year` 是年度中标事实在客户 / 产品线粒度上的状态表达，不是标签字段
- 它的直接事实来源是 `annual_award`，而不是 `annuity_performance`
- 它既是独立状态对象，也是 `is_new` 的上游条件之一

## 哪些来源是强证

- `customer_status_rules.yml`

## 哪些来源只是旁证

- `verification_guide_real_data.md`
- `annual_award` 相关 domain 文档

## 当前证据缺口

- current project 还没有为 `is_winning_this_year` 建立独立对象级 replay / evidence page
- 当前 wiki 仍主要通过 shared status pages 承接这条状态的 current implementation evidence

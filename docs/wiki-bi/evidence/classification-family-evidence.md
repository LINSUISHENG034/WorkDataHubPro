# classification family 证据

## 结论主题

本页聚合 classification family 相关证据：`计划类型`、`年金计划类型`、`业务类型`、`管理资格` 与 `组合代码`。

目标不是把这些字段压成同一层定义，而是明确它们分别属于输入分类、衍生分类、customer-master 聚合结果与 portfolio 锚点。

## 证据记录

| evidence_id | source_type | evidence_strength | coverage_state | supported_pages | last_verified | notes |
|---|---|---|---|---|---|---|
| E-CF-001 | legacy_doc | strong | absorbed | `classification-family-evidence`, `plan-type`, `company-id` | 2026-04-18 | `E:\Projects\WorkDataHub\docs\business-background\年金计划类型与客户名称业务背景.md` 明确单一计划 / 集合计划会改变客户识别假设，说明输入侧 `计划类型` 不能直接等同于 customer-master 聚合标签。 |
| E-CF-002 | legacy_config | strong | absorbed | `classification-family-evidence`, `plan-type`, `annuity-performance-field-processing-evidence`, `annuity-income-field-processing-evidence`, `annual-loss-field-processing-evidence` | 2026-04-18 | `E:\Projects\WorkDataHub\config\foreign_keys.yml` 显式声明 `业务类型 -> 管理资格`、`concat_distinct(年金计划类型)`、`fk_portfolio(组合代码)` 等聚合/映射规则，证明 classification family 跨越输入、reference 与 customer-master 多层。 |
| E-CF-003 | legacy_doc | strong | absorbed | `classification-family-evidence`, `annuity-performance-field-processing-evidence` | 2026-04-18 | `E:\Projects\WorkDataHub\docs\cleansing-rules\annuity-performance.md` 明确 `业务类型 -> 产品线代码`、`组合代码` 的 defaulting 以及 `计划类型` 对默认计划/组合锚点的影响。 |
| E-CF-004 | legacy_doc | strong | absorbed | `classification-family-evidence`, `annuity-income-field-processing-evidence`, `plan-type` | 2026-04-18 | `E:\Projects\WorkDataHub\docs\cleansing-rules\annuity-income.md` 明确 `组合代码` 会按 `业务类型` / `计划类型` 补默认值，且单一计划 / 集合计划会改变计划名称解释与客户识别路径。 |
| E-CF-005 | legacy_doc | strong | absorbed | `classification-family-evidence`, `annuity-performance-field-processing-evidence`, `annuity-income-field-processing-evidence`, `annual-loss-field-processing-evidence` | 2026-04-18 | `E:\Projects\WorkDataHub\docs\verification_guide_real_data.md` 把 `管理资格`、`年金计划类型`、`其他年金计划`、`其他开拓机构` 等聚合结果列为 operator 需核验的正式输出，而不是纯实现细节。 |

## 本轮已吸收的稳定结论

- 输入侧 `计划类型` 与 customer-master `年金计划类型` 不是同一层对象；前者属于 fact / plan 解释锚点，后者是聚合后的 customer-master 分类结果。
- `业务类型` 既是输入分类，又经常成为 `产品线代码`、`管理资格` 与组合默认规则的解释锚点，因此不能被简化成“普通枚举字段”。
- `管理资格` 属于 customer-master 聚合分类，不等于输入侧某一行的 `业务类型` 原值。
- `组合代码` 更接近 portfolio / classification anchor，而不是 enterprise identity truth。
- classification family 同时跨越 input contract、field-processing evidence 与 customer-master aggregation；如果只看某一页里的字段处理，很容易把层次混写。

## 哪些来源是强证

- `E:\Projects\WorkDataHub\docs\business-background\年金计划类型与客户名称业务背景.md`
- `E:\Projects\WorkDataHub\config\foreign_keys.yml`
- `E:\Projects\WorkDataHub\docs\cleansing-rules\annuity-performance.md`
- `E:\Projects\WorkDataHub\docs\cleansing-rules\annuity-income.md`
- `E:\Projects\WorkDataHub\docs\verification_guide_real_data.md`

## 哪些来源只是旁证

- `annuity_performance` / `annuity_income` / `annual_loss` 相关字段处理证据页中的 current-side 承接说明

## 对象级分发入口

- [年金计划类型：`plan_type`](../concepts/plan-type.md)
- [`annuity_performance` 字段处理证据](./annuity-performance-field-processing-evidence.md)
- [`annuity_income` 字段处理证据](./annuity-income-field-processing-evidence.md)
- [`annual_loss` 字段处理证据](./annual-loss-field-processing-evidence.md)

## 当前证据缺口

- `管理资格` 与 `组合代码` 目前还没有独立 concept page；本轮先建立 cross-domain dispatcher，不强行继续拆页。
- `annual_award` 对 classification family 的承接仍主要通过 event-domain contract 与 customer-master signal family 间接呈现，尚未形成单独对象页。
- current project 还没有把 classification family 作为整组对象写成 repo-native contract tests；当前主要依赖 legacy raw sources 与现有 field-processing pages 的 current 承接说明。

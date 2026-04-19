# 年金计划类型：`plan_type`

## 定义

这里的 `plan_type` 主要区分：

- 单一计划
- 集合计划

它不是装饰性字段，而是会改变客户识别、计划号解释和后续判断语义的业务概念。

## 业务意义

单一计划与集合计划在业务上代表不同的识别假设：

- 单一计划更容易对应单一企业主体
- 集合计划更容易承载多个企业参与方

因此，计划名称、客户名称、计划代码的解释方式也会不同。

它还会连带影响一组相邻分类对象：

- 输入侧 `计划类型`
- customer-master 聚合后的 `年金计划类型`
- 作为产品线与管理资格解释锚点的 `业务类型`
- 作为 portfolio/classification anchor 的 `组合代码`

## 不应被改写的约束

- 不能把单一计划与集合计划套用同一识别假设
- 不能把“客户名称为空”直接推成“无法识别客户”
- plan type 会影响 plan-code enrichment 与相关 fallback 的判断
- `plan_type` 不应被静默改写成 customer-master `年金计划类型`

## 输入现实与边界情况

- 真实输入里，集合计划经常不直接对应一个企业主体
- 某些记录会依赖多线索识别，而不是单字段兜底
- event domain 往往通过 multi-sheet 输入携带不同业务语境
- `annuity_performance` 与 `annuity_income` 虽共用目录结构，但面向不同 sheet
- `业务类型` 与 `组合代码` 经常参与对 plan type 的进一步解释，但这不意味着它们与 `plan_type` 是同一层对象

## 对输出与下游的影响

- 影响 `company_id` 识别
- 影响 event domain 的计划号补全
- 影响主数据与快照解释
- 影响输入合同设计：不能把所有域统一写成“单 sheet + 单字段识别”
- 影响 classification family：`计划类型`、`年金计划类型`、`业务类型`、`管理资格`、`组合代码` 之间的边界需要一起理解

## 常见误解 / 非例

- 计划名称不必然等于客户全称
- 集合计划不应被简化成“只是另一种单一计划”
- `plan_type` 不等于 customer-master `年金计划类型`
- `组合代码` 不等于企业身份键，它首先是 portfolio/classification anchor

## 相关概念

- [企业身份标识：`company_id`](./company-id.md)
- [回填：`backfill`](./backfill.md)
- [管理资格](./management-qualification.md)
- [组合代码](./portfolio-code.md)

## 相关标准

- [输入现实合同](../standards/input-reality/input-reality-contracts.md)
- [real-data validation](../standards/verification-method/real-data-validation.md)

## 相关证据

- [输入现实证据](../evidence/input-reality-evidence.md)
- [身份与补查证据](../evidence/identity-and-lookup-evidence.md)
- [classification family 证据](../evidence/classification-family-evidence.md)

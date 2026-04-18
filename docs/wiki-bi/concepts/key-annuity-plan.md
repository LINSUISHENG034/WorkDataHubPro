# 关键年金计划

## 定义

这里的“关键年金计划”指 customer-master / reference semantics 上用于表达某个客户最具主导性的计划锚点。

它不是简单复制某一条输入记录上的 `计划代码` 或 `年金计划号`，而是从同一客户的一组事实记录里按稳定权重选出的 dominant value。

## 业务意义

如果没有“关键年金计划”这一层：

- customer master 很难回答“这个客户当前最应被哪一个计划解释”
- `主拓机构`、`关联计划数` 与计划归属会退化成一堆零散字段
- operator 很难区分“主导计划”与“这个客户关联过哪些计划”

## 不应被改写的约束

- `关键年金计划` 不是原始 `计划代码` / `年金计划号` 的别名
- `关键年金计划` 必须和“按什么权重选出”一起理解
- `关键年金计划` 属于 customer-master signal，不是 snapshot status 或 contract truth
- `关键年金计划` 不等于 `关联计划数`，也不等于 `其他年金计划`

## 输入现实与边界情况

- `annuity_performance` 用 `期末资产规模` 选出主导计划
- `annuity_income` 用 `固费` 选出主导计划
- `annual_award` / `annual_loss` 以 `计划规模` 形成 event-driven 主导计划
- 同一客户可能同时拥有多个计划，因此 `关键年金计划` 只能回答“主导锚点”，不能替代 relationship breadth
- 不同 domain 进入 backfill 的计划列名可能不同，但 customer-master 语义层要保留“主导计划”这一稳定对象

## 对输出与下游的影响

- 影响 `customer.客户明细` 的主导计划解释
- 影响 `主拓机构`、`关联计划数`、`其他年金计划` 等相邻 customer-master signals 的可解释性
- 影响 real-data validation 中对 customer-master signal family 的核验路径

## 常见误解 / 非例

- `关键年金计划` 不等于“当前这条事实行上的计划代码”
- `关键年金计划` 不等于“客户唯一有效计划”
- `关键年金计划` 不等于“该客户出现过的所有计划”

## 相关概念

- [回填：`backfill`](./backfill.md)
- [主拓机构](./primary-branch.md)
- [年金计划类型：`plan_type`](./plan-type.md)

## 相关标准

- [输出正确性标准](../standards/output-correctness/output-correctness.md)
- [`annuity_performance` 输出合同](../standards/output-correctness/annuity-performance-output-contract.md)
- [`annuity_income` 输出合同](../standards/output-correctness/annuity-income-output-contract.md)

## 相关证据

- [customer-master signals 证据](../evidence/customer-master-signals-evidence.md)
- [引用同步与回填证据](../evidence/reference-and-backfill-evidence.md)
- [`annuity_performance` 字段处理证据](../evidence/annuity-performance-field-processing-evidence.md)
- [`annuity_income` 字段处理证据](../evidence/annuity-income-field-processing-evidence.md)

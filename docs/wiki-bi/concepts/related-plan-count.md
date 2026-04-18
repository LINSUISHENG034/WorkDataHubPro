# 关联计划数

## 定义

这里的“关联计划数”指 customer-master semantics 上用于表达某个客户关联了多少个不同计划的 relationship-breadth signal。

它不是某条事实行上的原始字段，而是从同一客户的一组事实记录中按 `count_distinct` 规则聚合出来的 customer-master 结果。

## 业务意义

如果没有“关联计划数”这一层：

- operator 很难快速判断一个客户是单计划关系还是多计划关系
- `关键年金计划`、`其他年金计划` 与计划关系宽度会混成一个模糊描述
- customer master 很难直接回答“这个客户关联计划的广度”而只能退回原始明细或拼接字段

## 不应被改写的约束

- `关联计划数` 不等于 `关键年金计划`
- `关联计划数` 不等于 `其他年金计划`
- `关联计划数` 不等于 snapshot-side `plan_count`
- `关联计划数` 只回答“有多少个不同计划”，不枚举具体是哪几个计划

## 输入现实与边界情况

- `annuity_performance` / `annuity_income` 以 `计划代码` 聚合 relationship breadth
- `annual_award` / `annual_loss` 以 `年金计划号` 聚合 relationship breadth
- 它与 `其他年金计划`、`其他开拓机构` 一起构成 customer-master relationship breadth，但三者回答的问题不同
- blank value filtering 与 distinct 规则会直接影响最终计数

## 对输出与下游的影响

- 影响 `customer.客户明细` 对客户计划关系广度的解释
- 影响 `关键年金计划` 和 `其他年金计划` 的可读性
- 影响 real-data validation 中对 customer-master aggregation 是否合理的核验路径

## 常见误解 / 非例

- `关联计划数` 不等于“当前快照里有效合约计划数”
- `关联计划数` 不等于 snapshot-side `plan_count`
- `关联计划数` 不等于“这个客户最重要的计划”
- `关联计划数` 不等于具体计划清单

## 相关概念

- [回填：`backfill`](./backfill.md)
- [关键年金计划](./key-annuity-plan.md)
- [快照粒度：`snapshot_granularity`](./snapshot-granularity.md)

## 相关标准

- [输出正确性标准](../standards/output-correctness/output-correctness.md)
- [`annuity_performance` 输出合同](../standards/output-correctness/annuity-performance-output-contract.md)
- [`annuity_income` 输出合同](../standards/output-correctness/annuity-income-output-contract.md)

## 相关证据

- [customer-master signals 证据](../evidence/customer-master-signals-evidence.md)
- [引用同步与回填证据](../evidence/reference-and-backfill-evidence.md)
- [annuity workbook family 证据](../evidence/annuity-workbook-family-evidence.md)

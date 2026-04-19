# 其他开拓机构

## 定义

这里的“其他开拓机构”指 customer-master semantics 上用于表达某个客户还关联了哪些机构的 relationship-breadth list signal。

它不是某条事实行上的原始 `机构名称`，而是从同一客户的一组事实记录中按 `concat_distinct` 规则聚合出来的 customer-master 结果。

## 业务意义

如果没有“其他开拓机构”这一层：

- operator 很难直接看到某个客户除了主导机构之外还横跨了哪些机构语境
- `主拓机构`、`关联机构数` 与机构关系宽度会继续混成一句模糊描述
- customer master 很难回答“这些机构宽度具体展开到哪些机构”，只能退回原始明细

## 不应被改写的约束

- `其他开拓机构` 不等于 `主拓机构`
- `其他开拓机构` 不等于 `关联机构数`
- `其他开拓机构` 回答的是 breadth list，不是 dominant-value anchor
- `其他开拓机构` 的字段名虽然带“其他”，但在当前稳定 raw-source 证据下，应先把它治理为 breadth-list context，而不是先假定它已经严格等于“剔除主拓机构后的精确余集”

## 输入现实与边界情况

- 四个 accepted domains 都以 `机构名称` 做 `concat_distinct`
- blank value filtering、去重与分隔符规则会直接影响最终列表形态
- 它与 `主拓机构`、`关联机构数` 一起构成机构侧 relationship breadth，但三者回答的问题不同
- 当前 durable wiki 把它理解为“机构侧宽度的列表表达”，而不是要求本页先证明每个 domain 都执行了完全同形的排除主导机构规则

## 对输出与下游的影响

- 影响 `customer.客户明细` 对客户机构关系宽度的解释
- 影响 `主拓机构` 与 `关联机构数` 的可读性
- 影响 real-data validation 中对 customer-master aggregation 是否合理的核验路径

## 常见误解 / 非例

- `其他开拓机构` 不等于“主导机构”
- `其他开拓机构` 不等于“有多少个机构”
- `其他开拓机构` 不应在没有额外证据时被写成“已经严格排除了主拓机构的精确数学余集”
- `其他开拓机构` 不等于组织维表中的机构主键清单

## 相关概念

- [回填：`backfill`](./backfill.md)
- [主拓机构](./primary-branch.md)
- [关联机构数](./related-branch-count.md)

## 相关标准

- [输出正确性标准](../standards/output-correctness/output-correctness.md)
- [`annuity_performance` 输出合同](../standards/output-correctness/annuity-performance-output-contract.md)
- [`annuity_income` 输出合同](../standards/output-correctness/annuity-income-output-contract.md)

## 相关证据

- [customer-master signals 证据](../evidence/customer-master-signals-evidence.md)
- [引用同步与回填证据](../evidence/reference-and-backfill-evidence.md)

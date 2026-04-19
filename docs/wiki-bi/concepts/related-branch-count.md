# 关联机构数

## 定义

这里的“关联机构数”指 customer-master semantics 上用于表达某个客户关联了多少个不同机构的 relationship-breadth signal。

它不是某条事实行上的原始字段，而是从同一客户的一组事实记录中按 `count_distinct` 规则聚合出来的 customer-master 结果。

## 业务意义

如果没有“关联机构数”这一层：

- operator 很难快速判断一个客户是单机构关系还是多机构关系
- `主拓机构`、`其他开拓机构` 与机构归属宽度会混成一个模糊描述
- customer master 很难直接回答“这个客户关联机构的广度”，只能退回原始明细或拼接字段

## 不应被改写的约束

- `关联机构数` 不等于 `主拓机构`
- `关联机构数` 不等于 `其他开拓机构`
- `关联机构数` 只回答“有多少个不同机构”，不回答“哪一个机构占主导”
- `关联机构数` 不枚举具体是哪几个机构

## 输入现实与边界情况

- 四个 accepted domains 都以 `机构名称` 的 `count_distinct` 聚合 relationship breadth
- 它与 `主拓机构`、`其他开拓机构` 一起构成机构侧 relationship breadth，但三者回答的问题不同
- blank value filtering 与 distinct 规则会直接影响最终计数
- 不同 domain 的 dominant-value 权重列可以不同，但 breadth count 仍回答同一类问题：客户横跨了多少个机构

## 对输出与下游的影响

- 影响 `customer.客户明细` 对客户机构关系广度的解释
- 影响 `主拓机构` 和 `其他开拓机构` 的可读性
- 影响 real-data validation 中对 customer-master aggregation 是否合理的核验路径

## 常见误解 / 非例

- `关联机构数` 不等于“主拓机构数量”
- `关联机构数` 不等于具体机构清单
- `关联机构数` 不等于组织维表里的机构主键数量
- `关联机构数` 不自动等于 snapshot 粒度下的机构维度展开

## 相关概念

- [回填：`backfill`](./backfill.md)
- [主拓机构](./primary-branch.md)
- [其他开拓机构](./other-branches.md)
- [关联计划数](./related-plan-count.md)

## 相关标准

- [输出正确性标准](../standards/output-correctness/output-correctness.md)
- [`annuity_performance` 输出合同](../standards/output-correctness/annuity-performance-output-contract.md)
- [`annuity_income` 输出合同](../standards/output-correctness/annuity-income-output-contract.md)

## 相关证据

- [customer-master signals 证据](../evidence/customer-master-signals-evidence.md)
- [引用同步与回填证据](../evidence/reference-and-backfill-evidence.md)

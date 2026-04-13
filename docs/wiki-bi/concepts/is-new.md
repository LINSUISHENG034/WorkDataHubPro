# 新到账客户状态：`is_new`

## 定义

`is_new` 表示客户在快照语义上属于“新到账客户”。

当前稳定口径是：

- 当年中标
- 且不是 existing

在 legacy 配置合同里，它被表达为：

- `is_winning_this_year`
- `AND`
- `NOT BOOL_OR(is_existing)`

## 业务意义

`is_new` 是分析与经营判断层状态，不是主数据标签，也不是 event 明细字段。

## 不应被改写的约束

- `is_new` 不等于 `年金客户类型`
- `is_new` 当前只定义在客户 / 产品线粒度
- 不能因为实现方便把它下沉成 plan 粒度或 event 明细标签
- 它属于 derived status，而不是单源事实字段

## 输入现实与边界情况

- 它依赖 award 事实
- 它依赖 existing 状态
- 如果这两类上游事实不稳定，`is_new` 的结论也会漂移
- 计划级快照当前没有 `is_new`

## 对输出的影响

- 影响 `customer.客户业务月度快照`
- 影响“新到账客户”相关分析口径
- 影响与 legacy / replay 输出的 compare 结论
- 不能被 `customer.客户明细` 中的标签字段替代

## 常见误解 / 非例

- `中标客户` 不等于 `is_new = true`
- `年金客户类型 = 新客 / 中标客户` 不等于快照状态
- `is_new` 不是 plan 层字段
- `is_new` 也不是 `annual_award` 明细表中的原生字段

## 相关概念

- [客户状态总览](./customer-status.md)
- [年金客户类型：`customer_type`](./customer-type.md)
- [快照粒度：`snapshot_granularity`](./snapshot-granularity.md)

## 相关标准

- [客户状态语义正确性](../standards/semantic-correctness/customer-status-semantics.md)
- [输出正确性标准](../standards/output-correctness/output-correctness.md)
- [real-data validation](../standards/verification-method/real-data-validation.md)

## 相关证据

- [状态与快照证据](../evidence/status-and-snapshot-evidence.md)

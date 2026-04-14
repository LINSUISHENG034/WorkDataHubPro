# `annuity_performance` 输出合同

> standard_type: `output-correctness`
> related_standard_types: `input-reality`, `verification-method`

## 标准对象

本页定义 `annuity_performance` 的输出合同。

它回答的是：

- 这个 domain 直接产出什么
- 哪些对象属于回填结果
- 哪些对象属于下游派生结果

## 直接事实输出

- 目标 schema
  - `business`
- 目标表
  - `business."规模明细"`
- 刷新范围
  - `月度`
  - `业务类型`
  - `计划类型`

这部分是 annuity-performance 自身最直接的事实输出。

## 回填输出

legacy raw sources 明确表明，annuity-performance 还会驱动下列回填对象：

- `mapping."年金计划"`
- `mapping."组合计划"`
- `mapping."产品线"`
- `mapping."组织架构"`
- `customer."客户明细"`

这些不等于“重复写事实表”，而是从事实中补齐主数据 / 参考对象。

## 下游派生输出

在 direct fact 与 backfill 之后，annuity-performance 还会承接并推动：

- `customer."客户年金计划"`
- `customer."客户业务月度快照"`
- `customer."客户计划月度快照"`

它们不是 annuity-performance 原始事实本身，但属于这个 domain 的实际治理后果，因此必须纳入输出合同视野。

## 关键输出边界

- direct fact output
  - `business."规模明细"`
- backfill output
  - reference / customer object 补齐
- derived output
  - contract / snapshot 相关对象

这三层不能混成一个“最终都写库了”的模糊说法。

## 正确性约束

- 事实输出、回填输出、派生输出必须可彼此解释
- 回填不能冒充状态判断
- 派生快照不能改写事实来源
- output compare 不能只看 row count，而应看 sink、粒度与语义关系

## 相关概念

- [回填：`backfill`](../../concepts/backfill.md)
- [客户状态总览](../../concepts/customer-status.md)
- [快照粒度：`snapshot_granularity`](../../concepts/snapshot-granularity.md)

## 相关证据

- [annuity_performance 字段处理证据](../../evidence/annuity-performance-field-processing-evidence.md)
- [状态与快照证据](../../evidence/status-and-snapshot-evidence.md)

## 相关验证方法

- [real-data validation](../verification-method/real-data-validation.md)
- [golden scenarios](../verification-method/golden-scenarios.md)

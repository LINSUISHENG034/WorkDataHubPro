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

legacy 侧的稳定 direct fact sink 是：

- `business."规模明细"`

刷新范围由 `月度`、`业务类型`、`计划类型` 定义。

在 current project 的 accepted slice 中，对应显式 publication target 是：

- `fact_annuity_performance`

这部分是 annuity-performance 自身最直接的事实输出。

## 回填输出

legacy raw sources 明确表明，annuity-performance 还会驱动下列回填对象：

- `mapping."年金计划"`
- `mapping."组合计划"`
- `mapping."产品线"`
- `mapping."组织架构"`
- `customer."客户明细"`

这些不等于“重复写事实表”，而是从事实中补齐主数据 / 参考对象。

其中关键隐藏语义包括：

- `fk_plan` 与 `fk_customer` 中多个字段使用 `max_by(order_column=期末资产规模)`，决定 `主拓机构` / `关键年金计划` 等主导值
- `fk_customer.skip_blank_values=true` 明确 temp-id（`IN*`）不应作为客户主数据回填键
- `fk_customer.tags` 由 `月度` 派生 `yyMM新建`，不是源表直接字段搬运
- `fk_customer.年金客户类型` 通过模板固定为 `新客`，属于衍生标签而非输入原值
- 上述字段应作为同一 customer-master signal family 理解：`主拓机构`、`关键年金计划`、`关联计划数`、`关联机构数`、`其他年金计划`、`其他开拓机构`、`yyMM新建`、`年金客户类型`
- 其中 [`关键年金计划`](../../concepts/key-annuity-plan.md) 现在已有独立对象页；它回答主导计划锚点，不替代 relationship breadth 信号
- [`关联计划数`](../../concepts/related-plan-count.md) 现在也有独立对象页；它回答 relationship breadth，不等于主导计划锚点，也不等于 snapshot-side `plan_count`
- [`关联机构数`](../../concepts/related-branch-count.md) 现在也有独立对象页；它回答机构侧 relationship breadth，不等于 `主拓机构`，也不等于 `其他开拓机构`
- [`其他年金计划`](../../concepts/other-annuity-plans.md) 现在也有独立对象页；它回答计划侧 breadth-list context，不等于 `关键年金计划`，也不等于 `关联计划数`
- [`其他开拓机构`](../../concepts/other-branches.md) 现在也有独立对象页；它回答机构侧 breadth-list context，不等于 `主拓机构`，也不等于 `关联机构数`
- backfill classification outputs 还包括 [管理资格](../../concepts/management-qualification.md)；它属于聚合分类，不等于输入侧单行 `业务类型`

## 下游派生输出

在 direct fact 与 backfill 之后，annuity-performance 还会承接并推动：

- `customer."客户年金计划"`
- `customer."客户业务月度快照"`
- `customer."客户计划月度快照"`

在 current project 的 replay 证据中，对应显式 publication/projection 结果为：

- publication targets: `fact_annuity_performance`、`company_reference`、`contract_state`、`monthly_snapshot`
- projection targets: `contract_state`、`monthly_snapshot`

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

## 当前实现证据

- `current_test`
  - `tests/integration/test_annuity_performance_processing.py`
  - `tests/replay/test_annuity_performance_slice.py`
- `current_reference_asset`
  - `reference/historical_replays/annuity_performance/`
- `current_runbook`
  - `docs/runbooks/annuity-performance-replay.md`

## 相关概念

- [回填：`backfill`](../../concepts/backfill.md)
- [`tags`](../../concepts/tags.md)
- [主拓机构](../../concepts/primary-branch.md)
- [关联计划数](../../concepts/related-plan-count.md)
- [其他年金计划](../../concepts/other-annuity-plans.md)
- [关联机构数](../../concepts/related-branch-count.md)
- [其他开拓机构](../../concepts/other-branches.md)
- [管理资格](../../concepts/management-qualification.md)
- [客户状态总览](../../concepts/customer-status.md)
- [快照粒度：`snapshot_granularity`](../../concepts/snapshot-granularity.md)

## 相关证据

- [annuity_performance 字段处理证据](../../evidence/annuity-performance-field-processing-evidence.md)
- [customer-master signals 证据](../../evidence/customer-master-signals-evidence.md)
- [classification family 证据](../../evidence/classification-family-evidence.md)
- [状态与快照证据](../../evidence/status-and-snapshot-evidence.md)

## 相关验证方法

- [real-data validation](../verification-method/real-data-validation.md)
- [golden scenarios](../verification-method/golden-scenarios.md)

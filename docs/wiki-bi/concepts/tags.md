# `tags`

## 定义

这里的 `tags` 指写入 `customer.客户明细` 等 customer-master 层对象的业务事件轨迹标签，例如：

- `yyMM新建`
- `yyMM中标`
- `yyMM流失`

它们不是原始事实表中的直接业务字段，而是由 backfill / customer-master signal 规则派生出来的标签族。

## 业务意义

`tags` 的业务意义不是“给客户打个备注”，而是：

- 保留跨 domain 的客户经营轨迹
- 把某月发生过的 `新建` / `中标` / `流失` 事件写成 customer-master 可见信号
- 为 operator 核验与 customer-master explainability 提供轻量但稳定的历史线索

## 不应被改写的约束

- `tags` 属于 customer-master / backfill signal，不属于 snapshot status 本体
- `tags` 的日期前缀是业务语义的一部分，不是无关格式
- `tags` 可以与 `customer_type` 共存，但两者不是同一个字段族
- 不能把 `yyMM新建`、`yyMM中标`、`yyMM流失` 直接当作 `is_new`、`is_winning_this_year`、`is_loss_reported` 的同义词

## 输入现实与边界情况

- `annuity_performance` / `annuity_income` 会通过 `月度` 派生 `yyMM新建`
- `annual_award` 通过 `上报月份` 派生 `yyMM中标`
- `annual_loss` 通过 `上报月份` 派生 `yyMM流失`
- `tags` 的落地前提是 customer-master backfill 能以受治理键固化到 `customer.客户明细`
- temp-id / blank-value 过滤会影响哪些标签能进入 customer master

## 对输出与下游的影响

- 影响 `customer.客户明细` 的业务历史解释
- 影响 operator 对客户事件轨迹的核验方式
- 影响 cross-domain customer-master signal 的可追溯性

## 常见误解 / 非例

- `2510中标` 不等于 `is_winning_this_year`
- `2510流失` 不等于 `is_loss_reported`
- `2510新建` 不自动等于 `is_new`
- `tags` 不是“只是 JSONB 存储格式不同”的技术细节

## 相关概念

- [回填：`backfill`](./backfill.md)
- [年金客户类型：`customer_type`](./customer-type.md)
- [主拓机构](./primary-branch.md)

## 相关标准

- [客户状态语义正确性](../standards/semantic-correctness/customer-status-semantics.md)
- [输出正确性标准](../standards/output-correctness/output-correctness.md)

## 相关证据

- [customer-master signals 证据](../evidence/customer-master-signals-evidence.md)
- [引用同步与回填证据](../evidence/reference-and-backfill-evidence.md)

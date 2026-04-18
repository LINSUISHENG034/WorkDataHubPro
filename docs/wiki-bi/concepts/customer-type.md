# 年金客户类型：`customer_type`

## 定义

这里的 `customer_type` 指 legacy 与 rebuild 语境中用于表达客户分类标签的一类字段或标签值，例如：

- `新客`
- `新客*`
- `中标客户`
- `流失客户`

它是 customer-master-derived signal family 的一部分，经常与 [`tags`](./tags.md)、主拓对象和关键计划等信号并存。

## 业务意义

这类标签更接近：

- 主数据分类
- 回填生成的客户标签
- 某些事实来源触发的静态或半静态分类

它不等同于快照状态判断。

## 不应被改写的约束

- `customer_type` 与 `is_new` 不是同一层语义
- 它的来源可能是回填模板或聚合机制，而不是快照状态引擎
- 不能因为名字相似，把客户标签误当作经营状态
- `customer_type` 往往缺少时间前缀，因此需要与 `tags` 配合看，不能单靠标签值推断事件月份

## 输入现实与边界情况

- 不同 domain 可写入不同客户类型标签
- award / loss / performance / income 的标签生成逻辑并不完全相同
- `新客` / `新客*` / `中标客户` / `流失客户` 更像分类结论；`yyMM新建` / `yyMM中标` / `yyMM流失` 则承接时间轨迹

## 对输出与下游的影响

- 影响 `customer.客户明细` 等主数据层的解释
- 影响 operator 对客户分类标签的理解
- 容易在对照 `is_new` 时引发语义误读

## proxy 冲突提醒

- `customer_type` 与 `is_new` 在语义上不等价。
- legacy 相邻流程里可能会把 `customer_type` label 当作 `is_new` 的近似 proxy，但这只是治理上下文，不是 durable semantic definition。
- 当前应把这类 proxy usage 显式保留为冲突背景，而不是静默写成“客户类型就是新到账状态”。

## 常见误解 / 非例

- `年金客户类型 = 中标客户` 不等于 `is_new`
- `年金客户类型 = 新客` 不自动等于快照新到账状态
- `年金客户类型 = 流失客户` 不自动等于 `is_loss_reported`

## 相关概念

- [新到账客户状态：`is_new`](./is-new.md)
- [回填：`backfill`](./backfill.md)
- [`tags`](./tags.md)

## 相关标准

- [客户状态语义正确性](../standards/semantic-correctness/customer-status-semantics.md)

## 相关证据

- [customer 年度身份证据](../evidence/customer-status-annual-identity-evidence.md)
- [状态与快照证据](../evidence/status-and-snapshot-evidence.md)
- [operator 与 surface 证据](../evidence/operator-and-surface-evidence.md)
- [customer-master signals 证据](../evidence/customer-master-signals-evidence.md)

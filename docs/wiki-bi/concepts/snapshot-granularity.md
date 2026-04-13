# 快照粒度：`snapshot_granularity`

## 定义

当前稳定快照粒度至少包括两层：

- 客户 / 产品线粒度
- 客户 / 计划 / 产品线粒度

## 业务意义

不同粒度承载不同判断：

- 客户 / 产品线粒度更适合表达经营状态与年度状态
- 客户 / 计划粒度更适合表达具体计划层 contract 与 churn 判断

## 不应被改写的约束

- 不同粒度不应被混成同一张“万能快照”
- 某些状态只存在于产品线粒度，不存在计划粒度
- 粒度变化会直接改变输出解释，不是普通实现细节

## 输入现实与边界情况

- 粒度依赖 fact、contract、award、loss 等多类输入
- 计划层与产品线层的聚合路径不同

## 对输出与下游的影响

- 影响 `is_new` 这样的状态应落在哪一层
- 影响 plan_count、aum_balance、contract_status 等输出解释

## 常见误解 / 非例

- 计划粒度快照不等于“把客户粒度快照复制一份”
- 没有计划粒度的 `is_new` 不代表设计缺漏，而是语义边界不同

## 相关概念

- [客户状态总览](./customer-status.md)
- [新到账客户状态：`is_new`](./is-new.md)

## 相关标准

- [输出正确性标准](../standards/output-correctness/output-correctness.md)

## 相关证据

- [状态与快照证据](../evidence/status-and-snapshot-evidence.md)

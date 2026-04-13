# 客户状态总览

## 定义

客户状态是一组用于表达客户经营语义、业务变化与快照判断的状态对象。

它不是单一字段，也不应被混同为单一表结构。

## 业务意义

客户状态回答的不是“表里有没有值”，而是：

- 客户是否在当前年度中标
- 是否被申报流失
- 是否已经流失
- 是否属于新到账
- 在年度身份维度上是否 strategic / existing

## 不应被改写的约束

- 状态字段的业务意义不能被某次实现方式重写
- 状态与客户分类标签不是同一层语义
- 不同状态可能来自不同事实来源，不能强行归并为单一 source
- 快照状态与主数据标签必须分层理解

## 输入现实与边界情况

- `annual_award` 与 `annual_loss` 会影响部分状态判断
- `annuity_performance` 提供规模与快照所需的关键事实
- 有些状态只存在于客户/产品线粒度，不存在计划粒度

## 主要状态

- [`is_new`](./is-new.md)
- `is_winning_this_year`
- `is_loss_reported`
- `is_churned_this_year`

## 常见误解 / 非例

- `is_new` 不等于 `年金客户类型`
- `中标客户` 标签不等于“当前快照中的新到账状态”
- 状态不应被理解为 hook 顺序本身

## 相关 atomic concepts

- [新到账客户状态：`is_new`](./is-new.md)

## 相关标准

- [客户状态语义正确性](../standards/semantic-correctness/customer-status-semantics.md)
- [输出正确性标准](../standards/output-correctness/output-correctness.md)

## 相关证据

- [状态与快照证据](../evidence/status-and-snapshot-evidence.md)

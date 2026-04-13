# 客户状态语义正确性

> standard_type: `semantic-correctness`
> related_standard_types: `output-correctness`, `verification-method`

## 标准对象

本页定义客户状态相关判断在语义上怎样才算正确。

## 适用范围

- `is_new`
- `is_winning_this_year`
- `is_loss_reported`
- `is_churned_this_year`
- `customer_type` 与状态的边界

## 正确性定义

语义正确的状态判断应满足：

- 不把标签字段误写成状态字段
- 不混淆不同事实来源
- 不跨粒度滥用状态定义

## 关键约束

- `is_new` 与 `年金客户类型` 必须分层理解
- status source 可以不同，不能假设所有状态都来自同一事实表
- 产品线粒度与计划粒度的状态集合不应被强行对齐

## 非例

- 用 `customer_type` 直接替代 `is_new`
- 因为实现方便，就给计划级快照添加并不存在的状态语义

## 相关概念

- [客户状态总览](../../concepts/customer-status.md)
- [新到账客户状态：`is_new`](../../concepts/is-new.md)
- [年金客户类型：`customer_type`](../../concepts/customer-type.md)

## 相关证据

- [状态与快照证据](../../evidence/status-and-snapshot-evidence.md)

## 相关验证方法

- [real-data validation](../verification-method/real-data-validation.md)

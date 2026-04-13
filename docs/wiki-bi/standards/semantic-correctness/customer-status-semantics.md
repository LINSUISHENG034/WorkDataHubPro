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
- 把 contract / status / snapshot 分层理解

## 状态语义检查表

判断客户状态语义是否正确时，至少要检查：

1. 该状态的事实来源是否明确
2. 该状态属于哪一层
   - fact source
   - contract / customer plan
   - snapshot
3. 该状态适用于哪个粒度
4. 它是否被错误地与标签字段混同

## 关键状态口径

- `is_winning_this_year`
  - 年度中标事实
- `is_loss_reported`
  - 年度流失申报事实
- `is_churned_this_year`
  - 基于规模表现的已流失判断
- `is_new`
  - 当年中标且非 existing
- `is_strategic` / `is_existing` / `contract_status`
  - 以 `customer.客户年金计划` 为核心锚点的状态家族

## 关键约束

- `is_new` 与 `年金客户类型` 必须分层理解
- status source 可以不同，不能假设所有状态都来自同一事实表
- 产品线粒度与计划粒度的状态集合不应被强行对齐
- `customer.客户年金计划` 的状态锚点不应被误写为快照字段本身

## 非例

- 用 `customer_type` 直接替代 `is_new`
- 因为实现方便，就给计划级快照添加并不存在的状态语义
- 因为 hook 顺序存在，就把顺序本身写成状态定义

## 相关概念

- [客户状态总览](../../concepts/customer-status.md)
- [新到账客户状态：`is_new`](../../concepts/is-new.md)
- [年金客户类型：`customer_type`](../../concepts/customer-type.md)
- [快照粒度：`snapshot_granularity`](../../concepts/snapshot-granularity.md)

## 相关证据

- [状态与快照证据](../../evidence/status-and-snapshot-evidence.md)

## 相关验证方法

- [real-data validation](../verification-method/real-data-validation.md)

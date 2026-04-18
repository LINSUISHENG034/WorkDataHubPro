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
- `is_strategic`
- `is_existing`
- `contract_status`
- `status_year`
- `customer_type` 与状态的边界

## 正确性定义

语义正确的状态判断应满足：

- 不把标签字段误写成状态字段
- 不混淆不同事实来源
- 不跨粒度滥用状态定义
- 把 formula memory / yearly lifecycle semantics / operator surface 分层理解

## 状态语义检查表

判断客户状态语义是否正确时，至少要检查：

1. 该状态的事实来源是否明确
2. 该状态属于哪一层
   - fact source
   - contract / customer plan
   - snapshot
3. 该状态是 yearly 还是 monthly 语义
4. 该状态适用于哪个粒度
5. 它是否被错误地与标签字段混同

## 关键状态口径

- `is_winning_this_year`
  - 由 [`annual_award`](../../domains/annual-award.md) 提供的年度中标事实
- `is_loss_reported`
  - 由 [`annual_loss`](../../domains/annual-loss.md) 提供的年度流失申报事实
- `is_churned_this_year`
  - 由 [`annuity_performance`](../../domains/annuity-performance.md) 承接规模表现后的已流失判断
- `is_new`
  - 当年中标且非 existing
- `is_strategic` / `is_existing` / `contract_status` / `status_year`
  - 以 `customer.客户年金计划` 为核心锚点的年度身份家族

## `status_year` 语义口径

- `status_year` 表达的是年度身份锚点，不应被误解为“所有状态字段唯一数据源”。
- `status_year` 与 `snapshot_month` 不是可互换字段：一个是年度语义锚点，一个是月度快照锚点。
- 若运行时来源仍未完全闭环，应登记为 evidence gap，不可写成稳定 runtime 结论。

## annual identity family 语义口径

- `is_strategic`、`is_existing`、`contract_status`、`status_year` 应作为同一 annual identity family 分层理解，而不是拆成互不相关的零散状态。
- strategic 身份具有 ratchet-style 语义：允许升级，不应因短期回落自动降级。
- `customer.客户年金计划` 承担年度身份锚点；快照负责消费与展示，不应反向改写 annual identity family 的定义。

## `customer_type` proxy 冲突口径

- `customer_type` 不能被静默提升为 `is_new` truth。
- 若 legacy 相邻流程中存在把 `customer_type` label 当作 `is_new` proxy 的做法，应记录为治理上下文或 evidence gap，而不是写成语义等价。
- 这类 proxy conflict 尚未 current-side 收口时，应保持“语义已分层、治理仍待裁决”的表达。
- 一旦进入治理收口阶段，应把它写成显式 disposition package，而不是继续只保留一句“存在冲突”的提醒。

## 关键约束

- `is_new` 与 `年金客户类型` 必须分层理解
- status source 可以不同，不能假设所有状态都来自同一事实表
- 产品线粒度与计划粒度的状态集合不应被强行对齐
- `customer.客户年金计划` 的状态锚点不应被误写为快照字段本身
- `status_year` 与 `snapshot_month` 不应互相替代
- strategic ratchet 语义属于业务定义，不应降格为“实现细节”
- 命令调用方式、hook 顺序、CLI 参数不属于语义标准正文

## 非例

- 用 `customer_type` 直接替代 `is_new`
- 因为实现方便，就给计划级快照添加并不存在的状态语义
- 因为 hook 顺序存在，就把顺序本身写成状态定义

## 相关概念

- [客户状态总览](../../concepts/customer-status.md)
- [新到账客户状态：`is_new`](../../concepts/is-new.md)
- [年金客户类型：`customer_type`](../../concepts/customer-type.md)
- [快照粒度：`snapshot_granularity`](../../concepts/snapshot-granularity.md)

## 相关 domains

- [`annual_award`](../../domains/annual-award.md)
- [`annual_loss`](../../domains/annual-loss.md)
- [`annuity_performance`](../../domains/annuity-performance.md)

## 相关证据

- [状态与快照证据](../../evidence/status-and-snapshot-evidence.md)
- [customer 年度身份证据](../../evidence/customer-status-annual-identity-evidence.md)
- [customer_type vs `is_new` 治理证据](../../evidence/customer-type-is-new-governance-evidence.md)
- [customer MDM 生命周期证据](../../evidence/customer-mdm-lifecycle-evidence.md)
- [`is_new` 对象级证据](../../evidence/is-new-evidence.md)
- [`is_winning_this_year` 对象级证据](../../evidence/is-winning-this-year-evidence.md)
- [`is_loss_reported` 对象级证据](../../evidence/is-loss-reported-evidence.md)

## 相关验证方法

- [real-data validation](../verification-method/real-data-validation.md)

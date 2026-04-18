# 客户状态总览

## 定义

客户状态是一组用于表达客户经营语义、年度身份与快照判断的状态对象。

它不是单一字段，也不应被混同为单一表结构。

## 业务意义

客户状态回答的不是“表里有没有值”，而是：

- 客户是否在当前年度中标
- 是否被申报流失
- 是否已经流失
- 是否属于新到账
- 在年度身份维度上是否 strategic / existing，以及它处在哪种 contract / status_year 语境

## 公式记忆（语义层）

- `is_new = is_winning_this_year AND NOT is_existing`
- `is_winning_this_year` / `is_loss_reported` 属于年度语义
- `is_churned_this_year` 由月度规模事实承接，表示匹配粒度在当前快照月的 AUM 汇总为 `0`，或当月已无记录
- `is_churned_this_year` 不等于 `is_loss_reported`；前者是 monthly churn judgement，后者是 annual loss-report fact

这里保留的是语义与公式记忆，不承载命令触发、hook 顺序或运行时参数。

## 年度身份家族

`is_strategic`、`is_existing`、`contract_status`、`status_year` 应一起理解为 customer annual identity family。

这组字段回答的是“客户在某一年度语境中的身份与合同状态如何被锚定”，而不是单次快照有没有命中某个标签。

- `status_year`
  - 年度身份锚点，不等于 `snapshot_month`
- `is_strategic`
  - 承接 strategic 身份判断，并保留 ratchet-style 只升不自动降的语义
- `is_existing`
  - 承接“上一年度语境已存在”的身份记忆
- `contract_status`
  - 承接年度身份语境中的合同状态判断

这组语义的对象级证据入口见 [customer 年度身份证据](../evidence/customer-status-annual-identity-evidence.md)。

## 分层模型

从业务角度，客户状态至少要分成三层来看：

- 事实层
  - [`annuity_performance`](../domains/annuity-performance.md)、[`annual_award`](../domains/annual-award.md)、[`annual_loss`](../domains/annual-loss.md) 提供原始事实
- 主数据 / contract 层
  - `customer.客户年金计划` 承载 contract、existing、strategic、status_year 等状态锚点
- 快照层
  - `customer.客户业务月度快照`
  - `customer.客户计划月度快照`

这三层不能被理解成一张“万能状态表”。

## 不应被改写的约束

- 状态字段的业务意义不能被某次实现方式重写
- 状态与客户分类标签不是同一层语义
- 不同状态可能来自不同事实来源，不能强行归并为单一 source
- 快照状态与主数据标签必须分层理解
- contract / strategic / existing 与 snapshot 判断不是同一层逻辑

## 状态来源映射

- `is_winning_this_year`
  - 来源于 [`annual_award`](../domains/annual-award.md)
- `is_loss_reported`
  - 来源于 [`annual_loss`](../domains/annual-loss.md)
- `is_churned_this_year`
  - 来源于 [`annuity_performance`](../domains/annuity-performance.md)
  - 客户 / 产品线粒度以 `company_id + product_line_code` 匹配；计划层 sibling 字段再加上 `plan_code`
- `is_new`
  - 来源于派生判断：当年中标且非 existing
- `is_strategic` / `is_existing` / `contract_status` / `status_year`
  - 主要锚定在 `customer.客户年金计划` 的年度生命周期语义

## 主要状态

- [`is_new`](./is-new.md)
- `is_winning_this_year`
- `is_loss_reported`
- `is_churned_this_year`
- `is_strategic`
- `is_existing`
- `contract_status`
- `status_year`

## 常见误解 / 非例

- `is_new` 不等于 `年金客户类型`
- `中标客户` 标签不等于“当前快照中的新到账状态”
- 状态不应被理解为 hook 顺序本身
- `contract_status` 不等于“所有状态的总开关”
- `status_year` 不等于普通年份字段，也不等于 `snapshot_month`
- `is_churned_this_year` 不等于 `is_loss_reported`；不能把申报流失事实当作 monthly churn 的 proxy

## 生命周期证据入口

- [customer 年度身份证据](../evidence/customer-status-annual-identity-evidence.md)
- [customer MDM 生命周期证据](../evidence/customer-mdm-lifecycle-evidence.md)
- [`customer-mdm` 手工命令面](../surfaces/customer-mdm-commands.md)

## 相关原子概念

- [新到账客户状态：`is_new`](./is-new.md)

## 相关 domain

- [`annual_award`](../domains/annual-award.md)
- [`annual_loss`](../domains/annual-loss.md)
- [`annuity_performance`](../domains/annuity-performance.md)

## 相关标准

- [客户状态语义正确性](../standards/semantic-correctness/customer-status-semantics.md)
- [输出正确性标准](../standards/output-correctness/output-correctness.md)
- [real-data validation](../standards/verification-method/real-data-validation.md)

## 相关证据

- [状态与快照证据](../evidence/status-and-snapshot-evidence.md)
- [customer 年度身份证据](../evidence/customer-status-annual-identity-evidence.md)
- [customer MDM 生命周期证据](../evidence/customer-mdm-lifecycle-evidence.md)
- [operator 与 surface 证据](../evidence/operator-and-surface-evidence.md)
- [`is_new` 对象级证据](../evidence/is-new-evidence.md)
- [`is_winning_this_year` 对象级证据](../evidence/is-winning-this-year-evidence.md)
- [`is_loss_reported` 对象级证据](../evidence/is-loss-reported-evidence.md)

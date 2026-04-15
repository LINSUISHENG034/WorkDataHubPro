# `annual_award`

## 该 domain 处理的业务事实

`annual_award` 处理年度中标事实，是 event-style domain 的代表之一。

它最关键的业务特点包括：

- 多 sheet 输入现实
- `company_id` 识别
- 缺失计划号的补全
- 对客户状态判断的下游影响
- 与 `annual_loss` 共同证明 event domain 不是“单 sheet 边缘例外”

## 核心概念入口

- [企业身份标识：`company_id`](../concepts/company-id.md)
- [临时身份：`temp_id`](../concepts/temp-id.md)
- [年金计划类型：`plan_type`](../concepts/plan-type.md)
- [客户状态总览](../concepts/customer-status.md)
- [快照粒度：`snapshot_granularity`](../concepts/snapshot-granularity.md)

## 关键输出结果

- `fact_annual_award` 直接事实输出
- `company_reference` 与 `customer_master_signal`
- 对 `is_winning_this_year` / `is_new` 的上游支撑
- 为 `contract_state` / `monthly_snapshot` 提供年度中标事实来源
- 对缺失计划号和身份识别形成 event-domain 级别的补齐压力

## 适用标准

- [输入现实合同](../standards/input-reality/input-reality-contracts.md)
- [`annual_award` 输入合同](../standards/input-reality/annual-award-input-contract.md)
- [客户状态语义正确性](../standards/semantic-correctness/customer-status-semantics.md)
- [身份治理语义正确性](../standards/semantic-correctness/identity-governance.md)
- [输出正确性标准](../standards/output-correctness/output-correctness.md)
- [`annual_award` 输出合同](../standards/output-correctness/annual-award-output-contract.md)
- [real-data validation](../standards/verification-method/real-data-validation.md)
- [golden scenarios](../standards/verification-method/golden-scenarios.md)

## 关键证据来源

- [输入现实证据](../evidence/input-reality-evidence.md)
- [`annual_award` 字段处理证据](../evidence/annual-award-field-processing-evidence.md)
- [身份与补查证据](../evidence/identity-and-lookup-evidence.md)
- [状态与快照证据](../evidence/status-and-snapshot-evidence.md)
- [`is_winning_this_year` 对象级证据](../evidence/is-winning-this-year-evidence.md)
- [验证资产证据](../evidence/verification-assets-evidence.md)
- [validation result history 证据](../evidence/validation-result-history-evidence.md)

## 相关 domains

- [`annual_loss`](./annual-loss.md)
- [`annuity_performance`](./annuity-performance.md)

## 明确不在本页描述的内容

- adapter / service walkthrough
- 每个 trace event 的实现细节
- 当前 rebuild coverage status

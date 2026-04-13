# `annual_loss`

## 该 domain 处理的业务事实

`annual_loss` 处理年度流失申报事实，与 `annual_award` 一样属于 event-style domain，但在业务含义上对应流失而不是中标。

## 核心概念入口

- [企业身份标识：`company_id`](../concepts/company-id.md)
- [年金计划类型：`plan_type`](../concepts/plan-type.md)
- [客户状态总览](../concepts/customer-status.md)
- [快照粒度：`snapshot_granularity`](../concepts/snapshot-granularity.md)

## 关键输出结果

- 流失事实输出
- 客户标签与回填信号
- 对 `is_loss_reported` 的上游支撑

## 适用标准

- [输入现实合同](../standards/input-reality/input-reality-contracts.md)
- [客户状态语义正确性](../standards/semantic-correctness/customer-status-semantics.md)
- [输出正确性标准](../standards/output-correctness/output-correctness.md)
- [real-data validation](../standards/verification-method/real-data-validation.md)
- [golden scenarios](../standards/verification-method/golden-scenarios.md)

## 关键证据来源

- [输入现实证据](../evidence/input-reality-evidence.md)
- [身份与补查证据](../evidence/identity-and-lookup-evidence.md)
- [状态与快照证据](../evidence/status-and-snapshot-evidence.md)
- [验证资产证据](../evidence/verification-assets-evidence.md)

## 明确不在本页描述的内容

- event pipeline 代码流程
- 当前 rebuild coverage status

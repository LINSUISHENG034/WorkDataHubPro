# `annuity_performance`

## 该 domain 处理的业务事实

`annuity_performance` 处理规模相关事实，是当前跨 domain 链路里最能把：

- 输入现实
- 身份解析
- 回填
- contract / snapshot

串起来的核心业务域。

## 核心概念入口

- [企业身份标识：`company_id`](../concepts/company-id.md)
- [客户状态总览](../concepts/customer-status.md)
- [年金计划类型：`plan_type`](../concepts/plan-type.md)
- [回填：`backfill`](../concepts/backfill.md)
- [快照粒度：`snapshot_granularity`](../concepts/snapshot-granularity.md)

## 关键输出结果

- 规模事实输出
- 客户 / 参考对象回填
- customer contract 与快照相关输出

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
- [operator 与 surface 证据](../evidence/operator-and-surface-evidence.md)

## 明确不在本页描述的内容

- pipeline step 顺序
- hook 具体执行顺序
- 当前 rebuild 实现进度

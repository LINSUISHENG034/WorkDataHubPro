# `annuity_income`

## 该 domain 处理的业务事实

`annuity_income` 处理收入相关事实。

在当前 `wiki-bi` 里，这个 domain 还同时承担一个额外角色：

- 保留 legacy 证据簇与未闭合问题的入口

因为它是 first-wave 中最需要避免“被遗忘”的 domain 之一。

在输入现实上，它还意味着：

- 不能因为当前 rebuild 未实现，就丢失其 source workbook、sheet 和 branch mapping 等制度记忆

## 核心概念入口

- [企业身份标识：`company_id`](../concepts/company-id.md)
- [临时身份：`temp_id`](../concepts/temp-id.md)
- [年金计划类型：`plan_type`](../concepts/plan-type.md)
- [回填：`backfill`](../concepts/backfill.md)

## 关键输出结果

- 收入事实输出
- customer / mapping 相关回填信号
- identity / branch mapping 相关遗留约束
- identity fallback retirement decisions 与 unresolved-name artifacts 的制度记忆

## 适用标准

- [输入现实合同](../standards/input-reality/input-reality-contracts.md)
- [输出正确性标准](../standards/output-correctness/output-correctness.md)
- [golden scenarios](../standards/verification-method/golden-scenarios.md)

## 关键证据来源

- [输入现实证据](../evidence/input-reality-evidence.md)
- [身份与补查证据](../evidence/identity-and-lookup-evidence.md)
- [验证资产证据](../evidence/verification-assets-evidence.md)
- [operator 与 surface 证据](../evidence/operator-and-surface-evidence.md)

## 明确不在本页描述的内容

- 当前 rebuild 是否已实现该 domain 的执行态结论
- 具体规划步骤

本页更适合作为后续把 `annuity_income` 的稳定语义、验证资产与遗留约束吸收进 wiki 的导航入口。

当前尤其要避免的是：

- 因为 `annuity_income` 尚未落地，就把其 golden / parity / identity 制度记忆从 wiki 中删除

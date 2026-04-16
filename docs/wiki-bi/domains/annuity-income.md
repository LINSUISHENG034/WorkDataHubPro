# `annuity_income`

## 该 domain 处理的业务事实

`annuity_income` 处理收入相关事实。

在当前 `wiki-bi` 里，这个 domain 还承担两个额外角色：

- 保留 legacy 证据簇与 identity / artifact 制度记忆的入口
- 作为已确认 confirmed domain 的合同级问答入口

它不再只是“等待以后实现”的占位对象。

current project 已有：

- accepted validation slice
- targeted tests
- replay assets
- runbook

在输入现实上，它还意味着：

- 不能因为它与 `annuity_performance` 共用 workbook family，就把 `收入明细` sheet 的独立合同写没

在身份与验证上，它还意味着：

- 不能忘记 ID5 fallback 已被显式 retirement
- 不能忘记它有自己的 parity validation memory 与 operator artifacts

## 核心概念入口

- [企业身份标识：`company_id`](../concepts/company-id.md)
- [临时身份：`temp_id`](../concepts/temp-id.md)
- [年金计划类型：`plan_type`](../concepts/plan-type.md)
- [回填：`backfill`](../concepts/backfill.md)

## 关键输出结果

- direct fact output
- reference / customer signal
- unresolved identity 的 operator-facing artifacts
- post-ID5 identity governance 与 branch mapping 约束

## Wave 01 M2 语义聚焦（薄页指针）

- hidden field semantics：
  - `客户名称` 在清洗前会复制为 `年金账户名`，用于后续 identity 解析与审计线索保留
  - `计划类型=单一计划` 且 `计划名称` 匹配 `企业年金计划` 后缀时，空 `客户名称` 可由计划名提取
- operator-visible differences：
  - unresolved identity 不是静默丢弃；需要外显为 `unknown_names_csv` / failed-record artifacts
  - 当前 contract 明确 `projection_results = []`，不把 legacy hook 路径伪装成默认运行路径

具体规则、证据强度与缺口统一沉淀在输入/输出合同与字段处理证据页，本页不展开 pipeline 细节。

## 合同级入口

- [`annuity_income` 输入合同](../standards/input-reality/annuity-income-input-contract.md)
- [`annuity_income` 输出合同](../standards/output-correctness/annuity-income-output-contract.md)
- [`annuity_income` 字段处理证据](../evidence/annuity-income-field-processing-evidence.md)

## 适用标准

- [输入现实合同](../standards/input-reality/input-reality-contracts.md)
- [`annuity_income` 输入合同](../standards/input-reality/annuity-income-input-contract.md)
- [输出正确性标准](../standards/output-correctness/output-correctness.md)
- [`annuity_income` 输出合同](../standards/output-correctness/annuity-income-output-contract.md)
- [golden scenarios](../standards/verification-method/golden-scenarios.md)
- [身份治理语义正确性](../standards/semantic-correctness/identity-governance.md)

## 关键证据来源

- [引用同步与回填证据](../evidence/reference-and-backfill-evidence.md)
- [`annuity_income` 字段处理证据](../evidence/annuity-income-field-processing-evidence.md)
- [annuity workbook family 证据](../evidence/annuity-workbook-family-evidence.md)
- [输入现实证据](../evidence/input-reality-evidence.md)
- [身份与补查证据](../evidence/identity-and-lookup-evidence.md)
- [验证资产证据](../evidence/verification-assets-evidence.md)
- [operator 与 surface 证据](../evidence/operator-and-surface-evidence.md)
- [`annuity_income` 专题证据](../evidence/annuity-income-gap-evidence.md)
- [`annuity_income` branch mapping 证据](../evidence/annuity-income-branch-mapping-evidence.md)
- [`annuity_income` ID5 retirement 证据](../evidence/annuity-income-id5-retirement-evidence.md)
- [`annuity_income` operator artifacts 证据](../evidence/annuity-income-operator-artifacts-evidence.md)

## 当前 production reality 问答

- accepted source contract：[`annuity_income` 输入合同](../standards/input-reality/annuity-income-input-contract.md) 中定义的 `收入明细` sheet contract。
- observed production reality：代表性单月生产样本验证表明，annuity workbook family 在同一本物理 workbook 中同时出现 `规模明细` 与 `收入明细`。
- stable contract：`annuity_income` 仍只认领 `收入明细`，shared workbook family 不会把收入域与规模域写成同一 accepted contract。
- observed production variant：shared workbook family 属于 workbook-discovery 与 explainability 线索，不是把一个观测月份自动推广为 universal contract 的依据。

## 明确不在本页描述的内容

- 当前实现的完整代码 walkthrough
- 具体规划步骤

本页现在既是问题空间导航入口，也是 contract page / object-level evidence 的分发入口。

当前 current project 已有显式 validation slice、runbook、replay assets 与 targeted tests，说明这些先前由 wiki 保留的 institutional memory 已经成功转化为实际开发任务。

当前尤其要避免的是：

- 因为它最早以制度记忆方式进入 wiki，就让它长期停留在“只导航、不回答合同问题”的状态
- 把 compatibility memory、active runtime path 与 retired behavior 混写成一段模糊的 identity 叙述

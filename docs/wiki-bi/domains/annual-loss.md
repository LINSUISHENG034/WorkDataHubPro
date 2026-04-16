# `annual_loss`

## 该 domain 处理的业务事实

`annual_loss` 处理年度流失申报事实，与 `annual_award` 一样属于 event-style domain，但在业务含义上对应流失而不是中标。

它同样证明 multi-sheet event intake 不是单个 domain 的偶发特殊情况，而是输入现实的一部分。

## 核心概念入口

- [企业身份标识：`company_id`](../concepts/company-id.md)
- [临时身份：`temp_id`](../concepts/temp-id.md)
- [年金计划类型：`plan_type`](../concepts/plan-type.md)
- [客户状态总览](../concepts/customer-status.md)
- [快照粒度：`snapshot_granularity`](../concepts/snapshot-granularity.md)

## 关键输出结果

- `fact_annual_loss` 直接事实输出
- `company_reference` 与 `customer_loss_signal`
- 对 `is_loss_reported` 的上游支撑
- 为 `contract_state` / `monthly_snapshot` 提供年度流失申报事实来源
- 对缺失计划号、身份识别与 temp-id 治理形成 event-domain 级别的补齐压力

## 适用标准

- [输入现实合同](../standards/input-reality/input-reality-contracts.md)
- [`annual_loss` 输入合同](../standards/input-reality/annual-loss-input-contract.md)
- [客户状态语义正确性](../standards/semantic-correctness/customer-status-semantics.md)
- [身份治理语义正确性](../standards/semantic-correctness/identity-governance.md)
- [输出正确性标准](../standards/output-correctness/output-correctness.md)
- [`annual_loss` 输出合同](../standards/output-correctness/annual-loss-output-contract.md)
- [real-data validation](../standards/verification-method/real-data-validation.md)
- [golden scenarios](../standards/verification-method/golden-scenarios.md)

## 关键证据来源

- [引用同步与回填证据](../evidence/reference-and-backfill-evidence.md)
- [输入现实证据](../evidence/input-reality-evidence.md)
- [business collection workbook variants 证据](../evidence/business-collection-workbook-variants-evidence.md)
- [`annual_loss` 字段处理证据](../evidence/annual-loss-field-processing-evidence.md)
- [身份与补查证据](../evidence/identity-and-lookup-evidence.md)
- [状态与快照证据](../evidence/status-and-snapshot-evidence.md)
- [`is_loss_reported` 对象级证据](../evidence/is-loss-reported-evidence.md)
- [验证资产证据](../evidence/verification-assets-evidence.md)
- [validation result history 证据](../evidence/validation-result-history-evidence.md)
- [business collection ledger workbook](../surfaces/business-collection-ledger-workbook.md)

## 当前 production reality 问答

- accepted source contract：[`annual_loss` 输入合同](../standards/input-reality/annual-loss-input-contract.md) 中定义的 accepted contract，即台账 workbook 内的流失 sheet subset。
- observed production reality：代表性单月生产样本验证表明，business-collection ledger workbook 当前承载 accepted loss sheets，同时同目录里还存在相邻 summary workbook。
- stable contract：`annual_loss` 只认领自己的 event-domain sheets，不把整个 ledger workbook 或 summary workbook 写成 accepted contract。
- observed production variant / adjacent operator reality：`业务收集` 目录中的相邻 summary / attachment workbook 先作为 observed production variant 或 surface 处理，再等待更强证据判断是否进入未来 contract。

## 当前验证资产姿态

- 当前 active protection 由 `replay_baseline`、`synthetic_fixture` 与四个 `checkpoint_baseline` 组成。
- `golden_set`、`golden_baseline`、`error_case_fixture`、`real_data_sample` 仍是显式 `deferred`；其中 error path 当前主要由 inline event-intake tests 保护，而不是 repo-native fixture 文件。
- 这意味着本域当前已被纳入 replay-grade parity protection，但尚未进入更宽的 domain-level golden-set governance；在更广的 curated scenario pack 被 admitted 前，不应把 `golden_set` / `golden_baseline` 升级成 `planned`。

## 相关 domains

- [`annual_award`](./annual-award.md)
- [`annuity_performance`](./annuity-performance.md)

## 明确不在本页描述的内容

- event pipeline walkthrough
- 每个 compatibility case 的实现细节
- 当前 rebuild coverage status

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
- [临时身份：`temp_id`](../concepts/temp-id.md)
- [客户状态总览](../concepts/customer-status.md)
- [年金计划类型：`plan_type`](../concepts/plan-type.md)
- [回填：`backfill`](../concepts/backfill.md)
- [快照粒度：`snapshot_granularity`](../concepts/snapshot-granularity.md)

## 关键输出结果

- 规模事实输出
- 客户 / 参考对象回填
- customer contract 与快照相关输出
- 作为 [`annual_award`](./annual-award.md) / [`annual_loss`](./annual-loss.md) 状态落地的关键承接域

## 适用标准

- [输入现实合同](../standards/input-reality/input-reality-contracts.md)
- [`annuity_performance` 输入合同](../standards/input-reality/annuity-performance-input-contract.md)
- [客户状态语义正确性](../standards/semantic-correctness/customer-status-semantics.md)
- [输出正确性标准](../standards/output-correctness/output-correctness.md)
- [`annuity_performance` 输出合同](../standards/output-correctness/annuity-performance-output-contract.md)
- [real-data validation](../standards/verification-method/real-data-validation.md)
- [golden scenarios](../standards/verification-method/golden-scenarios.md)

## 关键证据来源

- [输入现实证据](../evidence/input-reality-evidence.md)
- [annuity workbook family 证据](../evidence/annuity-workbook-family-evidence.md)
- [`annuity_performance` 字段处理证据](../evidence/annuity-performance-field-processing-evidence.md)
- [`annuity_performance` implementation gap 证据](../evidence/annuity-performance-implementation-gap-evidence.md)
- [身份与补查证据](../evidence/identity-and-lookup-evidence.md)
- [状态与快照证据](../evidence/status-and-snapshot-evidence.md)
- [验证资产证据](../evidence/verification-assets-evidence.md)
- [operator 与 surface 证据](../evidence/operator-and-surface-evidence.md)

## 当前 production reality 问答

- accepted source contract：[`annuity_performance` 输入合同](../standards/input-reality/annuity-performance-input-contract.md) 中定义的 `规模明细` sheet contract。
- observed production reality：代表性单月生产样本验证表明，annuity workbook family 在同一本物理 workbook 中同时出现 `规模明细` 与 `收入明细`。
- stable contract：`annuity_performance` 只认领 `规模明细`，不会因为 shared workbook family 而与 `annuity_income` 合并成一个 accepted contract。
- observed production variant：shared workbook family 用于 workbook discovery 与 explainability 补强，不用于把单月观测上升为 universal contract。

## 当前验证资产姿态

- 当前 active protection 由 `replay_baseline`、`synthetic_fixture` 与四个 `checkpoint_baseline` 组成。
- `golden_set`、`golden_baseline`、`error_case_fixture`、`real_data_sample` 仍是显式 `deferred`；其中 error path 当前主要由 inline intake tests 保护，而不是 repo-native fixture 文件。
- 这足以支撑 accepted slice parity gates，但不应被误写成已具备 repo-native golden set 或 real-data sample。

## 相关 domains

- [`annual_award`](./annual-award.md)
- [`annual_loss`](./annual-loss.md)

## 明确不在本页描述的内容

- pipeline step 顺序
- hook 具体执行顺序
- 当前 rebuild 实现进度

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
- [组合代码](../concepts/portfolio-code.md)
- [回填：`backfill`](../concepts/backfill.md)
- [`tags`](../concepts/tags.md)
- [主拓机构](../concepts/primary-branch.md)
- [关联计划数](../concepts/related-plan-count.md)
- [其他年金计划](../concepts/other-annuity-plans.md)
- [关联机构数](../concepts/related-branch-count.md)
- [其他开拓机构](../concepts/other-branches.md)
- [管理资格](../concepts/management-qualification.md)
- [快照粒度：`snapshot_granularity`](../concepts/snapshot-granularity.md)

## 关键输出结果

- direct fact output（规模事实）
- reference / customer object backfill
- customer contract 与快照相关派生输出
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

- [引用同步与回填证据](../evidence/reference-and-backfill-evidence.md)
- [输入现实证据](../evidence/input-reality-evidence.md)
- [annuity workbook family 证据](../evidence/annuity-workbook-family-evidence.md)
- [customer-master signals 证据](../evidence/customer-master-signals-evidence.md)
- [`annuity_performance` 字段处理证据](../evidence/annuity-performance-field-processing-evidence.md)
- [`annuity_performance` implementation gap 证据](../evidence/annuity-performance-implementation-gap-evidence.md)
- [身份与补查证据](../evidence/identity-and-lookup-evidence.md)
- [状态与快照证据](../evidence/status-and-snapshot-evidence.md)
- [验证资产证据](../evidence/verification-assets-evidence.md)
- [operator 与 surface 证据](../evidence/operator-and-surface-evidence.md)
- [unresolved-name and failed-record 证据](../evidence/unresolved-name-and-failed-record-evidence.md)

## 当前生产现实问答

- accepted source contract：[`annuity_performance` 输入合同](../standards/input-reality/annuity-performance-input-contract.md) 中定义的 `规模明细` sheet contract。
- 观测到的生产现实：代表性单月生产样本验证表明，annuity workbook family 在同一本物理 workbook 中同时出现 `规模明细` 与 `收入明细`。
- stable contract：`annuity_performance` 只认领 `规模明细`，不会因为 shared workbook family 而与 `annuity_income` 合并成一个 accepted contract。
- observed production variant：shared workbook family 用于 workbook discovery 与 explainability 补强，不用于把单月观测上升为 universal contract。

## 当前验证资产姿态

- 当前 active protection 由 `replay_baseline`、`synthetic_fixture` 与四个 `checkpoint_baseline` 组成。
- `golden_set`、`golden_baseline`、`error_case_fixture`、`real_data_sample` 仍是显式 `deferred`；其中 error path 当前主要由 inline intake tests 保护，而不是 repo-native fixture 文件。
- 这足以支撑 accepted slice parity gates，但不应被误写成已具备 repo-native golden set 或 real-data sample。

## 隐藏字段语义入口（M1）

- 输入侧关键语义（`客户名称` / `年金账户名`、`集团企业客户号` / `年金账户号`、row-level hard gate）见 [`annuity_performance` 输入合同](../standards/input-reality/annuity-performance-input-contract.md)。
- 输出侧关键语义（`max_by` 主拓机构/关键计划、`tags=yyMM新建`、temp-id backfill 边界）见 [`annuity_performance` 输出合同](../standards/output-correctness/annuity-performance-output-contract.md)。
- cross-domain customer-master-derived signal family（`主拓机构`、`关键年金计划`、`关联计划数`、`关联机构数`、`其他年金计划`、`其他开拓机构`、`yyMM新建`）见 [customer-master signals 证据](../evidence/customer-master-signals-evidence.md)。
- relationship breadth 现在在计划侧与机构侧都形成 dominant/count/list 三层：
  - 计划侧见 [关键年金计划](../concepts/key-annuity-plan.md)、[关联计划数](../concepts/related-plan-count.md)、[其他年金计划](../concepts/other-annuity-plans.md)
  - 机构侧见 [主拓机构](../concepts/primary-branch.md)、[关联机构数](../concepts/related-branch-count.md)、[其他开拓机构](../concepts/other-branches.md)
- classification family 中的 customer-master 聚合分类见 [管理资格](../concepts/management-qualification.md) 与 [classification family 证据](../evidence/classification-family-evidence.md)。
- portfolio/classification anchor 见 [组合代码](../concepts/portfolio-code.md)；它回答 fact rows 如何接回 `mapping.组合计划` 语境，而不是客户身份或 customer-master 聚合分类。
- legacy unresolved-name / failed-record artifacts 现在有 shared evidence page；它说明 `annuity_performance` 属于 historical artifact breadth，但 current accepted parity 仍未闭环：[unresolved-name and failed-record 证据](../evidence/unresolved-name-and-failed-record-evidence.md)。
- 字段级证据和证据强度分层见 [`annuity_performance` 字段处理证据](../evidence/annuity-performance-field-processing-evidence.md)。

## 相关 domains

- [`annual_award`](./annual-award.md)
- [`annual_loss`](./annual-loss.md)

## 明确不在本页描述的内容

- pipeline step 顺序
- hook 具体执行顺序
- 当前 rebuild 实现进度

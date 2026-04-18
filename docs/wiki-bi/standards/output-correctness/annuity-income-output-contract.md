# `annuity_income` 输出合同

> standard_type: `output-correctness`
> related_standard_types: `verification-method`, `input-reality`

## 标准对象

本页定义 `annuity_income` 的输出合同。

它回答：

- 哪些结果属于 direct fact output
- 哪些结果属于 reference / customer signal
- 当前 slice 明确不经过哪些 projection hook

## 证据锚点（evidence-first）

- `legacy_doc`
  - `E:\Projects\WorkDataHub\docs/domains/annuity_income.md`
  - `E:\Projects\WorkDataHub\docs/domains/annuity_income-capability-map.md`
  - `E:\Projects\WorkDataHub\docs/runbooks/annuity_income.md`
- `legacy_code`
  - `E:\Projects\WorkDataHub\src\work_data_hub\domain\annuity_income\service.py`
  - `E:\Projects\WorkDataHub\src\work_data_hub\domain\annuity_income\helpers.py`
  - `E:\Projects\WorkDataHub\src\work_data_hub\domain\annuity_income\schemas.py`
- `current_code`
  - `src/work_data_hub_pro/capabilities/fact_processing/annuity_income/service.py`
  - `src/work_data_hub_pro/apps/orchestration/replay/annuity_income_slice.py`

## 直接事实输出

legacy 侧的稳定 direct fact sink 是：

- `business."收入明细"`

这代表 domain 自身首先要交付的是收入事实，而不是先交付状态投影。

在 current project 中，对应的显式 publication target 是：

- `fact_annuity_income`

## 回填目标

legacy 合同仍明确要求该域能为下列 reference / customer objects 提供输入：

- `mapping."年金计划"`
- `mapping."组合计划"`
- `mapping."产品线"`
- `mapping."组织架构"`
- `customer."客户明细"`

这些对象说明 `annuity_income` 不只是 fact-processing domain，它还要向 reference / customer 层提供稳定 signal。

这些 customer-master-derived signals 至少包括：

- fee-weighted `主拓机构`
- `关键年金计划`、`关联计划数` 与 `关联机构数`
- `其他年金计划` 与 `其他开拓机构`
- `tags=yyMM新建`
- `年金客户类型=新客*`
- 聚合分类结果 `管理资格`
- 其中 [`关键年金计划`](../../concepts/key-annuity-plan.md) 现在已有独立对象页；它回答 fee-weighted 主导计划，而不是“所有关联计划”的列表
- [`关联计划数`](../../concepts/related-plan-count.md) 现在也有独立对象页；它回答 relationship breadth，而不是“哪一个计划最重要”
- [`关联机构数`](../../concepts/related-branch-count.md) 现在也有独立对象页；它回答机构侧 relationship breadth，而不是主导机构选择
- [管理资格](../../concepts/management-qualification.md) 回答聚合分类结果，而不是原始 `业务类型`

## 下游派生输出

在 current project 的 validation slice 中，当前显式 publication 结果是：

- `company_reference`
- `customer_master_signal`

同时，replay evidence 明确当前 slice：

- `projection_results = []`

也就是说：

- 当前 slice 已显式交付 fact + reference / customer signal
- 但没有把 legacy 后置 projection hook 重新伪装成当前必须运行的默认路径

## 面向操作人员的可见差异（必须外显给运维 / 核查）

- `unknown_names_csv` 属于 operator-facing artifact，不属于 fact table 字段
- unresolved identity 也会生成 failed-record artifact，避免“处理失败但无可见证据”
- 这两类 artifact 都是输出合同的一部分；不能因为 fact 已落表就忽略
- 当前可见差异点：legacy 与 current 在 artifact 触发谓词上不完全同形（`IN*` 结果标记 vs `temp_id_fallback` 解析方法），兼容口径以 evidence page 追踪，不在本页强行统一
- shared family 与 remaining parity gap 统一见 [unresolved-name and failed-record 证据](../../evidence/unresolved-name-and-failed-record-evidence.md)

## 正确性判断边界

判断 `annuity_income` 输出是否正确时，至少要同时满足：

- direct fact output 可复现收入事实
- identity 结果不恢复已退役的 ID5 fallback
- unresolved identity 会进入显式 artifact / signal 路径，而不是静默丢弃
- reference / customer signal 可解释地承接 branch mapping 与 temp-id fallback 结果

## 输出合同 gate

- gate-1：`fact_annuity_income` 与 replay direct fact evidence 一致
- gate-2：`company_reference`、`customer_master_signal` 可由输入锚点与 identity 结果追溯解释
- gate-3：`projection_results` 保持空集合，除非有新证据显式修改合同
- gate-4：unresolved identity 必须产出可定位 artifact，而不是仅日志提示

## 当前实现证据

- `current_test`
  - `tests/integration/test_annuity_income_operator_artifacts.py`
  - `tests/replay/test_annuity_income_slice.py`
- `current_reference_asset`
  - `reference/historical_replays/annuity_income/`
- `current_runbook`
  - `docs/runbooks/annuity-income-replay.md`

## 相关概念

- [企业身份标识：`company_id`](../../concepts/company-id.md)
- [回填：`backfill`](../../concepts/backfill.md)
- [`tags`](../../concepts/tags.md)
- [主拓机构](../../concepts/primary-branch.md)
- [关联计划数](../../concepts/related-plan-count.md)
- [关联机构数](../../concepts/related-branch-count.md)
- [管理资格](../../concepts/management-qualification.md)
- [年金计划类型：`plan_type`](../../concepts/plan-type.md)

## 相关证据

- [`annuity_income` 字段处理证据](../../evidence/annuity-income-field-processing-evidence.md)
- [customer-master signals 证据](../../evidence/customer-master-signals-evidence.md)
- [classification family 证据](../../evidence/classification-family-evidence.md)
- [unresolved-name and failed-record 证据](../../evidence/unresolved-name-and-failed-record-evidence.md)
- [`annuity_income` operator artifacts 证据](../../evidence/annuity-income-operator-artifacts-evidence.md)
- [`annuity_income` ID5 retirement 证据](../../evidence/annuity-income-id5-retirement-evidence.md)
- [验证资产证据](../../evidence/verification-assets-evidence.md)

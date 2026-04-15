# `annuity_income` 输出合同

> standard_type: `output-correctness`
> related_standard_types: `verification-method`, `input-reality`

## 标准对象

本页定义 `annuity_income` 的输出合同。

它回答：

- 哪些结果属于 direct fact output
- 哪些结果属于 reference / customer signal
- 当前 slice 明确不经过哪些 projection hook

## direct fact output

legacy 侧的稳定 direct fact sink 是：

- `business."收入明细"`

这代表 domain 自身首先要交付的是收入事实，而不是先交付状态投影。

在 current project 中，对应的显式 publication target 是：

- `fact_annuity_income`

## backfill targets

legacy 合同仍明确要求该域能为下列 reference / customer objects 提供输入：

- `mapping."年金计划"`
- `mapping."组合计划"`
- `mapping."产品线"`
- `mapping."组织架构"`
- `customer."客户明细"`

这些对象说明 `annuity_income` 不只是 fact-processing domain，它还要向 reference / customer 层提供稳定 signal。

## derived downstream outputs

在 current project 的 validation slice 中，当前显式 publication 结果是：

- `company_reference`
- `customer_master_signal`

同时，replay evidence 明确当前 slice：

- `projection_results = []`

也就是说：

- 当前 slice 已显式交付 fact + reference / customer signal
- 但没有把 legacy 后置 projection hook 重新伪装成当前必须运行的默认路径

## 正确性判断边界

判断 `annuity_income` 输出是否正确时，至少要同时满足：

- direct fact output 可复现收入事实
- identity 结果不恢复已退役的 ID5 fallback
- unresolved identity 会进入显式 artifact / signal 路径，而不是静默丢弃
- reference / customer signal 可解释地承接 branch mapping 与 temp-id fallback 结果

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
- [年金计划类型：`plan_type`](../../concepts/plan-type.md)

## 相关证据

- [`annuity_income` 字段处理证据](../../evidence/annuity-income-field-processing-evidence.md)
- [`annuity_income` operator artifacts 证据](../../evidence/annuity-income-operator-artifacts-evidence.md)
- [`annuity_income` ID5 retirement 证据](../../evidence/annuity-income-id5-retirement-evidence.md)
- [验证资产证据](../../evidence/verification-assets-evidence.md)

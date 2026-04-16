# `annual_award` 输出合同

> standard_type: `output-correctness`
> related_standard_types: `input-reality`, `verification-method`, `semantic-correctness`

## 标准对象

本页定义 `annual_award` 的输出合同。

它回答：

- 当前 accepted slice 直接发布什么
- 哪些 reference / customer signals 属于本域的显式治理后果
- 哪些下游 projection 由它驱动，但不应反写成“本域原始事实”

## direct fact output

当前 accepted slice 的直接事实发布目标是：

- `fact_annual_award`

这层表达的是中标事件事实本身，而不是状态推论。

## reference / customer signals

replay evidence 表明，`annual_award` 当前还会显式发布：

- `company_reference`
- `customer_master_signal`

这说明本域不只是写一张事实表，它还会把 identity 与客户主数据相关信号推进到可验证输出层。

## enrichment 语义合同（hidden but required）

`plan_code` enrichment 在 current accepted slice 的稳定顺序是：

- 先保留 source `plan_code`
- 若为空：按 `company_id + product_line_code` 从 `customer_plan_history` 候选中选择
- 候选按 `effective_period` 倒序；`plan_type=COLLECTIVE` 优先 `P` 前缀，否则优先 `S` 前缀
- 若仍无候选：fallback 到 domain default（`AN001` / `AN002`）

该顺序属于输出可解释性合同的一部分，不应在无证据情况下重排。

## derived downstream outputs

当前 accepted slice 的 projection 结果是：

- `contract_state`
- `monthly_snapshot`

这些结果依赖：

- `fact_annual_award`
- `annuity_performance` fixture / fact bridge
- `annual_loss` fixture bridge

因此更准确的边界是：

- `annual_award` 直接贡献中标事件事实
- 下游 projection 把该事实接入 contract / snapshot 语义
- 不能把 projection 表误写成 award domain 自身的原始事实输出
- 不能把 replay seed 的 `fixture_annual_loss` / `fact_annuity_performance` 误记为 award domain direct outputs

## 正确性判断边界

判断 `annual_award` 输出是否正确时，至少要同时满足：

- 中标事实被稳定发布到 `fact_annual_award`
- `company_reference` 与 `customer_master_signal` 能解释该事实的身份与客户侧后果
- `contract_state` / `monthly_snapshot` 明确消费已发布事实，而不是只依赖旧 fixture
- compatibility case 若出现，应定位到真实失败 checkpoint，而不是被模糊折叠成单一 row-count 差异

## 输出 merge gates（merge 前最小通过线）

- publication targets 保持 5 个：`fact_annual_award`、`company_reference`、`customer_master_signal`、`contract_state`、`monthly_snapshot`
- projection targets 保持 2 个：`contract_state`、`monthly_snapshot`
- checkpoint 链保持：`source_intake` -> `fact_processing` -> `identity_resolution` -> `reference_derivation` -> `contract_state` -> `monthly_snapshot`
- `compatibility_case=False` 才满足默认 merge gate；若为 true，需先完成 compatibility case 诊断与证据定位

## 当前实现证据

- `current_test`
  - `tests/replay/test_annual_award_slice.py`
  - `tests/integration/test_projection_outputs.py`
- `current_reference_asset`
  - `reference/historical_replays/annual_award/`
- `current_runbook`
  - `docs/runbooks/annual-award-replay.md`

## 相关概念

- [客户状态总览](../../concepts/customer-status.md)
- [企业身份标识：`company_id`](../../concepts/company-id.md)
- [回填：`backfill`](../../concepts/backfill.md)

## 相关证据

- [`annual_award` 字段处理证据](../../evidence/annual-award-field-processing-evidence.md)
- [状态与快照证据](../../evidence/status-and-snapshot-evidence.md)
- [验证资产证据](../../evidence/verification-assets-evidence.md)

## 相关验证方法

- [real-data validation](../verification-method/real-data-validation.md)
- [golden scenarios](../verification-method/golden-scenarios.md)

## 当前证据缺口

- legacy SQL lookup 以 `valid_to='9999-12-31'` 过滤 current contract rows；current Pro enrichment 以 `effective_period` 排序挑选候选，尚无跨实现等价性证明
- output contract 已证实 replay fixture bridge 仍在使用，但尚无证据将其升级为“可移除”或“已退役”的状态结论

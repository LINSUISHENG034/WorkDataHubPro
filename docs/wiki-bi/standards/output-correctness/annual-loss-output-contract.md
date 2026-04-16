# `annual_loss` 输出合同

> standard_type: `output-correctness`
> related_standard_types: `input-reality`, `verification-method`, `semantic-correctness`

## 标准对象

本页定义 `annual_loss` 的输出合同。

它回答：

- 当前 accepted slice 直接发布什么
- 哪些 identity / customer-facing signals 是本域显式产物
- 哪些 projection 是 loss fact 的下游治理结果

## direct fact output

当前 accepted slice 的直接事实发布目标是：

- `fact_annual_loss`

这层表达的是年度流失事件事实本身，而不是状态或 operator artifact 的替代物。

## reference / customer signals

replay evidence 表明，`annual_loss` 当前还会显式发布：

- `company_reference`
- `customer_loss_signal`

这说明本域除了事实，还要把 unresolved / resolved identity 后果与客户侧流失信号写成可验证输出。

## derived downstream outputs

当前 accepted slice 的 projection 结果是：

- `contract_state`
- `monthly_snapshot`

这些结果依赖：

- `fact_annual_loss`
- `annuity_performance` fixture / fact bridge
- `annual_award` fixture bridge

因此更准确的边界是：

- `annual_loss` 直接贡献流失事件事实
- 下游 projection 把该事实接回 contract / snapshot 语义
- 不能把 projection 表或 compatibility package 误写成 loss domain 本身的 direct fact output

## temporal enrichment correctness

对 `annual_loss` 来说，`plan_code` 不是简单字段搬运，而是带时间约束的输出语义：

- 若源行已有 `plan_code`，保持 source value（`preserve_source_plan_code`）
- 若源行为空，优先查 `customer_plan_history` 的 current contract rows（`valid_to=9999-12-31`）
- current rows 内按 `effective_period` 倒序优先，并结合 `plan_type` 偏好前缀（集合 `P` / 单一 `S`）
- 仍未命中时退回 domain default（集合 `AN001` / 单一 `AN002`）

因此输出正确性必须覆盖“保留源值 -> temporal lookup -> default fallback”的顺序稳定性，而不只是检查是否最终有 `plan_code`。

## 正确性判断边界

判断 `annual_loss` 输出是否正确时，至少要同时满足：

- 流失事实被稳定发布到 `fact_annual_loss`
- `company_reference` 与 `customer_loss_signal` 能解释 loss event 的身份与客户侧后果
- temp-id fallback 保持 opaque / governed，不恢复 legacy `TE...` 前缀式临时身份
- `plan_code` enrichment 事件应可追溯到 `fact_processing.plan_code_enrichment`，且 rule_id 在 `preserve_source_plan_code`、`customer_plan_history_lookup`、`domain_default_plan_code` 中三选一
- `contract_state` / `monthly_snapshot` 明确消费已发布 loss facts，而不是只依赖 fixture-only 路径
- compatibility case 若出现，应能准确回指 `fact_processing`、`identity_resolution`、`contract_state` 或 `monthly_snapshot` 等真实失败 checkpoint

## 当前实现证据

- `current_test`
  - `tests/replay/test_annual_loss_slice.py`
  - `tests/integration/test_annual_loss_plan_code_enrichment.py`
  - `tests/integration/test_projection_outputs.py`
- `current_reference_asset`
  - `reference/historical_replays/annual_loss/`
- `current_runbook`
  - `docs/runbooks/annual-loss-replay.md`

## 相关概念

- [企业身份标识：`company_id`](../../concepts/company-id.md)
- [临时身份：`temp_id`](../../concepts/temp-id.md)
- [客户状态总览](../../concepts/customer-status.md)

## 相关证据

- [`annual_loss` 字段处理证据](../../evidence/annual-loss-field-processing-evidence.md)
- [状态与快照证据](../../evidence/status-and-snapshot-evidence.md)
- [验证资产证据](../../evidence/verification-assets-evidence.md)

## 相关验证方法

- [real-data validation](../verification-method/real-data-validation.md)
- [golden scenarios](../verification-method/golden-scenarios.md)

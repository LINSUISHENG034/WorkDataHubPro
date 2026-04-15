# `annual_loss` 字段处理证据

## 结论主题

本页把 `annual_loss` 的关键字段处理拆成两类：

- 工程性质量提升
- 直接改变业务解释的处理

重点不是重演 pipeline，而是说明流失事件如何从双 sheet workbook 进入当前 accepted replay / publication 链。

## 证据记录

| evidence_id | source_type | evidence_strength | coverage_state | supported_pages | last_verified | notes |
|---|---|---|---|---|---|---|
| E-AL-FLD-001 | current_code | strong | explicitly_tracked | `annual-loss`, `annual-loss-input-contract` | 2026-04-15 | `src/work_data_hub_pro/capabilities/source_intake/annual_loss/service.py` 固化双 sheet intake、字段别名适配、空尾行跳过与 `source_intake_adaptation` 写回。 |
| E-AL-FLD-002 | current_test | strong | explicitly_tracked | `annual-loss`, `annual-loss-input-contract`, `annual-loss-output-contract` | 2026-04-15 | `tests/integration/test_annual_loss_processing.py` 明确 `company_name`、`plan_type`、`business_type`、`product_line_code`、`period`、`loss_date` 与 `institution_code` 的 canonical 结果。 |
| E-AL-FLD-003 | current_test | strong | explicitly_tracked | `annual-loss-output-contract`, `company-id`, `identity-governance` | 2026-04-15 | `tests/integration/test_annual_loss_plan_code_enrichment.py` 证明 plan-code enrichment 会过滤非 current rows、忽略 blank/Noneish plan codes，并在 lookup miss 时退回 domain default。 |
| E-AL-FLD-004 | current_test | strong | explicitly_tracked | `annual-loss-output-contract`, `temp-id`, `verification-assets-evidence` | 2026-04-15 | `tests/replay/test_annual_loss_slice.py` 证明 loss slice 会把 temp-id fallback 保持为 opaque `IN...` 形式，不恢复 legacy `TE...` 风格，同时将 failure 定位到真实 checkpoint。 |
| E-AL-FLD-005 | current_runbook | supporting | explicitly_tracked | `annual-loss-input-contract`, `annual-loss-output-contract` | 2026-04-15 | `docs/runbooks/annual-loss-replay.md` 把 replay root、comparison package 与 temp-id salt 前置条件写成 operator-facing 执行入口。 |

## 关键字段处理矩阵

| 字段 / 对象 | 处理后对象 | 类型 | 稳定规则 | 对输出的影响 |
|---|---|---|---|---|
| `客户全称` | canonical `company_name` | 工程性质量提升 | trim + normalize | 影响 identity explainability 与 fact payload 稳定性 |
| `计划类型` | canonical `plan_type` | 工程性质量提升 | 归一为 `集合计划` / `单一计划` | 决定 plan-code prefix 偏好 |
| `业务类型` | canonical `business_type` | 工程性质量提升 | 归一为 `企年受托` / `企年投资` | 为产品线解释提供稳定枚举 |
| `上报月份` | canonical `period` | 工程性质量提升 | `YYYY年MM月` 归一为 `YYYY-MM` | 锚定 replay / projection period |
| `流失日期` | canonical `loss_date` | 工程性质量提升 | 支持零填充、去时间戳；歧义短日期退回 `None` | 决定 loss event 的日期解释质量 |
| `业务类型` | `product_line_code` | 业务语义处理 | `企年投资 -> PL201`，`企年受托 -> PL202` | 决定 downstream contract / snapshot 语义 |
| `机构` | `institution_code` | 业务语义处理 | 当前 accepted slice 对未知机构退回 `G00` | 保持组织解释可治理 |
| `plan_code` | enriched `plan_code` | 业务语义处理 | 先保留源值；否则按 current customer-plan-history 的 current rows 查找；再退回 `AN001/AN002` | 决定流失事实如何与 contract / snapshot 对齐 |
| unresolved identity | governed temp-id | 业务语义处理 | identity resolution 保持 opaque `IN...` fallback，不恢复 legacy `TE...` | 决定 `company_reference` 与 customer-loss signal 的治理边界 |

## 工程性质量提升

当前可稳定归入工程性质量提升的处理包括：

- 名称规范化
- 计划类型与业务类型枚举归一
- 月份与日期格式清洗
- 空尾行跳过与 header alias 适配

这些动作提升的是数据可消费性，不直接定义流失语义。

## 业务语义处理

当前可稳定归入业务语义处理的处理包括：

- `业务类型 -> product_line_code` 的领域映射
- `机构 -> institution_code` 的当前治理默认
- 基于 current contract rows 的 plan-code enrichment
- unresolved identity 的 governed temp-id fallback

## 哪些来源是强证

- `annual_loss` intake / processing / plan-code enrichment / replay tests
- current source-intake 与 fact-processing code
- projection output tests

## 哪些来源只是旁证

- replay runbook

## 当前证据缺口

- 当前仍未为 `annual_loss` 单独拆出 implementation-gap audit page；现阶段没有证据要求立即追加
- `institution_code = G00` 当前是 accepted slice 的明确行为，但更细的 organization-resolution 分层仍可在 future audit 中继续收紧

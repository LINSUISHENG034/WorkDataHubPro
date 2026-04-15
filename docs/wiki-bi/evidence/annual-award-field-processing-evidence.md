# `annual_award` 字段处理证据

## 结论主题

本页把 `annual_award` 的关键字段处理拆成两类：

- 工程性质量提升
- 直接改变业务解释的处理

重点不是复述 event pipeline，而是说明中标事件在 current accepted slice 中如何从 multi-sheet workbook 进入可验证事实。

## 证据记录

| evidence_id | source_type | evidence_strength | coverage_state | supported_pages | last_verified | notes |
|---|---|---|---|---|---|---|
| E-AA-FLD-001 | current_code | strong | explicitly_tracked | `annual-award`, `annual-award-input-contract` | 2026-04-15 | `src/work_data_hub_pro/capabilities/source_intake/annual_award/service.py` 固化双 sheet intake、header alias 适配、merged anchor sequence 与 `source_intake_adaptation` 写回。 |
| E-AA-FLD-002 | current_test | strong | explicitly_tracked | `annual-award`, `annual-award-input-contract`, `annual-award-output-contract` | 2026-04-15 | `tests/integration/test_annual_award_intake.py`、`tests/integration/test_annual_award_processing.py` 明确 `company_name`、`plan_type`、`product_line_code`、`award_amount` 与 `business_type` 的 canonical 结果。 |
| E-AA-FLD-003 | current_test | strong | explicitly_tracked | `annual-award-output-contract`, `company-id` | 2026-04-15 | `tests/integration/test_annual_award_plan_code_enrichment.py` 证明 plan-code enrichment 先看 customer-plan-history，再退回 domain default，而不是把空计划号直接当作失败。 |
| E-AA-FLD-004 | current_test | strong | explicitly_tracked | `annual-award-output-contract`, `verification-assets-evidence`, `status-and-snapshot-evidence` | 2026-04-15 | `tests/replay/test_annual_award_slice.py` 与 `tests/integration/test_projection_outputs.py` 证明 `fact_annual_award -> company_reference/customer_master_signal -> contract_state/monthly_snapshot` 的完整链路。 |
| E-AA-FLD-005 | current_runbook | supporting | explicitly_tracked | `annual-award-input-contract`, `annual-award-output-contract` | 2026-04-15 | `docs/runbooks/annual-award-replay.md` 把 accepted replay root、comparison package 与 gate 结果写成 operator-facing 执行入口。 |

## 关键字段处理矩阵

| 字段 / 对象 | 处理后对象 | 类型 | 稳定规则 | 对输出的影响 |
|---|---|---|---|---|
| `company_name` | canonical `company_name` | 工程性质量提升 | trim + uppercase normalize | 影响 identity explainability 与 fact payload 稳定性 |
| `plan_type` | canonical `plan_type` | 工程性质量提升 | `collective/single` 归一为大写枚举 | 决定后续 plan-code prefix 偏好 |
| `product_line_code` | canonical `product_line_code` | 工程性质量提升 | 标准化大小写与分隔表达 | 影响 history lookup 与下游客户信号 |
| `award_amount` | canonical `award_amount` | 工程性质量提升 | 字符串金额转为数值 | 决定中标事实载荷 |
| `source_sheet` | `business_type` | 业务语义处理 | `TrusteeAwards -> trustee_award`，否则 `investee_award` | 将 sheet 差异转成事件语义差异 |
| `plan_code` | enriched `plan_code` | 业务语义处理 | 先保留源值；否则按 `company_id + product_line_code + plan_type` 查 customer history；再退回 `AN001/AN002` | 决定事实如何与 contract / snapshot 对齐 |
| merged anchor rows | stable `anchor_row_no` | 业务语义处理 | 双 sheet 合并后统一编号 | 保证 trace、lineage 与 compatibility case 可定位 |
| `source_company_id` | identity clue | 业务语义处理 | 可作为 source-value-first 线索保留，不要求源行必须已解析成最终身份 | 影响 `company_reference` 与后续 identity 解释 |

## 工程性质量提升

当前可稳定归入工程性质量提升的处理包括：

- 名称规范化
- 枚举值标准化
- 数值字段清洗
- header alias 适配

这些动作提高的是数据可消费性，而不是单独创造新的业务结论。

## 业务语义处理

当前可稳定归入业务语义处理的处理包括：

- 由 `source_sheet` 派生 `business_type`
- 按 current customer-plan-history 进行 plan-code enrichment
- 保留 source-company 线索，而不是强制要求每行自带最终身份
- 使用 merged anchor rows 维持跨 checkpoint 的可追踪事件语义

## 哪些来源是强证

- `annual_award` intake / processing / plan-code enrichment / replay tests
- current source-intake 与 fact-processing code
- projection output tests

## 哪些来源只是旁证

- replay runbook

## 当前证据缺口

- 当前仍未为 `annual_award` 单独拆出 implementation-gap audit page；现阶段没有证据要求立即追加
- 输入合同当前固化的是 accepted slice 的 workbook / sheet contract，而不是仓库外部完整扫描约束

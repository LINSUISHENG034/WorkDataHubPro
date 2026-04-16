# `annual_award` 字段处理证据

## 结论主题

本页把 `annual_award` 的关键字段处理拆成两类：

- 工程性质量提升
- 直接改变业务解释的处理

重点不是复述 event pipeline，而是说明中标事件在 current accepted slice 中如何从 multi-sheet workbook 进入可验证事实。

## legacy 原始来源（证据优先级前置）

本轮语义加深优先吸收下列 legacy 来源，再与 current code/tests 对照：

- `E:\Projects\WorkDataHub\docs\domains\annual_award.md`
- `E:\Projects\WorkDataHub\docs\domains\annual_award-capability-map.md`
- `E:\Projects\WorkDataHub\docs\runbooks\annual_award.md`
- `E:\Projects\WorkDataHub\config\data_sources.yml` / `foreign_keys.yml` / `customer_status_rules.yml`
- `E:\Projects\WorkDataHub\src\work_data_hub\domain\annual_award\pipeline_builder.py` / `schemas.py` / `helpers.py`

它们用于稳定 lineage 语义，不直接覆盖 current accepted contract。

## 证据记录

| evidence_id | source_type | evidence_strength | coverage_state | supported_pages | last_verified | notes |
|---|---|---|---|---|---|---|
| E-AA-FLD-001 | current_code | strong | explicitly_tracked | `annual-award`, `annual-award-input-contract` | 2026-04-15 | `src/work_data_hub_pro/capabilities/source_intake/annual_award/service.py` 固化双 sheet intake、header alias 适配、merged anchor sequence 与 `source_intake_adaptation` 写回。 |
| E-AA-FLD-002 | current_test | strong | explicitly_tracked | `annual-award`, `annual-award-input-contract`, `annual-award-output-contract` | 2026-04-15 | `tests/integration/test_annual_award_intake.py`、`tests/integration/test_annual_award_processing.py` 明确 `company_name`、`plan_type`、`product_line_code`、`award_amount` 与 `business_type` 的 canonical 结果。 |
| E-AA-FLD-003 | current_test | strong | explicitly_tracked | `annual-award-output-contract`, `company-id` | 2026-04-15 | `tests/integration/test_annual_award_plan_code_enrichment.py` 证明 plan-code enrichment 先看 customer-plan-history，再退回 domain default，而不是把空计划号直接当作失败。 |
| E-AA-FLD-004 | current_test | strong | explicitly_tracked | `annual-award-output-contract`, `verification-assets-evidence`, `status-and-snapshot-evidence` | 2026-04-15 | `tests/replay/test_annual_award_slice.py` 与 `tests/integration/test_projection_outputs.py` 证明 `fact_annual_award -> company_reference/customer_master_signal -> contract_state/monthly_snapshot` 的完整链路。 |
| E-AA-FLD-005 | current_runbook | supporting | explicitly_tracked | `annual-award-input-contract`, `annual-award-output-contract` | 2026-04-15 | `docs/runbooks/annual-award-replay.md` 把 accepted replay root、comparison package 与 gate 结果写成 operator-facing 执行入口。 |
| E-AA-FLD-006 | legacy_doc | supporting | explicitly_tracked | `annual-award-input-contract`, `annual-award-output-contract` | 2026-04-16 | legacy `docs/domains/annual_award*.md` + `docs/runbooks/annual_award.md` + `config/data_sources.yml` 记录双 sheet lineage（中文 sheet 名称、file patterns、refresh key、requires_backfill），用于 current contract 的语义背景。 |
| E-AA-FLD-007 | current_code | strong | explicitly_tracked | `annual-award-input-contract`, `annual-award-output-contract` | 2026-04-16 | `apps/orchestration/replay/annual_award_slice.py` 固化 source-intake contract 的 required fields / allowed adaptations，以及 6-checkpoint gate 顺序与 compatibility case 定位。 |
| E-AA-FLD-008 | current_test | strong | explicitly_tracked | `annual-award-output-contract`, `verification-assets-evidence` | 2026-04-16 | `tests/replay/test_annual_award_slice.py` 明确 publication=5、projection=2、checkpoint 顺序稳定，并验证 failure case 回指真实失败 checkpoint 而非固定折叠到 snapshot。 |

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
| `source_intake_adaptation` | adaptation contract payload | 业务语义处理 | 仅允许 `aliases_applied` / `derived_fields` / `ignored_columns` / `missing_non_golden_columns` / `source_headers` | 约束 intake 证据边界，避免把非合同输入 silently 升级 |
| `customer_plan_history.effective_period` | lookup ordering key | 业务语义处理 | 候选按 period 倒序后再应用 `P/S` 前缀偏好 | 决定空 plan-code 的 enrichment 结果与可解释性 |

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
- legacy capability-map / runbook / config（用于 lineage 背景，不单独构成 current 强证）

## 禁止 page drift 的护栏

- 不把 legacy 目录扫描 pattern、中文 sheet 名称直接写成 current runtime 必然接受事实，除非有 current tests/replay 证据
- 不把 replay seed fixture（如 `fixture_annual_loss`）写成 `annual_award` direct output
- 不把跨模块依赖结论扩写到其他 module 页面；未闭合项只在本页“当前证据缺口”记录

## 合并 gate 证据摘要

- gate 通过时应满足：`publication_results=5`、`projection_results=2`、`compatibility_case=False`
- gate 失败时应能在 `fact_processing` / `identity_resolution` / `contract_state` / `monthly_snapshot` 中定位 primary failure checkpoint
- `source_intake` checkpoint 属于 contract-type（warn severity），用于约束适配键与 required fields，不是 self-compare payload

## 当前证据缺口

- 当前仍未为 `annual_award` 单独拆出 implementation-gap audit page；现阶段没有证据要求立即追加
- 输入合同当前固化的是 accepted slice 的 workbook / sheet contract，而不是仓库外部完整扫描约束
- legacy `valid_to='9999-12-31'` current-row 过滤语义与 Pro `effective_period` 倒序语义尚未完成等价性证明
- legacy 中文 sheet 名称是否在 current Pro runtime 被直接接受，尚无 current tests/replay 强证

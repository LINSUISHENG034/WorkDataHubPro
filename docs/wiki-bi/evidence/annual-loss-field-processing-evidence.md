# `annual_loss` 字段处理证据

## 结论主题

本页把 `annual_loss` 的关键字段处理拆成两类：

- 工程性质量提升
- 直接改变业务解释的处理

重点不是重演 pipeline，而是说明流失事件如何从双 sheet workbook 进入当前 accepted replay / publication 链。

## 证据记录

| evidence_id | source_type | evidence_strength | coverage_state | supported_pages | last_verified | notes |
|---|---|---|---|---|---|---|
| E-AL-FLD-001 | legacy_doc | strong | absorbed | `annual-loss`, `annual-loss-input-contract`, `annual-loss-output-contract` | 2026-04-16 | `E:\Projects\WorkDataHub\docs\domains\annual_loss.md` 与 `E:\Projects\WorkDataHub\docs\domains\annual_loss-capability-map.md` 固化双 sheet contract、`sheet_name/sheet_names` 边界与 plan-code enrichment 的时间语义来源。 |
| E-AL-FLD-002 | legacy_runbook | supporting | absorbed | `annual-loss-input-contract` | 2026-04-16 | `E:\Projects\WorkDataHub\docs\runbooks\annual_loss.md` 明确 annual_loss 运行前提是 workbook 同时包含 trustee/investee 两个流失 sheet。 |
| E-AL-FLD-003 | legacy_config | strong | absorbed | `annual-loss-input-contract`, `annual-loss-output-contract` | 2026-04-16 | `E:\Projects\WorkDataHub\config\data_sources.yml` 固化 `annual_loss` 的 file patterns + 双 sheet 入口；`config/customer_status_rules.yml` 明确 `is_loss_reported` 由 annual_loss source 的 `exists_in_year` 驱动。 |
| E-AL-FLD-004 | current_code | strong | explicitly_tracked | `annual-loss`, `annual-loss-input-contract` | 2026-04-16 | `src/work_data_hub_pro/capabilities/source_intake/annual_loss/service.py` 固化双 sheet intake、字段别名适配、merged anchor sequence、空尾行跳过与 `source_intake_adaptation` 写回。 |
| E-AL-FLD-005 | current_test | strong | explicitly_tracked | `annual-loss`, `annual-loss-input-contract`, `annual-loss-output-contract` | 2026-04-16 | `tests/integration/test_annual_loss_intake.py`、`tests/integration/test_annual_loss_processing.py` 明确 multi-sheet 合并、anchor 稳定序列、`period/loss_date/business_type/product_line_code/institution_code` canonical 结果。 |
| E-AL-FLD-006 | current_test | strong | explicitly_tracked | `annual-loss-output-contract`, `company-id`, `identity-governance` | 2026-04-16 | `tests/integration/test_annual_loss_plan_code_enrichment.py` 证明 plan-code enrichment 仅使用 current rows（`valid_to=9999-12-31`）、按 `effective_period` 与 plan-type 前缀偏好择优，并在 lookup miss 时退回 domain default。 |
| E-AL-FLD-007 | current_reference_asset | strong | explicitly_tracked | `annual-loss-output-contract`, `verification-assets-evidence` | 2026-04-16 | `reference/historical_replays/annual_loss/customer_plan_history_2026_03.json` 与 `legacy_fact_processing_2026_03.json` 给出 current/non-current 合约行并存与双 sheet 事实落盘样例，是 temporal lookup 回放基线。 |
| E-AL-FLD-008 | current_test | strong | explicitly_tracked | `annual-loss-output-contract`, `temp-id`, `verification-assets-evidence` | 2026-04-16 | `tests/replay/test_annual_loss_slice.py` 证明 loss slice 会把 temp-id fallback 保持为 opaque `IN...` 形式，不恢复 legacy `TE...` 风格，同时将 failure 定位到真实 checkpoint。 |
| E-AL-FLD-009 | current_runbook | supporting | explicitly_tracked | `annual-loss-input-contract`, `annual-loss-output-contract` | 2026-04-16 | `docs/runbooks/annual-loss-replay.md` 把 replay root、comparison package、`customer_plan_history` 夹具和 temp-id salt 前置条件写成 operator-facing 执行入口。 |

## 关键字段处理矩阵

| 字段 / 对象 | 处理后对象 | 类型 | 稳定规则 | 对输出的影响 |
|---|---|---|---|---|
| `客户全称` | canonical `company_name` | 工程性质量提升 | trim + normalize | 影响 identity explainability 与 fact payload 稳定性 |
| `计划类型` | canonical `plan_type` | 工程性质量提升 | 归一为 `集合计划` / `单一计划` | 决定 plan-code prefix 偏好 |
| `业务类型` | canonical `business_type` | 工程性质量提升 | 归一为 `企年受托` / `企年投资` | 为产品线解释提供稳定枚举 |
| `上报月份` | canonical `period` | 工程性质量提升 | `YYYY年MM月` 归一为 `YYYY-MM` | 锚定 replay / projection period |
| `流失日期` | canonical `loss_date` | 工程性质量提升 | 支持零填充、去时间戳；歧义短日期退回 `None` | 决定 loss event 的日期解释质量 |
| `source_sheet` | lineage/source clue | 工程性质量提升 | intake 保留每条记录来源 sheet 与 source_row_no，不在中途丢失 | 支撑 multi-sheet explainability 与 compatibility case 定位 |
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
- 基于 current contract rows（`valid_to=9999-12-31`）与 `effective_period` 顺序的 plan-code temporal enrichment
- unresolved identity 的 governed temp-id fallback

## 哪些来源是强证

- `annual_loss` intake / processing / plan-code enrichment / replay tests
- legacy annual_loss domain contract / capability map / runbook / config
- current source-intake 与 fact-processing code
- replay historical assets（包含 customer-plan-history 与 fact-processing baselines）
- projection output tests

## 哪些来源只是旁证

- replay runbook

## 当前证据缺口

- 当前仍未为 `annual_loss` 单独拆出 implementation-gap audit page；现阶段没有证据要求立即追加
- `institution_code = G00` 当前是 accepted slice 的明确行为，但更细的 organization-resolution 分层仍可在 future audit 中继续收紧
- legacy capability map 明确 annual_loss 对 `customer."客户明细"` backfill tags / customer type 有贡献；该语义横跨 reference/backfill 模块，当前仅记录为证据缺口，不在本模块页面内扩写其他域合同
- current replay 资产中的 `legacy_source_intake_2026_03.json` 为空列表，暂不支持以 repo-native row payload 回放 legacy intake 细节；后续若补齐该资产，可把 multi-sheet 原始行级对齐从 supporting 提升到 strong

## 当前实现证据

- `current_test`
  - `tests/integration/test_annual_loss_intake.py`
  - `tests/integration/test_annual_loss_processing.py`
  - `tests/integration/test_annual_loss_plan_code_enrichment.py`
  - `tests/replay/test_annual_loss_slice.py`
- `current_reference_asset`
  - `reference/historical_replays/annual_loss/`
- `current_runbook`
  - `docs/runbooks/annual-loss-replay.md`

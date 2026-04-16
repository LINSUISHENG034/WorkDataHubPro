# `annual_loss` 输入合同

> standard_type: `input-reality`
> related_standard_types: `verification-method`, `output-correctness`

## 标准对象

本页定义 `annual_loss` 的输入合同。

它回答的是：

- loss event 的双 sheet workbook 在当前 accepted slice 中如何被稳定识别
- 哪些字段属于最小输入骨架
- 哪些缺失属于可降级处理，哪些会直接破坏输入合同

## 输入介质与发现规则

- 文件格式
  - Excel workbook（`.xlsx`）
- 当前 accepted slice 入口
  - 单个 workbook，内部同时包含流失事件的双 sheet
- config release
  - `2026-04-12-annual-loss-baseline`
- 当前 runbook 示例
  - `data/annual_loss_2026_03.xlsx`

本页当前优先固化的是 accepted slice 已显式验证的 workbook + sheet contract。

## Sheet 合同

- 必需 sheet
  - `企年受托流失(解约)`
  - `企年投资流失(解约)`
- 输入形态
  - multi-sheet event domain
- intake 结果
  - 双 sheet 合并进入同一个 `annual_loss:{period}` batch
  - merged `anchor_row_no` 在双 sheet 间连续递增，不按 sheet 重置
  - trailing empty rows 会被跳过，不应污染 anchor row 序列

## observed production reality

- representative single-month production-sample validation shows the business-collection ledger workbook currently contains the accepted event-domain sheets
- the same business-collection folder also contains adjacent summary and attachment-style workbooks
- those adjacent workbooks should not be silently rewritten into the accepted event-domain contract without stronger source support
- accepted contract 仍然是本页定义的 event-domain sheet subset，而不是把整个 ledger workbook 或 summary workbook 自动提升为 accepted contract

## 最小字段骨架

当前 current intake / processing / replay evidence 能稳定支撑的最小输入骨架是：

- `上报月份`
- `业务类型`
- `客户全称`
- 至少一个计划锚点：`年金计划号` 或 `计划类型`

当前更适合视为高价值补强字段，但不宜直接上升为绝对 intake gate 的还有：

- `流失日期`
- `company_id`
- `机构`
- `受托人`

这些字段会影响 explainability、日期语义或 operator-facing 解释，但 current accepted slice 允许它们以降级方式进入后续处理。

## temporal lookup 输入前提（非 intake gate）

`annual_loss` 的 plan-code temporal lookup 发生在 fact-processing 阶段，不属于 intake gate 本身；但当前输入合同需要保留它的最小前提线索：

- 计划锚点至少一项：`年金计划号` 或 `计划类型`
- 身份线索可空但应可承载：`company_id` / `source_company_id`
- multi-sheet 来源线索：`source_sheet`

这组前提用于支撑后续 `customer_plan_history` 的 current-row lookup（仅当前有效行）与 domain default 回退，不应被误写成 intake 必须先完成 enrichment。

## 字段别名与适配边界

当前 accepted slice 已显式支持下列归一：

- `上报月份` / `period` -> `period`
- `业务类型` / `business_type` -> `business_type`
- `客户全称` / `上报客户名称` / `company_name` -> `company_name`
- `计划类型` / `plan_type` -> `plan_type`
- `年金计划号` / `plan_code` -> `plan_code`
- `流失日期` / `loss_date` -> `loss_date`
- `company_id` / `source_company_id` -> `source_company_id`

同时，raw 行上像 `区域`、`年金中心`、`上报人`、`考核标签` 这类列会被保留在适配记录中，但不自动提升为 canonical loss fact 字段。

## 运行时容忍边界

当前 evidence 表明：

- `plan_code` 可以为空，后续允许走 current contract lookup 或 domain defaulting
- `company_id` 可以为空，identity 解析可继续进行
- `流失日期` 可以为空，也可能在歧义格式下被规范化为 `None`
- `机构` 缺失或未知时，当前 processing 会退回到默认 `institution_code`
- `company_id` / `source_company_id` 为空时，不阻断 intake，但会影响后续 temporal lookup 命中率

因此更准确的理解是：

- 输入合同优先保护 loss event 被稳定读入
- 解释力不足的字段会影响下游治理质量，但不等于必须在 intake 阶段丢弃整行

## 无效源条件

下面几类情况应视为输入合同被破坏：

- workbook 缺失 `企年受托流失(解约)` 或 `企年投资流失(解约)`
- 缺失 `上报月份` 或 `客户全称`
- 缺失 `业务类型`，使产品线解释锚点消失
- 同时缺失 `年金计划号` 与 `计划类型`
- 把 synthetic fixture 冒充为 accepted replay / workbook 现实

## 当前实现证据

- `current_test`
  - `tests/integration/test_annual_loss_intake.py`
  - `tests/integration/test_annual_loss_plan_code_enrichment.py`
  - `tests/replay/test_annual_loss_slice.py`
- `current_reference_asset`
  - `reference/historical_replays/annual_loss/`
- `current_runbook`
  - `docs/runbooks/annual-loss-replay.md`

## 相关概念

- [企业身份标识：`company_id`](../../concepts/company-id.md)
- [临时身份：`temp_id`](../../concepts/temp-id.md)
- [年金计划类型：`plan_type`](../../concepts/plan-type.md)

## 相关证据

- [输入现实证据](../../evidence/input-reality-evidence.md)
- [business collection workbook variants 证据](../../evidence/business-collection-workbook-variants-evidence.md)
- [`annual_loss` 字段处理证据](../../evidence/annual-loss-field-processing-evidence.md)
- [身份与补查证据](../../evidence/identity-and-lookup-evidence.md)

## 相关验证方法

- [real-data validation](../verification-method/real-data-validation.md)
- [golden scenarios](../verification-method/golden-scenarios.md)

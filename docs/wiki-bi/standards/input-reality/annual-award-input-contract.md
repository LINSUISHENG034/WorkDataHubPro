# `annual_award` 输入合同

> standard_type: `input-reality`
> related_standard_types: `verification-method`, `output-correctness`

## 标准对象

本页定义 `annual_award` 的输入合同。

它回答的是：

- 什么样的 workbook / sheet 组合才算有效输入
- multi-sheet event intake 在当前 accepted slice 中如何被稳定识别
- 哪些字段缺失会破坏输入合同，哪些属于可降级处理

## 输入介质与发现规则

- 文件格式
  - Excel workbook（`.xlsx`）
- 当前 accepted slice 入口
  - 单个 workbook，内部同时包含中标事件的双 sheet
- config release
  - `2026-04-11-annual-award-baseline`
- 当前 runbook 示例
  - `data/annual_award_2026_03.xlsx`

本页当前优先固化的是 workbook + sheet contract，而不是仓库外部目录扫描策略。

## Sheet 合同

- 必需 sheet
  - `TrusteeAwards`
  - `InvesteeAwards`
- 输入形态
  - multi-sheet event domain
- intake 结果
  - 两个 sheet 的记录会被并入同一个 `annual_award:{period}` batch
  - anchor row 序列按合并后的稳定顺序编号，而不是各 sheet 各自重起

## observed production reality

- representative single-month production-sample validation shows the business-collection ledger workbook currently contains the accepted event-domain sheets
- the same business-collection folder also contains adjacent summary and attachment-style workbooks
- those adjacent workbooks should not be silently rewritten into the accepted event-domain contract without stronger source support
- accepted contract 仍然是本页定义的 event-domain sheet subset，而不是把整个 ledger workbook 或 summary workbook 自动提升为 accepted contract

## 最小字段骨架

当前 current intake / processing / replay evidence 能稳定支撑的最小输入骨架是：

- `period`
- `company_name`
- `award_amount`
- 至少一个计划锚点：`plan_code` 或 `plan_type`

当前仍可作为高价值线索但不宜直接写成绝对硬门槛的还有：

- `source_company_id`
- `product_line_code`

它们会显著影响后续 identity explainability 与 plan-code enrichment，但 current intake 合同并未把它们写成一票否决。

## 字段别名与适配边界

当前 accepted slice 已显式支持中英文别名归一：

- `上报月份` / `period` -> `period`
- `客户全称` / `上报客户名称` / `company_name` -> `company_name`
- `company_id` / `source_company_id` -> `source_company_id`
- `年金计划号` / `plan_code` -> `plan_code`
- `计划类型` / `plan_type` -> `plan_type`
- `产品线代码` / `product_line_code` -> `product_line_code`
- `奖励金额` / `award_amount` -> `award_amount`

因此输入合同允许 header level 的别名适配，但不允许缺失业务上不可替代的核心含义。

## 运行时容忍边界

当前 evidence 表明：

- `plan_code` 可以为空，后续允许走 customer-plan-history lookup 或 domain defaulting
- `source_company_id` 可以为空，identity 解析不会因此立刻把整条记录判为无效
- `product_line_code` 为空会削弱后续 enrichment 的解释力，但不是 intake gate 本身

更准确的理解是：

- 输入合同先保护“事件可被读入并保留”
- 后续再由 identity / plan-code / projection 规则决定它能否达到 contract-grade explainability

## 无效源条件

下面几类情况应视为输入合同被破坏：

- workbook 缺失 `TrusteeAwards` 或 `InvesteeAwards`
- 缺失 `period` 或 `company_name`
- 同时缺失 `plan_code` 与 `plan_type`，使计划锚点消失
- 缺失 `award_amount`，使记录不再表达中标事实
- 把 synthetic fixture 冒充为 real replay / accepted workbook 现实

## 当前实现证据

- `current_test`
  - `tests/integration/test_annual_award_intake.py`
  - `tests/replay/test_annual_award_slice.py`
- `current_reference_asset`
  - `reference/historical_replays/annual_award/`
- `current_runbook`
  - `docs/runbooks/annual-award-replay.md`

## 相关概念

- [企业身份标识：`company_id`](../../concepts/company-id.md)
- [年金计划类型：`plan_type`](../../concepts/plan-type.md)

## 相关证据

- [输入现实证据](../../evidence/input-reality-evidence.md)
- [business collection workbook variants 证据](../../evidence/business-collection-workbook-variants-evidence.md)
- [`annual_award` 字段处理证据](../../evidence/annual-award-field-processing-evidence.md)
- [身份与补查证据](../../evidence/identity-and-lookup-evidence.md)

## 相关验证方法

- [real-data validation](../verification-method/real-data-validation.md)
- [golden scenarios](../verification-method/golden-scenarios.md)

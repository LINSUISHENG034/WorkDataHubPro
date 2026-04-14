# `annuity_performance` 输入合同

> standard_type: `input-reality`
> related_standard_types: `verification-method`, `output-correctness`

## 标准对象

本页定义 `annuity_performance` 的输入合同。

它回答的不是“旧代码怎么读文件”，而是：

- 什么样的源文件才算这个 domain 的有效输入
- workbook / sheet 现实长什么样
- 哪些字段缺失时应判为无效源

## 输入介质与发现规则

- 文件格式
  - Excel workbook（`.xlsx`）
- 基础目录
  - `data/real_data/{YYYYMM}/收集数据/数据采集`
- 文件名关键字
  - `*年金规模收入*.xlsx`
  - `*规模*收入数据*.xlsx`
- 排除模式
  - `*回复*`
- 版本策略
  - `highest_number`

## Sheet 合同

- 主 sheet
  - `规模明细`
- 输入形态
  - single-sheet domain
- 非例
  - 不应把 event domain 的 multi-sheet 经验套到 `annuity_performance`
  - 也不应因为测试夹具常常很小，就假定真实 workbook 没有额外列

## 最小字段骨架

这里的“最小字段骨架”当前按 `wiki-bi` 的 golden-set / durable Q&A 视角表达，
不是直接照抄 legacy Bronze schema。

当前可明确写实的最小输入骨架是：

- `月度`
- `计划代码`
- `客户名称`
- `期末资产规模`

这些字段缺失时，不应继续把该 workbook 当成有效 annuity-performance 输入。

## 运行时容忍边界

当前代码核对表明：

- `客户名称` 缺失并不必然让整份源数据失效
- 在 `计划代码` 可用时，部分记录仍可能通过 plan-code 路径继续完成 identity 解析

因此更准确的理解是：

- `客户名称` 缺失
  - 对 golden-set / explainability 视角来说属于重要缺口
  - 对 runtime 代码路径来说更接近“降级输入”，而不是绝对无效源

## 常见输入字段

除最小骨架外，legacy 材料还明确出现或反复依赖下列字段：

- `业务类型`
- `机构`
- `计划号`
- `机构名称`
- `组合代码`
- `计划类型`
- `集团企业客户号`
- `期初资产规模`
- `投资收益`
- `当期收益率`
- `流失(含待遇支付)`

它们不全都属于“缺失即无效”的骨架字段，但其中很多直接影响后续 canonical fact、backfill 或 snapshot 解释。

## 无效源条件

下面几类情况应视为输入合同被破坏：

- 找不到匹配 workbook
- 匹配到多个 workbook 且未做版本裁决
- workbook 中缺失 `规模明细` sheet
- 缺失 `月度`、`计划代码`、`期末资产规模` 这类关键列
- 把 synthetic fixture 冒充为 real-data sample

补充说明：

- `客户名称` 缺失应优先视为“解释力下降 / identity 线索减弱”
- 只有当 runtime 也无法通过其他线索继续处理时，才应进一步升级为无效输入判断

## 相关概念

- [年金计划类型：`plan_type`](../../concepts/plan-type.md)
- [企业身份标识：`company_id`](../../concepts/company-id.md)

## 相关证据

- [输入现实证据](../../evidence/input-reality-evidence.md)
- [annuity_performance 字段处理证据](../../evidence/annuity-performance-field-processing-evidence.md)

## 相关验证方法

- [real-data validation](../verification-method/real-data-validation.md)
- [golden scenarios](../verification-method/golden-scenarios.md)

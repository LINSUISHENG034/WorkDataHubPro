# 输入现实合同

> standard_type: `input-reality`
> related_standard_types: `verification-method`

## 标准对象

本页定义 `wiki-bi` 对真实输入现实的基本理解方式。

## 适用范围

- source workbook
- sheet 结构
- 目录与版本命名
- synthetic fixture 与 real-data sample 的边界

## 正确性定义

如果某项知识要被视为“输入现实”，至少应满足：

- 能回指到真实样本、稳定配置或明确的输入合同
- 不是从实现细节反推出来的猜测
- 不把 synthetic fixture 误写成真实世界形态

## 关键约束

- real-data sample 与 synthetic fixture 必须严格区分
- 多 sheet 事件域的输入现实不能被简化成单 sheet 假设
- 目录、版本、命名策略属于输入现实的一部分，而不是无关噪音
- `sheet_name` 与 `sheet_names` 这种配置差异本身就是输入合同
- accepted contract 与 observed production variant 是不同 evidence layer
- observed workbook variants can strengthen input reality understanding without automatically becoming accepted source contracts

## 输入现实检查表

判断某项输入现实是否被正确吸收时，至少检查：

1. 它是否来自真实样本、稳定配置或验证指引
2. 它是单 sheet 还是 multi-sheet 现实
3. 它是否依赖版本目录、命名模式或 fallback 规则
4. 它是否被错误地简化成当前测试夹具形状

## 当前关键输入现实

- [`annuity_performance`](../../domains/annuity-performance.md) 与 [`annuity_income`](../../domains/annuity-income.md)
  - 共用 `data/real_data/{YYYYMM}/收集数据/数据采集`
  - 共用 `highest_number` 版本策略
  - 但使用不同 sheet
  - 当前还可由 [annuity workbook family 证据](../../evidence/annuity-workbook-family-evidence.md) 回答代表性生产样本中的物理 workbook 实际同时包含哪些 sheet
- [`annual_award`](../../domains/annual-award.md) 与 [`annual_loss`](../../domains/annual-loss.md)
  - 使用 `data/real_data/{YYYYMM}/收集数据/业务收集`
  - 是 multi-sheet 事件域
  - 不能被简化为单 sheet 输入假设
  - 当前已分别补成 [`annual_award` 输入合同](./annual-award-input-contract.md) 与 [`annual_loss` 输入合同](./annual-loss-input-contract.md)
  - 当前还可由 [business collection workbook variants 证据](../../evidence/business-collection-workbook-variants-evidence.md) 与 [business collection ledger workbook](../../surfaces/business-collection-ledger-workbook.md) 回答相邻 workbook / sheet 的 observed production reality
- real-data validation
  - 依赖真实样本与真实结构，而不等于“把 synthetic workbook 换个名字”

## 非例

- “当前测试用 workbook 长这样，所以真实输入也应如此”
- “某个 adapter 只支持一种 sheet 结构，所以现实世界只有这一种结构”
- “当前 project 尚未实现某个 domain，所以它的输入现实可以暂时不写”

## 相关概念

- [年金计划类型：`plan_type`](../../concepts/plan-type.md)
- [企业身份标识：`company_id`](../../concepts/company-id.md)

## 相关 domains

- [`annual_award`](../../domains/annual-award.md)
- [`annual_loss`](../../domains/annual-loss.md)
- [`annuity_performance`](../../domains/annuity-performance.md)
- [`annuity_income`](../../domains/annuity-income.md)

## 相关证据

- [输入现实证据](../../evidence/input-reality-evidence.md)
- [annuity workbook family 证据](../../evidence/annuity-workbook-family-evidence.md)
- [business collection workbook variants 证据](../../evidence/business-collection-workbook-variants-evidence.md)
- [`annual_award` 输入合同](./annual-award-input-contract.md)
- [`annual_loss` 输入合同](./annual-loss-input-contract.md)
- [`annuity_performance` 输入合同](./annuity-performance-input-contract.md)
- [`annuity_income` 输入合同](./annuity-income-input-contract.md)

## 相关验证方法

- [real-data validation](../verification-method/real-data-validation.md)
- [golden scenarios](../verification-method/golden-scenarios.md)

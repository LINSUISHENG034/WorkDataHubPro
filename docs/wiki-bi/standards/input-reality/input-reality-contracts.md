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

## 非例

- “当前测试用 workbook 长这样，所以真实输入也应如此”
- “某个 adapter 只支持一种 sheet 结构，所以现实世界只有这一种结构”

## 相关概念

- [年金计划类型：`plan_type`](../../concepts/plan-type.md)
- [企业身份标识：`company_id`](../../concepts/company-id.md)

## 相关证据

- [输入现实证据](../../evidence/input-reality-evidence.md)

## 相关验证方法

- [real-data validation](../verification-method/real-data-validation.md)

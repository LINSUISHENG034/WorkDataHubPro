# 输出正确性标准

> standard_type: `output-correctness`
> related_standard_types: `semantic-correctness`, `verification-method`

## 标准对象

本页定义输出在什么情况下才算“正确”。

## 适用范围

- fact 输出
- reference / customer backfill 输出
- contract / snapshot 输出

## 正确性定义

正确输出不只是“文件能生成”或“表里有数据”，而应同时满足：

- 语义正确
- 粒度正确
- 关键关系正确
- 能被相应验证资产和方法证明

## 关键约束

- 回填结果、快照结果与事实结果不能各自为政
- 状态字段不能因为实现方便而改变业务含义
- 输出 compare 应围绕稳定语义与受治理资产，而不是临时运行偶然结果

对状态与快照相关输出，还应额外满足：

- 状态来源与字段语义一致
- 粒度与字段集合一致
- `is_new` 只出现在客户 / 产品线粒度，而不是计划粒度
- `customer_type` 这类标签不被误当作快照状态

## 非例

- 测试全绿就直接等于输出正确
- 只看 row count，不看状态语义和关系约束
- 看到某字段有值，就假设其粒度和业务语义都正确

## 相关概念

- [企业身份标识：`company_id`](../../concepts/company-id.md)
- [快照粒度：`snapshot_granularity`](../../concepts/snapshot-granularity.md)
- [回填：`backfill`](../../concepts/backfill.md)

## 相关证据

- [状态与快照证据](../../evidence/status-and-snapshot-evidence.md)
- [验证资产证据](../../evidence/verification-assets-evidence.md)
- [`annuity_performance` 输出合同](./annuity-performance-output-contract.md)
- [`annuity_performance` 字段处理证据](../../evidence/annuity-performance-field-processing-evidence.md)

## 相关验证方法

- [real-data validation](../verification-method/real-data-validation.md)
- [golden scenarios](../verification-method/golden-scenarios.md)

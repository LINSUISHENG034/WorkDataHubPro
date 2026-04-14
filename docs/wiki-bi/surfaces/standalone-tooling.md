# `standalone tooling`

## Surface 定义

这里指 legacy 中以独立 CLI 或 GUI 形式暴露给 operator 的相邻工具面，而不是事实 domain 主路径本身。

当前已明确识别到的对象至少包括：

- `cleanse`
- `eqc-gui`
- `eqc-gui-fluent`
- `intranet-deploy-gui`

## Surface 类型

- tool surface
- operator surface

## Legacy 职责

- 提供手工数据清洗入口
- 提供 ad hoc EQC 查询与可选 persistence
- 提供部署打包类 GUI 工具

## 为什么它是独立 surface

这些对象并不是普通 helper，因为它们在 unified CLI 中有独立命令入口，且其中一部分有自己的 GUI 应用与 controller。

但它们也不应被自动提升为产品级 business truth，因为：

- 它们主要服务 operator convenience 或 support workflow
- 它们与主 ETL / domain / validation 路径并不等价
- 其中有些工具更接近 support tooling，而不是 rebuild 的核心 runtime surface

## 相关概念

- [企业身份标识：`company_id`](../concepts/company-id.md)

## 相关标准

- [输出正确性标准](../standards/output-correctness/output-correctness.md)

## 关键证据来源

- [operator 与 surface 证据](../evidence/operator-and-surface-evidence.md)

## 当前重构处理状态

- 当前应作为相邻 operator tooling family 显式登记
- 不应因为它们不属于主 ETL path，就从 wiki 中完全消失
- 也不应因为它们有独立 CLI / GUI 入口，就自动假定都要进入 rebuild 核心边界

## 仍未决的问题

- `cleanse` 是否属于 rebuild 需要保留的 operator tool
- EQC GUI 是否应继续承担可选 persistence 角色
- intranet deployment GUI 是否属于 durable product surface，还是独立 support tooling

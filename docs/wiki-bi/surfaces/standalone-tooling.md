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

## operator / runtime / verification 合同

- operator 合同：独立工具的入口、输入前置条件、输出去向必须可查询；否则只能算临时脚本，不应提升为治理 surface。
- runtime 合同：standalone tooling 默认是“邻接运行面”，不自动并入 domain runtime；是否与主线共享持久化要单独裁决。
- verification 合同：工具面验证关注可执行性、输出可核查性与边界不越权，而不是追求 domain contract 全覆盖。

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

## 当前证据缺口

- `cleanse` 的 retain / retire 决策仍未形成对象级 closure
- EQC GUI 家族是否保留可选 persistence 语义仍未闭环
- intranet deployment GUI 是否属于 durable product surface 仍待明确
- 本仓库未携带 legacy `src/work_data_hub/cli/__main__.py` 与 GUI 原始实现；当前对象边界依赖既有 code-audit 证据，原始路径级复核仍待补证

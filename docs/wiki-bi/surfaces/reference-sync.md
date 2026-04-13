# `reference_sync`

## Surface 定义

`reference_sync` 是把 authoritative reference data 同步进业务可消费目标的独立 surface。

## Surface 类型

- runtime surface
- operator surface
- integration surface

## Legacy 职责

- 同步 authoritative reference data
- 管理 reference target 的刷新/更新
- 形成普通 fact domain 之外的独立操作路径

## 为什么它是独立 surface

它不是普通事实处理 domain，也不只是一个 helper。它有自己的入口、目标表、配置与运行语义。

## 相关概念

- [回填：`backfill`](../concepts/backfill.md)

## 相关标准

- [输入现实合同](../standards/input-reality/input-reality-contracts.md)
- [输出正确性标准](../standards/output-correctness/output-correctness.md)

## 关键证据来源

- [operator 与 surface 证据](../evidence/operator-and-surface-evidence.md)

## 当前重构处理状态

- 当前应作为显式治理 surface 保留在 wiki 中
- retain / replace / retire 仍需独立决策

## 仍未决的问题

- 是保留 legacy-like reference sync，还是被新的 bootstrap/publication 模式替代

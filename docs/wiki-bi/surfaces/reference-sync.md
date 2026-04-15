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

## 配置化合同

legacy `reference_sync.yml` 说明这个 surface 不是抽象概念，而是显式配置治理对象：

- 有独立启停、schedule、concurrency 与 batch size
- 明确 target schema / table
- 同时覆盖 `postgres` authoritative source 与 `config_file` source
- 对不同目标使用 `upsert` / `delete_insert` 等不同 sync 语义

## 关键目标表面

legacy 审计明确指出，这个 surface 至少涉及：

- `business.年金计划`
- `business.组合计划`
- `business.组织架构`
- `business.产品线`

这说明它不是抽象的“同步能力”，而是明确写到业务可消费目标上的操作面。

## 为什么它是独立 surface

它不是普通事实处理 domain，也不只是一个 helper。它有自己的入口、目标表、配置与运行语义。

它还意味着：

- reference data 不是只靠 fact domain 自然长出来
- sync / bootstrap / authoritative target 更新需要被单独治理

## 相关 surfaces

- [enterprise enrichment persistence](./enterprise-enrichment-persistence.md)

## 相关概念

- [回填：`backfill`](../concepts/backfill.md)

## 相关标准

- [输入现实合同](../standards/input-reality/input-reality-contracts.md)
- [输出正确性标准](../standards/output-correctness/output-correctness.md)

## 关键证据来源

- [operator 与 surface 证据](../evidence/operator-and-surface-evidence.md)

## 当前重构处理状态

- 当前应作为显式治理 surface 保留在 wiki 中
- 对 current accepted validation slices 而言，legacy `reference_sync` runtime 已被显式 `reference_derivation -> publication` 链取代，而不是继续作为独立日常 sync runtime 存在
- 被保留的是 target inventory、authoritative source-of-truth 映射与 sync contract 这层治理记忆，而不是 legacy daily schedule / sync-state persistence 本身
- current repo 尚未保留 repo-native `reference_sync` runtime、schedule 或 sync-state persistence；这些 production/bootstrap concerns 继续保持 deferred
- 目前至少不能再把它当成“跟随 domain 一起自然覆盖”的隐含对象

## Round 21 决策边界

- `retain`
  - target inventory
  - authoritative source-of-truth mapping
  - `upsert` / `delete_insert` 这类 sync contract 语义
- `replace`
  - accepted slices 中的 hidden sync side effects
  - 以显式 reference derivation 与 publication groups 取代 legacy-like orchestration surface
- `defer`
  - daily schedule
  - sync-state persistence
  - 独立 operator-facing reference bootstrap/runtime plan
- `retire`
  - “reference data 会在 fact domain 主链里自然长出来，不需要单独治理”这一假设

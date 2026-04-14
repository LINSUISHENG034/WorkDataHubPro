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
- retain / replace / retire 仍需独立决策
- 目前至少不能再把它当成“跟随 domain 一起自然覆盖”的隐含对象
- 即使未来不保留 legacy-like sync 机制，也应保留其 target inventory、source-of-truth 映射与 sync contract

## 仍未决的问题

- 是保留 legacy-like reference sync，还是被新的 bootstrap/publication 模式替代
- 如果被替代，最小需要保留哪些 target inventory 与 contract guarantees

# Round 24：reference and backfill pilot

> 状态：Completed
> 日期：2026-04-16
> 主题簇：reference-derivation / backfill / subagent-pilot

## 本轮目标

- 用单一 subagent 验证 reference/backfill 模块的 wiki 吸收任务设计
- 检查 evidence-first 写法和 domain thin-navigation 规则能否稳定保持
- 记录下一次 pilot 要怎样收紧 prompt 和 review gate

## Raw Sources

- `E:\Projects\WorkDataHub\config\foreign_keys.yml`
- `E:\Projects\WorkDataHub\config\reference_sync.yml`
- `E:\Projects\WorkDataHub\src\work_data_hub\domain\reference_backfill\*`
- `E:\Projects\WorkDataHub\src\work_data_hub\orchestration\reference_sync_ops.py`
- `E:\Projects\WorkDataHub\src\work_data_hub\io\loader\*`
- `E:\Projects\WorkDataHub\docs\business-background\客户主数据回填与状态来源分析.md`
- 四份 legacy domain capability map，用于核对 domain-specific aggregation 与 customer-master signal 差异

## Stable Findings Absorbed

- `reference_sync` 与 `backfill` 应被稳定写成同一 reference strategy 下的两层对象，而不是一团“补齐逻辑”
- `backfill` 的稳定语义是从 canonicalized facts 派生 reference/customer objects，并以 domain-specific aggregation 写 customer-master signals
- `reference_sync` 的稳定语义是 authoritative source pre-load，并带有 sync mode、schedule、incremental state 与 provenance 区分
- 同名业务对象在两层里可能拥有不同 target footprint，wiki 不应因对象名相同而把写入面压扁

## Pilot Review Lessons

- 先写 durable evidence page，再回写 concept / surface / domain / index，确实能减少“边读边散写”造成的结构漂移
- domain thin-navigation 规则在本轮可稳定维持；四个 domain 页只需要补一个高价值 evidence 入口，不需要扩成 narrative page
- 下一次 pilot prompt 应提前点明“runtime/state 只写已证实对象，剩余一律进 `当前证据缺口`”，这样可进一步降低把 deferred runtime 误写成 stable conclusion 的风险
- 下一次 review gate 应显式检查 aggregate evidence page 是否只做 dispatcher 连接，而不是重新吸回对象级细节

## Next Entry Points

- [引用同步与回填证据](../../evidence/reference-and-backfill-evidence.md)
- [回填：`backfill`](../../concepts/backfill.md)
- [`reference_sync`](../../surfaces/reference-sync.md)

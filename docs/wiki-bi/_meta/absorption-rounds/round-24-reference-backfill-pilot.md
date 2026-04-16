# Round 24：引用同步与回填语义收紧

> 状态：Completed
> 日期：2026-04-16
> 主题簇：引用派生 / 回填 / 语义边界

## 本轮目标

- 把 `reference_sync` 与 `backfill` 从模糊的“补齐逻辑”拆成两个独立治理对象
- 把 authoritative pre-load、fact-derived writeback 与 customer-master 衍生信号分层写清
- 为四个 domain 建立统一可复用的引用同步 / 回填入口

## 使用的原始来源

- `E:\Projects\WorkDataHub\config\foreign_keys.yml`
- `E:\Projects\WorkDataHub\config\reference_sync.yml`
- `E:\Projects\WorkDataHub\src\work_data_hub\domain\reference_backfill\*`
- `E:\Projects\WorkDataHub\src\work_data_hub\orchestration\reference_sync_ops.py`
- `E:\Projects\WorkDataHub\src\work_data_hub\io\loader\*`
- `E:\Projects\WorkDataHub\docs\business-background\客户主数据回填与状态来源分析.md`
- 四份 legacy domain capability map，用于核对 domain-specific aggregation 与 customer-master signal 差异

## 本轮吸收的稳定结论

- `reference_sync` 与 `backfill` 应被稳定写成同一 reference strategy 下的两层对象，而不是一团“补齐逻辑”。
- `backfill` 的稳定语义是从 canonicalized facts 派生 reference/customer objects，并以 domain-specific aggregation 写 customer-master signals。
- `reference_sync` 的稳定语义是 authoritative source pre-load，并带有 sync mode、schedule、incremental state 与 provenance 区分。
- 同名业务对象在两层里可能拥有不同 target footprint；wiki 不应因对象名相同而把写入面压扁。
- `skip_blank_values`、temp-id 过滤与 `_needs_review` provenance 属于业务语义边界，不应退化成实现细节。

## 本轮回写页

- [引用同步与回填证据](../../evidence/reference-and-backfill-evidence.md)
- [回填：`backfill`](../../concepts/backfill.md)
- [`reference_sync`](../../surfaces/reference-sync.md)
- [`annuity_performance`](../../domains/annuity-performance.md)
- [`annuity_income`](../../domains/annuity-income.md)
- [`annual_award`](../../domains/annual-award.md)
- [`annual_loss`](../../domains/annual-loss.md)

## 下一步入口

- [引用同步与回填证据](../../evidence/reference-and-backfill-evidence.md)
- [回填：`backfill`](../../concepts/backfill.md)
- [`reference_sync`](../../surfaces/reference-sync.md)

# Round 30：relationship breadth deepening

> 状态：Completed
> 日期：2026-04-18
> 主题簇：customer-master relationship breadth / object promotion

## 本轮目标

- 把 `关联计划数` 从 dispatcher-only 提示推进为 durable concept page。
- 继续保持 Round 29 的 object-first 路径：先收紧 evidence dispatcher，再只提升一个最值得单独解释的对象。
- 不因为 relationship breadth 还存在其他对象，就一次性把 `其他年金计划`、`其他开拓机构` 也拆成独立页面。

## 本轮吸收的稳定结论

- `关联计划数` 是 customer-master relationship breadth signal，表达的是“这个客户关联了多少个不同计划”，而不是主导计划锚点。
- `关联计划数` 与 `关键年金计划` 同属 customer-master signal family，但回答的问题不同：一个回答 breadth，一个回答 dominance。
- `关联计划数` 也不等于 snapshot-side `plan_count`；前者属于 customer-master backfill 聚合，后者属于快照 / contract 语境下的输出解释。
- `其他年金计划` 与 `其他开拓机构` 目前仍更适合留在 evidence dispatcher，作为 relationship breadth 的附属解释对象。

## 本轮回写页

- [关联计划数](../../concepts/related-plan-count.md)
- [customer-master signals 证据](../../evidence/customer-master-signals-evidence.md)
- [回填：`backfill`](../../concepts/backfill.md)
- [关键年金计划](../../concepts/key-annuity-plan.md)
- [`annuity_performance`](../../domains/annuity-performance.md)
- [`annuity_income`](../../domains/annuity-income.md)
- [`annuity_performance` 输出合同](../../standards/output-correctness/annuity-performance-output-contract.md)
- [`annuity_income` 输出合同](../../standards/output-correctness/annuity-income-output-contract.md)

## 有意留在本轮之外的缺口

- `其他年金计划`
- `其他开拓机构`
- `管理资格`
- `组合代码`

这些对象仍先保留在 dispatcher / evidence 层，除非后续 raw sources 或 current-side evidence 把它们推进到独立 object-page 阈值。

## 下一步入口

- [关联计划数](../../concepts/related-plan-count.md)
- [customer-master signals 证据](../../evidence/customer-master-signals-evidence.md)
- [classification family 证据](../../evidence/classification-family-evidence.md)
- semantic-map-first 的 `company_lookup_queue` / `reference_sync` / shared operator artifacts discovery wave

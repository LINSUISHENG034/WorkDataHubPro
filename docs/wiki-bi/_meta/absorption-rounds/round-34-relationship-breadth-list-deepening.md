# Round 34：relationship breadth list deepening

> 状态：Completed
> 日期：2026-04-19
> 主题簇：customer-master relationship breadth / list signals / object promotion

## 本轮目标

- 把 `其他年金计划` 从 dispatcher-only 状态推进成 durable wiki 对象。
- 把 `其他开拓机构` 从 dispatcher-only 状态推进成 durable wiki 对象。
- 让计划侧与机构侧 relationship breadth 都形成 dominant value / breadth count / breadth list 三层对称表达。

## 本轮吸收的稳定结论

- `其他年金计划` 是计划侧 relationship-breadth list signal，用来补充“还关联了哪些计划”的 customer-master 语义，不等于 `关键年金计划`，也不等于 `关联计划数`。
- `其他开拓机构` 是机构侧 relationship-breadth list signal，用来补充“还关联了哪些机构”的 customer-master 语义，不等于 `主拓机构`，也不等于 `关联机构数`。
- 当前 durable wiki 对这两个对象的稳定治理重点是 breadth-list context，而不是先把字段名里的“其他”过度解释成“已经严格排除了 dominant anchor 的精确余集”。
- 经过本轮后，relationship breadth 已形成两组对称对象：
  - 计划侧：`关键年金计划` / `关联计划数` / `其他年金计划`
  - 机构侧：`主拓机构` / `关联机构数` / `其他开拓机构`

## 本轮回写页

- [其他年金计划](../../concepts/other-annuity-plans.md)
- [其他开拓机构](../../concepts/other-branches.md)
- [customer-master signals 证据](../../evidence/customer-master-signals-evidence.md)
- [回填：`backfill`](../../concepts/backfill.md)
- [关键年金计划](../../concepts/key-annuity-plan.md)
- [主拓机构](../../concepts/primary-branch.md)
- [关联计划数](../../concepts/related-plan-count.md)
- [关联机构数](../../concepts/related-branch-count.md)
- [`annuity_performance`](../../domains/annuity-performance.md)
- [`annuity_income`](../../domains/annuity-income.md)
- [`annuity_performance` 输出合同](../../standards/output-correctness/annuity-performance-output-contract.md)
- [`annuity_income` 输出合同](../../standards/output-correctness/annuity-income-output-contract.md)
- [`annual_award` 输出合同](../../standards/output-correctness/annual-award-output-contract.md)
- [`annual_loss` 输出合同](../../standards/output-correctness/annual-loss-output-contract.md)

## 有意留在本轮之外的缺口

- `组合代码`
- `is_churned_this_year` standalone object promotion
- manual `customer-mdm` / enterprise persistence closure wave

其中：

- `组合代码` 仍更适合留在 classification dispatcher / field-processing / contract 交叉入口层，除非后续 raw sources 或 current-side evidence 把它推进到独立 object-page 阈值。
- `is_churned_this_year` 仍继续留在 shared status pages，因为它还夹着 product-line / plan 双粒度与 AUM 汇总语义。

## 下一步入口

- [其他年金计划](../../concepts/other-annuity-plans.md)
- [其他开拓机构](../../concepts/other-branches.md)
- [customer-master signals 证据](../../evidence/customer-master-signals-evidence.md)
- `组合代码` / portfolio-anchor tightening，或回到 semantic-map-first 的 manual `customer-mdm` / enterprise persistence closure wave

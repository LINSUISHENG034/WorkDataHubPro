# Round 31：relationship breadth and classification closeout

> 状态：Completed
> 日期：2026-04-18
> 主题簇：customer-master relationship breadth / classification family / object promotion

## 本轮目标

- 把 `关联机构数` 从遗漏状态补入 durable wiki，收紧机构侧 relationship-breadth 语义。
- 把 `管理资格` 从 classification dispatcher 提升为独立 concept page。
- 继续保持 object-first 路径：只提升已满足 standalone question-answer 阈值的对象，不把 `其他年金计划`、`其他开拓机构`、`组合代码` 一次性都拆成概念页。

## 本轮吸收的稳定结论

- `关联机构数` 是 customer-master relationship-breadth signal，表达“这个客户关联了多少个不同机构”，不等于 `主拓机构`，也不等于 `其他开拓机构`。
- 机构侧 relationship breadth 现在可分成三层：`主拓机构` 回答 dominant value，`关联机构数` 回答 breadth count，`其他开拓机构` 回答 breadth list。
- `管理资格` 是 customer-master aggregation result，由 `业务类型` 经过 `concat_distinct` 等规则汇总而成，不等于输入侧单行 `业务类型`。
- classification family 现在更明确分成：输入解释锚点 `计划类型`、下游解释锚点 `业务类型`、customer-master 聚合分类 `年金计划类型` / `管理资格`、portfolio 锚点 `组合代码`。
- `组合代码` 仍更适合留在 evidence / field-processing / contract 交叉入口层，不在本轮提升为独立 concept page。

## 本轮回写页

- [关联机构数](../../concepts/related-branch-count.md)
- [管理资格](../../concepts/management-qualification.md)
- [customer-master signals 证据](../../evidence/customer-master-signals-evidence.md)
- [classification family 证据](../../evidence/classification-family-evidence.md)
- [回填：`backfill`](../../concepts/backfill.md)
- [主拓机构](../../concepts/primary-branch.md)
- [关联计划数](../../concepts/related-plan-count.md)
- [年金计划类型：`plan_type`](../../concepts/plan-type.md)
- [`annuity_performance` 字段处理证据](../../evidence/annuity-performance-field-processing-evidence.md)
- [`annuity_income` 字段处理证据](../../evidence/annuity-income-field-processing-evidence.md)
- [`annual_loss` 字段处理证据](../../evidence/annual-loss-field-processing-evidence.md)
- [`annuity_performance`](../../domains/annuity-performance.md)
- [`annuity_income`](../../domains/annuity-income.md)
- [`annuity_performance` 输出合同](../../standards/output-correctness/annuity-performance-output-contract.md)
- [`annuity_income` 输出合同](../../standards/output-correctness/annuity-income-output-contract.md)
- [`annual_award` 输出合同](../../standards/output-correctness/annual-award-output-contract.md)
- [`annual_loss` 输出合同](../../standards/output-correctness/annual-loss-output-contract.md)

## 有意留在本轮之外的缺口

- `其他年金计划`
- `其他开拓机构`
- `组合代码`

这些对象仍先保留在 dispatcher / evidence / contract 交叉入口层，除非后续 raw sources 或 current-side evidence 把它们推进到独立 object-page 阈值。

## 下一步入口

- [关联机构数](../../concepts/related-branch-count.md)
- [管理资格](../../concepts/management-qualification.md)
- [customer-master signals 证据](../../evidence/customer-master-signals-evidence.md)
- [classification family 证据](../../evidence/classification-family-evidence.md)
- semantic-map-first 的 `company_lookup_queue` / `reference_sync` / shared operator artifacts discovery wave

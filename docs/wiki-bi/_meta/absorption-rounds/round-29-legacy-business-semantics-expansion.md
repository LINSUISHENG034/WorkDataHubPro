# Round 29：legacy 业务语义扩展包

> 状态：Completed
> 日期：2026-04-18
> 主题簇：legacy business semantics / object promotion / shared-page tightening / classification package

## 本轮目标

- 把 customer-master relationship breadth 中最值得单独解释的对象提升为 durable concept page。
- 把 `is_churned_this_year` 从“只留在 aggregate status page 的一句说明”推进到共享状态页可直接回答的语义层。
- 把 `计划类型`、`年金计划类型`、`业务类型`、`管理资格`、`组合代码` 收紧成一组 cross-domain classification dispatcher，而不是继续散落在字段处理页。

## 本轮吸收的稳定结论

- `关键年金计划` 是 customer-master signal family 里的主导计划锚点，不等于任意一条源记录上的 `计划代码` / `年金计划号`。
- `关键年金计划`、`主拓机构` 与 `关联计划数` 需要一起理解，但只有前者在本轮达到了独立 concept page 的阈值。
- `is_churned_this_year` 是 monthly churn judgement：匹配粒度在当前快照月的 `规模明细` AUM 汇总为 `0`，或该月已无记录；它不等于 `is_loss_reported`。
- `is_churned_this_year` 与计划层 sibling 字段共享同一 semantic family，但两者的 match key 不同，因此本轮只收紧 shared pages，不强行拆成 standalone object page。
- `计划类型`、`年金计划类型`、`业务类型`、`管理资格`、`组合代码` 属于同一 classification family 的不同层，不应在单页字段处理语境里被误写成同一对象。

## 本轮回写页

- [关键年金计划](../../concepts/key-annuity-plan.md)
- [customer-master signals 证据](../../evidence/customer-master-signals-evidence.md)
- [回填：`backfill`](../../concepts/backfill.md)
- [主拓机构](../../concepts/primary-branch.md)
- [客户状态总览](../../concepts/customer-status.md)
- [客户状态语义正确性](../../standards/semantic-correctness/customer-status-semantics.md)
- [状态与快照证据](../../evidence/status-and-snapshot-evidence.md)
- [`is_loss_reported` 对象级证据](../../evidence/is-loss-reported-evidence.md)
- [classification family 证据](../../evidence/classification-family-evidence.md)
- [年金计划类型：`plan_type`](../../concepts/plan-type.md)
- [`annuity_performance` 字段处理证据](../../evidence/annuity-performance-field-processing-evidence.md)
- [`annuity_income` 字段处理证据](../../evidence/annuity-income-field-processing-evidence.md)
- [`annual_loss` 字段处理证据](../../evidence/annual-loss-field-processing-evidence.md)

## 有意留在本轮之外的缺口

- `关联计划数`、`其他年金计划`、`其他开拓机构` 继续留在 customer-master signal dispatcher；本轮不继续拆更多 concept pages。
- `is_churned_this_year` 暂不创建 standalone evidence page；剩余未拆内容主要是 product-line / plan 双粒度细节。
- `管理资格` 与 `组合代码` 暂不创建独立 concept page；先由 classification dispatcher 承接跨域语义。
- broader runtime / operator closure 继续留给 semantic-map-first discovery，而不是被本轮顺手吸收。
- semantic-map ledger registration alone does not justify semantic promotion；queue / runtime / operator surfaces 即使被 ledger 发现，也必须继续留在 runtime/operator discovery，而不是被误写成 canonical business semantics。

## 下一步入口

- [关键年金计划](../../concepts/key-annuity-plan.md)
- [classification family 证据](../../evidence/classification-family-evidence.md)
- [状态与快照证据](../../evidence/status-and-snapshot-evidence.md)
- semantic-map-first 的 `company_lookup_queue` / `reference_sync` / shared operator artifacts discovery wave

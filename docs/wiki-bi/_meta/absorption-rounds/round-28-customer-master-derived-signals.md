# Round 28：customer-master derived signals 收紧

> 状态：Completed
> 日期：2026-04-18
> 主题簇：customer master / backfill / cross-domain signal family

## 本轮目标

- 把 `tags`、`主拓机构` 与 customer-master-derived signal family 从 scattered mentions 收紧成 durable object pages 与 evidence dispatcher
- 让四个高流量 domain 的输出合同都能把 customer-master signal 说清，而不再只靠 `foreign_keys.yml` / capability map 原始材料
- 继续保持本轮只处理 durable business semantics，不扩张到新的 runtime/operator closure

## 本轮吸收的稳定结论

- `tags` 是 customer-master 事件轨迹，不是 snapshot status 的别名。
- `主拓机构`、`关键年金计划` 等字段是 weighted dominant values，而不是输入列直接复制。
- `年金客户类型` 与 `tags` 同属 customer-master signal family，但分别承载分类标签与时间轨迹两类语义。
- 不同 domain 以不同权重列（`期末资产规模`、`固费`、`计划规模`）形成 customer-master 主导值；字段名相同不等于来源规则相同。
- 这组语义更适合落在 object pages + evidence dispatcher，而不是继续散落在 output contract 与 field-processing 页面里。

## 本轮回写页

- [customer-master signals 证据](../../evidence/customer-master-signals-evidence.md)
- [`tags`](../../concepts/tags.md)
- [主拓机构](../../concepts/primary-branch.md)
- [回填：`backfill`](../../concepts/backfill.md)
- [年金客户类型：`customer_type`](../../concepts/customer-type.md)
- [`annuity_performance` 输出合同](../../standards/output-correctness/annuity-performance-output-contract.md)
- [`annuity_income` 输出合同](../../standards/output-correctness/annuity-income-output-contract.md)
- [`annual_award` 输出合同](../../standards/output-correctness/annual-award-output-contract.md)
- [`annual_loss` 输出合同](../../standards/output-correctness/annual-loss-output-contract.md)

## 有意留在本轮之外的缺口

- `is_churned_this_year` 仍保持在 aggregate status page，不在本轮拆成对象级 evidence。
- `关键年金计划`、`关联计划数`、`其他年金计划`、`其他开拓机构` 仍先由 evidence dispatcher 承载，不在本轮一次性拆成更多 concept pages。
- broader runtime/operator closure（queue、reference sync、standalone tooling 等）继续遵循 semantic-map-first discovery，而不是被本轮 customer-master 语义补强顺手带入。

## 下一步入口

- [customer-master signals 证据](../../evidence/customer-master-signals-evidence.md)
- [回填：`backfill`](../../concepts/backfill.md)
- [wiki-bi 首页](../../index.md)

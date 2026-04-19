# customer-master signals 证据

## 结论主题

本页聚合 customer-master-derived signal family 相关证据：`tags`、`主拓机构`、`关键年金计划`、`关联计划数`、`关联机构数`、`其他年金计划`、`其他开拓机构` 与 `年金客户类型`。

## 证据记录

| evidence_id | source_type | evidence_strength | coverage_state | supported_pages | last_verified | notes |
|---|---|---|---|---|---|---|
| E-CMS-001 | legacy_config | strong | absorbed | `backfill`, `customer-type`, `tags`, `primary-branch`, `key-annuity-plan`, `related-plan-count`, `related-branch-count`, `other-annuity-plans`, `other-branches`, `annuity-performance-output-contract`, `annuity-income-output-contract`, `annual-award-output-contract`, `annual-loss-output-contract` | 2026-04-19 | `E:\Projects\WorkDataHub\config\foreign_keys.yml` 为四个 domain 的 `fk_customer` 明确声明 `max_by`、`concat_distinct`、`count_distinct`、`template` 与 `jsonb_append(tags)`，证明 customer-master signals 是配置化但真实执行的业务语义。 |
| E-CMS-002 | legacy_doc | strong | absorbed | `backfill`, `customer-type`, `tags`, `primary-branch`, `key-annuity-plan`, `related-plan-count`, `related-branch-count`, `other-annuity-plans`, `other-branches` | 2026-04-19 | `E:\Projects\WorkDataHub\docs\business-background\客户主数据回填与状态来源分析.md` 明确 customer master backfill、状态规则与 snapshot 是三层对象，并把 `年金客户类型=新客/新客*` 与 `is_new` 分开。 |
| E-CMS-003 | legacy_doc | strong | absorbed | `customer-master-signals-evidence`, `primary-branch`, `key-annuity-plan`, `related-plan-count`, `related-branch-count`, `other-annuity-plans`, `other-branches`, `annuity-performance-output-contract` | 2026-04-19 | `E:\Projects\WorkDataHub\docs\domains\annuity_performance-capability-map.md` 把 `主拓机构`、`关键年金计划`、`关联计划数`、`tags` 写成 annuity-performance 对 `customer.客户明细` 的显式 backfill 输出，并指出 dominant-value 由 `期末资产规模` 决定。 |
| E-CMS-004 | legacy_doc | strong | absorbed | `customer-master-signals-evidence`, `key-annuity-plan`, `related-plan-count`, `related-branch-count`, `other-annuity-plans`, `other-branches`, `annuity-income-output-contract`, `customer-type` | 2026-04-19 | `E:\Projects\WorkDataHub\docs\domains\annuity_income-capability-map.md` 明确 annuity_income 的 `fk_customer` 以 `固费` 为主导权重，并写入 `tags=yyMM新建` 与 `年金客户类型=新客*`。 |
| E-CMS-005 | legacy_doc | supporting | absorbed | `customer-master-signals-evidence`, `annual-award-output-contract`, `tags`, `customer-type`, `other-annuity-plans`, `other-branches` | 2026-04-19 | `E:\Projects\WorkDataHub\docs\domains\annual_award-capability-map.md` 明确 annual_award 会向 `customer.客户明细` 写入 `yyMM中标` 与 `年金客户类型=中标客户`，并使用 `计划规模` 形成主导 customer-master signals。 |
| E-CMS-006 | legacy_doc | supporting | absorbed | `customer-master-signals-evidence`, `annual-loss-output-contract`, `tags`, `customer-type`, `other-annuity-plans`, `other-branches` | 2026-04-19 | `E:\Projects\WorkDataHub\docs\domains\annual_loss-capability-map.md` 明确 annual_loss 会向 `customer.客户明细` 写入 `yyMM流失` 与 `年金客户类型=流失客户`，并使用 `计划规模` 形成 event-driven 主导 customer-master signals。 |
| E-CMS-007 | legacy_doc | strong | absorbed | `customer-master-signals-evidence`, `primary-branch`, `key-annuity-plan`, `related-plan-count`, `related-branch-count`, `other-annuity-plans`, `other-branches`, `tags` | 2026-04-19 | `E:\Projects\WorkDataHub\docs\verification_guide_real_data.md` 第 5 步把 `主拓机构`、`关键年金计划`、`关联计划数`、`关联机构数`、`其他年金计划`、`其他开拓机构`、`tags` 与 `年金客户类型` 视为 operator 需要显式核验的结果，而不是可忽略的实现副产物。 |

## 本轮已吸收的稳定结论

- customer-master-derived signals 是独立的业务语义层，不等于 snapshot status。
- `tags` 是按时间编码的 customer-master 事件轨迹，`yyMM新建` / `yyMM中标` / `yyMM流失` 都来自 backfill 聚合，而不是事实表原始列搬运。
- `主拓机构`、`关键年金计划` 这类字段是 weighted dominant values，不是某条源记录的直接复制结果。
- `关联计划数` 与 `关联机构数` 这类字段是 relationship-breadth count signals；它们回答的是“宽度有多大”，而不是“哪一个对象最主导”。
- `其他年金计划`、`其他开拓机构` 这类字段是 relationship-breadth list signals；它们用来补充 breadth context，但不替代 dominant value 或 breadth count。
- `关键年金计划` 现在已提升为独立 durable concept page；它回答“哪一个计划最具主导性”，不替代 relationship breadth 信号。
- `关联计划数` 现在已提升为独立 durable concept page；它回答“有多少个不同计划”，不回答“哪一个计划最具主导性”。
- `关联机构数` 现在也已提升为独立 durable concept page；它回答“有多少个不同机构”，不回答“哪一个机构占主导”，也不枚举完整机构清单。
- `其他年金计划` 现在也已提升为独立 durable concept page；它回答“还关联了哪些计划”的 breadth-list context，不等于 `关键年金计划`，也不等于 `关联计划数`。
- `其他开拓机构` 现在也已提升为独立 durable concept page；它回答“还关联了哪些机构”的 breadth-list context，不等于 `主拓机构`，也不等于 `关联机构数`。
- 对这两个 breadth-list 对象，当前稳定 raw-source 证据支持“list-form context”这一层语义，但还不足以把字段名里的“其他”强写成“已经严格排除 dominant anchor 的精确数学余集”。
- `年金客户类型` 与 `tags` 都属于 customer-master signal family，但它们分别承担分类标签与时间轨迹两类不同语义。
- 不同 domain 对同一 `fk_customer` 写入不同 signal family 成员，真正稳定的语义来自“domain + aggregation rule + target field”的组合，而不是字段名孤立存在。

## 哪些来源是强证

- `E:\Projects\WorkDataHub\config\foreign_keys.yml`
- `E:\Projects\WorkDataHub\docs\business-background\客户主数据回填与状态来源分析.md`
- `E:\Projects\WorkDataHub\docs\verification_guide_real_data.md`
- `E:\Projects\WorkDataHub\docs\domains\annuity_performance-capability-map.md`
- `E:\Projects\WorkDataHub\docs\domains\annuity_income-capability-map.md`

## 哪些来源只是旁证

- `E:\Projects\WorkDataHub\docs\domains\annual_award-capability-map.md`
- `E:\Projects\WorkDataHub\docs\domains\annual_loss-capability-map.md`

## 对象级分发入口

- [`tags`](../concepts/tags.md)
- [主拓机构](../concepts/primary-branch.md)
- [关键年金计划](../concepts/key-annuity-plan.md)
- [关联计划数](../concepts/related-plan-count.md)
- [关联机构数](../concepts/related-branch-count.md)
- [其他年金计划](../concepts/other-annuity-plans.md)
- [其他开拓机构](../concepts/other-branches.md)
- [回填：`backfill`](../concepts/backfill.md)
- [年金客户类型：`customer_type`](../concepts/customer-type.md)

## 当前证据缺口

- dominant value、breadth count 与 breadth list 三层关系现在都已有独立对象页；本页继续承担 cross-domain dispatcher，而不再承担 breadth-list 的唯一解释入口。
- multi-domain 情况下 customer-master signal 最终写入 precedence 仍主要由 legacy config + verification path 证明，尚未提升为 current-side 独立治理对象。
- current project 已显式保护部分 customer-master signal publication，但 relationship breadth 与 classification family 仍主要依赖 legacy raw sources + durable wiki 吸收，而非独立 current-side object family contract。

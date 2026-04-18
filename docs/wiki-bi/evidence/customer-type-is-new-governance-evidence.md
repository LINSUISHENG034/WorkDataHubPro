# customer_type vs `is_new` 治理证据

## 结论主题

本页固化 `customer_type` 与 `is_new` 的治理收口：两者在语义上不等价，但 legacy 相邻流程曾把 customer-type label 当作 operational proxy 使用。这里需要表达的不是“它们像不像”，而是如何把 semantic truth、proxy history 与 disposition question 分层保留。

## 证据记录

| evidence_id | source_type | evidence_strength | coverage_state | supported_pages | last_verified | notes |
|---|---|---|---|---|---|---|
| E-CTN-001 | legacy_doc | strong | absorbed | `customer-type`, `is-new`, `customer-status-semantics` | 2026-04-18 | `E:\Projects\WorkDataHub\docs\business-background\客户主数据回填与状态来源分析.md` 明确 `年金客户类型` 属于主数据/回填标签，而 `is_new` 属于快照状态判断。 |
| E-CTN-002 | current_wiki | supporting | absorbed | `customer-type`, `customer-status-semantics`, `status-and-snapshot-evidence` | 2026-04-18 | 当前 wiki 已明确两者不等价，但此前仍主要停留在概念提示层，尚未把 proxy usage 写成独立治理对象。 |
| E-CTN-003 | semantic_map | supporting | absorbed | `customer-status-semantics`, `legacy-semantic-map` successor-wave reports | 2026-04-18 | `sem-non-equivalence-customer-type-vs-is-new` 已证明 semantic non-equivalence，但剩余问题已转化为 governance disposition，而不是继续补 discovery。 |

## 稳定语义结论

- `customer_type` 与 `is_new` 在语义上不等价。
- `customer_type` 属于 customer-master-derived label family；`is_new` 属于快照状态语义。
- `is_new` 的稳定定义来自年度状态判断（当年中标且非 existing），而不是来自 customer-type label。
- 即使某些标签值看起来接近“新客”或“中标客户”，也不能把 customer-type label 提升成 `is_new` 的 semantic truth。

## legacy proxy usage 的治理处置

应明确区分三层：

- semantic truth
  - `customer_type` 不是 `is_new`
- legacy proxy usage
  - 相邻流程可能借用 customer-type label 作为操作近似信号
- governance disposition
  - 这类 proxy usage 应被判定为：
    - `deferred compatibility bridge`
    - `retired for future semantic interpretation`
    - 或 `historical_context_only`

当前 durable wiki 的任务，不是替 proxy usage 洗白，而是把它从“语义定义”降回“待处置治理对象”。

## 当前证据缺口

- 尚未形成最终主线程裁决：legacy customer-type proxy usage 应视为 deferred compatibility bridge，还是只保留为 historical context。
- current rebuild-side 并未把 customer-type label 收为 `is_new` truth，但仍需明确后续文档/验证资产是否允许继续以 proxy 口径叙述该冲突。
- 若未来存在兼容性说明，仍需明确其边界：只能描述 historical / compatibility context，不能改写 semantic standard。

## 相关页面

- [年金客户类型：`customer_type`](../concepts/customer-type.md)
- [新到账客户状态：`is_new`](../concepts/is-new.md)
- [客户状态语义正确性](../standards/semantic-correctness/customer-status-semantics.md)
- [customer 年度身份证据](./customer-status-annual-identity-evidence.md)
- [状态与快照证据](./status-and-snapshot-evidence.md)

# `enterprise enrichment persistence`

## Surface 定义

这里指围绕 identity lookup / provider persistence 形成的一组 enterprise 侧持久化 surface，至少包括：

- `enterprise.enrichment_index`
- `enterprise.enrichment_requests`
- `enterprise.base_info`

它们共同承接缓存、异步补查排队、provider 结果持久化与后续复用。

## Surface 类型

- persistence surface
- runtime surface
- operator-adjacent surface

## Legacy 职责

- 为 `company_id` 解析提供可复用的 cache / lookup persistence
- 将 unresolved names 以 `pending` / `processing` 语义写入异步补查队列
- 持久化 EQC / provider 返回的企业原始与解析结果
- 为 GUI / manual lookup / domain backflow 提供共享 persistence footing

## 关键对象

- `enterprise.enrichment_index`
  - identity cache 与后续 lookup 的核心持久化对象
- `enterprise.enrichment_requests`
  - unresolved-name async queue 的持久化入口
- `enterprise.base_info`
  - provider 结果与解析字段的持久化对象

## 为什么它是独立 surface

它不属于某个单独 domain 的内部表，而是一组被多条运行路径共同写入和读取的 persistence surface。

它至少同时服务：

- resolver 的 DB cache lookup
- temp-id 之后的 async enqueue
- EQC/provider 结果持久化
- GUI 工具的可选持久化

因此它不能被简化成“queue 的内部实现细节”或“某个 provider helper 的附属表”。

## 相关概念

- [企业身份标识：`company_id`](../concepts/company-id.md)
- [临时身份：`temp_id`](../concepts/temp-id.md)

## 相关标准

- [输出正确性标准](../standards/output-correctness/output-correctness.md)
- [golden scenarios](../standards/verification-method/golden-scenarios.md)

## 关键证据来源

- [operator 与 surface 证据](../evidence/operator-and-surface-evidence.md)
- [身份与补查证据](../evidence/identity-and-lookup-evidence.md)

## 当前重构处理状态

- 当前应被视为 Phase E governance 中的显式 persistence surface
- 至少不能再把 `enrichment_index`、`enrichment_requests`、`base_info` 统称为“identity 附属表”后长期隐身
- current accepted validation runtime 没有 repo-native `enrichment_requests`、`enrichment_index`、`company_name_index`、`base_info`、`business_info`、`biz_label` 等 surface；被保留的是 identity 行为链与 evidence contract，而不是 legacy 表面宽度
- 因此更合理的 closure 方式不是整体 retain / retire，而是分别判断 cache、queue persistence、provider raw/cleansed persistence 的 active runtime status

## Round 21 决策边界

| 子对象 | 当前边界 | 说明 |
|---|---|---|
| `enrichment_index` / `company_name_index` | `replace + defer` | current validation runtime 以 cache interface / in-memory cache 替代 legacy DB cache footprint；durable cache persistence 继续 deferred。 |
| `enrichment_requests` | `defer` | queue persistence 不属于 current active runtime；若 future async lookup runtime 被 admitted，再单独决定 retain / replace。 |
| `base_info` / `business_info` / `biz_label` | `defer` | provider raw/cleansed persistence 不是 current accepted validation scope；若 future live provider operations 需要 durable persistence，应单独 re-admit。 |

额外约束：

- `retain`
  - 这些对象作为独立 persistence family 的制度记忆
  - cache / queue / provider persistence 三层分化本身
- `retire`
  - “identity 行为链只有在保留 legacy 表面宽度时才成立”这一假设

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
- 当前更合理的处理方式是分别判断 cache、queue、provider persistence 哪些需要 retain，哪些应该 replace 或 defer

## 仍未决的问题

- `enrichment_index` 是否属于 rebuild 必须保留的核心 cache surface
- `enrichment_requests` 这类 queue persistence 是必须保留，还是可被其他异步机制替代
- `base_info` 这类 provider-facing persistence 是核心运行面，还是 operator-adjacent support surface

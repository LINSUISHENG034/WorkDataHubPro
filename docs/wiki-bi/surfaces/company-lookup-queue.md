# `company_lookup_queue`

## Surface 定义

`company_lookup_queue` 是围绕企业补查、异步解析与队列处理形成的独立 runtime surface。

## Surface 类型

- runtime surface
- operator surface
- persistence-adjacent surface

## Legacy 职责

- 承接异步补查请求
- 驱动企业补查重试与状态更新
- 与 enrichment persistence surfaces 协同工作
- 通过独立 operator entrypoint 暴露给运行面

## 关键运行语义

legacy code 进一步说明：

- queue 写入发生在 temp-id 生成之后，而不是任意时刻都可触发
- queue 去重依赖 `normalized_name` 与 `pending` / `processing` 状态
- enqueue 失败采用 graceful degradation，不阻断主处理链路

## 关键运行面对象

- `enterprise.enrichment_requests`
- `enterprise.enrichment_index`
- 相关 provider / refresh persistence

这说明它不是“一个函数名”，而是一整块 identity runtime surface。

## 为什么它是独立 surface

它不是普通 business domain，因为它处理的不是业务事实表，而是 identity lookup 的运行面与操作面。

它也不能被简化成“某个 domain 内部的 fallback 细节”，因为：

- 它有独立 CLI / orchestration 入口
- 它有独立 persistence footprint
- 它承担 queue、retry、status update 语义

## 相关 surfaces

- [enterprise enrichment persistence](./enterprise-enrichment-persistence.md)
- [`unknown_names_csv`](./unknown-names-csv.md)

## 相关概念

- [企业身份标识：`company_id`](../concepts/company-id.md)

## 相关标准

- [身份治理语义正确性](../standards/semantic-correctness/identity-governance.md)
- [输出正确性标准](../standards/output-correctness/output-correctness.md)
- [real-data validation](../standards/verification-method/real-data-validation.md)

## 关键证据来源

- [operator 与 surface 证据](../evidence/operator-and-surface-evidence.md)
- [身份与补查证据](../evidence/identity-and-lookup-evidence.md)

## 当前重构处理状态

- 当前应视为显式治理对象
- current accepted validation runtime 没有 repo-native `company_lookup_queue`；当前主链路已被同步 identity chain、temp-id fallback 与 operator-visible unresolved artifacts 替代
- 被保留的是 async lookup runtime 这一治理对象与其 dedup / retry / graceful degradation 语义，而不是 legacy queue runtime 本身
- `enterprise.enrichment_requests` 一类 queue persistence 仍随 broader queue/runtime plan 一并 deferred
- 当前至少不应再被当作“隐含存在，不必登记”的对象

## Round 21 决策边界

- `retain`
  - async lookup runtime 是独立 surface，不是 identity fallback chain 的一个可省略细节
  - dedup、status update、retry、graceful degradation 这些运行语义需要作为 future design requirement 被记住
- `replace`
  - current validation runtime 以 `source_value -> cache_hit -> provider_lookup -> temp_id_fallback` 替代 queue 依赖
  - unresolved names 以 operator artifacts 外显，而不是写入 current repo 的 queue persistence
- `defer`
  - queue persistence
  - retry orchestration
  - schedule / sensor / operator flow
- `retire`
  - “accepted slices 已经保留 queue runtime”这一说法

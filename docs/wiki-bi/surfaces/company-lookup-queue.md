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

## 相关概念

- [企业身份标识：`company_id`](../concepts/company-id.md)

## 相关标准

- [输出正确性标准](../standards/output-correctness/output-correctness.md)
- [real-data validation](../standards/verification-method/real-data-validation.md)

## 关键证据来源

- [operator 与 surface 证据](../evidence/operator-and-surface-evidence.md)
- [身份与补查证据](../evidence/identity-and-lookup-evidence.md)

## 当前重构处理状态

- 当前应视为显式治理对象
- retain / replace / retire 结论仍需后续稳定决策页明确
- 当前至少不应再被当作“隐含存在，不必登记”的对象
- enterprise persistence breadth 仍需后续拆分和澄清

## 仍未决的问题

- queue 运行面是否会在 rebuild 中保留
- 与 live provider mode 的边界如何定义

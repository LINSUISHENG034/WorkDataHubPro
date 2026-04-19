# Round 36：manual customer-mdm and persistence closure

> 状态：Completed
> 日期：2026-04-19
> 主题簇：manual operator runtime / enterprise persistence layering / object-level evidence routing

## 本轮目标

- 把 manual `customer-mdm` runtime boundary 从 surface-level 叙述推进成对象级 evidence route。
- 把 enterprise enrichment persistence family 的 layering 从 aggregate surface text 推进成对象级 evidence route。
- 明确 current accepted runtime 保护的是 projection / identity behavior chain，而不是 repo-native manual commands 或 legacy persistence footprint。

## 本轮吸收的稳定结论

- legacy manual `customer-mdm` commands 是独立 operator surface，不是 hook path 的副产品。
- `sync`、`snapshot`、`init-year`、`cutover` 是 write / recompute surfaces，而 `validate` 是 read-only validation surface。
- legacy monthly default path 更接近由 `annuity_performance` 成功后的 hook chain 驱动；manual commands 属于 recovery / recompute path，而不是默认 primary trigger。
- enterprise persistence family 至少分成三层：cache/queue persistence、provider-retention root、downstream normalized/parsed persistence。
- `base_info` 是 provider-retention root，`business_info` / `biz_label` 是 downstream business-canonicalized persistence，不应再被和 queue/cache tables 混写成一层。
- current accepted runtime 证明了 projection semantics 与 identity behavior chain，但没有 re-admit repo-native manual commands 或 legacy persistence footprint。

## 本轮回写页

- [`customer-mdm` manual runtime 证据](../../evidence/customer-mdm-manual-runtime-evidence.md)
- [enterprise enrichment persistence 证据](../../evidence/enterprise-enrichment-persistence-evidence.md)
- [`customer-mdm` 手工命令面](../../surfaces/customer-mdm-commands.md)
- [enterprise enrichment persistence](../../surfaces/enterprise-enrichment-persistence.md)
- [customer MDM 生命周期证据](../../evidence/customer-mdm-lifecycle-evidence.md)
- [身份与补查证据](../../evidence/identity-and-lookup-evidence.md)
- [operator 与 surface 证据](../../evidence/operator-and-surface-evidence.md)
- [身份治理语义正确性](../../standards/semantic-correctness/identity-governance.md)

## 有意留在本轮之外的缺口

- `company_lookup_queue` retry/runtime closure
- standalone tooling closure
- manual `customer-mdm` commands 的逐命令 retain / replace / retire 裁决
- enterprise persistence family 的逐表 current-side retain / replace / retire 裁决

## 下一步入口

- [`customer-mdm` manual runtime 证据](../../evidence/customer-mdm-manual-runtime-evidence.md)
- [enterprise enrichment persistence 证据](../../evidence/enterprise-enrichment-persistence-evidence.md)
- `company_lookup_queue` / standalone tooling 等 runtime/operator decision package

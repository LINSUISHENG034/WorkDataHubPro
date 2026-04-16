# Round 25：身份治理语义分层收紧

> 状态：Completed
> 日期：2026-04-16
> 主题簇：身份治理 / 分层表达

## 本轮目标

- 深化 `company_id` / `temp_id` / identity governance 的语义表达
- 显式分离“当前运行路径”“兼容性清单 / 历史记忆”“已退休回退行为”“面向操作人员的可见后果”
- 保持 `company_lookup_queue` 与 `enterprise enrichment persistence` 作为两个独立 surface

## 本轮吸收的稳定结论

- 身份治理叙述必须维持四层分离，避免把 historical memory 或 deferred runtime 混写为当前运行路径。
- `company_lookup_queue` 与 `enterprise enrichment persistence` 不是同一对象；前者描述异步补查调度语义，后者描述 cache / queue / provider persistence family。
- unresolved identity 必须对 operator 可见；如果 queue/persistence 当前未物化，就必须进入 artifacts、signals 或 evidence gaps。
- ID5 fallback 与 legacy `TE...` temp identity 属于已退休行为；它们只能作为 provenance 和记忆保留，不能被误写成当前可选路径。

## 本轮回写页

- [企业身份标识：`company_id`](../../concepts/company-id.md)
- [临时身份：`temp_id`](../../concepts/temp-id.md)
- [身份治理语义正确性](../../standards/semantic-correctness/identity-governance.md)
- [`company_lookup_queue`](../../surfaces/company-lookup-queue.md)
- [enterprise enrichment persistence](../../surfaces/enterprise-enrichment-persistence.md)
- [身份与补查证据](../../evidence/identity-and-lookup-evidence.md)

## 下一步入口

- [身份治理语义正确性](../../standards/semantic-correctness/identity-governance.md)
- [企业身份标识：`company_id`](../../concepts/company-id.md)
- [临时身份：`temp_id`](../../concepts/temp-id.md)

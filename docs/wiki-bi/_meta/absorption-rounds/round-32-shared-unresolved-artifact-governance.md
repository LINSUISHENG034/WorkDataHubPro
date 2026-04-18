# Round 32：shared unresolved artifact governance

> 状态：Completed
> 日期：2026-04-18
> 主题簇：semantic-map-adjacent surface discovery / unresolved-name / failed-record artifacts / queue replacement evidence

## 本轮目标

- 把 shared unresolved-name / failed-record artifacts 从 scattered gaps 收紧成一个 durable evidence dispatcher。
- 明确 `company_lookup_queue` deferred 之后，operator-visible consequence 由哪些 artifacts / evidence 承接。
- 保持 current accepted closure 的边界真实：只把 `annuity_income` 写成已显式保护的 artifact contract，不把它误推广成全域 active runtime。

## 本轮吸收的稳定结论

- `unknown_names_csv` 与 failed-record export 共同构成 unresolved identity / failure-path 的 operator-visible artifact family，但两者回答的问题不同。
- legacy breadth 中，`annuity_income` 与 `annuity_performance` 都有 unresolved-name + failed-record artifacts，`annual_award` / `annual_loss` 至少保留 failed-record export。
- deferred `company_lookup_queue` runtime 不等于 operator-visible consequence 消失；当 queue 不在 current active runtime 中时，artifacts / signal / evidence package 仍需承接这层可见后果。
- current accepted artifact closure 目前只对 `annuity_income` 明确成立。
- 因此本轮写入的是 shared evidence dispatcher，不是 cross-domain parity completed claim。

## 本轮回写页

- [unresolved-name and failed-record 证据](../../evidence/unresolved-name-and-failed-record-evidence.md)
- [operator 与 surface 证据](../../evidence/operator-and-surface-evidence.md)
- [身份与补查证据](../../evidence/identity-and-lookup-evidence.md)
- [`annuity_income` operator artifacts 证据](../../evidence/annuity-income-operator-artifacts-evidence.md)
- [`company_lookup_queue`](../../surfaces/company-lookup-queue.md)
- [`unknown_names_csv`](../../surfaces/unknown-names-csv.md)
- [failed-record 导出](../../surfaces/failed-record-export.md)
- [身份治理语义正确性](../../standards/semantic-correctness/identity-governance.md)
- [企业身份标识：`company_id`](../../concepts/company-id.md)
- [`annuity_income`](../../domains/annuity-income.md)
- [`annuity_performance`](../../domains/annuity-performance.md)
- [`annuity_income` 输出合同](../../standards/output-correctness/annuity-income-output-contract.md)

## 有意留在本轮之外的缺口

- `annuity_performance` / `annual_award` / `annual_loss` 的 current-side artifact parity
- domain-agnostic failed-record export schema / retention / operator consumption contract
- `company_lookup_queue` retry / schedule / persistence runtime closure

## 下一步入口

- [unresolved-name and failed-record 证据](../../evidence/unresolved-name-and-failed-record-evidence.md)
- [`company_lookup_queue`](../../surfaces/company-lookup-queue.md)
- [`unknown_names_csv`](../../surfaces/unknown-names-csv.md)
- [failed-record 导出](../../surfaces/failed-record-export.md)
- semantic-map-first 的 `reference_sync` / manual `customer-mdm` / enterprise persistence closure wave

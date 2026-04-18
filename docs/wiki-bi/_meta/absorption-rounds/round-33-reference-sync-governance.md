# Round 33：reference_sync governance

> 状态：Completed
> 日期：2026-04-19
> 主题簇：semantic-map-adjacent surface discovery / reference_sync / target inventory / incremental state / current replacement boundary

## 本轮目标

- 把 `reference_sync` 的 target inventory、incremental sync-state 与 current replacement boundary 从 scattered statements 收紧成 durable object-level evidence route。
- 继续保持 `reference_sync` 作为治理 surface，而不是误写成已恢复的 repo-native runtime。
- 给高流量标准页和 `backfill` / `reference_sync` 边界页一个直接入口，而不是只依赖 aggregate dispatcher。

## 本轮吸收的稳定结论

- `reference_sync` 通过 explicit target inventory 受治理，而不是作为 background helper 隐身存在。
- `reference_sync` 的 legacy contract 包含 per-table `last_synced_at` incremental sync-state，不是单纯的 stateless full refresh。
- current accepted slices 已用显式 `reference_derivation -> publication` 取代 hidden sync runtime side effects。
- 被取代的是 legacy runtime breadth，不是 target inventory、authoritative source mapping 或 sync contract 这层治理记忆。
- 因此本轮写入的是 object-level evidence route，不是 bootstrap/runtime closure claim。

## 本轮回写页

- [`reference_sync` runtime and state 证据](../../evidence/reference-sync-runtime-and-state-evidence.md)
- [`reference_sync`](../../surfaces/reference-sync.md)
- [引用同步与回填证据](../../evidence/reference-and-backfill-evidence.md)
- [operator 与 surface 证据](../../evidence/operator-and-surface-evidence.md)
- [回填：`backfill`](../../concepts/backfill.md)
- [输出正确性标准](../../standards/output-correctness/output-correctness.md)

## 有意留在本轮之外的缺口

- repo-native `reference_sync` runtime / schedule / state store re-admission
- sync-state persistence schema / retention / operator recovery contract 的更细对象化表达
- `manual customer-mdm` 与 enterprise persistence closure wave

## 下一步入口

- [`reference_sync` runtime and state 证据](../../evidence/reference-sync-runtime-and-state-evidence.md)
- [`reference_sync`](../../surfaces/reference-sync.md)
- [引用同步与回填证据](../../evidence/reference-and-backfill-evidence.md)
- semantic-map-first 的 `manual customer-mdm` / enterprise persistence closure wave

# `reference_sync` runtime and state 证据

## 结论主题

本页聚合 `reference_sync` 的 object-level evidence，重点是：

- explicit target inventory
- incremental sync-state contract
- current `reference_derivation -> publication` replacement boundary

目标不是把这三层压成同一件事，而是明确：

- target inventory 定义它“同步什么”
- sync-state contract 定义它“如何增量同步”
- current replacement evidence 定义“今天 accepted slices 用什么替代 legacy hidden runtime”

## 证据记录

| evidence_id | source_type | evidence_strength | coverage_state | supported_pages | last_verified | notes |
|---|---|---|---|---|---|---|
| E-RS-001 | legacy_config | strong | absorbed | `reference-sync`, `reference-sync-runtime-and-state-evidence`, `reference-and-backfill-evidence` | 2026-04-19 | `E:\Projects\WorkDataHub\config\reference_sync.yml` 显式声明 target schema / table、source type、sync mode、schedule、concurrency 与部分 `last_synced_at` incremental contract。 |
| E-RS-002 | legacy_code | strong | absorbed | `reference-sync`, `reference-sync-runtime-and-state-evidence` | 2026-04-19 | `E:\Projects\WorkDataHub\src\work_data_hub\orchestration\reference_sync_ops.py` 明确 `plan_only`、`force_full_sync`、显式 state、persisted state 与 state persistence 是 operator-facing runtime controls。 |
| E-RS-003 | legacy_code | strong | absorbed | `reference-sync`, `reference-sync-runtime-and-state-evidence` | 2026-04-19 | `E:\Projects\WorkDataHub\src\work_data_hub\io\repositories\sync_state_repository.py` 证明 legacy runtime 有 per-job / per-table `last_synced_at` state persistence，而不是无状态全量刷新。 |
| E-RS-004 | legacy_code | strong | absorbed | `reference-sync`, `reference-sync-runtime-and-state-evidence`, `reference-and-backfill-evidence` | 2026-04-19 | `E:\Projects\WorkDataHub\src\work_data_hub\domain\reference_backfill\sync_models.py` 把 target table、target schema、source type、sync mode、primary key 与 incremental config 变成正式契约，而不是实现注释。 |
| E-RS-005 | current_test | strong | explicitly_tracked | `reference-sync`, `reference-sync-runtime-and-state-evidence`, `operator-and-surface-evidence` | 2026-04-19 | `tests/integration/test_reference_derivation.py` 与 `tests/integration/test_publication_service.py` 证明 current accepted slices 已用显式 `reference_derivation -> publication` 链取代 hidden `reference_sync` side effects。 |
| E-RS-006 | current_wiki | supporting | absorbed | `reference-sync-runtime-and-state-evidence`, `reference-sync` | 2026-04-19 | 当前 `reference-sync.md` 已登记 deferred runtime / retained governance truth，但此前 target inventory、incremental state 与 replacement story 仍分散在多页。 |

## 本轮已吸收的稳定结论

- `reference_sync` 通过 explicit target inventory 受治理，而不是作为一个背景 helper 隐身存在。
- `reference_sync` 的 legacy contract 包含 per-table incremental sync-state，不是“每次都无条件 full refresh”。
- `last_synced_at` 不是内部实现细节，而是 operator-facing incremental contract 的一部分。
- current accepted slices 已用显式 `reference_derivation -> publication` 取代 hidden sync runtime side effects。
- 被取代的是 legacy runtime breadth，不是 target inventory、authoritative source mapping 或 sync contract 这层治理记忆。

## 哪些来源是强证

- `E:\Projects\WorkDataHub\config\reference_sync.yml`
- `E:\Projects\WorkDataHub\src\work_data_hub\orchestration\reference_sync_ops.py`
- `E:\Projects\WorkDataHub\src\work_data_hub\io\repositories\sync_state_repository.py`
- `E:\Projects\WorkDataHub\src\work_data_hub\domain\reference_backfill\sync_models.py`
- `tests/integration/test_reference_derivation.py`
- `tests/integration/test_publication_service.py`

## 哪些来源只是旁证

- [引用同步与回填证据](./reference-and-backfill-evidence.md)
- [operator 与 surface 证据](./operator-and-surface-evidence.md)
- [`reference_sync`](../surfaces/reference-sync.md)

## 对象级分发入口

- [`reference_sync`](../surfaces/reference-sync.md)
- [引用同步与回填证据](./reference-and-backfill-evidence.md)
- [operator 与 surface 证据](./operator-and-surface-evidence.md)

## 当前证据缺口

- current repo 没有 repo-native `reference_sync` runtime / state store；因此 current replacement 目前只覆盖 accepted slice runtime，而不是 bootstrap/runtime closure。
- sync-state persistence 的 schema、保留策略与 operator recovery contract 仍未形成更细的对象级 wiki 表达。
- target inventory 与 current publication replacement 现在已有 shared evidence route，但 future bootstrap/runtime plan 仍需要独立 admission，而不是从本页直接外推。

# 引用同步与回填证据

## 结论主题

本页聚合 `reference_sync`、`backfill`、customer-master 衍生写入、authoritative source mapping 与 domain-specific aggregation 相关证据。

## 证据记录

| evidence_id | source_type | evidence_strength | coverage_state | supported_pages | last_verified | notes |
|---|---|---|---|---|---|---|
| E-RB-001 | legacy_doc | strong | absorbed | `backfill`, `reference-sync`, `output-correctness` | 2026-04-16 | `E:\Projects\WorkDataHub\docs\guides\infrastructure\backfill-mechanism-guide.md` 把 reference data strategy 明确分成 pre-load `reference_sync` 与 process-time `backfill` 两层，并把 FK-safe 顺序写成正式约束。 |
| E-RB-002 | legacy_config | strong | absorbed | `backfill`, `annuity-performance`, `annuity-income`, `annual-award`, `annual-loss` | 2026-04-16 | `E:\Projects\WorkDataHub\config\foreign_keys.yml` 为四个域显式声明 FK targets、`depends_on`、`skip_blank_values`、customer-master 衍生字段与 domain-specific aggregation。 |
| E-RB-003 | legacy_code | strong | absorbed | `backfill`, `annuity-performance`, `annuity-income`, `annual-award`, `annual-loss` | 2026-04-16 | `src/work_data_hub/domain/reference_backfill/generic_service.py` 证明 backfill 候选是从 processed fact rows 派生，并通过拓扑排序、blank/temp-id 过滤、tracking fields 与 idempotent write 保护执行边界。 |
| E-RB-004 | legacy_code | strong | absorbed | `backfill`, `output-correctness`, `annuity-performance`, `annuity-income`, `annual-award`, `annual-loss` | 2026-04-16 | `generic_service.py` 与 `models.py` 证明 `max_by`、`concat_distinct`、`template`、`count_distinct`、`lambda`、`jsonb_append` 是真正执行的业务衍生语义，不只是配置注释。 |
| E-RB-005 | legacy_doc | strong | absorbed | `backfill`, `output-correctness`, `annuity-performance`, `annuity-income`, `annual-award`, `annual-loss` | 2026-04-16 | `E:\Projects\WorkDataHub\docs\business-background\客户主数据回填与状态来源分析.md` 明确客户主数据回填、状态规则与快照是三层对象，并把 `年金客户类型` 与 `is_new` 分开。 |
| E-RB-006 | legacy_config | strong | absorbed | `reference-sync`, `backfill` | 2026-04-16 | `E:\Projects\WorkDataHub\config\reference_sync.yml` 显式给出 authoritative source type、schedule、concurrency、batch size、target inventory、`upsert` / `delete_insert` sync contract 与部分 incremental config。 |
| E-RB-007 | legacy_code | strong | absorbed | `reference-sync` | 2026-04-16 | `src/work_data_hub/orchestration/reference_sync_ops.py`、`sync_models.py` 与 `sync_service.py` 证明 legacy `reference_sync` 具有 `plan_only` / `force_full_sync` / `persist_state`、per-table `last_synced_at` state、authoritative tracking fields 与 per-table adapter dispatch。 |
| E-RB-008 | legacy_doc | supporting | absorbed | `annuity-performance`, `annuity-income`, `annual-award`, `annual-loss`, `backfill` | 2026-04-16 | 四份 capability map 共同写实了 customer-master 衍生在不同域中的 weighting column 差异：`期末资产规模`、`固费`、`计划规模`。 |
| E-RB-009 | legacy_config | supporting | absorbed | `reference-sync`, `backfill` | 2026-04-16 | 对照 `foreign_keys.yml` 与 `reference_sync.yml` 可见，同名业务对象不代表同一写入面；例如 plan / organization family 在 backfill 与 authoritative sync 中分别落到不同 schema / column footprint。 |

## 本轮已吸收的稳定结论

- `reference_sync` 与 `backfill` 是同一 reference strategy 下的两层对象，不应再被写成同一条“补齐逻辑”。
- `reference_sync` 负责把 authoritative reference data 预先同步到受治理 target inventory；`backfill` 负责从 processed facts 派生缺失对象与 customer-master signals。
- `backfill` 的输入前提是 canonicalized fact rows，而不是 raw workbook rows；它在 legacy contract 中承担 FK-safe gate，先于事实加载完成。
- `backfill` 不只补 reference keys，还会写 customer-master 级别的 `主拓机构`、`关键年金计划`、`关联计划数`、`关联机构数`、`tags`、`年金客户类型` 等派生结果。
- domain-specific aggregation 是业务语义，不是实现细节：`annuity_performance` 以 `期末资产规模` 选主拓对象，`annuity_income` 以 `固费` 选主拓对象，event domains 以 `计划规模` 形成 customer-master signals。
- `skip_blank_values` 与 `company_id` 的 temp-id 过滤属于稳定语义边界；未解析身份或 `(空白)` 键不应被直接物化成 customer master。
- `reference_sync` 的 authoritative 写入与 backfill 的 auto-derived 写入有不同 provenance：前者标记为 `authoritative` 且默认 `needs_review = false`，后者标记为 `auto_derived` 且 `needs_review = true`。
- 同名业务对象在 `reference_sync` 与 `backfill` 中可能拥有不同的 target schema / column footprint；对象名重合不等于写入面相同。
- `年金客户类型`、event tags 与 customer-master labels 属于 backfill/classification 结果，不应被误写成 snapshot status 本体。

## 哪些来源是强证

- `backfill-mechanism-guide.md`
- `foreign_keys.yml`
- `reference_sync.yml`
- `generic_service.py`、`models.py`、`reference_sync_ops.py`、`sync_service.py`
- `客户主数据回填与状态来源分析.md`

## 哪些来源只是旁证

- 四个 legacy capability map 中对 weighting column 与 customer-master signals 的 field trace
- `io/loader/` 中对 idempotent load / delete-insert / upsert contract 的通用实现细节

## 对象级分发入口

- [回填：`backfill`](../concepts/backfill.md)
- [`reference_sync`](../surfaces/reference-sync.md)
- [operator 与 surface 证据](./operator-and-surface-evidence.md)

## 当前证据缺口

- legacy `reference_sync` 的 sync-state persistence 已在 op/service 层被观察到，但状态表 schema、保留策略与 operator recovery contract 仍未形成对象级 wiki page。
- backfill 写入后的 `_needs_review` closure flow 目前只被 raw code/doc 侧证明，尚未被提升为独立 operator workflow object。
- 同名业务对象在 authoritative sync 与 derived backfill 中的 schema drift 已被识别，但哪些 footprint 应在 current wiki 中被长期保留仍待后续治理裁决。

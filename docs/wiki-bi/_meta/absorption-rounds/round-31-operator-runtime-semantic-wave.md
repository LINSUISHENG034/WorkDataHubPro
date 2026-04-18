# Round 31：operator/runtime semantic wave

> 状态：Completed
> 日期：2026-04-18
> 主题簇：reference strategy layering / reference_sync preload lifecycle / customer_mdm hook-chain

## 本轮目标

- 延续 Round 30 留下的 semantic-map-first discovery 入口，优先深挖 `reference_sync`、`customer_mdm` 与 shared operator/runtime surfaces。
- 不追求一次性扩宽所有 runtime 面，而是只提升已经具备强 primary evidence、且会影响 durable 语义解释的对象。
- 继续保持 execution-first：从调度、hook 链、manual recovery surface 与 config-driven contract 出发，而不是先写一张抽象语义清单再倒找证据。

## 本轮吸收的稳定结论

- `reference_sync` 与 `backfill` 属于同一 reference strategy，但不是同一条“补齐逻辑”；前者是 authoritative pre-load，后者是 processed-fact 之后的 derived write / FK-safe gate。
- `reference_sync` 是独立的 pre-load lifecycle，而不是 domain ETL 的隐藏 side effect。它拥有独立 job、独立 schedule，以及 `state` / `persist_state` / `force_full_sync` 等显式运行控制。
- `annuity_performance` 之后触发的 customer MDM 更新链是稳定的 ordered post-hook chain：`contract_status_sync` → `year_init`（仅 1 月）→ `snapshot_refresh`。
- `customer-mdm sync` 与 `customer-mdm snapshot` 手工命令面仍然重要，但应被解释为 operator recovery surface，而不是默认 primary trigger。
- 本轮新增 4 个 reviewable semantic proposals，且复跑后 immutability 已收敛：
  - `sem-concept-reference-strategy-layering`
  - `sem-non-equivalence-reference-sync-vs-backfill`
  - `sem-lifecycle-reference-sync-preload-cycle`
  - `sem-rule-annuity-performance-post-hook-chain`

## 本轮回写产物

- `legacy-semantic-map` claims
  - `claim-wave-2026-04-17-semantic-governance-reframe-reference-layering`
  - `claim-wave-2026-04-17-semantic-governance-reframe-reference-sync-preload-cycle`
  - `claim-wave-2026-04-17-semantic-governance-reframe-annuity-performance-hook-chain`
- semantic-map canonical outputs / reports
  - `semantic/concepts/sem-concept-reference-strategy-layering.yaml`
  - `semantic/non-equivalences/sem-non-equivalence-reference-sync-vs-backfill.yaml`
  - `semantic/lifecycles/sem-lifecycle-reference-sync-preload-cycle.yaml`
  - `semantic/rules/sem-rule-annuity-performance-post-hook-chain.yaml`
  - `reports/waves/wave-2026-04-17-semantic-governance-reframe/*`

## 有意留在本轮之外的缺口

- `company_lookup_queue` 的 schedule / sensor / queue-depth trigger / stale-processing reset，已确认仍是高价值 runtime surface，但本轮没有把它继续提升成新的独立 semantic rule。
- `reference_sync` 的 state table schema、保留策略与 operator recovery contract 仍停留在 evidence / deferred governance 层，尚未提升为独立 durable object page。
- `customer_mdm` hook chain 的 current-side 最终保留边界仍待治理裁决；当前只能确认 legacy 触发语义稳定，不应提前写成 rebuild 已完全保留。

## 下一步入口

- [`reference_sync`](../../surfaces/reference-sync.md)
- [回填：`backfill`](../../concepts/backfill.md)
- [`customer-mdm` 手工命令面](../../surfaces/customer-mdm-commands.md)
- [引用同步与回填证据](../../evidence/reference-and-backfill-evidence.md)
- [customer MDM 生命周期证据](../../evidence/customer-mdm-lifecycle-evidence.md)
- [客户状态语义正确性](../../standards/semantic-correctness/customer-status-semantics.md)

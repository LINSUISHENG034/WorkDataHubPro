# operator 与 surface 证据

## 结论主题

本页聚合 queue、reference sync、manual commands、operator artifacts、enterprise persistence 等 surface 相关证据。

## 证据记录

| evidence_id | source_type | evidence_strength | coverage_state | supported_pages | last_verified | notes |
|---|---|---|---|---|---|---|
| E-SF-001 | audit | strong | absorbed | `company-lookup-queue`, `reference-sync`, `customer-mdm-commands`, `failed-record-export` | 2026-04-14 | `2026-04-12-legacy-code-audit.md` 明确 queue、reference sync、manual commands、operator artifacts 与 enterprise persistence 都是显式 surface。 |
| E-SF-002 | audit | strong | absorbed | `failed-record-export`, `unknown-names-csv`, `annuity-income` | 2026-04-14 | `2026-04-12-verification-assets-search-findings.md` 把 operator artifacts 与 missing surfaces 提升为治理对象，并把 annuity_income 相关 artifact gap 留为制度记忆。 |
| E-SF-003 | legacy_code | strong | absorbed | `customer-mdm-commands`, `standalone-tooling` | 2026-04-14 | `src/work_data_hub/cli/__main__.py` 直接暴露 `customer-mdm`、`cleanse`、`eqc-gui`、`eqc-gui-fluent`、`intranet-deploy-gui` 等独立 CLI / GUI 入口，说明这些对象不是隐形 helper。 |
| E-SF-004 | legacy_config | strong | absorbed | `reference-sync`, `backfill` | 2026-04-14 | `config/reference_sync.yml` 明确 schedule、concurrency、batch size、target schema/table、source type 与 `sync_mode`，说明 reference sync 是配置治理 surface，而不是泛化 backfill。 |
| E-SF-005 | legacy_code | strong | absorbed | `company-lookup-queue`, `enterprise-enrichment-persistence` | 2026-04-14 | `resolver/backflow.py` 与 `repository/other_ops.py` 明确 temp-id 之后会向 `enterprise.enrichment_requests` enqueue，采用 `pending` / `processing` 去重与 graceful degradation。 |
| E-SF-006 | legacy_code | strong | absorbed | `enterprise-enrichment-persistence`, `standalone-tooling`, `company-lookup-queue` | 2026-04-14 | `eqc_provider.py`、EQC GUI controller 与 enrichment repository 共同说明 `enterprise.enrichment_index`、`enterprise.base_info`、former-name writes 与 GUI optional persistence 构成共享 persistence surface。 |
| E-SF-007 | legacy_doc | supporting | absorbed | `customer-mdm-commands`, `reference-sync`, `standalone-tooling` | 2026-04-14 | `deployment_run_guide.md` 把 `customer-mdm` 手工补跑、GUI 环境变量与 operator-facing command path 写成正式运行指引。 |
| E-SF-008 | current_spec | strong | explicitly_tracked | `company-lookup-queue`, `reference-sync`, `enterprise-enrichment-persistence`, `customer-mdm-commands`, `standalone-tooling` | 2026-04-15 | `2026-04-11-workdatahubpro-refactor-program.md` 与 first-wave legacy coverage matrix 把 `company_lookup_queue`、`reference_sync`、enterprise persistence、manual commands 与 shared artifacts 显式登记为 deferred cross-cutting tracks，而不是隐含 runtime。 |
| E-SF-009 | current_test | strong | explicitly_tracked | `reference-sync`, `backfill` | 2026-04-15 | `tests/integration/test_reference_derivation.py` 与 `tests/integration/test_publication_service.py` 证明 current repo 已用显式 `reference_derivation -> publication` 链取代 accepted slices 中对 hidden reference-sync side effects 的依赖。 |
| E-SF-010 | current_code | supporting | explicitly_tracked | `company-lookup-queue`, `enterprise-enrichment-persistence` | 2026-04-15 | `src/work_data_hub_pro/capabilities/identity_resolution/service.py` 当前采用 `source_value -> cache_hit -> provider_lookup -> temp_id_fallback` 的同步治理链，且 repo 中不存在 `enrichment_requests`、`enrichment_index`、`base_info` 等 repo-native runtime surface。 |
| E-SF-011 | current_test | supporting | explicitly_tracked | `company-lookup-queue`, `unknown-names-csv`, `failed-record-export`, `annuity-income` | 2026-04-15 | `tests/integration/test_annuity_income_operator_artifacts.py` 证明 unresolved identity 当前会被外显到 `unknown_names_csv` 与 failed-record artifacts，而不是被当前 repo 的 async lookup queue 吞掉。 |
| E-SF-012 | current_reference_asset | supporting | explicitly_tracked | `business-collection-ledger-workbook`, `business-collection-workbook-variants-evidence`, `annual-award`, `annual-loss` | 2026-04-15 | representative single-month production-sample validation 显示 business-collection ledger workbook 与相邻 summary workbook 共同构成 `业务收集` workbook family；写回内容仅限 workbook metadata 与 sheet names，raw workbook path 不作为 durable wiki 引用对象。 |
| E-SF-013 | current_runbook | supporting | explicitly_tracked | `failed-record-export`, `unknown-names-csv`, `customer-mdm-commands` | 2026-04-16 | `docs/runbooks/annuity-income-replay.md` 把 operator artifact visibility 明确写成 replay run 目标之一，说明 artifact 不是实现副作用，而是可验证的运行面义务。 |

## 本轮已吸收的稳定结论

- `reference_sync` 不是普通 helper，而是带有明确 target inventory、source mode 与 sync contract 的独立 runtime / integration surface
- `reference_sync` 的 target inventory、incremental sync-state 与 current replacement story 现在已有对象级 evidence route，不再只停留在 shared decision table
- `failed-record export` 不是普通 debug 输出，而是 operator artifact
- manual `customer-mdm` commands 不是 hook 的副产品，而是独立 operator surface，并且 deployment guide 暴露了手工 recovery / recompute 路径
- manual `customer-mdm` runtime boundary 现在已有独立 evidence route，可直接回答 legacy operator surface、primary-vs-recovery trigger 与 current deferred boundary
- `enterprise.enrichment_index`、`enterprise.enrichment_requests`、`enterprise.base_info` 共同构成 identity 相关 persistence surface，不能长期隐身
- enterprise persistence family 现在已有独立 evidence route，可直接回答 cache/queue persistence、provider-retention root 与 downstream normalized persistence 的 layering
- `company_lookup_queue` 不是模糊的 fallback 细节，而是 temp-id 之后的异步补查运行面，带有 dedup 与 graceful degradation 语义
- standalone `cleanse` CLI 与多种 GUI 工具是 operator-adjacent tooling family，应显式登记，但不应自动提升为 rebuild 核心边界
- surface 主题最容易被“当前主线只关注 fact domain”掩盖，因此必须显式登记
- current accepted validation slices 已经用显式 `reference_derivation + publication` 取代 hidden reference-sync side effects；被替代的是 legacy runtime surface，不是 target inventory 与 source-of-truth contract
- current accepted validation slices 没有 repo-native async lookup queue；被 accepted 的是同步 identity chain、temp-id fallback 与 operator-visible unresolved artifacts，而不是 legacy queue orchestration
- shared unresolved-name / failed-record artifacts 现在已有独立 evidence dispatcher，可直接解释 queue deferred 之后由什么来承接 operator-visible consequence
- enterprise persistence 不应再被当作一整团“identity 附属表”；更合理的 closure 方式是把 cache、queue persistence、provider raw/cleansed persistence 分别判断是否处于 active runtime
- 对 first-wave validation runtime 来说，`reference_sync`、`company_lookup_queue` 与 enterprise persistence 的 runtime breadth 都不属于 active retained surface；它们要么已经被更显式的 flow 替代，要么仍保持 deferred
- `业务收集` workbook reality 现在已从“聊天里提到过的文件夹记忆”升级为显式 surface/evidence topic
- business collection ledger workbook 的 surface 宽度明显大于 `annual_award` / `annual_loss` 任一单独 accepted contract

## 哪些来源是强证

- legacy code / CLI dispatch / persistence repository
- legacy code audit
- refactor program 与 first-wave coverage matrix
- current reference-derivation / publication tests

## 哪些来源只是旁证

- deployment guide
- current identity-resolution code path
- income-specific operator artifact tests

## 聚合页 dispatcher 边界

- 本页继续承载 surface family 的 shared decision package，尤其是 queue、reference sync、manual commands、operator artifacts 与 enterprise persistence 之间的边界关系。
- 已经形成稳定独立对象的 surface，应优先分发到对应 surface page，而不是在本页重复承载完整对象叙述。
- shared unresolved-name / failed-record family 现在已有对象级 evidence page；本页只保留其与 queue deferred、identity surface 和 current replacement story 的聚合裁决。

## operator / runtime / verification 治理口径

- operator surface 必须同时回答三个问题：谁触发、输出落到哪里、失败后由谁消费；缺一项即不应宣称“已闭环”。
- runtime surface 的 retain / replace / defer 必须与 current accepted slices 的真实保护方式一一对应，避免把 legacy breadth 误写成 current active runtime。
- verification surface 只负责“如何证明”与“证据路径”；不替代 runtime design，也不替代 operator runbook。
- 聚合页只维护 shared adjudication memory；对象级生命周期决策应落在独立 surface page。

## 当前治理裁决

| 对象 | retain | replace | defer | retire |
|---|---|---|---|---|
| `reference_sync` | 保留 target inventory、authoritative source mapping、sync contract 这层治理记忆 | accepted slices 已由显式 `reference_derivation -> publication` 取代 hidden sync side effects | daily schedule、sync-state persistence、独立 runtime operator flow 继续 deferred | retire “reference data 会随 fact ETL 自然覆盖”的隐含假设 |
| `company_lookup_queue` | 保留 async lookup / dedup / retry / graceful degradation 作为独立治理问题 | current validation runtime 以同步 identity chain + temp-id fallback + unresolved artifacts 替代 queue runtime | queue persistence、retry orchestration、schedule/sensor operator flow 继续 deferred | retire “当前 accepted runtime 已含 queue”的表述 |
| enterprise cache / queue / provider persistence | 保留“这些对象曾是独立 persistence surface”的制度记忆 | current validation runtime 以 cache interface、evidence refs、artifact visibility 替代 legacy table footprint | durable cache、queue persistence、provider raw/cleansed persistence 继续 deferred | retire “identity 附属表默认属于当前 active runtime”的假设 |

## 对象级补强页

- [enterprise enrichment persistence](../surfaces/enterprise-enrichment-persistence.md)
- [enterprise enrichment persistence 证据](./enterprise-enrichment-persistence-evidence.md)
- [standalone tooling](../surfaces/standalone-tooling.md)
- [reference_sync](../surfaces/reference-sync.md)
- [`reference_sync` runtime and state 证据](./reference-sync-runtime-and-state-evidence.md)
- [引用同步与回填证据](./reference-and-backfill-evidence.md)
- [`company_lookup_queue`](../surfaces/company-lookup-queue.md)
- [`customer-mdm` manual runtime 证据](./customer-mdm-manual-runtime-evidence.md)
- [business collection ledger workbook](../surfaces/business-collection-ledger-workbook.md)
- [business collection workbook variants 证据](./business-collection-workbook-variants-evidence.md)
- [unresolved-name and failed-record 证据](./unresolved-name-and-failed-record-evidence.md)
- [`annuity_income` operator artifacts 证据](./annuity-income-operator-artifacts-evidence.md)

## 当前证据缺口

- shared unresolved-name / failed-record artifact parity 仍未完成 cross-domain closure；当前已有 shared evidence dispatcher，但 accepted artifact contract 仍只有 `annuity_income`
- standalone tooling family 已被显式登记，但 retain / retire / defer 边界仍待后续治理决策
- manual `customer-mdm` commands 现在已有对象级 evidence route，但每条命令的 retain / replace / retire 边界仍待后续治理决策
- `业务收集` 目录下相邻 workbook variants 的多月稳定性与最终 surface catalog 仍待更多样本验证
- 本仓库未携带 legacy `src/work_data_hub/*` 与 `docs/guides/validation/*` 原始路径，当前对 legacy runtime breadth 的表述依赖既有 audit 产物；若后续需要对象级 closure，需补充可复核的原始证据映射

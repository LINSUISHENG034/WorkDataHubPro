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
| E-SF-008 | audit | supporting | open_question | `company-lookup-queue`, `reference-sync`, `failed-record-export`, `customer-mdm-commands`, `enterprise-enrichment-persistence`, `standalone-tooling` | 2026-04-14 | retain / replace / retire 仍有未决部分，但 Round 11 已将这些问题收敛成可单独治理的对象簇。 |

## 本轮已吸收的稳定结论

- `reference_sync` 不是普通 helper，而是带有明确 target inventory、source mode 与 sync contract 的独立 runtime / integration surface
- `failed-record export` 不是普通 debug 输出，而是 operator artifact
- manual `customer-mdm` commands 不是 hook 的副产品，而是独立 operator surface，并且 deployment guide 暴露了手工 recovery / recompute 路径
- `enterprise.enrichment_index`、`enterprise.enrichment_requests`、`enterprise.base_info` 共同构成 identity 相关 persistence surface，不能长期隐身
- `company_lookup_queue` 不是模糊的 fallback 细节，而是 temp-id 之后的异步补查运行面，带有 dedup 与 graceful degradation 语义
- standalone `cleanse` CLI 与多种 GUI 工具是 operator-adjacent tooling family，应显式登记，但不应自动提升为 rebuild 核心边界
- surface 主题最容易被“当前主线只关注 fact domain”掩盖，因此必须显式登记

## 哪些来源是强证

- legacy code / CLI dispatch / persistence repository
- legacy code audit

## 哪些来源只是旁证

- deployment guide
- open-question level audit synthesis

## Round 11 对象级补强页

- [enterprise enrichment persistence](../surfaces/enterprise-enrichment-persistence.md)
- [standalone tooling](../surfaces/standalone-tooling.md)

## `annuity_income` 对象级补强页

- [`annuity_income` operator artifacts 证据](./annuity-income-operator-artifacts-evidence.md)

## 当前证据缺口

- `reference_sync` 的 replace 形态仍未形成稳定结论
- `enterprise enrichment persistence` 内部的 cache / queue / provider persistence 分层仍未完全收口
- standalone tooling family 已被显式登记，但 retain / retire / defer 边界仍待后续治理决策
- `annuity_income` artifact detail 已拆出，但 cross-domain artifact parity 仍未闭合

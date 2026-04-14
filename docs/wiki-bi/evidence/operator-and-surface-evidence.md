# operator 与 surface 证据

## 结论主题

本页聚合 queue、reference sync、manual commands、operator artifacts、enterprise persistence 等 surface 相关证据。

## 证据记录

| evidence_id | source_type | evidence_strength | coverage_state | supported_pages | last_verified | notes |
|---|---|---|---|---|---|---|
| E-SF-001 | audit | strong | absorbed | `company-lookup-queue`, `reference-sync`, `customer-mdm-commands`, `failed-record-export` | 2026-04-14 | `2026-04-12-legacy-code-audit.md` 明确 queue、reference sync、manual commands、operator artifacts 与 enterprise persistence 都是显式 surface。 |
| E-SF-002 | audit | strong | absorbed | `failed-record-export`, `unknown-names-csv`, `annuity-income` | 2026-04-14 | `2026-04-12-verification-assets-search-findings.md` 把 operator artifacts 与 missing surfaces 提升为治理对象，并把 annuity_income 相关 artifact gap 留为制度记忆。 |
| E-SF-003 | legacy_code | strong | absorbed | `customer-mdm-commands`, `reference-sync` | 2026-04-14 | legacy CLI dispatch、hooks、customer_mdm modules 直接证明 manual commands 与 reference sync 是独立入口。 |
| E-SF-004 | legacy_config | supporting | absorbed | `reference-sync`, `backfill` | 2026-04-14 | `reference_sync.yml`、`foreign_keys.yml` 体现 sync / backfill 的配置入口、目标表与顺序依赖。 |
| E-SF-005 | audit | supporting | open_question | `company-lookup-queue`, `reference-sync`, `failed-record-export`, `customer-mdm-commands` | 2026-04-14 | retain / replace / retire 仍有未决部分，应继续留在 surface 治理视野中。 |
| E-SF-006 | legacy_doc | supporting | absorbed | `customer-mdm-commands`, `reference-sync`, `company-lookup-queue` | 2026-04-14 | legacy runbooks 与 CLI 文档说明这些 surface 不是单纯内部 helper，而是 operator-facing 能力。 |

## 本轮已吸收的稳定结论

- `reference_sync` 不是普通 helper，而是独立 runtime / integration surface
- `failed-record export` 不是普通 debug 输出，而是 operator artifact
- manual `customer-mdm` commands 不是 hook 的副产品，而是独立 operator surface
- enterprise persistence surfaces 是 queue / enrichment / refresh 的重要组成部分，不能长期隐身
- surface 主题最容易被“当前主线只关注 fact domain”掩盖，因此必须显式登记

## 哪些来源是强证

- legacy code / CLI dispatch
- legacy code audit

## 哪些来源只是旁证

- config summary
- open-question level audit synthesis

## `annuity_income` 对象级补强页

- [`annuity_income` operator artifacts 证据](./annuity-income-operator-artifacts-evidence.md)

## 当前证据缺口

- enterprise persistence surfaces 尚未拆成对象级 evidence page
- GUI / standalone tools 仍未形成明确治理结论
- standalone `cleanse` CLI 仍未形成明确治理结论
- `annuity_income` artifact detail 已拆出，但 cross-domain artifact parity 仍未闭合

# operator 与 surface 证据

## 结论主题

本页聚合 queue、reference sync、manual commands、operator artifacts、enterprise persistence 等 surface 相关证据。

## 证据记录

| evidence_id | source_type | evidence_strength | coverage_state | supported_pages | last_verified | notes |
|---|---|---|---|---|---|---|
| E-SF-001 | audit | strong | absorbed | `company-lookup-queue`, `reference-sync`, `customer-mdm-commands` | 2026-04-14 | `2026-04-12-legacy-code-audit.md` 明确这些对象是显式 runtime / operator surfaces。 |
| E-SF-002 | audit | strong | absorbed | `failed-record-export`, `unknown-names-csv` | 2026-04-14 | `2026-04-12-verification-assets-search-findings.md` 把 operator artifacts 和 missing surfaces 提升为治理对象。 |
| E-SF-003 | legacy_code | strong | legacy_only | `customer-mdm-commands`, `reference-sync` | 2026-04-14 | legacy CLI dispatch、hooks、customer_mdm modules 证明这些 surfaces 真实存在。 |
| E-SF-004 | legacy_config | supporting | legacy_only | `reference-sync`, `backfill` | 2026-04-14 | `reference_sync.yml`、`foreign_keys.yml` 体现 sync / backfill 的配置入口与目标表面。 |
| E-SF-005 | audit | supporting | open_question | `company-lookup-queue`, `reference-sync`, `failed-record-export` | 2026-04-14 | 当前 retain / replace / retire 仍有未决部分，应继续留在 surface 治理视野中。 |

## 哪些来源是强证

- legacy code / CLI dispatch
- legacy code audit

## 哪些来源只是旁证

- config summary
- open-question level audit synthesis

## 当前证据缺口

- enterprise persistence surfaces 尚未拆成对象级 evidence page
- GUI / standalone tools 仍未形成明确治理结论

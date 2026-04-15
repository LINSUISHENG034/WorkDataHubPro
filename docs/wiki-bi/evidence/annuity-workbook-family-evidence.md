# annuity workbook family 证据

## 结论主题

本页聚合 annuity workbook family 的直接证据，重点是“真实生产数据样式经单一月份代表性样本验证后，当前可稳定表达的 workbook metadata / sheet reality”。

## 证据记录

| evidence_id | source_type | evidence_strength | coverage_state | supported_pages | last_verified | notes |
|---|---|---|---|---|---|---|
| E-AWF-001 | legacy_config | strong | absorbed | `input-reality-contracts`, `annuity-performance-input-contract`, `annuity-income-input-contract` | 2026-04-15 | `E:\Projects\WorkDataHub\config\data_sources.yml` 说明 `annuity_performance` 与 `annuity_income` 共用 `data/real_data/{YYYYMM}/收集数据/数据采集`、文件名模式与 `highest_number` 版本策略，但用不同 sheet contract。 |
| E-AWF-002 | current_reference_asset | strong | explicitly_tracked | `annuity-workbook-family-evidence`, `annuity-performance`, `annuity-income` | 2026-04-15 | workbook metadata validated against a representative single-month production sample from the external real-data tree; only workbook metadata and sheet names are written back, the raw workbook path is not used as a durable wiki reference, and the specific month is intentionally not part of the stable conclusion because the value lies in the recurring production data shape. |
| E-AWF-003 | legacy_doc | supporting | absorbed | `annuity-performance`, `annuity-income`, `input-reality-evidence` | 2026-04-15 | `annuity_performance-capability-map.md` 与 `annuity_income-capability-map.md` 都把单 workbook discovery + 单独 sheet ownership 写成 domain capability map，支撑“shared workbook family, separate sheet contracts”这一表达。 |

## 本轮已吸收的稳定结论

- 经单一月份代表性生产样本验证，当前 annuity workbook family 同时包含 `规模明细` 与 `收入明细`
- 这强化了 `annuity_performance` 与 `annuity_income` 共用一个 workbook family、但分别消费不同 sheet 的既有结论
- shared physical workbook does not collapse the two domains into one contract; accepted contract 仍然是按 sheet 分开的 domain-specific contract

## 哪些来源是强证

- `E:\Projects\WorkDataHub\config\data_sources.yml`
- representative single-month production-sample validation of annuity workbook metadata

## 哪些来源只是旁证

- `annuity_performance-capability-map.md`
- `annuity_income-capability-map.md`

## 当前证据缺口

- 当前只有“单一月份代表性生产样本验证”被写回，尚未形成多月 workbook-family variance 视角
- 本页只写 workbook metadata 与 sheet names，不承载 row-level 或 field-level production payload

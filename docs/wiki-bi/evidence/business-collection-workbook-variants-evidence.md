# business collection workbook variants 证据

## 结论主题

本页聚合 business-collection workbook variants 的直接证据，重点是“真实生产数据样式经单一月份代表性样本验证后，当前可稳定表达的台账 workbook 与相邻 summary workbook 现实”。

## 证据记录

| evidence_id | source_type | evidence_strength | coverage_state | supported_pages | last_verified | notes |
|---|---|---|---|---|---|---|
| E-BCWV-001 | legacy_config | strong | absorbed | `input-reality-contracts`, `annual-award-input-contract`, `annual-loss-input-contract` | 2026-04-15 | `E:\Projects\WorkDataHub\config\data_sources.yml` 说明 `annual_award` 与 `annual_loss` 的 accepted contract 都指向 `data/real_data/{YYYYMM}/收集数据/业务收集`，并把 `*台账登记*.xlsx` 视为 event-domain file pattern。 |
| E-BCWV-002 | current_reference_asset | strong | explicitly_tracked | `business-collection-workbook-variants-evidence`, `annual-award`, `annual-loss` | 2026-04-15 | workbook metadata validated against a representative single-month production sample from the external business-collection real-data tree; only workbook metadata and sheet names are written back, the raw workbook path is not used as a durable wiki reference, and the specific month is intentionally not part of the stable conclusion because the value lies in the recurring production data shape. |
| E-BCWV-003 | current_reference_asset | strong | explicitly_tracked | `business-collection-workbook-variants-evidence`, `business-collection-ledger-workbook`, `operator-and-surface-evidence` | 2026-04-15 | adjacent summary-workbook metadata validated against the same representative single-month production sample; only workbook metadata and sheet names are written back, and the wiki records the workbook kind rather than a month-specific raw path. |
| E-BCWV-004 | legacy_doc | supporting | absorbed | `annual-award-input-contract`, `annual-loss-input-contract`, `business-collection-ledger-workbook` | 2026-04-15 | `annual_award-capability-map.md` 与 `annual_loss-capability-map.md` 把 `业务收集` workbook family 的双 sheet accepted contract 写成 multi-sheet merged read reality，但并未把相邻 workbook 自动提升为 domain contract。 |

## 本轮已吸收的稳定结论

- 经单一月份代表性生产样本验证，business-collection ledger workbook contains the accepted event-domain sheets and many adjacent sheets
- 经同一类样本验证，business-collection folder 还存在相邻 summary workbook，其 sheet names 与 accepted event-domain contract 明显不同，例如 `表1 受托考核加扣分反馈` 与 `表2 投资考核加扣分反馈`
- these adjacent workbooks should be treated as observed production variants or adjacent operator reality unless stronger evidence admits them into an accepted contract

## 哪些来源是强证

- `E:\Projects\WorkDataHub\config\data_sources.yml`
- representative single-month production-sample validation of business-collection workbook metadata
- representative single-month production-sample validation of adjacent summary-workbook metadata

## 哪些来源只是旁证

- `annual_award-capability-map.md`
- `annual_loss-capability-map.md`

## 当前证据缺口

- 当前只写回“单一月份代表性生产样本验证”这一层，尚未确认相邻 summary / attachment workbook 在多月中的稳定性
- 本页仍停留在 observation/evidence duty，不直接裁定哪些相邻 workbook 将来会进入 retained operator surface catalog

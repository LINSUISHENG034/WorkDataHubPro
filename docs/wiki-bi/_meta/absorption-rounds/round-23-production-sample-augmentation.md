# Round 23: production-sample augmentation

> 状态：Completed
> 日期：2026-04-15
> 主题簇：input-reality / production-sample / operator-surface

## 本轮目标

- 用 legacy sources 与单一月份代表性生产样本验证补强 wiki 对真实生产数据形态的表达
- 把 accepted contract 与 observed production variants 明确分层
- 把台账型 workbook、汇总型 workbook 与相邻 sheet 现实升级成显式治理对象

## Raw Sources

- `E:\Projects\WorkDataHub\config\data_sources.yml`
- `E:\Projects\WorkDataHub\docs\domains\annuity_performance-capability-map.md`
- `E:\Projects\WorkDataHub\docs\domains\annuity_income-capability-map.md`
- `E:\Projects\WorkDataHub\docs\domains\annual_award-capability-map.md`
- `E:\Projects\WorkDataHub\docs\domains\annual_loss-capability-map.md`
- representative single-month production sample metadata validation for annuity workbook family
- representative single-month production sample metadata validation for business-collection ledger workbook
- representative single-month production sample metadata validation for adjacent summary workbook

## Exit Criteria

- concrete workbook-family and workbook-variant evidence exists as durable pages
- four first-wave domain pages can answer “real production data currently looks like what” with bounded, sourced statements
- adjacent operator workbooks are no longer left as unnamed context outside the wiki

## Stable Findings Absorbed

- representative single-month production-sample validation shows the annuity workbook family currently exposes both `规模明细` and `收入明细` in one physical workbook while keeping domain-specific sheet contracts separate
- representative single-month production-sample validation shows the business-collection ledger workbook is a real workbook-level object that contains the accepted event-domain sheets and many adjacent operator-facing sheets
- the same validation also shows an adjacent summary workbook with different sheet names, which should stay at observed-variant / surface level unless stronger evidence promotes it
- workbook metadata from external production samples can be written back as bounded evidence when the wiki records that only workbook metadata and sheet names were copied and the raw workbooks remain outside the repository

## Reusable Maintenance Lessons

- object-level workbook evidence should land in `evidence/` before downstream contract and domain pages are tightened
- workbook-variant observation pages and surface-governance pages should not carry the same responsibility
- one observed month can strengthen explainability and workbook discovery guidance without redefining a universal input contract, and the durable wiki should retain the validated shape rather than the month-specific raw path

## Next Entry Points

- `evidence/input-reality-evidence.md`
- `evidence/business-collection-workbook-variants-evidence.md`
- `standards/verification-method/real-data-validation.md`

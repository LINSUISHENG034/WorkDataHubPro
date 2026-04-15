# business collection ledger workbook

## Surface Object

`台账登记v1.xlsx` 是 `业务收集\V1` 目录中的 workbook-level operator surface。

它不是单一 domain 的中性容器，而是一个把 event-domain sheets、adjacent operator sheets 与目录级制度记忆聚在一起的运行对象。

## Why It Is A Surface Instead Of A Domain Contract

- `annual_award` 与 `annual_loss` 的 accepted contract 只各自认领其中一部分 sheet contract
- 同一本 workbook 里还存在 `数据源`、`历史数据`、`续签客户清单`、`企年受托战客`、`企年投资战客` 等相邻 sheet
- 因此 “business collection workbook” 的 runtime / operator object 明显宽于任一单独 event-domain contract

## Observed Production Reality

- `台账登记v1.xlsx` is not just a neutral container; it is a workbook-level operator surface with multiple adjacent sheets
- the presence of adjacent sheets means “business collection workbook” is a broader runtime/operator object than either single event-domain contract
- summary workbooks in the same folder should be classified here or in evidence first, not auto-admitted into event-domain input contracts

## Relationship To `annual_award` And `annual_loss`

- `annual_award` 的 accepted contract 仍是 `企年受托中标(空白)` + `企年投资中标(空白)` 这一 bounded sheet subset
- `annual_loss` 的 accepted contract 仍是 `企年受托流失(解约)` + `企年投资流失(解约)` 这一 bounded sheet subset
- observed production reality 说明它们当前共享一个更宽的台账 workbook surface，但这不等于 accepted contract 被 ledger workbook 整体吞并

## Non-Goals

- 不在本页重复 `business-collection-workbook-variants-evidence.md` 中完整 sheet inventory
- 不在本页把相邻 summary workbook 直接判为 accepted domain source
- 不在本页把一个观测月份上升成 universal contract

## Key Evidence

- [business collection workbook variants 证据](../evidence/business-collection-workbook-variants-evidence.md)
- [operator 与 surface 证据](../evidence/operator-and-surface-evidence.md)
- [`annual_award` 输入合同](../standards/input-reality/annual-award-input-contract.md)
- [`annual_loss` 输入合同](../standards/input-reality/annual-loss-input-contract.md)

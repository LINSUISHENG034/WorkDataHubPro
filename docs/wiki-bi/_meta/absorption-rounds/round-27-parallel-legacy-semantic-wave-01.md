# Round 27：legacy 语义补强收口

> 状态：Completed
> 日期：2026-04-16
> 主题簇：领域语义 / operator 与 verification 补强

## 本轮覆盖对象

- `annuity_performance`
- `annuity_income`
- `annual_award`
- `annual_loss`
- operator / runtime / verification 相关 shared pages

## 本轮收口的稳定结论

- 四个高流量 domain 继续保持薄导航页形态，但已经具备更完整的合同级入口与对象级证据回链。
- `annuity_income` 的隐藏字段语义、operator-visible differences 与 current contract posture 已被收紧到输入/输出合同与字段处理证据页。
- `annual_award` / `annual_loss` 的 event-domain 输入、输出与字段处理语义继续保持对称，不再只依赖薄导航页的碎片记忆。
- `annuity_performance` / `annuity_income` / event domains 与 shared evidence pages 之间的 cross-link 现在更接近“对象页先承载结论，domain 页只做分发”的形态。
- operator、runtime 与 verification 相关 shared pages 继续把未闭环项留在 `当前证据缺口`，而不是把 legacy breadth 写成 current active runtime。

## 本轮回写页

- [`annuity_performance`](../../domains/annuity-performance.md)
- [`annuity_income`](../../domains/annuity-income.md)
- [`annual_award`](../../domains/annual-award.md)
- [`annual_loss`](../../domains/annual-loss.md)
- [operator 与 surface 证据](../../evidence/operator-and-surface-evidence.md)
- [验证资产证据](../../evidence/verification-assets-evidence.md)
- [validation result history 证据](../../evidence/validation-result-history-evidence.md)

## 下一步入口

- [`annuity_income` 输入合同](../../standards/input-reality/annuity-income-input-contract.md)
- [`annual_award` 输入合同](../../standards/input-reality/annual-award-input-contract.md)
- [`annual_loss` 输入合同](../../standards/input-reality/annual-loss-input-contract.md)
- [operator 与 surface 证据](../../evidence/operator-and-surface-evidence.md)

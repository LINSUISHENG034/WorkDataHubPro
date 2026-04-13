# Round 04：验证资产

> 状态：Completed
> 日期：2026-04-14
> 主题簇：verification-assets

## 本轮目标

- 强化 verification asset taxonomy 与角色边界
- 明确 legacy-only 高价值资产、current accepted replay baselines 与缺口之间的关系
- 把 error-case fixtures 与 `annuity_income` 的验证资产缺口显式保留下来

## 使用的 raw sources

- `docs/superpowers/audits/2026-04-12-verification-assets-search-findings.md`
- `docs/superpowers/audits/verification-asset-candidates.json`
- `E:\Projects\WorkDataHub\tests\fixtures\golden_dataset\curated\dataset_requirements.md`
- `E:\Projects\WorkDataHub\docs\verification_guide_real_data.md`
- `reference/verification_assets/phase2-accepted-slices.json`
- `docs/wiki-cn/governance/verification-assets.md`

## 本轮吸收的 Stable Findings

- verification asset 是治理对象，不是测试附件
- `dataset_requirements.md` 是高价值 legacy-only 资产
- `verification_guide_real_data.md` 是 operator-facing verification evidence guide
- current project 的 accepted replay baselines 已形成 registry，但没有替代全部 legacy verification assets
- error-case fixtures 当前更准确的状态是 `planned but not created`
- `annuity_income` 的验证资产制度记忆必须保留

## 本轮更新的目标页

- `evidence/verification-assets-evidence.md`
- `standards/verification-method/real-data-validation.md`
- `standards/verification-method/golden-scenarios.md`
- `domains/annuity_income.md`

## 可复用经验

- validation 主题很容易被“current project 已有 replay baselines”遮蔽，因此必须同时写出 legacy richness 和 current accepted scope
- `planned but not created` 这种状态如果不显式写出来，最容易在后续轮次中消失
- `annuity_income` 的价值在验证资产主题中更容易被看见，而不必等到实现开始才讨论

## 下一轮建议

下一轮应优先进入：

- [operator 与 surface 证据](../../evidence/operator-and-surface-evidence.md)
- [reference_sync](../../surfaces/reference-sync.md)
- [failed-record export](../../surfaces/failed-record-export.md)
- [customer-mdm 手工命令面](../../surfaces/customer-mdm-commands.md)

目标是把 reference sync、failed-record export、enterprise persistence 与 operator commands 进一步闭环成第五轮主题。

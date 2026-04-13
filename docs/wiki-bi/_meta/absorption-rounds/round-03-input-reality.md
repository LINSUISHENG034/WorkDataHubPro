# Round 03：输入现实

> 状态：Completed
> 日期：2026-04-14
> 主题簇：input-reality

## 本轮目标

- 强化真实输入形态、目录/版本策略、sheet contract 与 fixture 边界
- 明确 multi-sheet event domain 是系统级输入现实
- 保留 `annuity_income` 的输入现实制度记忆，避免因未实现而丢失

## 使用的 raw sources

- `E:\Projects\WorkDataHub\docs\verification_guide_real_data.md`
- `E:\Projects\WorkDataHub\config\data_sources.yml`
- `E:\Projects\WorkDataHub\tests\fixtures\golden_dataset\curated\dataset_requirements.md`
- `docs/superpowers/audits/2026-04-12-verification-assets-search-findings.md`

## 本轮吸收的 Stable Findings

- real-data sample 与 synthetic fixture 必须严格区分
- 输入现实不只是 workbook 文件，还包括目录、版本选择、sheet contract 与命名策略
- `annual_award` / `annual_loss` 的 multi-sheet intake 是系统级现实，不是边缘特例
- `verification_guide_real_data.md` 兼具输入现实与验证方法桥梁角色
- `annuity_income` 即使尚未在 rebuild 实现，其输入现实仍应作为制度记忆保留

## 本轮更新的目标页

- `evidence/input-reality-evidence.md`
- `standards/input-reality/input-reality-contracts.md`
- `concepts/plan-type.md`
- `domains/annual_award.md`
- `domains/annual_loss.md`
- `domains/annuity_income.md`

## 可复用经验

- 输入现实主题最容易被“当前 fixture 形状”误导，因此必须优先使用 config、real-data guide 和 dataset requirements 三类强证
- 目录结构与版本策略不是纯技术细节，而是输入合同的一部分
- 对尚未实现的 domain，应优先保留制度记忆，而不是等实现后再补

## 下一轮建议

下一轮应优先进入：

- [验证资产证据](../../evidence/verification-assets-evidence.md)
- [real-data validation](../../standards/verification-method/real-data-validation.md)
- [golden scenarios](../../standards/verification-method/golden-scenarios.md)

目标是把 golden set、replay baseline、error-case fixture、validation history 与 verification guide 进一步闭环成第四轮主题。

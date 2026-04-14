# Round 12：verification result history and fixture governance

> 状态：Completed
> 日期：2026-04-14
> 主题簇：follow-on / verification assets / result history

## 本轮目标

- 把 validation result history 从“legacy 目录里有一些结果文件”推进到显式 evidence object
- 收紧 `error_case_fixture`、`golden_set`、`real_data_sample` 的 `deferred` / `planned but not created` 治理语义
- 把 `annual_award` / `annual_loss` 的 validation governance 从“模糊 open question”推进到“已登记但未物化”的清楚状态

## 使用的 raw sources

- `E:\Projects\WorkDataHub\tests\fixtures\golden_dataset\curated\dataset_requirements.md`
- `E:\Projects\WorkDataHub\docs\verification_guide_real_data.md`
- `E:\Projects\WorkDataHub\docs\guides\validation\legacy-parity-validation.md`
- `E:\Projects\WorkDataHub\tests\fixtures\validation_results\`
- `reference/verification_assets/phase2-accepted-slices.json`
- `reference/historical_replays/`
- `docs/runbooks/phase2-verification-assets.md`
- `tests/integration/test_phase2_event_intake_validation.py`
- `tests/integration/test_phase2_intake_validation.py`
- 现有 `wiki-bi` 中与 verification assets 相关页面

## 本轮吸收的 Stable Findings

- validation result history 是独立治理对象，不应被 replay baseline、golden baseline 或单次测试结论吞并
- legacy 已明确把 parity result outputs 写成标准目录与多种报告格式，这说明“结果记忆”曾经是正式资产，而不是一次性工作痕迹
- current project 已通过 Phase 2 asset registry 把多类资产写成显式状态模型；这意味着 `deferred` 应被理解为“已登记但尚未物化”
- accepted slices 当前的 error-path coverage 仍主要靠 inline tests，而不是 repo-native error-case fixture 文件
- `annual_award` / `annual_loss` 的 `golden_set` / `golden_baseline` 目前更准确的语义是“显式 deferred”，而不是完全未决

## 本轮更新的目标页

- `docs/wiki-bi/evidence/verification-assets-evidence.md`
- `docs/wiki-bi/evidence/validation-result-history-evidence.md`
- `docs/wiki-bi/standards/verification-method/golden-scenarios.md`
- `docs/wiki-bi/standards/verification-method/real-data-validation.md`
- `docs/wiki-bi/domains/annual-award.md`
- `docs/wiki-bi/domains/annual-loss.md`
- `docs/wiki-bi/index.md`

## 可复用经验

- 当 current project 已经把资产状态写成显式 registry 时，wiki 不应继续沿用“open question / missing”这种更模糊的说法
- validation history 最容易被误当成临时产物，但它其实承担 adjudication memory、explainability provenance 与 later-governance input 的角色
- “inline tests 保护 failure path” 与 “repo-native error-case fixture 已存在” 是两种不同治理状态，必须明确区分

## 下一轮建议

- 进入 Round 13，继续收紧 identity governance，重点处理 `temp-id`、mapping files、fallback chain 与 queue / cache / provider 边界

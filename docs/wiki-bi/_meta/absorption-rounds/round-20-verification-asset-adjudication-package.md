# Round 20：verification asset adjudication package

> 状态：Completed
> 日期：2026-04-15
> 主题簇：maintenance / verification assets / adjudication

## 本轮目标

- 把 `golden_set`、`golden_baseline`、`error_case_fixture`、`real_data_sample` 的治理状态收紧为更可执行的裁决表达
- 判断 `annual_award` / `annual_loss` 是否需要继续维持“显式 deferred”的 domain-level golden-set 语义，还是应升级为更具体的后续要求
- 把 legacy validation result corpus 与 current registry 之间的关系收束成 current adjudication memory，而不只是“legacy 有结果、current 有登记”

## 启动理由

- [验证资产证据](./../../evidence/verification-assets-evidence.md) 仍把 error-case fixture 列为高优先级缺口
- [validation result history 证据](./../../evidence/validation-result-history-evidence.md) 已确认 legacy result corpus 存在，但 current adjudication-facing durable package 仍未形成
- [golden scenarios](./../../standards/verification-method/golden-scenarios.md) 已有 taxonomy，但 asset state 仍偏“知道有问题”，还不够“知道下一步怎么裁决”

## 使用的 raw sources

- `reference/verification_assets/phase2-accepted-slices.json`
- `reference/historical_replays/`
- `docs/runbooks/phase2-verification-assets.md`
- `E:\Projects\WorkDataHub\docs\guides\validation\legacy-parity-validation.md`
- `E:\Projects\WorkDataHub\tests\fixtures\validation_results\`
- `E:\Projects\WorkDataHub\tests\fixtures\golden_dataset\curated\dataset_requirements.md`
- `tests/contracts/test_phase2_verification_assets.py`
- `tests/integration/test_phase2_event_intake_validation.py`
- `tests/integration/test_phase2_intake_validation.py`
- `src/work_data_hub_pro/governance/compatibility/gate_runtime.py`

## 本轮吸收的 Stable Findings

- Phase 2 accepted slices 当前的 active protection story 已经明确，是 `replay_baseline + synthetic_fixture + checkpoint_baseline`，不应再被含糊写成“只有 replay”
- `golden_set`、`golden_baseline`、`real_data_sample` 当前都应继续保持显式 `deferred`；它们是治理目标，不是已经存在的 repo-native assets
- error-case fixture 的最准确表达不是“已存在”也不是“仍未拍板”，而是“显式 deferred，且当前由 inline failure-path tests 部分保护”
- `annual_award` / `annual_loss` 的 domain-level `golden_set` / `golden_baseline` 目前不应升级成 `planned`，因为 current repo 还没有 admitted broader scenario pack
- legacy validation result corpus 当前应被保留为 provenance 与 adjudication input；current repo 虽已有 registry、checkpoint baselines 与 comparison-run package schema，但尚未吸收出 repo-native comparison-run corpus

## 本轮更新的目标页

- `docs/wiki-bi/evidence/verification-assets-evidence.md`
- `docs/wiki-bi/evidence/validation-result-history-evidence.md`
- `docs/wiki-bi/standards/verification-method/golden-scenarios.md`
- `docs/wiki-bi/standards/verification-method/real-data-validation.md`
- `docs/wiki-bi/domains/annuity-performance.md`
- `docs/wiki-bi/domains/annual-award.md`
- `docs/wiki-bi/domains/annual-loss.md`
- `docs/wiki-bi/index.md`
- `docs/wiki-bi/_meta/absorption-rounds/index.md`
- `docs/wiki-bi/_meta/wiki-absorption-roadmap.md`

## 可复用经验

- 当 manifest 状态模型已经稳定时，wiki 不必再发明新的枚举；更高价值的是把“状态 + 当前保护方式 + 裁决含义”一起写清
- result-history governance 最容易把 “legacy provenance” 与 “current adopted package” 混在一起，最好显式区分 registry、checkpoint baselines、package schema 与 repo-native package corpus
- domain page 只要补一小段“当前验证资产姿态”，就能显著减少读者把 accepted replay protection 误读成更宽 golden governance 的风险

## 下一步建议

- 下一轮应转到 Round 21，继续收口 `reference_sync`、`company_lookup_queue` 与 enterprise persistence 的 retain / replace / retire / defer 边界
- 如果后续实现工作真的需要 repo-native `error_case_fixture`、`golden_set` 或 `real_data_sample`，应进入 slice plan 或 implementation work，而不是把这些缺口继续停留在 aggregate evidence page 里

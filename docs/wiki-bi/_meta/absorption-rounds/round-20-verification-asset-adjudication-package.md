# Round 20：verification asset adjudication package

> 状态：Planned
> 日期：2026-04-15
> 主题簇：planned / verification assets / adjudication

## 本轮目标

- 把 `golden_set`、`golden_baseline`、`error_case_fixture`、`real_data_sample` 的治理状态收紧为更可执行的裁决表达
- 判断 `annual_award` / `annual_loss` 是否需要继续维持“显式 deferred”的 domain-level golden-set 语义，还是应升级为更具体的后续要求
- 把 legacy validation result corpus 与 current registry 之间的关系收束成 current adjudication memory，而不只是“legacy 有结果、current 有登记”

## 启动理由

- [验证资产证据](./../../evidence/verification-assets-evidence.md) 仍把 error-case fixture 列为高优先级缺口
- [validation result history 证据](./../../evidence/validation-result-history-evidence.md) 已确认 legacy result corpus 存在，但 current adjudication-facing durable package 仍未形成
- [golden scenarios](./../../standards/verification-method/golden-scenarios.md) 已有 taxonomy，但 asset state 仍偏“知道有问题”，还不够“知道下一步怎么裁决”

## 计划读取的 raw sources

- `reference/verification_assets/phase2-accepted-slices.json`
- `reference/historical_replays/`
- `docs/runbooks/phase2-verification-assets.md`
- `E:\Projects\WorkDataHub\docs\guides\validation\legacy-parity-validation.md`
- `E:\Projects\WorkDataHub\tests\fixtures\validation_results\`
- `E:\Projects\WorkDataHub\tests\fixtures\golden_dataset\curated\dataset_requirements.md`
- accepted slices 相关 current tests 与 replay assets

## 计划更新的目标页

- `docs/wiki-bi/evidence/verification-assets-evidence.md`
- `docs/wiki-bi/evidence/validation-result-history-evidence.md`
- `docs/wiki-bi/standards/verification-method/golden-scenarios.md`
- `docs/wiki-bi/standards/verification-method/real-data-validation.md`
- 必要时更新 `docs/wiki-bi/domains/annual-award.md`
- 必要时更新 `docs/wiki-bi/domains/annual-loss.md`

## 完成定义

- `golden_set`、`golden_baseline`、`error_case_fixture`、`real_data_sample` 四类对象的状态词不再混用
- `annual_award` / `annual_loss` 的 domain-level golden-set 边界被明确写成 durable 结论，而不是继续停留在模糊 follow-up
- legacy result corpus 是否需要被 current project 显式承接，形成了清楚的裁决语义
- 本轮产出与 Round 19 规则一致：durable pages、`HH:MM` 日志、round note / lint summary 同轮回写

## 后续依赖

- 若本轮收口后仍发现验证资产缺口直接阻塞实现或验收，再把这些缺口交给 slice plan 或 implementation work，而不是继续留在 aggregate evidence page 中

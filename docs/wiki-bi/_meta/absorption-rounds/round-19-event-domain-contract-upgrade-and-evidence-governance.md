# Round 19：event-domain contract upgrade and evidence governance tightening

> 状态：Completed
> 日期：2026-04-15
> 主题簇：maintenance / event-domains / evidence-governance

## 本轮目标

- 把 `annual_award` 与 `annual_loss` 从薄导航页升级到对称的合同级问答入口
- 将 evidence page 的最小模板从“建议”收紧为更明确的治理骨架
- 把 substantial maintenance 的固定产物收束为 durable pages + 时间戳日志 + round note / lint summary
- 继续收紧 identity governance 的 narrative layering

## 使用的 raw sources

- `tests/integration/test_annual_award_intake.py`
- `tests/integration/test_annual_award_processing.py`
- `tests/integration/test_annual_award_plan_code_enrichment.py`
- `tests/replay/test_annual_award_slice.py`
- `docs/runbooks/annual-award-replay.md`
- `src/work_data_hub_pro/capabilities/source_intake/annual_award/service.py`
- `src/work_data_hub_pro/capabilities/fact_processing/annual_award/service.py`
- `src/work_data_hub_pro/capabilities/fact_processing/annual_award/plan_code_lookup.py`
- `tests/integration/test_annual_loss_intake.py`
- `tests/integration/test_annual_loss_processing.py`
- `tests/integration/test_annual_loss_plan_code_enrichment.py`
- `tests/replay/test_annual_loss_slice.py`
- `docs/runbooks/annual-loss-replay.md`
- `src/work_data_hub_pro/capabilities/source_intake/annual_loss/service.py`
- `src/work_data_hub_pro/capabilities/fact_processing/annual_loss/service.py`
- `src/work_data_hub_pro/capabilities/fact_processing/annual_loss/plan_code_lookup.py`
- `tests/integration/test_projection_outputs.py`
- 现有 `docs/wiki-bi/` 中的 event-domain / identity / maintenance meta pages

## 本轮吸收的 Stable Findings

- `annual_award` 与 `annual_loss` 已经具备 current tests、replay assets 与 runbook，不应继续只停留在“event-style domain 导航页”
- event-domain 的对称升级不必先做 implementation-gap audit；当前更高收益的是先把 input / output / field-processing 入口固化
- evidence page 的最小模板应默认包含 `evidence_id`、`source_type`、`evidence_strength`、`coverage_state`、`supported_pages`、`last_verified`、`notes`
- substantial maintenance 不应只留下 durable pages；还应固定留下 `HH:MM` 日志与 round note / lint summary
- identity governance 的叙述必须持续区分 compatibility inventory、active runtime path、retired behavior 与 operator-visible consequence

## 本轮更新的目标页

- `docs/wiki-bi/standards/input-reality/annual-award-input-contract.md`
- `docs/wiki-bi/standards/output-correctness/annual-award-output-contract.md`
- `docs/wiki-bi/evidence/annual-award-field-processing-evidence.md`
- `docs/wiki-bi/standards/input-reality/annual-loss-input-contract.md`
- `docs/wiki-bi/standards/output-correctness/annual-loss-output-contract.md`
- `docs/wiki-bi/evidence/annual-loss-field-processing-evidence.md`
- `docs/wiki-bi/domains/annual-award.md`
- `docs/wiki-bi/domains/annual-loss.md`
- `docs/wiki-bi/standards/input-reality/input-reality-contracts.md`
- `docs/wiki-bi/standards/output-correctness/output-correctness.md`
- `docs/wiki-bi/evidence/input-reality-evidence.md`
- `docs/wiki-bi/evidence/identity-and-lookup-evidence.md`
- `docs/wiki-bi/standards/semantic-correctness/identity-governance.md`
- `docs/wiki-bi/concepts/company-id.md`
- `docs/wiki-bi/_meta/wiki-design.md`
- `docs/wiki-bi/_meta/wiki-domain-upgrade-framework.md`
- `docs/wiki-bi/_meta/wiki-maintenance-lint-checklist.md`
- `docs/wiki-bi/index.md`
- `docs/wiki-bi/_meta/absorption-rounds/index.md`

## 可复用经验

- 对称 domain-upgrade 的真实门槛不是“有没有 legacy 大文档”，而是 current repo 是否已经形成 contract-grade evidence 组合
- event-domain pages 应优先把 workbook + sheet contract、publication targets、plan-code enrichment 与 downstream projection boundary 讲清，而不是先回到实现 gap 审计
- evidence 模板治理最好在“每次触碰 evidence 页时顺手归一”，而不是单独发起一轮只做格式改造
- lint 的制度化关键不是继续堆规则，而是固定本轮产物和写回位置

## 下一步建议

- 后续如果 `annual_award` 或 `annual_loss` 出现 wiki 与 current implementation 的明显漂移，再按 domain-upgrade framework 单独追加 implementation-gap audit
- 后续触碰旧 evidence pages 时，优先把它们逐步收紧到本轮明确的最小模板，而不是一次性批量重写全部历史页

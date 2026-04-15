# Round 18：`annuity_income` domain upgrade and maintenance controls

> 状态：Completed
> 日期：2026-04-15
> 主题簇：maintenance / annuity-income / maintenance-controls

## 本轮目标

- 在现有 domain-upgrade framework 基础上优化维护流程
- 把 `annuity_income` 从“已确认但未对称升级”的 domain 推进到合同级问答能力
- 为后续 round 增加 implementation-evidence 与 lint gate

## 使用的 raw sources

- `E:\Projects\WorkDataHub\docs\domains\annuity_income.md`
- `E:\Projects\WorkDataHub\docs\cleansing-rules\annuity-income.md`
- `E:\Projects\WorkDataHub\config\data_sources.yml`
- `E:\Projects\WorkDataHub\config\foreign_keys.yml`
- `docs/runbooks/annuity-income-replay.md`
- `tests/integration/test_annuity_income_processing.py`
- `tests/integration/test_annuity_income_operator_artifacts.py`
- `tests/replay/test_annuity_income_slice.py`
- 现有 `docs/wiki-bi/` 中的 `annuity_income` domain / evidence / identity pages

## 本轮吸收的 Stable Findings

- `wiki-domain-upgrade-framework` 已经是现有 canonical playbook，应优化而不是平行替换
- `annuity_income` 不只是 confirmed domain，而且已经具备 current tests / replay assets / runbook，足以支撑合同级升级
- implementation-evidence writeback、identity-narrative separation 与 maintenance lint gate 应成为后续维护 round 的固定控制项

## 本轮更新的目标页

- `docs/wiki-bi/_meta/wiki-domain-upgrade-framework.md`
- `docs/wiki-bi/_meta/wiki-maintenance-lint-checklist.md`
- `docs/wiki-bi/standards/input-reality/annuity-income-input-contract.md`
- `docs/wiki-bi/standards/output-correctness/annuity-income-output-contract.md`
- `docs/wiki-bi/evidence/annuity-income-field-processing-evidence.md`
- `docs/wiki-bi/domains/annuity-income.md`
- `docs/wiki-bi/concepts/company-id.md`
- `docs/wiki-bi/standards/semantic-correctness/identity-governance.md`

## 可复用经验

- 维护者发现路径不能只依赖 catalog；首页需要显式暴露 canonical playbook、confirmed domain set 与 lint gate
- 当某个 domain 已经有 current tests / replay assets / runbook 时，应尽快把它从“制度记忆入口”升级到合同级页面
- identity governance 最容易发生 narrative drift，尤其要把 compatibility inventory 与 active runtime path 分层书写

## 下一步建议

- 后续如果继续执行本框架，优先对 `annual_award` 与 `annual_loss` 检查是否也需要补成更对称的 contract-grade page set
- 如果 `annuity_income` 后续出现 current implementation drift，再单独开 implementation-gap audit，而不是把 drift 重新塞回 aggregate evidence page

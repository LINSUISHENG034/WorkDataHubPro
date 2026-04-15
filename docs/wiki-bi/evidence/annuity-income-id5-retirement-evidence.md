# `annuity_income` ID5 retirement 证据

## 结论主题

本页聚合 `annuity_income` 中 ID5 fallback 被显式 retirement 的制度记忆。

## 证据记录

| evidence_id | source_type | evidence_strength | coverage_state | supported_pages | last_verified | notes |
|---|---|---|---|---|---|---|
| E-AI-ID5-001 | legacy_doc | strong | absorbed | `annuity-income`, `company-id`, `temp-id`, `identity-governance`, `annuity-income-gap-evidence` | 2026-04-14 | `E:\Projects\WorkDataHub\docs\cleansing-rules\annuity-income.md` 明确 `CR-011` 属于 legacy-only fallback，迁移中已 dropped，并要求新 pipeline 不得实现。 |
| E-AI-ID5-002 | legacy_doc | supporting | absorbed | `golden-scenarios`, `real-data-validation`, `identity-governance`, `annuity-income` | 2026-04-14 | `E:\Projects\WorkDataHub\docs\guides\validation\legacy-parity-validation.md` 说明 annuity_income parity 要把 ID5 去除视为 intentional difference，而不是 parity failure。 |
| E-AI-ID5-003 | audit | supporting | absorbed | `verification-assets-evidence`, `annuity-income` | 2026-04-14 | `docs/superpowers/audits/2026-04-12-verification-assets-search-findings.md` 把 ID5 retirement 列为 annuity_income 必须保留的 institutional memory。 |
| E-AI-ID5-004 | current_test | strong | explicitly_tracked | `annuity-income`, `verification-assets-evidence`, `golden-scenarios` | 2026-04-14 | `tests/integration/test_annuity_income_operator_artifacts.py` 与 `reference/historical_replays/annuity_income/legacy_identity_resolution_2026_03.json` 共同证明 current project 已把 “不恢复 ID5，只走 temp-id fallback” 变成显式受测行为。 |

## 哪些来源是强证

- `annuity-income` cleansing rules 中对 `CR-011` 的显式说明

## 哪些来源只是旁证

- parity validation guide
- verification-assets audit synthesis

## 本轮已吸收的稳定结论

- ID5 fallback retirement 是显式的历史决策，不是实现细节
- 后续 `annuity_income` slice 只能证明自己保护了 post-ID5 行为，不能把 ID5 作为“补兼容”的临时恢复路径
- parity 验证里出现的 company_id 差异，需要优先按 “是否来自 ID5 removal” 来解释

## 叙述分层

- compatibility inventory / historical memory
  - legacy docs 仍保留 ID5 fallback 曾经存在的痕迹
- active runtime path
  - current project 显式走 temp-id fallback，而不是 account-name ID5 fallback
- retired behavior that must not be reintroduced
  - ID5 recovery path
- operator-visible consequence
  - parity / replay 中的 identity 差异必须先按 ID5 retirement 解释

## 当前实现证据

- `current_test`
  - `tests/integration/test_annuity_income_operator_artifacts.py`
- `current_reference_asset`
  - `reference/historical_replays/annuity_income/legacy_identity_resolution_2026_03.json`
- `current_runbook`
  - `docs/runbooks/annuity-income-replay.md`

## 当前证据缺口

- current project 已有针对 ID5 retirement 的独立测试和 replay baseline
- ID5 removal 与 temp-id fallback 的边界还没有在 current project 中形成独立标准页

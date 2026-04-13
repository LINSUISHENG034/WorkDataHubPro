# 验证资产证据

## 结论主题

本页聚合 golden set、replay baseline、real-data sample、error-case fixture、validation history 等验证资产相关证据。

## 证据记录

| evidence_id | source_type | evidence_strength | coverage_state | supported_pages | last_verified | notes |
|---|---|---|---|---|---|---|
| E-VA-001 | audit | strong | absorbed | `golden-scenarios`, `real-data-validation`, `annuity-income` | 2026-04-14 | `2026-04-12-verification-assets-search-findings.md` 系统化汇总 96 个 candidates，并明确 `dataset_requirements.md`、error-case fixtures、real-data guide、annuity_income gap 等高优先级资产问题。 |
| E-VA-002 | audit | supporting | absorbed | `golden-scenarios` | 2026-04-14 | `verification-asset-candidates.json` 适合作为 asset inventory 的辅助来源，但不应替代 wiki 主结论。 |
| E-VA-003 | legacy_doc | strong | absorbed | `golden-scenarios`, `real-data-validation`, `input-reality-contracts` | 2026-04-14 | `dataset_requirements.md` 定义 golden dataset strategy、scenario taxonomy、real-data principle、identity scenarios 与 error-case fixture 预期。 |
| E-VA-004 | legacy_doc | strong | absorbed | `real-data-validation`, `output-correctness` | 2026-04-14 | `verification_guide_real_data.md` 不只是 runbook，而是 operator-facing verification evidence guide。 |
| E-VA-005 | current_reference_asset | strong | absorbed | `golden-scenarios`, `output-correctness`, `real-data-validation` | 2026-04-14 | `reference/historical_replays/` 与 `reference/verification_assets/phase2-accepted-slices.json` 共同定义当前 accepted replay baselines 与 asset registry。 |
| E-VA-006 | current_reference_asset | supporting | explicitly_tracked | `golden-scenarios` | 2026-04-14 | current replay runbooks 与 phase parity artifacts 说明 rebuild 已有部分验证资产治理，但不足以覆盖 legacy 全部 richness。 |
| E-VA-007 | legacy_only | supporting | open_question | `golden-scenarios`, `annuity-income` | 2026-04-14 | `annual_award` / `annual_loss` 是否需要独立 domain-level golden set 仍未形成显式治理结论。 |
| E-VA-008 | legacy_only | strong | open_question | `golden-scenarios`, `real-data-validation` | 2026-04-14 | error-case fixtures 在 legacy 文档中被明确规划，但实体文件并未创建，应视为 `planned but not created`。 |
| E-VA-009 | legacy_only | strong | absorbed | `annuity-income`, `golden-scenarios` | 2026-04-14 | `annuity_income` 的 capability map、parity history、ID5 retirement decision 与 COMPANY_BRANCH_MAPPING 缺口应作为制度记忆保留。 |

## 本轮已吸收的稳定结论

- validation asset 不是测试附件，而是定义“如何证明正确”的治理对象
- `dataset_requirements.md` 是高价值 legacy-only 资产，不应被当作普通旧文档遗忘
- `verification_guide_real_data.md` 是 operator-facing verification evidence guide，不只是执行说明
- current accepted replay baselines 已经形成 registry，但并没有替代所有 legacy verification assets
- error-case fixtures 当前更准确的状态是 `planned but not created`
- `annuity_income` 的验证资产制度记忆必须保留，不能因为当前未实现而被删除

## 哪些来源是强证

- verification asset search findings
- `dataset_requirements.md`
- `verification_guide_real_data.md`
- current replay baselines 与 accepted-slices registry

## 哪些来源只是旁证

- phase artifacts summary
- runbooks

## 当前证据缺口

- error-case fixtures 仍然是高优先级缺口
- `annuity_income` 的验证资产仍主要停留在 legacy 侧
- current project 仍缺少对 validation result history 的制度化吸收

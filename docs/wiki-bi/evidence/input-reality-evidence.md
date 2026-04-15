# 输入现实证据

## 结论主题

本页聚合与真实输入形态、sheet 结构、fixture 角色、目录命名策略相关的证据。

## 证据记录

| evidence_id | source_type | evidence_strength | coverage_state | supported_pages | last_verified | notes |
|---|---|---|---|---|---|---|
| E-IR-001 | legacy_doc | strong | absorbed | `input-reality-contracts`, `real-data-validation`, `annuity_performance` | 2026-04-14 | `dataset_requirements.md` 明确“Golden Dataset 必须从真实生产数据中筛选，禁止使用模拟数据”，并给出 real_data 目录结构。 |
| E-IR-002 | legacy_doc | strong | absorbed | `real-data-validation`, `output-correctness`, `customer-status-semantics` | 2026-04-14 | `verification_guide_real_data.md` 提供真实数据运行、hook 顺序、状态/快照 SQL 检查与 operator 排障路径。 |
| E-IR-003 | legacy_config | strong | absorbed | `input-reality-contracts`, `annual-award-input-contract`, `annual-loss-input-contract`, `annuity-income-input-contract` | 2026-04-15 | `config/data_sources.yml` 直接定义 base_path、file_patterns、version_strategy、sheet_name / sheet_names，是输入现实合同的一部分。 |
| E-IR-004 | audit | supporting | absorbed | `input-reality-contracts`, `real-data-validation`, `golden-scenarios` | 2026-04-14 | `2026-04-12-verification-assets-search-findings.md` 明确 synthetic fixture 与 real-data sample 的治理边界，以及 annuity_income 的 real-input institutional memory。 |
| E-IR-005 | current_test | supporting | explicitly_tracked | `annuity-income`, `annuity-income-input-contract` | 2026-04-15 | `tests/integration/test_annuity_income_processing.py`、`tests/replay/test_annuity_income_slice.py` 与 `docs/runbooks/annuity-income-replay.md` 表明 annuity_income 输入现实已接回 current replay path；当前缺口不再是“无实现”，而是 asset richness 仍需继续扩展。 |
| E-IR-006 | current_test | strong | explicitly_tracked | `annual-award-input-contract`, `annual-loss-input-contract`, `input-reality-contracts` | 2026-04-15 | `tests/integration/test_annual_award_intake.py` 与 `tests/integration/test_annual_loss_intake.py` 明确双 sheet event domains 的 workbook contract、merged anchor order 与空尾行处理边界。 |

## 本轮已吸收的稳定结论

- real-data sample 与 synthetic fixture 必须严格区分
- 目录结构、版本选择与 sheet contract 属于输入现实的一部分
- `annual_award` / `annual_loss` 的 multi-sheet intake 不是边缘案例，而是系统级现实
- `annual_award` 与 `annual_loss` 现在都已有专门 input contract，不再只停留在 domain 导航页里的泛化描述
- `verification_guide_real_data.md` 不只是 runbook，而是输入现实和验证方法之间的桥梁
- `annuity_income` 的输入现实已接回 current replay path，不再只是 legacy-only 制度记忆
- `annuity_performance` 已具备专门 input contract，可直接回答 workbook / sheet / skeleton 问题

## 哪些来源是强证

- `dataset_requirements.md`
- `verification_guide_real_data.md`
- `data_sources.yml`

## 哪些来源只是旁证

- audit synthesis

## 当前证据缺口

- 当前 `wiki-bi` 还没有把具体 workbook shape / sample 类型拆成对象级 evidence page
- `annuity_income` 的输入现实虽然已有 current path，但 source workbook family 的对象级 evidence 仍可继续细化
- 事件域的 multi-sheet merge 现在已有 contract-grade 页面，但仍未拆成独立对象级 evidence page

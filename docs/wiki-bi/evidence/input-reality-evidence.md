# 输入现实证据

## 结论主题

本页聚合与真实输入形态、sheet 结构、fixture 角色、目录命名策略相关的证据。

## 证据记录

| evidence_id | source_type | evidence_strength | coverage_state | supported_pages | last_verified | notes |
|---|---|---|---|---|---|---|
| E-IR-001 | legacy_doc | strong | absorbed | `input-reality-contracts`, `real-data-validation`, `annuity_performance` | 2026-04-14 | `dataset_requirements.md` 明确“Golden Dataset 必须从真实生产数据中筛选，禁止使用模拟数据”，并给出 real_data 目录结构。 |
| E-IR-002 | legacy_doc | strong | absorbed | `real-data-validation`, `output-correctness`, `customer-status-semantics` | 2026-04-14 | `verification_guide_real_data.md` 提供真实数据运行、hook 顺序、状态/快照 SQL 检查与 operator 排障路径。 |
| E-IR-003 | legacy_config | strong | absorbed | `input-reality-contracts`, `annual_award`, `annual_loss`, `annuity_income` | 2026-04-14 | `config/data_sources.yml` 直接定义 base_path、file_patterns、version_strategy、sheet_name / sheet_names，是输入现实合同的一部分。 |
| E-IR-004 | audit | supporting | absorbed | `input-reality-contracts`, `real-data-validation`, `golden-scenarios` | 2026-04-14 | `2026-04-12-verification-assets-search-findings.md` 明确 synthetic fixture 与 real-data sample 的治理边界，以及 annuity_income 的 real-input institutional memory。 |
| E-IR-005 | audit | supporting | open_question | `annuity-income`, `input-reality-contracts` | 2026-04-14 | `annuity_income` 在 current project 仍缺少 source implementation，但其输入现实不能因未实现而被删除。 |

## 本轮已吸收的稳定结论

- real-data sample 与 synthetic fixture 必须严格区分
- 目录结构、版本选择与 sheet contract 属于输入现实的一部分
- `annual_award` / `annual_loss` 的 multi-sheet intake 不是边缘案例，而是系统级现实
- `verification_guide_real_data.md` 不只是 runbook，而是输入现实和验证方法之间的桥梁
- `annuity_income` 即便尚未在 current project 实现，其输入现实仍属于应保留的制度记忆
- `annuity_performance` 已具备专门 input contract，可直接回答 workbook / sheet / skeleton 问题

## 哪些来源是强证

- `dataset_requirements.md`
- `verification_guide_real_data.md`
- `data_sources.yml`

## 哪些来源只是旁证

- audit synthesis

## 当前证据缺口

- 当前 `wiki-bi` 还没有把具体 workbook shape / sample 类型拆成对象级 evidence page
- `annuity_income` 的输入现实仍主要停留在 legacy 侧证据
- 事件域的 multi-sheet merge 仍未拆成对象级 evidence page

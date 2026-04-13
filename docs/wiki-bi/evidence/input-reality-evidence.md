# 输入现实证据

## 结论主题

本页聚合与真实输入形态、sheet 结构、fixture 角色、目录命名策略相关的证据。

## 证据记录

| evidence_id | source_type | evidence_strength | coverage_state | supported_pages | last_verified | notes |
|---|---|---|---|---|---|---|
| E-IR-001 | legacy_doc | strong | legacy_only | `input-reality-contracts`, `annuity_performance`, `annual_award`, `annual_loss` | 2026-04-14 | `E:\Projects\WorkDataHub\tests\fixtures\golden_dataset\curated\dataset_requirements.md` 定义真实数据优先、scenario taxonomy 与 error-case 预期。 |
| E-IR-002 | legacy_doc | strong | legacy_only | `real-data-validation`, `output-correctness` | 2026-04-14 | `E:\Projects\WorkDataHub\docs\verification_guide_real_data.md` 提供 real-data 验证路径与 SQL 检查思路。 |
| E-IR-003 | legacy_config | strong | explicitly_tracked | `input-reality-contracts`, `annual_award`, `annual_loss` | 2026-04-14 | legacy `config/data_sources.yml` 明确 file discovery、version strategy 与 multi-sheet contract。 |
| E-IR-004 | audit | supporting | absorbed | `input-reality-contracts`, `real-data-validation` | 2026-04-14 | `docs/superpowers/audits/2026-04-12-verification-assets-search-findings.md` 明确 synthetic fixture 与 real-data sample 的治理边界。 |

## 哪些来源是强证

- `dataset_requirements.md`
- `verification_guide_real_data.md`
- `data_sources.yml`

## 哪些来源只是旁证

- audit synthesis

## 当前证据缺口

- 当前 `wiki-bi` 还没有把具体 workbook shape / sample 类型拆成对象级 evidence page
- `annuity_income` 的输入现实仍主要停留在 legacy 侧证据

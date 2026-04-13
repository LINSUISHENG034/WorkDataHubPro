# 身份与补查证据

## 结论主题

本页聚合 `company_id`、temp-id、identity fallback chain、lookup queue、plan-code enrichment 等相关证据。

## 证据记录

| evidence_id | source_type | evidence_strength | coverage_state | supported_pages | last_verified | notes |
|---|---|---|---|---|---|---|
| E-ID-001 | legacy_doc | strong | absorbed | `company-id`, `plan-type`, `annuity-performance`, `annuity-income` | 2026-04-14 | `E:\Projects\WorkDataHub\docs\business-background\年金计划类型与客户名称业务背景.md` 明确“客户名称为空不等于无法识别客户”，并强调多线索识别。 |
| E-ID-002 | legacy_doc | strong | absorbed | `company-id`, `temp-id`, `golden-scenarios` | 2026-04-14 | `dataset_requirements.md` 定义 5-step identity fallback chain、temp-id 格式、determinism 与 lookup 场景。 |
| E-ID-003 | audit | strong | absorbed | `company-lookup-queue`, `unknown-names-csv`, `company-id` | 2026-04-14 | `2026-04-12-legacy-code-audit.md` 明确 queue、enterprise persistence、`unknown_names_csv`、manual operator surfaces 都是真实存在的治理对象。 |
| E-ID-004 | audit | supporting | absorbed | `company-id`, `golden-scenarios`, `annuity-income` | 2026-04-14 | `2026-04-12-verification-assets-search-findings.md` 总结 identity fallback chain、mapping files、annuity_income 身份缺口与 missing artifacts。 |
| E-ID-005 | current_test | supporting | explicitly_tracked | `company-id`, `annual_award`, `annual_loss` | 2026-04-14 | WorkDataHubPro 已有 identity / plan-code enrichment 相关集成测试，说明 rebuild 已显式保护其中一部分。 |

## 本轮已吸收的稳定结论

- `company_id` 识别不应被理解为单字段映射，而是多线索解析
- 单一计划与集合计划会影响身份识别可用线索
- 5-step fallback chain 属于制度记忆，不只是实现细节
- temp-id 是受治理 fallback，不等于正式身份
- `company_lookup_queue` 与 `unknown_names_csv` 都是 identity 主题中的独立 surface / artifact

## 哪些来源是强证

- 业务背景文档
- `dataset_requirements.md`
- legacy code audit 中对 operator/runtime surfaces 的识别

## 哪些来源只是旁证

- verification-assets audit synthesis
- current test coverage notes

## 当前证据缺口

- temp-id、ID1-ID5 mapping files 与 annuity_income 相关身份差异仍未形成对象级 evidence page
- current project 中 identity governance 仍未形成独立标准页

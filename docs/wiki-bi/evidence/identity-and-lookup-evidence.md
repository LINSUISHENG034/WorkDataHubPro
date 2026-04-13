# 身份与补查证据

## 结论主题

本页聚合 `company_id`、temp-id、identity fallback chain、lookup queue、plan-code enrichment 等相关证据。

## 证据记录

| evidence_id | source_type | evidence_strength | coverage_state | supported_pages | last_verified | notes |
|---|---|---|---|---|---|---|
| E-ID-001 | legacy_doc | strong | legacy_only | `company-id`, `plan-type` | 2026-04-14 | `E:\Projects\WorkDataHub\docs\business-background\年金计划类型与客户名称业务背景.md` 说明识别不能依赖单一字段。 |
| E-ID-002 | legacy_doc | strong | legacy_only | `company-id`, `golden-scenarios` | 2026-04-14 | `dataset_requirements.md` 定义 5-step identity fallback chain 与 temp-id 预期。 |
| E-ID-003 | audit | supporting | absorbed | `company-id`, `company-lookup-queue`, `unknown-names-csv` | 2026-04-14 | `2026-04-12-legacy-code-audit.md` 与 `verification-assets-search-findings.md` 共同指出 lookup/runtime/persistence surfaces。 |
| E-ID-004 | current_test | supporting | explicitly_tracked | `company-id`, `annual_award`, `annual_loss` | 2026-04-14 | WorkDataHubPro 已有 identity / plan-code enrichment 相关集成测试，说明该问题在 rebuild 中已被显式保护一部分。 |

## 哪些来源是强证

- 业务背景文档
- `dataset_requirements.md`

## 哪些来源只是旁证

- audit synthesis
- current test coverage notes

## 当前证据缺口

- temp-id、ID1-ID5 mapping files 与 annuity_income 相关身份差异仍未形成对象级证据页

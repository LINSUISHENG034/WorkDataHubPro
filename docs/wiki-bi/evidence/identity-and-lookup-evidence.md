# 身份与补查证据

## 结论主题

本页聚合 `company_id`、temp-id、identity fallback chain、lookup queue、plan-code enrichment 等相关证据。

## 证据记录

| evidence_id | source_type | evidence_strength | coverage_state | supported_pages | last_verified | notes |
|---|---|---|---|---|---|---|
| E-ID-001 | legacy_doc | strong | absorbed | `company-id`, `plan-type`, `annuity-performance`, `annuity-income` | 2026-04-14 | `E:\Projects\WorkDataHub\docs\business-background\年金计划类型与客户名称业务背景.md` 明确“客户名称为空不等于无法识别客户”，并强调多线索识别。 |
| E-ID-002 | legacy_doc | strong | absorbed | `company-id`, `temp-id`, `golden-scenarios` | 2026-04-14 | `dataset_requirements.md` 定义 5-step identity fallback chain、temp-id 格式、determinism 与 lookup 场景。 |
| E-ID-003 | audit | strong | absorbed | `company-lookup-queue`, `unknown-names-csv`, `company-id` | 2026-04-14 | `2026-04-12-legacy-code-audit.md` 明确 queue、enterprise persistence、`unknown_names_csv`、manual operator surfaces 都是真实存在的治理对象。 |
| E-ID-004 | audit | supporting | absorbed | `company-id`, `golden-scenarios`, `annuity-income`, `temp-id` | 2026-04-14 | `2026-04-12-verification-assets-search-findings.md` 总结 identity fallback chain、mapping files、annuity_income 身份缺口与 missing artifacts。 |
| E-ID-005 | current_test | supporting | explicitly_tracked | `company-id`, `annual_award`, `annual_loss` | 2026-04-14 | WorkDataHubPro 已有 identity / plan-code enrichment 相关集成测试，说明 rebuild 已显式保护其中一部分。 |
| E-ID-006 | legacy_doc | strong | absorbed | `annuity-income`, `company-id`, `temp-id` | 2026-04-14 | `annuity-income` cleansing rules 明确 ID5 fallback retirement，不应在 rebuild 中无意恢复。 |
| E-ID-007 | legacy_config | strong | absorbed | `company-id`, `identity-governance` | 2026-04-14 | `config/mappings/company_id/company_id_overrides_plan.yml`、`company_id_overrides_hardcode.yml`、`company_id_overrides_name.yml` 说明 mapping / override family 本身就是 identity governance 的一部分，而不只是实现输入。 |
| E-ID-008 | current_test | strong | explicitly_tracked | `temp-id`, `identity-governance` | 2026-04-14 | `tests/integration/test_temp_identity_policy.py` 与 `tests/integration/test_identity_resolution.py` 明确 current project 已显式保护 deterministic temp identity、opaque fallback、placeholder 归零与 source-value-first 行为。 |
| E-ID-009 | current_code | supporting | explicitly_tracked | `identity-governance`, `company-id`, `temp-id` | 2026-04-14 | `src/work_data_hub_pro/capabilities/identity_resolution/service.py` 说明 current project 当前采用 `source_value -> cache_hit -> provider_lookup -> temp_id_fallback` 的治理链路，并为每次解析写 trace / evidence refs。 |

## 本轮已吸收的稳定结论

- `company_id` 识别不应被理解为单字段映射，而是多线索解析
- 单一计划与集合计划会影响身份识别可用线索
- 5-step fallback chain 属于制度记忆，不只是实现细节
- temp-id 是受治理 fallback，不等于正式身份
- `company_lookup_queue` 与 `unknown_names_csv` 都是 identity 主题中的独立 surface / artifact
- mapping / override files、cache、provider、queue 与 temp-id 一起构成 identity governance，而不是彼此孤立的“小功能”
- current project 已显式保护 deterministic / opaque temp identity 与 source-value-first 行为，Round 13 已把 broader identity governance 提升为独立标准层

## 哪些来源是强证

- 业务背景文档
- `dataset_requirements.md`
- mapping override configs
- current temp-identity / identity-resolution tests
- legacy code audit 中对 operator/runtime surfaces 的识别

## 哪些来源只是旁证

- verification-assets audit synthesis
- current test coverage notes

## `annuity_income` 对象级补强页

- [`annuity_income` branch mapping 证据](./annuity-income-branch-mapping-evidence.md)
- [`annuity_income` ID5 retirement 证据](./annuity-income-id5-retirement-evidence.md)
- [`annuity_income` operator artifacts 证据](./annuity-income-operator-artifacts-evidence.md)

## 当前证据缺口

- temp-id、ID1-ID5 mapping files 与 annuity_income 相关身份差异仍未形成对象级 evidence page
- current project 已有 identity governance 的局部实现与测试，但 queue / cache / provider / mapping 的完整边界仍待持续收紧
- annuity_income 的 branch mapping / ID5 gap 已被拆出，并且已经能接回 broader identity governance 视角

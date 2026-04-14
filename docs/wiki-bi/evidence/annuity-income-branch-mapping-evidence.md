# `annuity_income` branch mapping 证据

## 结论主题

本页聚合 `annuity_income` 中 `COMPANY_BRANCH_MAPPING` manual overrides 的制度记忆，以及它们在 rebuild 中的安放缺口。

## 证据记录

| evidence_id | source_type | evidence_strength | coverage_state | supported_pages | last_verified | notes |
|---|---|---|---|---|---|---|
| E-AI-BM-001 | legacy_doc | strong | absorbed | `annuity-income`, `company-id`, `plan-type`, `annuity-income-gap-evidence` | 2026-04-14 | `E:\Projects\WorkDataHub\docs\cleansing-rules\annuity-income.md` 明确 `机构名称 -> 机构代码` 使用 `COMPANY_BRANCH_MAPPING`，并把 6 个 manual overrides 标记为 `Critical`，要求新实现必须保留。 |
| E-AI-BM-002 | audit | supporting | absorbed | `annuity-income`, `identity-and-lookup-evidence` | 2026-04-14 | `docs/superpowers/audits/2026-04-12-verification-assets-search-findings.md` 把这组 branch mapping gap 提升为 annuity_income 的 first-wave 风险。 |
| E-AI-BM-003 | current_test | strong | explicitly_tracked | `annuity-income`, `annuity-income-gap-evidence` | 2026-04-14 | `config/domains/annuity_income/cleansing.json`、`src/work_data_hub_pro/capabilities/fact_processing/annuity_income/service.py` 与 `tests/integration/test_annuity_income_processing.py` 共同证明 current project 已显式实现并保护 branch mapping overrides。 |

## 哪些来源是强证

- `annuity-income` cleansing rules

## 哪些来源只是旁证

- verification-assets search findings

## 本轮已吸收的稳定结论

- `COMPANY_BRANCH_MAPPING` manual overrides 不是普通数据清洗细节，而是 `annuity_income` 的稳定输入解释合同
- 这组 overrides 不能被“沿用共享 mapping 即可”之类的模糊说法吞掉
- `annuity_income` slice planning 必须显式决定这些 overrides 落在 domain config、shared mapping 还是其他受治理位置

## 当前证据缺口

- current project 已在 validation slice 中显式落地并测试保护这组 overrides
- 后续仍可讨论它们是否应从 domain-local 实现进一步抽到 shared mapping 层

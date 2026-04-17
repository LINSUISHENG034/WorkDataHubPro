# `annuity_income` 专题证据

## 结论主题

本页聚合 `annuity_income` 的专题差异，并把 admission-critical 细节分发到对象级 evidence page。

## 证据记录

| evidence_id | source_type | evidence_strength | coverage_state | supported_pages | last_verified | notes |
|---|---|---|---|---|---|---|
| E-AI-001 | legacy_doc | strong | absorbed | `annuity-income`, `company-id`, `golden-scenarios` | 2026-04-14 | `E:\Projects\WorkDataHub\docs\domains\annuity_income-capability-map.md` 证明 `annuity_income` 是 active legacy domain，且有独立 capability / mechanism / field trace 结构。 |
| E-AI-002 | legacy_doc | strong | absorbed | `annuity-income`, `company-id` | 2026-04-14 | `E:\Projects\WorkDataHub\docs\cleansing-rules\annuity-income.md` 明确 ID5 fallback 在迁移中被 dropped，且 current implementation note 不应重新启用。 |
| E-AI-003 | legacy_doc | strong | absorbed | `annuity-income`, `golden-scenarios`, `real-data-validation` | 2026-04-14 | `E:\Projects\WorkDataHub\docs\guides\validation\legacy-parity-validation.md` 明确 legacy 存在 annuity_income parity validation script 与结果目录。 |
| E-AI-004 | audit | strong | absorbed | `annuity-income`, `verification-assets-evidence`, `operator-and-surface-evidence` | 2026-04-14 | `2026-04-12-verification-assets-search-findings.md` 明确 annuity_income 是唯一未闭合 first-wave domain，且 15 个关键事项都主要停留在 legacy 侧。 |
| E-AI-005 | audit | supporting | absorbed | `annuity-income`, `company-id`, `unknown-names-csv`, `failed-record-export` | 2026-04-14 | `2026-04-12-legacy-code-audit.md` 明确 annuity_income 仍是 active domain，且有 `unknown_names_csv` 和 failed-record export 等 operator artifacts。 |
| E-AI-006 | legacy_doc | supporting | absorbed | `annuity-income`, `plan-type`, `annuity-income-branch-mapping-evidence` | 2026-04-17 | cleansing rules 文档指出的 6 个 COMPANY_BRANCH_MAPPING manual overrides 已在 `annuity-income-branch-mapping-evidence`、current config、processor 与 integration tests 中获得显式安放；本页只保留 dispatcher 级摘要。 |

## 哪些来源是强证

- `annuity_income-capability-map.md`
- `annuity-income.md`
- `annuity-income` cleansing rules
- legacy parity validation guide

## 哪些来源只是旁证

- audits 对缺口的综合总结

## 对象级补强页

- [`annuity_income` branch mapping 证据](./annuity-income-branch-mapping-evidence.md)
- [`annuity_income` ID5 retirement 证据](./annuity-income-id5-retirement-evidence.md)
- [`annuity_income` operator artifacts 证据](./annuity-income-operator-artifacts-evidence.md)

## 本轮已吸收的稳定结论

- `annuity_income` 不能因为早期尚未实现就从 wiki 视野中消失
- ID5 fallback retirement 是必须保留的制度记忆，不应在后续重构中被无意复活
- `annuity_income` 既有验证资产记忆，也有 operator artifact 记忆
- annuity_income 的差异不只是“少一个 domain”，还包括身份、artifact、validation 和 branch mapping 的特殊遗留
- `COMPANY_BRANCH_MAPPING` manual overrides 现已通过对象级 branch-mapping 证据页与 current validation slice 资产显式安放
- 当前 aggregate page 应主要承担 dispatcher 角色，而不是继续承载全部细节

## 当前证据缺口

- current project 已有显式 slice、contract-grade input / output / field-processing 页面、测试、replay assets 与 runbook 承接
- branch mapping manual overrides 的制度记忆已在对象级 evidence page 与 current implementation/test evidence 中获得明确落点
- 当前 remaining follow-on 仅是后续是否把这组 overrides 从 domain-local 实现进一步抽象到更广的 shared mapping governance；这不再是 first-wave absorption blocker

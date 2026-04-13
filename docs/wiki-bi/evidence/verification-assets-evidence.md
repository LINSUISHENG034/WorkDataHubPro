# 验证资产证据

## 结论主题

本页聚合 golden set、replay baseline、real-data sample、error-case fixture、validation history 等验证资产相关证据。

## 证据记录

| evidence_id | source_type | evidence_strength | coverage_state | supported_pages | last_verified | notes |
|---|---|---|---|---|---|---|
| E-VA-001 | audit | strong | absorbed | `golden-scenarios`, `real-data-validation` | 2026-04-14 | `docs/superpowers/audits/2026-04-12-verification-assets-search-findings.md` 系统化汇总了 96 个 candidates。 |
| E-VA-002 | audit | supporting | absorbed | `golden-scenarios` | 2026-04-14 | `docs/superpowers/audits/verification-asset-candidates.json` 适合作为 record 索引原始来源。 |
| E-VA-003 | legacy_doc | strong | legacy_only | `golden-scenarios`, `real-data-validation` | 2026-04-14 | `dataset_requirements.md` 定义 golden dataset strategy、scenario taxonomy 与 error-case 预期。 |
| E-VA-004 | current_reference_asset | strong | explicitly_tracked | `golden-scenarios`, `output-correctness` | 2026-04-14 | `reference/historical_replays/` 是当前项目已经显式治理的 replay baselines。 |
| E-VA-005 | current_reference_asset | supporting | explicitly_tracked | `real-data-validation` | 2026-04-14 | 当前 replay runbooks 与 phase parity artifacts 说明 rebuild 已有部分验证资产治理。 |

## 哪些来源是强证

- verification asset search findings
- `dataset_requirements.md`
- current replay baselines

## 哪些来源只是旁证

- phase artifacts summary
- runbooks

## 当前证据缺口

- error-case fixtures 仍然是高优先级缺口
- `annuity_income` 的验证资产仍主要停留在 legacy 侧

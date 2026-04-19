# enterprise enrichment persistence 证据

## 结论主题

本页聚合 enterprise enrichment persistence family 的证据，重点回答：

- 哪些对象属于 cache / queue persistence
- 哪些对象属于 provider-retention root
- 哪些对象属于 downstream normalized / parsed persistence
- current accepted runtime 为什么仍把这整组表面宽度保持为 `deferred`

## 证据记录

| evidence_id | source_type | evidence_strength | coverage_state | supported_pages | last_verified | notes |
|---|---|---|---|---|---|---|
| E-EEP-001 | legacy_code | strong | absorbed | `enterprise-enrichment-persistence`, `enterprise-enrichment-persistence-evidence`, `identity-and-lookup-evidence` | 2026-04-19 | `E:\Projects\WorkDataHub\src\work_data_hub\infrastructure\enrichment\repository\enrichment_index_ops.py` 说明 `enterprise.enrichment_index` 是受治理的 cache / lookup persistence，而不是临时 scratch state。 |
| E-EEP-002 | legacy_code | strong | absorbed | `enterprise-enrichment-persistence`, `enterprise-enrichment-persistence-evidence`, `identity-and-lookup-evidence` | 2026-04-19 | `E:\Projects\WorkDataHub\src\work_data_hub\infrastructure\enrichment\repository\other_ops.py` 同时定义 `enterprise.enrichment_requests` enqueue persistence 与 `enterprise.base_info` provider-result persistence，证明 queue/cache/root persistence 并不是同一层对象。 |
| E-EEP-003 | legacy_code | strong | absorbed | `enterprise-enrichment-persistence`, `enterprise-enrichment-persistence-evidence` | 2026-04-19 | `E:\Projects\WorkDataHub\src\work_data_hub\infrastructure\enrichment\business_info_repository.py` 与 `biz_label_repository.py` 说明 `business_info` / `biz_label` 是 downstream normalized or parsed persistence，不是 provider-retention root。 |
| E-EEP-004 | legacy_code | supporting | absorbed | `enterprise-enrichment-persistence`, `enterprise-enrichment-persistence-evidence` | 2026-04-19 | `E:\Projects\WorkDataHub\src\work_data_hub\infrastructure\enrichment\data_refresh_service.py` 说明 refresh flow 以 `base_info` 为 provider refresh root，并把 `business_info` cleansing 作为 downstream best-effort integration。 |
| E-EEP-005 | current_spec | strong | explicitly_tracked | `enterprise-enrichment-persistence`, `enterprise-enrichment-persistence-evidence`, `operator-and-surface-evidence` | 2026-04-19 | `docs/superpowers/specs/2026-04-11-workdatahubpro-refactor-program.md` 与 coverage matrix `CT-013` / `CT-014` 都把 cache/queue persistence 与 EQC raw/cleansed persistence 标记为 `deferred` cross-cutting tracks。 |
| E-EEP-006 | current_code | supporting | explicitly_tracked | `enterprise-enrichment-persistence-evidence`, `identity-governance` | 2026-04-19 | `src/work_data_hub_pro/capabilities/identity_resolution/service.py` 当前显式保护的是同步 identity behavior chain：`source_value -> cache_hit -> provider_lookup -> temp_id_fallback`，而不是 repo-native persistence tables。 |
| E-EEP-007 | current_test | supporting | explicitly_tracked | `enterprise-enrichment-persistence-evidence`, `identity-governance` | 2026-04-19 | `tests/integration/test_identity_resolution.py` 与 `tests/integration/test_temp_identity_policy.py` 证明 current accepted runtime 已保护 identity 行为链，但未把 enterprise persistence footprint 提升为 active runtime contract。 |

## 本轮已吸收的稳定结论

- enterprise persistence family 至少分成三层：
  - cache / queue persistence：`enrichment_index`、`company_name_index`、`enrichment_requests`
  - provider-retention root：`base_info`
  - downstream normalized / parsed persistence：`business_info`、`biz_label`
- `base_info` 与 `business_info` / `biz_label` 不是同一层对象；前者更接近 provider-retention root，后者是 downstream business-canonicalized persistence。
- `enrichment_requests` / `enrichment_index` 也不应与 `base_info` 混写，因为一个重点在 queue/cache behavior，另一个重点在 provider-result retention。
- current accepted runtime 证明了 identity behavior chain，但没有 re-admit legacy enterprise persistence footprint。
- 因此这组对象当前应被写成：治理记忆与 layering 已经明确，repo-native runtime 继续 deferred。

## 哪些来源是强证

- `E:\Projects\WorkDataHub\src\work_data_hub\infrastructure\enrichment\repository\enrichment_index_ops.py`
- `E:\Projects\WorkDataHub\src\work_data_hub\infrastructure\enrichment\repository\other_ops.py`
- `E:\Projects\WorkDataHub\src\work_data_hub\infrastructure\enrichment\business_info_repository.py`
- `E:\Projects\WorkDataHub\src\work_data_hub\infrastructure\enrichment\biz_label_repository.py`
- `docs/superpowers/specs/2026-04-11-workdatahubpro-refactor-program.md`
- `docs/superpowers/specs/2026-04-11-workdatahubpro-first-wave-legacy-coverage-matrix.md`

## 哪些来源只是旁证

- `E:\Projects\WorkDataHub\src\work_data_hub\infrastructure\enrichment\data_refresh_service.py`
- `src/work_data_hub_pro/capabilities/identity_resolution/service.py`
- `tests/integration/test_identity_resolution.py`
- `tests/integration/test_temp_identity_policy.py`

## 对象级分发入口

- [enterprise enrichment persistence](../surfaces/enterprise-enrichment-persistence.md)
- [身份与补查证据](./identity-and-lookup-evidence.md)
- [operator 与 surface 证据](./operator-and-surface-evidence.md)

## 当前证据缺口

- cache / queue persistence、provider-retention root、downstream normalized persistence 已分层清楚，但 current-side retain / replace / retire decision 仍未逐表闭环。
- current accepted runtime 已证明 identity behavior chain 不依赖这些 repo-native tables；尚未闭环的是 future persistence-surface decision package，而不是这些对象是否曾在 legacy 存在。
- `company_lookup_queue` 与 enterprise persistence family 仍有交叉，但 queue runtime/retry orchestration 不在本页收口；那是独立 follow-on。

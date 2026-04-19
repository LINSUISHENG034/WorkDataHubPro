# `customer-mdm` manual runtime 证据

## 结论主题

本页聚合 manual `customer-mdm` command surface 的证据，重点回答：

- legacy 中这组命令是否真的是独立 operator surface
- 它们与 `annuity_performance` 成功后自动触发的 hook chain 是什么关系
- current accepted runtime 为什么仍把这组 manual runtime 保持为 `deferred`

## 证据记录

| evidence_id | source_type | evidence_strength | coverage_state | supported_pages | last_verified | notes |
|---|---|---|---|---|---|---|
| E-CMR-001 | legacy_code | strong | absorbed | `customer-mdm-commands`, `customer-mdm-manual-runtime-evidence` | 2026-04-19 | `E:\Projects\WorkDataHub\src\work_data_hub\cli\__main__.py` 明确暴露 `customer-mdm sync`、`snapshot`、`init-year`、`validate`、`cutover` 子命令，说明这不是隐形 helper。 |
| E-CMR-002 | legacy_doc | strong | absorbed | `customer-mdm-commands`, `customer-mdm-manual-runtime-evidence` | 2026-04-19 | `E:\Projects\WorkDataHub\docs\deployment_run_guide.md` 明确给出在 `annuity_performance` 成功执行后手工补跑 `customer-mdm sync` 与 `snapshot` 的 operator 路径，证明 manual commands 是正式 recovery / recompute surface。 |
| E-CMR-003 | legacy_code | strong | absorbed | `customer-mdm-manual-runtime-evidence`, `customer-mdm-lifecycle-evidence`, `customer-mdm-commands` | 2026-04-19 | `E:\Projects\WorkDataHub\src\work_data_hub\cli\customer_mdm\*.py` 与 `E:\Projects\WorkDataHub\src\work_data_hub\customer_mdm\*.py` 共同说明：`sync` / `snapshot` / `init-year` / `cutover` 是 write surfaces，而 `validate` 是 read-only validation surface。 |
| E-CMR-004 | legacy_doc | strong | absorbed | `customer-mdm-manual-runtime-evidence`, `customer-mdm-lifecycle-evidence` | 2026-04-19 | `E:\Projects\WorkDataHub\docs\domains\annuity_performance-capability-map.md` 明确 monthly default path 是 post-ETL hook chain；manual `customer-mdm` commands 作为 recovery path 存在，不应被误写成 primary monthly trigger。 |
| E-CMR-005 | current_spec | strong | explicitly_tracked | `customer-mdm-manual-runtime-evidence`, `customer-mdm-commands`, `operator-and-surface-evidence` | 2026-04-19 | `docs/superpowers/specs/2026-04-11-workdatahubpro-refactor-program.md` 与 coverage matrix `CT-015` 都把 manual `customer-mdm` operator surface 标记为 `deferred`，说明 current accepted runtime 尚未 re-admit 该 surface。 |
| E-CMR-006 | current_code | supporting | explicitly_tracked | `customer-mdm-manual-runtime-evidence` | 2026-04-19 | `src/work_data_hub_pro/apps/etl_cli/main.py` 当前只显式暴露 replay / compatibility CLI surface；repo 中没有对应的 `customer-mdm` manual subcommand surface。 |
| E-CMR-007 | current_test | supporting | explicitly_tracked | `customer-mdm-manual-runtime-evidence`, `customer-mdm-lifecycle-evidence` | 2026-04-19 | `tests/integration/test_projection_outputs.py` 与 replay slices 证明 current accepted runtime 已保护 projection semantics，但这些证据并不等于 manual command surface 已被 admitted。 |

## 本轮已吸收的稳定结论

- legacy manual `customer-mdm` commands 是真实存在的 operator surface，不是 hook path 的副产品。
- `sync`、`snapshot`、`init-year`、`cutover` 属于 write / recompute surfaces；`validate` 属于 read-only validation surface。
- 在 legacy monthly default path 里，更接近 primary trigger 的仍是 `annuity_performance` 成功后的 hook chain；manual commands 更适合被理解为 recovery / recompute path，而不是日常默认触发器。
- current accepted runtime 证明了 projection semantics、contract state 与 snapshot outputs 的行为链，但没有 re-admit repo-native manual `customer-mdm` command surface。
- 因此 manual `customer-mdm` commands 当前应被写成：保留制度记忆与 operator boundary，runtime re-admission 继续 deferred。

## 哪些来源是强证

- `E:\Projects\WorkDataHub\src\work_data_hub\cli\__main__.py`
- `E:\Projects\WorkDataHub\docs\deployment_run_guide.md`
- `E:\Projects\WorkDataHub\src\work_data_hub\cli\customer_mdm\*.py`
- `E:\Projects\WorkDataHub\src\work_data_hub\customer_mdm\*.py`
- `E:\Projects\WorkDataHub\docs\domains\annuity_performance-capability-map.md`
- `docs/superpowers/specs/2026-04-11-workdatahubpro-refactor-program.md`
- `docs/superpowers/specs/2026-04-11-workdatahubpro-first-wave-legacy-coverage-matrix.md`

## 哪些来源只是旁证

- `src/work_data_hub_pro/apps/etl_cli/main.py`
- `tests/integration/test_projection_outputs.py`
- current replay slices

## 对象级分发入口

- [`customer-mdm` 手工命令面](../surfaces/customer-mdm-commands.md)
- [customer MDM 生命周期证据](./customer-mdm-lifecycle-evidence.md)
- [operator 与 surface 证据](./operator-and-surface-evidence.md)

## 当前证据缺口

- 每个 manual command 在 rebuild 中最终 retain / replace / retire 的命运仍未逐条裁决。
- current accepted runtime 已证明 projection semantics，但尚未给 manual `customer-mdm` commands 提供 repo-native operator tests、runbook closure 与 explicit re-admission decision。
- current repo 没有 repo-native manual command surface，这一“未保留”现状已经清楚；真正未闭环的是 future operator-tools decision package，而不是它是否曾在 legacy 存在。

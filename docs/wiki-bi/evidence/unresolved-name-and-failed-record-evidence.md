# unresolved-name and failed-record 证据

## 结论主题

本页聚合 shared unresolved-name / failed-record artifacts 相关证据，重点是：

- `unknown_names_csv`
- failed-record export

目标不是把它们压成同一个 artifact，而是明确：

- `unknown_names_csv` 负责 unresolved identity visibility
- failed-record export 负责 failure-path row visibility
- current accepted runtime 目前只在 `annuity_income` 上显式保护这组 artifact contract

## 证据记录

| evidence_id | source_type | evidence_strength | coverage_state | supported_pages | last_verified | notes |
|---|---|---|---|---|---|---|
| E-UA-001 | legacy_doc | strong | absorbed | `unresolved-name-and-failed-record-evidence`, `annuity-income`, `unknown-names-csv`, `failed-record-export` | 2026-04-18 | `E:\Projects\WorkDataHub\docs\domains\annuity_income-capability-map.md` 把 `unknown_names_csv` 与 failed-record export 一起写成 operator-facing outputs，并明确它们是 service side effect 而不是 fact schema 字段。 |
| E-UA-002 | legacy_doc | strong | absorbed | `unresolved-name-and-failed-record-evidence`, `annuity-income`, `unknown-names-csv` | 2026-04-18 | `E:\Projects\WorkDataHub\docs\cleansing-rules\annuity-income.md` 明确 unresolved cases 可能导出 `unknown_names_csv` 供人工 review。 |
| E-UA-003 | legacy_code | strong | absorbed | `unresolved-name-and-failed-record-evidence`, `annuity-performance`, `unknown-names-csv`, `failed-record-export` | 2026-04-18 | `E:\Projects\WorkDataHub\src\work_data_hub\domain\annuity_performance\service.py` 同时导出 `unknown_names_csv` 与 failed-record CSV，说明这组 artifact 并非 income 私有记忆。 |
| E-UA-004 | legacy_code | strong | absorbed | `unresolved-name-and-failed-record-evidence`, `failed-record-export` | 2026-04-18 | `E:\Projects\WorkDataHub\src\work_data_hub\domain\annual_award\service.py` 会在失败行存在时导出 failed-record CSV，说明 event domains 也保留 failure-path artifact。 |
| E-UA-005 | legacy_code | strong | absorbed | `unresolved-name-and-failed-record-evidence`, `failed-record-export` | 2026-04-18 | `E:\Projects\WorkDataHub\src\work_data_hub\domain\annual_loss\service.py` 会在失败行存在时导出 failed-record CSV，说明 event domains 的 failure visibility 不是偶发现象。 |
| E-UA-006 | current_test | strong | explicitly_tracked | `unresolved-name-and-failed-record-evidence`, `annuity-income`, `unknown-names-csv`, `failed-record-export`, `company-lookup-queue` | 2026-04-18 | `tests/integration/test_annuity_income_operator_artifacts.py`、`tests/contracts/test_annuity_income_replay_assets.py` 与 `tests/replay/test_annuity_income_slice.py` 共同证明 current project 已把 income-specific unresolved-name / failed-record visibility 写成显式 contract。 |
| E-UA-007 | current_runbook | supporting | explicitly_tracked | `unresolved-name-and-failed-record-evidence`, `annuity-income`, `unknown-names-csv`, `failed-record-export` | 2026-04-18 | `docs/runbooks/annuity-income-replay.md` 把 operator artifact visibility 明确写成 replay run 目标之一，说明 artifact 不只是内部副作用。 |

## 本轮已吸收的稳定结论

- legacy breadth 中，`annuity_income` 与 `annuity_performance` 都存在 `unknown_names_csv` 与 failed-record artifact；`annual_award` / `annual_loss` 至少保留 failed-record export。
- `unknown_names_csv` 与 failed-record export 不是同一件事：前者回答 unresolved identity 的人工可见性，后者回答 failure-path row 的 operator 可见性。
- deferred `company_lookup_queue` runtime 不等于 operator-visible consequence 消失；当 queue 不在 current active runtime 中时，artifacts / signal / evidence package 仍需承接这层可见后果。
- current accepted runtime 目前只对 `annuity_income` 显式保护了这组 artifact contract。
- 因此，shared artifact family 现在已有 durable evidence dispatcher，但 cross-domain parity 仍未闭环，不应把 income-specific current evidence误写成全域 active contract。

## 哪些来源是强证

- `E:\Projects\WorkDataHub\docs\domains\annuity_income-capability-map.md`
- `E:\Projects\WorkDataHub\docs\cleansing-rules\annuity-income.md`
- `E:\Projects\WorkDataHub\src\work_data_hub\domain\annuity_performance\service.py`
- `E:\Projects\WorkDataHub\src\work_data_hub\domain\annual_award\service.py`
- `E:\Projects\WorkDataHub\src\work_data_hub\domain\annual_loss\service.py`
- `tests/integration/test_annuity_income_operator_artifacts.py`
- `tests/contracts/test_annuity_income_replay_assets.py`
- `tests/replay/test_annuity_income_slice.py`

## 哪些来源只是旁证

- `docs/runbooks/annuity-income-replay.md`
- `docs/wiki-bi/evidence/operator-and-surface-evidence.md`
- `docs/wiki-bi/evidence/identity-and-lookup-evidence.md`

## 对象级分发入口

- [`company_lookup_queue`](../surfaces/company-lookup-queue.md)
- [`unknown_names_csv`](../surfaces/unknown-names-csv.md)
- [failed-record 导出](../surfaces/failed-record-export.md)
- [`annuity_income` operator artifacts 证据](./annuity-income-operator-artifacts-evidence.md)

## 当前证据缺口

- current project 目前只有 `annuity_income` 具备 accepted artifact contract；`annuity_performance`、`annual_award`、`annual_loss` 的 current-side parity 仍未对象级闭环。
- artifact format 是否必须保持 CSV、是否允许等价结构化格式，以及最小 operator consumption contract 仍待后续治理裁决。
- queue deferred 与 artifact replacement 的 mapping 现在已有共享证据页，但还不是完整 runtime closure；retry / schedule / queue persistence 仍继续 deferred。

# `annuity_income` operator artifacts 证据

## 结论主题

本页聚合 `annuity_income` 的 operator-facing artifacts，重点是 `unknown_names_csv` 与 failed-record export。

## 证据记录

| evidence_id | source_type | evidence_strength | coverage_state | supported_pages | last_verified | notes |
|---|---|---|---|---|---|---|
| E-AI-OA-001 | legacy_doc | strong | absorbed | `annuity-income`, `unknown-names-csv`, `failed-record-export` | 2026-04-14 | `E:\Projects\WorkDataHub\docs\domains\annuity_income-capability-map.md` 把 `unknown_names_csv` 直接列为 `CAP-AI-003` / `FLD-AI-007` 的 operator-facing output，并把 failed-record export 视为 service side effect。 |
| E-AI-OA-002 | legacy_doc | strong | absorbed | `annuity-income`, `unknown-names-csv` | 2026-04-14 | `E:\Projects\WorkDataHub\docs\cleansing-rules\annuity-income.md` 的 Current Implementation Note 明确 unresolved cases 可能导出 `unknown_names_csv` 供人工 review。 |
| E-AI-OA-003 | audit | strong | absorbed | `annuity-income`, `operator-and-surface-evidence`, `failed-record-export` | 2026-04-14 | `docs/superpowers/audits/2026-04-12-legacy-code-audit.md` 识别 `annuity_income` 的 `unknown_names_csv` 与 failed-record CSV 是真实存在的 operator artifacts，而不是临时 debug 输出。 |
| E-AI-OA-004 | current_test | strong | explicitly_tracked | `annuity-income`, `unknown-names-csv`, `failed-record-export`, `operator-and-surface-evidence` | 2026-04-14 | `tests/integration/test_annuity_income_operator_artifacts.py`、`tests/contracts/test_annuity_income_replay_assets.py`、`tests/replay/test_annuity_income_slice.py` 与 `docs/runbooks/annuity-income-replay.md` 共同证明 current project 已把 income-specific artifact visibility 变成显式 contract。 |

## 哪些来源是强证

- `annuity_income` capability map
- `annuity_income` cleansing rules
- legacy code audit

## 哪些来源只是旁证

- verification-assets search findings 对 artifact gap 的追认

## 本轮已吸收的稳定结论

- `annuity_income` 不只是 fact-processing domain，它还有明确的 operator-facing artifact 合同
- `unknown_names_csv` 负责把 unresolved identity 显式暴露给人工治理
- failed-record export 负责把 failure path 从日志层拉到可消费 artifact 层

## 叙述分层

- compatibility inventory / historical memory
  - legacy docs 与 legacy audit 都把 artifacts 当作真实 operator-facing output
- active runtime path
  - current project 已把 artifact visibility 写进 tests、replay 与 runbook
- operator-visible consequence
  - unresolved identity 与 failed record 不再只是内部日志，而是显式消费面

## 当前实现证据

- `current_test`
  - `tests/integration/test_annuity_income_operator_artifacts.py`
  - `tests/replay/test_annuity_income_slice.py`
- `current_reference_asset`
  - `reference/historical_replays/annuity_income/`
- `current_runbook`
  - `docs/runbooks/annuity-income-replay.md`

## 当前证据缺口

- current project 已有显式 runbook、replay assertion 与 targeted tests 来保护这些 artifact
- artifact 形态是否仍是 CSV 可以后续再定，但“必须显式治理”这一点已经稳定

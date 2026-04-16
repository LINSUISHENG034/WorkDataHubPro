# validation result history 证据

## 结论主题

本页聚合 validation result history 相关证据。

它关注的不是“应该用什么资产验证”，而是：

- 历史验证输出是否被保存
- 是否存在可复核的比较结果与差异报告
- current project 是否已经把这些结果记忆制度化登记

## 证据记录

| evidence_id | source_type | evidence_strength | coverage_state | supported_pages | last_verified | notes |
|---|---|---|---|---|---|---|
| E-VRH-001 | legacy_doc | strong | absorbed | `validation-result-history-evidence`, `golden-scenarios`, `real-data-validation` | 2026-04-14 | `docs/guides/validation/legacy-parity-validation.md` 明确把 `tests/fixtures/validation_results/` 定义为标准结果目录，并说明 JSON / Excel / parquet 报告共同构成 parity result history。 |
| E-VRH-002 | legacy_test | strong | absorbed | `validation-result-history-evidence`, `annuity-income`, `golden-scenarios` | 2026-04-14 | `E:\Projects\WorkDataHub\tests\fixtures\validation_results\annuity_income\` 与 `annuity_performance\` 下存在多批 dated 输出，说明 legacy 曾保留可追溯的 validation result history。 |
| E-VRH-003 | current_reference_asset | strong | absorbed | `validation-result-history-evidence`, `golden-scenarios`, `real-data-validation` | 2026-04-15 | `reference/verification_assets/phase2-accepted-slices.json` 明确把 replay_baseline、checkpoint_baseline、golden_set、error_case_fixture、real_data_sample 等状态写成显式 registry，而不是隐式约定。 |
| E-VRH-004 | current_runbook | supporting | explicitly_tracked | `validation-result-history-evidence`, `golden-scenarios` | 2026-04-15 | `docs/runbooks/phase2-verification-assets.md` 把 accepted / deferred / planned / retired 状态模型、checkpoint baselines 与 Phase 2 当前位置写成 current governance runbook。 |
| E-VRH-005 | current_test | supporting | explicitly_tracked | `validation-result-history-evidence`, `real-data-validation` | 2026-04-15 | `tests/integration/test_phase2_event_intake_validation.py` 与 `tests/integration/test_phase2_intake_validation.py` 说明 accepted slices 当前的 error-path coverage 仍主要以内联方式存在，而不是 repo-native error-case fixture 文件。 |
| E-VRH-006 | current_test | strong | explicitly_tracked | `validation-result-history-evidence`, `golden-scenarios` | 2026-04-15 | `tests/contracts/test_phase2_verification_assets.py` 证明 current repo 已显式保护 verification-asset registry 的状态字段、accepted slices 清单与 checkpoint baseline 完整性。 |
| E-VRH-007 | current_code | supporting | explicitly_tracked | `validation-result-history-evidence`, `golden-scenarios`, `real-data-validation` | 2026-04-15 | `src/work_data_hub_pro/governance/compatibility/gate_runtime.py` 已定义 comparison-run package 的固定路径骨架，并对 accepted checkpoint baselines 采用 fail-closed 读取；这说明 current repo 具备 package schema，但尚无 repo-native result corpus。 |

## 本轮已吸收的稳定结论

- validation result history 是独立治理对象，不等于 replay baseline 或 golden baseline 本身
- legacy 不只是“跑过 parity”，而是保留了可复核的结果目录、结构化报告与多次运行记录
- current project 已经把 accepted / deferred 资产状态制度化写入 registry，并为 comparison-run package 预留了固定路径骨架
- accepted checkpoint baselines 已经是 current repo 的 active result-memory 组成部分，但这不等于 legacy 整体 result corpus 已被吸收
- legacy result corpus 当前更适合被表述为 provenance 与 adjudication input，而不是 current repo 已承接的 active package
- `deferred` 表示“显式登记但尚未物化”，不等于“未知”或“已经存在”
- accepted slices 当前的 error-path coverage 主要仍依赖 inline tests，因此 error-case fixture 的治理状态应表达为“显式 deferred”，不是“已实现”

## 哪些来源是强证

- `legacy-parity-validation.md`
- legacy `tests/fixtures/validation_results/`
- `reference/verification_assets/phase2-accepted-slices.json`
- `tests/contracts/test_phase2_verification_assets.py`

## 哪些来源只是旁证

- `docs/runbooks/phase2-verification-assets.md`
- 当前 integration tests 中的 inline failure cases
- `gate_runtime.py` 中的 comparison-run package schema

## Round 20 裁决表达

| 对象 | 当前状态 | 当前裁决含义 | 不应误写成什么 |
|---|---|---|---|
| legacy validation result corpus | legacy 侧保留多批 dated parity outputs | 保留为 provenance 与 adjudication input，必要时为 future package 提供来源 | 不应写成“current repo 已经承接了完整结果包” |
| Phase 2 asset registry | current repo 已登记 accepted / deferred 资产状态 | 它是当前 governance memory 的权威入口之一 | 不应等同于某个具体 comparison report 或历史输出目录 |
| accepted checkpoint baselines | repo-native JSON 已存在并受 gate runtime / contract tests 保护 | 它们是 current active result-memory 的一部分 | 不应被降格成“只是将来可能要加的资产” |
| comparison-run package schema | current code 已定义固定 package 路径 | current repo 已有 durable package contract，可承接未来 comparison artifacts | 不应被误写成“当前已经有 comparison_runs corpus” |
| repo-native comparison-run package | 当前缺失 | 仍是未来可吸收对象，而不是既成事实 | 不应因为有 legacy corpus 或 package schema 就被宣称已存在 |

## operator / runtime / verification 治理口径

- result history 属于 verification governance，不替代 runtime contract，也不替代 operator runbook。
- operator 侧结论必须能回指到具体 comparison package 或 checkpoint baseline；仅保留“通过/失败”口头结论不构成可复核证据。
- runtime 若发生语义变更，必须在 result history 中留下可追溯差异入口；否则不应宣称“兼容性已被证明”。
- 聚合页只维护 history 的裁决语义与 provenance 边界；具体 domain 差异应下沉到 domain evidence 或 replay artifacts。

## 当前证据缺口

- legacy validation result history 仍未形成 current project 的 adjudication-facing durable package
- `annual_award` / `annual_loss` 的 domain-level golden set 仍是显式 deferred，而不是已物化资产
- real-data sample 仍是治理目标，但 current repo 尚无 repo-native sample
- legacy `tests/fixtures/validation_results/` 原始目录在本仓库不可直接读取，当前以 audit 记录作为替代来源；若进入关闭裁决阶段需补充可执行路径级再验证

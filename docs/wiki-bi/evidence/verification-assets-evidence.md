# 验证资产证据

## 结论主题

本页聚合 golden set、replay baseline、real-data sample、error-case fixture、validation history 等验证资产相关证据。

## 证据记录

| evidence_id | source_type | evidence_strength | coverage_state | supported_pages | last_verified | notes |
|---|---|---|---|---|---|---|
| E-VA-001 | audit | strong | absorbed | `golden-scenarios`, `real-data-validation`, `annuity-income` | 2026-04-14 | `2026-04-12-verification-assets-search-findings.md` 系统化汇总 96 个 candidates，并明确 `dataset_requirements.md`、error-case fixtures、real-data guide、annuity_income gap 等高优先级资产问题。 |
| E-VA-002 | audit | supporting | absorbed | `golden-scenarios` | 2026-04-14 | `verification-asset-candidates.json` 适合作为 asset inventory 的辅助来源，但不应替代 wiki 主结论。 |
| E-VA-003 | legacy_doc | strong | absorbed | `golden-scenarios`, `real-data-validation`, `input-reality-contracts` | 2026-04-14 | `dataset_requirements.md` 定义 golden dataset strategy、scenario taxonomy、real-data principle、identity scenarios 与 error-case fixture 预期。 |
| E-VA-004 | legacy_doc | strong | absorbed | `real-data-validation`, `output-correctness` | 2026-04-14 | `verification_guide_real_data.md` 不只是 runbook，而是 operator-facing verification evidence guide。 |
| E-VA-005 | current_reference_asset | strong | absorbed | `golden-scenarios`, `output-correctness`, `real-data-validation`, `validation-result-history-evidence` | 2026-04-15 | `reference/historical_replays/` 与 `reference/verification_assets/phase2-accepted-slices.json` 共同定义当前 accepted replay baselines、checkpoint baselines 与 asset registry。 |
| E-VA-006 | current_reference_asset | supporting | explicitly_tracked | `golden-scenarios` | 2026-04-14 | current replay runbooks 与 phase parity artifacts 说明 rebuild 已有部分验证资产治理，但不足以覆盖 legacy 全部 richness。 |
| E-VA-007 | current_reference_asset | supporting | explicitly_tracked | `golden-scenarios`, `annuity_performance`, `annual-award`, `annual-loss` | 2026-04-15 | `phase2-accepted-slices.json` 把三条 accepted slices 的 `golden_set`、`golden_baseline`、`error_case_fixture` 与 `real_data_sample` 都写成显式 `deferred`，说明 current governance 选择了“登记但不物化”。 |
| E-VA-008 | legacy_doc | strong | absorbed | `golden-scenarios`, `real-data-validation`, `validation-result-history-evidence` | 2026-04-15 | `dataset_requirements.md` 明确规划 error-case fixture family，但 legacy / current 两侧都未物化 repo-native 文件，因此更准确的语义是“legacy 已定义目标，current 仍显式 deferred”，而不是继续停留在 open question。 |
| E-VA-009 | legacy_only | strong | absorbed | `annuity-income`, `golden-scenarios` | 2026-04-14 | `annuity_income` 的 capability map、parity history、ID5 retirement decision 与 COMPANY_BRANCH_MAPPING 缺口应作为制度记忆保留。 |
| E-VA-010 | current_runbook | supporting | explicitly_tracked | `golden-scenarios`, `real-data-validation`, `validation-result-history-evidence` | 2026-04-15 | `docs/runbooks/phase2-verification-assets.md` 把 accepted / deferred / planned / retired 状态模型、checkpoint baselines 与各 slice 的当前保护姿态写成 current governance runbook。 |
| E-VA-011 | current_test | supporting | explicitly_tracked | `golden-scenarios`, `real-data-validation`, `validation-result-history-evidence` | 2026-04-15 | `tests/integration/test_phase2_event_intake_validation.py` 与 `tests/integration/test_phase2_intake_validation.py` 表明 accepted slices 当前的 failure-path coverage 主要以内联 workbook / assertions 存在。 |
| E-VA-012 | current_test | strong | explicitly_tracked | `verification-assets-evidence`, `validation-result-history-evidence`, `golden-scenarios` | 2026-04-15 | `tests/contracts/test_phase2_verification_assets.py` 显式保护 manifest 的状态字段、accepted slices 清单与 checkpoint baseline 注册完整性，说明 current repo 已把 verification-asset registry 变成受测治理对象。 |
| E-VA-013 | current_code | supporting | explicitly_tracked | `verification-assets-evidence`, `validation-result-history-evidence` | 2026-04-15 | `src/work_data_hub_pro/governance/compatibility/gate_runtime.py` 对 accepted checkpoint baselines 采用 fail-closed 读取，并定义 comparison-run package 的固定路径骨架，说明 current project 已有 package schema，但尚未将 legacy result corpus 吸收成现成 repo-native package。 |

## 本轮已吸收的稳定结论

- validation asset 不是测试附件，而是定义“如何证明正确”的治理对象
- `dataset_requirements.md` 是高价值 legacy-only 资产，不应被当作普通旧文档遗忘
- `verification_guide_real_data.md` 是 operator-facing verification evidence guide，不只是执行说明
- current accepted protection story 由 `replay_baseline`、`synthetic_fixture` 与 `checkpoint_baseline` 组成，但这并不等于所有 verification asset 都已经物化
- current registry 已把 `golden_set`、`golden_baseline`、`error_case_fixture`、`real_data_sample` 的缺口写成显式 `deferred`，这比“没有记录”更强，但仍不等于资产已存在
- error-case fixture 当前更准确的裁决语义是“显式 deferred，且已有 inline failure-path coverage”，而不是“已存在 repo-native fixture”或“仍未拍板”
- `annual_award` / `annual_loss` 的 domain-level `golden_set` 与 `golden_baseline` 当前应继续保持显式 `deferred`，而不是升级成 `planned`
- `annuity_income` 的验证资产制度记忆必须保留，不能因为当前未实现而被删除
- validation result history 应被视为独立 evidence object，而不是零散遗留在 parity output 目录中的工作痕迹
- legacy validation result corpus 当前应被保留为 adjudication input 与 provenance，而不是被误写成已经由 current repo 承接的 active package

## 哪些来源是强证

- verification asset search findings
- `dataset_requirements.md`
- `verification_guide_real_data.md`
- current replay baselines 与 accepted-slices registry
- `tests/contracts/test_phase2_verification_assets.py`

## 哪些来源只是旁证

- phase artifacts summary
- runbooks
- `gate_runtime.py` 的 package schema 与 fail-closed baseline loading

## 聚合页 dispatcher 边界

- 本页继续承载 verification asset taxonomy、asset state model 与 cross-slice adjudication memory。
- 已经形成独立结果历史对象的内容，应优先分发到 [validation result history 证据](./validation-result-history-evidence.md)，而不是在本页重复维护整套 result-history 细节。
- domain-specific validation memory 只在仍承担治理入口价值时保留摘要；细节应继续下沉到对象级 evidence page 或 slice-specific page。

## operator / runtime / verification 治理口径

- verification assets 的治理对象是“可复核证明路径”，不是“实现细节列表”。
- operator-facing validation 必须同时声明输入样本类型、检查口径与证据落点；否则只能算执行记录，不能算治理资产。
- runtime 真实保护面与 asset state 必须一致：`accepted` 需有 repo-native 资产与受测入口；`deferred` 仅表示显式登记，不得推断已存在。
- 聚合页只承载 state model 与跨域裁决记忆，具体资产的物化/消费方式必须下沉到标准页或对象页。

## Round 20 裁决表达

| 对象 | manifest 状态 | 当前保护方式 | 当前裁决含义 |
|---|---|---|---|
| `replay_baseline` | `accepted` | repo-native historical replay JSON + replay slice gate | 当前 active protection 的主基线，已用于 accepted slice parity story。 |
| `synthetic_fixture` | `accepted` | replay / intake tests 中的确定性 workbook fixture | 受管验证资产，但不应冒充 real-data sample。 |
| `checkpoint_baseline` | `accepted` | `reference/historical_replays/*/legacy_<checkpoint>_2026_03.json` + fail-closed loader | 当前已被纳入 active gate runtime 的中间检查点资产。 |
| `golden_set` | `deferred` | 无 repo-native asset；仅有 legacy 目标定义与 current registry 登记 | 保持为显式治理目标，不应因为 replay slice 已 accepted 就被暗示为已存在。 |
| `golden_baseline` | `deferred` | 无独立 result corpus；当前只有 replay / checkpoint baselines | 与 replay baseline 是不同对象；在更宽的 curated baseline 被 admitted 前继续维持 `deferred`。 |
| `error_case_fixture` | `deferred` | accepted slices 的 inline failure-path tests | 应表达为“显式 deferred + inline-protected”，而不是“fixture 已存在”。 |
| `real_data_sample` | `deferred` | legacy guide + verification standard 明确要求，但 repo 中无 governed sample | 继续作为治理目标保留；synthetic fixture 与 replay baseline 都不能替代它。 |
| validation result history | 不适用 | legacy result corpus + current registry / runbook / package schema | 当前应被视为 adjudication input 与 provenance；尚未被 current repo 吸收成 repo-native comparison-run package。 |

## 对象级补强页

- [validation result history 证据](./validation-result-history-evidence.md)
- [`annuity_income` ID5 retirement 证据](./annuity-income-id5-retirement-evidence.md)
- [`annuity_income` operator artifacts 证据](./annuity-income-operator-artifacts-evidence.md)

## 当前证据缺口

- repo-native `error_case_fixture` pack 仍不存在；如果后续要提高 failure-path 复用度，应进入 slice plan 或 implementation work，而不是继续让语义停留在模糊状态
- repo-native `golden_set` / `golden_baseline` 仍未被任何 accepted slice admitted；在更宽的 curated scenario pack 成立前，不应回退成“可能已经有”
- `annuity_income` 的验证资产虽然已有对象级 admission evidence，但 dated parity result history 仍主要停留在 legacy 侧
- current project 已经有 explicit registry 与 package schema，但仍缺少对 legacy validation result corpus 的 adjudication-facing 吸收
- 本仓库当前不可直接读取 legacy `dataset_requirements.md` 与 `verification_guide_real_data.md` 原始文件；相关稳定结论基于已吸收 audit 证据，原始路径级再核验仍是待补证事项

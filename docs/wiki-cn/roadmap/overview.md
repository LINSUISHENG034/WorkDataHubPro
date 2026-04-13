# 开发路线图

## 总体路线

当前项目主路线图围绕两个核心验收轴展开：

- 旧项目结果 parity
- 显式、可由 agent 操作的架构

开发不是按“功能堆叠”推进，而是按 phase 渐进推进。

## Phase 总览

### Phase 1：Legacy Capability Mapping & Parity Harness

目标：

- 建立 authoritative 的 legacy-to-pro 映射
- 建立 parity baseline 与首个 must-pass checkpoint

关注点：

- capability mapping
- source-recognition mapping
- rule classification
- parity dataset / golden output
- mismatch severity policy

### Phase 2：Transparent Pipeline Contracts & Parity Gates

目标：

- 把 replay 流程表达为显式 stage contract
- 建立可机器判断的 parity / adjudication gate

关注点：

- 输入、阶段、中间产物、输出契约
- rule evidence contract
- deterministic compare + adjudication
- parity-critical CI gate

### Phase 3：Orchestration Refactor & Failure Explainability

目标：

- 消除多个 replay slice 的重复 orchestration
- 提升失败路径可解释性与 typed diagnostics

关注点：

- 抽取共享 orchestration primitive
- 标准化 error taxonomy
- 改善 agent 入口与诊断体验

当前已确认的治理基线：

- replay 共享边界采用 `shared primitives + explicit per-domain runners`
- failure contract 采用 `typed run report + typed exceptions`
- 入口采用”保留 domain wrapper + 新增 unified replay surface”
- temp-id 采用 legacy-backed 的确定性 opaque 规则，前缀默认 `IN`

详见：

- [Phase 3 决策基线](../governance/phase-3-decisions.md)

### Phase 03.1：Phase 3 治理补口 — truthful failure evidence and diagnose hardening

**状态：** 已完成 (2026-04-13)

Phase 03.1 治理补口解决了 2026-04-13 Phase 3 审核中发现的三个问题：

1. **Truthful failure evidence（已修复）：** 修复了 `build_failure_compatibility_case_payload` helper，替换了旧的 two-branch fallback，使 compatibility-case evidence 与第一个 failed checkpoint 正确对应，涵盖 `fact_processing`、`identity_resolution`、`contract_state` 等所有 checkpoint 类型
2. **Diagnose hardening（已修复）：** 实现了 fail-closed package-path  enforcement（`_resolve_package_path_for_run`），拒绝 manifest 中声明的 escape path 和绝对路径
3. **Typed CLI boundary（已修复）：** 修复了 invalid `comparison_run_id` 的 CLI 处理，现在返回 typed stderr message 和 exit code 1，不再暴露 Python traceback

验证命令：
- `uv run pytest tests/contracts/test_phase3_governance_status_sync.py -v` → `Phase 3 governance status sync contract 验证通过`
- `uv run pytest tests/contracts/test_replay_diagnose_contracts.py -v` → `Diagnose contract 验证通过`

**Phase 3 governance sign-off 已于 2026-04-13 正式闭合。**

相关经验：

- [Phase 3 审核经验：failure explainability 必须落到持久化证据与诊断边界](../lessons/phase-3-governance-review-lessons.md)

### Phase 4：Agent Operations & Governance Hardening

目标：

- 把系统推进到更适合 agent 接管的运维与治理形态

关注点：

- runbook + config contract
- 更强的 lineage 查询能力
- evidence redaction 与治理元数据
- adjudication lifecycle

### Phase 5：Performance Reliability Optimization with Drift Safeguards

目标：

- 在不引入业务漂移的前提下处理性能与可靠性问题

关注点：

- projection / trace 热点优化
- policy/config fail-safe
- 性能收益与 parity 稳定性的联合验证

## 当前阶段位置

当前主线状态已经不再是“准备开始 Phase 1”，也不再是“继续收口 Phase 2”，而是：

- Phase 1 已完成
- Phase 2 implementation 已完成
- Phase 6 已完成，Phase 2 governance sign-off 已闭合

这意味着：

- Phase 2 的治理补口已经不是当前 active implementation target
- 当前 wiki 叙述必须从“Phase 2 还在补口”切换到“Phase 2 已闭环，后续关注应转回 Phase 3 及之后的主线问题”

### 2026-04-13 审核补记

2026-04-13 的治理审查补充了一个需要显式记住的状态差异：

- `.planning/` 当前将 Phase 2 标记为完成
- 当前仓库代码与自动化测试说明 Phase 2 的实现面已经基本闭合
- Phase 6 审核指出的治理补口项已经闭合，尤其是中间 checkpoint 的真实 compare 语义、`source_intake` contract gate 语义、以及 `reference_derivation` / `fact_processing` / `identity_resolution` / `contract_state` 的 accepted baseline 比较路径

因此更准确的当前表述应是：

- Phase 2 implementation：已完成
- Phase 2 governance sign-off：已闭合（2026-04-13），依据是 replay acceptance suite 与 governance contract suite 均已通过，且 Phase 6 verification 已用真实执行结果重写

Phase 6 remediation 已完成项目（2026-04-13）：
- truthfulness: 共享 fail-closed baseline 加载、explicit bootstrap 路径、fact/identity/contract_state 中间 checkpoint 基于 accepted baseline 比较而非自比较
- accuracy: `_build_diff` duplicate-row 计数修正为正确的 multiset 减法语义
- stability: annuity / award / loss 的中间 checkpoint payload 归一化为稳定 compare 形状，避免 run-scoped ID 造成 accepted baseline 漂移
- coverage: contract 测试 `tests/contracts/test_phase2_governance_status_sync.py` 守护 planning/wiki 状态同步

本次闭合使用的验证命令：

- `uv run pytest tests/contracts/test_phase6_gate_runtime.py tests/contracts/test_phase2_governance_status_sync.py -v` → `9 passed`
- `uv run pytest tests/contracts/test_phase2_verification_assets.py -v` → `4 passed`
- `uv run pytest tests/replay/test_phase2_reference_derivation_gates.py tests/replay/test_phase2_event_domain_gates.py tests/replay/test_annuity_performance_slice.py tests/replay/test_annual_award_slice.py tests/replay/test_annual_loss_slice.py -v` → `15 passed`

因此当前更合理的推进判断是：

- 如果目标是治理闭环：Phase 2 已完成，不应继续把“补口叙述”当成当前主线
- 如果目标是实现推进：后续注意力应回到 Phase 3 之后的 replay orchestration、failure explainability、agent operability 与运行时治理
- 进入 Phase 3 前，应先把 replay contract、failure contract、CLI contract、temp-id contract 作为实现 admission 前置条件写清楚

相关经验已沉淀到：

- [Phase 2 审核经验：测试全绿不等于治理闭环](../lessons/phase-2-governance-review-lessons.md)

## 当前开发必记

为了减少在 roadmap、governance、audit 之间来回跳转，当前开发至少先记住下面几条：

- accepted 的三个 slice 只说明验证态 closure 已经建立，不代表 first-wave 已整体完成。
- 当前最明确的未闭合业务域仍是 `annuity_income`；除非出现新的治理决策，后续 breadth work 默认应优先考虑它。
- special orchestration / operator surface 仍是显式治理对象，尤其是 `company_lookup_queue`、`reference_sync`、manual `customer-mdm` commands、shared operator artifacts。
- verification asset 不能混用：`synthetic fixture` 不是 `real-data sample`，历史 parity 结果也不是当前 accepted replay baseline。
- 如果 wiki、audit、legacy 文档与当前规划不一致，legacy behavior 看旧项目代码；rebuild current state 看当前代码、coverage matrix 与 refactor program。

需要展开时，优先看：

- [旧项目审计基线](../governance/legacy-audit-baseline.md)
- [Phase 2 决策基线](../governance/phase-2-decisions.md)
- [Verification Assets](../governance/verification-assets.md)

## Phase 1 已沉淀策略

Phase 1 已经沉淀出几条可继续复用的策略：

- 映射采用“双层映射”：业务能力为主键，stage/function chain 为辅助证据
- 范围采用“一个深样板 + 多个宽注册”
- parity 采用“最终输出 must-match + 关键中间检查点 selective-match”
- 首个 must-pass gate 采用“离线报告 + 人工确认”
- 证据采用“最小证据集先固定，完整 taxonomy 后置”

## 当前阶段性重点

Phase 1 完成后，已沉淀的关键产物包括：

- capability map
- intake-path map
- rule classification
- parity baseline
- mismatch report
- decision log

这些产物不是附属说明，而是 phase 执行系统的一部分。

当前阶段性重点已经转向：

- 明确 replay 的 stage contract
- 建立 deterministic parity / adjudication gate
- 逐步减少 orchestration duplication
- 强化 agent 入口、诊断与治理能力

## Phase 2 已确认决策

截至 2026-04-12，Phase 2 已确认的关键治理方向包括：

- checkpoint 采用分层策略，`reference_derivation` 作为 Wave 2 收口项
- adjudication 采用 `severity + decision_status + precedent_status` 三层模型
- contract strictness 采用“双层策略”：对源数据入口受控宽容，对内部 contract 严格校验
- `source_intake` 的目标基线是 `real-data-style`，当前简化 workbook 只保留为 deterministic test fixture
- CI 采用 PR / merge / nightly 三层 gate
- failed parity gate 采用 comparison-run evidence package，而不是只保留 trace 与单个 case
- `golden set`、`real-data sample`、`synthetic fixture`、`replay baseline` 被明确提升为 verification assets
- 新 phase / 新 slice 进入规划前，需要做一次 `forgotten mechanism sweep`

更详细的治理说明见：

- [Phase 2 决策基线](../governance/phase-2-decisions.md)
- [Verification Assets](../governance/verification-assets.md)

## 后续推进原则

后续各 phase 建议持续遵守下面几条原则：

- 先收敛灰区决策，再拆执行计划
- 设计原则必须落到 schema、artifact、test
- 证据必须尽量来自真实运行，而不是模板
- human gate 只基于可审证据作判断
- validation 文档必须反映真实状态，而不是预期状态

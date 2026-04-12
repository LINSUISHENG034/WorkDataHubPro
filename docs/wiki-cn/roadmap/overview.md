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

当前主线状态已经不再是“准备开始 Phase 1”，而是：

- Phase 1 已完成
- 当前推荐推进目标为 Phase 2

原因是：

- Phase 1 已经完成 acceptance baseline、mapping、rule classification 和首个离线 parity checkpoint
- 下一步的主要价值不再是继续补 Phase 1 文档，而是把 parity 与可解释性推进到显式 stage contract 和 deterministic gate

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

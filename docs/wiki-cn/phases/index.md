# 阶段索引

> 按 phase 聚合当前已经沉淀的路线、决策、审查经验与阶段间衔接信息
> 当前策略：先用索引聚合 phase 知识；当单个 phase 累积出持续性的状态、决策和验收摘要，再拆独立页面

## Phase 1

- [开发路线图](../roadmap/overview.md)
  Phase 1 的目标、成功标准与其在整体路线图中的位置。
- [GSD Lesson: 计划与证据要同样可执行](../lessons/planning-and-evidence.md)
  沉淀 Phase 1 计划审查与 parity checkpoint 审核经验。

## Phase 2

- [Phase 2 决策基线](../governance/phase-2-decisions.md)
  固定 checkpoint taxonomy、adjudication、contract strictness、CI 与 evidence package 基线。
- [Verification Assets](../governance/verification-assets.md)
  固定 Phase 2 起适用的 verification asset taxonomy 与 registry 口径。
- [Phase 2 审核经验：测试全绿不等于治理闭环](../lessons/phase-2-governance-review-lessons.md)
  沉淀 truthful gate、baseline 强依赖与 implementation / governance sign-off 分层经验。

## Phase 3

- [Phase 3 决策基线](../governance/phase-3-decisions.md)
  固定 replay 共享边界、failure contract、agent 入口与 temp-id policy。
- [Phase 3 审核经验：failure explainability 必须落到持久化证据与诊断边界](../lessons/phase-3-governance-review-lessons.md)
  沉淀 persisted evidence truthfulness、diagnose fail-closed 与状态合同经验。
- [开发路线图](../roadmap/overview.md)
  包含 Phase 03.1 remediation 与当前 Phase 3 governance sign-off 的闭合语境。

## Phase 4 及后续

- [开发路线图](../roadmap/overview.md)
  当前下一步规划目标已经转向 Phase 4；待出现稳定决策页或 lesson 后再单独接入本索引。

## 后续扩展规则

- 当某个 phase 已同时形成“当前状态 + 已确认决策 + 可复用经验 + 进入/退出条件”时，新增独立 `phase-xx.md`
- 如果某个 phase 的 durable knowledge 持续增长，再拆 `phases/phase-xx/` 子目录
- 新增 phase 页面后，必须同时回写 `index.md` 与 `log.md`

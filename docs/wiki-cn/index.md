# WorkDataHubPro Wiki CN

> 中文项目 wiki 根索引
> 作用：作为 content-oriented catalog，先给出全量 durable page 入口，再按主题深入
> 维护规则：新增或重写稳定页面时，同时更新本页与 `log.md`

## 项目总览

- [项目背景](./project/background.md)
  项目定位、能力边界、当前状态、主要约束与风险。
- [开发路线图](./roadmap/overview.md)
  主路线图、Phase 目标、当前阶段位置与近期推进判断。
- [阶段索引](./phases/index.md)
  按 phase 聚合当前已经沉淀的决策页、审查经验与阶段间衔接页。

## 治理知识

- [治理索引](./governance/index.md)
  治理页总入口，汇总 parity、evidence、verification asset 与 legacy surface 相关页面。
- [Phase 2 决策基线](./governance/phase-2-decisions.md)
  固定 checkpoint taxonomy、adjudication、contract strictness、CI 与 evidence package 的治理基线。
- [Phase 3 决策基线](./governance/phase-3-decisions.md)
  固定 replay 共享边界、failure contract、agent 入口与 temp-id policy。
- [Verification Assets](./governance/verification-assets.md)
  定义 verification asset taxonomy、状态口径与当前 registry 语义。
- [旧项目审计基线](./governance/legacy-audit-baseline.md)
  固定 first-wave legacy surfaces、operator artifacts 与 verification gap 的治理结论。

## 经验沉淀

- [GSD Lesson: 计划与证据要同样可执行](./lessons/planning-and-evidence.md)
  沉淀 Phase 1 计划审查与 parity checkpoint 审核经验。
- [Phase 2 审核经验：测试全绿不等于治理闭环](./lessons/phase-2-governance-review-lessons.md)
  沉淀 truthful gate、baseline 强依赖、implementation 与 governance sign-off 分层经验。
- [Phase 3 审核经验：failure explainability 必须落到持久化证据与诊断边界](./lessons/phase-3-governance-review-lessons.md)
  沉淀 persisted evidence truthfulness、diagnose trust boundary 与 status sync contract 经验。

## 维护与元信息

- [变更日志](./log.md)
  append-only 时间线，记录 wiki 的新增、重构、同步与 lint。
- [本仓库 Wiki 维护约定](./_meta/wiki-maintenance.md)
  说明 `WorkDataHubPro` 如何把 `LLM Wiki` 模式落到当前仓库的 source、wiki、schema 与 lint 工作流。
- [LLM Wiki 说明](./_meta/llm-wiki.md)
  当前 wiki 维护思想来源；用于对照抽象模式，而不是替代本仓库约定。

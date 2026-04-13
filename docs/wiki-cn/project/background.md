# 项目背景

## 项目是什么

`WorkDataHubPro` 是对旧项目 `E:\Projects\WorkDataHub` 的 brownfield rebuild。目标不是推倒重来，也不是仅做目录重排，而是在保留旧项目已验证业务结果的前提下，重建一套更清晰、可解释、可验证、可维护、可由 agent 接管的系统。

## 核心价值

在不牺牲旧项目业务结果一致性的前提下，把数据处理流程重构为：

- 可解释
- 可验证
- 可维护
- 可由 agent 接管

## 当前重构方向

当前项目采用 capability-first 架构，而不是沿用旧项目中更隐式、更高耦合的 hook-centric 或 generic-service-centric 结构。主边界为：

- `capabilities/`
- `platform/`
- `governance/`
- `apps/`

这意味着：

- 业务语义应主要落在 `capabilities/`
- 发布、存储、追踪、契约等运行时职责放在 `platform/`
- 裁决、证据索引、兼容性治理放在 `governance/`
- CLI、replay、调度等入口放在 `apps/`

## 当前已具备能力

仓库已经具备以下基础：

- `annuity_performance`、`annual_award`、`annual_loss` 的 replay CLI 和 replay slice
- capability-first 包边界
- 基于 `config/releases/*.json` 与 `config/domains/*/cleansing.json` 的受治理清洗清单
- trace / evidence / adjudication 基线链路
- 分层测试边界：`contracts`、`integration`、`replay`、`performance`

## 当前状态

截至当前主线状态：

- Phase 1 已完成
- Phase 2 implementation 已完成
- Phase 2 governance sign-off 已于 2026-04-13 随 Phase 6 remediation 闭合
- 已建立 legacy-to-pro capability mapping 与 intake-path mapping 基线
- 已完成 parity-critical rule classification 与默认 `block / warn` 严重性策略
- 已完成 `PAR-01` 的 baseline、真实 deep-sample 回放比对与离线人工 checkpoint
- 已完成 Phase 6：truthful intermediate gates、stable intermediate payload normalization、governance status sync
- 当前主线不应继续把 Phase 2 收口当成 active 目标；后续应转向 post-Phase-2 的 roadmap 决策与后续 phase admission

仍需继续推进的事项包括：

- Phase 3 对 replay orchestration duplication 和 failure explainability 的收口
- 更强的 agent-operable 入口、诊断和 runbook
- 运行时与治理面的后续闭环

## 当前主要约束

- **结果一致性优先**：输出必须与旧项目业务语义保持一致，这是 release gate
- **非黑盒化优先**：阶段、规则、失败路径和中间结果要可观察
- **渐进交付**：优先小范围、可验证的 phase，而不是大爆炸迁移
- **agent 可操作性**：入口、配置、诊断、runbook 需要适合 AI agent 使用
- **性能优化不能引入漂移**：任何优化都必须附带 parity 校验

## 当前主要风险

当前代码图谱和规划文档显示，项目仍有以下主要风险：

- replay orchestration 在多个 slice 间重复
- runtime 中存在硬编码的 release / policy / fixture 路径
- 证据持久化与治理仍偏验证态
- projection 与 trace 查询存在性能热点
- 生产态 operator surface 和部分 runtime surface 仍未闭环

## 当前工作方式

当前项目同时维护两类知识资产：

- `.planning/`：面向当前阶段执行与治理的本地规划资产
- `docs/wiki-cn/`：面向持续沉淀的中文 wiki 资产

简单理解：

- `.planning/` 更偏“当前怎么做”
- `wiki-cn/` 更偏“这个项目是什么、为什么这么做、主计划是什么、学到了什么”

当前这两类资产的关系也进一步明确了：

- `.planning/` 记录当前 Phase 6 已闭合、对应验证命令已通过
- `docs/wiki-cn/` 负责把这一状态沉淀成可复用的中文治理知识，而不是继续保留“Phase 2 尚待闭合”的旧叙述

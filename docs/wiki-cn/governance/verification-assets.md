# Verification Assets

> 类型：治理模型
> 日期：2026-04-12
> 状态：初版
> 适用范围：Phase 2 及后续 slices

本页用于定义项目中的 verification asset 类型、用途、刷新条件和治理口径。目标是避免把关键验证资产当成“测试附属文件”，从而在 phase 规划或 slice 扩展时被遗忘。

---

## 为什么需要这页

当前项目已经确认：

- parity、checkpoint、adjudication 和 CI gate 都依赖验证资产
- `golden set` 是重要机制，但它很容易散落在旧项目测试、脚本、能力图谱或运行经验中
- 如果 verification asset 不被显式登记，后续 phase 很容易只规划代码，不规划保护机制

因此从 Phase 2 开始，verification asset 要被视为治理对象，而不是测试附件。

---

## 资产类型

### `golden set`

定义：

- 高价值、可重复、场景经过挑选的标准样本集

用途：

- 快速保护关键清洗、映射、fallback、identity、projection 语义

特点：

- 场景覆盖是刻意设计的
- 不是为了模拟所有真实数据
- 适合进入 CI 或高频回归

### `golden baseline`

定义：

- 已确认参考结果对应的基准输出

用途：

- 与当前运行结果做稳定对比

特点：

- 可以是 parquet、json、snapshot、report
- 更偏“结果基线”，不等于输入样本本身

### `real-data sample`

定义：

- 来自真实生产输入形态的样本文件或样本子集

用途：

- 证明 intake contract 没有脱离真实世界
- 暴露 synthetic fixture 无法覆盖的结构问题

特点：

- 更贴近真实输入
- 结构可能复杂、脏、并不适合高频 CI

### `synthetic fixture`

定义：

- 为测试稳定性和可控性人工构造的简化样本

用途：

- 快速 replay
- unit / integration / small-scope regression

特点：

- 小、稳定、好构造
- 不能冒充真实输入标准

### `error-case fixture`

定义：

- 专门用于验证错误路径的输入样本

用途：

- 缺列
- 空 sheet
- 非法日期
- 阈值超限
- schema drift 超过允许范围

### `replay baseline`

定义：

- accepted slice 的回放参考资产

用途：

- replay gate
- final output compare
- accepted slice 回归保护

### `operator runbook evidence`

定义：

- 供人工排查、解释、验证、运营使用的证据与步骤

用途：

- 证明系统不仅能“跑通”，还能被排查和操作

---

## 治理规则

每个 verification asset 都应回答以下问题：

- 它保护什么行为
- 它属于哪个 domain 或哪个共享 runtime
- 它在什么场景下使用
- 它何时必须刷新
- 它由哪个文档、测试、runbook 或 gate 引用
- 它当前状态是什么

允许的状态建议统一为：

- `accepted`
- `planned`
- `deferred`
- `retired`

任何重要 verification asset 都不能处于“存在但未登记”的状态。

---

## 与其他治理对象的关系

### 与 CI 的关系

- `golden set` 更适合进入高频 CI 或 targeted gate
- `real-data sample` 更适合进入较重的 nightly / release 验证
- `synthetic fixture` 适合 PR gate 和快速回归
- `error-case fixture` 适合 contract strictness 和 failure-path 测试

### 与 parity gate 的关系

- `golden baseline` 和 `replay baseline` 是 parity compare 的直接输入
- `source-intake-adaptation` 证据包负责解释 verification asset 如何被消费和适配

### 与 adjudication 的关系

- verification asset 负责证明“发生了什么”
- adjudication 负责决定“这个差异怎么处理”

---

## 当前项目口径

截至当前讨论，项目已经确认：

- `source_intake` 的外部目标基线是 `real-data-style`
- 当前简化 workbook 输入仍保留，但它们只是 `synthetic fixture`
- `golden set` 是显式治理对象，不允许继续作为隐含机制存在
- `reference/verification_assets/phase2-accepted-slices.json` 已成为 accepted slice 资产 registry
- Phase 6 闭合后，`source_intake` 仍然是 `contract checkpoint`，而不是 `checkpoint_baseline` 文件资产

### 已明确存在或应被登记的资产

- `annuity_performance` 相关 `golden set / golden baseline`
  旧项目已有明确痕迹，应在后续治理资产清单中显式登记
- accepted slices 的 `replay baseline`
  当前已经存在于 `reference/historical_replays/*`
- accepted slices 的中间 `checkpoint_baseline`
  当前仅包括 `reference_derivation`、`fact_processing`、`identity_resolution`、`contract_state`
- 当前 Pro 仓库中的简化 workbook 输入
  应登记为 `synthetic fixture`
- 后续 `source_intake` 真实样本
  应登记为 `real-data sample`

这里需要特别避免一个语义混淆：

- `source_intake` 的长期目标仍是 `real-data-style` 外部 intake baseline
- 但在当前 replay gate 模型里，`source_intake` 不对应 `legacy_source_intake_*.json`
- 它通过固定 contract expectation + runtime observation 的方式做 truthful contract compare
- 因此它应被视为 checkpoint semantics，而不是 repo-native baseline file

### 当前已知缺口

- `annual_award` 与 `annual_loss` 是否需要独立的 domain-level `golden set`，还未形成显式治理结论
- verification asset manifest 已落地，但后续仍需继续扩展到更多 deferred 资产

## 审计补充

2026-04-12 的 legacy audit 与 verification-asset sweep 进一步确认，除了本页定义的 taxonomy 之外，项目还存在一批需要显式治理、但不适合直接写成当前 accepted baseline 的 legacy-only 资产与 operator artifact。

应特别记住：

- legacy `dataset_requirements.md` 是高价值治理资产，不应被当成普通测试附件遗忘
- 文档里提到但未找到实体文件的 error-case fixtures，应按 `planned but not created` 管理
- `verification_guide_real_data.md` 与历史 `validation_results` 更接近 operator / adjudication reference，而不是当前 replay baseline
- `annuity_income` 相关 legacy 资产与 ID5 retirement decision 仍需保留为制度记忆，避免后续 slice admission 时丢失关键上下文

相关稳定结论已另外沉淀到：

- [旧项目审计基线](./legacy-audit-baseline.md)

---

## 推荐清单结构

后续如果把 verification asset 再向前推进一层，建议每个 asset 至少登记下面几项：

- `asset_id`
- `asset_type`
- `domain`
- `purpose`
- `path`
- `used_by`
- `refresh_trigger`
- `status`
- `notes`

这份清单可以后续挂到治理页、coverage matrix，或单独形成 registry。

当前项目里，这个 registry 已经落在：

- `reference/verification_assets/phase2-accepted-slices.json`

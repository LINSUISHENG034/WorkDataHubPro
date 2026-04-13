# Phase 2 决策基线

> 类型：治理决策
> 日期：2026-04-12
> 状态：已确认
> 适用范围：`Transparent Pipeline Contracts & Parity Gates`

本页用于沉淀 Phase 2 已确认的五项灰区决策，作为后续计划、实现、测试、评审和 wiki 同步的共同基线。

---

## 总原则

Phase 2 的目标不是把系统一次性做成重型治理平台，而是把当前 replay harness 推进到：

- checkpoint 可分层
- 差异可裁决
- contract 可机器执行
- CI gate 可分层
- failed gate 有完整证据包

其中最重要的一条 intake 原则已经确认：

- 对源数据，允许长得不整齐
- 但不允许连最小可用骨架都没有

---

## 1. Gate Checkpoints

Phase 2 采用分层 checkpoint taxonomy。

- `source_intake`：`controlled-tolerance contract gate`
- `fact_processing`：`deterministic parity gate`
- `identity_resolution`：`deterministic parity gate`
- `reference_derivation`：`deterministic parity gate`
- `publication`：`operational / contract gate`
- `contract_state`：`deterministic parity gate`
- `monthly_snapshot`：最终 `must-match parity gate`

执行节奏也已确认：

- Wave 1：`source_intake`、`fact_processing`、`identity_resolution`、`contract_state`、`monthly_snapshot`
- Wave 2：补齐 `reference_derivation`
- `publication` 在两个 wave 中都保持为运行时行为 gate，不做 legacy 内容 parity

2026-04-13 Phase 6 闭合后，还需要补一句当前稳定口径：

- `source_intake` 仍然是 `contract gate`
- 它没有被提升成 `legacy_source_intake_*.json` 这类 repo-native baseline file
- 当前 accepted `checkpoint_baseline` 只覆盖 `reference_derivation`、`fact_processing`、`identity_resolution`、`contract_state`

---

## 2. Adjudication Behavior

`CompatibilityCase` 不再只是一个“待人工审核”的占位对象，而要成为明确的治理对象。

最小治理字段：

- `severity`：`block` / `warn`
- `decision_status`：`pending_review` / `approved_exception` / `approved_precedent` / `rejected` / `superseded`
- `precedent_status`：`none` / `candidate` / `accepted`
- `precedent_key`：稳定差异签名
- `expires_at`：临时豁免到期时间

已确认运行规则：

- `block + pending_review` 必须挡 gate
- `warn + pending_review` 不能静默通过
- 只有命中 `approved_precedent` 的重复差异，才允许机器自动接受
- `approved_exception` 只代表“这次接受”，不代表长期规则
- 已被 `source_intake` 成功适配的 benign source-schema drift，默认不生成 `CompatibilityCase`
- 只有破坏最小骨架、破坏内部 contract、或改变业务 parity 的差异，才进入 adjudication

---

## 3. Contract Strictness

Phase 2 采用双层策略：

- 对源数据入口，受控宽容
- 对内部 contract，严格校验

### 3.1 外部 Intake 契约

外部 `source_intake` 的目标契约已经确认不是 `legacy-style`，而是：

- `real-data-style source intake contract`

这意味着：

- 后续要对齐真实生产 workbook 形态
- 旧项目的价值在于“真实数据处理经验”和“已验证的适配规则”，而不是旧架构本身

当前 Pro 仓库里已有的简化输入仍然保留，但角色已经重新定义为：

- synthetic deterministic fixtures

它们可继续用于：

- 快速 replay
- 小型 integration test
- 单场景回归测试

但它们不再作为 Phase 2 的 intake baseline。

### 3.2 入口宽容规则

`source_intake` 允许：

- 已知字段别名和字段映射
- extra non-golden columns 忽略，但要产出 warning 和证据
- non-golden 字段缺失告警
- 空的 `company_id`、`年金计划号` 等 enrichable 字段延后到下游 lookup / fallback 处理

`source_intake` 必须失败的情况：

- golden required fields 缺失
- 无法构造 `InputBatch` / `InputRecord` 的最小可用骨架
- 无法确定稳定的 `batch_id`、`period`、row anchor 或该 slice 继续执行所需的最小业务识别字段

### 3.3 内部 Contract 规则

一旦数据进入内部对象，例如：

- `InputBatch`
- `InputRecord`
- `CanonicalFactRecord`
- `FieldTraceEvent`
- `PublicationPlan`

就执行严格结构校验：

- 必填字段
- 类型形状
- `batch_id` / `run_id` / `domain` 一致性
- `anchor_row_no`
- `event_seq`
- `PublicationPlan` 的合法组合

结构错误直接 fail fast。
业务语义差异继续走 parity gate 和 adjudication。

---

## 4. CI Scope

Phase 2 采用分层 CI。

### PR Gate

- affected tests
- source-intake tolerance tests
- minimum-skeleton failure tests
- `annuity_performance` replay
- explainability retrieval test

### Protected Branch Merge Gate

- 所有 accepted replay slices

当前包括：

- `annuity_performance`
- `annual_award`
- `annual_loss`

### Nightly / Release Gate

- `uv run pytest -v`
- 更宽 replay 集合
- performance checks

这个分层的目的不是形式分级，而是让 Phase 2 已确认的规则真正进入自动执行系统。

---

## 5. Evidence Shape

Phase 2 的 failed gate 不能只产出 trace JSON 和单个 compatibility case，而要产出一套 comparison-run evidence package。

最小证据包固定包含：

- `manifest.json`
- `gate-summary.json`
- `checkpoint-results.json`
- `source-intake-adaptation.json`
- `diffs/<checkpoint>.json`
- `trace/`
- `lineage-impact.json`
- `publication-results.json`
- `compatibility-case.json`
- `report.md`

其中有几项尤其关键：

- `source-intake-adaptation.json`
  记录 schema fingerprint、字段映射、忽略列、缺失 non-golden 列、golden 失败项、最小骨架构造结果
- `checkpoint-results.json`
  回答“从哪一站开始歪了”
- `lineage-impact.json`
  回答“歪了之后影响了谁”
- `compatibility-case.json`
  回答“最终怎么裁决”

Phase 2 先固定 file-backed evidence package 即可，不要求本阶段同时完成数据库化 evidence index。

---

## 6. Verification Assets Governance

`golden set` 不应被视为“测试附件”或“旧项目遗留物”，而应被视为一等验证资产。

Phase 2 起，下面这些对象都应按 verification asset 管理：

- `golden set`
- `golden baseline`
- `real-data sample`
- `synthetic fixture`
- `error-case fixture`
- `replay baseline`
- `operator runbook evidence`

这些资产的职责不同，不能混用：

- `golden set`
  用于高价值、可重复、快速保护的标准样本集
- `golden baseline`
  用于和既定参考结果做稳定比对
- `real-data sample`
  用于证明 intake 和真实输入形态没有脱节
- `synthetic fixture`
  用于快速、稳定、可控的小场景测试
- `error-case fixture`
  用于验证缺列、空 sheet、坏格式、阈值超限等失败路径
- `replay baseline`
  用于 accepted slice 的回放和最终结果对比
- `operator runbook evidence`
  用于证明系统在人工排查和运行操作层面仍然可用

治理规则：

- 任何影响 parity、explainability、operator behavior 或 data-shape protection 的机制，都必须作为显式 verification asset 或显式 mechanism 登记
- verification asset 必须有明确用途、刷新条件、引用位置和当前状态
- `synthetic fixture` 不得冒充 `real-data-style` intake baseline
- `real-data sample` 不能替代 `golden set` 的稳定保护角色
- `golden set`、`replay baseline`、`error-case fixture` 的缺失如果会影响 phase 目标，必须显式写成 `deferred` 或 `retired`，不能只是未提及

### 6.1 当前确认口径

当前项目已经确认：

- `real-data-style` 是 `source_intake` 的目标基线
- 当前简化 workbook 输入继续保留，但只作为 `synthetic deterministic fixture`
- `golden set` 是需要显式治理的一等机制，不能只散落在 requirements、tests 或旧项目记忆中
- `source_intake` 的 truthful gate 语义已经在 Phase 6 中闭合，但闭合方式是固定 contract compare，不是新增 baseline 文件资产

当前仍需后续补齐的点：

- `annuity_performance` 之外，`annual_award` 与 `annual_loss` 是否要形成独立的 domain-level `golden set`
- 每个 accepted slice 的 verification asset manifest 需要单独落地

---

## 7. Forgotten Mechanism Sweep

为了避免像 `golden set` 这样的重要机制被遗漏，后续 phase 和 slice 进入规划前，必须执行一次 `forgotten mechanism sweep`。

这不是“建议动作”，而是 phase admission 的治理检查。

### 7.1 Sweep 目标

回答一个简单问题：

- 这个机制如果今天不做，是明确延期了，还是只是被忘了？

如果答案是“只是被忘了”，那说明当前治理流程有缺口。

### 7.2 Sweep 必查来源

每次 sweep 至少检查下面几类来源：

- 旧项目的 `docs/domains/`
- 旧项目的 `tests/fixtures/`
- 旧项目的 `tests/e2e/`
- 旧项目的 `scripts/tools/parity/`
- 旧项目的 `config/`
- 旧项目的 `docs/runbooks/`
- 当前项目的 coverage matrix、refactor program、architecture blueprint、accepted slice plans

### 7.3 Sweep 输出要求

每个发现的关键机制都必须进入以下状态之一：

- `accepted`
- `deferred`
- `retired`

不允许存在下面这种状态：

- 机制客观存在
- 旧项目或测试里确实依赖它
- 但当前 phase 文档没有记录，也没有做延期/退役决定

### 7.4 应重点防遗漏的机制类型

后续 sweep 必须特别关注下面几类对象：

- verification assets，例如 `golden set`、`real-data sample`、`error-case fixture`
- 隐式 runtime contract，例如 sheet merge contract、fallback chain、delete-scope contract
- operator artifacts，例如 runbook、manual checkpoint、人工排查查询路径
- parity scripts 与 legacy baseline 生成脚本
- config 里的 mapping、fallback、筛选规则、文件识别规则

---

## 域级 Intake 基线

下面的 domain baseline 不是最终 schema 细节文档，而是当前已确认的 Phase 2 治理口径。它们应优先参考真实数据样本、旧项目已验证 capability map、当前 data-source config，以及现有 accepted slice 的处理路径。

### `annuity_performance`

建议的 golden required fields：

- `月度`
- `业务类型`
- `计划类型`
- `计划代码`
- `客户名称`
- `期末资产规模`
- 至少一个 identity hint，例如 `公司代码` 或 `集团企业客户号`

建议的 minimum usable skeleton：

- `月度`
- `业务类型`
- `客户名称`
- `期末资产规模`
- `计划代码` 或 `计划类型` 二选一

允许的 source drift 示例：

- workbook 文件名变体
- 字段别名如 `计划号 -> 计划代码`
- extra non-golden columns
- 空 `计划代码`，只要 fallback/defaulting 仍有足够上下文

### `annual_award`

建议的 golden required fields：

- `上报月份`
- `客户全称`
- `计划类型`
- `计划规模`
- `source_sheet` 或等价业务类型来源

说明：

- `年金计划号` 和 `company_id` 是 blank-allowed enrichable fields

建议的 minimum usable skeleton：

- `上报月份`
- `客户全称`
- `source_sheet` 或 `业务类型` 二选一
- `年金计划号` 或 `计划类型` 二选一

允许的 source drift 示例：

- 双 sheet merge + fallback
- `客户全称 -> 上报客户名称`
- `机构 -> 机构名称`
- extra non-golden event metadata
- 空 `年金计划号` / `company_id` 继续走 lookup 与 fallback

### `annual_loss`

建议的 golden required fields：

- `上报月份`
- `客户全称`
- `流失日期`
- `计划类型`
- `计划规模`
- `source_sheet` 或等价业务类型来源

说明：

- `年金计划号` 和 `company_id` 是 blank-allowed enrichable fields

建议的 minimum usable skeleton：

- `上报月份`
- `客户全称`
- `source_sheet` 或 `业务类型` 二选一
- `年金计划号` 或 `计划类型` 二选一

允许的 source drift 示例：

- 双 sheet merge + fallback
- trailing empty rows skip
- `客户全称 -> 上报客户名称`
- `机构 -> 机构名称`
- extra non-golden event metadata
- 空 `年金计划号` / `company_id` 继续走 current-contract lookup 与 fallback

---

## 当前落地含义

本页确认后，Phase 2 后续文档和实现都应遵守下面三条：

1. intake baseline 以 `real-data-style` 为目标，而不是以当前简化 fixture 为目标
2. 简化 fixture 继续保留，但只作为测试夹具
3. 旧项目的价值在于可复用的真实数据处理经验、字段映射经验和 drift handling 经验，不在于回退到旧架构
4. `golden set`、`replay baseline`、`real-data sample` 等 verification assets 必须显式登记，不能只散落在测试、脚本或旧项目记忆中
5. 新 phase / 新 slice 进入规划前，必须完成一次 `forgotten mechanism sweep`

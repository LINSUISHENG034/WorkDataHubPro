# Phase 3 决策基线

> 类型：治理决策
> 日期：2026-04-13
> 状态：已确认
> 适用范围：`Orchestration Refactor & Failure Explainability`

本页沉淀 Phase 3 当前已经足够稳定的四项灰区决策，用于约束后续计划、实现、评审、runbook 与 agent 入口设计。

---

## 总原则

Phase 3 的目标不是把 replay 做成一个更大的黑盒，而是：

- 减少重复 orchestration
- 提升失败路径可解释性
- 改善 agent 的操作入口
- 在不隐藏 domain 语义的前提下加强共享能力

如果“更统一”和“更可解释”发生冲突，优先保留可解释性与 capability-first 边界。

---

## 1. Replay 共享边界

### 已确认方向

- 只抽共享 primitive
- 保留显式的 per-domain runner
- 不采用“一个 fully generic replay runner + domain adapter”的方向

### 应共享的部分

- trace / lineage scaffolding
- checkpoint construction
- gate summary
- evidence package assembly
- publication-plan helper 使用方式
- `source_intake -> fact_processing -> identity_resolution` 的 orchestration loop skeleton

### 必须继续显式保留的部分

- intake service 选择
- processor 选择
- domain enrichment 步骤
- replay asset 加载
- domain publication target wiring
- rule manifest 与 hook-sensitive 行为

尤其要记住：

- `annuity_income` 不是“再来一个普通单 sheet domain”
- legacy 中它还带有 `unknown_names_csv`、`固费` 加权 backfill、service delegation、以及显式 no-hook contract
- 这些都不应被 generic runner 吞掉

### 当前治理口径

Phase 3 应建设：

- 一个共享 replay runtime
- 多个显式 domain runner

而不是：

- 一个把 domain 语义藏进 callback / config / adapter 的大统一 runner

---

## 2. Failure Contract

### 已确认方向

- 采用 `typed run report + typed exceptions`

### 分层口径

下面两类失败必须显式分开：

- 运行前失败
  - 例如缺 baseline、config release 不匹配、contract validation 失败
  - 这类失败使用 typed exceptions
- 运行已形成后发现差异
  - 例如 checkpoint failed、gate failed、生成 `CompatibilityCase`
  - 这类失败进入 typed run report

### typed run report 最小字段

- `comparison_run_id`
- `overall_outcome`
- `checkpoint_results`
- `primary_failure`
- `compatibility_case`
- `evidence_paths`

### 当前治理口径

Phase 3 不应使用一个统一大 failure object 去混合这两层语义。

---

## 3. Agent 入口

### 已确认方向

- 保留当前 domain 命令
- 在其上增加统一的 replay agent 入口

### Phase 3 replay CLI v1

保留：

- `replay-annuity-performance`
- `replay-annual-award`
- `replay-annual-loss`

新增：

- `replay run --domain <domain> --workbook <path> --period <period>`
- `replay diagnose --comparison-run-id <id>`
- `replay list-domains`

### agent-facing 最小输出

- `comparison_run_id`
- `overall_outcome`
- `primary_failed_checkpoint`
- `evidence_root`
- `compatibility_case_id`

### 不应并入 Phase 3 replay surface 的对象

下面这些能力不属于当前 replay gray-area closure，后续应进入独立 `etl` / `operator` / `adjudication` surface：

- `--all-domains`
- file discovery control
- DB diagnostics
- `company_lookup_queue`
- `reference_sync`
- manual `customer-mdm` commands

---

## 4. Temporary Identity Policy

### 已确认方向

- 不再使用 `TEMP-{company_name}`
- 采用 legacy-backed 的确定性 opaque temp-id 生成规则
- temp-id 前缀允许全局配置
- 默认前缀设为 `IN`

### 最小生成口径

- 先做名字规范化
- 再使用带 salt 的 HMAC 生成稳定 temp-id
- 同一规范化输入在同一 salt 下必须得到同一结果
- 空值或占位值应返回 `None`
- 原始公司名只进入 sidecar evidence，不进入 `company_id`

### 配置治理口径

temp-id 前缀不是普通运行时参数，而是受治理的 compatibility 参数：

- 只允许一个全局设置
- 不允许按 domain 配
- 不允许按 run 配
- 不应暴露成随手可改的 CLI 选项
- 前缀变更必须经过 config release 与 compatibility review

### 推荐 helper 边界

- `generate_temp_identity(...)`
- `is_temp_identity(...)`
- `normalize_identity_fallback_input(...)`
- `temp_identity_prefix()`

---

## 5. Phase 3 开工前必须锁定的合同

在进入 Phase 3 实现前，至少应先锁定下面四项：

1. replay 共享边界
   - 哪些属于 `shared_primitive`
   - 哪些属于 `shared_with_domain_parameters`
   - 哪些必须作为 `explicit_domain_contract`
2. typed exception 集合与 typed run report schema
3. replay CLI v1 的命令与输出合同
4. temp-id 的 helper、salt、prefix 与空值语义

这些属于 phase admission 的前置合同，不应边实现边临时决定。

---

## 6. 当前明确后置的事项

下面这些事项可以后置，不应阻塞本页四项决策：

- broader `etl` execution parity
- `etl` / `operator` / `adjudication` 完整命令树
- `company_lookup_queue`、`reference_sync`、manual `customer-mdm` 的 retain / replace / retire 决策
- 超出 first-wave 的未来 domain 泛化设计

---

## 当前落地含义

本页确认后，Phase 3 的更准确推进口径应是：

- 可以开始实现准备
- 但必须先把 replay contract、failure contract、CLI contract、temp-id contract 写成正式实现前置条件
- 不应再把“大方向是否成立”继续当成开放问题

更详细的工作材料见：

- `docs/gsd/reviews/2026-04-13-phase3-gray-area-governance-review.md`
- `docs/gsd/grey-areas/2026-04-13-phase3-gray-area-decisions.md`

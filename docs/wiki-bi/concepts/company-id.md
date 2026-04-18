# 企业身份标识：`company_id`

## 定义

`company_id` 是跨 domain 连接事实、主数据、快照、回填与验证资产的企业身份标识。

它的核心作用不是“看起来像一个编号”，而是：

- 作为跨表连接键
- 作为 customer / plan / snapshot 聚合的稳定身份锚点
- 作为验证和比较时的重要一致性条件

## 业务意义

如果没有稳定的企业身份标识：

- 同一企业会在不同 domain 中裂成多个对象
- 回填、快照、标签、客户状态会失去统一锚点
- 输出正确性会被表面上的“字段都有值”所掩盖

## 解析链

legacy 中最值得保留为制度记忆的，不是某个具体实现类，而是解析链本身的层次：

1. YAML overrides
2. DB cache
3. existing column passthrough
4. EQC / provider lookup
5. temp-id fallback

这条链回答的是“身份问题如何在不丢失记录的前提下被稳定处理”，而不是“某个函数先调用谁”。

在 current project 中，当前显式受测的治理链更接近：

1. source value
2. cache
3. provider lookup
4. temp-id fallback

这说明实现可以阶段性收缩，但治理目标不能因此消失。

对维护者更重要的是把下面几层分开写：

- 兼容性清单 / 历史记忆
- 当前运行路径
- 已退休且不得恢复的行为
- 面向操作人员的可见后果

当前可以这样理解：

- 兼容性清单 / 历史记忆
  - legacy 仍保留 YAML overrides、passthrough、EQC/provider、5-step fallback 等制度记忆
- 当前运行路径
  - current project 当前受测的是 `source_value -> cache -> provider -> temp-id fallback`
  - `annual_award` / `annual_loss` 还显式保护了 history-aware plan-code enrichment
- 已退休且不得恢复的行为
  - ID5 fallback 与 legacy `TE...` 风格 temp identity 都不应被写成“还可随时恢复”
- 面向操作人员的可见后果
  - unresolved identity 不只影响内部解析，还会影响 `company_reference`、operator artifacts 与 queue/signal surfaces

## 四层分离

### 当前运行路径

- current accepted runtime 的身份主链是 `source_value -> cache -> provider -> temp-id fallback`
- `annual_award` / `annual_loss` 的 history-aware plan-code enrichment 已有 current tests 承接
- 这层只写当前受测、可验证、可复述的行为，不把 deferred runtime 混入 active 叙述

### 兼容性清单 / 历史记忆

- legacy `company_id_overrides_*` family、`company_branch.yml`、`eqc_confidence.yml` 仍是制度记忆
- legacy 5-step chain（含 passthrough）仍属于历史记忆，不等于当前优先级栈被完整复刻
- 这层用于解释“为什么过去会这样”，不是宣布“现在仍这样执行”

### 已退休且不得恢复的回退行为

- ID5 fallback 已退休，不得作为“临时兼容开关”回写到 current runtime
- legacy `TE...` 风格临时身份已退休，current runtime 应继续保持 opaque `IN...` temp identity
- 退休项应保留 provenance 与证据页链接，但不应写成可随时恢复的候选路径

### 面向操作人员的可见后果

- unresolved identity 必须对 operator 可见：artifact、signal、queue decision/evidence 至少命中其一
- shared artifact route 见 [unresolved-name and failed-record 证据](../evidence/unresolved-name-and-failed-record-evidence.md)；它负责解释 deferred queue 之外还有哪些 operator-visible consequence
- 如果缺少 queue/persistence 物化，必须在 evidence 页登记为 gap，而不是在概念页假设“已由内部处理”
- 结论页可以陈述后果，未闭环项只能进入 `当前证据缺口`

## 不应被改写的约束

- `company_id` 的语义优先于生成方式
- 它必须服务跨 domain 的稳定身份，而不是单次运行方便
- temp-id 是 fallback，不等于“任何未知身份都可以随意生成”
- `company_id` 不能泄露原始业务标识的敏感语义
- 不能把单字段识别误写成唯一有效路径
- 某些 domain / 计划类型天然需要多线索解析

## 输入现实与边界情况

- 企业身份往往不能只依赖单一字段
- `客户名称` 为空不必然等于无法识别
- 计划代码、计划名称、账户名、历史映射、缓存与 lookup 可能共同参与识别
- unknown / unresolved 情况必须被显式记录，而不是静默吞没
- 单一计划与集合计划会影响可用线索与解释方式
- `annuity_income` 还带有一批 legacy-only 身份约束，不能因为当前未实现而被遗忘
- `annuity_income` 当前已经有 current tests / replay assets / runbook，因此不应再被写成“只有制度记忆，没有实现承接”

## 对输出与下游的影响

- 影响 `customer.客户明细` 的汇总与回填
- 影响 `customer.客户年金计划` 的 contract / snapshot 结果
- 影响 event domain 的计划号补全与后续对齐
- 影响 replay、parity、golden 比较时的身份一致性
- 影响 `company_lookup_queue`、`unknown_names_csv` 这类 surface 是否仍有制度价值

## 常见误解 / 非例

- `company_id` 不是“客户名称的另一个写法”
- temp-id 不是正式身份，只是受治理的 fallback
- `company_id` 解析链不是单纯实现细节，因为它直接改变输出语义
- “客户名称为空”不等于“无法识别客户”
- “当前 project 还没实现某条 fallback”不等于这条制度记忆可以被删除
- “在 legacy 出现过的 persistence/queue”不等于“在 current active runtime 已存在同名对象”

## 相关概念

- [客户状态总览](./customer-status.md)
- [年金计划类型：`plan_type`](./plan-type.md)
- [回填：`backfill`](./backfill.md)
- [临时身份：`temp_id`](./temp-id.md)

## 相关标准

- [身份治理语义正确性](../standards/semantic-correctness/identity-governance.md)
- [输入现实合同](../standards/input-reality/input-reality-contracts.md)
- [输出正确性标准](../standards/output-correctness/output-correctness.md)
- [real-data validation](../standards/verification-method/real-data-validation.md)
- [golden scenarios](../standards/verification-method/golden-scenarios.md)

## 相关证据

- [身份与补查证据](../evidence/identity-and-lookup-evidence.md)
- [unresolved-name and failed-record 证据](../evidence/unresolved-name-and-failed-record-evidence.md)
- [operator 与 surface 证据](../evidence/operator-and-surface-evidence.md)
- [`annuity_income` branch mapping 证据](../evidence/annuity-income-branch-mapping-evidence.md)
- [`annuity_income` ID5 retirement 证据](../evidence/annuity-income-id5-retirement-evidence.md)

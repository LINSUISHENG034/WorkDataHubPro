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

## 相关概念

- [客户状态总览](./customer-status.md)
- [年金计划类型：`plan_type`](./plan-type.md)
- [回填：`backfill`](./backfill.md)
- [临时身份：`temp_id`](./temp-id.md)

## 相关标准

- [输入现实合同](../standards/input-reality/input-reality-contracts.md)
- [输出正确性标准](../standards/output-correctness/output-correctness.md)
- [real-data validation](../standards/verification-method/real-data-validation.md)
- [golden scenarios](../standards/verification-method/golden-scenarios.md)

## 相关证据

- [身份与补查证据](../evidence/identity-and-lookup-evidence.md)
- [operator 与 surface 证据](../evidence/operator-and-surface-evidence.md)

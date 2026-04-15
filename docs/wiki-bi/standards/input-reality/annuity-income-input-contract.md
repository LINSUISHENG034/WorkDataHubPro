# `annuity_income` 输入合同

> standard_type: `input-reality`
> related_standard_types: `verification-method`, `output-correctness`

## 标准对象

本页定义 `annuity_income` 的输入合同。

它回答的不是旧实现“怎么跑”，而是：

- 哪类 workbook / sheet 才算这个 domain 的有效输入
- 哪些字段是稳定输入骨架
- 哪些缺失属于可降级处理，哪些会破坏输入合同

## 输入介质与发现规则

- 文件格式
  - Excel workbook（`.xlsx`）
- 基础目录
  - `data/real_data/{YYYYMM}/收集数据/数据采集`
- 文件名关键字
  - `*年金规模收入*.xlsx`
  - `*规模*收入数据*.xlsx`
- 排除模式
  - `*回复*`
- 版本策略
  - `highest_number`

## Sheet 合同

- 主 sheet
  - `收入明细`
- 输入形态
  - single-sheet domain
- 关键区别
  - 它与 `annuity_performance` 共用 workbook family，但处理的是不同 sheet
- 非例
  - 不能把 `规模明细` 当作 `annuity_income` 的有效输入 sheet
  - 也不能把 multi-sheet event-domain 经验直接套到本域

## observed production reality

- representative single-month production-sample validation shows the current workbook family contains both `规模明细` and `收入明细` in one physical workbook
- `annuity_performance` still owns the `规模明细` sheet contract
- `annuity_income` still owns the `收入明细` sheet contract
- the shared workbook family strengthens workbook-discovery and explainability understanding, not domain collapse
- accepted contract 仍然是 `收入明细` sheet，而 shared workbook family 属于 observed production reality

## 最小字段骨架

当前 raw sources 能稳定支撑的最小输入骨架是：

- `月度`
- `业务类型`
- `客户名称`
- 至少一个计划锚点：`计划号` 或 `计划代码`
- 收入数值族：`固费`、`浮费`、`回补`、`税`

这些字段共同定义了：

- 月度定位
- 业务类型解释
- 身份解析线索
- 收入事实载荷

当前更适合视为“高价值补强字段”，但不宜在本页直接上升为硬门槛的还有：

- `计划类型`
- `机构名称`

它们对 current project 和 legacy 行为都很重要，但现阶段更像：

- 强输入线索
- 处理质量和解释力的重要来源

而不应在没有更强 source contract 支撑时直接写成“缺失即破坏输入合同”。

## 运行时容忍边界

当前 legacy 与 current evidence 一致表明：

- `组合代码` 缺失可以进入 defaulting，而不必然使整份输入无效
- `机构代码` 可以由 `机构名称` + branch mapping 推导
- `计划类型` 缺失会削弱 defaulting 与解释能力，但当前不宜直接写成一票否决
- `company_id` 不要求作为输入直接提供；运行时允许进入 temp-id fallback
- ID5 account-name fallback 不属于当前允许恢复的输入补救路径

## 无效源条件

下面几类情况应视为输入合同被破坏：

- 找不到匹配 workbook
- workbook 中缺失 `收入明细` sheet
- 同时缺失 `计划号` 与 `计划代码`，使计划锚点消失
- 缺失 `月度`、`业务类型` 这类主解释字段
- 收入数值载荷整体缺失，导致记录不再能表达收入事实
- 将 synthetic fixture 冒充为 real-data sample

补充说明：

- unresolved identity 不等于输入无效；它应优先进入受治理的 temp-id / artifact 路径
- `计划类型`、`机构名称` 目前更适合被视为“高价值输入线索”，而不是本页直接判定为绝对硬门槛
- 关键是不能让输入合同把“身份待补强”误写成“记录必须丢弃”

## 当前实现证据

- `current_test`
  - `tests/integration/test_annuity_income_processing.py`
- `current_reference_asset`
  - `reference/historical_replays/annuity_income/`
- `current_runbook`
  - `docs/runbooks/annuity-income-replay.md`

## 相关概念

- [企业身份标识：`company_id`](../../concepts/company-id.md)
- [临时身份：`temp_id`](../../concepts/temp-id.md)
- [年金计划类型：`plan_type`](../../concepts/plan-type.md)

## 相关证据

- [`annuity_income` 专题证据](../../evidence/annuity-income-gap-evidence.md)
- [annuity workbook family 证据](../../evidence/annuity-workbook-family-evidence.md)
- [`annuity_income` branch mapping 证据](../../evidence/annuity-income-branch-mapping-evidence.md)
- [`annuity_income` ID5 retirement 证据](../../evidence/annuity-income-id5-retirement-evidence.md)
- [输入现实证据](../../evidence/input-reality-evidence.md)

## 相关验证方法

- [real-data validation](../verification-method/real-data-validation.md)
- [golden scenarios](../verification-method/golden-scenarios.md)

# `annuity_performance` 输入合同

> standard_type: `input-reality`
> related_standard_types: `verification-method`, `output-correctness`

## 标准对象

本页定义 `annuity_performance` 的输入合同。

它回答的不是“旧代码怎么读文件”，而是：

- 什么样的源文件才算这个 domain 的有效输入
- workbook / sheet 现实长什么样
- 哪些字段缺失时应判为无效源

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
  - `规模明细`
- 输入形态
  - single-sheet domain
- 非例
  - 不应把 event domain 的 multi-sheet 经验套到 `annuity_performance`
  - 也不应因为测试夹具常常很小，就假定真实 workbook 没有额外列

## 观测到的生产现实

- representative single-month production-sample validation shows the current workbook family contains both `规模明细` and `收入明细` in one physical workbook
- `annuity_performance` still owns the `规模明细` sheet contract
- `annuity_income` still owns the `收入明细` sheet contract
- the shared workbook family strengthens workbook-discovery and explainability understanding, not domain collapse
- accepted contract 仍然是 `规模明细` sheet，而 shared workbook family 属于观测到的生产现实

## 最小字段骨架

当前 raw sources 与 legacy code audit 共同支撑的最小输入骨架是：

- `月度`
- `计划代码`
- `客户名称`
- `期末资产规模`

这些字段定义了本域最小可解释输入：

- `月度`：时间锚点
- `计划代码`：计划锚点
- `客户名称`：identity 线索
- `期末资产规模`：下游 `max_by` / 主拓归属语义的关键排序字段

## 运行时容忍边界

当前代码核对表明：

- `客户名称` 缺失并不必然让整份源数据失效
- 在 `计划代码` 可用时，部分记录仍可能通过 plan-code 路径继续完成 identity 解析
- `convert_dataframe_to_models` 对 row-level 的硬门槛是：`月度` 与 `计划代码` 同时可用；缺失其一会被直接丢弃

因此更准确的理解是：

- `客户名称` 缺失
  - 对 golden-set / explainability 视角来说属于重要缺口
  - 对 runtime 代码路径来说更接近“降级输入”，而不是绝对无效源
- `月度` 或 `计划代码` 缺失
  - 更接近 row-level hard invalid，不是单纯降级

## 常见输入字段

除最小骨架外，legacy 材料还明确出现或反复依赖下列字段：

- `业务类型`
- `机构`
- `计划号`
- `机构名称`
- `组合代码`
- `计划类型`
- `集团企业客户号`
- `期初资产规模`
- `投资收益`
- `当期收益率`
- `流失(含待遇支付)`

它们不全都属于“缺失即无效”的骨架字段，但其中很多直接影响后续 canonical fact、backfill 或 snapshot 解释。

## 隐藏字段语义（输入侧）

| 字段 / 字段对 | 隐藏语义 | 输入合同意义 |
|---|---|---|
| `客户名称` -> `年金账户名` | 在清洗前先复制为 `年金账户名`，保留原始账户名线索供 identity resolver 使用 | 输入合同不仅关心“能不能读到列”，还关心 identity clue 是否被保留 |
| `集团企业客户号` -> `年金账户号` | 先清理前缀 `C`，再复制到 `年金账户号`，随后原列可被 drop | 输入合同需要承认“源列可消失，但其语义必须以派生字段继续存在” |
| `期末资产规模` | 被下游 backfill 聚合用于 `max_by`（主拓机构、关键计划等）排序 | 这是输入侧对输出语义有直接影响的关键字段，不应被降级为“普通数值列” |
| `月度` | 一方面是输入定位；另一方面参与 `tags` 的 `yyMM新建` 生成 | 输入合同应显式声明其跨入 output/backfill 的语义传递 |

## 无效源条件

下面几类情况应视为输入合同被破坏：

- 找不到匹配 workbook
- 匹配到多个 workbook 且未做版本裁决
- workbook 中缺失 `规模明细` sheet
- 缺失 `月度`、`计划代码`、`期末资产规模` 这类关键列
- 把 synthetic fixture 冒充为 real-data sample

补充说明：

- `客户名称` 缺失应优先视为“解释力下降 / identity 线索减弱”
- 只有当 runtime 也无法通过其他线索继续处理时，才应进一步升级为无效输入判断

## 当前实现证据

- `current_test`
  - `tests/integration/test_annuity_performance_intake.py`
  - `tests/integration/test_annuity_performance_processing.py`
  - `tests/replay/test_annuity_performance_slice.py`
- `current_reference_asset`
  - `reference/historical_replays/annuity_performance/`
- `current_runbook`
  - `docs/runbooks/annuity-performance-replay.md`

## 相关概念

- [年金计划类型：`plan_type`](../../concepts/plan-type.md)
- [企业身份标识：`company_id`](../../concepts/company-id.md)

## 相关证据

- [输入现实证据](../../evidence/input-reality-evidence.md)
- [annuity workbook family 证据](../../evidence/annuity-workbook-family-evidence.md)
- [annuity_performance 字段处理证据](../../evidence/annuity-performance-field-processing-evidence.md)

## 相关验证方法

- [real-data validation](../verification-method/real-data-validation.md)
- [golden scenarios](../verification-method/golden-scenarios.md)

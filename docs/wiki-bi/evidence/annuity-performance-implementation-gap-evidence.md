# `annuity_performance` implementation gap 证据

## 结论主题

本页记录 `annuity_performance` 在当前 wiki 知识与 legacy 代码实现之间的差距。

这些差距不预设 blame 方向：

- 可能是 wiki 结论过宽或过窄
- 也可能是 legacy 代码实现存在 bug、漂移或内部自相矛盾

## 审计范围

本轮只审计 annuity-performance 的三类内容：

- 输入合同
- 输出合同
- 字段处理 / 空值默认规则

## 差距记录

| gap_id | 类型 | 当前判断 | 说明 |
|---|---|---|---|
| GAP-AP-001 | input_contract | wiki 可能过窄 | wiki 当前最小输入骨架写为 `月度`、`计划代码`、`客户名称`、`期末资产规模`；但 `schemas.py` 的 Bronze required columns 还包括 `期初资产规模`、`投资收益`、`当期收益率`。当前看起来是 wiki 没完全吸收 schema-level contract，或代码比文档更严格。 |
| GAP-AP-002 | input_contract | code 可能偏宽 | wiki 把缺失 `客户名称` 视为无效输入的一部分，但 `pipeline_builder.py` 中 `CompanyIdResolutionStep` 会在缺失 `客户名称` 列时主动补一个空列继续处理。说明代码对该列缺失的容忍度高于 wiki 合同。 |
| GAP-AP-003 | output_contract | code 内部自相矛盾 | `schemas.py` 的 Gold required columns把 `company_id`、`客户名称`、`期末资产规模` 等列视为必需；但 `helpers.py` 的 `convert_dataframe_to_models()` 只基于 `计划代码` 和 `月度` 过滤行，随后允许 `AnnuityPerformanceOut` 中的 `company_id` / `客户名称` / `期末资产规模` 继续为 `None`。说明 schema contract 与最终落模逻辑并不一致。 |
| GAP-AP-004 | backfill_contract | code 可能有 bug | `foreign_keys.yml` 中 `fk_organization` 仍引用 source 字段 `机构` 作为目标 `机构` 的来源，但 annuity-performance pipeline 已在最开始把 `机构` 重命名成 `机构名称`。如果 backfill 运行在 canonical rows 上，则组织架构表很可能拿不到预期的机构名称。 |
| GAP-AP-005 | field_processing | code 可能有 bug | pipeline 对 `集团企业客户号` 先执行 `.astype(str).replace(\"nan\", None).str.lstrip(\"C\")`，这会把真实 Python `None` 变成字符串 `\"None\"`，随后又复制到 `年金账户号`。wiki 语义是“缺失应继续保持缺失”，而不是物化成字面值 `None`。 |
| GAP-AP-006 | field_processing | wiki 可能过宽 | wiki 当前把“空值默认补 plan code”写成一般规则，但 `apply_plan_code_defaults()` 实际只对 `NaN` / `\"\"` 生效，不覆盖所有空值占位符字符串。若源数据含字面值 `\"None\"` 等占位符，代码语义比 wiki 描述更窄。 |

## 证据来源

- `E:\Projects\WorkDataHub\src\work_data_hub\domain\annuity_performance\pipeline_builder.py`
- `E:\Projects\WorkDataHub\src\work_data_hub\domain\annuity_performance\service.py`
- `E:\Projects\WorkDataHub\src\work_data_hub\domain\annuity_performance\helpers.py`
- `E:\Projects\WorkDataHub\src\work_data_hub\domain\annuity_performance\models.py`
- `E:\Projects\WorkDataHub\src\work_data_hub\domain\annuity_performance\schemas.py`
- `E:\Projects\WorkDataHub\src\work_data_hub\infrastructure\transforms\plan_portfolio_helpers.py`
- `E:\Projects\WorkDataHub\config\data_sources.yml`
- `E:\Projects\WorkDataHub\config\foreign_keys.yml`

## 当前可下的稳定结论

- annuity-performance 的 legacy 文档、config、schema、helper 之间并非完全一致
- 其中至少有一部分差距不是“表述粗细不同”，而是 contract 层级真的存在冲突
- 这些 gap 应先被显式登记，再决定是修 wiki、修代码，还是把它们改写成经过 adjudication 的 intentional difference

## 后续处理建议

- 先判定 GAP-AP-001 到 GAP-AP-006 各自属于：
  - wiki 吸收遗漏
  - legacy 文档漂移
  - legacy 代码 bug
  - intentional but undocumented behavior
- 在没有完成 adjudication 前，不应把这些差距静默覆盖进主结论页

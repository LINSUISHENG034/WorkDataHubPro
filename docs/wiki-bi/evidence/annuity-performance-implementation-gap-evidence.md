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
| GAP-AP-001 | input_contract | 已判定：非 gap | 当前 wiki 的最小输入骨架对齐的是 golden-set / durable Q&A 视角；代码里的 Bronze schema 属于更底层、更严格的校验层。两者层级不同，不再视为冲突项。 |
| GAP-AP-002 | input_contract | 已确认：wiki 过窄 | `pipeline_builder.py` 中 `CompanyIdResolutionStep` 会在缺失 `客户名称` 列时补空列继续处理，而 company_id 解析链也允许通过 plan-code 路径命中。因此 `客户名称` 缺失更应被视为降级输入，而不是绝对无效源。 |
| GAP-AP-003 | output_contract | 已确认：代码路径漂移 | annuity-performance 代码同时存在两套 Gold contract：`schemas.py` / `validate_gold_dataframe()` 定义了更严格的 Gold 要求，但 active `service.py` 并未调用 Gold validation，而是直接把结果送进 `helpers.py` 的 `convert_dataframe_to_models()`。因此这是“已存在但未执行的 stricter contract”与“active runtime path”之间的代码漂移。 |
| GAP-AP-004 | backfill_contract | 已确认：高概率代码问题 | `MappingStep` 使用 `df.rename(columns=...)`，会把 `机构` 改成 `机构名称`；而 `foreign_keys.yml` 的 `fk_organization` 仍从 source 字段 `机构` 回填目标 `机构`。GenericBackfillService 对缺失 source 字段会回填 `None`，因此这条配置与 canonical rows 高概率不一致。 |
| GAP-AP-005 | field_processing | 已确认：高概率代码问题 | `pipeline_builder.py` 先对 `集团企业客户号` 执行 `.astype(str).replace(\"nan\", None).str.lstrip(\"C\")`，真实 `None` 会先变成字符串 `\"None\"`，随后 Step 10 又把它复制到 `年金账户号`。这与“缺失应继续保持缺失”的语义不一致。 |
| GAP-AP-006 | field_processing | 已判定：非 gap | 当前代码里 `apply_plan_code_defaults()` 只对 `NaN` / `\"\"` 生效；在已知现实里，“空值”语义也正是这两类，因此 wiki 当前写法不再视为过宽。 |
| GAP-AP-007 | identity_processing | 已确认：实现文档 /代码存在优先级漂移 | `config.mapping_loader`、`company_id_resolver.py` facade、resolver `core.py` 仍把 YAML priority 叙述为 5 层（`plan -> account -> hardcode -> name -> account_name`），但 `resolver/yaml_strategy.py` 实际只执行 3 层（`plan -> hardcode -> name`），并明确说明 `account` / `account_name` 已移除。这说明 annuity-performance 所依赖的 identity 解析文档与实际实现存在漂移。 |

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
- 其中至少一部分差距已经可以确认属于 active runtime path 与声明 contract 的真实漂移
- 另有一部分差距已完成 adjudication，不再视为有效 gap
- 这些 gap 应先被显式登记，再决定是修 wiki、修代码，还是把它们改写成经过 adjudication 的 intentional difference

## 后续处理建议

- 先判定 GAP-AP-002 到 GAP-AP-007 各自属于：
  - wiki 吸收遗漏
  - legacy 文档漂移
  - legacy 代码 bug
  - intentional but undocumented behavior
- 在没有完成 adjudication 前，不应把这些差距静默覆盖进主结论页

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
| GAP-AP-002 | input_contract | 已判定：resolved_wiki_correction | `pipeline_builder.py` 中 `CompanyIdResolutionStep` 会在缺失 `客户名称` 列时补空列继续处理，而 company_id 解析链也允许通过 plan-code 路径命中。对应 wiki 已改写为“降级输入”，不再视为待处理 gap。 |
| GAP-AP-003 | output_contract | 已判定：resolved_code_fix | 已在 legacy `service.py` 中补上 `validate_gold_dataframe()`，使 annuity-performance active runtime path 与声明的 Gold contract 对齐；针对非法 Gold output 的回归测试现已通过。 |
| GAP-AP-004 | backfill_contract | 已判定：resolved_code_fix | 已将 legacy `foreign_keys.yml` 中 annuity-performance 的 `fk_organization` source 从 `机构` 修正为 canonical `机构名称`；针对 generic backfill candidate derivation 的回归测试现已通过。 |
| GAP-AP-005 | field_processing | 已判定：resolved_code_fix | 已将 legacy `pipeline_builder.py` 的 `集团企业客户号` 清洗改为保留真实空值语义，不再把 Python `None` 物化为字符串 `\"None\"` 再复制到 `年金账户号`；对应 null-handling 回归测试现已通过。 |
| GAP-AP-006 | field_processing | 已判定：非 gap | 当前代码里 `apply_plan_code_defaults()` 只对 `NaN` / `\"\"` 生效；在已知现实里，“空值”语义也正是这两类，因此 wiki 当前写法不再视为过宽。 |
| GAP-AP-007 | identity_processing | 已判定：resolved_drift_cleanup | 已在 legacy `mapping_loader.py`、`company_id_resolver.py` facade、resolver `__init__.py` 与 `core.py` 中收紧说明文字，明确区分 compatibility-era mapping inventory 与 active annuity-performance YAML execution path（`plan -> hardcode -> name`），不再把两者混写为同一条运行时优先级。 |

## 当前状态快照

### Resolved Wiki Corrections

- `GAP-AP-002`

### Resolved Code Fixes

- `GAP-AP-003`
- `GAP-AP-004`
- `GAP-AP-005`

### Resolved Drift Cleanup

- `GAP-AP-007`

### Intentional Differences

- none currently confirmed

### Non-Gaps

- `GAP-AP-001`
- `GAP-AP-006`

## 证据来源

- `E:\Projects\WorkDataHub\src\work_data_hub\domain\annuity_performance\pipeline_builder.py`
- `E:\Projects\WorkDataHub\src\work_data_hub\domain\annuity_performance\service.py`
- `E:\Projects\WorkDataHub\src\work_data_hub\domain\annuity_performance\helpers.py`
- `E:\Projects\WorkDataHub\src\work_data_hub\domain\annuity_performance\models.py`
- `E:\Projects\WorkDataHub\src\work_data_hub\domain\annuity_performance\schemas.py`
- `E:\Projects\WorkDataHub\src\work_data_hub\config\mapping_loader.py`
- `E:\Projects\WorkDataHub\src\work_data_hub\infrastructure\enrichment\company_id_resolver.py`
- `E:\Projects\WorkDataHub\src\work_data_hub\infrastructure\enrichment\resolver\__init__.py`
- `E:\Projects\WorkDataHub\src\work_data_hub\infrastructure\enrichment\resolver\core.py`
- `E:\Projects\WorkDataHub\src\work_data_hub\infrastructure\transforms\plan_portfolio_helpers.py`
- `E:\Projects\WorkDataHub\config\data_sources.yml`
- `E:\Projects\WorkDataHub\config\foreign_keys.yml`
- `E:\Projects\WorkDataHub\tests\unit\domain\annuity_performance\test_pipeline_builder.py`
- `E:\Projects\WorkDataHub\tests\unit\domain\annuity_performance\test_failed_records_export.py`
- `E:\Projects\WorkDataHub\tests\unit\domain\reference_backfill\test_generic_backfill_service.py`

## 当前可下的稳定结论

- annuity-performance 的 legacy 文档、config、schema、helper 之间并非完全一致
- 其中至少一部分差距已经可以确认属于 active runtime path 与声明 contract 的真实漂移
- 另有一部分差距已完成 adjudication，不再视为有效 gap
- 原先收敛为代码修复候选的 `GAP-AP-003`、`GAP-AP-004`、`GAP-AP-005` 已在 legacy 仓库完成定点修复
- 原先收敛为 stale drift 的 `GAP-AP-007` 已完成 resolver-facing 文档/注释清理
- 当前 annuity-performance gap register 中不再存在 active gap；剩余条目要么已关闭，要么已判定非 gap

## 后续处理建议

- 后续若再出现 annuity-performance contract drift，应直接新增新的 gap_id，而不是重开已关闭条目
- 维持 targeted regression coverage，重点关注 Gold validation、organization backfill candidate derivation 与 `年金账户号` 空值语义

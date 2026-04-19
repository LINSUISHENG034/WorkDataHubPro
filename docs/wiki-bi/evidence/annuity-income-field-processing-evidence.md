# `annuity_income` 字段处理证据

## 结论主题

本页把 `annuity_income` 的关键字段处理从“制度记忆碎片”提升为可复用的字段处理证据页。

重点不是重演 pipeline 顺序，而是区分：

- 工程性质量提升
- 直接改变业务解释的处理

## 证据记录

| evidence_id | source_type | evidence_strength | coverage_state | supported_pages | last_verified | notes |
|---|---|---|---|---|---|---|
| E-AI-FP-001 | legacy_doc | strong | absorbed | `annuity-income`, `annuity-income-input-contract`, `annuity-income-output-contract` | 2026-04-15 | `E:\Projects\WorkDataHub\docs\cleansing-rules\annuity-income.md` 明确 `annuity_income` 的主要字段处理、ID5 retirement 与 branch mapping 约束。 |
| E-AI-FP-002 | legacy_config | strong | absorbed | `annuity-income-input-contract`, `annuity-income-output-contract`, `backfill` | 2026-04-15 | `E:\Projects\WorkDataHub\config\data_sources.yml` 与 `E:\Projects\WorkDataHub\config\foreign_keys.yml` 固化输入发现规则、output destination 与 reference/customer backfill inventory。 |
| E-AI-FP-003 | current_test | strong | explicitly_tracked | `annuity-income`, `annuity-income-output-contract`, `annuity-income-operator-artifacts-evidence` | 2026-04-15 | `tests/integration/test_annuity_income_processing.py`、`tests/integration/test_annuity_income_operator_artifacts.py` 与 `tests/replay/test_annuity_income_slice.py` 共同证明 current project 已显式保护 branch mapping、temp-id fallback 与 artifact visibility。 |
| E-AI-FP-004 | current_runbook | supporting | explicitly_tracked | `annuity-income-input-contract`, `annuity-income-output-contract` | 2026-04-15 | `docs/runbooks/annuity-income-replay.md` 说明 current replay path 如何把 direct fact、identity 与 publication evidence 接回可执行 runbook。 |
| E-AI-FP-005 | legacy_code | strong | absorbed | `annuity-income-input-contract`, `annuity-income-output-contract`, `annuity-income` | 2026-04-16 | `E:\Projects\WorkDataHub\src\work_data_hub\domain\annuity_income\pipeline_builder.py` 明确 hidden semantics：`客户名称` 空值包含 `"0"` 占位、`单一计划 + 企业年金计划后缀` 才允许计划名提取、`年金账户名` 在清洗前复制保留。 |
| E-AI-FP-006 | legacy_code | strong | absorbed | `annuity-income-input-contract`, `annuity-income-output-contract` | 2026-04-16 | 同一 `pipeline_builder.py` 明确 `机构代码` fallback 链：`COMPANY_BRANCH_MAPPING` -> 源 `机构代码/机构` -> `G00`，并把字符串 `"null"` 视为无效值。 |
| E-AI-FP-007 | legacy_code | supporting | explicitly_tracked | `annuity-income-output-contract`, `annuity-income-operator-artifacts-evidence` | 2026-04-16 | `E:\Projects\WorkDataHub\src\work_data_hub\domain\annuity_income\helpers.py` 与 `service.py` 显示 operator artifact 与解析结果耦合，且 unknown-name 识别在 legacy 侧以 `company_id` 前缀 `IN` 为观测信号。 |
| E-AI-FP-008 | current_code | supporting | explicitly_tracked | `annuity-income-output-contract`, `annuity-income-operator-artifacts-evidence` | 2026-04-16 | `src/work_data_hub_pro/capabilities/fact_processing/annuity_income/service.py` 显示 current exporter 以 `resolution_method=temp_id_fallback` 触发 `unknown_names_csv`，并在 unresolved identity 时写出 `failed_records.csv`。 |

## 哪些来源是强证

- `annuity-income` cleansing rules
- `config/data_sources.yml`
- `config/foreign_keys.yml`
- current processing / operator-artifact / replay tests

## 哪些来源只是旁证

- current replay runbook

## 关键字段处理矩阵

| 字段 / 对象 | 处理后对象 | 类型 | 稳定规则 | 对输出的影响 |
|---|---|---|---|---|
| `月度` | canonical period | 工程性质量提升 | 中文日期标准化为统一 period 表达 | 决定 fact 与 replay 对齐 |
| `机构名称` | `机构代码` | 业务语义处理 | 通过 `COMPANY_BRANCH_MAPPING` 与 manual overrides 推导 branch code | 影响 identity 解释与 reference/customer signal |
| `计划号` / `计划代码` | canonical plan anchor | 业务语义处理 | 作为 company resolution 与 plan-level signal 的主要锚点 | 影响 fact identity 与 backfill |
| `客户名称` | normalized `客户名称` | 工程性质量提升 | 清理空白与标准化名称 | 影响 identity 解释与 explainability |
| `客户名称` | `年金账户名` | 业务语义处理 | 在清理前保留原始账户名线索 | 保留 operator / identity 审计线索 |
| `计划名称` + `计划类型` | 补全 `客户名称` | 业务语义处理 | 仅当 `单一计划` 且 `计划名称` 以 `企业年金计划` 结尾才提取公司名；不匹配不强补 | 防止集合计划或脏计划名被误当客户 |
| `组合代码` | canonical `组合代码` | 工程性质量提升 | regex 清洗 + conditional defaulting | 保护 portfolio anchor contract，并影响 portfolio-level signal |
| `业务类型` | `产品线代码` | 业务语义处理 | 映射到产品线编码 | 影响 output classification |
| `固费` / `浮费` / `回补` / `税` | canonical income facts | 工程性质量提升 | 数值清洗与默认值处理 | 决定 direct fact payload |
| unresolved identity | temp-id / artifacts | 业务语义处理 | 不恢复 ID5，改走 governed temp-id fallback 与 artifact 输出 | 决定 `company_reference`、`unknown_names_csv`、failed-record visibility |
| `company_id` | resolved identity | 业务语义处理 | active runtime path 依赖 cache / provider / temp-id fallback，而不是历史 ID5 | 决定 publication 与 replay 解释边界 |

## 显式空值 / 默认值规则

| 字段 | 空值 / 默认规则 | 说明 |
|---|---|---|
| `客户名称` | `null`、空字符串、`"0"` 视为空 | `"0"` 在 legacy source 中是占位符，不应进入业务客户名 |
| `机构代码` | 映射缺失或值为 `"null"` 时继续 fallback；最终默认 `G00` | 避免 source branch 字段脏值直接污染机构归属 |
| `固费` / `浮费` / `回补` / `税` | 缺失补 `0` | 保持明细行可计量，不把缺值误解释为整行无效 |
| `company_id` | 输入侧可缺失；解析阶段可落到 temp-id fallback | unresolved 需要外显 artifact，而不是删除记录 |

## 工程性质量提升

当前可稳定归入工程性质量提升的处理包括：

- 日期标准化
- 名称清洗与空白归一化
- 收入数值默认值与数值清洗
- `组合代码` 的格式修整与缺省补位，用于保护 portfolio anchor，而不是把它降级成纯显示字段

这些处理的目标是：

- 提高数据可消费性
- 减少脏值噪声
- 但不单独创造新的业务真理

## 业务语义处理

当前可稳定归入业务语义处理的处理包括：

- `机构名称 -> 机构代码` 的 branch mapping overrides
- 计划锚点参与的 identity resolution
- 不恢复 ID5 的 retirement boundary
- unresolved cases 的 operator artifact / signal 外显
- `计划类型`、`业务类型`、`组合代码` 与 customer-master `年金计划类型` / `管理资格` 属于同一 classification family 的不同层；统一解释见 [classification family 证据](./classification-family-evidence.md)、[管理资格](../concepts/management-qualification.md) 与 [组合代码](../concepts/portfolio-code.md)

这些规则会直接改变：

- 记录被归到哪个企业身份
- 哪个 branch 被视为解释该记录的机构
- 哪些输出必须显式暴露给 operator

## 当前实现证据

- `current_test`
  - `tests/integration/test_annuity_income_processing.py`
  - `tests/integration/test_annuity_income_operator_artifacts.py`
  - `tests/replay/test_annuity_income_slice.py`
- `current_reference_asset`
  - `reference/historical_replays/annuity_income/`
- `current_runbook`
  - `docs/runbooks/annuity-income-replay.md`

## 当前证据缺口

- legacy 与 current 对 `unknown_names_csv` 的触发谓词不同（`IN*` 标记 vs `temp_id_fallback`），目前缺少统一兼容断言测试来证明两者在边界场景等价
- legacy `service.py` 的 failed-record 导出受 `session_id` 影响，current exporter 则以 unresolved identity 直接导出；跨代行为差异尚未形成单页契约化证据
- 本页仅覆盖 `annuity_income`；shared cross-domain artifact parity 仍属于其他模块范围，保持为 evidence gap，不在本模块越界编辑

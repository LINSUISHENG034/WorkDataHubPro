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
| `组合代码` | canonical `组合代码` | 工程性质量提升 | regex 清洗 + conditional defaulting | 影响 portfolio-level signal |
| `业务类型` | `产品线代码` | 业务语义处理 | 映射到产品线编码 | 影响 output classification |
| `固费` / `浮费` / `回补` / `税` | canonical income facts | 工程性质量提升 | 数值清洗与默认值处理 | 决定 direct fact payload |
| unresolved identity | temp-id / artifacts | 业务语义处理 | 不恢复 ID5，改走 governed temp-id fallback 与 artifact 输出 | 决定 `company_reference`、`unknown_names_csv`、failed-record visibility |
| `company_id` | resolved identity | 业务语义处理 | active runtime path 依赖 cache / provider / temp-id fallback，而不是历史 ID5 | 决定 publication 与 replay 解释边界 |

## 工程性质量提升

当前可稳定归入工程性质量提升的处理包括：

- 日期标准化
- 名称清洗与空白归一化
- 收入数值默认值与数值清洗
- `组合代码` 的格式修整与缺省补位

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

## 仍需补强的缺口

- 当前已具备 contract-grade input / output / field-processing 入口，但尚未形成独立 implementation-gap audit page
- 后续如果 `annuity_income` 出现 wiki 与 current implementation 明显漂移，再按 domain-upgrade framework 追加 code-gap audit

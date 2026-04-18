# `annuity_performance` 字段处理证据

## 结论主题

本页把 `annuity_performance` 的字段处理拆成三层证据：

- raw-source 合同语义（legacy docs/config）
- 代码审计语义（legacy pipeline/service/schemas/helpers）
- current accepted slice 的可执行证据（tests/reference/runbook）

目标不是复述 pipeline，而是把隐藏字段语义与下游意义写成可审计结论。

## 证据记录

| evidence_id | source_type | evidence_strength | coverage_state | supported_pages | last_verified | notes |
|---|---|---|---|---|---|---|
| E-AP-FLD-001 | legacy_doc | strong | absorbed | `annuity-performance`, `annuity-performance-input-contract`, `annuity-performance-output-contract` | 2026-04-16 | `E:\Projects\WorkDataHub\docs/domains/annuity_performance.md` 固化输入发现、single-sheet、refresh key 与 backfill required 的 domain 合同。 |
| E-AP-FLD-002 | legacy_doc | strong | absorbed | `annuity-performance`, `annuity-performance-output-contract`, `backfill` | 2026-04-16 | `E:\Projects\WorkDataHub\docs/domains/annuity_performance-capability-map.md` 明确 direct fact -> backfill -> contract/snapshot 的链路和关键字段 trace。 |
| E-AP-FLD-003 | legacy_doc | strong | absorbed | `annuity-performance-input-contract`, `annuity-performance-output-contract` | 2026-04-16 | `E:\Projects\WorkDataHub\docs/cleansing-rules/annuity-performance.md` 给出列映射、defaulting、`company_id` 解析优先链与 `年金账户号` 派生。 |
| E-AP-FLD-004 | legacy_config | strong | absorbed | `annuity-performance-input-contract`, `annuity-performance-output-contract`, `backfill` | 2026-04-16 | `E:\Projects\WorkDataHub\config/data_sources.yml` 固化 workbook discovery（`file_patterns`、`exclude_patterns`、`highest_number`）与 output refresh key。 |
| E-AP-FLD-005 | legacy_config | strong | absorbed | `annuity-performance-output-contract`, `backfill`, `customer-status` | 2026-04-16 | `E:\Projects\WorkDataHub\config/foreign_keys.yml` 固化 `fk_plan`/`fk_customer` 的 `max_by`、`skip_blank_values`、`jsonb_append(tags)` 与 template 衍生。 |
| E-AP-FLD-006 | legacy_code | strong | absorbed | `annuity-performance-input-contract`, `annuity-performance-output-contract`, `company-id` | 2026-04-16 | `E:\Projects\WorkDataHub\src\work_data_hub\domain\annuity_performance\pipeline_builder.py` 证明 `客户名称 -> 年金账户名` 线索保留、`集团企业客户号 -> 年金账户号` 派生、`company_id` 解析链与 drop-before/after 边界。 |
| E-AP-FLD-007 | legacy_code | supporting | absorbed | `annuity-performance-input-contract`, `annuity-performance-implementation-gap-evidence` | 2026-04-16 | `E:\Projects\WorkDataHub\src\work_data_hub\domain\annuity_performance\helpers.py` 与 `schemas.py` 显示 row-level hard gate（`月度`/`计划代码`）与 Gold 侧 `company_id` 非空约束。 |
| E-AP-FLD-008 | current_test | strong | explicitly_tracked | `annuity-performance`, `annuity-performance-input-contract`, `annuity-performance-output-contract` | 2026-04-16 | `tests/integration/test_annuity_performance_intake.py`、`tests/integration/test_annuity_performance_processing.py`、`tests/replay/test_annuity_performance_slice.py` 共同证明 current slice 的 source-intake contract、cleansing trace 与 replay publication/projection 链闭环。 |
| E-AP-FLD-009 | current_reference_asset | strong | explicitly_tracked | `annuity-performance-output-contract`, `verification-assets-evidence`, `real-data-validation` | 2026-04-16 | `reference/historical_replays/annuity_performance/` 提供 accepted replay baseline 与 checkpoint baseline，支撑 direct fact 到 snapshot 的对比证据。 |
| E-AP-FLD-010 | current_runbook | supporting | explicitly_tracked | `annuity-performance-input-contract`, `annuity-performance-output-contract` | 2026-04-16 | `docs/runbooks/annuity-performance-replay.md` 把 replay entrypoints、compatibility case 处理与 temp-id salt 前置条件落到 operator 路径。 |

## 字段处理矩阵

| 字段 | 处理类型 | 处理说明 | 业务语义 |
|---|---|---|---|
| `月度` | 工程性质量提升 | 中文日期格式标准化 | 把原始 period 变成可用于事实、回填和 snapshot 的统一时间锚点 |
| `计划代码` | 双重：工程 + 业务 | 先做特例修正，再按 `计划类型` 在缺失时补默认值 | 既保证键的可用性，也决定计划对象如何被识别 |
| `业务类型` | 业务语义处理 | 映射为 `产品线代码` | 把源业务分类转成后续 join / snapshot / backfill 的稳定产品线键 |
| `机构` / `机构名称` | 双重：工程 + 业务 | 列重命名后再映射为 `机构代码`，并处理 branch overrides/default | 将机构文本转成受治理的组织对象 |
| `组合代码` | 工程性质量提升 | 去掉前缀 `F`，并在缺失时按业务类型/计划类型补默认 | 让 portfolio 相关引用具备稳定格式 |
| `客户名称` | 双重：工程 + 业务 | 先复制为 `年金账户名`，再做名称归一 | 既保护 identity clue，又保持清洗后的统一客户名称 |
| `年金账户名` | 业务语义处理 | 保留清洗前 clue 供 identity 解析使用 | 不是显示字段，而是 identity governance 的线索保留 |
| `集团企业客户号` -> `年金账户号` | 业务语义处理 | 去掉前缀 `C` 后派生到账户号 | 为 identity 解析与后续账户相关解释保留结构化线索 |
| `company_id` | 业务语义处理 | 经多线索解析链得到 | 是跨事实、回填、contract、snapshot 的稳定身份锚点 |
| `期末资产规模` | 业务语义处理 | 在 `fk_plan` / `fk_customer` 中作为 `max_by` 排序列 | 决定主拓机构、关键年金计划等“主导值” |
| `company_id`（temp-id） | 业务语义处理 | `fk_customer.skip_blank_values=true` 下 temp-id（`IN*`）不回填客户主数据 | 区分“事实可落地”与“客户主数据可固化”边界 |
| `customer."客户明细".tags` | 业务语义处理 | 通过 backfill 聚合生成如 `yyMM新建` | 这是从事实域派生出的 customer 侧经营轨迹 |
| `customer."客户年金计划".contract_status` | 业务语义处理 | 从 fact + contract sync 规则派生 | 直接影响 contract 状态与后续 snapshot |
| `customer."客户业务月度快照"` / `customer."客户计划月度快照"` | 业务语义处理 | 基于 fact、contract 与状态规则生成 | 是 annuity-performance 最重要的下游派生输出之一 |

## 显式空值 / 默认值规则

| 字段 | 空值 / 默认规则 | 说明 |
|---|---|---|
| `计划代码` | 空值按 `计划类型` 补默认 | `集合计划 -> AN001`，`单一计划 -> AN002` |
| `机构代码` | 映射缺失或映射结果为 `null` 时补 `G00` | 代表总部默认代码 |
| `组合代码` | 空值先看 `业务类型`，再看 `计划类型` | `职年受托/职年投资 -> QTAN003`；否则按 `计划类型` 补 `QTAN001/QTAN002` |
| `客户名称` | 空值不自动补业务默认值 | 只做 trim / normalize；其缺失会削弱 identity 解释能力，但在 `计划代码` 可用时不必然阻断 runtime 处理 |
| `集团企业客户号` | 清洗时去掉前缀 `C` | 作为派生 `年金账户号` 的输入线索 |
| `年金账户号` | 来自清洗后的 `集团企业客户号` | 属于派生线索，不是源字段直接照搬 |
| 数值字段 | 多种空值占位符清洗为 `None` | 包括 `""`、`-`、`N/A`、`无`、`暂无`、`null`、`NULL`、`None` |
| 百分比字段 | `%` 形式转成小数 | 例如收益率类字段按比例归一 |
| row-level 记录生存 | 缺失 `月度` 或 `计划代码` 的行会在模型转换阶段被丢弃 | 这属于处理链硬门槛，不应被误写为“仅告警不影响记录” |

## 稳定结论

- 列重命名、日期标准化、prefix 清理、null/default 处理这类动作主要属于工程性数据质量提升
- identity resolution、plan-code defaulting、backfill 聚合、contract / snapshot 派生这类动作属于明确业务语义处理
- 某些字段同时跨两类，例如 `计划代码`、`客户名称`、`机构代码`，因为它们先要被清洗成可用格式，之后才进入业务解释
- `annuity_performance` 的隐藏字段语义不是“字段数量”，而是字段在 direct fact、backfill、snapshot 三层里的角色迁移
- `计划类型`、`业务类型`、`组合代码` 与 customer-master `年金计划类型` / `管理资格` 属于同一 classification family 的不同层；统一解释见 [classification family 证据](./classification-family-evidence.md) 与 [管理资格](../concepts/management-qualification.md)

## 哪些来源是强证

- legacy domain docs / capability map / cleansing rules
- legacy config（`data_sources.yml` + `foreign_keys.yml`）
- legacy pipeline code（`pipeline_builder.py`）与 current replay/intake/processing tests

## 哪些来源用于代码审计补强

- `E:\Projects\WorkDataHub\src\work_data_hub\domain\annuity_performance\helpers.py`
- `E:\Projects\WorkDataHub\src\work_data_hub\domain\annuity_performance\schemas.py`
- `E:\Projects\WorkDataHub\src\work_data_hub\domain\annuity_performance\service.py`

## 哪些来源只是旁证

- legacy runbook 与 current replay runbook

## 当前证据缺口

- current `wiki-bi` 尚未为 annuity-performance 建立独立 operator-artifacts evidence page（unknown-names / failed-row 导出语义仍分散在跨域证据页）
- legacy `service.py` 中 drop-rate warning 与 failed-row export 规则尚未形成 annuity-performance 专属 contract 条款，当前仅作为审计补强
- 若后续需要把 `skip_blank_values` 的 temp-id 过滤升级为 current runtime 明示合同，需要跨入 reference/customer 模块证据，不在本模块内直接改写

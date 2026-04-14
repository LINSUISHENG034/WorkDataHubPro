# `annuity_performance` 字段处理证据

## 结论主题

本页把 `annuity_performance` 的字段处理拆成两类：

- 数据质量提升的工程手段
- 基于明确业务语义的数据处理

这样做的目的不是复制 pipeline 步骤，而是让人能判断每类处理“为什么存在”。

## 证据记录

| evidence_id | source_type | evidence_strength | coverage_state | supported_pages | last_verified | notes |
|---|---|---|---|---|---|---|
| E-AP-FLD-001 | legacy_doc | strong | absorbed | `annuity-performance`, `annuity-performance-input-contract`, `annuity-performance-output-contract` | 2026-04-14 | `docs/cleansing-rules/annuity-performance.md` 给出输入字段、列映射、清洗规则、company_id 解析链与输出目标，是最直接的字段处理 raw source。 |
| E-AP-FLD-002 | legacy_doc | strong | absorbed | `annuity-performance`, `annuity-performance-output-contract`, `backfill` | 2026-04-14 | `docs/domains/annuity_performance-capability-map.md` 把 direct fact output、backfill targets、derived downstream tables 与关键字段 trace 明确写实。 |
| E-AP-FLD-003 | legacy_config | strong | absorbed | `annuity-performance-input-contract`, `annuity-performance-output-contract`, `backfill` | 2026-04-14 | `config/data_sources.yml` 与 `config/foreign_keys.yml` 分别给出 source discovery contract 与 backfill target contract。 |
| E-AP-FLD-004 | legacy_doc | supporting | absorbed | `annuity-performance-output-contract`, `customer-status` | 2026-04-14 | `docs/verification_guide_real_data.md` 说明 contract / snapshot / status 的验证路径，证明 annuity-performance 的下游派生不是抽象推断。 |

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
| `customer."客户明细".tags` | 业务语义处理 | 通过 backfill 聚合生成如 `yyMM新建` | 这是从事实域派生出的 customer 侧经营轨迹 |
| `customer."客户年金计划".contract_status` | 业务语义处理 | 从 fact + contract sync 规则派生 | 直接影响 contract 状态与后续 snapshot |
| `customer."客户业务月度快照"` / `customer."客户计划月度快照"` | 业务语义处理 | 基于 fact、contract 与状态规则生成 | 是 annuity-performance 最重要的下游派生输出之一 |

## 稳定结论

- 列重命名、日期标准化、prefix 清理、null/default 处理这类动作主要属于工程性数据质量提升
- identity resolution、plan-code defaulting、backfill 聚合、contract / snapshot 派生这类动作属于明确业务语义处理
- 某些字段同时跨两类，例如 `计划代码`、`客户名称`、`机构代码`，因为它们先要被清洗成可用格式，之后才进入业务解释

## 哪些来源是强证

- `annuity-performance` cleansing rules
- `annuity_performance` capability map
- `data_sources.yml` / `foreign_keys.yml`

## 哪些来源只是旁证

- real-data verification guide

## 当前证据缺口

- current `wiki-bi` 仍未把 annuity-performance 的 source workbook shape 拆成更细对象级输入证据
- 还没有为 annuity-performance 的每个 downstream sink 建独立 evidence page；当前阶段不需要机械拆分

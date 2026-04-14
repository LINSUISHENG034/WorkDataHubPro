# Round 11：Phase E operator/runtime surfaces decision package

> 状态：Completed
> 日期：2026-04-14
> 主题簇：follow-on / Phase E surfaces / decision package

## 本轮目标

- 把 Phase E operator/runtime surfaces 从“已知存在”推进到“可直接引用的治理对象簇”
- 不再只把 enterprise persistence、standalone tooling、manual operator controls 混写在同一张主题 evidence page 中
- 为后续 `retain / replace / retire / defer` 讨论准备更清晰的 durable decision package

## 使用的 raw sources

- `E:\Projects\WorkDataHub\src\work_data_hub\cli\__main__.py`
- `E:\Projects\WorkDataHub\src\work_data_hub\cli\cleanse_data.py`
- `E:\Projects\WorkDataHub\src\work_data_hub\gui\eqc_query\controller.py`
- `E:\Projects\WorkDataHub\src\work_data_hub\gui\eqc_query\app.py`
- `E:\Projects\WorkDataHub\src\work_data_hub\gui\eqc_query_fluent\app.py`
- `E:\Projects\WorkDataHub\src\work_data_hub\gui\intranet_deploy\app.py`
- `E:\Projects\WorkDataHub\src\work_data_hub\gui\intranet_deploy\controller.py`
- `E:\Projects\WorkDataHub\src\work_data_hub\infrastructure\enrichment\resolver\backflow.py`
- `E:\Projects\WorkDataHub\src\work_data_hub\infrastructure\enrichment\repository\other_ops.py`
- `E:\Projects\WorkDataHub\src\work_data_hub\infrastructure\enrichment\eqc_provider.py`
- `E:\Projects\WorkDataHub\config\reference_sync.yml`
- `E:\Projects\WorkDataHub\docs\deployment_run_guide.md`
- 现有 `wiki-bi` 中的 surface / evidence / roadmap 页面

## 本轮吸收的 Stable Findings

- `reference_sync` 是带有 target inventory、schedule、source mode 与 sync contract 的显式配置治理 surface，不应退化成泛化 backfill helper
- `company_lookup_queue` 是 temp-id 之后的 async lookup runtime，带有 `pending` / `processing` 去重与 graceful degradation 语义
- `enterprise.enrichment_index`、`enterprise.enrichment_requests`、`enterprise.base_info` 共同构成 identity 相关 persistence surface，应作为一个可讨论的对象簇被显式登记
- standalone `cleanse` CLI 与多种 GUI 工具确实是 operator-facing tooling，但不应自动提升为 rebuild 的核心 business/runtime truth
- manual `customer-mdm` commands 既是 operator controls，也是恢复/重算 contract、snapshot 与 annual lifecycle 的正式入口

## 本轮更新的目标页

- `docs/wiki-bi/evidence/operator-and-surface-evidence.md`
- `docs/wiki-bi/surfaces/reference-sync.md`
- `docs/wiki-bi/surfaces/company-lookup-queue.md`
- `docs/wiki-bi/surfaces/customer-mdm-commands.md`
- `docs/wiki-bi/surfaces/enterprise-enrichment-persistence.md`
- `docs/wiki-bi/surfaces/standalone-tooling.md`
- `docs/wiki-bi/index.md`

## 可复用经验

- surface 治理的下一步不总是“再建更大的总览页”，很多时候更高价值的是把混在一起的对象簇拆成几个真正独立的治理对象
- 对 legacy tooling 的处理要同时避免两个极端：既不能因为它们不在主 ETL path 就当作不存在，也不能因为它们有独立入口就自动视为产品核心
- 对 persistence surface，最重要的不是记录表名本身，而是记录谁写、谁读、承载什么运行语义、哪些语义不能静默丢失

## 下一轮建议

- 进入 Round 12，把 validation result history、error-case fixtures 与 domain-level golden set 的治理边界收紧
- 如果后续确实进入 Phase E 设计/实现讨论，再基于本轮对象簇做 `retain / replace / retire / defer` 的更细分决策

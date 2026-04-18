# Round 29：legacy 业务语义扩展包

> 状态：Planned
> 日期：2026-04-18
> 主题簇：legacy business semantics / object promotion / classification family

## 为什么现在做

- Round 28 已经把 `tags`、`主拓机构` 与 customer-master-derived signal family 收紧成 durable objects + dispatcher，但仍有一批高价值业务对象停留在 dispatcher 或 aggregate narrative 中。
- semantic map 当前的覆盖率已经足够高，下一步不该继续只做发现账本扩写，而应把已经成熟的 business semantics 提升到 `docs/wiki-bi/` 主体。
- 本轮刻意只处理 business semantics，不顺手扩张到 queue、`reference_sync`、manual commands、standalone tooling 等 runtime/operator closure。

## 本轮目标

- 把 customer-master relationship breadth 相关对象从 dispatcher 提升成更可直接问答的 durable 入口。
- 把 `is_churned_this_year` 从 aggregate status 叙事推进到对象级语义入口，同时保留粒度分裂与 AUM 汇总边界。
- 把 `计划类型`、`业务类型`、`管理资格`、`组合代码`、`年金计划类型` 之间的跨层语义收紧成一组可复用的 business classification package。

## 建议包序

### Package A：customer-master relationship breadth

优先对象：

- `关键年金计划`
- `关联计划数`
- `其他年金计划`
- `其他开拓机构`

建议写法：

- 先更新 [customer-master signals 证据](../../evidence/customer-master-signals-evidence.md)，把 dominant value、relationship breadth 与 customer-master label 三类子对象拆开表述。
- 只优先提升最能独立回答“它是什么 / 它不是什么 / 为什么重要”的对象页；默认先考虑 `关键年金计划`，再评估 `关联计划数` 是否达到独立页阈值。
- `其他年金计划` 与 `其他开拓机构` 默认先留在 dispatcher，除非本轮证据显示它们已具有稳定独立语义，而不只是解释性附属字段。

推荐 raw sources：

- `E:\Projects\WorkDataHub\config\foreign_keys.yml`
- `E:\Projects\WorkDataHub\docs\verification_guide_real_data.md`
- `E:\Projects\WorkDataHub\docs\domains\annuity_performance-capability-map.md`
- `E:\Projects\WorkDataHub\docs\domains\annuity_income-capability-map.md`
- `E:\Projects\WorkDataHub\docs\domains\annual_award-capability-map.md`
- `E:\Projects\WorkDataHub\docs\domains\annual_loss-capability-map.md`

### Package B：`is_churned_this_year` 对象级收口

目标：

- 新增对象级 evidence 入口，明确它是 monthly churn judgement，而不是年度流失申报事实。
- 把 product-line 粒度与 plan-level 变体放在同一对象族下解释，避免继续让“还没拆页”成为长期理由。
- 显式接回 `customer_status_rules.yml`、verification SQL 与 semantic-map mature claims。

推荐 durable targets：

- 新增 `evidence/is-churned-this-year-evidence.md`
- 更新 [客户状态总览](../../concepts/customer-status.md)
- 更新 [客户状态语义正确性](../../standards/semantic-correctness/customer-status-semantics.md)
- 更新 [状态与快照证据](../../evidence/status-and-snapshot-evidence.md)

推荐 raw sources：

- `E:\Projects\WorkDataHub\config\customer_status_rules.yml`
- `E:\Projects\WorkDataHub\docs\business-background\客户主数据回填与状态来源分析.md`
- `E:\Projects\WorkDataHub\docs\verification_guide_real_data.md`
- `docs/wiki-bi/_meta/legacy-semantic-map/semantic/rules/sem-rule-is-churned-this-year-definition.yaml`
- `docs/wiki-bi/_meta/legacy-semantic-map/semantic/rules/sem-grain-split-is-churned-this-year.yaml`

### Package C：classification family 收紧

目标对象：

- `计划类型`
- `业务类型`
- `管理资格`
- `组合代码`
- `年金计划类型`

本轮要回答的问题：

- `计划类型` 与 `年金计划类型` 的关系是什么，为什么不能互换？
- `业务类型` 什么时候是输入分类，什么时候被提升成 `管理资格` 或 `产品线代码` 的解释锚点？
- `组合代码` 在业务上是 portfolio/classification 语义，还是 identity 线索，边界在哪里？

建议写法：

- 稳定业务意义留在概念 / 标准页，域内实现步骤继续留在字段处理证据页。
- 默认先补一个 cross-domain evidence dispatcher，再决定是否拆出 `管理资格` 或 `组合代码` 的独立 concept page。
- 不把 cleansing rule 顺序、regex 细节或 defaulting 分支直接写成 product truth；这些只作为 evidence records 留存。

推荐 raw sources：

- `E:\Projects\WorkDataHub\docs\business-background\年金计划类型与客户名称业务背景.md`
- `E:\Projects\WorkDataHub\docs\cleansing-rules\annuity-performance.md`
- `E:\Projects\WorkDataHub\docs\cleansing-rules\annuity-income.md`
- `E:\Projects\WorkDataHub\docs\verification_guide_real_data.md`
- `E:\Projects\WorkDataHub\config\foreign_keys.yml`

## 本轮不处理

- `company_lookup_queue`、`reference_sync`、enterprise persistence、manual `customer-mdm` commands 等 Phase E runtime/operator closure
- semantic map registry / compiler / wave plumbing 本身
- 把 legacy cleansing / capability-map 文档逐页镜像进 wiki

## 完成定义

- 至少一个目前仍停留在 dispatcher 的 business object 被提升成 durable object page。
- `is_churned_this_year` 不再只留在 aggregate status page 的一句说明里。
- classification family 至少形成一个 cross-domain dispatcher 或一组收紧后的概念/标准入口，而不是继续散落在各域字段处理页。
- `docs/wiki-bi/index.md`、`docs/wiki-bi/log.md`、`docs/wiki-bi/_meta/absorption-rounds/index.md` 与 `docs/wiki-bi/_meta/wiki-absorption-roadmap.md` 同轮回写。

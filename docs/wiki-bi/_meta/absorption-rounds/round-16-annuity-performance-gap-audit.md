# Round 16：`annuity_performance` implementation gap audit

> 状态：Completed
> 日期：2026-04-14
> 主题簇：maintenance / implementation-gap audit

## 本轮目标

- 在补完 annuity-performance 合同页之后，直接回到 legacy 代码核对 wiki 是否与实现一致
- 把差距项从聊天中的临时判断，沉淀成 durable gap evidence
- 不急于决定 blame 归属，而是先显式列出 contract-level mismatch

## 使用的 raw sources

- `E:\Projects\WorkDataHub\src\work_data_hub\domain\annuity_performance\pipeline_builder.py`
- `E:\Projects\WorkDataHub\src\work_data_hub\domain\annuity_performance\service.py`
- `E:\Projects\WorkDataHub\src\work_data_hub\domain\annuity_performance\helpers.py`
- `E:\Projects\WorkDataHub\src\work_data_hub\domain\annuity_performance\models.py`
- `E:\Projects\WorkDataHub\src\work_data_hub\domain\annuity_performance\schemas.py`
- `E:\Projects\WorkDataHub\src\work_data_hub\infrastructure\transforms\plan_portfolio_helpers.py`
- `E:\Projects\WorkDataHub\config\data_sources.yml`
- `E:\Projects\WorkDataHub\config\foreign_keys.yml`
- 刚更新后的 annuity-performance wiki contract / evidence pages

## 本轮吸收的 Stable Findings

- wiki 与 legacy 代码在 annuity-performance 的 contract 层并非完全一致
- 主要差距集中在：
  - required skeleton 口径
  - output row 过滤口径
  - backfill source 字段一致性
  - 空值清洗后的派生字段语义
- 审核 follow-up 进一步确认：其中有些是层级差异，不再视为 gap；另一些已经足够明确到可以认定为 wiki 过窄或高概率代码问题
- 继续代码核对后，剩余 active gaps 已经可以分流成：
  - code-fix candidates
  - stale documentation drift
- 后续执行阶段已在 legacy 仓库中关闭 `GAP-AP-003`、`GAP-AP-004`、`GAP-AP-005` 三个代码候选，并清理 `GAP-AP-007` 的 resolver-facing stale drift
- 这些差距已经足够厚，值得单独立一页 implementation gap evidence

## 本轮更新的目标页

- `docs/wiki-bi/evidence/annuity-performance-field-processing-evidence.md`
- `docs/wiki-bi/evidence/annuity-performance-implementation-gap-evidence.md`
- `docs/wiki-bi/index.md`
- `docs/superpowers/plans/2026-04-14-annuity-performance-code-gap-fixes.md`
- `docs/superpowers/plans/2026-04-14-annuity-performance-contract-drift-adjudication.md`

## 可复用经验

- 当 wiki 开始具备合同级表达后，下一步最自然的动作就是回到代码核 contract drift
- “wiki 说得更清楚”并不等于“代码就一定符合 wiki”；
  反过来也一样
- 对实现差距最稳妥的处理方式，是先登记为 gap evidence，再决定是否升格为主结论修订

## 下一步建议

- 本轮原先登记的 active gaps 已完成收口；后续仅在出现新的 contract drift 时再开新条目
- 如果未来再次出现“schema contract 与 active runtime path 脱节”，优先先补 targeted regression，再回写 gap register

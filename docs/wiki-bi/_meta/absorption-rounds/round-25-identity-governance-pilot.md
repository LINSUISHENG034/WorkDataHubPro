# Round 25：identity governance pilot

> 状态：Completed
> 日期：2026-04-16
> 主题簇：identity-governance / pilot

## 本轮目标

- 深化 `company_id` / `temp_id` / identity governance 的语义表达，显式分离 active runtime path、compatibility inventory / historical memory、retired fallback behavior、operator-visible consequence
- 保持 `company_lookup_queue` 与 `enterprise enrichment persistence` 作为两个独立 surface，不再合并叙述
- 将未闭环事项继续保留在 evidence gaps，不把 deferred runtime 写成稳定结论

## Prompt Changes From Round 24

- 提前强制四层分离措辞，禁止把 historical memory 或 deferred runtime 混写为 active runtime path
- 提前要求 queue surface 与 persistence surface 分页收口，不允许“identity runtime 一页通吃”
- 提前要求 unresolved 相关结论必须带 operator-visible consequence 或 evidence-gap 去向

## Review Friction Reduced

- 评审可直接按四层分离检查语义正确性，减少“这句到底在讲 current 还是 legacy memory”的来回确认
- queue 与 persistence 分页后，runtime 语义与 durable 对象族边界更清晰，减少跨页冲突
- evidence gaps 的入口更稳定，避免把未验证实现误判为已承接

## Review Friction Still Present

- 部分聚合页仍容易把 historical memory 写成“默认现行行为”，需要继续收紧 wording
- active runtime path 与 deferred runtime 的边界仍依赖 reviewer 逐条核验证据引用
- prompt 中“不要合并相邻 surface”已更清楚，但仍可能在摘要段落被弱化

## Adjustments Required Before Parallel Execution

- 在并行波次前，把四层分离检查问句纳入每个模块 review checklist（必须逐条回答）
- 控制器侧增加“queue vs persistence split”硬门槛，未通过则不得进入集成回写
- 继续要求 integration files（`index.md`、`log.md`、round note）在同一 closure change 落地

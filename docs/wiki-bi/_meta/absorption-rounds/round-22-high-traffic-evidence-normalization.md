# Round 22：high-traffic evidence normalization

> 状态：Planned
> 日期：2026-04-15
> 主题簇：planned / evidence pages / normalization

## 本轮目标

- 把高流量 aggregate evidence pages 逐步收紧到 Round 19 确认的最小模板
- 优先处理仍承担大量入口职责的 evidence pages，而不是一次性批量重写全部历史页
- 让后续 lint 能基于更一致的 evidence 结构执行，而不是继续依赖页面作者的自由发挥

## 启动理由

- Round 19 已经把 evidence 最小模板写入 [wiki-design](./../wiki-design.md) 与 [wiki maintenance lint checklist](./../wiki-maintenance-lint-checklist.md)
- 当前高流量页如 [状态与快照证据](./../../evidence/status-and-snapshot-evidence.md)、[验证资产证据](./../../evidence/verification-assets-evidence.md)、[operator 与 surface 证据](./../../evidence/operator-and-surface-evidence.md) 的结构仍不完全一致
- 这类收紧工作只有在高价值结论已基本稳定后才值得做；Round 20 / 21 之后是合适窗口

## 计划读取的 raw sources

- `docs/wiki-bi/_meta/wiki-design.md`
- `docs/wiki-bi/_meta/wiki-maintenance-lint-checklist.md`
- `docs/wiki-bi/evidence/status-and-snapshot-evidence.md`
- `docs/wiki-bi/evidence/verification-assets-evidence.md`
- `docs/wiki-bi/evidence/operator-and-surface-evidence.md`
- 相关对象级 evidence pages，用于确认哪些内容应继续留在 aggregate page，哪些应只保留 dispatcher 角色

## 计划更新的目标页

- `docs/wiki-bi/evidence/status-and-snapshot-evidence.md`
- `docs/wiki-bi/evidence/verification-assets-evidence.md`
- `docs/wiki-bi/evidence/operator-and-surface-evidence.md`
- 必要时更新 `docs/wiki-bi/_meta/wiki-design.md`
- 必要时更新 `docs/wiki-bi/_meta/wiki-maintenance-lint-checklist.md`

## 完成定义

- 目标 aggregate evidence pages 都具备一致的 `结论主题`、`证据记录`、强证 / 旁证区分与 `当前证据缺口`
- aggregate page 与对象级 evidence page 的 dispatcher 边界更清楚，不再重复承载同一层细节
- lint 可以直接用这些页面验证模板一致性，而不是每次先解释“这页是特殊情况”
- 本轮产出与 Round 19 规则一致：durable pages、`HH:MM` 日志、round note / lint summary 同轮回写

## 后续依赖

- 如果在模板归一过程中发现新的稳定对象已满足拆分阈值，应优先创建对象级 evidence page，而不是继续把厚内容堆回 aggregate page

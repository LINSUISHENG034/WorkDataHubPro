# Round 22：high-traffic evidence normalization

> 状态：Completed
> 日期：2026-04-15
> 主题簇：maintenance / evidence pages / normalization

## 本轮目标

- 把高流量 aggregate evidence pages 逐步收紧到 Round 19 确认的最小模板
- 优先处理仍承担大量入口职责的 evidence pages，而不是一次性批量重写全部历史页
- 让后续 lint 能基于更一致的 evidence 结构执行，而不是继续依赖页面作者的自由发挥

## 启动理由

- Round 19 已经把 evidence 最小模板写入 [wiki-design](./../wiki-design.md) 与 [wiki maintenance lint checklist](./../wiki-maintenance-lint-checklist.md)
- 当前高流量页如 [状态与快照证据](./../../evidence/status-and-snapshot-evidence.md)、[验证资产证据](./../../evidence/verification-assets-evidence.md)、[operator 与 surface 证据](./../../evidence/operator-and-surface-evidence.md) 的结构仍不完全一致
- 这类收紧工作只有在高价值结论已基本稳定后才值得做；Round 20 / 21 之后是合适窗口

## 使用的 raw sources

- `docs/wiki-bi/_meta/wiki-design.md`
- `docs/wiki-bi/_meta/wiki-maintenance-lint-checklist.md`
- `docs/wiki-bi/evidence/status-and-snapshot-evidence.md`
- `docs/wiki-bi/evidence/verification-assets-evidence.md`
- `docs/wiki-bi/evidence/operator-and-surface-evidence.md`
- `docs/wiki-bi/evidence/is-new-evidence.md`
- `docs/wiki-bi/evidence/is-winning-this-year-evidence.md`
- `docs/wiki-bi/evidence/is-loss-reported-evidence.md`
- 相关对象级 evidence pages，用于确认哪些内容应继续留在 aggregate page，哪些应只保留 dispatcher 角色

## 本轮吸收的 Stable Findings

- 高流量 aggregate evidence page 的主要漂移不在证据表本身，而在表后 section 的自由发挥
- 对 aggregate evidence page 来说，最稳定的归一骨架应是：`结论主题`、`证据记录`、强证 / 旁证、dispatcher 边界、对象级补强页、`当前证据缺口`
- `status-and-snapshot-evidence` 仍需要承担共享状态语义与未拆对象的容器角色，因此不应被机械拆薄
- `verification-assets-evidence` 与 `operator-and-surface-evidence` 已经形成 decision package，但仍应把对象级分发入口与 aggregate dispatcher 角色显式分开

## 本轮更新的目标页

- `docs/wiki-bi/evidence/status-and-snapshot-evidence.md`
- `docs/wiki-bi/evidence/verification-assets-evidence.md`
- `docs/wiki-bi/evidence/operator-and-surface-evidence.md`
- `docs/wiki-bi/index.md`
- `docs/wiki-bi/_meta/absorption-rounds/index.md`
- `docs/wiki-bi/_meta/wiki-absorption-roadmap.md`

## 可复用经验

- evidence page 的模板归一不需要追求 section 名完全机械一致，但至少应让 dispatcher 边界与对象级分发入口一眼可见
- 当 aggregate page 已承担 round-specific decision package 时，不必删掉决策表；更高价值的是在其前后补齐统一骨架
- 若对象级 evidence page 已存在，aggregate page 应尽量回到 dispatcher 角色，而不是继续双写完整细节

## 下一步建议

- 后续如再触碰其他 aggregate evidence page，应直接套用本轮归一后的 section 顺序，而不是重新发明局部模板
- 如果在后续维护中发现新的稳定对象已满足拆分阈值，应优先创建对象级 evidence page，而不是继续把厚内容堆回 aggregate page

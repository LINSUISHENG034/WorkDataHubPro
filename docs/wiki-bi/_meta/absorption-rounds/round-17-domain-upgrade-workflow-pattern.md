# Round 17：domain upgrade workflow pattern

> 状态：Completed
> 日期：2026-04-14
> 主题簇：maintenance / reusable workflow pattern

## 本轮目标

- 把 `annuity_performance` 这次有效的 wiki 升级路径提炼成可复用工作流
- 让下次更新其他 domain 时，不需要重新发明“从导航页到合同页，再到 gap audit”的方法
- 给 `wiki-bi` 增加一个真正可复用的 meta-level 维护框架

## 使用的 raw sources

- `docs/wiki-bi/_meta/wiki-design.md`
- `docs/wiki-bi/_meta/wiki-absorption-workflow.md`
- `docs/wiki-bi/_meta/absorption-rounds/round-15-annuity-performance-io-contracts.md`
- `docs/wiki-bi/_meta/absorption-rounds/round-16-annuity-performance-gap-audit.md`
- `docs/wiki-bi/index.md`
- `docs/wiki-bi/log.md`

## 本轮吸收的 Stable Findings

- 对高价值 domain，单靠导航页通常不足以支撑 operator-grade 问答
- 一个有效的 domain wiki 升级流程，应先补 `input contract`、`output contract`、`field-processing evidence`
- 只有在合同级页面已经成型后，才值得追加 `implementation-gap audit`
- “先让 wiki 能答，再去查实现 drift” 是比“先看代码再写 wiki”更稳的顺序

## 本轮更新的目标页

- `docs/wiki-bi/_meta/wiki-domain-upgrade-framework.md`
- `docs/wiki-bi/index.md`
- `docs/wiki-bi/log.md`
- `docs/wiki-bi/_meta/absorption-rounds/index.md`

## 可复用经验

- 通用框架应写在 `_meta/`，而不是继续塞进某个 round 纪要里
- round 纪要更适合承载“这次如何把框架跑通”的样板实例
- 最好同时保留：
  - 一个通用框架页
  - 一个真实 domain 样板

## 下一步建议

- 后续如果用这个框架更新 `annual_award` 或 `annual_loss`，应优先比较它们是否也值得补合同级页面
- 如果某个主题不是 domain，而是 surface 或单个 concept，不要机械套用这个框架

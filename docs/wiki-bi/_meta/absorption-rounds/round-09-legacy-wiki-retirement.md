# Round 09：legacy wiki 退役收口

> 类型：follow-on absorption round
> 日期：2026-04-14
> 目标：把 `docs/wiki-cn/` 从并行 wiki 收口为 retired navigation layer，并明确 durable 归宿

## 本轮使用的 raw sources

- `docs/wiki-cn/` 现存页面
- `docs/system/index.md`
- `docs/system/document-authority-model.md`
- `docs/wiki-bi/index.md`
- `docs/wiki-bi/_meta/wiki-design.md`
- `docs/superpowers/specs/2026-04-11-workdatahubpro-rebuild-architecture-draft.md`
- `docs/superpowers/specs/2026-04-11-workdatahubpro-refactor-program.md`
- `.planning/ROADMAP.md`
- `.planning/PROJECT.md`

## 本轮稳定结论

- `docs/wiki-cn/` 不再作为 `WorkDataHubPro` 的 durable knowledge layer 继续维护。
- `project/`、`roadmap/`、`phases/` 这类页面更接近产品级入口或 framework workflow 入口，应导回 `docs/system/`、`docs/superpowers/specs/` 与 `.planning/`。
- `governance/` 下稳定的业务语义、验收标准、surface 与 evidence 已由 `docs/wiki-bi/` 承接，不应继续在旧 wiki 保留并行正文。
- `lessons/` 与 `wiki-cn/_meta/` 中的大部分内容属于历史 phase trace 或旧 schema，应保留 provenance，但不再承担当前 durable 规则角色。
- 对仍可能被旧链接引用的 legacy wiki 路径，优先改为 retired stub，而不是直接物理删除。

## 本轮执行结果

- 重写 `docs/wiki-cn/index.md`，把入口切换为 `docs/system/`、`docs/wiki-bi/`、framework specs 与 `.planning/`
- 将 `docs/wiki-cn/` 下现存正文页统一改为 retired stub，并为每页明确“现在去哪里看”
- 保留 `docs/wiki-cn/log.md` 时间线，但增加退役收口记录，说明旧层已退出 durable 维护

## 2026-04-14 follow-up：physical removal

- 活跃测试已改为读取 `.planning/` 文档，而不再依赖 `docs/wiki-cn/`
- `reference/verification_assets/phase2-accepted-slices.json` 已改为指向 `docs/wiki-bi/` 的 current durable pages
- active skill/docs 中对 `docs/wiki-cn/` 的当前时态引用已改成 former/legacy 表述
- `docs/wiki-cn/` 已从当前仓库树中物理删除；后续回溯依赖 git history 与本轮沉淀页

## 可复用经验

- 退役 legacy wiki 时，优先保持路径稳定，再收紧正文角色；这样可以避免清理动作本身制造新的断链成本。
- 当旧页面混合了 durable knowledge、framework workflow 与 current-state 叙述时，应先按 authority layer 重新分流，再决定是否删除。
- “显式判定为历史 trace” 也是一种有效收口结果，不需要把所有旧内容都硬塞进新的 durable page。

## 下一步入口

- 后续新增 durable wiki 内容，只写入 `docs/system/` 或 `docs/wiki-bi/` 的正确层级。
- 如果未来确认某些 retired stub 已无入链且无 provenance 价值，可再做一轮物理删除清理。

# wiki maintenance lint checklist

## Purpose

为 `docs/wiki-bi/` 的 substantial maintenance round 提供一个轻量完工 gate。

它的目标不是替代审计，而是避免维护者在页面已改动后遗漏最常见的闭环动作。

## 何时使用

- durable page 有实质变化
- 新增了 contract / evidence / meta page
- 某个 gap 的 disposition 被更新
- 当前实现证据被写回 wiki

## Checks

- 本轮变更过的 durable pages 已在 `docs/wiki-bi/index.md` 中可达
- `docs/wiki-bi/log.md` 已追加同轮日志，且标题使用 `YYYY-MM-DD HH:MM`
- 本轮变更过的 evidence pages 仍保持最小模板：`结论主题` + `证据记录` + 强/旁证区分 + `当前证据缺口`
- active gap 没有停留在“已讨论但无 disposition”的中间状态
- implementation-backed 结论在可行处显式写入 `current_test`、`current_reference_asset`、`current_runbook`
- domain page -> standards / evidence 与 evidence -> supported pages 的主链路仍然可追踪
- 没有为了补信息而新建本可落到既有 object page 的宽泛 summary page
- substantial round 已留下 round note，或至少有一段可回溯的 lint 结果摘要

## Exclusion

`docs/wiki-bi/_meta/legacy-semantic-map/` 不属于 durable wiki page family。

因此这棵子树：

- 不参加 `docs/wiki-bi/index.md` 可达性检查
- 不参加 concept / standard / domain / surface / evidence 模板检查
- 不因未被 catalog 收录而被视为 lint failure

如果本轮改动了 semantic map 子树，应该改查：

- `docs/wiki-bi/index.md` 仍然没有收录 `legacy-semantic-map`
- `docs/wiki-bi/_meta/legacy-semantic-map/README.md` 仍明确写着 `not durable wiki content`
- `README.md` 仍写着 active owner 与 archive trigger

## 推荐执行方式

完成一轮 substantial maintenance 后，至少做下面两步：

1. `rg -n "<new-page-or-keyword>" docs/wiki-bi`
2. `git diff -- docs/wiki-bi docs/superpowers/plans`

如果这两步暴露出页面不可达、日志缺失或结论漂移，应先修正再结束本轮。

建议将本轮固定产物理解为：

1. 更新后的 durable pages
2. 一条带 `HH:MM` 的 `log.md` 记录
3. 一个 round note，或至少一段 lint 结果摘要

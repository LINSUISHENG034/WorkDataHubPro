# Round 10：domain 导航与 cross-reference 收紧

> 状态：Completed
> 日期：2026-04-14
> 主题簇：maintenance / wiki lint / navigation tightening

## 本轮目标

- 对当前 `docs/wiki-bi/` 做一次 maintenance-oriented lint，检查断链、孤页与低入链 durable pages
- 在不创建重复 summary page 的前提下，把 event-style domains 接回概念、标准、证据与其他 domain 页
- 把本轮维护经验沉淀为后续 wiki lint 的可复用入口

## 使用的 raw sources

- `docs/wiki-bi/index.md`
- `docs/wiki-bi/log.md`
- `docs/wiki-bi/_meta/wiki-design.md`
- `docs/wiki-bi/_meta/wiki-absorption-workflow.md`
- `docs/wiki-bi/domains/annual-award.md`
- `docs/wiki-bi/domains/annual-loss.md`
- `docs/wiki-bi/domains/annuity-performance.md`
- `docs/wiki-bi/concepts/customer-status.md`
- `docs/wiki-bi/standards/semantic-correctness/customer-status-semantics.md`
- `docs/wiki-bi/standards/input-reality/input-reality-contracts.md`
- `docs/wiki-bi/standards/verification-method/golden-scenarios.md`
- `docs/wiki-bi/evidence/status-and-snapshot-evidence.md`

## 本轮吸收的 Stable Findings

- 当前 `wiki-bi` 没有断链，也没有完全无入链的 durable page，但 `annual_award` 与 `annual_loss` 这类 event-style domains 仍然存在“几乎只靠首页进入”的导航弱点
- 这类问题更适合通过 `update-existing` 收紧 cross-reference 来修复，而不是新增更宽泛的 summary page
- 对 event-style domains，最自然的回链入口是客户状态、输入现实、验证方法与状态证据页，而不是额外再造一层 domain 总览

## 本轮更新的目标页

- `docs/wiki-bi/domains/annual-award.md`
- `docs/wiki-bi/domains/annual-loss.md`
- `docs/wiki-bi/domains/annuity-performance.md`
- `docs/wiki-bi/concepts/customer-status.md`
- `docs/wiki-bi/standards/semantic-correctness/customer-status-semantics.md`
- `docs/wiki-bi/standards/input-reality/input-reality-contracts.md`
- `docs/wiki-bi/standards/verification-method/golden-scenarios.md`
- `docs/wiki-bi/evidence/status-and-snapshot-evidence.md`
- `docs/wiki-bi/index.md`

## 可复用经验

- `wiki-bi` 的 lint 不应只看断链；低入链 durable pages 同样会削弱知识对象的长期可达性
- 当某个 domain 在业务上本来就是概念、标准与证据的交汇点时，应优先把这些现有页互相接回，而不是新增“中间导航页”
- 维护轮次同样应遵守 `index.md` 与 `log.md` 同轮回写规则，否则 wiki 会逐步偏离自身 schema

## 下一轮建议

- 对 `wiki-bi` 继续做对象级 inbound-link lint，优先检查是否还有 durable page 只有首页单点入链
- 如果后续 `is_winning_this_year` / `is_loss_reported` 被拆成对象级 evidence page，应同步把对应 domain 页接回这些新对象

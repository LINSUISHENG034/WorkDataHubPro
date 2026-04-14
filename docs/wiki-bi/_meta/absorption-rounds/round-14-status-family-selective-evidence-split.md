# Round 14：status family selective evidence split

> 状态：Completed
> 日期：2026-04-14
> 主题簇：follow-on / selective object-level evidence split

## 本轮目标

- 不机械地把所有状态都拆成单页
- 只拆出真正满足对象级 evidence 阈值的状态对象
- 显式说明哪些状态继续留在主题型 evidence page 更合理

## 使用的 raw sources

- `docs/wiki-bi/evidence/status-and-snapshot-evidence.md`
- `docs/wiki-bi/concepts/customer-status.md`
- `docs/wiki-bi/standards/semantic-correctness/customer-status-semantics.md`
- `docs/wiki-bi/evidence/is-new-evidence.md`
- `docs/wiki-bi/domains/annual-award.md`
- `docs/wiki-bi/domains/annual-loss.md`
- `E:\Projects\WorkDataHub\config\customer_status_rules.yml`
- `E:\Projects\WorkDataHub\docs\verification_guide_real_data.md`
- `E:\Projects\WorkDataHub\tests\slice_tests\test_g_snapshot_status.py`
- `E:\Projects\WorkDataHub\tests\slice_tests\test_i_snapshot_refresh_contract.py`

## 本轮吸收的 Stable Findings

- `is_winning_this_year` 满足对象级 evidence 拆分阈值：有独立事实来源、独立验证 SQL、被多个页面频繁引用，并且直接作为 `is_new` 的上游条件
- `is_loss_reported` 也满足对象级 evidence 拆分阈值：有独立事实来源、独立验证 SQL、且其语义边界与 `is_churned_this_year` 不同
- `is_churned_this_year` 当前不适合强行拆页，因为它同时牵涉 product-line / plan 双粒度、AUM 汇总语义与 plan-level 变体
- selective split 比“把剩余状态全部拆完”更符合 `wiki-bi` 的对象阈值规则

## 本轮更新的目标页

- `docs/wiki-bi/evidence/is-winning-this-year-evidence.md`
- `docs/wiki-bi/evidence/is-loss-reported-evidence.md`
- `docs/wiki-bi/evidence/status-and-snapshot-evidence.md`
- `docs/wiki-bi/concepts/customer-status.md`
- `docs/wiki-bi/standards/semantic-correctness/customer-status-semantics.md`
- `docs/wiki-bi/domains/annual-award.md`
- `docs/wiki-bi/domains/annual-loss.md`
- `docs/wiki-bi/index.md`

## 可复用经验

- 最适合对象级拆分的状态，通常具备三点：独立事实来源、独立验证路径、跨多个页面的高频引用
- 即使某个对象“理论上也能拆”，如果它还夹着多个粒度或派生层次，继续留在主题页往往更稳
- selective split 的价值在于减少未来重复分析，而不是追求“状态对象数目上的完整”

## 下一步建议

- 当前没有新的高收益预设 round 必须继续执行
- 后续更适合回到机会式维护：只在实现、验证或治理决策引入新的稳定结论时再做增量写回

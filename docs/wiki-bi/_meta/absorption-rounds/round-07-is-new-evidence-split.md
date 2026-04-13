# Round 07：`is_new` 对象级证据拆分

> 状态：Completed
> 日期：2026-04-14
> 主题簇：follow-on / object-level evidence split

## 本轮目标

- 从厚主题 evidence page 中拆出一个真正值得单独引用的对象级 evidence page
- 验证“对象级 evidence 拆分”这类 follow-on work 能否形成稳定闭环

## 使用的 raw sources

- `E:\Projects\WorkDataHub\docs\business-background\客户主数据回填与状态来源分析.md`
- `E:\Projects\WorkDataHub\config\customer_status_rules.yml`
- `E:\Projects\WorkDataHub\docs\verification_guide_real_data.md`
- 现有 `wiki-bi` 中与状态与快照相关的吸收结果

## 本轮吸收的 Stable Findings

- `is_new` 已满足对象级 evidence page 的拆分阈值
- `is_new` 的强证主要来自业务背景文档与 config contract
- `is_new` 的 operator 验证路径可由 verification guide 补强
- 对象级 evidence 拆分可以在不破坏主题型 evidence page 的前提下增强引用精度

## 本轮更新的目标页

- `evidence/is-new-evidence.md`
- `concepts/is-new.md`
- `concepts/customer-status.md`
- `standards/semantic-correctness/customer-status-semantics.md`
- `evidence/status-and-snapshot-evidence.md`

## 可复用经验

- 对象级 evidence page 不应从零开始讲大背景，而应只承载该对象的强证、稳定结论与缺口
- 主题型 evidence page 在拆分后仍有价值，适合作为总览和余下对象的容器
- 最适合率先拆分的对象，通常是：高频引用、强证集中、粒度边界清楚、非例明确

## 下一轮建议

如果继续做 follow-on work，下一步最自然的是：

- `is_winning_this_year` 对象级证据拆分
- `is_loss_reported` 对象级证据拆分
- 或 `annuity_income` branch mapping / ID5 / unknown-name artifact 的更细对象级拆分

# `wiki-bi` 吸收工作流

> 状态：Active
> 日期：2026-04-14
> 作用：定义如何把 legacy docs、config、tests、audits 持续吸收进 `wiki-bi`

---

## 1. 目标

`wiki-bi` 的内容吸收不是“把材料搬进 wiki”，而是：

- 从 raw sources 中提取稳定结论
- 把可复用综合判断写入 wiki 主体
- 把未决问题和证据关系沉淀到 `evidence/`
- 让每一轮吸收都能产出可复用经验和下一轮目标

## 2. 工作流

每轮吸收统一按下面顺序执行：

1. 选择一个主题簇
2. 收集并核对 raw sources
3. 先更新 `evidence/`
4. 再更新相关 `concepts/`、`standards/`、`surfaces/`、`domains/`
5. 回写 `index.md`
6. 追加 `log.md`
7. 产出轮次沉淀文档

## 3. 主题簇优先级

默认吸收顺序如下：

1. 状态与快照
2. 身份与补查
3. 输入现实
4. 验证资产
5. operator / surfaces
6. `annuity_income` 专题补强

## 4. 分类 gate

所有待吸收信息都必须先经过 4 层分类：

- `Stable Finding`
- `Evidence Record`
- `Open Question`
- `Working Trace`

规则：

- 只有 `Stable Finding` 才能进入 wiki 主结论层
- `Evidence Record` 和 `Open Question` 优先进入 `evidence/`
- `Working Trace` 保留在 raw sources 或轮次沉淀中

## 5. 每轮的最小输出

每一轮吸收至少应产出：

- 1 个被实质更新的 evidence page
- 1 个被实质更新的 concept / standard / surface / domain page
- 1 条 `log.md` 记录
- 1 份轮次沉淀文档

## 6. 每轮验收清单

一轮吸收完成后，至少检查：

- 新写入的稳定结论都有强证据或多源互证
- open question 没有混入主结论
- 新页和更新页都已进入 `index.md`
- 没有断链
- 没有新增孤页
- 轮次沉淀已经写入 `absorption-rounds/`

## 7. 轮次沉淀要求

每轮结束后，都必须在 `docs/wiki-bi/_meta/absorption-rounds/` 留下一份文档，记录：

- 本轮主题
- 使用的 raw sources
- 吸收进 wiki 的 stable findings
- 可复用经验
- 下一轮目标与入口页

这样做的目的不是写会议纪要，而是让下一轮吸收有明确起点，并形成正向循环。

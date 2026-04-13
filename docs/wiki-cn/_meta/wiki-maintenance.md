# 本仓库 Wiki 维护约定

> 类型：维护约定
> 日期：2026-04-13
> 作用：把 `LLM Wiki` 的抽象模式实例化到 `WorkDataHubPro`

---

## 1. 三层模型在本仓库里的对应关系

`LLM Wiki` 提到的三层模型，在本仓库中对应为：

- raw sources
  - `.planning/` 当前执行与状态文档
  - `docs/superpowers/specs/` 中的 active blueprint、refactor program、coverage matrix
  - `docs/disciplines/` 中与当前动作直接相关的规则
  - `src/`、`tests/`、`config/`、`reference/` 中的已实现事实与验证资产
  - 需要判断 legacy behavior 时，旧项目 `E:\Projects\WorkDataHub` 的代码与稳定资产
- the wiki
  - `docs/wiki-cn/` 下的中文 durable knowledge pages
- the schema
  - 仓库根 `AGENTS.md`
  - `wdhp-governance` 协作技能
  - 相关 discipline docs

对当前仓库来说，`docs/gsd/` 默认属于 working material，不是 durable wiki，也不是 current-state source of truth。

---

## 2. 本 wiki 的角色边界

`docs/wiki-cn/` 用来沉淀下面三类稳定知识：

- 项目是什么
- 当前主路线图和治理基线是什么
- 已经被验证过、未来还会反复复用的经验是什么

它不负责替代下面这些对象：

- `.planning/`
  - 当前 phase、plan、verification 的执行态细节
- 代码与测试
  - 当前仓库实际支持什么
- 一次性审计工作稿
  - 例如 `docs/gsd/` 下的灰区讨论、一次性调查和候选清单

当 wiki、`.planning/`、代码彼此冲突时：

- current-state claim 先看代码与测试
- 当前推进状态再看 `.planning/`
- wiki 负责把稳定结论写成可复用说明，并显式记录冲突已经如何被澄清

---

## 3. 页面类型

当前中文 wiki 采用下面几类页面：

- `project/`
  - 项目定位、边界、约束、风险与当前主线状态
- `roadmap/`
  - 主路线图、phase 顺序、当前推进判断
- `phases/`
  - 按 phase 聚合决策页、经验页与阶段间衔接信息
- `governance/`
  - 治理模型、决策基线、verification asset 与 legacy surface 结论
- `lessons/`
  - 已经足够稳定、可跨 phase 复用的经验
- `_meta/`
  - 说明 wiki 的维护方式、抽象来源和本仓库约定

只有当一个结论已经足够稳定、未来会被反复引用时，才应进入这些页面。

---

## 4. 更新工作流

### 4.1 Ingest stable conclusion

当一项结论已经从讨论、计划或审查中稳定下来时：

1. 先确认 source of truth
   - 状态类结论看代码、测试和 `.planning/`
   - 治理类结论看 specs、disciplines、accepted decisions 与 executed evidence
2. 更新最贴近主题的现有页面
3. 如果现有页面装不下，再新增 durable page
4. 同步更新 `index.md`
5. 追加 `log.md`

### 4.2 Query the wiki

查询或回答问题时，默认顺序是：

1. 先读 `docs/wiki-cn/index.md`
2. 再进入相关主题索引页或正文页
3. 如果状态判断会影响结论，再回源到 `.planning/`、代码、测试或 blueprint

### 4.3 Lint the wiki

定期做 wiki health check，至少检查：

- 是否有陈旧状态表述
- 是否有 planning、wiki、代码三方冲突但未显式写出
- 是否有 durable page 没进根索引
- 是否有 orphan page 只有文件存在、没有被其他页面引用
- 是否有重要概念已经反复出现但还没有独立页面
- 是否有日志记录了新增/重构，但索引和交叉链接没有同步

---

## 5. `index.md` 与 `log.md` 的合同

### `index.md`

根索引必须满足：

- content-oriented，而不是只做少数入口页导航
- 列出当前所有 durable page
- 每个页面都有一句可快速判断用途的 summary
- 新增 durable page 时同一轮更新

### `log.md`

日志必须满足：

- append-only
- 按时间顺序记录新增、重构、同步、lint
- 标题采用可扫描格式，例如 `## [2026-04-13] lint | 主题`

日志不是内容页目录，索引也不代替时间线；两者都要维护。

---

## 6. 什么时候新建页面

下面几种情况，可以考虑从索引或长页中拆出新页面：

- 某个 phase 已经同时拥有稳定状态、决策基线、经验教训与后续 admission 规则
- 某个治理对象会被多次引用，例如 verification asset、operator surface、failure contract
- 某项经验已经超出单次复盘，足以变成跨 phase 的复用规则

新页面一旦创建，至少要同步：

- `index.md`
- 相关主题索引页
- `log.md`

---

## 7. 当前维护重点

截至 2026-04-13，当前中文 wiki 的维护重点是：

- 保持 root index 真正覆盖全量 durable page
- 把 Phase 2、Phase 3 与后续主线的治理状态写准确
- 让 phase、governance、lesson 三类页面之间保持可追踪的交叉链接
- 避免把 `.planning/` 的执行态草稿或 `docs/gsd/` 的工作材料直接当成 durable knowledge

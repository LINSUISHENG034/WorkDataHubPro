# `wiki-bi` 轻量实施计划

> 状态：Active
> 日期：2026-04-14
> 依据：`wiki-design.md`
> 目的：把 `docs/wiki-bi/` 从 schema 设计推进到首批可用 wiki

---

## 1. 实施目标

本计划不再讨论顶层 schema，而是完成 `wiki-bi` 的首批可用落地：

- 建立 `docs/wiki-bi/` 的目录骨架
- 建立 `index.md` 与 `log.md`
- 建立首批 `concepts/`、`domains/`、`surfaces/`、`standards/`、`evidence/` 页面
- 让首页已经能回答首批高价值问题
- 让首批页面之间具备稳定交叉引用

## 2. 首批范围

本轮实施只覆盖首批 seed pages，不做下面事项：

- 不尝试一次性吸收全部 legacy 文档
- 不追求覆盖所有 concept / surface / standard
- 不把所有 audit candidates 都转成独立页面
- 不把 `wiki-bi` 做成完整的 legacy 镜像

## 3. 实施顺序

### Step 1. Scaffold

- 创建 `concepts/`
- 创建 `domains/`
- 创建 `surfaces/`
- 创建 `standards/` 下 4 个子目录
- 创建 `evidence/`

### Step 2. Root Files

- 创建 `index.md`
- 创建 `log.md`

### Step 3. Seed Concepts

首批建立：

- `company-id.md`
- `customer-status.md`
- `is-new.md`
- `customer-type.md`
- `plan-type.md`
- `snapshot-granularity.md`
- `backfill.md`

### Step 4. Seed Standards

首批建立：

- `standards/input-reality/input-reality-contracts.md`
- `standards/semantic-correctness/customer-status-semantics.md`
- `standards/output-correctness/output-correctness.md`
- `standards/verification-method/real-data-validation.md`
- `standards/verification-method/golden-scenarios.md`

### Step 5. Seed Surfaces

首批建立：

- `company-lookup-queue.md`
- `reference-sync.md`
- `customer-mdm-commands.md`
- `failed-record-export.md`
- `unknown-names-csv.md`

### Step 6. Seed Domains

首批建立：

- `annuity-performance.md`
- `annual-award.md`
- `annual-loss.md`
- `annuity-income.md`

### Step 7. Seed Evidence

首批建立：

- `input-reality-evidence.md`
- `identity-and-lookup-evidence.md`
- `status-and-snapshot-evidence.md`
- `verification-assets-evidence.md`
- `operator-and-surface-evidence.md`

### Step 8. Verification

- 确认所有新页面都被 `index.md` 编目
- 确认 FAQ 卡片都能落到真实页面
- 确认核心页面之间存在交叉链接
- 确认 `log.md` 已记录本轮 seed scaffold

## 4. 完成定义

本轮实施完成的标准是：

- `docs/wiki-bi/` 已经不再是空目录
- 首页已具备三层导航
- 首批高价值问题已有落点
- 证据容器页已能承接后续吸收工作
- 首批页面已形成最小知识网络，而不是孤页集合

## 5. 风险控制

- 如果某个主题尚未形成稳定结论，只保留到 `evidence/`，不硬写成 `concept` / `standard`
- 如果某个页面内容过薄，不为凑数量强行拆页
- 如果首批 evidence 容器已足够承接，就不提前拆第二批对象级 evidence 页

## 6. 验证方式

- docs-only link and coverage check
- root index completeness check
- orphan-page spot check
- manual review of page naming against `wiki-design.md`

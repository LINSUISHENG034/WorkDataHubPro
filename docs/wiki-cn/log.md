# Wiki Log

## [2026-04-12] seed | WorkDataHubPro 中文 wiki 初始化

- 新增 `index.md`
- 新增 `00-project-background.md`
- 新增 `10-development-roadmap.md`
- 接入已有经验页 `2026-04-12-phase1-planning-review-lessons.md`
- 形成中文 wiki 最小骨架：索引、背景、计划、经验、日志

## [2026-04-12] update | 同步 Phase 1 完成状态

- 更新 `00-project-background.md`，补充“Phase 1 已完成”和当前主线状态
- 更新 `10-development-roadmap.md`，将“推荐从 Phase 1 开始”改为“当前转向 Phase 2”
- 保持 wiki 与 `.planning/PROJECT.md`、`.planning/REQUIREMENTS.md` 当前状态一致

## [2026-04-12] refactor | 重组 wiki 目录结构

- 将 `llm-wiki.md` 移入 `_meta/`
- 将项目背景页移入 `project/background.md`
- 将路线图页移入 `roadmap/overview.md`
- 将经验页移入 `lessons/planning-and-evidence.md`
- 新增 `phases/index.md` 与 `governance/index.md` 作为后续扩展入口
- 更新根索引以反映新的两层语义结构

## [2026-04-12] governance | 沉淀 Phase 2 决策基线

- 新增 `governance/phase-2-decisions.md`
- 记录 Phase 2 的五项已确认决策：checkpoint、adjudication、contract strictness、CI、evidence shape
- 明确 `source_intake` 采用 `real-data-style` 目标基线
- 明确当前简化 workbook 输入仅作为 deterministic test fixture
- 补充三个 accepted slice 的 intake baseline 口径
- 更新治理索引与路线图页面以指向该决策页

## [2026-04-12] governance | 增补 verification assets 与防遗漏规则

- 扩写 `governance/phase-2-decisions.md`，新增 verification asset governance 与 `forgotten mechanism sweep`
- 新增 `governance/verification-assets.md`
- 明确 `golden set` 是一等 verification asset，而不是测试附件
- 明确新 phase / 新 slice 进入规划前必须做一次防遗漏扫描
- 更新治理索引与路线图页面，接入 verification assets 入口

## [2026-04-12] governance | 吸收 legacy 审计稳定结论

- 新增 `governance/legacy-audit-baseline.md`
- 只吸收 2026-04-12 audit 中已稳定的治理结论，不复制候选清单与一次性调查明细
- 明确 `company_lookup_queue`、`reference_sync`、enterprise persistence、manual `customer-mdm` commands、shared operator artifacts 都是需要显式治理的 legacy surfaces
- 在 `governance/verification-assets.md` 补充审计后确认的资产缺口口径
- 更新治理索引，接入新的审计基线页

## [2026-04-12] governance | 前置当前开发速记

- 在 `governance/legacy-audit-baseline.md` 增加“开发速记”，把最常用的治理约束前置
- 在 `roadmap/overview.md` 增加“当前开发必记”，减少 roadmap、governance、audit 之间的查阅跳转
- 明确 first-wave 未闭合面不只包括 `annuity_income`，还包括显式登记的 cross-cutting runtime / operator surfaces

## [2026-04-13] lessons | 沉淀 Phase 2 完成审查经验

- 新增 `lessons/phase-2-governance-review-lessons.md`
- 抽象出 5 条可复用经验：checkpoint 真实性、baseline 资产强依赖、实现完成与治理签收分层、evidence diff 准确性、planning/code/wiki 冲突显式记录
- 更新 `index.md`，把新的 lesson 接入中文 wiki 根索引
- 更新 `roadmap/overview.md`，补记 2026-04-13 的治理审查状态差异

## [2026-04-13] sync | Phase 6 治理状态同步 — Phase 2 governance sign-off 已闭合

- Phase 2 实现已完成：显式 stage contracts、确定性 parity gates、derivation checkpoint governance、CI-ready gate tiers 均已到位
- Phase 2 governance sign-off 已闭合：Phase 6 truthful intermediate gates、stable intermediate payload normalization、diff accuracy remediation、以及 governance status sync 已全部完成
- Phase 6 包含 3 个 plan：06-01（fail-closed baseline + bootstrap + diff 修正）、06-02（truthful intermediate checkpoint wiring）、06-03（governance 状态同步 + contract coverage）
- 验证命令：`uv run pytest tests/contracts/test_phase6_gate_runtime.py tests/contracts/test_phase2_governance_status_sync.py -v`（`9 passed`）
- 验证命令：`uv run pytest tests/replay/test_phase2_reference_derivation_gates.py tests/replay/test_phase2_event_domain_gates.py tests/replay/test_annuity_performance_slice.py tests/replay/test_annual_award_slice.py tests/replay/test_annual_loss_slice.py -v`（`15 passed`）

## [2026-04-13] governance | 基于 Phase 6 闭合结果更新中文 wiki

- 更新 `project/background.md`，把当前状态从“转向 Phase 2”改为“Phase 2 已闭环，后续应转回 post-Phase-2 主线”
- 更新 `roadmap/overview.md`，补充 verification-asset contract suite，并明确当前不应继续把 Phase 2 补口叙述视为 active target
- 更新 `governance/verification-assets.md`，明确 `source_intake` 是 contract checkpoint，不是 `checkpoint_baseline` 文件资产
- 更新 `governance/phase-2-decisions.md`，补记当前稳定口径：accepted checkpoint baseline 仅覆盖 `reference_derivation`、`fact_processing`、`identity_resolution`、`contract_state`

## [2026-04-13] governance | 沉淀 Phase 3 灰区拍板决策

- 新增 `governance/phase-3-decisions.md`
- 把 Phase 3 的四项灰区结论沉淀为稳定治理页：replay 共享边界、failure contract、agent 入口、temp-id policy
- 明确 Phase 3 不采用 fully generic replay runner，而采用 `shared primitives + explicit per-domain runners`
- 明确 failure contract 采用 `typed run report + typed exceptions`
- 明确 replay 入口采用“保留 domain wrapper + 新增 unified replay surface”
- 明确 temp-id 采用 legacy-backed 的确定性 opaque 规则，prefix 默认 `IN`
- 更新 `governance/index.md` 与 `roadmap/overview.md`，把新决策页接入当前路线图语境

## [2026-04-13] sync | Phase 03.1 治理状态同步 — Phase 3 governance sign-off 已闭合

- Phase 3 实现已完成：shared replay primitives、typed diagnostics、replay CLI entrypoints 均已到位
- Phase 3 governance sign-off 已闭合（2026-04-13）：Phase 03.1 remediation 解决了 2026-04-13 Phase 3 审核中发现的三个问题
- Phase 03.1 包含 3 个 plan：03.1-01（truthful failed-checkpoint compatibility-case payload selection）、03.1-02（fail-closed diagnose package-path enforcement + typed invalid-id CLI）、03.1-03（governance artifact 同步 + Phase 3 governance-status contract coverage）
- 验证命令：`uv run pytest tests/contracts/test_phase3_governance_status_sync.py -v`
- 状态文档同步：`.planning/STATE.md`、`.planning/ROADMAP.md`、`.planning/PROJECT.md`、`03-VERIFICATION.md`、`docs/wiki-cn/roadmap/overview.md` 均已更新为"Phase 3 governance sign-off closed"表述

## [2026-04-13] lint | 按 `LLM Wiki` 模式重整中文 wiki 编目与维护约定

- 更新 `index.md`，把根索引从最小入口页整理为全量 durable page catalog，并为每页补一句 summary
- 新增 `_meta/wiki-maintenance.md`，把 `LLM Wiki` 的 source / wiki / schema / lint 模式实例化到当前仓库
- 更新 `phases/index.md`，把占位页改为按 Phase 聚合的导航页
- 更新 `roadmap/overview.md`，补回 Phase 3 审核经验的交叉引用，消除当前 orphan lesson

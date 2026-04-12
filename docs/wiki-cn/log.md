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

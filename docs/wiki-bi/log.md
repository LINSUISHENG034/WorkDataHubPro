# Wiki BI Log

## [2026-04-14] remove | 物理删除 legacy wiki layer

- 在删除前已将活跃测试、verification-asset `reference_location`、以及 active skill/docs 中的旧 wiki 路径迁移到 `docs/wiki-bi/`、`docs/system/` 或 `.planning/`
- 旧 wiki 目录已从当前仓库树中移除
- 其历史 provenance 由 git history、`.planning/` 历史材料以及 `docs/wiki-bi/_meta/absorption-rounds/round-09-legacy-wiki-retirement.md` 承接

## [2026-04-14] retire | 收口 legacy wiki layer

- 将旧 wiki 层先改写为 retired stub，再完成物理移除
- `project/`、`roadmap/`、`phases/` 路径统一改指 `docs/system/`、`docs/superpowers/specs/` 与 `.planning/`
- `governance/`、`lessons/`、`_meta/` 路径统一改指 `docs/wiki-bi/`、`docs/disciplines/` 与 `docs/system/`
- 新增 `round-09-legacy-wiki-retirement.md`，把这次退役动作沉淀为正式 absorption round

## [2026-04-14] scaffold | 初始化 `wiki-bi` 首批可用结构

- 新增 `_meta/wiki-implementation-plan.md`，将设计文档转为首批实施顺序与完成定义
- 新增 `index.md`，采用“阅读意图主轴 + 常见问题卡片 + 全量 catalog”的三层导航
- 新增 `log.md`，作为 append-only 时间线
- 新增首批 `concepts/`、`domains/`、`surfaces/`、`standards/`、`evidence/` seed pages
- 首批内容目标是建立知识骨架与稳定入口，不是一次性吸收全部 legacy 材料

## [2026-04-14] absorb | Round 01 闭环吸收 `status-and-snapshot`

- 新增 `_meta/wiki-absorption-workflow.md` 与 `_meta/wiki-absorption-roadmap.md`，把后续内容吸收机制和整体顺序显式化
- 新增 `_meta/absorption-rounds/index.md` 与 `round-01-status-and-snapshot.md`，把本轮经验与下一轮入口沉淀为可复用资产
- 更新 `evidence/status-and-snapshot-evidence.md`，将状态来源、粒度边界、customer MDM surface 相关 strong/supporting evidence 聚合并区分
- 更新 `concepts/customer-status.md`、`concepts/is-new.md`、`concepts/customer-type.md`、`concepts/snapshot-granularity.md`，把回填/状态/快照分层、`is_new` 公式与粒度边界写实
- 更新 `standards/semantic-correctness/customer-status-semantics.md` 与 `standards/output-correctness/output-correctness.md`，把状态语义检查表与输出约束补齐
- 更新 `surfaces/customer-mdm-commands.md` 与相关 domain 导航页，明确手工命令面和 event fact 对状态判断的支撑关系

## [2026-04-14] absorb | Round 02 闭环吸收 `identity-and-lookup`

- 新增 `concepts/temp-id.md`，把 temp-id 从 `company_id` 总页中拆成独立 atomic concept
- 更新 `evidence/identity-and-lookup-evidence.md`，把多线索识别、5-step fallback chain、queue/runtime surface、annuity_income 身份缺口聚合并区分强弱证据
- 更新 `concepts/company-id.md`，把 `company_id` 从“身份键”进一步写实为一条受治理的多线索解析链
- 更新 `surfaces/company-lookup-queue.md` 与 `surfaces/unknown-names-csv.md`，把 runtime surface 与 operator artifact 的独立性写实
- 更新 `standards/verification-method/golden-scenarios.md`，把 identity fallback chain 和 temp-id 场景纳入 golden scenario 视野
- 更新 `domains/annual-award.md`、`domains/annual-loss.md`、`domains/annuity-performance.md`、`domains/annuity-income.md`，明确身份解析和 plan-code 补齐对各域的重要性

## [2026-04-14] absorb | Round 03 闭环吸收 `input-reality`

- 更新 `evidence/input-reality-evidence.md`，将 real-data sample、version strategy、sheet contract、多 sheet 事件域与 annuity_income 制度记忆聚合为输入现实证据簇
- 更新 `standards/input-reality/input-reality-contracts.md`，补入输入现实检查表、关键输入现实与非例
- 更新 `concepts/plan-type.md`，把 plan type 与输入现实、多线索识别、event domain sheet contract 的关系写实
- 更新 `domains/annual-award.md`、`domains/annual-loss.md`、`domains/annuity-income.md`，把 multi-sheet 输入现实与未实现 domain 的制度记忆显式化
- 新增 `_meta/absorption-rounds/round-03-input-reality.md`，沉淀本轮经验并把下一轮切到 `verification-assets`

## [2026-04-14] absorb | Round 04 闭环吸收 `verification-assets`

- 更新 `evidence/verification-assets-evidence.md`，把 legacy 高价值资产、current replay registry、error-case fixtures 与 annuity_income 资产缺口聚合为稳定证据簇
- 更新 `standards/verification-method/real-data-validation.md`，把 verification asset 组合作为 real-data validation 的组成部分写实
- 更新 `standards/verification-method/golden-scenarios.md`，把 asset taxonomy、open questions 和 legacy-only memory 边界写实
- 更新 `domains/annuity-income.md`，明确 annuity_income 的验证资产制度记忆不能因未实现而消失
- 新增 `_meta/absorption-rounds/round-04-verification-assets.md`，沉淀本轮经验并把下一轮切到 `operator-and-surfaces`

## [2026-04-14] absorb | Round 05 闭环吸收 `operator-and-surfaces`

- 更新 `evidence/operator-and-surface-evidence.md`，把 queue、reference sync、manual commands、failed-record export、enterprise persistence 的治理边界写实
- 更新 `surfaces/reference-sync.md`，明确其 target tables、integration 语义与非隐含性
- 更新 `surfaces/failed-record-export.md`，明确其作为 operator artifact 的制度价值
- 更新 `surfaces/customer-mdm-commands.md` 与 `surfaces/company-lookup-queue.md`，把独立 operator/runtime surface 语义继续收紧
- 新增 `_meta/absorption-rounds/round-05-operator-and-surfaces.md`，沉淀本轮经验并把下一轮切到 `annuity_income`

## [2026-04-14] absorb | Round 06 闭环吸收 `annuity_income`

- 新增 `evidence/annuity-income-gap-evidence.md`，把 annuity_income 的 capability map、ID5 retirement、parity validation memory、operator artifact gap 收束成专题证据页
- 更新 `domains/annuity-income.md`，把 annuity_income 从“未实现 domain”进一步写实为一组必须保留的制度记忆簇
- 更新 `evidence/identity-and-lookup-evidence.md`、`evidence/verification-assets-evidence.md`、`evidence/operator-and-surface-evidence.md`，把 annuity_income 的 identity / verification / operator gap 接回现有主题页
- 新增 `_meta/absorption-rounds/round-06-annuity-income.md`，把本轮作为当前路线图的第六轮闭环完成记录

## [2026-04-14] absorb | Round 07 follow-on 闭环吸收 `is_new` 对象级证据拆分

- 新增 `evidence/is-new-evidence.md`，把 `is_new` 的公式、粒度边界、非例与验证路径从主题型 evidence page 中拆成对象级 evidence page
- 更新 `concepts/is-new.md`、`concepts/customer-status.md`、`standards/semantic-correctness/customer-status-semantics.md`，把新对象级证据页接入主结论层
- 更新 `evidence/status-and-snapshot-evidence.md`，把 `is_new` 对象级拆分标记为可复用样板
- 新增 `_meta/absorption-rounds/round-07-is-new-evidence-split.md`，把本轮作为 follow-on work 的首个对象级拆分页记录

## [2026-04-14] absorb | Round 08 闭环吸收 `annuity_income` slice admission package

- 新增 `_meta/absorption-rounds/round-08-annuity-income-slice-admission.md`，把 `annuity_income` 的专题 gap 转成可直接支撑 slice admission 的轮次沉淀
- 新增 `evidence/annuity-income-branch-mapping-evidence.md`、`evidence/annuity-income-id5-retirement-evidence.md`、`evidence/annuity-income-operator-artifacts-evidence.md`，把 branch mapping、ID5 retirement、operator artifacts 拆成对象级 evidence page
- 更新 `evidence/annuity-income-gap-evidence.md`、`evidence/identity-and-lookup-evidence.md`、`evidence/operator-and-surface-evidence.md`、`evidence/verification-assets-evidence.md`，把 `annuity_income` 的 admission-critical 细节从专题页接回对象级 evidence page
- 更新 `domains/annuity-income.md`、`standards/verification-method/golden-scenarios.md`、`surfaces/unknown-names-csv.md`、`surfaces/failed-record-export.md`，把 slice-admission-ready evidence 接入 domain、standard 与 surface 入口
- 新增 `docs/superpowers/plans/2026-04-14-workdatahubpro-annuity-income-validation-slice.md` 并更新 first-wave coverage matrix，把 `annuity_income` 从“只有制度记忆”推进到显式 admitted slice 入口

## [2026-04-14] validate | annuity_income wiki-guided implementation loop

- `COMPANY_BRANCH_MAPPING`、ID5 retirement、operator artifacts 这三组 wiki 结论都直接转化成了 current project 的实现、测试与 replay assets
- 更新 `annuity_income` 相关 evidence pages，把 current_test / current_reference_asset / current_runbook 证据接回 wiki，验证这些页面对实际开发工作具有指导意义

## [2026-04-14] maintain | 收紧 domain 导航与 cross-reference

- 对 `annual_award`、`annual_loss`、`annuity_performance` 的主链路页面补入显式 cross-reference，避免 event-style domains 只由首页单点可达
- 更新 `customer-status`、`customer-status-semantics`、`input-reality-contracts`、`golden-scenarios` 与 `status-and-snapshot-evidence`，把 domain 导航重新接回概念、标准与证据层
- 更新 `index.md` FAQ / catalog 入口，并新增 Round 10 轮次沉淀，记录本次 wiki lint 与导航收紧经验

## [2026-04-14] plan | 更新下一阶段吸收轮次排序

- 基于当前 evidence pages 中的 open question 与缺口，重新给下一阶段 round 做收益排序
- 将 Round 11 定位为 `Phase E operator/runtime surfaces decision package`
- 将 validation result history / fixture governance、identity governance deepening、status family selective split 排到后续轮次

## [2026-04-14] absorb | Round 11 闭环吸收 `Phase E operator/runtime surfaces`

- 更新 `operator-and-surface-evidence.md`，把 CLI / GUI entrypoints、reference sync config、async queue persistence、provider persistence 与 standalone tooling 的 raw-source 证据写成正式 decision package
- 新增 `enterprise-enrichment-persistence.md` 与 `standalone-tooling.md`，把先前只在缺口清单里出现的对象簇提升为独立治理对象
- 更新 `reference-sync.md`、`company-lookup-queue.md`、`customer-mdm-commands.md`，把 target inventory、queue semantics、manual recovery path 与相邻 tooling 边界收紧
- 更新 `index.md`、`_meta/absorption-rounds/index.md` 与 `wiki-absorption-roadmap.md`，将 Round 11 标记为已完成，并把推荐入口推进到 Round 12

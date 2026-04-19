# Wiki BI 日志

> 标题格式规则：自 `2026-04-15` 起，新日志标题统一使用 `## [YYYY-MM-DD HH:MM] action | summary`。
> 目的：区分同一天内的多次改动；历史条目保留原日期格式，不做追溯性改写。

## [2026-04-19 10:34] maintain | round 34 relationship breadth list deepening

- 新增 `other-annuity-plans.md` 与 `other-branches.md`，把 `其他年金计划` 与 `其他开拓机构` 从 dispatcher-only 状态推进成 durable wiki 对象
- 回写 `customer-master-signals-evidence`、相邻 concept / domain / output-contract 页面，使 relationship breadth 在计划侧与机构侧都形成 dominant / count / list 三层表达
- 新增 Round 34 轮次沉淀并更新 `index.md` / `wiki-absorption-roadmap.md` / `absorption-rounds/index.md`，明确 `组合代码` 成为剩余主要 business-semantics follow-on candidate

## [2026-04-18 20:34] maintain | customer_type vs is_new governance package

## [2026-04-19 00:11] maintain | round 33 reference_sync governance

- 新增 `reference-sync-runtime-and-state-evidence.md`，把 `reference_sync` 的 target inventory、incremental sync-state 与 current replacement boundary 从 scattered statements 收紧成 durable object-level evidence route
- 回写 `reference-sync.md`、`reference-and-backfill-evidence`、`operator-and-surface-evidence`、`backfill` 与 `output-correctness`，使 `reference_sync` 的治理边界更直接可答
- 新增 Round 33 轮次沉淀并更新 `index.md` / `wiki-absorption-roadmap.md` / `absorption-rounds/index.md`，明确 runtime breadth 仍继续 deferred，下一步优先转向 manual `customer-mdm` / enterprise persistence closure wave

## [2026-04-18 23:42] maintain | round 32 shared unresolved artifact governance

- 新增 `unresolved-name-and-failed-record-evidence.md`，把 shared unresolved-name / failed-record artifact family 从 scattered gaps 收紧成 durable evidence dispatcher
- 回写 `operator-and-surface-evidence`、`identity-and-lookup-evidence`、相邻 surface / identity / domain / contract 页面，使 queue deferred 与 artifact replacement 的关系更直接可答
- 新增 Round 32 轮次沉淀并更新 `index.md` / `wiki-absorption-roadmap.md` / `absorption-rounds/index.md`，明确 current accepted artifact closure 仍以 `annuity_income` 为主，cross-domain parity 继续留在 follow-on

## [2026-04-18 23:06] maintain | round 31 relationship breadth and classification closeout

- 新增 `related-branch-count.md` 与 `management-qualification.md`，把 `关联机构数` 与 `管理资格` 从遗漏或 dispatcher-only 状态推进成 durable wiki 对象
- 回写 `customer-master-signals-evidence`、`classification-family-evidence`、相邻 concept / field-processing / output-contract / domain 页面，使 relationship breadth 与 classification family 的边界更直接可答
- 新增 Round 31 轮次沉淀并更新 `index.md` / `wiki-absorption-roadmap.md` / `absorption-rounds/index.md`，明确 `其他年金计划`、`其他开拓机构`、`组合代码` 仍保留为 follow-on candidates

- 新增 `customer-type-is-new-governance-evidence.md`，把 semantic non-equivalence、legacy proxy usage 与 disposition question 收紧成独立治理对象
- 回写 `customer-type`、`is-new`、`customer-status-semantics` 与相邻 evidence/index 页面，使它们统一使用 semantic truth / proxy history / governance disposition 这组表达
- 收紧 semantic-map canonical non-equivalence 节点，准备把该项从“模糊 contested discovery”推进到“已确认语义、待裁决 disposition”的 successor-wave 视图

## [2026-04-18 21:43] maintain | round 29 legacy business semantics expansion

- 新增 `key-annuity-plan.md` 与 `classification-family-evidence.md`，把 `关键年金计划` 和 classification family 从 dispatcher / field-processing 碎片推进成 durable wiki 入口
- 回写 `customer-master-signals-evidence`、`backfill`、`primary-branch`、`customer-status`、`customer-status-semantics` 与相邻合同/证据页，使 `is_churned_this_year`、relationship breadth 与 classification family 的边界更直接可答
- 新增 Round 29 轮次沉淀并更新 `index.md` / `wiki-absorption-roadmap.md` / `absorption-rounds/index.md`，明确本轮仍停留在 business-semantics scope，没有重开 runtime/operator closure

## [2026-04-18 22:21] maintain | round 30 relationship breadth deepening

- 新增 `related-plan-count.md`，把 `关联计划数` 从 customer-master signal dispatcher 提升为独立 relationship-breadth object page
- 回写 `customer-master-signals-evidence`、`backfill`、`key-annuity-plan` 与相邻 domain/output-contract 页面，使 `关联计划数`、`关键年金计划` 与 snapshot `plan_count` 的边界更直接可答
- 新增 Round 30 轮次沉淀并更新 `index.md` / `wiki-absorption-roadmap.md` / `absorption-rounds/index.md`，明确 `其他年金计划`、`其他开拓机构` 仍暂留在 dispatcher 层

## [2026-04-18 20:19] maintain | annual identity semantics coverage

- 新增 `customer-status-annual-identity-evidence.md`，把 `is_strategic`、`is_existing`、`contract_status`、`status_year` 收紧成 annual identity family 的 durable object page
- 收紧 `customer-status` / `customer-status-semantics` / `customer-type`，显式写清 `status_year` 锚点、strategic ratchet 语义与 `customer_type` vs `is_new` 的 proxy-conflict
- 回写 `customer-mdm-lifecycle-evidence`、`status-and-snapshot-evidence` 与 `index.md`，让维护者和读者都能直接进入这个主题

## [2026-04-16 19:50] plan | semantic map 驱动的下一阶段 wiki 吸收

- 将 `wiki-absorption-roadmap.md` 改写为 semantic-map-first 路线：先建 discovery ledger，再把稳定结论吸收到 durable wiki
- 在 `wiki-maintenance-lint-checklist.md` 中显式排除 `docs/wiki-bi/_meta/legacy-semantic-map/`，并要求继续检查其未进入 `index.md` 且 `README.md` 保留 owner / archive trigger
- 收紧 semantic map bootstrap 边界，明确下一阶段优先围绕 `company_lookup_queue`、`reference_sync`、enterprise persistence、manual `customer-mdm` commands 与 shared operator artifacts 做 discovery wave

## [2026-04-18 19:48] maintain | customer-master derived signals 收紧

- 新增 `customer-master-signals-evidence.md`，把 `tags`、`主拓机构`、`关键年金计划`、关系计数与 `年金客户类型` 收紧成 cross-domain customer-master signal family
- 新增 `tags` 与 `主拓机构` concept pages，并将它们接回 `backfill`、`customer_type`、四个高流量 domain 与四份输出合同
- 本轮只收紧 cross-domain customer-master semantics，不扩写新的 runtime/operator surface 决策范围

## [2026-04-16 10:23] maintain | 清理 `wiki-bi` 中的执行态流程漂移

- 从 `docs/wiki-bi/_meta/` 移除 subagent/worktree/merge sequencing 这类执行层材料，避免 durable wiki 再次承担 workflow 说明职责
- 将 Round 24-27、`index.md`、`wiki-absorption-roadmap.md` 与吸收轮次索引重写为纯语义沉淀，不再把试点、并行波次与集成流程当作主导航对象
- 清理 durable page 中的 round-specific 标题，使对象页只保留当前有效结论而不绑定某次维护轮次

## [2026-04-16 08:43] maintain | Round 27 legacy 语义补强收口

- 对 `annuity_performance`、`annuity_income`、`annual_award`、`annual_loss` 与 shared operator / verification pages 做对象级补强与 cross-link 收口
- 继续保持 domain 页的薄导航形态，把 contract-grade 结论留在输入/输出合同与字段处理证据页
- 将 current runtime、历史记忆与未闭环项继续分层表达，未收口部分统一留在 `当前证据缺口`

## [2026-04-16 08:14] absorb | Round 26 状态与快照生命周期补强

- 新增 `customer-mdm` 年度生命周期证据页，补入 `yearly-init`、`sync`、`snapshot`、ratchet-style 与 `status_year` 的语义边界
- 收紧概念层与命令 / runtime 层分离，使年度状态语义回到概念 / 标准，命令触发路径继续留在 surface / evidence
- 将尚未 current-side 闭环的 runtime 项继续登记在 evidence gaps，而不是提升成稳定结论

## [2026-04-16 08:08] absorb | Round 25 身份治理语义分层收紧

- 将 `company_id`、`temp_id` 与 identity governance 收紧成“当前运行路径 / 历史记忆 / 已退休行为 / operator-visible consequence”四层表达
- 明确 `company_lookup_queue` 与 enterprise persistence 是两个不同 surface，避免再把异步补查语义与持久化对象族混写
- 将 unresolved identity 的外显要求继续写成 operator artifact / signal / evidence-gap 边界，而不是内部 trace 假设

## [2026-04-16 01:36] absorb | Round 24 引用同步与回填语义收紧

- 新增 `reference-and-backfill-evidence.md`，把 authoritative `reference_sync`、fact-derived `backfill` 与 customer-master 衍生写入写成 durable evidence page
- 收紧 `backfill` 概念页、`reference_sync` surface 页与四个 domain 导航页的连接，明确“对象页承载结论，domain 页只做分发”
- 明确 `reference_sync` 与 `backfill` 同属 reference strategy，但拥有不同 provenance、target footprint 与治理边界

## [2026-04-15 23:43] plan | Round 23 production-sample augmentation

- planned a wiki maintenance round focused on legacy plus representative single-month production-sample reality
- scoped the round around workbook-family evidence, workbook variants, and business-collection adjacent surfaces
- executed the round by adding object-level evidence for annuity workbook family and business-collection variants, then registering the ledger workbook as an explicit surface

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

## [2026-04-14] absorb | Round 12 闭环吸收 `verification result history`

- 更新 `verification-assets-evidence.md`，把 current registry 的 `deferred` 状态、inline failure-path coverage 与 legacy result corpus 的角色写实
- 新增 `validation-result-history-evidence.md`，把 parity result 目录、current asset registry 与 validation history 变成独立 evidence object
- 更新 `golden-scenarios.md` 与 `real-data-validation.md`，明确 `deferred` 不等于“没有资产”，并把 validation result history 接入验证方法层
- 更新 `annual-award.md`、`annual-loss.md`、`index.md`、`_meta/absorption-rounds/index.md` 与 `wiki-absorption-roadmap.md`，将 Round 12 标记为已完成，并把推荐入口推进到 Round 13

## [2026-04-14] absorb | Round 13 闭环吸收 `identity governance`

- 新增 `standards/semantic-correctness/identity-governance.md`，把 `company_id`、`temp_id`、mapping / cache / provider / queue 边界提升为独立标准层
- 更新 `identity-and-lookup-evidence.md`，补入 mapping override configs、current identity tests 与 current identity service 的实现证据
- 更新 `company-id.md`、`temp-id.md` 与 `company-lookup-queue.md`，把治理链、fallback 边界与相关标准接回概念 / surface 层
- 更新 `annuity-income-branch-mapping-evidence.md` 与 `annuity-income-id5-retirement-evidence.md`，把这两组 annuity_income 专题记忆明确接回 broader identity governance
- 更新 `index.md`、`_meta/absorption-rounds/index.md` 与 `wiki-absorption-roadmap.md`，将 Round 13 标记为已完成，并把推荐入口推进到 Round 14

## [2026-04-14] absorb | Round 14 闭环吸收 `status family selective split`

- 新增 `is-winning-this-year-evidence.md` 与 `is-loss-reported-evidence.md`，把这两个已满足阈值的状态对象拆成独立 evidence page
- 更新 `status-and-snapshot-evidence.md`、`customer-status.md`、`customer-status-semantics.md`、`annual-award.md` 与 `annual-loss.md`，把新对象级证据页接回概念、标准与 domain 层
- 在 Round 14 中显式判定 `is_churned_this_year` 继续留在主题页，因为它当前仍夹着 product-line / plan 双粒度与 AUM 汇总语义
- 更新 `index.md`、`_meta/absorption-rounds/index.md` 与 `wiki-absorption-roadmap.md`，将 Round 14 标记为已完成，并把后续入口切到机会式增量维护

## [2026-04-14] absorb | Round 15 闭环吸收 `annuity_performance` I/O contracts

- 新增 `annuity-performance-input-contract.md`，把 annuity-performance 的 workbook、file pattern、sheet、版本策略与最小字段骨架写成专门输入合同
- 新增 `annuity-performance-output-contract.md`，把 direct fact sink、backfill targets 与 derived downstream tables 写成专门输出合同
- 新增 `annuity-performance-field-processing-evidence.md`，把字段处理区分为工程性质量提升与业务语义处理
- 更新 `annuity-performance.md`、`input-reality-contracts.md`、`output-correctness.md`、`input-reality-evidence.md`、`backfill.md` 与 `index.md`，把 annuity-performance 的 I/O 问答入口接回主 wiki
- 更新 `_meta/absorption-rounds/index.md`，把本轮沉淀纳入正式轮次索引

## [2026-04-14] audit | Round 16 闭环吸收 `annuity_performance` implementation gaps

- 更新 `annuity-performance-field-processing-evidence.md`，补入显式空值 / 默认值规则，避免 annuity-performance 只停留在处理分类层
- 新增 `annuity-performance-implementation-gap-evidence.md`，把 annuity-performance wiki 合同与 legacy 代码实现之间的差距项正式沉淀
- 更新 `annuity-performance.md`、`index.md`、`_meta/absorption-rounds/index.md` 与 `wiki-absorption-roadmap.md`，把 gap audit 作为持续维护轮次显式登记

## [2026-04-14] adjudicate | annuity_performance gap review follow-up

- 根据后续人工审核与再次代码核对，将 `GAP-AP-001`、`GAP-AP-006` 降级为已判定非 gap
- 将 `GAP-AP-002` 收紧为“wiki 过窄已确认”，并把 `客户名称` 缺失从绝对无效源调整为降级输入语义
- 将 `GAP-AP-003` 收紧为“当前运行路径与 schema-level contract 的代码漂移”
- 将 `GAP-AP-004`、`GAP-AP-005` 收紧为高概率代码问题，并新增 `GAP-AP-007` 记录 company_id YAML priority 的实现漂移

## [2026-04-15] adjudicate | annuity_performance gap disposition split

- 将 `GAP-AP-002` 进一步关闭为 `resolved_wiki_correction`
- 将 `GAP-AP-003`、`GAP-AP-004`、`GAP-AP-005` 统一收敛为 `code_fix_candidate`
- 将 `GAP-AP-007` 收敛为 `stale_documentation_drift`
- 为剩余 active items 拆出代码修复候选计划与 contract drift 清理计划

## [2026-04-14] maintain | 提炼 domain wiki 升级框架

- 新增 `_meta/wiki-domain-upgrade-framework.md`，把高价值 domain 从导航页升级到合同级 wiki 的工作流沉淀为可复用框架
- 新增 `round-17-domain-upgrade-workflow-pattern.md`，用 annuity-performance 的 Round 15 / 16 作为样板实例
- 更新 `index.md` 与 `_meta/absorption-rounds/index.md`，把这套“通用框架 + 真实样板”接入主导航

## [2026-04-15 08:30] maintain | 为日志标题规则补入 `HH:MM`

- 在 `log.md` 顶部显式规定新标题格式为 `## [YYYY-MM-DD HH:MM] action | summary`
- 更新 `wiki-design.md` 的推荐示例与日志规则描述，使 schema 与实际执行页保持一致
- 更新 `index.md` 对变更日志的说明，明确后续记录按“日期 + 时间”维护

## [2026-04-15 09:36] validate | 关闭 annuity_performance 剩余 active gaps

- 在 legacy `E:\Projects\WorkDataHub` 中补上 annuity-performance active path 的 Gold validation，关闭 `GAP-AP-003`
- 修正 legacy `foreign_keys.yml` 中 `fk_organization` 对 canonical `机构名称` 的回填来源，关闭 `GAP-AP-004`
- 修正 legacy `集团企业客户号` 清洗对 Python `None` 的串值物化，关闭 `GAP-AP-005`
- 收紧 legacy resolver-facing 文档/注释，对齐 active annuity-performance YAML execution path，关闭 `GAP-AP-007`
- 验证命令：`PYTHONPATH=src uv run pytest tests/unit/domain/annuity_performance/test_pipeline_builder.py tests/unit/domain/annuity_performance/test_failed_records_export.py tests/unit/domain/annuity_performance/test_schemas.py tests/unit/domain/reference_backfill/test_generic_backfill_service.py -q`

## [2026-04-15 11:51] maintain | 收紧 wiki 发现路径并升级 annuity_income 合同入口

- 在 `index.md` 中新增维护者入口，显式提示 canonical playbook、confirmed domain-upgrade set 与 lint checklist
- 在 `wiki-domain-upgrade-framework.md` 中明确其为当前唯一 canonical maintenance playbook，并补入 implementation-evidence / identity narrative / lint gate 三个控制项
- 为 `annuity_income` 新增输入合同、输出合同与字段处理证据页，使它不再只停留在专题 evidence + institutional memory 层
- 更新 `annuity_income`、`company_id`、`identity-governance` 与相关 evidence pages，把“当前运行路径”“兼容性清单”“已退休行为”“可见后果”分层写清
- 新增 Round 18，记录这次“发现路径优化 + annuity_income 对称升级”的 maintenance 闭环

## [2026-04-15 13:03] maintain | 收紧 annuity_income 合同边界与字段处理证据形态

- 将 `annuity_income` 输入合同中的硬门槛表述退回到更有 raw-source 支撑的边界，不再把 `计划类型`、`机构名称` 直接写成绝对门槛
- 为 `annuity_income` 字段处理证据页补入显式 evidence records、强证 / 旁证划分与 supported pages 视角，使其更贴近标准 evidence page 形态

## [2026-04-15 13:57] maintain | 升级 event domains 并制度化 evidence/lint writeback

- 新增 `annual_award` / `annual_loss` 的输入合同、输出合同与字段处理证据页，使 confirmed event domains 不再只停留在薄导航层
- 更新 `annual_award`、`annual_loss`、`input-reality-contracts`、`output-correctness` 与相关 evidence pages，把 event-domain contract-grade 入口接回主 wiki
- 收紧 `wiki-design.md`、`wiki-domain-upgrade-framework.md` 与 `wiki-maintenance-lint-checklist.md`，将 evidence 最小模板与 substantial maintenance 的固定产物写成正式规则
- 新增 Round 19，记录这次“event-domain 对称升级 + evidence/lint 制度化”的 maintenance 闭环

## [2026-04-15 14:47] plan | 写入 Round 20-22 短期治理计划

- 更新 `wiki-absorption-roadmap.md`，把“无预设新 round”收紧为 Round 20-22 的短期计划与明确执行顺序
- 新增 Round 20、Round 21、Round 22 三个 planned round notes，分别对应 verification asset 裁决包、Phase E surface closure 与高流量 evidence 页模板归一
- 更新 `_meta/absorption-rounds/index.md` 与 `index.md`，让新计划页进入主导航与全量 catalog

## [2026-04-15 15:11] maintain | 完成 Round 20 verification asset 裁决包

- 更新 `verification-assets-evidence.md` 与 `validation-result-history-evidence.md`，把 verification assets / result history 收紧为“manifest 状态 + 当前保护方式 + 裁决含义”的 durable 表达，并补入 contract test 与 gate runtime 证据
- 更新 `golden-scenarios.md` 与 `real-data-validation.md`，明确 accepted slices 当前的 active protection story 是 `replay_baseline + synthetic_fixture + checkpoint_baseline`，而 `golden_set`、`golden_baseline`、`error_case_fixture`、`real_data_sample` 仍为显式 `deferred`
- 更新 `annuity_performance`、`annual_award`、`annual_loss` 三个 domain 页，为读者直接暴露当前验证资产姿态，避免把 accepted replay protection 误读成更宽的 golden governance
- 将 Round 20 从 planned 推进到 completed，并在 `wiki-absorption-roadmap.md`、`_meta/absorption-rounds/index.md` 与 `index.md` 中把下一推荐入口切到 Round 21

## [2026-04-15 15:24] maintain | 完成 Round 21 Phase E surface closure

- 更新 `operator-and-surface-evidence.md`，把 surface 治理从“对象已识别”收紧成 `reference_sync`、`company_lookup_queue`、enterprise persistence 的 decision package，并补入 current spec / tests / code 证据
- 更新 `reference-sync.md`、`company-lookup-queue.md` 与 `enterprise-enrichment-persistence.md`，显式写清 current accepted runtime 中哪些 legacy surface 已被替代、哪些治理记忆需保留、哪些 runtime breadth 继续 deferred
- 将 `reference_derivation + publication`、同步 identity chain、temp-id fallback 与 operator artifacts 写成 current-side replacement evidence，避免继续把 legacy special orchestration surfaces 误读成“当前已保留”
- 将 Round 21 从 planned 推进到 completed，并在 `wiki-absorption-roadmap.md`、`_meta/absorption-rounds/index.md` 与 `index.md` 中把下一推荐入口切到 Round 22

## [2026-04-15 15:32] maintain | 完成 Round 22 high-traffic evidence normalization

- 更新 `status-and-snapshot-evidence.md`、`verification-assets-evidence.md` 与 `operator-and-surface-evidence.md`，把高流量 aggregate evidence page 收紧成更一致的骨架：证据表、强/旁证、dispatcher 边界、对象级补强页、当前证据缺口
- 为状态与快照主题补入 current projection / replay evidence，并把三张 aggregate page 的“对象级细节”与“aggregate dispatcher 角色”分层写清
- 将 Round 22 从 planned 推进到 completed，并在 `wiki-absorption-roadmap.md`、`_meta/absorption-rounds/index.md` 与 `index.md` 中收口本批短期治理计划

# Wiki BI Log

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

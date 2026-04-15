# WorkDataHubPro Wiki BI

> 业务语义与验收标准 wiki
> 用途：连接 legacy evidence 与 rebuild design
> 读取方式：先按阅读意图进入，再看常见问题卡片，最后使用全量 catalog 深入

## 维护者入口

- 我正在维护 wiki，本轮该先看哪里
  - 先看 [domain wiki 升级框架](./_meta/wiki-domain-upgrade-framework.md)；它是当前 canonical maintenance playbook。
- 我怀疑要新建一个新的维护流程
  - 先看 [domain wiki 升级框架](./_meta/wiki-domain-upgrade-framework.md) 与 [wiki maintenance lint checklist](./_meta/wiki-maintenance-lint-checklist.md)，默认应优化既有 playbook，而不是创建平行流程。
- 我想确认哪些 domain 已经是 confirmed upgrade targets
  - 当前明确集合是 `annuity_performance`、`annual_award`、`annual_loss`、`annuity_income`。

## 阅读意图

- 我想知道一个业务判断到底是什么意思
  - 从 [概念页](./concepts/customer-status.md) 开始
- 我想知道某个 domain 在业务上处理什么
  - 从 [domain 导航页](./domains/annuity-performance.md) 开始
- 我想知道哪些 system surfaces 需要独立治理
  - 从 [surface 页](./surfaces/reference-sync.md) 开始
- 我想知道什么才算正确输出
  - 从 [标准页](./standards/output-correctness/output-correctness.md) 开始
- 我想知道为什么能相信某条结论
  - 从 [证据页](./evidence/status-and-snapshot-evidence.md) 开始

## 常见问题卡片

- [`is_new` 与 `年金客户类型` 的区别](./concepts/is-new.md)
  - 新到账状态与客户分类标签不是同一层语义。
- [`company_id` 在业务上到底是什么](./concepts/company-id.md)
  - 企业身份标识是跨 domain 连接事实、主数据、快照和验证的核心对象。
- [什么算受治理的身份 fallback](./standards/semantic-correctness/identity-governance.md)
  - temp-id、mapping files、cache、provider、queue 的边界需要作为 identity governance 统一理解。
- [什么算 real-data validation](./standards/verification-method/real-data-validation.md)
  - 真实数据验证不是“拿真实文件跑一下”，而是有边界和目标的验证方法。
- [什么样的输出才算“正确”](./standards/output-correctness/output-correctness.md)
  - 正确输出应满足语义、粒度、关系和验收资产多重约束。
- [为什么 `deferred` 不等于“没有验证资产”](./evidence/validation-result-history-evidence.md)
  - current registry 已显式登记很多尚未物化的 asset kinds，问题是治理状态，而不是是否被看见。
- [`annuity_performance` 的输入、输出和处理到底是什么](./standards/input-reality/annuity-performance-input-contract.md)
  - 先看输入合同，再看输出合同和字段处理证据，可以直接回答 annuity-performance 的 I/O 问题。
- [`annual_award` / `annual_loss` 的输入、输出和处理到底是什么](./standards/input-reality/annual-award-input-contract.md)
  - event-style domains 现在也有对称的输入合同、输出合同和字段处理证据，不必再只停在导航页。
- [`annuity_performance` 的 wiki 知识和原实现有哪些差距](./evidence/annuity-performance-implementation-gap-evidence.md)
  - 合同页补齐后，应先看 gap evidence，再决定是修 wiki 还是修实现。
- [哪些 system surfaces 不能被隐含忽略](./surfaces/company-lookup-queue.md)
  - queue、reference sync、manual commands、operator artifacts 都是显式治理对象。
- [哪些 legacy tools 属于相邻 operator tooling，而不是业务主路径](./surfaces/standalone-tooling.md)
  - `cleanse`、EQC GUI、deployment GUI 需要显式登记，但不能自动等同于 rebuild 核心边界。
- [为什么旧项目不能直接作为新架构模板](./_meta/wiki-design.md)
  - wiki 借鉴 legacy 的稳定语义与标准，而不是复制其实现结构。
- [我在维护 wiki 时应该先走哪条 canonical 路径](./_meta/wiki-domain-upgrade-framework.md)
  - 先确认现有 playbook 是否已覆盖，再决定是否需要新 round 或新页面。
- [如何把某个 domain 从导航页升级成合同级 wiki](./_meta/wiki-domain-upgrade-framework.md)
  - 先补输入/输出/处理合同，再按需做 code-gap audit，这是当前最可复用的 domain wiki 升级路径。
- [event-style domains 如何接回状态判断与输入现实](./domains/annual-award.md)
  - 从 `annual_award` 进入，再串到 `annual_loss`、`annuity_performance` 与相关标准页，看 event domain 如何进入状态语义与输入现实。

## 全量 Catalog

### Concepts

- [企业身份标识：`company_id`](./concepts/company-id.md) : 定义企业身份标识的业务意义、边界和验证约束。
- [临时身份：`temp_id`](./concepts/temp-id.md) : 定义 temp-id 的语义、边界及其与正式身份的区别。
- [客户状态总览](./concepts/customer-status.md) : 汇总客户状态相关概念、判定边界与下游影响。
- [`is_new`：新到账客户状态](./concepts/is-new.md) : 解释新到账状态与中标、存量、客户分类的关系。
- [年金客户类型：`customer_type`](./concepts/customer-type.md) : 说明客户分类标签与状态字段的区别。
- [年金计划类型：`plan_type`](./concepts/plan-type.md) : 说明单一计划与集合计划的语义差异和约束。
- [快照粒度：`snapshot_granularity`](./concepts/snapshot-granularity.md) : 定义客户/产品线与客户/计划两类快照粒度。
- [回填：`backfill`](./concepts/backfill.md) : 说明主数据/参考数据回填的业务语义和边界。

### Domains

- [`annuity_performance`](./domains/annuity-performance.md) : 导航规模域相关概念、输出和关键证据。
- [`annual_award`](./domains/annual-award.md) : 导航中标域如何接入客户状态、multi-sheet 输入现实与关键证据。
- [`annual_loss`](./domains/annual-loss.md) : 导航流失域如何接入客户状态、multi-sheet 输入现实与关键证据。
- [`annuity_income`](./domains/annuity-income.md) : 导航收入域相关概念、输出以及 slice admission 相关证据入口。

### Surfaces

- [`company_lookup_queue`](./surfaces/company-lookup-queue.md) : 识别异步企业补查队列这一独立治理 surface。
- [enterprise enrichment persistence](./surfaces/enterprise-enrichment-persistence.md) : 识别 `enrichment_index`、`enrichment_requests`、`base_info` 组成的 identity persistence surface。
- [`reference_sync`](./surfaces/reference-sync.md) : 识别 authoritative reference sync 这一独立治理 surface。
- [`customer-mdm` 手工命令面](./surfaces/customer-mdm-commands.md) : 识别 contract/snapshot/init-year/cutover 等 operator surface。
- [failed-record export](./surfaces/failed-record-export.md) : 识别失败记录导出这一 operator artifact surface。
- [standalone tooling](./surfaces/standalone-tooling.md) : 识别 `cleanse`、EQC GUI 与 deployment GUI 这类相邻 operator tooling family。
- [`unknown_names_csv`](./surfaces/unknown-names-csv.md) : 识别 unresolved names 导出这一 operator artifact surface。

### Standards

#### Input Reality

- [输入现实合同](./standards/input-reality/input-reality-contracts.md) : 定义真实输入形态、sheet/目录/fixture 边界与约束。
- [`annual_award` 输入合同](./standards/input-reality/annual-award-input-contract.md) : 明确 annual_award 的双 sheet workbook、最小字段骨架与 merged anchor intake 边界。
- [`annual_loss` 输入合同](./standards/input-reality/annual-loss-input-contract.md) : 明确 annual_loss 的双 sheet workbook、空尾行处理与最小 loss-event 输入骨架。
- [`annuity_performance` 输入合同](./standards/input-reality/annuity-performance-input-contract.md) : 明确 annuity-performance 的 workbook、file pattern、sheet、版本策略与最小字段骨架。
- [`annuity_income` 输入合同](./standards/input-reality/annuity-income-input-contract.md) : 明确 annuity_income 的 workbook family、`收入明细` sheet、计划锚点与收入数值族输入边界。

#### Semantic Correctness

- [客户状态语义正确性](./standards/semantic-correctness/customer-status-semantics.md) : 定义客户状态相关判断的稳定语义。
- [身份治理语义正确性](./standards/semantic-correctness/identity-governance.md) : 定义 `company_id`、`temp_id`、mapping / cache / provider / queue 的治理边界。

#### Output Correctness

- [输出正确性标准](./standards/output-correctness/output-correctness.md) : 定义输出结果什么情况下才算正确。
- [`annual_award` 输出合同](./standards/output-correctness/annual-award-output-contract.md) : 明确 annual_award 的 direct fact、customer/reference signal 与 projection 边界。
- [`annual_loss` 输出合同](./standards/output-correctness/annual-loss-output-contract.md) : 明确 annual_loss 的 direct fact、customer loss signal 与 temp-id 治理边界。
- [`annuity_performance` 输出合同](./standards/output-correctness/annuity-performance-output-contract.md) : 明确 annuity-performance 的 direct fact sink、backfill targets 与 derived outputs。
- [`annuity_income` 输出合同](./standards/output-correctness/annuity-income-output-contract.md) : 明确 annuity_income 的 direct fact output、reference/customer signal 与当前 slice 的无-projection-hook 边界。

#### Verification Method

- [real-data validation](./standards/verification-method/real-data-validation.md) : 定义何为真实数据验证及其适用边界。
- [golden scenarios](./standards/verification-method/golden-scenarios.md) : 定义 scenario taxonomy 与 golden asset 的角色。

### Evidence

- [输入现实证据](./evidence/input-reality-evidence.md) : 聚合输入形态、sheet、fixture 与 real-data 相关证据。
- [`annual_award` 字段处理证据](./evidence/annual-award-field-processing-evidence.md) : 把 annual_award 的 multi-sheet intake、business-type 派生与 plan-code enrichment 写成 contract-grade 证据页。
- [`annual_loss` 字段处理证据](./evidence/annual-loss-field-processing-evidence.md) : 把 annual_loss 的 date normalization、product-line mapping、current-row lookup 与 temp-id 边界写成 contract-grade 证据页。
- [`annuity_performance` 字段处理证据](./evidence/annuity-performance-field-processing-evidence.md) : 将 annuity-performance 的字段处理分成工程性质量提升与业务语义处理两类。
- [`annuity_performance` implementation gap 证据](./evidence/annuity-performance-implementation-gap-evidence.md) : 记录 annuity-performance 的 wiki 合同与 legacy 实现之间的差距项。
- [身份与补查证据](./evidence/identity-and-lookup-evidence.md) : 聚合 `company_id`、temp-id、lookup、plan-code enrichment 相关证据。
- [状态与快照证据](./evidence/status-and-snapshot-evidence.md) : 聚合客户状态、快照、customer MDM 相关证据。
- [`is_new` 对象级证据](./evidence/is-new-evidence.md) : 聚合 `is_new` 的公式、粒度边界、非例与验证路径。
- [`is_winning_this_year` 对象级证据](./evidence/is-winning-this-year-evidence.md) : 聚合年度中标状态的事实来源、粒度边界与验证路径。
- [`is_loss_reported` 对象级证据](./evidence/is-loss-reported-evidence.md) : 聚合年度流失申报状态的事实来源、粒度边界与验证路径。
- [验证资产证据](./evidence/verification-assets-evidence.md) : 聚合 golden set、replay baseline、validation guide、error fixtures 等证据。
- [validation result history 证据](./evidence/validation-result-history-evidence.md) : 聚合 legacy parity result 目录、current asset registry 与 validation history 的治理结论。
- [operator 与 surface 证据](./evidence/operator-and-surface-evidence.md) : 聚合 queue、reference sync、manual commands 与 operator artifacts 相关证据。
- [`annuity_income` 专题证据](./evidence/annuity-income-gap-evidence.md) : 聚合 annuity_income 的专题差异，并把细节分发到对象级 evidence page。
- [`annuity_income` 字段处理证据](./evidence/annuity-income-field-processing-evidence.md) : 把 annuity_income 的关键字段处理分成工程性质量提升与业务语义处理。
- [`annuity_income` branch mapping 证据](./evidence/annuity-income-branch-mapping-evidence.md) : 固化 `COMPANY_BRANCH_MAPPING` manual overrides 与 placement gap。
- [`annuity_income` ID5 retirement 证据](./evidence/annuity-income-id5-retirement-evidence.md) : 固化 ID5 fallback retirement 的历史决策与验证边界。
- [`annuity_income` operator artifacts 证据](./evidence/annuity-income-operator-artifacts-evidence.md) : 固化 `unknown_names_csv` 与 failed-record export 的 operator-facing 角色。

### Meta

- [设计草案](./_meta/wiki-design.md) : `wiki-bi` 的顶层 schema、规则与运营模型。
- [domain wiki 升级框架](./_meta/wiki-domain-upgrade-framework.md) : 定义如何把某个高价值 domain 从导航页升级成可直接问答的合同级 wiki。
- [wiki maintenance lint checklist](./_meta/wiki-maintenance-lint-checklist.md) : 为 substantial wiki maintenance round 提供轻量完工 gate。
- [轻量实施计划](./_meta/wiki-implementation-plan.md) : 首批 seed scaffold 的实施范围、顺序与完成定义。
- [吸收工作流](./_meta/wiki-absorption-workflow.md) : 定义主题簇吸收、分类 gate、每轮输出与验收清单。
- [吸收路线图](./_meta/wiki-absorption-roadmap.md) : 定义主题簇整体顺序与每轮主入口页。
- [吸收轮次索引](./_meta/absorption-rounds/index.md) : 记录每轮闭环的经验沉淀与下一轮入口。
- [Round 01：状态与快照](./_meta/absorption-rounds/round-01-status-and-snapshot.md) : 首轮闭环沉淀，记录状态与快照主题簇的稳定结论、可复用经验与下一轮目标。
- [Round 02：身份与补查](./_meta/absorption-rounds/round-02-identity-and-lookup.md) : 第二轮闭环沉淀，记录 `company_id`、temp-id、lookup surface 与下一轮目标。
- [Round 03：输入现实](./_meta/absorption-rounds/round-03-input-reality.md) : 第三轮闭环沉淀，记录真实输入形态、版本策略、sheet contract 与下一轮目标。
- [Round 04：验证资产](./_meta/absorption-rounds/round-04-verification-assets.md) : 第四轮闭环沉淀，记录 golden set、replay baseline、error-case fixture 与下一轮目标。
- [Round 05：operator 与 surfaces](./_meta/absorption-rounds/round-05-operator-and-surfaces.md) : 第五轮闭环沉淀，记录 reference sync、manual commands、failed-record export 与下一轮目标。
- [Round 06：`annuity_income` 专题补强](./_meta/absorption-rounds/round-06-annuity-income.md) : 第六轮闭环沉淀，记录 annuity_income 的制度记忆、身份差异、验证资产与 operator artifact 缺口。
- [Round 07：`is_new` 对象级证据拆分](./_meta/absorption-rounds/round-07-is-new-evidence-split.md) : follow-on 轮次，验证厚主题拆分为对象级 evidence page 的可行性。
- [Round 08：`annuity_income` slice admission package](./_meta/absorption-rounds/round-08-annuity-income-slice-admission.md) : follow-on 轮次，把 annuity_income 的专题 gap 转成可直接支撑 slice admission 的对象级 evidence。
- [Round 09：legacy wiki 退役收口](./_meta/absorption-rounds/round-09-legacy-wiki-retirement.md) : follow-on 轮次，记录旧 wiki 层的退役收口与 durable 归宿。
- [Round 10：domain 导航与 cross-reference 收紧](./_meta/absorption-rounds/round-10-domain-navigation-tightening.md) : maintenance 轮次，记录低入链 durable pages 的 lint 结果与导航收紧经验。
- [Round 11：Phase E operator/runtime surfaces decision package](./_meta/absorption-rounds/round-11-phase-e-surface-decision-package.md) : follow-on 轮次，把 surface open questions 收束成 enterprise persistence、standalone tooling 与 operator/runtime decision package。
- [Round 12：verification result history and fixture governance](./_meta/absorption-rounds/round-12-verification-result-history-and-fixture-governance.md) : follow-on 轮次，把 validation result history、error-case fixtures 与 deferred asset 状态收束成正式治理对象。
- [Round 13：identity governance deepening](./_meta/absorption-rounds/round-13-identity-governance-deepening.md) : follow-on 轮次，把 identity governance 从概念/证据碎片推进到独立标准层。
- [Round 14：status family selective evidence split](./_meta/absorption-rounds/round-14-status-family-selective-evidence-split.md) : follow-on 轮次，只拆出真正满足阈值的状态对象，并明确哪些状态继续留在主题页。
- [Round 15：`annuity_performance` I/O contracts](./_meta/absorption-rounds/round-15-annuity-performance-io-contracts.md) : follow-on 轮次，把 annuity-performance 的输入、输出与字段处理提升为合同级 wiki 页面。
- [Round 16：`annuity_performance` implementation gap audit](./_meta/absorption-rounds/round-16-annuity-performance-gap-audit.md) : maintenance 轮次，对照 legacy 代码审计 annuity-performance wiki 合同与实现差距。
- [Round 17：domain upgrade workflow pattern](./_meta/absorption-rounds/round-17-domain-upgrade-workflow-pattern.md) : maintenance 轮次，把 annuity-performance 的有效升级路径提炼成可复用框架。
- [Round 18：`annuity_income` domain upgrade and maintenance controls](./_meta/absorption-rounds/round-18-annuity-income-domain-upgrade-and-maintenance-controls.md) : maintenance 轮次，收紧维护者发现路径，并把 annuity_income 升级到合同级问答入口。
- [Round 19：event-domain contract upgrade and evidence governance tightening](./_meta/absorption-rounds/round-19-event-domain-contract-upgrade-and-evidence-governance.md) : maintenance 轮次，把 `annual_award` / `annual_loss` 升级到合同级入口，并把 evidence / lint 固定产物收紧成正式治理规则。
- [LLM Wiki 参考](./_meta/llm-wiki.md) : 上位方法论参考文本。
- [变更日志](./log.md) : 按日期与时间记录 `wiki-bi` 的搭建与后续增量维护。

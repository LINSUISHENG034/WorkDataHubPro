# `wiki-bi` 吸收路线图

> 状态：Active
> 日期：2026-04-14
> 作用：给 `wiki-bi` 的内容吸收提供整体顺序和每轮主题边界

---

## Round 1：状态与快照

目标：

- 把客户状态、快照粒度、customer MDM 命令面和相关证据关系写实

主入口页：

- `evidence/status-and-snapshot-evidence.md`
- `concepts/customer-status.md`
- `concepts/is-new.md`
- `standards/semantic-correctness/customer-status-semantics.md`
- `surfaces/customer-mdm-commands.md`

状态：

- completed on 2026-04-14

## Round 2：身份与补查

目标：

- 强化 `company_id`、temp-id、lookup queue、identity fallback chain、plan-code enrichment 相关内容

主入口页：

- `evidence/identity-and-lookup-evidence.md`
- `concepts/company-id.md`
- `surfaces/company-lookup-queue.md`
- `surfaces/unknown-names-csv.md`

状态：

- completed on 2026-04-14

## Round 3：输入现实

目标：

- 强化 real-data sample、sheet 结构、目录策略、fixture 边界与输入现实合同

主入口页：

- `evidence/input-reality-evidence.md`
- `standards/input-reality/input-reality-contracts.md`
- `concepts/plan-type.md`

状态：

- completed on 2026-04-14

## Round 4：验证资产

目标：

- 强化 golden set、replay baseline、error-case fixture、validation guide 等验证资产治理

主入口页：

- `evidence/verification-assets-evidence.md`
- `standards/verification-method/golden-scenarios.md`
- `standards/verification-method/real-data-validation.md`

状态：

- completed on 2026-04-14

## Round 5：operator 与 surfaces

目标：

- 补强 reference sync、failed-record export、enterprise persistence、GUI / standalone tool 的治理识别

主入口页：

- `evidence/operator-and-surface-evidence.md`
- `surfaces/reference-sync.md`
- `surfaces/failed-record-export.md`

状态：

- completed on 2026-04-14

## Round 6：`annuity_income` 专题补强

目标：

- 防止 `annuity_income` 的 legacy-only 资产和未闭合问题继续掉出视野

主入口页：

- `domains/annuity-income.md`
- `evidence/verification-assets-evidence.md`
- `evidence/identity-and-lookup-evidence.md`

状态：

- completed on 2026-04-14

## Follow-on Round 07：`is_new` 对象级证据拆分

目标：

- 验证对象级 evidence page 拆分机制是否有效

主入口页：

- `evidence/is-new-evidence.md`
- `concepts/is-new.md`
- `concepts/customer-status.md`

状态：

- completed on 2026-04-14

## Follow-on Round 08：`annuity_income` slice admission package

目标：

- 把 `annuity_income` 的制度记忆转成 slice-admission-ready evidence
- 把 branch mapping、ID5 retirement、operator artifacts 从专题 gap 页拆成对象级 evidence
- 在不提前卷入 Phase E surface 决策的前提下，为下一份可执行 slice plan 建立稳定入口

主入口页：

- `evidence/annuity-income-gap-evidence.md`
- `evidence/annuity-income-branch-mapping-evidence.md`
- `evidence/annuity-income-id5-retirement-evidence.md`
- `evidence/annuity-income-operator-artifacts-evidence.md`

状态：

- completed on 2026-04-14

## Follow-on Round 09：legacy wiki 退役收口

目标：

- 把旧 wiki 层从并行知识层收口并移除
- 明确 `project/`、`roadmap/`、`phases/`、`governance/`、`lessons/`、`_meta/` 的 durable 去向
- 在保留 provenance 的前提下，停止让旧 wiki 层出现在当前权威文档里

主入口页：

- `docs/system/index.md`
- `docs/wiki-bi/index.md`
- `docs/wiki-bi/_meta/absorption-rounds/round-09-legacy-wiki-retirement.md`

状态：

- completed on 2026-04-14

## 当前位置

首批六轮吸收已经完成，follow-on Round 07、Round 08 与 Round 09 也已经完成。

Round 10 已完成当前 wiki 的导航收紧与低入链维护。

后续如需继续推进，不建议再按“还能补哪些零散页”来选题，而应按预估收益大小推进。

## 下一阶段收益排序

### 1. Round 11：Phase E operator/runtime surfaces decision package

预估收益：最高

原因：

- 当前 `wiki-bi` 中最集中的 open question 已经收敛到 surface 治理主题，而不是 domain 语义主题
- `operator-and-surface-evidence.md` 已明确指出 `reference_sync`、`company_lookup_queue`、manual `customer-mdm` commands、enterprise persistence、GUI / standalone tools 仍处于未决状态
- 这组问题横跨 identity、operator、runtime、artifact 与 future rebuild governance，收口后能直接提高后续设计与 slice admission 的决策质量
- legacy raw sources 已经足够丰富，包括 CLI dispatch、runbook、`reference_sync.yml`、`customer_mdm` 模块、`enterprise.enrichment_requests` / `enterprise.enrichment_index` 相关代码路径

目标：

- 把 Phase E surface 相关对象从“已知存在”推进到“明确的治理问题陈述”
- 对 `retain / replace / retire / defer` 形成对象级 evidence package，而不是继续停留在泛化 evidence page 里
- 优先收紧 `reference_sync`、`company_lookup_queue`、manual `customer-mdm` commands、enterprise persistence、standalone `cleanse` CLI、GUI tooling 之间的边界

主入口页：

- `evidence/operator-and-surface-evidence.md`
- `surfaces/reference-sync.md`
- `surfaces/company-lookup-queue.md`
- `surfaces/customer-mdm-commands.md`

状态：

- proposed

### 2. Round 12：verification result history and fixture governance

预估收益：高

原因：

- 当前验证资产层已经有较完整的 taxonomy，但 `validation result history`、error-case fixtures、domain-level golden set 仍未制度化收口
- 这组内容直接决定 future acceptance story 是否可追溯，收益仅次于 surface decision package
- `verification_guide_real_data.md`、`dataset_requirements.md`、legacy parity validation guide 与 current replay registry 已经形成足够强的 raw-source 基底

目标：

- 把 validation result history 从“存在于 legacy / replay 记忆中”推进到明确 evidence object
- 收紧 error-case fixtures 的 `planned but not created` 语义，不让它继续处于模糊状态
- 判断 `annual_award` / `annual_loss` 是否需要独立 domain-level golden set，至少把判断边界写清楚

主入口页：

- `evidence/verification-assets-evidence.md`
- `standards/verification-method/golden-scenarios.md`
- `standards/verification-method/real-data-validation.md`

状态：

- proposed

### 3. Round 13：identity governance deepening

预估收益：中高

原因：

- `company_id` 相关基础语义已经吸收，但 identity governance 仍缺少更明确的标准层表达
- `temp-id`、ID1-ID5 mapping files、branch mapping、queue / cache / provider 边界仍分散在 evidence 与 domain 记忆中
- 这轮的收益高于继续做状态对象级拆分，因为它更直接服务后续 identity-related design 与 rebuild review

目标：

- 判断是否需要新增独立 identity governance standard，或者继续以现有标准页承载但收紧结构
- 继续把 `temp-id`、mapping files、identity fallback chain 的制度边界从主题 evidence page 中拆得更清楚
- 把 `annuity_income` 已拆出的 branch mapping / ID5 记忆，与 broader identity governance 重新接回

主入口页：

- `evidence/identity-and-lookup-evidence.md`
- `concepts/company-id.md`
- `concepts/temp-id.md`
- `surfaces/company-lookup-queue.md`

状态：

- proposed

### 4. Round 14：selective object-level evidence split for status family

预估收益：中

原因：

- `is_new` 的对象级拆分已经证明机制可行，但继续拆 `is_winning_this_year`、`is_loss_reported`、`is_churned_this_year` 的边际收益不如前三项
- 这轮更适合作为结构优化，而不是当前阶段的主攻方向

目标：

- 只在明确满足拆分阈值时，继续做状态家族的对象级 evidence page
- 优先服务高频复用对象，而不是机械式把所有状态都拆成单页

主入口页：

- `evidence/status-and-snapshot-evidence.md`
- `concepts/customer-status.md`
- `standards/semantic-correctness/customer-status-semantics.md`

状态：

- deferred until higher-yield rounds complete

## 下一阶段执行顺序

建议按下面顺序推进：

1. Round 11：Phase E operator/runtime surfaces decision package
2. Round 12：verification result history and fixture governance
3. Round 13：identity governance deepening
4. Round 14：selective object-level evidence split for status family

## 当前推荐入口

当前最推荐的下一轮入口是 Round 11。

它的价值不在于“再补几页 surface 文档”，而在于把 current wiki 已知但尚未收口的治理难题，转成一组可直接被后续架构/切片决策引用的 durable evidence package。

后续如需继续推进，应从下面几类 follow-on work 中选择：

- 把 `annuity_income` slice 执行过程中形成的新稳定结论继续回写到 wiki
- 以 Round 11 为主线，继续判断 `CT-016` 与 Phase E operator/runtime surfaces 的 retain / replace / retire 边界
- 完成 Round 11 后，再进入 validation / identity / selective split 这三类 follow-on round
- 旧 wiki 层的物理删除已于 2026-04-14 完成；后续只需在发现新的历史硬引用时继续回修

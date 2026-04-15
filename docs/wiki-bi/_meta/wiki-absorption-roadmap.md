# `wiki-bi` 吸收路线图

> 状态：Active
> 日期：2026-04-15
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
Round 11 已完成 Phase E operator/runtime surfaces decision package。
Round 12 已完成 verification result history and fixture governance。
Round 13 已完成 identity governance deepening。
Round 14 已完成 status family selective evidence split。
Round 15 已完成 `annuity_performance` I/O contracts。
Round 16 已完成 `annuity_performance` implementation gap audit。
Round 17、Round 18、Round 19 与 Round 20 已把 domain-upgrade workflow、`annuity_income` 合同入口、event-domain 对称升级以及 verification-asset adjudication 进一步收口。

后续如需继续推进，不建议再按“还能补哪些零散页”来选题，而应继续按预估收益大小推进。

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

- completed on 2026-04-14

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

- completed on 2026-04-14

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

- completed on 2026-04-14

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

- completed on 2026-04-14

## 短期计划（2026-04-15）

Round 20 完成后，当前 wiki 已不再主要缺“domain I/O 问答入口”，也不再缺 verification asset 的基础裁决表达，而是更缺：

- Phase E surface 的边界关闭
- 高流量 evidence 页的模板一致性

因此这批短期计划里，Round 20 已完成，剩余重点应继续推进下面两轮，而不是回到“机会式维护”：

### Round 20：verification asset adjudication package

预估收益：最高

原因：

- [验证资产证据](../evidence/verification-assets-evidence.md) 与 [validation result history 证据](../evidence/validation-result-history-evidence.md) 已经把问题对象识别清楚，但状态词仍不够收束
- 这组问题直接影响后续 acceptance story、adjudication memory 与 slice governance
- 相比继续补 domain 页面，这一轮对未来决策的杠杆更高

主入口页：

- `evidence/verification-assets-evidence.md`
- `evidence/validation-result-history-evidence.md`
- `standards/verification-method/golden-scenarios.md`

状态：

- completed on 2026-04-15

### Round 21：Phase E surface decision closure

预估收益：高

原因：

- Round 11 已经把主要 surface 对象显式登记，但 retain / replace / retire / defer 仍未闭环
- `reference_sync`、`company_lookup_queue` 与 enterprise persistence 都已经足够成熟，不应继续长期停留在“还需独立决策”的状态
- 这轮直接服务 future architecture / runtime governance，而不是重复对象识别

主入口页：

- `evidence/operator-and-surface-evidence.md`
- `surfaces/reference-sync.md`
- `surfaces/company-lookup-queue.md`
- `surfaces/enterprise-enrichment-persistence.md`

状态：

- planned on 2026-04-15

### Round 22：high-traffic evidence normalization

预估收益：中高

原因：

- Round 19 已经把 evidence 最小模板制度化
- 但 [状态与快照证据](../evidence/status-and-snapshot-evidence.md)、[验证资产证据](../evidence/verification-assets-evidence.md)、[operator 与 surface 证据](../evidence/operator-and-surface-evidence.md) 仍未完全收紧到统一骨架
- 这轮适合作为 Round 20 / 21 之后的维护收口，而不是抢在高价值结论之前做纯格式整理

主入口页：

- `evidence/status-and-snapshot-evidence.md`
- `evidence/verification-assets-evidence.md`
- `evidence/operator-and-surface-evidence.md`

状态：

- planned on 2026-04-15

## 下一阶段执行顺序

建议按下面顺序推进：

1. Round 21：Phase E surface decision closure
2. Round 22：high-traffic evidence normalization

执行原则：

- 先收口影响 acceptance / governance 判断的高价值结论
- 再处理模板一致性与 lint 友好性
- 只有新的实现、验证或治理结论真正稳定后，才继续回写 durable page

## 当前推荐入口

当前最推荐的立即动作是从 Round 21 启动。

原因不是它“最容易写”，而是：

- Round 20 已把 verification asset 的裁决表达收口，后续最集中的未决问题重新回到了 surface closure
- `reference_sync`、`company_lookup_queue` 与 enterprise persistence 都已经具备足够 raw-source 基底，不应继续长期维持“对象已识别但边界未闭合”的状态
- Round 21 的结论会直接影响 future architecture / runtime governance，而不是重复对象识别

如果当前工作流仍更偏 verification lint，而不是 surface closure，则可改从 Round 22 启动。

Round 22 仍不应抢在 Round 21 之前执行，除非本次任务本身就是 wiki lint / evidence 模板收紧。

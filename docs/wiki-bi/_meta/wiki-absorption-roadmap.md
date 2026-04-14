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

后续如需继续推进，应从下面几类 follow-on work 中选择：

- 把 `annuity_income` slice 执行过程中形成的新稳定结论继续回写到 wiki
- 继续判断 `CT-016` 与 Phase E operator/runtime surfaces 的 retain / replace / retire 边界
- 只在确有复用价值时继续做新的对象级 evidence 拆分
- 旧 wiki 层的物理删除已于 2026-04-14 完成；后续只需在发现新的历史硬引用时继续回修

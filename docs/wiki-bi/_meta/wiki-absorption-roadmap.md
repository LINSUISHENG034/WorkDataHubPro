# `wiki-bi` 吸收路线图

> 状态：Active
> 日期：2026-04-16
> 作用：给 `wiki-bi` 的内容吸收提供整体顺序和每轮主题边界

---

## 基础主题簇（已完成）

### Round 1：状态与快照

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

### Round 2：身份与补查

目标：

- 强化 `company_id`、temp-id、lookup queue、identity fallback chain、plan-code enrichment 相关内容

主入口页：

- `evidence/identity-and-lookup-evidence.md`
- `concepts/company-id.md`
- `surfaces/company-lookup-queue.md`
- `surfaces/unknown-names-csv.md`

状态：

- completed on 2026-04-14

### Round 3：输入现实

目标：

- 强化 real-data sample、sheet 结构、目录策略、fixture 边界与输入现实合同

主入口页：

- `evidence/input-reality-evidence.md`
- `standards/input-reality/input-reality-contracts.md`
- `concepts/plan-type.md`

状态：

- completed on 2026-04-14

### Round 4：验证资产

目标：

- 强化 golden set、replay baseline、error-case fixture、validation guide 等验证资产治理

主入口页：

- `evidence/verification-assets-evidence.md`
- `standards/verification-method/golden-scenarios.md`
- `standards/verification-method/real-data-validation.md`

状态：

- completed on 2026-04-14

### Round 5：operator 与 surfaces

目标：

- 补强 reference sync、failed-record export、enterprise persistence、GUI / standalone tool 的治理识别

主入口页：

- `evidence/operator-and-surface-evidence.md`
- `surfaces/reference-sync.md`
- `surfaces/failed-record-export.md`

状态：

- completed on 2026-04-14

### Round 6：`annuity_income` 专题补强

目标：

- 防止 `annuity_income` 的 legacy-only 资产和未闭合问题继续掉出视野

主入口页：

- `domains/annuity-income.md`
- `evidence/verification-assets-evidence.md`
- `evidence/identity-and-lookup-evidence.md`

状态：

- completed on 2026-04-14

## Follow-on 轮次（已完成）

### Round 07：`is_new` 对象级证据拆分

主入口页：

- `evidence/is-new-evidence.md`
- `concepts/is-new.md`
- `concepts/customer-status.md`

状态：

- completed on 2026-04-14

### Round 08：`annuity_income` slice admission package

主入口页：

- `evidence/annuity-income-gap-evidence.md`
- `evidence/annuity-income-branch-mapping-evidence.md`
- `evidence/annuity-income-id5-retirement-evidence.md`
- `evidence/annuity-income-operator-artifacts-evidence.md`

状态：

- completed on 2026-04-14

### Round 09：legacy wiki 退役收口

主入口页：

- `docs/system/index.md`
- `docs/wiki-bi/index.md`
- `docs/wiki-bi/_meta/absorption-rounds/round-09-legacy-wiki-retirement.md`

状态：

- completed on 2026-04-14

## Maintenance 轮次（已完成）

### Round 10-23

覆盖范围：

- domain 导航与 cross-reference 收紧
- Phase E operator/runtime surfaces decision package
- verification result history and fixture governance
- identity governance deepening
- status family selective evidence split
- `annuity_performance` I/O contracts 与 implementation gap audit
- domain upgrade workflow pattern
- `annuity_income` 合同入口升级
- event-domain contract upgrade
- verification asset adjudication package
- Phase E surface decision closure
- high-traffic evidence normalization
- production-sample augmentation

状态：

- completed on 2026-04-15

## Round 24-27：legacy 隐含语义补强（已完成）

### Round 24：引用同步与回填语义收紧

目标：

- 把 `reference_sync` 与 `backfill` 从模糊补齐逻辑拆成两个独立治理对象

主入口页：

- `evidence/reference-and-backfill-evidence.md`
- `concepts/backfill.md`
- `surfaces/reference-sync.md`

状态：

- completed on 2026-04-16

### Round 25：身份治理语义分层收紧

目标：

- 把 identity governance 收紧成“当前运行路径 / 历史记忆 / 已退休行为 / operator-visible consequence”四层表达

主入口页：

- `concepts/company-id.md`
- `concepts/temp-id.md`
- `standards/semantic-correctness/identity-governance.md`
- `surfaces/company-lookup-queue.md`
- `surfaces/enterprise-enrichment-persistence.md`

状态：

- completed on 2026-04-16

### Round 26：状态与快照生命周期补强

目标：

- 为 `customer-mdm` 年度生命周期补齐对象级证据，并继续保持概念层与命令面的分层

主入口页：

- `evidence/customer-mdm-lifecycle-evidence.md`
- `concepts/customer-status.md`
- `standards/semantic-correctness/customer-status-semantics.md`

状态：

- completed on 2026-04-16

### Round 27：legacy 语义补强收口

目标：

- 对四个高流量 domain 与 shared operator / verification pages 做最后一轮对象级补强与 cross-link 收口

主入口页：

- `domains/annuity-performance.md`
- `domains/annuity-income.md`
- `domains/annual-award.md`
- `domains/annual-loss.md`
- `evidence/operator-and-surface-evidence.md`
- `evidence/verification-assets-evidence.md`

状态：

- completed on 2026-04-16

## 当前位置

`wiki-bi` 当前已经完成基础主题簇、follow-on 拆分、主干 maintenance 轮次，以及 Round 24-27 的 legacy 隐含语义补强。

当前应明确保持两条边界：

- durable wiki 只保留业务语义、标准、surface、evidence 与 round sediment
- subagent / worktree / merge sequencing 这类执行层材料不再放在 `docs/wiki-bi/`，应留在 `docs/superpowers/`、`.planning/` 或 git history

## 当前推荐入口

如果后续继续推进，推荐优先从以下对象簇重新做收益排序：

- 仍有显著 `当前证据缺口` 的 aggregate evidence family
- 仍停留在 shared page、但已具备对象级拆分条件的高频对象
- 仍需要补 current-side evidence 或 current-side decision package 的 surface / verification topic

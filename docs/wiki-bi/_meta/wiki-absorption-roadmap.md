# `wiki-bi` 吸收路线图

> 状态：Active
> 日期：2026-04-19
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

## Round 24-31：legacy 隐含语义补强（已完成）

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

### Round 28：customer-master derived signals 收紧

目标：

- 把 `tags`、`主拓机构` 与 cross-domain customer-master-derived signals 从 scattered mentions 收紧成 durable concepts + evidence dispatcher

主入口页：

- `evidence/customer-master-signals-evidence.md`
- `concepts/tags.md`
- `concepts/primary-branch.md`
- `concepts/backfill.md`

状态：

- completed on 2026-04-18

### Round 29：legacy 业务语义扩展包

目标：

- 把 `关键年金计划`、`is_churned_this_year` shared coverage 与 classification family 推进成新的 durable business-semantics 入口

主入口页：

- `concepts/key-annuity-plan.md`
- `evidence/customer-master-signals-evidence.md`
- `concepts/customer-status.md`
- `evidence/status-and-snapshot-evidence.md`
- `evidence/classification-family-evidence.md`
- `concepts/plan-type.md`

状态：

- completed on 2026-04-18

### Round 30：relationship breadth deepening

目标：

- 把 `关联计划数` 从 dispatcher 提示推进成 durable relationship-breadth 对象页

主入口页：

- `concepts/related-plan-count.md`
- `evidence/customer-master-signals-evidence.md`
- `concepts/key-annuity-plan.md`
- `domains/annuity_performance.md`
- `domains/annuity_income.md`

状态：

- completed on 2026-04-18

### Round 31：relationship breadth and classification closeout

目标：

- 把 `关联机构数` 补成 durable relationship-breadth object page，并把 `管理资格` 从 classification dispatcher 提升为独立概念页

主入口页：

- `concepts/related-branch-count.md`
- `concepts/management-qualification.md`
- `evidence/customer-master-signals-evidence.md`
- `evidence/classification-family-evidence.md`

状态：

- completed on 2026-04-18

## Round 32：shared unresolved artifact governance（已完成）

目标：

- 把 shared unresolved-name / failed-record artifact family 从 scattered gap text 收紧成 durable evidence dispatcher

主入口页：

- `evidence/unresolved-name-and-failed-record-evidence.md`
- `surfaces/company-lookup-queue.md`
- `surfaces/unknown-names-csv.md`
- `surfaces/failed-record-export.md`

状态：

- completed on 2026-04-18

## Round 33：reference_sync governance（已完成）

目标：

- 把 `reference_sync` 的 target inventory、incremental sync-state 与 current replacement boundary 收紧成 durable object-level evidence route

主入口页：

- `evidence/reference-sync-runtime-and-state-evidence.md`
- `surfaces/reference-sync.md`
- `evidence/reference-and-backfill-evidence.md`

状态：

- completed on 2026-04-19

## Round 34：relationship breadth list deepening（已完成）

目标：

- 把 `其他年金计划` 与 `其他开拓机构` 从 dispatcher-only 提示推进成 durable relationship-breadth list objects

主入口页：

- `concepts/other-annuity-plans.md`
- `concepts/other-branches.md`
- `evidence/customer-master-signals-evidence.md`

状态：

- completed on 2026-04-19

## Round 35：portfolio anchor tightening（已完成）

目标：

- 把 `组合代码` 从 dispatcher / field-processing 交叉入口层推进成 durable portfolio-anchor object

主入口页：

- `concepts/portfolio-code.md`
- `evidence/classification-family-evidence.md`
- `concepts/plan-type.md`

状态：

- completed on 2026-04-19

## 当前位置

`wiki-bi` 当前已经完成基础主题簇、follow-on 拆分、主干 maintenance 轮次、Round 24-31 的 legacy 隐含语义补强、Round 32-33 的第一批 semantic-map-adjacent surface-discovery 收口，以及 Round 34-35 对 remaining high-value business-semantics queue 的收口。

当前应明确保持两条边界：

- durable wiki 只保留业务语义、标准、surface、evidence 与 round sediment
- subagent / worktree / merge sequencing 这类执行层材料不再放在 `docs/wiki-bi/`，应留在 `docs/superpowers/`、`.planning/` 或 git history

## 下阶段：业务语义与 surface discovery 双轨收口

Round 29 到 Round 31 已经把 dominant value / breadth count / classification family 的高价值对象补了一轮；Round 32 把 shared unresolved-name / failed-record artifact family 从“gap-only 提示”推进成了 durable evidence dispatcher；Round 33 则把 `reference_sync` 的 target inventory / sync-state / replacement boundary 补成了对象级 evidence route；Round 34-35 则把 remaining relationship-breadth list side 与 portfolio-anchor side 收口成 durable objects。

因此，当前已经没有另一个同等明显、仍停留在 dispatcher-only 的 high-value business-semantics candidate。若没有新的 raw-source sweep 改变这个判断，下一步更合理的方向应回到 semantic-map-first 的 runtime/operator discovery。

工作原则：

- `docs/wiki-bi/` 仍是唯一长期知识层
- `docs/wiki-bi/_meta/legacy-semantic-map/` 只是内部发现账本，不进入 durable catalog
- semantic map 负责暴露 coverage holes、source provenance、open questions 与 candidate boundaries
- semantic-map ledger registration alone does not justify semantic promotion；runtime/operator surfaces 只有在达到 `Stable Finding` 阈值后才允许进入 durable wiki
- durable wiki 只吸收已经达到 `Stable Finding` 阈值的对象、标准、surface 与 domain 结论
- 一旦目标吸收波次完成，semantic map 对应波次应进入归档评估，而不是继续并行维护

双轨顺序：

1. 若目标是继续补 business semantics，只在新的 raw-source sweep 发现真正达到 standalone question-answer 阈值的对象时再 promotion
2. 若目标是补 runtime/operator truth，则先围绕 first-wave 未闭合的 cross-cutting surfaces 开 discovery wave，而不是重复已完成的相邻 business-semantics closeout
3. 每个 discovery wave 先补 semantic map，再把稳定结论吸收到 `evidence/`
4. `evidence/` 稳定后，再回写 `concepts/`、`standards/`、`surfaces/`、`domains/`
5. wiki 更新被接受后，关闭对应 semantic-map wave，并评估 claims / tooling 的归档

remaining business-semantic candidates：

- 当前无同等明显的 dispatcher-only high-value object；除非后续 raw-source sweep 暴露新的独立语义对象

## 优先 discovery 主题簇

建议优先围绕下列仍未闭合的语义带做 semantic-map-first discovery：

- `company_lookup_queue` 的异步重试、恢复与 operator-visible consequence
- `reference_sync` 的 authoritative sync-state 与 retained-or-replaced runtime boundary
- enterprise identity / EQC persistence surfaces 的 retain / defer / retire decision package
- manual `customer-mdm` command surfaces 的保留边界与 current-side evidence
- shared unresolved-name / failed-record artifacts 的跨域治理与 runbook evidence

## 当前推荐入口

如果马上继续推进，推荐按下面顺序开工：

- surface-discovery track：manual `customer-mdm` + enterprise persistence closure wave

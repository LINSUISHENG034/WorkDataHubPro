# Round 08：`annuity_income` slice admission package

> 状态：Completed
> 日期：2026-04-14
> 主题簇：annuity-income / slice-admission bridge

## 本轮目标

- 把 `annuity_income` 的 institutional memory 转成 slice-admission-ready evidence
- 把 branch mapping、ID5 retirement、operator artifacts 从专题 gap 页拆成可直接引用的对象级 evidence page
- 为后续 `annuity_income` executable slice plan 提供比 audit summary 更稳定的引用入口

## 使用的 raw sources

- `E:\Projects\WorkDataHub\docs\domains\annuity_income.md`
- `E:\Projects\WorkDataHub\docs\domains\annuity_income-capability-map.md`
- `E:\Projects\WorkDataHub\docs\cleansing-rules\annuity-income.md`
- `E:\Projects\WorkDataHub\docs\guides\validation\legacy-parity-validation.md`
- `docs/superpowers/audits/2026-04-12-legacy-code-audit.md`
- `docs/superpowers/audits/2026-04-12-verification-assets-search-findings.md`

## 本轮吸收的 Stable Findings

- `COMPANY_BRANCH_MAPPING` manual overrides 是 `annuity_income` 的稳定清洗合同，不是可忽略的迁移注释
- ID5 fallback retirement 是显式历史决策，后续 slice 只能保护它，不能意外复活它
- `unknown_names_csv` 与 failed-record export 对 `annuity_income` 来说是 operator-facing artifact，不只是 debug 输出
- `annuity_income` slice 可以先围绕 AI-001 到 AI-005 入场，不必把 `company_lookup_queue`、`reference_sync`、manual `customer-mdm` 等 Phase E surface 决策提前卷进同一轮

## 本轮更新的目标页

- `docs/wiki-bi/evidence/annuity-income-gap-evidence.md`
- `docs/wiki-bi/evidence/annuity-income-branch-mapping-evidence.md`
- `docs/wiki-bi/evidence/annuity-income-id5-retirement-evidence.md`
- `docs/wiki-bi/evidence/annuity-income-operator-artifacts-evidence.md`
- `docs/wiki-bi/evidence/identity-and-lookup-evidence.md`
- `docs/wiki-bi/evidence/operator-and-surface-evidence.md`
- `docs/wiki-bi/evidence/verification-assets-evidence.md`
- `docs/wiki-bi/domains/annuity-income.md`
- `docs/wiki-bi/standards/verification-method/golden-scenarios.md`
- `docs/wiki-bi/surfaces/unknown-names-csv.md`
- `docs/wiki-bi/surfaces/failed-record-export.md`
- `docs/superpowers/plans/2026-04-14-workdatahubpro-annuity-income-validation-slice.md`
- `docs/superpowers/specs/2026-04-11-workdatahubpro-first-wave-legacy-coverage-matrix.md`

## 可复用经验

- 当某个 domain 已经成为 governance 上的 next recommended slice 时，继续做泛化的 evidence split 通常不如先把它的 admission package 做实
- 对象级 evidence page 最适合承接“必须被未来 slice plan 直接引用”的稳定记忆，而不是继续堆在专题型 gap 页里
- wiki 可以保持 problem-space 角色，同时为 slice admission 提供稳定输入，不必退化成执行流水账

## 下一步建议

- 以 `docs/superpowers/plans/2026-04-14-workdatahubpro-annuity-income-validation-slice.md` 为入口进入真正的 `annuity_income` slice planning / execution
- 在 slice 执行过程中，把 branch mapping placement、artifact retention shape、intentional parity diffs 的稳定结论继续回写到这批对象级 evidence 页
- 保持 `CT-016` 的 broader cross-domain artifact parity 为显式 follow-on，而不是假装在本轮已全部闭合

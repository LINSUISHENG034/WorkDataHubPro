# Round 06：`annuity_income`

> 状态：Completed
> 日期：2026-04-14
> 主题簇：annuity-income

## 本轮目标

- 防止 `annuity_income` 的 legacy-only 制度记忆继续掉出 wiki 视野
- 把 annuity_income 的身份差异、验证资产缺口与 operator artifact gap 集中收束

## 使用的 raw sources

- `E:\Projects\WorkDataHub\docs\domains\annuity_income.md`
- `E:\Projects\WorkDataHub\docs\domains\annuity_income-capability-map.md`
- `E:\Projects\WorkDataHub\docs\cleansing-rules\annuity-income.md`
- `E:\Projects\WorkDataHub\docs\guides\validation\legacy-parity-validation.md`
- `docs/superpowers/audits/2026-04-12-verification-assets-search-findings.md`
- `docs/superpowers/audits/2026-04-12-legacy-code-audit.md`

## 本轮吸收的 Stable Findings

- `annuity_income` 不能因 current project 尚未实现而从 wiki 中消失
- ID5 fallback retirement 是必须保留的制度记忆
- `annuity_income` 既有 parity validation memory，也有 operator artifact memory
- 该 domain 的差异不只是“尚未实现”，还包括 branch mapping、artifact、identity 与 validation 的特殊遗留

## 本轮更新的目标页

- `domains/annuity-income.md`
- `evidence/annuity-income-gap-evidence.md`
- `evidence/identity-and-lookup-evidence.md`
- `evidence/verification-assets-evidence.md`
- `evidence/operator-and-surface-evidence.md`

## 可复用经验

- 对未实现 domain，最稳的做法不是写 current status，而是保留 institutional memory
- 专题型 evidence page 很适合收纳“横跨 identity / validation / operator / config”的 domain-specific gap
- annuity_income 这类主题应优先保留“不能被忘记的差异”，而不是先追求完整复述 legacy 流程

## 下一轮建议

当前路线图中的六轮首批吸收已完成。

后续如果继续推进，更适合进入：

- 对象级 evidence 拆分
- `annuity_income` branch mapping / ID5 / unknown-name artifact 的进一步细化
- 以及从 open questions 中挑选新的闭环主题

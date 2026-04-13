# Round 05：operator 与 surfaces

> 状态：Completed
> 日期：2026-04-14
> 主题簇：operator-and-surfaces

## 本轮目标

- 强化 `reference_sync`、failed-record export、manual customer-mdm commands 与 queue/persistence 的治理识别
- 防止 non-domain surfaces 再次掉出 wiki 主体视野

## 使用的 raw sources

- `docs/superpowers/audits/2026-04-12-legacy-code-audit.md`
- `docs/superpowers/audits/2026-04-12-verification-assets-search-findings.md`
- `E:\Projects\WorkDataHub\docs\runbooks\annuity_performance.md`
- `E:\Projects\WorkDataHub\src\work_data_hub\cli\__main__.py`
- `E:\Projects\WorkDataHub\src\work_data_hub\cli\etl\hooks.py`

## 本轮吸收的 Stable Findings

- `reference_sync` 是独立 runtime / integration surface，不是普通 helper
- manual `customer-mdm` commands 是独立 operator surface
- failed-record export 是 operator artifact，不只是 debug 输出
- queue / enrichment / refresh 背后的 enterprise persistence breadth 不能长期隐身
- 对 surface 主题，最重要的不是实现细节，而是“入口、职责、目标表面、治理状态”

## 本轮更新的目标页

- `evidence/operator-and-surface-evidence.md`
- `surfaces/reference-sync.md`
- `surfaces/failed-record-export.md`
- `surfaces/customer-mdm-commands.md`
- `surfaces/company-lookup-queue.md`

## 可复用经验

- 与其先讨论是否保留，不如先把 surface 的 existence、职责和目标表面写实
- `operator artifact` 如果不尽早抽出，很容易被误判成“只是旧项目遗留输出”
- 审计文档在 surface 主题上尤其重要，因为很多对象没有更好的 legacy narrative docs

## 下一轮建议

下一轮应优先进入：

- [annuity-income](../../domains/annuity-income.md)
- [身份与补查证据](../../evidence/identity-and-lookup-evidence.md)
- [验证资产证据](../../evidence/verification-assets-evidence.md)

目标是把 `annuity_income` 的 legacy-only 制度记忆、身份差异、验证资产缺口与 operator artifacts 汇成第六轮专题闭环。

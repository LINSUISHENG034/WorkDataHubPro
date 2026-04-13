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

- next

## Round 3：输入现实

目标：

- 强化 real-data sample、sheet 结构、目录策略、fixture 边界与输入现实合同

主入口页：

- `evidence/input-reality-evidence.md`
- `standards/input-reality/input-reality-contracts.md`
- `concepts/plan-type.md`

状态：

- pending

## Round 4：验证资产

目标：

- 强化 golden set、replay baseline、error-case fixture、validation guide 等验证资产治理

主入口页：

- `evidence/verification-assets-evidence.md`
- `standards/verification-method/golden-scenarios.md`
- `standards/verification-method/real-data-validation.md`

状态：

- pending

## Round 5：operator 与 surfaces

目标：

- 补强 reference sync、failed-record export、enterprise persistence、GUI / standalone tool 的治理识别

主入口页：

- `evidence/operator-and-surface-evidence.md`
- `surfaces/reference-sync.md`
- `surfaces/failed-record-export.md`

状态：

- pending

## Round 6：`annuity_income` 专题补强

目标：

- 防止 `annuity_income` 的 legacy-only 资产和未闭合问题继续掉出视野

主入口页：

- `domains/annuity-income.md`
- `evidence/verification-assets-evidence.md`
- `evidence/identity-and-lookup-evidence.md`

状态：

- pending

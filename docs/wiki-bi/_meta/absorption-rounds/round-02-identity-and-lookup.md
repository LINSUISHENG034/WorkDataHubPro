# Round 02：身份与补查

> 状态：Completed
> 日期：2026-04-14
> 主题簇：identity-and-lookup

## 本轮目标

- 强化 `company_id` 的多线索识别语义
- 把 temp-id 从总页中拆成独立 atomic concept
- 强化 `company_lookup_queue` 与 `unknown_names_csv` 的独立 surface 定位
- 把 identity fallback chain 与相关验证场景写实

## 使用的 raw sources

- `E:\Projects\WorkDataHub\docs\business-background\年金计划类型与客户名称业务背景.md`
- `E:\Projects\WorkDataHub\tests\fixtures\golden_dataset\curated\dataset_requirements.md`
- `docs/superpowers/audits/2026-04-12-legacy-code-audit.md`
- `docs/superpowers/audits/2026-04-12-verification-assets-search-findings.md`

## 本轮吸收的 Stable Findings

- `company_id` 识别不应被理解为单字段映射，而是受治理的多线索解析链
- 计划类型会改变身份识别可用线索与解释方式
- 5-step fallback chain 是制度记忆，不只是某次实现细节
- temp-id 是受治理 fallback，不等于正式身份
- `company_lookup_queue` 与 `unknown_names_csv` 都是 identity 主题中的独立 surface / artifact

## 本轮更新的目标页

- `evidence/identity-and-lookup-evidence.md`
- `concepts/company-id.md`
- `concepts/temp-id.md`
- `surfaces/company-lookup-queue.md`
- `surfaces/unknown-names-csv.md`
- `standards/verification-method/golden-scenarios.md`
- `domains/annuity_performance.md`
- `domains/annual_award.md`
- `domains/annual_loss.md`
- `domains/annuity_income.md`

## 可复用经验

- 对 identity 主题，最应该抽象的不是“某个 resolver 类”，而是 fallback chain 与 operator-visible consequences
- temp-id 一旦满足“独立约束 + 高频引用”，就应从 anchor concept 拆成 atomic concept
- queue / artifact 这类 surface 只有在 concept 与 evidence 同步更新时，才不容易再次掉出视野

## 下一轮建议

下一轮应优先进入：

- [输入现实证据](../../evidence/input-reality-evidence.md)
- [输入现实合同](../../standards/input-reality/input-reality-contracts.md)
- [年金计划类型：`plan_type`](../../concepts/plan-type.md)

目标是把 real-data sample、sheet 结构、目录策略、fixture 边界与多 sheet 输入现实吸收成第三个完整闭环。

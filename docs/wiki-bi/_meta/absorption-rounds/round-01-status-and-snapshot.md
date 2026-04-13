# Round 01：状态与快照

> 状态：Completed
> 日期：2026-04-14
> 主题簇：status-and-snapshot

## 本轮目标

- 强化客户状态语义
- 强化 `is_new` 的边界
- 强化 customer MDM 手工命令面的治理识别
- 把状态与快照相关 strong evidence 聚合到主题证据页

## 使用的 raw sources

- `E:\Projects\WorkDataHub\docs\business-background\客户主数据回填与状态来源分析.md`
- `E:\Projects\WorkDataHub\docs\business-background\战客身份定义与更新逻辑.md`
- `E:\Projects\WorkDataHub\config\customer_status_rules.yml`
- `docs/superpowers/audits/2026-04-12-legacy-code-audit.md`

## 本轮吸收的 Stable Findings

- 客户状态与主数据回填是两层语义，不能混同
- `is_winning_this_year`、`is_loss_reported`、`is_churned_this_year` 的事实来源不同
- `is_new` 是客户 / 产品线粒度状态，不存在计划层版本
- `is_new = is_winning_this_year AND NOT BOOL_OR(is_existing)` 是当前稳定语义
- `customer-mdm` 手工命令面是独立 operator surface，不应只当 hook 的附属物

## 本轮更新的目标页

- `evidence/status-and-snapshot-evidence.md`
- `concepts/customer-status.md`
- `concepts/is-new.md`
- `concepts/customer-type.md`
- `concepts/snapshot-granularity.md`
- `standards/semantic-correctness/customer-status-semantics.md`
- `standards/output-correctness/output-correctness.md`
- `surfaces/customer-mdm-commands.md`
- `domains/annuity_performance.md`
- `domains/annual_award.md`
- `domains/annual_loss.md`

## 可复用经验

- 第一轮应先用主题 evidence page 把强证和旁证分开，再回写 concept / standard
- 对状态类主题，最重要的不是实现流程，而是“来源分层 + 粒度边界 + 非例”
- operator surface 在第一轮就应显式挂入主题簇，否则很容易再次掉出知识网络

## 下一轮建议

下一轮应优先进入：

- [身份与补查证据](../..//evidence/identity-and-lookup-evidence.md)
- [企业身份标识：`company_id`](../../concepts/company-id.md)
- [company_lookup_queue](../../surfaces/company-lookup-queue.md)
- [unknown_names_csv](../../surfaces/unknown-names-csv.md)

目标是把 `company_id`、temp-id、lookup runtime、identity fallback chain 这条线吸收成第二个完整闭环。

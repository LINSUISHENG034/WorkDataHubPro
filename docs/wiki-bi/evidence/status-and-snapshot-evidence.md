# 状态与快照证据

## 结论主题

本页聚合客户状态、snapshot granularity、customer MDM、`is_new` 与客户类型边界相关证据。

## 证据记录

| evidence_id | source_type | evidence_strength | coverage_state | supported_pages | last_verified | notes |
|---|---|---|---|---|---|---|
| E-ST-001 | legacy_doc | strong | absorbed | `customer-status`, `is-new`, `customer-type`, `customer-status-semantics` | 2026-04-14 | `E:\Projects\WorkDataHub\docs\business-background\客户主数据回填与状态来源分析.md` 明确区分回填、状态、快照，并给出 `is_new` 语义与粒度边界。 |
| E-ST-002 | legacy_doc | strong | absorbed | `customer-status`, `snapshot-granularity`, `customer-mdm-commands` | 2026-04-14 | `E:\Projects\WorkDataHub\docs\business-background\战客身份定义与更新逻辑.md` 明确 `customer.客户年金计划` 的状态锚点、SCD2 与快照关系。 |
| E-ST-003 | legacy_config | strong | absorbed | `customer-status-semantics`, `output-correctness`, `is-new`, `annual-award`, `annual-loss`, `annuity-performance` | 2026-04-14 | `E:\Projects\WorkDataHub\config\customer_status_rules.yml` 直接定义 `is_winning_this_year`、`is_loss_reported`、`is_churned_this_year`、`is_new` 的来源与表达。 |
| E-ST-004 | legacy_doc | supporting | legacy_only | `real-data-validation`, `output-correctness`, `customer-mdm-commands` | 2026-04-14 | `verification_guide_real_data.md` 提供 snapshot / contract 输出的 operator 验证路径，但尚未被 `wiki-bi` 完全吸收。 |
| E-ST-005 | audit | supporting | absorbed | `customer-mdm-commands`, `snapshot-granularity`, `annuity_performance` | 2026-04-14 | `2026-04-12-legacy-code-audit.md` 识别 manual command surface 与 hook-linked outputs，适合作为 surface 级旁证。 |
| E-ST-006 | audit | supporting | absorbed | `customer-status`, `output-correctness` | 2026-04-14 | `2026-04-12-verification-assets-search-findings.md` 说明状态与 snapshot 相关验证资产仍存在显式缺口。 |
| E-ST-007 | current_test | supporting | explicitly_tracked | `customer-status`, `snapshot-granularity`, `annual-award`, `annual-loss`, `annuity-performance` | 2026-04-15 | `tests/integration/test_projection_outputs.py`、`tests/replay/test_annuity_performance_slice.py`、`tests/replay/test_annual_award_slice.py` 与 `tests/replay/test_annual_loss_slice.py` 说明 current repo 已把 published facts、`contract_state` 与 `monthly_snapshot` 的主链路变成显式受测行为。 |
| E-ST-008 | legacy_code+config | strong | absorbed | `customer-status`, `snapshot-granularity`, `customer-status-semantics`, `customer-mdm-commands` | 2026-04-16 | 新增 [`customer-mdm-lifecycle-evidence`](./customer-mdm-lifecycle-evidence.md)，聚合 `year_init`/`sync`/`snapshot` 生命周期、ratchet-style 含义与 `status_year` 语义边界。 |
| E-ST-009 | current_wiki | supporting | absorbed | `customer-status`, `customer-type`, `customer-status-semantics` | 2026-04-18 | 新增 [`customer-status-annual-identity-evidence`](./customer-status-annual-identity-evidence.md)，把 `is_strategic` / `is_existing` / `contract_status` / `status_year` 收紧成独立 annual identity object page。 |

## 本轮已吸收的稳定结论

- 回填、客户状态、快照是三层语义，不能混成一个对象
- `is_new` 是 derived status，不是客户分类标签
- `is_new` 只存在于客户 / 产品线粒度，不存在计划层版本
- `customer.客户年金计划` 是 strategic / existing / contract_status / status_year 的关键锚点
- annual identity family 现在有了独立对象页，避免继续把 `is_strategic` / `is_existing` / `contract_status` / `status_year` 只留在 aggregate narrative 里
- `customer-mdm` 手工命令面是独立 operator surface，不应被“自动 hook 已覆盖”吞掉
- `is_winning_this_year` 与 `is_loss_reported` 已满足对象级 evidence 拆分阈值
- `is_churned_this_year` 当前仍更适合留在主题页，因为它同时牵涉 product-line / plan 双粒度与 AUM 汇总语义
- current repo 已对 `contract_state -> monthly_snapshot` 形成显式 projection tests 与 replay evidence，但状态家族的对象级 current evidence 仍未完全拆开
- `customer-mdm` 生命周期语义已形成独立证据页：概念页保留公式/语义，命令与运行时细节留在 surface/evidence

## 哪些来源是强证

- 客户状态业务背景文档
- `customer_status_rules.yml`
- `customer-mdm` 相关代码与配置（`year_init`、`contract_sync`、`snapshot_refresh`、`status_year` 注释）

## 哪些来源只是旁证

- audit synthesis
- verification guide 中的操作说明

## 聚合页 dispatcher 边界

- 本页继续承载客户状态总览、快照粒度、customer-mdm surface 与未拆状态对象之间的共享语义。
- 已形成独立对象且被高频单独引用的状态，应优先落到对象级 evidence page，而不是继续把细节堆回 aggregate page。
- domain 入口仍主要通过 [`annual_award`](../domains/annual-award.md)、[`annual_loss`](../domains/annual-loss.md)、[`annuity_performance`](../domains/annuity-performance.md) 接入本页；本页不负责重复这些 domain 的合同级叙述。
- 三层分工固定为：概念页保留公式记忆、生命周期页承载 yearly 语义证据、surface 页承载 command/runtime 细节。

## 对象级补强页

- [`is_new` 对象级证据](./is-new-evidence.md)
- [`is_winning_this_year` 对象级证据](./is-winning-this-year-evidence.md)
- [`is_loss_reported` 对象级证据](./is-loss-reported-evidence.md)
- [customer 年度身份证据](./customer-status-annual-identity-evidence.md)
- [customer_type vs `is_new` 治理证据](./customer-type-is-new-governance-evidence.md)
- [customer MDM 生命周期证据](./customer-mdm-lifecycle-evidence.md)

## 当前证据缺口

- `is_churned_this_year` 仍未拆成对象级 evidence page
- `verification_guide_real_data.md` 的更多 operator query path 仍待后续吸收
- `is_new` 已经满足对象级 evidence 拆分条件，并已作为后续对象级拆分样板落地
- current project 对 `is_new`、`is_winning_this_year`、`is_loss_reported` 的对象级 current evidence 仍主要通过 shared status / projection pages 承接
- `status_year` 在 current runtime 的 authoritative 取值路径仍待决策收口
- `customer_type` 被当作 `is_new` proxy 的 legacy 相邻用法现在已有独立治理页，但最终 disposition 仍待主线程裁决，不可写成已关闭冲突

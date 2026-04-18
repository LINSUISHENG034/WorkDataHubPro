# customer 年度身份证据

## 结论主题

本页固化 customer annual identity family 的证据：`is_strategic`、`is_existing`、`contract_status`、`status_year`，以及它们与 yearly init、status sync、snapshot 和 customer-type proxy 冲突的边界。

## 证据记录

| evidence_id | source_type | evidence_strength | coverage_state | supported_pages | last_verified | notes |
|---|---|---|---|---|---|---|
| E-CAI-001 | legacy_doc | strong | absorbed | `customer-status`, `customer-status-semantics` | 2026-04-18 | `E:\Projects\WorkDataHub\docs\business-background\战客身份定义与更新逻辑.md` 明确 `is_strategic`、`is_existing`、`contract_status`、`status_year` 是围绕 `customer.客户年金计划` 的年度身份家族。 |
| E-CAI-002 | legacy_code | strong | absorbed | `customer-status`, `customer-status-semantics`, `customer-mdm-lifecycle-evidence` | 2026-04-18 | `src/work_data_hub/customer_mdm/contract_sync.py`、`year_init.py`、`strategic.py` 共同承接 yearly init、status sync、strategic ratchet 与年度身份更新语义。 |
| E-CAI-003 | current_wiki | supporting | absorbed | `status-and-snapshot-evidence`, `customer-mdm-lifecycle-evidence`, `customer-type` | 2026-04-18 | 当前 wiki 已确认 lifecycle / command / snapshot 分层，但此前缺少 annual identity family 的单独 durable 入口，本页用于承接这一对象级语义。 |

## 稳定结论

- `is_strategic`、`is_existing`、`contract_status`、`status_year` 组成年度身份家族，而不是四个互不相干的状态字段。
- 这组语义主要锚定在 `customer.客户年金计划`，快照负责分析展示，不负责重写年度身份定义。
- `status_year` 是年度身份锚点，不等于 `snapshot_month`，也不应被降格理解为普通时间标签。
- strategic 身份具有 ratchet-style 语义：允许升级，不应因短期回落自动降级。
- `is_existing` 与 `contract_status` 属于年度身份判断的一部分，应与 `is_new` / `is_winning_this_year` / `is_loss_reported` 等事实承接状态分层理解。

## 非等价 / 易混边界

- `status_year` 不等于 `snapshot_month`：前者锚定年度身份，后者锚定月度快照。
- `customer_type` 不等于 `is_new`：前者是 customer-master-derived label，后者是年度状态派生判断。
- yearly init / sync / snapshot 是不同生命周期动作，不应把动作顺序本身误写成状态定义。
- `customer.客户年金计划` 的年度身份字段不等于快照字段本身；快照消费它们，但不自动成为它们的同义表达。

## 当前证据缺口

- rebuild-side `status_year` authoritative runtime carrier 仍未闭环；当前只能稳定表达 legacy 语义，不能提前宣称 current runtime 已收口。
- legacy 相邻流程中仍存在把 `customer_type` label 当作 `is_new` proxy 的用法；这属于治理冲突背景，不是 durable semantic definition。
- annual identity family 在 current project 中的对象级 current evidence 仍主要通过 shared projection / status pages 承接，尚未完全拆成更细的 current-side object evidence。
- `customer_type vs is_new` 的 proxy-disposition 已邻接本页，但其具体 defer / retire / historical-context 结论应留在独立治理页，不在 annual identity family 页面内混写。

## 相关页面

- [客户状态总览](../concepts/customer-status.md)
- [年金客户类型：`customer_type`](../concepts/customer-type.md)
- [customer_type vs `is_new` 治理证据](./customer-type-is-new-governance-evidence.md)
- [客户状态语义正确性](../standards/semantic-correctness/customer-status-semantics.md)
- [customer MDM 生命周期证据](./customer-mdm-lifecycle-evidence.md)
- [状态与快照证据](./status-and-snapshot-evidence.md)
- [`customer-mdm` 手工命令面](../surfaces/customer-mdm-commands.md)

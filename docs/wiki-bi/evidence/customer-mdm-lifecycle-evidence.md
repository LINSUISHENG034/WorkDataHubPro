# customer MDM 生命周期证据

## 结论主题

本页固化 `customer-mdm` 年度生命周期的证据：`yearly-init`、`sync`、`snapshot`、ratchet-style 含义与 `status_year` 语义边界。

## 证据记录

| evidence_id | source_type | evidence_strength | coverage_state | supported_pages | last_verified | notes |
|---|---|---|---|---|---|---|
| E-CML-001 | legacy_code | strong | absorbed | `customer-status`, `customer-status-semantics`, `customer-mdm-commands` | 2026-04-16 | `src/work_data_hub/customer_mdm/year_init.py` 表明 year init 更新 `is_strategic` / `is_existing`，并与年度切断 (`annual_cutover`) 共属年度生命周期动作。 |
| E-CML-002 | legacy_code | strong | absorbed | `customer-status`, `customer-status-semantics`, `customer-mdm-commands` | 2026-04-16 | `src/work_data_hub/customer_mdm/contract_sync.py` 与 `sql/close_old_records.sql`、`sql/sync_insert.sql` 明确 `contract_status`、`is_existing`、`is_strategic` 的 SCD2 同步与 ratchet-style 只增不减约束。 |
| E-CML-003 | legacy_code | strong | absorbed | `snapshot-granularity`, `customer-status-semantics`, `customer-mdm-commands` | 2026-04-16 | `src/work_data_hub/customer_mdm/snapshot_refresh.py` 明确快照分为客户/产品线与客户/计划两层，且年度状态字段与粒度绑定。 |
| E-CML-004 | legacy_config | strong | absorbed | `customer-status`, `customer-status-semantics`, `status-and-snapshot-evidence` | 2026-04-16 | `config/customer_status_rules.yml` 明确 `is_winning_this_year`、`is_loss_reported`、`is_new` 的 yearly 语义与 `is_churned_this_year` 的 monthly 语义。 |
| E-CML-005 | legacy_config | supporting | absorbed | `customer-status-semantics`, `status-and-snapshot-evidence` | 2026-04-16 | `config/customer_mdm.yaml` 含 `status_year` 配置项，但注释说明 sync 运行时按 period 年份推导，不应把配置值当作唯一运行时事实。 |
| E-CML-006 | legacy_code | supporting | absorbed | `customer-mdm-commands`, `status-and-snapshot-evidence` | 2026-04-16 | `src/work_data_hub/cli/customer_mdm/*` 与 `src/work_data_hub/cli/etl/hooks.py` 表明手工命令面与 post-ETL hooks 并存，属于不同 operator/runtime 入口。 |

## 稳定结论

- `yearly-init`、`sync`、`snapshot` 是不同生命周期动作，不是同一动作的别名。
- ratchet-style 含义当前稳定为：`is_strategic` 允许升级，不应被自动降级覆盖。
- `status_year` 语义是“年度身份锚点”，但具体运行时取值可能来自 period 推导而非单一配置项。
- 年度语义与公式记忆应留在概念/标准；命令触发路径与执行顺序应留在 surface/evidence。

## 语义边界提醒

- 本页不是 CLI 手册，不枚举操作参数与命令行示例。
- 未闭环的 runtime 保留策略应进入缺口，不可写成已确定结论。

## 当前证据缺口

- `status_year` 在 rebuild 中的 authoritative 来源尚未形成 current-side 决策包。
- hooks 自动链路与手工命令链路在 current runtime 的最终保留边界仍待后续裁决。

## 相关页面

- [客户状态总览](../concepts/customer-status.md)
- [快照粒度：`snapshot_granularity`](../concepts/snapshot-granularity.md)
- [客户状态语义正确性](../standards/semantic-correctness/customer-status-semantics.md)
- [状态与快照证据](./status-and-snapshot-evidence.md)
- [`customer-mdm` 手工命令面](../surfaces/customer-mdm-commands.md)

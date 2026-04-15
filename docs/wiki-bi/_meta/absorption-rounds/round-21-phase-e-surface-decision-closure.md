# Round 21：Phase E surface decision closure

> 状态：Planned
> 日期：2026-04-15
> 主题簇：planned / Phase E surfaces / decision closure

## 本轮目标

- 把已登记的 Phase E operator/runtime surfaces 从“明确存在”推进到“明确 retain / replace / retire / defer 边界”
- 优先收口 `reference_sync`、`company_lookup_queue` 与 enterprise persistence 的对象级治理结论
- 将 cross-domain operator artifact parity 与 surface decision 的关系写清，避免继续分散在多页 open question 中

## 启动理由

- [operator 与 surface 证据](./../../evidence/operator-and-surface-evidence.md) 仍保留多个 retain / replace / retire 未决项
- [reference-sync](./../../surfaces/reference-sync.md) 和 [company-lookup-queue](./../../surfaces/company-lookup-queue.md) 已被识别为独立 surface，但当前重构处理状态仍停留在“需后续决策”
- Round 11 已经完成对象识别，下一步收益不在“再发现对象”，而在“关闭边界判断”

## 计划读取的 raw sources

- `E:\Projects\WorkDataHub\config\reference_sync.yml`
- `E:\Projects\WorkDataHub\src\work_data_hub\cli\__main__.py`
- `E:\Projects\WorkDataHub\src\work_data_hub\infrastructure\enrichment\resolver\backflow.py`
- `E:\Projects\WorkDataHub\src\work_data_hub\infrastructure\enrichment\repository\other_ops.py`
- `E:\Projects\WorkDataHub\src\work_data_hub\infrastructure\enrichment\eqc_provider.py`
- `E:\Projects\WorkDataHub\docs\deployment_run_guide.md`
- current repo 中与 operator artifacts、identity runtime、reference publication 相关的 runbook / tests / specs

## 计划更新的目标页

- `docs/wiki-bi/evidence/operator-and-surface-evidence.md`
- `docs/wiki-bi/surfaces/reference-sync.md`
- `docs/wiki-bi/surfaces/company-lookup-queue.md`
- `docs/wiki-bi/surfaces/enterprise-enrichment-persistence.md`
- 必要时更新 `docs/wiki-bi/surfaces/customer-mdm-commands.md`
- 必要时更新 `docs/wiki-bi/surfaces/standalone-tooling.md`

## 完成定义

- 至少 `reference_sync`、`company_lookup_queue`、enterprise persistence 三个对象有显式的 retain / replace / retire / defer 判断边界
- surface 页不再只写“需要后续决策”，而是写清最小必须保留语义与可被替代部分
- `annuity_income` operator artifact parity 与 broader surface decision 的关系被接回主 surface 叙述
- 本轮产出与 Round 19 规则一致：durable pages、`HH:MM` 日志、round note / lint summary 同轮回写

## 后续依赖

- 若 surface closure 触发新的 architecture / implementation work，应将实现动作留在治理边界之外，只把稳定决策写回 wiki

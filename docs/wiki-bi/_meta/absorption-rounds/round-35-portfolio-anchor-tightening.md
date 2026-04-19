# Round 35：portfolio anchor tightening

> 状态：Completed
> 日期：2026-04-19
> 主题簇：classification family / portfolio anchor / object promotion

## 本轮目标

- 把 `组合代码` 从 dispatcher / field-processing 交叉入口层推进成 durable wiki 对象。
- 让 classification family 不再只在“输入类型 vs customer-master 分类”之间打转，而是把 portfolio anchor 这一层也单独说清。
- 收紧 `计划类型`、`管理资格`、backfill、field-processing 与 input/output contracts 对 `组合代码` 的入口。

## 本轮吸收的稳定结论

- `组合代码` 是 portfolio / classification anchor，不是 enterprise identity truth，也不是 customer-master 聚合分类。
- `组合代码` 的 regex 清洗与默认补位不是无意义格式修整，而是为了保护 portfolio anchor contract，使 fact rows 与 `mapping.组合计划` 之间保持可解释关系。
- classification family 现在可更稳定地分成四层：
  - 输入解释锚点：`计划类型`
  - 下游解释锚点：`业务类型`
  - customer-master 聚合分类：`管理资格`、`年金计划类型`
  - portfolio 锚点：`组合代码`
- 经过本轮后，legacy business-semantics queue 中已经没有另一个同等明显、仍停留在 dispatcher-only 的高价值对象。

## 本轮回写页

- [组合代码](../../concepts/portfolio-code.md)
- [classification family 证据](../../evidence/classification-family-evidence.md)
- [年金计划类型：`plan_type`](../../concepts/plan-type.md)
- [管理资格](../../concepts/management-qualification.md)
- [回填：`backfill`](../../concepts/backfill.md)
- [`annuity_performance` 字段处理证据](../../evidence/annuity-performance-field-processing-evidence.md)
- [`annuity_income` 字段处理证据](../../evidence/annuity-income-field-processing-evidence.md)
- [`annuity_performance`](../../domains/annuity-performance.md)
- [`annuity_income`](../../domains/annuity-income.md)
- [`annuity_performance` 输入合同](../../standards/input-reality/annuity-performance-input-contract.md)
- [`annuity_income` 输入合同](../../standards/input-reality/annuity-income-input-contract.md)
- [`annuity_performance` 输出合同](../../standards/output-correctness/annuity-performance-output-contract.md)
- [`annuity_income` 输出合同](../../standards/output-correctness/annuity-income-output-contract.md)

## 有意留在本轮之外的缺口

- `mapping.组合计划` 作为独立 surface / object family 的进一步治理
- manual `customer-mdm` / enterprise persistence closure wave
- semantic-map-first 的 runtime/operator discovery follow-on

其中：

- 本轮把 `组合代码` 收紧为 durable concept page，并不自动意味着 `mapping.组合计划` 也需要立即成为新的 surface page。
- 若后续没有新的 raw-source 证据把 portfolio family 推向更高阈值，下一步更合理的方向应回到 runtime/operator discovery。

## 下一步入口

- [组合代码](../../concepts/portfolio-code.md)
- [classification family 证据](../../evidence/classification-family-evidence.md)
- manual `customer-mdm` / enterprise persistence closure wave

# 组合代码

## 定义

这里的“组合代码”指 fact rows 与 `mapping.组合计划` 之间用于表达 portfolio / classification anchoring 的受治理对象。

它不是 enterprise identity truth，也不是 customer-master 聚合分类，而是把某条业务记录放进哪个组合 / portfolio 语境里解释的稳定锚点。

## 业务意义

如果没有“组合代码”这一层：

- `mapping.组合计划` 会退化成纯技术表，而不是被业务解释的 reference object
- `计划类型`、`业务类型`、`管理资格` 与 `年金计划类型` 很容易被误写成同一层分类对象
- operator 很难回答为什么两条拥有相同 `计划代码` 的记录还可能需要通过不同 portfolio 语境被区分

## 不应被改写的约束

- `组合代码` 不等于 `company_id`
- `组合代码` 不等于输入侧 `计划类型`
- `组合代码` 不等于输入侧 `业务类型`
- `组合代码` 不等于 customer-master 聚合后的 `管理资格` 或 `年金计划类型`
- `组合代码` 的 regex 清洗与默认补位属于保护 portfolio anchor contract 的手段，不应被误写成“只是无害格式修整”

## 输入现实与边界情况

- `annuity_performance` 与 `annuity_income` 都会把 `组合代码` 带进事实层与组合 reference 层
- `组合代码` 可以缺失后再按 `业务类型` / `计划类型` 补默认值，但这不意味着它不重要；恰恰说明该对象需要被治理
- legacy raw sources 反复表明 `组合代码` 与 `计划代码` 共同决定 portfolio-level interpretation，尤其在集合计划语境下更明显
- current accepted wiki 先把它治理为 portfolio/classification anchor，而不是直接提升成独立 surface

## 对输出与下游的影响

- 影响 `mapping.组合计划` 的 reference backfill
- 影响 fact rows 在 portfolio 语境下的稳定解释
- 影响 `计划类型` / `业务类型` / `管理资格` / `年金计划类型` 之间的 classification layering
- 影响 annuity domains 的 composite-key 与 explainability 叙述

## 常见误解 / 非例

- `组合代码` 不等于企业身份键
- `组合代码` 不等于 customer-master 聚合标签
- `组合代码` 不等于“只是字段清洗后的显示值”
- `组合代码` 不应在没有证据时被写成某个 domain 私有实现细节

## 相关概念

- [年金计划类型：`plan_type`](./plan-type.md)
- [管理资格](./management-qualification.md)
- [回填：`backfill`](./backfill.md)

## 相关标准

- [`annuity_performance` 输入合同](../standards/input-reality/annuity-performance-input-contract.md)
- [`annuity_income` 输入合同](../standards/input-reality/annuity-income-input-contract.md)
- [`annuity_performance` 输出合同](../standards/output-correctness/annuity-performance-output-contract.md)
- [`annuity_income` 输出合同](../standards/output-correctness/annuity-income-output-contract.md)

## 相关证据

- [classification family 证据](../evidence/classification-family-evidence.md)
- [`annuity_performance` 字段处理证据](../evidence/annuity-performance-field-processing-evidence.md)
- [`annuity_income` 字段处理证据](../evidence/annuity-income-field-processing-evidence.md)

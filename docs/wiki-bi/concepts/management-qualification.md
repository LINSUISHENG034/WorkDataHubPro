# 管理资格

## 定义

这里的“管理资格”指 customer-master aggregation 上用于表达某个客户在已归一化业务事实中对应了哪些受托 / 投资等管理角色的分类结果。

它不是输入行上单个 `业务类型` 字段的直接别名，而是通过 `concat_distinct` 等聚合规则写入 customer-master 的受治理分类对象。

## 业务意义

如果没有“管理资格”这一层：

- operator 很难解释一个客户在 customer master 上承担了哪些管理角色
- `业务类型`、`年金计划类型` 与 `组合代码` 很容易被误写成同一层分类字段
- customer master 只能回退到原始事实行语境，无法直接回答聚合后的分类结论

## 不应被改写的约束

- `管理资格` 不等于输入侧某一行的 `业务类型`
- `管理资格` 可以包含多个排重后的角色值，不能被简化成单值枚举
- `管理资格` 属于 customer-master 聚合分类，不等于 portfolio anchor `组合代码`
- `管理资格` 不等于 customer-master `年金计划类型`

## 输入现实与边界情况

- 四个 accepted domains 都会通过归一化 facts 把 `业务类型` 聚合成 `管理资格`
- 当同一客户覆盖多个管理角色时，结果会保留为排重拼接值，而不是只留一个 dominant label
- 它经常与 `年金计划类型`、`业务类型`、`组合代码` 一起出现，但四者属于同一 classification family 的不同层
- validation guide 会把多值拼接的 `管理资格` 显式当作需要核验的正式输出

## 对输出与下游的影响

- 影响 `customer.客户明细` 的分类解释
- 影响 operator 对 classification family 的核验路径
- 影响 `业务类型`、`年金计划类型` 与 `组合代码` 之间的边界理解

## 常见误解 / 非例

- `管理资格` 不等于输入列 `业务类型`
- `管理资格` 不等于 `年金计划类型`
- `管理资格` 不等于 `组合代码`
- `管理资格` 不是“实现里顺手拼出来的显示字段”

## 相关概念

- [年金计划类型：`plan_type`](./plan-type.md)
- [回填：`backfill`](./backfill.md)

## 相关标准

- [输出正确性标准](../standards/output-correctness/output-correctness.md)

## 相关证据

- [classification family 证据](../evidence/classification-family-evidence.md)
- [`annuity_performance` 字段处理证据](../evidence/annuity-performance-field-processing-evidence.md)
- [`annuity_income` 字段处理证据](../evidence/annuity-income-field-processing-evidence.md)

# 回填：`backfill`

## 定义

这里的 backfill 指从事实域派生并补齐主数据、参考数据或客户相关信息的过程与语义。

它不是单纯“补列值”，而是：

- 从事实中提炼稳定业务对象
- 补齐缺失主数据
- 为后续快照和治理提供结构化输入

## 业务意义

如果没有回填：

- facts 与 customer / mapping 层会失去连接
- 某些标签、计划、机构、客户对象不会被显式建立
- 后续状态和 operator 判断会缺少支撑对象

## 不应被改写的约束

- 回填解决的是主数据 / 参考数据补齐，不等于状态判断
- 回填语义不能与快照状态、运营判断混同
- 聚合与模板生成机制会改变主数据解释，不能被当作无害实现细节

## 输入现实与边界情况

- 不同 domain 会参与不同的 backfill 路径
- 回填常依赖聚合、模板、append、count 等机制
- temp-id / blank value 的处理会直接影响 backfill 输出

## 对输出与下游的影响

- 影响 `customer.客户明细`
- 影响 `mapping` 相关参考对象
- 影响后续 snapshot、plan-code enrichment、operator 查询

## 常见误解 / 非例

- 回填不等于“复制事实表到主数据表”
- 回填不等于客户状态同步

## 相关概念

- [企业身份标识：`company_id`](./company-id.md)
- [年金客户类型：`customer_type`](./customer-type.md)

## 相关标准

- [输出正确性标准](../standards/output-correctness/output-correctness.md)
- [golden scenarios](../standards/verification-method/golden-scenarios.md)

## 相关证据

- [身份与补查证据](../evidence/identity-and-lookup-evidence.md)
- [operator 与 surface 证据](../evidence/operator-and-surface-evidence.md)
- [`annuity_performance` 输出合同](../standards/output-correctness/annuity-performance-output-contract.md)
- [`annuity_performance` 字段处理证据](../evidence/annuity-performance-field-processing-evidence.md)

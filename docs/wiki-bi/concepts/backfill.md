# 回填：`backfill`

## 定义

这里的 `backfill` 指从已经规范化的业务事实中派生并补齐 reference / master objects 的语义层。

它不是单纯“补列值”，而是：

- 从 canonical facts 中提炼稳定业务对象
- 补齐缺失 reference / customer master
- 把客户级标签、主拓对象、关键计划与关系计数等派生结果写成可治理对象

## 业务意义

如果没有回填：

- facts 与 customer / mapping 层会失去连接
- 某些计划、组合、产品线、机构、客户对象不会被显式建立
- customer-master 层的主拓机构、关键计划、标签、关系计数与分类会失去受治理来源

## 不应被改写的约束

- 回填解决的是主数据 / 参考数据补齐，不等于状态判断
- 回填不等于 authoritative `reference_sync`
- 回填语义不能与快照状态、运营判断混同
- 聚合、模板与标签写入会改变主数据解释，不能被当作无害实现细节

## 输入现实与边界情况

- 回填建立在 processed fact rows 之上，而不是 raw workbook 行
- 不同 domain 会贡献不同 backfill targets 与 weighting column
- `tags`、`主拓机构`、`关键年金计划`、`关联计划数` 这类 customer-master signals 都依赖 aggregation rule，不能当作无来源字段
- temp-id / blank value 的处理会直接影响 backfill 输出

## 对输出与下游的影响

- 影响 `customer.客户明细`
- 影响 `mapping` 相关参考对象
- 为后续 snapshot、plan-code enrichment 与 operator verification 提供上游对象

## 常见误解 / 非例

- 回填不等于“复制事实表到主数据表”
- 回填不等于客户状态同步
- 回填不等于“把 authoritative reference source 同步到业务表”

## domain 级稳定差异

- `annuity_performance` / `annuity_income` 会同时衍生 reference tables 与 customer master
- `annual_award` / `annual_loss` 当前主要把 event facts 衍生为 customer-master signals
- customer-master 的主拓对象选择并不统一；不同 domain 分别使用 `期末资产规模`、`固费`、`计划规模` 作为主导权重
- `tags` 也不是统一常量；不同 domain 分别形成 `yyMM新建`、`yyMM中标`、`yyMM流失`

## 相关概念

- [企业身份标识：`company_id`](./company-id.md)
- [年金客户类型：`customer_type`](./customer-type.md)
- [`tags`](./tags.md)
- [主拓机构](./primary-branch.md)

## 相关标准

- [输出正确性标准](../standards/output-correctness/output-correctness.md)
- [golden scenarios](../standards/verification-method/golden-scenarios.md)

## 相关证据

- [引用同步与回填证据](../evidence/reference-and-backfill-evidence.md)
- [customer-master signals 证据](../evidence/customer-master-signals-evidence.md)
- [身份与补查证据](../evidence/identity-and-lookup-evidence.md)
- [operator 与 surface 证据](../evidence/operator-and-surface-evidence.md)
- [`annuity_performance` 输出合同](../standards/output-correctness/annuity-performance-output-contract.md)
- [`annuity_performance` 字段处理证据](../evidence/annuity-performance-field-processing-evidence.md)

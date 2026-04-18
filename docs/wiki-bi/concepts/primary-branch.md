# 主拓机构

## 定义

这里的“主拓机构”指 customer-master / reference object 上用于表达主导机构归属的受治理对象。

它不是简单复制输入行上的 `机构名称` / `机构代码`，而是从一组事实记录中按稳定权重挑选出的 dominant value。

## 业务意义

如果没有“主拓机构”这一层 customer-master signal：

- customer / plan master 很难表达“哪一个机构在业务上占主导”
- operator 很难解释为什么 `关键年金计划`、`关联计划数` 与机构归属会一起出现
- 不同 domain 对同一客户贡献的主导值会退化成难以比较的原始行文本

## 不应被改写的约束

- 主拓机构不是原始 `机构名称` 字段的别名
- 主拓机构必须和“按什么权重挑选”一起理解
- 不同 domain 的 dominant-value 规则可以不同，不能强行假设只有一条统一来源
- 主拓机构属于 customer-master / reference signal，不是 snapshot status 字段

## 输入现实与边界情况

- `annuity_performance` 以 `期末资产规模` 选择主导机构
- `annuity_income` 以 `固费` 选择主导机构
- `annual_award` / `annual_loss` 以 `计划规模` 形成 event-driven 主导值
- 它经常与 `主拓机构代码`、`关键年金计划`、`关联计划数` 一起出现
- 默认机构码或空值过滤会影响哪些输入能进入 dominant-value 选择

## 对输出与下游的影响

- 影响 `customer.客户明细` 与 `mapping.年金计划` 的 customer-master / reference 解释
- 影响 `关键年金计划` 等 customer-master signals 的可解释性
- 影响 operator 在 real-data validation 中对主导对象的核验路径

## 常见误解 / 非例

- 主拓机构不等于“当前这条事实行上的机构”
- 主拓机构不等于 snapshot 粒度中的机构维度
- 主拓机构不是永久不变的组织所有权声明

## 相关概念

- [回填：`backfill`](./backfill.md)
- [`tags`](./tags.md)

## 相关标准

- [输出正确性标准](../standards/output-correctness/output-correctness.md)
- [`annuity_performance` 输出合同](../standards/output-correctness/annuity-performance-output-contract.md)

## 相关证据

- [customer-master signals 证据](../evidence/customer-master-signals-evidence.md)
- [引用同步与回填证据](../evidence/reference-and-backfill-evidence.md)


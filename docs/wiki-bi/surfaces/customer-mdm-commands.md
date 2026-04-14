# `customer-mdm` 手工命令面

## Surface 定义

这里指 legacy 中独立存在的手工 operator commands，例如：

- `sync`
- `snapshot`
- `init-year`
- `validate`
- `cutover`

## Surface 类型

- operator surface

## Legacy 职责

- 手动触发 contract sync
- 手动刷新快照
- 执行年初初始化与年度 cutover
- 做状态分布验证

## 显式入口

legacy unified CLI 与 deployment guide 都把这组命令当作独立 operator entrypoint 暴露：

- `customer-mdm sync`
- `customer-mdm snapshot --period <YYYYMM>`
- `customer-mdm init-year`
- `customer-mdm validate`
- `customer-mdm cutover`

其中 deployment guide 还明确给出在 `annuity_performance` 成功执行后手工补跑 `sync` 与 `snapshot` 的路径。

## 手工命令分工

- `sync`
  - 重新计算 / 写入 `customer.客户年金计划`
- `snapshot`
  - 重新生成月度快照输出
- `init-year`
  - 承担年度初始化语义
- `cutover`
  - 承担年度切断语义
- `validate`
  - 提供状态分布验证入口

## 为什么它是独立 surface

这些命令不只是实现细节，而是明确暴露给 operator 的操作面。

它们也不应被简单折叠进“ETL hook 自动会做”的说法里，因为：

- 它们可以被手工重跑
- 它们暴露的是独立操作能力
- 它们影响 contract / snapshot / annual lifecycle 的治理边界

## 相关 surfaces

- [standalone tooling](./standalone-tooling.md)

## 相关概念

- [客户状态总览](../concepts/customer-status.md)
- [快照粒度：`snapshot_granularity`](../concepts/snapshot-granularity.md)

## 相关标准

- [客户状态语义正确性](../standards/semantic-correctness/customer-status-semantics.md)
- [real-data validation](../standards/verification-method/real-data-validation.md)

## 关键证据来源

- [状态与快照证据](../evidence/status-and-snapshot-evidence.md)
- [operator 与 surface 证据](../evidence/operator-and-surface-evidence.md)

## 当前重构处理状态

- 当前应被视为需要显式治理的 operator surface
- 具体哪些命令必须保留，仍待后续稳定决策
- 在做 state / snapshot / annual lifecycle 相关判断时，不应假设只有自动 hook 路径存在
- 当前至少应保留“手工 recovery / recompute controls 曾经是正式操作面”的制度记忆

## 仍未决的问题

- 哪些命令要 retain
- 哪些命令要 replace
- 哪些命令可以 retire
- 手工命令与自动 hook 的职责边界在 rebuild 中如何重组

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

## 为什么它是独立 surface

这些命令不只是实现细节，而是明确暴露给 operator 的操作面。

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

## 仍未决的问题

- 哪些命令要 retain
- 哪些命令要 replace
- 哪些命令可以 retire

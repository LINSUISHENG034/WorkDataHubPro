# failed-record 导出

## Surface 定义

failed-record export 指在验证或处理失败时，把失败记录导出为 operator 可消费 artifact 的机制。

## Surface 类型

- artifact surface
- operator surface

## Legacy 职责

- 保留失败记录
- 支持 operator 排查
- 让验证失败不只停留在日志层

## operator / runtime / verification 合同

- operator 合同：失败导出必须给出可消费记录（至少包含失败原因与定位字段），而不是只给汇总错误数。
- runtime 合同：失败导出应被视为 failure-path 的稳定输出面；是否同步写出、落盘路径与命名策略属于显式治理项。
- verification 合同：验证通过不只看“任务失败/成功”，还要检查失败导出 artifact 的可发现性与可追溯性。

## 为什么它是独立 surface

它不是普通 debug 输出，而是失败处理与可观测性的一部分。

如果只保留日志而不保留失败记录导出：

- operator 很难做行级排查
- failure path 的制度记忆会被削弱
- 一些 domain-specific artifact gap 会长期不可见

## 相关概念

- [回填：`backfill`](../concepts/backfill.md)

## 相关标准

- [输出正确性标准](../standards/output-correctness/output-correctness.md)
- [golden scenarios](../standards/verification-method/golden-scenarios.md)

## 关键证据来源

- [验证资产证据](../evidence/verification-assets-evidence.md)
- [operator 与 surface 证据](../evidence/operator-and-surface-evidence.md)
- [unresolved-name and failed-record 证据](../evidence/unresolved-name-and-failed-record-evidence.md)
- [`annuity_income` operator artifacts 证据](../evidence/annuity-income-operator-artifacts-evidence.md)

## 当前重构处理状态

- 当前应视为需要显式判断是否保留的 operator artifact
- legacy breadth 至少覆盖 `annuity_performance`、`annual_award`、`annual_loss` 与 `annuity_income`
- current accepted explicit artifact closure 目前主要来自 `annuity_income`
- 当前至少应继续在 wiki 中维持其制度记忆，不能因未实现而从治理视野中消失

## 当前证据缺口

- rebuild 是否必须保留 domain-agnostic 的 failed-record export contract 仍未闭环
- 若保留，artifact schema（字段、归档策略、保留期）与最小 operator 消费路径仍未成文
- shared breadth 与 remaining parity gap 见 [unresolved-name and failed-record 证据](../evidence/unresolved-name-and-failed-record-evidence.md)
- 本仓库未包含 legacy `infrastructure/validation/*` 原始实现；当前语义依赖已吸收 audit 证据，原始代码级核验仍待补证

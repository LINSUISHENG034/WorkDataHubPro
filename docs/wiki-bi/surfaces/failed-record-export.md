# failed-record export

## Surface 定义

failed-record export 指在验证或处理失败时，把失败记录导出为 operator 可消费 artifact 的机制。

## Surface 类型

- artifact surface
- operator surface

## Legacy 职责

- 保留失败记录
- 支持 operator 排查
- 让验证失败不只停留在日志层

## 为什么它是独立 surface

它不是普通 debug 输出，而是失败处理与可观测性的一部分。

## 相关概念

- [回填：`backfill`](../concepts/backfill.md)

## 相关标准

- [输出正确性标准](../standards/output-correctness/output-correctness.md)
- [golden scenarios](../standards/verification-method/golden-scenarios.md)

## 关键证据来源

- [验证资产证据](../evidence/verification-assets-evidence.md)
- [operator 与 surface 证据](../evidence/operator-and-surface-evidence.md)

## 当前重构处理状态

- 当前应视为需要显式判断是否保留的 operator artifact

## 仍未决的问题

- 是否必须在 rebuild 中保留等价 artifact
- 如果保留，最小交付形态是什么

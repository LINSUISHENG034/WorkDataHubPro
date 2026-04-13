# `unknown_names_csv`

## Surface 定义

`unknown_names_csv` 指 unresolved names 导出 artifact，用于记录仍未被稳定识别的企业名称。

## Surface 类型

- artifact surface
- operator surface

## Legacy 职责

- 导出未识别名称
- 支持人工排查与后续字典/映射补强
- 让 unresolved identity 不只是静默落入临时 fallback

## 为什么它是独立 surface

它不仅是调试文件，更是一种 operator-facing 的反馈路径。

## 相关概念

- [企业身份标识：`company_id`](../concepts/company-id.md)

## 相关标准

- [real-data validation](../standards/verification-method/real-data-validation.md)

## 关键证据来源

- [身份与补查证据](../evidence/identity-and-lookup-evidence.md)
- [operator 与 surface 证据](../evidence/operator-and-surface-evidence.md)

## 当前重构处理状态

- 当前应被视为需要显式治理的 operator artifact

## 仍未决的问题

- rebuild 是否保留该 artifact
- 若保留，是否仍使用 CSV 形态

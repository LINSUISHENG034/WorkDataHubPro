# 临时身份：`temp_id`

## 定义

`temp_id` 是在稳定企业身份无法被正常解析时，由受治理 fallback 机制生成的临时身份标识。

在 legacy 语境中，当前稳定格式是：

- `IN<16-char-Base32>`

## 业务意义

`temp_id` 的作用不是“把未知企业随便塞一个值”，而是：

- 让无法解析的记录仍可被显式追踪
- 避免在身份未决时静默丢失记录
- 避免直接暴露原始业务标识

## 不应被改写的约束

- `temp_id` 是 fallback，不是正式身份
- 它必须是受治理的，而不是随手拼接出来的字符串
- 同一输入在同一规则下应得到稳定结果
- 不应泄露原始业务标识

## 输入现实与边界情况

- 真实输入里会出现无法通过 YAML、DB cache、passthrough、EQC 等路径稳定解析的企业
- 这类记录不能简单当成错误行直接丢弃
- unknown / unresolved 状态应能被 operator 看见

## 对输出与下游的影响

- 影响 `company_id` 的一致性判断
- 影响回填、标签、快照和 compare 的身份解释
- 影响 `unknown_names_csv` 这类 operator artifact 的价值

## 常见误解 / 非例

- `temp_id` 不是“真正的 company_id”
- `temp_id` 不是普通测试桩
- 生成了 `temp_id` 不代表身份问题已经解决

## 相关概念

- [企业身份标识：`company_id`](./company-id.md)
- [回填：`backfill`](./backfill.md)

## 相关标准

- [输出正确性标准](../standards/output-correctness/output-correctness.md)
- [golden scenarios](../standards/verification-method/golden-scenarios.md)

## 相关证据

- [身份与补查证据](../evidence/identity-and-lookup-evidence.md)
- [operator 与 surface 证据](../evidence/operator-and-surface-evidence.md)

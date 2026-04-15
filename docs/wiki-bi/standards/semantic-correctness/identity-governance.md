# 身份治理语义正确性

> standard_type: `semantic-correctness`
> related_standard_types: `output-correctness`, `verification-method`

## 标准对象

本页定义身份治理在语义上怎样才算正确。

它关注的不是某个 resolver 类的细节，而是：

- 身份解析链如何受治理
- temp-id 何时可以出现
- mapping / cache / provider / queue 各自承担什么角色
- 哪些历史决策不能被静默改写

## 适用范围

- `company_id`
- `temp_id`
- YAML / mapping overrides
- DB cache / provider lookup
- async lookup queue
- ID5 retirement 等历史决策

## 正确性定义

语义正确的身份治理至少应满足：

- 不静默丢弃 unresolved 记录
- 不把 temp-id 误当作正式身份
- 不泄露原始业务标识
- 在相同输入与相同规则下保持可解释的一致结果
- 将 intentional retirement 视为显式治理边界，而不是兼容性细节

## 身份治理检查表

判断身份治理是否正确时，至少检查：

1. 当前解析链是否仍保留“先保留记录、后解释差异”的治理原则
2. temp-id 是否满足 deterministic / opaque / governed 三个条件
3. unresolved 情况是否能被 operator 看见，而不是只停在内部日志里
4. mapping files、cache、provider、queue 的职责边界是否清楚
5. 像 ID5 retirement 这类历史决策是否被显式保护，而不是可能被意外恢复

## 关键治理结论

- 身份治理的目标是跨 domain 的稳定解释，而不是单次运行“尽量填上值”
- YAML / mapping overrides、DB cache、provider lookup、temp-id fallback 可以变化实现，但不能失去可解释的边界
- temp-id 是治理后的保留记录手段，不是“解析失败也算成功”的借口
- async queue / operator artifact 是 unresolved identity 的外显治理面，而不是附属噪音
- `annuity_income` 的 branch mapping 与 ID5 retirement 属于 identity governance 的专题决策，而不是孤立 domain 特例

维护时尤其要把下面几层分开：

- compatibility inventory / historical memory
- active runtime path
- retired behavior that must not be reintroduced
- operator-visible consequence

## 非例

- 因为 provider 命中率高，就把 temp-id 规则和 unresolved 可见性删掉
- 因为 current project 简化了实现，就假定 legacy mapping / override memory 可以消失
- 把 ID5 fallback 当作“必要时再开”的临时兼容开关
- 生成了某个 `company_id` 就不再追问它来自 source、cache、provider 还是 temp-id fallback
- 把 current project 里仍可见的 compatibility artifacts 写成 active runtime priority

## 相关概念

- [企业身份标识：`company_id`](../../concepts/company-id.md)
- [临时身份：`temp_id`](../../concepts/temp-id.md)

## 相关证据

- [身份与补查证据](../../evidence/identity-and-lookup-evidence.md)
- [`annuity_income` branch mapping 证据](../../evidence/annuity-income-branch-mapping-evidence.md)
- [`annuity_income` ID5 retirement 证据](../../evidence/annuity-income-id5-retirement-evidence.md)
- [`annuity_income` operator artifacts 证据](../../evidence/annuity-income-operator-artifacts-evidence.md)

## 相关验证方法

- [golden scenarios](../verification-method/golden-scenarios.md)
- [real-data validation](../verification-method/real-data-validation.md)

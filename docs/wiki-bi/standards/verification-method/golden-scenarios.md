# golden scenarios

> standard_type: `verification-method`
> related_standard_types: `input-reality`, `output-correctness`

## 标准对象

本页定义 golden scenario / golden asset 在 `wiki-bi` 中的角色。

## 适用范围

- golden set
- golden baseline
- replay baseline
- error-case fixture
- scenario taxonomy

## 正确性定义

合理的 golden scenario 体系应满足：

- 场景覆盖有明确目的
- 资产类型角色不混用
- 资产与标准对象之间有清晰映射
- 高风险身份问题要有独立 scenario，而不是只埋在 happy path 里

## 关键约束

- golden set 不是普通测试附件
- replay baseline 不等于 real-data sample
- error-case fixture 不应被假装存在
- identity fallback chain 不能只依赖注释或口头记忆
- legacy-only asset 不应因为 current project 尚未吸收就失去制度记忆

## 当前资产角色边界

- `golden set`
  - 高价值、刻意挑选的标准样本集
- `golden baseline`
  - 稳定结果基线
- `replay baseline`
  - accepted slice 的回放参考资产
- `real-data sample`
  - 贴近真实世界输入形态的样本
- `synthetic fixture`
  - 稳定、可控、可快速执行的夹具
- `error-case fixture`
  - 显式保护错误路径的输入样本

这些资产之间不能互相冒充。

## 当前已知治理结论

- 当前 current project 已明确 accepted replay baselines
- `annuity_performance`、[`annual_award`](../../domains/annual-award.md)、[`annual_loss`](../../domains/annual-loss.md) 的 `golden_set` / `golden_baseline` 当前都已在 Phase 2 registry 中被显式标记为 `deferred`
- error-case fixtures 目前更准确的状态是“治理上显式 deferred，且 accepted slices 仍主要以内联 failure cases 保护”
- [`annuity_income`](../../domains/annuity-income.md) 仍保留大量 legacy-only verification assets 和 parity memory
- validation result history 是独立治理对象，不应被 replay baseline 或单次测试结果吞掉

## 身份相关场景

身份与补查主题至少应覆盖：

- YAML override
- DB cache hit
- existing column passthrough
- provider / EQC lookup
- temp-id fallback
- same-input determinism
- unresolved-name artifact visibility

这些场景不只是“实现分支”，而是直接定义身份正确性的验证边界。

对 `annuity_income` 来说，还应额外显式保护：

- post-ID5 行为，而不是把 legacy ID5 fallback 悄悄恢复
- unresolved-name artifact visibility
- failed-record artifact visibility

## 非例

- 用 replay baseline 代替 golden scenario taxonomy
- 用 synthetic fixture 声称覆盖真实输入边界
- 用一个“能跑通的 company_id happy path”代替整条身份解析链的验证
- 因为 current project 还没吸收某项 asset，就假定这项 asset 不再重要

## 相关概念

- [回填：`backfill`](../../concepts/backfill.md)
- [企业身份标识：`company_id`](../../concepts/company-id.md)
- [临时身份：`temp_id`](../../concepts/temp-id.md)

## 相关证据

- [验证资产证据](../../evidence/verification-assets-evidence.md)
- [身份与补查证据](../../evidence/identity-and-lookup-evidence.md)
- [validation result history 证据](../../evidence/validation-result-history-evidence.md)

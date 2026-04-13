# real-data validation

> standard_type: `verification-method`
> related_standard_types: `input-reality`, `output-correctness`

## 标准对象

本页定义什么才算 real-data validation。

## 适用范围

- 使用真实或真实结构数据进行验证的场景
- operator-facing 验证流程
- fact / contract / snapshot 的真实结果核验

## 正确性定义

real-data validation 至少应满足：

- 使用真实数据样本或真实结构样本，而不是只跑 synthetic fixture
- 有明确的验证目标，而不是“跑一下看看”
- 结果可回指到输出标准与证据路径
- operator 能基于结果做进一步核查，而不是只看一句“通过/失败”

## 关键约束

- real-data validation 不等于普通 replay
- 真实样本不能被 synthetic fixture 替代
- 真实运行结果必须可被审阅，而不是只保留口头结论
- 如果验证依赖 SQL / report / evidence package，这些都属于验证资产的一部分

## 当前可接受的资产组合

一次有效的 real-data validation，通常至少需要下面几类资产中的若干项组合：

- real-data sample 或 real-structure sample
- operator verification guide
- replay baseline 或 golden baseline
- evidence package / comparison report
- 明确的验证目标与检查口径

## 非例

- 只用 programmatic workbook fixture 跑一次就宣称完成 real-data validation
- 使用真实文件，但不定义要验证什么
- 只有运行命令，没有结果检查路径

## 相关概念

- [企业身份标识：`company_id`](../../concepts/company-id.md)
- [快照粒度：`snapshot_granularity`](../../concepts/snapshot-granularity.md)

## 相关证据

- [输入现实证据](../../evidence/input-reality-evidence.md)
- [验证资产证据](../../evidence/verification-assets-evidence.md)

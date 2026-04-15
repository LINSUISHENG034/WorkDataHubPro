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

## 当前治理边界

- current project 已把 real-data sample 写成显式 asset kind，但对 accepted slices 仍保持 `deferred`
- 这意味着 real-data sample 目前仍是治理目标，而不是已经存在的 repo-native asset
- accepted slices 当前虽已拥有 replay baseline 与 checkpoint baseline，但这些资产只足以支撑 replay-backed validation，不足以单独构成 full real-data validation
- 如果当前只能用 synthetic fixture 或 replay baseline 支撑验证，必须明确说明它们没有替代 real-data sample
- legacy comparison report、JSON diff 与 validation result corpus 可以作为 adjudication input，但它们本身并不等于 current project 已拥有 governed real-data sample
- 历史 comparison report、JSON diff、parity result 目录属于 validation result history，应作为可复核资产保留

## production-sample writeback 规则

- workbook metadata observed from real production samples may be written back as evidence even when raw files themselves are not repository assets
- when a single month is used only as a representative validation sample, the durable wiki should record the validated production data shape rather than a month-specific raw path
- such writeback must record whether the finding is accepted contract, observed production variant, or adjacent operator reality
- one observed month may strengthen or falsify assumptions, but it does not by itself promote a variant into a universal contract

## 非例

- 只用 programmatic workbook fixture 跑一次就宣称完成 real-data validation
- 使用真实文件，但不定义要验证什么
- 只有运行命令，没有结果检查路径

## 相关概念

- [企业身份标识：`company_id`](../../concepts/company-id.md)
- [快照粒度：`snapshot_granularity`](../../concepts/snapshot-granularity.md)

## 相关证据

- [输入现实证据](../../evidence/input-reality-evidence.md)
- [annuity workbook family 证据](../../evidence/annuity-workbook-family-evidence.md)
- [business collection workbook variants 证据](../../evidence/business-collection-workbook-variants-evidence.md)
- [验证资产证据](../../evidence/verification-assets-evidence.md)
- [validation result history 证据](../../evidence/validation-result-history-evidence.md)

# 计划与证据要同样可执行

> 类型：GSD Lesson
> 日期：2026-04-12
> 场景：Phase 1 计划审查与 parity checkpoint 审核

---

## 抽象经验

### 1. 先收敛决策，再拆执行计划

如果 phase 里存在多个灰区，先把决策锁定到 context 或 memo，再写 `PLAN`。

否则后续计划很容易出现：

- scope 漂移
- 字段定义反复变化
- 审查标准不一致

---

### 2. 设计原则必须落到可验证字段

一个原则如果真的是 phase 核心，就不能只写在说明里。

至少要同时出现在：

- schema
- artifact
- test

否则就是“口头规则”，不是执行规则。

---

### 3. artifact 不等于证据

一个产物文件存在，只说明“格式存在”，不说明“事实成立”。

特别是 parity、checkpoint、baseline 这类 phase：

- 模板文件不是证据
- 占位字段不是证据
- 真实运行结果才是证据

---

### 4. validation 文档必须反映真实状态

验证文档最容易制造“已经覆盖”的错觉。

因此必须保持以下几项一致：

- task 编号
- requirement 映射
- `File Exists` 状态
- Wave 0 缺口

如果这些内容彼此冲突，后续执行者会被误导。

---

### 5. human gate 的质量取决于证据质量

人工 gate 本身没有问题，但前提是证据可审、可追溯、可裁决。

如果 checkpoint 只有：

- 空的 mismatch 表
- 未填写的 decision owner
- `pending-human-review` 模板状态

那就不应该给通过结果。

---

### 6. 先固定最小证据集，再扩完整标准

早期 phase 更适合先固定“最小可用证据集”，不要一开始就定义完整 taxonomy。

但最小证据集也必须先统一 identity 字段，例如：

- `domain`
- `sample_batch_id`
- `baseline_version`
- `comparison_run_id`
- `decision_owner`

否则后续扩展会返工。

---

## 可复用规则

后续 phase 可以直接复用下面 4 条检查：

1. 这个计划依赖的灰区决策，是否已经被锁定？
2. 这个 must-have，是否同时落到了 schema、artifact、test？
3. 这个产物，是真实运行生成的证据，还是只是模板？
4. 这个 gate，是否有足够证据支持 `approved`，否则是否应当是 `changes-requested`？

---

## 总结

对本项目这类“治理 + parity + 重构”型工作，计划文档、验证文档、证据文档不是附属物，而是执行系统本身。

最重要的不是把计划写长，而是保证：

- 决策先收敛
- 规则可验证
- 证据来自真实运行
- gate 只基于可审证据做判断

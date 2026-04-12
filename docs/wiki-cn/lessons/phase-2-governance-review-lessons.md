# Phase 2 审核经验：测试全绿不等于治理闭环

> 类型：GSD Lesson
> 日期：2026-04-13
> 场景：Phase 2 完成后治理审查

---

## 抽象经验

### 1. 有 checkpoint 不等于 checkpoint 真能挡错

一个 checkpoint 被建模出来，只说明 runtime 里有这个名字。

只有当它满足下面两点时，才算真正的 gate：

- 它在和外部 accepted baseline 或显式 contract expectation 比较
- baseline 缺失时，它会 fail 或至少明确降级，而不是静默变绿

否则它只是一个“格式存在”的 checkpoint，不是“行为受保护”的 checkpoint。

---

### 2. baseline asset 不能是可选装饰

这次审查看到的关键问题不是没有测试，而是某些中间 checkpoint 的 baseline 不在仓库里时，runtime 仍然可以通过。

这说明一个治理规则：

- 对 parity-critical checkpoint，baseline asset 必须是强依赖
- “找不到 baseline 时回退到当前输出”不属于容错，属于取消 gate

特别是 `reference_derivation` 这类中间业务语义 checkpoint，如果没有 repo-native baseline，就不应继续宣称 checkpoint 已闭合。

---

### 3. 测试通过说明实现稳定，不自动说明 phase 可签收

`uv run pytest -v` 和当前 `protected_branch` gate 都通过，只能证明：

- 当前测试面没有破
- 当前 runner 和资产组合可以跑通

它们不能自动证明：

- 每个 declared checkpoint 都在做真实 compare
- evidence package 里的每一份差异证据都可信
- phase 的治理目标已经被完全兑现

因此对这类 phase，签收至少要分成两层：

- implementation pass
- governance sign-off

---

### 4. evidence package 的可信度取决于 diff 语义是否准确

comparison-run evidence package 不是普通日志目录，而是控制面证据。

如果 diff 逻辑把重复行差异算多，问题不只是“输出有点粗糙”，而是：

- reviewer 会被夸大的差异规模误导
- adjudication case 会带着失真的事实进入后续决策

所以 evidence writer、diff builder、fingerprint 逻辑本身都应该被当成治理对象，而不是普通辅助函数。

---

### 5. planning、代码、wiki 不一致时，必须显式写出冲突

这次 Phase 2 的典型冲突是：

- planning 文档把 phase 标成完成
- 代码和测试说明实现面基本闭合
- 但治理审查说明签收仍有缺口

遇到这种情况，正确做法不是选一个自己喜欢的说法，而是显式写成：

- 哪些来源说“已完成”
- 代码当前真正支持什么
- 哪些治理缺口仍未闭合

只有这样，后续执行者才不会把“开发做完”误读成“治理已签收”。

---

## 可复用检查清单

后续 phase 或 slice 完成后，可以先跑下面 5 条检查：

1. 每个声明为 gate 的 checkpoint，是否都在和外部 baseline 或显式 contract 做比较？
2. 如果某个 checkpoint 依赖 baseline asset，asset 缺失时是否会明确失败？
3. replay asset contract tests 是否覆盖了所有 phase-critical baseline，而不只是最终 snapshot？
4. evidence package 里的 diff 是否能正确处理重复行、空行和顺序无关比较？
5. 当前“完成”结论，指的是实现完成，还是已经满足治理签收条件？

---

## 总结

对 `WorkDataHubPro` 这类 parity-heavy、governance-heavy 的重构项目，最危险的假象不是测试失败，而是“所有东西都绿了，所以 phase 一定闭合了”。

更稳的判断标准应该是：

- checkpoint 要真实比较
- baseline 要显式存在
- evidence 要可审且不失真
- 签收结论要区分实现完成与治理完成

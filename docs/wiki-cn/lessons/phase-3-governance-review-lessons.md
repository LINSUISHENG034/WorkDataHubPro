# Phase 3 审核经验：failure explainability 必须落到持久化证据与诊断边界

> 类型：GSD Lesson
> 日期：2026-04-13
> 场景：Phase 3 完成审查与 Phase 03.1 remediation 计划审查

---

## 抽象经验

### 1. `run_report` 说对了，不等于持久化裁决证据也说对了

Phase 3 审核里暴露出的核心问题之一是：

- `primary_failure.checkpoint_name` 可以是正确的
- 但 `CompatibilityCase.sample_locator`、`legacy_result`、`pro_result` 仍可能回退到错误的 `monthly_snapshot` 证据

这说明一个治理规则：

- 失败语义不能只在 run-level summary 上正确
- persisted evidence 也必须和同一个 failed checkpoint 保持一致

否则系统只是“对外描述正确”，不是“证据本身真实”。

---

### 2. file-backed diagnose reader 必须把 manifest 当作不可信输入

Phase 03.1 的审查把另一个容易被忽略的点暴露出来：

- 只要 diagnose 入口会读 `manifest.package_paths`
- 它就不能默认相信这些路径一定安全

更稳的规则是：

- absolute path 默认拒绝
- escaping relative path 默认拒绝
- package file 只能解析到当前 comparison-run package 或其受治理 evidence root 内部

对这类系统来说，manifest 不是“配置便利层”，而是证据索引的一部分。索引如果不 fail-closed，诊断结果本身就不再可信。

---

### 3. agent-facing CLI contract 必须覆盖“非法输入”，不能只覆盖“缺少资源”

之前的 `replay diagnose` 已经能对 missing run 给出 typed error，但对 path-like invalid id 仍会掉成 traceback。

这类问题的抽象经验是：

- CLI 稳定性不只看 happy path
- 也不只看 missing resource path
- invalid input path 也必须属于正式 contract

对 agent surface，下面三类结果都应该是有意设计的：

- valid run：返回稳定 machine-readable output
- missing run：返回 typed missing-run error
- invalid identifier：返回 typed invalid-input error

如果第三类退化成 Python traceback，说明 interface 还没有真正闭合。

---

### 4. implementation complete 与 governance sign-off 必须是两个显式状态

Phase 3 审核和 03.1 计划审查共同说明了一个重复出现的治理问题：

- “功能已做完”
- “phase 可治理签收”

这两件事不能混成一句“已完成”。

更准确的状态模型应该至少区分：

- implementation complete
- governance sign-off pending
- governance sign-off closed

而且这些状态必须同步到：

- `.planning/STATE.md`
- `.planning/ROADMAP.md`
- `.planning/PROJECT.md`
- phase verification
- `docs/wiki-cn/`

否则后续执行者会把“代码能跑”误读成“治理已闭环”。

---

### 5. 状态同步 contract 要绑定语义，不要过度绑定单一句子

Phase 03.1 计划审查里还有一个更细但很有价值的经验：

- 文档同步测试应该守住语义一致
- 不应该强迫所有文件复用一模一样的英文句子

更稳的断言方式通常是：

- 关键概念出现
- 日期或 remediation note 存在
- 旧的错误结论已经消失
- 多个文档对同一状态没有互相矛盾

如果 contract test 绑定到单一措辞，后续哪怕只是正常的中文改写，也可能产生“语义正确但测试失败”的假阳性。

---

## 可复用检查清单

后续只要 phase 涉及 explainability、evidence package、diagnostics surface，都可以先跑下面 5 条检查：

1. `run_report.primary_failure`、`CompatibilityCase.checkpoint_name`、`sample_locator`、`legacy_result`、`pro_result` 是否都指向同一个 failed checkpoint？
2. file-backed evidence reader 是否把 manifest/package path 当作不可信输入并 fail-closed？
3. CLI contract 是否同时覆盖 valid、missing、invalid 三类输入路径？
4. 当前“已完成”结论，指的是 implementation complete，还是 governance sign-off closed？
5. 状态同步测试检查的是语义一致，还是只是强绑某一句固定措辞？

---

## 总结

对 `WorkDataHubPro` 这类 replay-heavy、evidence-heavy 的项目，failure explainability 不是“报错能看懂”就够了。

更完整的标准应该是：

- failed checkpoint 语义在 run report 和 persisted evidence 上同时真实
- diagnose reader 的信任边界是 fail-closed 的
- CLI 对非法输入也保持 typed contract
- implementation status 与 governance sign-off status 显式分层
- 状态同步 contract 守语义，不守表面措辞

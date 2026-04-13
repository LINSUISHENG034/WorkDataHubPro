# `wiki-bi` 设计草案

> 状态：Draft
> 日期：2026-04-13
> 适用目录：`docs/wiki-bi/`
> 本文作用：定义新 wiki 的定位、边界、信息架构、页面类型与增量维护工作流；作为后续继续讨论与实施的基线

---

## 1. 背景与问题

当前 `docs/wiki-cn/` 的主要问题不是“内容错误”，而是知识定位偏了。

它过度贴近以下对象：

- 当前项目的 phase / roadmap / closure 状态
- 当前项目已经做出的部分架构安排
- 当前执行过程中的治理补口与状态同步

这会带来两个直接问题：

1. 一旦 `.planning/` 的执行状态变化，wiki 很容易变旧。
2. 一旦当前架构文档已经足够完整，wiki 就会变成低价值的重复描述。

因此，新 wiki 不应继续承担：

- 执行态计划说明
- phase 进度镜像
- 当前架构文档的中文版或补充版

---

## 2. 新 Wiki 的核心定位

`docs/wiki-bi/` 的核心定位不是：

- 旧项目流程说明书
- 新项目架构文档
- `.planning/` 的稳定中文版

`docs/wiki-bi/` 的核心定位应当是：

**面向重构的业务语义与验收标准知识库**

它优先沉淀以下内容：

- 某条业务判断背后的稳定语义是什么
- 哪些约束不能因为实现方式变化而被改写
- 真实输入数据形态有哪些关键现实与边界情况
- 什么样的输出才算业务上正确
- 上述判断分别由哪些 legacy docs、config、tests、代表性代码支撑

可以把它理解为：

- `problem space`
- `semantic space`
- `acceptance space`
- `evidence space`

而不是 `solution space`。

它还应当是一个：

- persistent artifact
- compounding artifact
- synthesis layer

也就是说：

- 不应每次提问都重新从原始材料零散拼接结论
- 应把已经澄清的语义、标准、证据关系持续写回 wiki
- 应随着新证据进入而修订旧页，而不是让旧结论静态冻结

---

## 3. 新 Wiki 不负责什么

`docs/wiki-bi/` 不负责下列事项：

- 当前阶段状态、phase 完成度、plan 执行顺序
- 当前分支、worktree、命令与交付流程
- 当前架构边界如何落到代码目录
- 旧项目具体 pipeline 先后顺序、hook 触发顺序、实现细节复述
- 一次性 gray-area 讨论稿或审计工作稿

这些内容分别由其他资产负责：

- `.planning/`
  - 当前执行态与推进状态
- `docs/superpowers/specs/`
  - 当前项目的架构设计与重构方案
- `docs/disciplines/`
  - 当前项目的执行规则
- 旧项目代码与文档
  - 作为语义和验收标准的证据来源

---

## 4. 设计原则

新 wiki 应遵守以下原则。

### 4.1 语义优先于流程

正文优先回答“这件事在业务上是什么意思”，而不是“旧系统怎么跑到这个结果”。

### 4.2 标准优先于机制

正文优先沉淀“什么算对”，而不是“当前代码怎么做到”。

### 4.3 证据优先于印象

每条稳定结论都要能回指到：

- legacy 文档
- 配置合同
- 测试与验证资产
- 代表性代码入口

### 4.4 知识对象优先于项目阶段

目录和索引应围绕知识对象组织，而不是围绕 phase、roadmap、closure 组织。

### 4.5 新项目借鉴的是约束，不是旧实现流程

wiki 应帮助 `WorkDataHubPro` 识别：

- 哪些语义必须保留
- 哪些验收标准必须保留
- 哪些输入现实必须被正视

而不是要求新项目复制旧系统机制。

### 4.6 增量维护优先于重头推导

`wiki-bi` 应服务这样一种工作方式：

- 新 source 进入时，增量更新相关页面
- 新问题被澄清时，把可复用结论写回 wiki
- 新证据推翻旧说法时，修订既有页面并标明变化

因此它必须是“持续维护的综合层”，而不是“一次性写好的静态知识目录”。

### 4.7 cross-reference 是一等对象

`llm-wiki` 的价值不只是把页面分好类，而是把页面之间的关系维护出来。

对 `wiki-bi` 来说，至少要显式维护下面几类链接关系：

- concept -> related standards
- concept -> related evidence
- domain -> relevant concepts
- domain -> applicable standards
- standard -> supporting evidence
- evidence -> supported concepts / standards

如果只有分类，没有交叉引用，那么它仍然会退化成“好一点的文件夹”。

---

## 5. 三层模型在本仓库中的落地

`llm-wiki` 提到的三层模型，在本仓库中应明确对应为：

### 5.1 Raw Sources

Raw sources 是不可直接在 wiki 中改写的事实来源。

当前主要包括：

- 旧项目 `E:\Projects\WorkDataHub` 中的稳定文档
- 旧项目配置，如 `customer_status_rules.yml`、`foreign_keys.yml`
- 旧项目验证资产与测试夹具
- 旧项目代表性代码入口
- 当前项目中的 `docs/superpowers/audits/` 审计文档与候选清单
- 当前项目中用于重构对照的 specs、tests、reference assets

这些对象是 source of truth，不应在 wiki 中被“二次创造”为另一份未经标注的事实。

### 5.2 The Wiki

The wiki 是 `docs/wiki-bi/` 下由 LLM 维护的 markdown 知识层。

它负责：

- 抽取稳定语义
- 编译验收标准
- 维护证据索引
- 沉淀跨问题的综合判断

### 5.3 The Schema

The schema 是指导 LLM 如何维护这套 wiki 的规则层。

当前至少包括：

- `docs/wiki-bi/_meta/wiki-design.md`
- `docs/wiki-bi/_meta/llm-wiki.md`
- 项目级 `AGENTS.md` 中与 wiki 维护相关的约束
- `wdhp-governance` 的协作规则

---

## 6. 顶层信息架构

`docs/wiki-bi/` 建议采用如下结构：

```text
docs/wiki-bi/
├── index.md
├── log.md
├── _meta/
├── concepts/
├── domains/
├── surfaces/
├── standards/
└── evidence/
```

其中：

- `concepts/`
  - 主知识轴，沉淀跨域稳定概念与业务判断对象
- `domains/`
  - 阅读入口，串起某个 domain 相关的概念、标准与证据
- `surfaces/`
  - 承载对系统外部可见、需要独立治理判断的 operator/runtime/persistence/artifact/tool surfaces
- `standards/`
  - 沉淀输出标准、验收口径、真实数据校验方式、golden scenario 分类
- `evidence/`
  - 沉淀证据索引页，回指 legacy docs、config、tests、代表性代码
- `_meta/`
  - 定义 wiki 自身的定位、规则、模板与维护方式

这里最重要的约束是：

- `concepts/` 是知识主轴
- `domains/` 不是知识主轴，只是导航入口

---

## 7. 顶层目录说明

### 7.1 根文件

#### `index.md`

`index.md` 是 content-oriented catalog。

它必须：

- 列出当前 wiki 中所有 durable page
- 给每页一行 summary
- 按类别组织，但不遗漏页面
- 在每次 ingest 或新增 durable page 时同步更新

#### `log.md`

`log.md` 是 append-only 的时间线。

它必须记录：

- ingest
- query filing
- lint
- significant refactor
- major contradiction resolution

推荐标题格式：

- `## [2026-04-13] ingest | customer status rules`
- `## [2026-04-13] query | compare is_new vs 年金客户类型`
- `## [2026-04-13] lint | detect orphan concept pages`

`index.md` 解决“现在有什么”，`log.md` 解决“最近发生了什么”。两者不能互相替代。

### 7.2 `concepts/`

这里存放跨域稳定概念。

它们是新 wiki 的主轴，因为真正能长期支撑重构设计的，往往不是某个具体流程，而是这些稳定知识对象。

优先候选包括：

- `company_id`
- 客户状态
- `is_winning_this_year`
- `is_loss_reported`
- `is_churned_this_year`
- `is_new`
- 年金计划类型
- `tags`
- 年金客户类型
- 主拓机构
- 快照粒度
- 回填
- 计划代码补全

这些页面应回答：

- 它是什么
- 业务上为什么存在
- 哪些约束不能被改写
- 哪些输入现实会影响它
- 哪些输出会使用它

#### 颗粒度模型

`concepts/` 采用两层颗粒度模型：

- anchor concept
- atomic concept

##### Anchor Concept

anchor concept 是一级概念页，用来承载一个稳定主题簇。

它适合：

- 提供总览
- 定义共同背景
- 汇总相关子概念
- 作为早期建设阶段的主要入口

典型例子：

- `customer-status`
- `company-id`
- `plan-type`
- `snapshot-granularity`
- `backfill`

##### Atomic Concept

atomic concept 是从 anchor concept 中拆出的独立子概念页。

它适合：

- 语义已经足够独立
- 需要被反复单独引用
- 有独立的约束、边界或标准

典型例子：

- `is-new`
- `is-winning-this-year`
- `is-loss-reported`
- `is-churned-this-year`
- `temp-id`

#### 默认策略

默认策略应是：

- 先建 anchor concept
- 后续再按阈值拆出 atomic concept

也就是说，不建议一开始把所有概念都拆成碎片页。

#### 拆分阈值

一个子概念满足以下任意两条时，建议从 anchor concept 拆成独立 atomic page：

1. 有独立语义，不只是父概念的一个字段
2. 有独立的不应被改写约束
3. 有独立的输入现实或边界情况
4. 有独立的输出判定标准
5. 在多个 domain / surface / standard 中被单独引用
6. 未来很可能有独立 evidence page 或 open question

#### 拆分后的职责

拆分完成后：

- anchor concept 保留总览、共享背景和导航
- atomic concept 负责承载独立细节

不应在拆分后继续把完整细节同时保留在两边，以免产生双重维护

### 7.3 `domains/`

这里不是写 domain 实现文档，而是写 domain 导航页。

每个 domain 页只回答：

- 这个 domain 在业务上处理什么事实
- 它依赖哪些 `concepts`
- 它产出哪些结果
- 它的正确性由哪些 `standards` 判断
- 哪些 `evidence` 是关键证据来源

明确不写：

- pipeline step 顺序
- hook 链
- 实现模块清单
- 旧代码流程复述

### 7.4 `surfaces/`

这里承载那些既不是业务 `domain`，也不是抽象 `concept`，但又必须被独立识别和治理的 system surfaces。

它们通常包括：

- operator surface
- runtime surface
- persistence surface
- artifact surface
- tool / GUI surface

典型对象例如：

- `company_lookup_queue`
- `reference_sync`
- manual `customer-mdm` commands
- failed-record export
- `unknown_names_csv`
- `enterprise.enrichment_requests`
- `enterprise.enrichment_index`
- GUI / standalone tools

`surfaces/` 页面应回答：

- 这个 surface 是什么
- 为什么它是独立 surface，而不是普通 domain / concept
- 它在 legacy 中承担什么职责
- 它关联哪些 `concepts`
- 它受哪些 `standards` 约束
- 它在重构中当前属于 retain / replace / retire / deferred 哪一类对象
- 它有哪些关键证据来源

它明确不应退化成：

- 实现模块清单
- operator 手册全文
- 单纯证据摘录页

### 7.5 `standards/`

这里沉淀“什么算对”的知识。

它包括但不限于：

- 输出标准
- 验收口径
- real-data 校验方式
- golden scenario taxonomy
- parity 判断边界
- 允许和不允许的差异类型

如果 `concepts/` 负责定义“是什么”，那么 `standards/` 负责定义“怎样才算正确”。

#### 分层模型

`standards/` 不应被视为单一平面，而应至少区分以下 4 类标准：

##### 1. `input-reality`

回答：

- 真实输入应如何被理解
- 哪些 source shape、sheet、列、脏值模式必须被视为现实约束
- 哪些 synthetic fixture 不能冒充真实输入

##### 2. `semantic-correctness`

回答：

- 某类业务判断在语义上怎样才算正确
- 哪些规则不能因为实现变化而被改写

##### 3. `output-correctness`

回答：

- 最终输出满足什么条件才算正确
- 哪些字段、粒度、结果关系必须成立

##### 4. `verification-method`

回答：

- 用什么方式验证前面三类标准
- real-data validation、golden scenarios、replay baselines、contract tests 分别负责什么

#### 落地方式

`standards/` 的类型分层应体现在物理目录中，而不只停留在页面内容里。

推荐结构：

```text
docs/wiki-bi/standards/
├── input-reality/
├── semantic-correctness/
├── output-correctness/
└── verification-method/
```

这意味着：

- 标准页应放在其主类型对应的子目录下
- 不采用“所有标准页平铺在一个目录，仅靠元信息分类”的默认方案
- 路径本身应帮助人和 LLM 直接理解该标准页的主归属

#### 类型声明

虽然主类型由目录决定，但每个标准页仍应保留轻量类型声明。

建议至少包含：

- `standard_type`
- `related_standard_types`

规则如下：

- 每个标准页只放在一个主目录下
- 跨类型时不复制页面
- 次级关联通过 `related_standard_types` 声明，而不是通过多份页面副本表达

#### 可选扩展类

`adjudication-and-diff` 可以作为未来的独立标准类，但当前不建议一开始单独拆出。

当前策略应是：

- 先把差异裁决、acceptable difference、precedent、evidence package 等内容放在 `verification-method` 下
- 当该主题足够厚、足够稳定时，再拆成独立标准类

### 7.6 `evidence/`

这里不是材料堆场，而是证据索引层。

它负责把某条知识与其证据来源连接起来，例如：

- 哪份 legacy 文档解释了语义
- 哪份配置定义了判断合同
- 哪个测试或验证资产证明了输出标准
- 哪个代表性代码入口说明当前证据如何落地

原则是：

- 正文页不堆大量实现细节
- 证据页负责回指来源

#### 最小证据元数据模型

`evidence/` 中的每条证据记录，至少应显式包含以下字段：

##### `evidence_id`

- 稳定标识符
- 便于在 `concepts/`、`standards/`、`surfaces/`、`domains/` 中引用

##### `title`

- 证据名称

##### `claim_scope`

- 该证据主要支撑哪一类结论

建议取值：

- `concept`
- `standard`
- `surface`
- `domain`

##### `source_type`

- 证据来源类型

建议取值：

- `legacy_doc`
- `legacy_config`
- `legacy_test`
- `legacy_code`
- `audit`
- `current_spec`
- `current_test`
- `current_reference_asset`

##### `evidence_strength`

- 证据强度

建议取值：

- `strong`
- `supporting`
- `weak`

说明：

- `strong`
  - 能直接支撑某个稳定结论，例如 config contract、verification asset、真实样本、明确代码路径
- `supporting`
  - 提供补充语境或旁证，例如 capability map、runbook、业务背景文档
- `weak`
  - 只能提供线索或阶段性综合，例如 audit summary、一次性调查结果

##### `coverage_state`

- 证据在当前治理与吸收过程中的状态

建议取值：

- `absorbed`
- `explicitly_tracked`
- `implicitly_present`
- `legacy_only`
- `open_question`
- `working_trace`

说明：

- `absorbed`
  - 已被 wiki 主体吸收，外部来源主要保留 provenance 角色
- `explicitly_tracked`
  - 当前项目中已有明确对应物
- `implicitly_present`
  - 当前项目中有影子，但尚未被正式治理或命名
- `legacy_only`
  - 仅存在于 legacy 或外部 raw sources
- `open_question`
  - 当前仍未拍板
- `working_trace`
  - 一次性调查或收集痕迹

##### `supported_pages`

- 该证据当前支撑哪些 wiki 页面

##### `last_verified`

- 最后一次核验日期

##### `superseded_by`

- 如果该证据已被更高质量来源替代，应显式标注替代来源

##### `notes`

- 简短说明该证据的适用边界、局限或特别提醒

这个最小模型的目的不是把 `evidence/` 做成数据库，而是让证据层具备：

- 分类能力
- 强弱区分能力
- 吸收状态可视性
- 页面关联能力
- supersession 可见性

#### 粒度模型

`evidence/` 不建议采用“每条证据一页”，也不建议只做少量巨大的总索引页。

推荐采用：

**主题型 evidence page 为默认，对象级 evidence page 为例外**

##### 1. evidence record

- 最小单位
- 承载元数据
- 可以被多个页面引用

##### 2. 主题型 evidence page

- 默认容器页
- 按稳定证据主题聚合一组 evidence records

早期优先适合的主题例如：

- `input-reality-evidence`
- `status-and-snapshot-evidence`
- `identity-and-lookup-evidence`
- `verification-assets-evidence`
- `operator-and-surface-evidence`
- `annuity-income-gap-evidence`

##### 3. 对象级 evidence page

- 作为例外情况使用
- 只在某个对象形成独立、厚实、可复用的证据簇时才拆出

例如：

- `company-id-evidence`
- `is-new-evidence`
- `reference-sync-evidence`
- `customer-mdm-operator-evidence`

#### 拆分阈值

一个主题型 evidence page 下的某个对象，满足以下任意两条时，可以考虑拆成独立对象级 evidence page：

1. 它支撑多个 `supported_pages`
2. 它长期存在 conflict、supersession 或 `Open Question`
3. 它涉及多类 `source_type`
4. 它会被频繁单独引用
5. 它已经形成稳定的证据簇，而不是零散记录

#### 边界规则

- `concept` 页不等于 `evidence` 页
- `standard` 页不等于 `evidence` 页
- `surface` 页不等于 `evidence` 页

默认关系应是：

- 正文页放精选证据入口
- 完整 evidence records 放在主题型 evidence page
- 只有复杂度超过阈值时，才拆独立对象级 evidence page

### 7.7 `_meta/`

这里定义 wiki 自身。

至少应包含：

- 定位与边界
- 顶层目录说明
- 页面类型模板
- 索引、日志与交叉引用规则
- ingest / query / lint 工作流
- 冲突与 supersession 处理规则
- 哪些内容不应进入 wiki

---

## 8. 页面类型定义

新 wiki 建议只使用 4 种正文页类型。

### 8.1 Concept Page

回答“这个知识对象在业务上是什么”。

### 8.2 Domain Navigation Page

回答“某个 domain 与哪些概念、标准、证据有关”。

### 8.3 Surface Page

回答“某个系统 surface 是什么、为何独立存在、在重构中应如何治理”。

### 8.4 Standard Page

回答“什么算正确，如何判断正确”。

### 8.5 Evidence Index Page

回答“为什么可以相信这条结论，证据在哪里”。

除这 5 种外，不建议继续引入：

- phase summary page
- roadmap page
- current status page
- implementation progress page

---

## 9. 页面模板建议

### 9.1 Concept Page 模板

建议固定包含以下章节：

1. 定义
2. 业务意义
3. 不应被改写的约束
4. 输入现实与边界情况
5. 判断规则或语义边界
6. 对输出或下游判断的影响
7. 常见误解 / 非例
8. 相关标准
9. 相关证据

如果该页属于 anchor concept，还应额外包含：

10. 相关 atomic concepts

### 9.2 Domain Page 模板

建议固定包含以下章节：

1. 该 domain 处理的业务事实
2. 核心概念入口
3. 关键输出结果
4. 适用标准
5. 关键证据来源
6. 明确不在本页描述的内容

### 9.3 Surface Page 模板

建议固定包含以下章节：

1. surface 定义
2. surface 类型
3. legacy 职责
4. 相关概念
5. 相关标准
6. 关键证据来源
7. 当前重构处理状态
8. 仍未决的问题

### 9.4 Standard Page 模板

建议固定包含以下章节：

1. 标准对象
2. 适用范围
3. 正确性定义
4. 验收方式
5. 真实数据校验方式
6. golden / scenario 分类
7. 允许的灰区或待裁决边界
8. 相关概念
9. 相关证据

此外，标准页还应显式标注其所属标准类型：

- `input-reality`
- `semantic-correctness`
- `output-correctness`
- `verification-method`

如果该标准页与其他类型也有稳定关联，还应补充：

- `related_standard_types`

### 9.5 Evidence Page 模板

建议固定包含以下章节：

1. 结论主题
2. 证据类型概览
3. 关键来源列表
4. 证据强度说明
5. 哪些来源只是旁证，哪些来源是强证
6. 当前仍需补强的证据缺口

此外，每条 evidence record 至少应带上：

- `evidence_id`
- `claim_scope`
- `source_type`
- `evidence_strength`
- `coverage_state`
- `supported_pages`
- `last_verified`
- `superseded_by`
- `notes`

### 9.6 页面命名规则

页面命名规则的核心不是美观，而是：

- 路径稳定
- 语义清楚
- 便于交叉引用
- 不与临时阶段状态绑定

#### 文件名与标题分工

应明确区分两种角色：

- 文件名
  - 作为稳定标识符
- 页面标题
  - 作为面向读者的表达

因此推荐：

- 文件名使用稳定英文 slug
- 页面标题使用中文或中英混合标题

#### 文件名格式

所有正文页文件名默认使用：

- 英文
- kebab-case
- `.md`

例如：

- `customer-status.md`
- `company-id.md`
- `is-new.md`
- `reference-sync.md`
- `failed-record-export.md`
- `identity-and-lookup-evidence.md`

#### 默认禁止项

文件名默认不应包含：

- 日期
- phase 编号
- 状态词
- 版本尾巴
- `draft`
- `final`
- `new`
- `old`
- `v2`

例如不应使用：

- `2026-04-14-customer-status.md`
- `phase2-company-id.md`
- `customer-status-v2.md`
- `reference-sync-final.md`

#### 命名对象优先级

命名时，应优先反映知识对象本身，而不是文档类型或当前状态。

推荐顺序：

1. 当前项目与 legacy 中都稳定存在的英文术语
2. config / code / spec 中已稳定的英文术语
3. 项目内已经约定的英文表达

不建议：

- 默认使用中文文件名
- 默认使用拼音 slug
- 在文件名中重复加入 `concept-`、`standard-`、`domain-` 这类类型前缀

例外：

- evidence 页可使用 `-evidence` 后缀，避免与 concept / standard 页撞名

#### Anchor / Atomic 概念页命名

对 `concepts/`：

- anchor concept 与 atomic concept 默认都使用平铺文件名
- 不要求通过子目录表达从属关系

例如：

- `customer-status.md`
- `is-new.md`
- `is-winning-this-year.md`
- `temp-id.md`

不建议默认使用：

- `customer-status/is-new.md`

因为知识关系不应被强制等同于路径从属关系。

#### 重命名规则

文件名一旦建立，应尽量稳定。

仅在下列情况允许重命名：

- 页面边界被重新定义
- 原命名明显错误且已影响理解
- 页面主题已从对象 A 转变为对象 B

一般的标题微调、中文表述优化，不应触发文件名重命名。

---

## 10. 写作规则

### 10.1 先写语义，再写证据，最后才写实现线索

每页的主叙述顺序应当是：

1. 这件事在业务上是什么意思
2. 为什么可以这样认定
3. 如果需要追溯，去哪里看证据

### 10.2 区分三种层次

正文中要刻意区分：

- 业务语义
- legacy 证据
- 对重构的启发

不应把它们混成一个层次来写。

### 10.3 避免流程化语言占主导

例如以下内容只能作为证据或注释，不应成为正文主轴：

- “先跑哪个域，再跑哪个域”
- “某个 hook 在某一步触发”
- “某个 pipeline builder 里有 13 个 step”

除非这件事本身定义了语义或验收标准，否则不要让流程话语主导正文。

### 10.4 避免把 wiki 写成当前架构文档

以下问题应尽量交给架构文档回答，而不是由 wiki 回答：

- `capabilities/`、`platform/`、`governance/` 怎么拆
- 哪个 contract 放在哪个模块
- 哪个 adapter 调哪个 runtime

wiki 只需要说明：

- 哪些约束和标准，未来架构不能违背

---

## 11. 索引、日志与运营规则

### 11.1 根索引规则

根索引 `index.md` 不应按 phase 或 roadmap 展开。

它应同时满足两件事：

1. 作为用户导航入口
2. 作为全量 catalog

推荐采用：

**阅读意图主轴 + 常见问题卡片 + 全量 catalog**

#### 第一层：阅读意图主轴

首页骨架应先按“阅读意图”组织，例如：

- 我想知道一个业务判断到底是什么意思
  - 去 `concepts/`
- 我想知道某个 domain 在业务上处理什么
  - 去 `domains/`
- 我想知道哪些 system surfaces 需要独立治理
  - 去 `surfaces/`
- 我想知道什么才算正确输出
  - 去 `standards/`
- 我想知道为什么能相信这条结论
  - 去 `evidence/`

也就是说，索引主骨架要按“阅读意图”组织，而不是按“项目阶段”组织。

#### 第二层：常见问题卡片

在阅读意图主轴之后，可以增加少量精选的常见问题卡片，作为人类读者的快速入口。

这些问题卡片不应承担完整目录职责，只应作为高价值入口。

首版建议卡片清单：

1. `is_new` 与 `年金客户类型` 的区别
2. `company_id` 在业务上到底是什么
3. 什么算 real-data validation
4. 什么样的输出才算“正确”
5. 哪些 system surfaces 不能被隐含忽略
6. 为什么旧项目不能直接作为新架构模板

#### 第三层：全量 catalog

首页底部仍必须保留全量 catalog。

也就是说：

- `concepts/` 下所有 durable pages
- `domains/` 下所有 durable pages
- `surfaces/` 下所有 durable pages
- `standards/` 下所有 durable pages
- `evidence/` 下所有 durable pages

都应在 `index.md` 中出现，并带一句 summary。

但除了导航之外，它还必须满足：

- 全量列出 durable page
- 每页有一句 summary
- category 内部保持稳定排序
- 新增 durable page 时同轮回写

### 11.2 日志规则

`log.md` 必须是：

- append-only
- chronological
- parseable

每次下面这些动作发生后，都应追加日志：

- ingest 新 source
- 把 query 结果沉淀回 wiki
- lint 检查
- 修订旧结论
- 大规模重构页面结构

### 11.3 Ingest 工作流

当新 source 进入时，建议工作流如下：

1. 读取 source
2. 判断它影响哪些 concept / standard / evidence / domain 页
3. 优先更新已有页，而不是先新建孤页
4. 如有必要，再新增 page
5. 回写 `index.md`
6. 追加 `log.md`

一份 source 可能同时触发：

- 多个 concept 页修订
- 一个 standard 页补强
- 一个 evidence 页新增来源
- 一个 domain 导航页补新链接

### 11.4 Query 工作流

查询时，默认工作流如下：

1. 先读 `index.md`
2. 进入相关 concept / standard / evidence / domain 页
3. 必要时回源到 raw sources
4. 生成回答时显式区分：
   - wiki 已有综合结论
   - 新的临时推断
   - 仍需补强的证据

当 query 产出具有长期价值的综合结果时，不应让它只停留在聊天记录里。

应考虑两种处理方式：

- 更新已有页
- 新增一个 durable synthesis page

然后同步更新 `index.md` 与 `log.md`。

#### Query 回写阈值

query 结果的回写不应采用“写 / 不写”二分法，而应采用三档模型：

##### 1. `no-file`

含义：

- 不写回 durable page
- 视情况只记录 `log.md`，或完全不记录

适用情况：

- 纯一次性问题
- 回答没有新增稳定综合判断
- 只是重述现有 wiki 内容
- 对未来复用价值很低

##### 2. `update-existing`

含义：

- 不新建页面
- 直接更新已有 `concept` / `standard` / `surface` / `domain` / `evidence` 页
- 必要时同步更新 `index.md` 与 `log.md`

适用情况：

- query 产生了新的稳定综合判断
- 且这个判断明显属于某个已有页面
- 写回后会增强已有页的长期价值

这是默认优先策略。

也就是说：

- 能更新已有页，就不要新建页

##### 3. `create-synthesis-page`

含义：

- 新建 durable page
- 然后同步更新 `index.md` 与 `log.md`

适用情况：

- query 产出了新的、可独立复用的综合对象
- 不适合硬塞进已有页
- 后续很可能被反复引用

#### 判断规则

每次 query 后，建议至少问下面四个问题：

1. 这次回答有没有产生新的稳定综合判断？
2. 这个判断以后会不会被再次引用？
3. 它是否明显属于某个已有页面？
4. 如果不写回，未来是否还需要重新分析？

建议使用下面的决策方式：

- 如果没有新增稳定综合判断：`no-file`
- 如果有新增稳定综合判断，且归属已有页明确：`update-existing`
- 如果有新增稳定综合判断，且归属已有页不合适，但可独立复用：`create-synthesis-page`

#### 禁止回写的情形

即使 query 很详细，也不应写回 durable page，如果它属于以下情况：

- 仍然是 `Open Question`
- 主要内容仍然是 speculative reasoning
- 只是对外部 source 的转述，没有形成新综合
- 明显属于临时工作过程推理

这类内容最多进入：

- `log.md`
- `evidence/` 的 open questions 区

不应进入：

- `concepts/`
- `standards/`
- `surfaces/`
- `domains/`

### 11.5 Lint 工作流

lint 至少检查以下事项：

- 页面之间是否存在矛盾结论
- 是否有新证据已经使旧说法过时
- 是否有 orphan pages 没有 inbound links
- 是否有重要概念反复出现却还没有独立页面
- 是否缺失 cross-reference
- 是否存在 evidence gap
- `index.md` 是否遗漏 durable page
- `log.md` 是否缺失重要操作记录

### 11.6 冲突与 supersession 处理

当新证据与旧结论冲突时，不应：

- 静默并存两个相互矛盾的说法
- 把新结论只写进聊天，不修正文档
- 只新建一页而不回修旧页

建议处理顺序：

1. 识别受影响页面
2. 更新主结论页
3. 在 evidence 页记录支撑变化
4. 在需要时保留“旧结论为何被替换”的说明
5. 记录日志

也就是说，`wiki-bi` 应维护“当前综合判断”，而不是任由多个时期的说法无序堆叠。

#### 表达模型

`supersession` 应采用：

**主结论单轨 + 显式替代记录**

这意味着：

- 正文始终只维护当前有效的综合结论
- 被替代的旧说法不继续留在正文主叙述里并列出现
- 但必须通过 note、evidence relation、log entry 显式保留替代关系

#### 页面级规则

对 `concepts/`、`standards/`、`surfaces/`、`domains/` 正文页：

- 主正文只保留当前有效结论
- 历史结论不应与现行结论并列写在正文主段落中
- 如需说明变化，可使用 `Supersession Note` 或 `Recent Revision` 区块

该区块应尽量简短，只说明：

- 哪个旧结论被替代
- 替代原因
- 新证据来源
- 日期

#### 证据级规则

对 `evidence/`：

- evidence record 可通过 `superseded_by` 标记替代关系
- 被替代的来源仍可保留
- 但其角色应降级为 provenance / historical context
- 不应继续被当作 primary support 使用，除非重新核验

#### 日志规则

发生重大 supersession 时，`log.md` 必须追加记录。

典型触发包括：

- 某个 concept 的主结论被改写
- 某个 standard 的判断口径被修订
- 某条长期被引用的 evidence 被更高质量来源替代

#### 不推荐的做法

下面这些做法应明确避免：

- 在正文里长期并列保留“旧结论”和“新结论”
- 静默覆盖旧说法，不留下替代痕迹
- 为每次修订都新建独立页面，导致 wiki 碎片化

### 11.7 审计文档集成规则

`docs/superpowers/audits/` 对 `wiki-bi` 来说，默认不是正文页，而是：

- raw source
- synthesis candidate

更准确地说，它们属于：

- bootstrap raw sources

也就是说，审计文档是高价值来源，但不应被整篇搬进 wiki 正文。

#### 四层分类

从 audit 吸收内容时，统一分成以下四层：

##### 1. Stable Finding

定义：

- 已经足够稳定、可以被写成 wiki 主结论的综合判断

特点：

- 可以改写成长期知识，而不是一次性审计口吻
- 有强证据支撑
- 当前已知证据下不存在直接冲突

可进入位置：

- `concepts/`
- `standards/`
- `evidence/` 中的正式结论段

##### 2. Evidence Record

定义：

- 值得保留，但还不应该上升为 wiki 主结论的证据记录

特点：

- 可能只是说明 legacy 中存在某项机制、资产或 surface
- 可能仍缺少足够综合，暂时不能写成“稳定事实”

可进入位置：

- `evidence/`

##### 3. Open Question

定义：

- 当前明确尚未拍板的问题

特点：

- 可以被记录
- 不能被写成 concept / standard 的正文结论

可进入位置：

- `evidence/` 中的 open questions 区
- 或独立问题页（如果后续形成稳定问题簇）

##### 4. Working Trace

定义：

- 一次性的调查过程、收集痕迹、候选清单、并行采集记录

特点：

- 对追溯审计过程有用
- 对 wiki 主体的长期知识价值有限

可进入位置：

- 保留在 `docs/superpowers/audits/`
- 如有必要，只在 `evidence/` 中挂来源链接

#### 提升 gate

一个 audit 结论只有在满足以下条件时，才允许从 audit 提升进入 `concepts/` 或 `standards/`：

1. 能被改写成长期知识表达，而不是一次性审计语言
2. 至少有一类强证据直接支撑，例如：
   - config contract
   - code path
   - test / verification asset
   - 或多个独立 legacy 文档相互印证
3. 它不是 open question
4. 它不是纯 working trace

#### 默认处理原则

默认原则如下：

- 审计文档默认不是 wiki 正文
- `Stable Finding` 才能进入 wiki 主结论层
- `Evidence Record` 和 `Open Question` 进入 `evidence/`
- `Working Trace` 留在 audits

此外还应增加一条硬约束：

- 外部审计文档和当前设计文档都只是 bootstrap raw sources
- `wiki-bi` 一旦完成吸收与整合，后续回答核心问题时应优先依赖 wiki 内部页面
- 外部审计文档的长期角色应退化为 provenance 和 unresolved context
- 不应让 `wiki-bi` 长期把 audits 当成主知识入口

这样做的目标是：

- 吸收 audit 的高价值综合结论
- 防止 `wiki-bi` 退化成工作材料仓库
- 保持 wiki 主体长期可读，而不是混入过多一次性调查痕迹
- 促使稳定结论尽快内化到 wiki，而不是长期悬挂在外部 raw sources 上

---

## 12. 内容准入与排除规则

### 12.1 应进入 `wiki-bi` 的内容

- 稳定业务语义
- 真实输入数据形态与关键边界
- 输出标准与验收口径
- 真实数据验证方式
- golden scenario 分类
- 稳定术语定义
- 稳定重构约束
- 可回溯的证据关系

### 12.2 不应进入 `wiki-bi` 的内容

- 当前 phase 状态
- 当前计划拆分
- 当前实现进度
- 一次性执行记录
- 工作流命令说明
- 纯实现细节
- 纯 legacy 机制复述
- 当前 repo 的目录设计说明

---

## 13. 与其他文档体系的关系

### 13.1 与 `.planning/` 的关系

- `.planning/` 负责“当前做什么”
- `wiki-bi` 负责“为什么这样判断、什么算正确”

### 13.2 与 `docs/superpowers/specs/` 的关系

- `specs/` 负责“新项目准备怎么设计”
- `wiki-bi` 负责“设计时必须尊重哪些语义与标准”

### 13.3 与旧项目代码和文档的关系

- 旧项目是证据来源
- `wiki-bi` 是证据整理与知识抽象层

---

## 14. Source-Of-Truth 优先级模型

`wiki-bi` 不应使用一个全局单一的 source-of-truth 顺序。

原因是：

- 它既不是代码反编译文档
- 也不是单纯的业务背景笔记
- 更不是 audit 摘要集

不同类型的结论，应依赖不同的 primary sources。

因此建议采用：

**按 claim type 分层的优先级模型**

### 14.1 使用规则

处理任意结论时，先执行下面步骤：

1. 先判断当前要写的是哪一类 claim
2. 再查看该类 claim 对应的 primary sources
3. 如果 primary sources 一致，可以形成 `Stable Finding`
4. 如果 primary sources 冲突：
   - 不直接写成 `concepts/` 或 `standards/` 主结论
   - 进入 `evidence/`
   - 必要时标记为 conflict 或 `Open Question`
5. audit synthesis 只能辅助判断，不能直接覆盖 primary sources

### 14.2 Claim Type: 业务语义类

适用问题：

- 某个状态在业务上是什么意思
- 某个概念为什么存在
- 哪些约束不能被实现改写

推荐优先级：

1. 业务背景文档 / 稳定术语文档
2. 明确表达业务语义的 config contract
3. verification guide / golden requirements / capability map 中的语义段
4. 代表性 tests
5. 代表性代码入口
6. audit synthesis

说明：

- 业务语义不应默认被某次实现细节完全定义
- 代码是证据，但不是此类 claim 的唯一最高来源

### 14.3 Claim Type: 验收标准类

适用问题：

- 什么样的输出算正确
- 哪些 scenario 必须覆盖
- 哪些差异可接受、哪些不可接受

推荐优先级：

1. verification asset / golden dataset requirements / replay baseline
2. verification guide / validation 文档
3. config contract
4. tests
5. capability map / domain docs
6. audit synthesis

说明：

- 此类 claim 最接近“标准”本身，因此 verification assets 优先级最高

### 14.4 Claim Type: 输入现实类

适用问题：

- 原始数据真实长什么样
- 哪些异常、脏值、sheet 结构、命名模式是真实存在的

推荐优先级：

1. real-data sample / raw fixture / source workbook
2. data source config
3. verification guide / dataset requirements
4. tests
5. 代表性代码入口
6. audit synthesis

说明：

- 输入现实应尽量由真实样本定义，而不是由实现推测

### 14.5 Claim Type: 机制存在性类

适用问题：

- legacy 中是否真的存在某个 runtime surface / operator surface / write path
- 某个 command、queue、artifact 是否真实存在

推荐优先级：

1. code path / CLI dispatch / config wiring
2. tests / runbooks
3. stable legacy docs
4. audit synthesis

说明：

- 这类 claim 的核心是 existence，因此代码与 dispatch wiring 优先级最高

### 14.6 Claim Type: 当前重构决策类

适用问题：

- 当前新项目已经稳定接受了哪些设计约束
- 哪些重构判断已经是 accepted decision

推荐优先级：

1. committed specs / accepted governance docs / config policies
2. tests + code evidence
3. stabilized planning conclusions that have not yet been absorbed
4. audit / chat / working material

说明：

- `.planning/` 可以作为过渡来源，但不应长期充当最终知识来源

### 14.7 统一冲突规则

如果不同来源发生冲突，应先检查：

- 当前 claim 属于哪一类
- 冲突是否发生在 primary sources 之间

只有当 primary sources 已经足够一致时，结论才可以提升为 wiki 主结论。

如果 primary sources 本身冲突：

- 不应强行选一个写成定论
- 应进入 `evidence/`
- 并记录冲突点、来源、以及当前缺失的补强证据

---

## 15. 首批种子内容建议

实施时，建议优先建设以下页面，而不是先铺满所有 domain。

### `concepts/`

- `company-id.md`
- `customer-status.md`
- `is-new.md`
- `plan-type.md`
- `tags.md`
- `customer-type.md`
- `snapshot-granularity.md`
- `backfill.md`

### `domains/`

- `annuity-performance.md`
- `annual-award.md`
- `annual-loss.md`
- `annuity-income.md`

### `standards/`

- `real-data-validation.md`
- `golden-scenarios.md`
- `output-correctness.md`
- `parity-and-acceptable-difference.md`

### `evidence/`

- `input-reality-evidence.md`
- `identity-and-lookup-evidence.md`
- `status-and-snapshot-evidence.md`
- `verification-assets-evidence.md`
- `operator-and-surface-evidence.md`

第二批候选页：

- `annuity-income-gap-evidence.md`

这些只是实施建议，不代表本草案要求立即全部创建。

---

## 16. 仍需继续讨论的设计点

当前这份设计文档中的核心结构决策与首批实施入口决策已经完成。

如继续推进，后续工作应转向实际搭建 `docs/wiki-bi/`，而不是继续修改顶层 schema。

---

## 17. 当前结论

`docs/wiki-bi/` 的设计方向已经明确：

- 不再以 roadmap / phase / architecture 为主轴
- 以知识对象组织，而不是以执行过程组织
- 以稳定语义、验收标准、真实输入现实和证据关系为核心内容
- 把 `domains/` 降为阅读入口，而不是知识主轴
- 把 `concepts/` 与 `standards/` 提升为最核心的两层
- 把 `index.md` 与 `log.md` 同时视为一级对象
- 把 ingest / query / lint 视为 schema 的正式组成部分

如果这个方向后续得到确认，那么 `wiki-bi` 将成为：

**连接 legacy evidence 与 rebuild design 的知识编译层**

而不是当前项目的状态说明书或架构镜像文档。

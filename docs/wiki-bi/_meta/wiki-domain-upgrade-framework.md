# domain wiki 升级框架

> 状态：Active
> 日期：2026-04-14
> 作用：把某个 domain 从“只能导航”升级到“能直接回答输入-输出-处理问题”的可复用工作流

---

## 1. 适用场景

当出现下面任一信号时，应考虑启动这个框架：

- 用户要求某个 domain 的输入、输出、处理细节，而当前 wiki 只能给高层导航答案
- 某个 domain 的语义已经比较稳定，但 input / output / field-processing 仍未固化为合同级页面
- 某个 domain 的 wiki 与 legacy/current 实现之间开始出现可见 drift，需要 systematize 地比对而不是零散补记

这不是“逢域必做”的默认动作。

只有在下面两个条件都成立时才值得启动：

1. 该 domain 已经足够重要，值得 operator-grade 问答
2. 现有导航页明显不足以支撑问题

---

## 2. 工作流目标

这个框架的目标不是把旧项目实现镜像进 wiki。

目标是把一个 domain 升级成下面三层能力：

1. **输入合同可答**
   - 文件格式、路径、sheet、版本策略、最小字段骨架、无效源条件
2. **输出合同可答**
   - direct fact output、backfill targets、derived downstream outputs
3. **字段处理可答**
   - 哪些处理是工程性质量提升
   - 哪些处理是明确业务语义处理

如果需要，还增加第 4 层：

4. **实现差距可答**
   - wiki 与 legacy/current 代码实现之间的 contract drift、bug candidate、intentional difference

---

## 3. 最小原始材料集

启动时优先读取最小原始材料集，不要一上来扫完整个旧仓库。

对单个 domain，推荐最小集：

- 旧项目 domain contract 文档
- capability / mechanism / field trace map
- domain cleansing rules
- 该 domain runbook
- `config/data_sources.yml`
- `config/foreign_keys.yml`
- 当前 `wiki-bi` 中该 domain 导航页
- 当前 `wiki-bi` 中相关 concept / standard / evidence 页

只有当需要做 code-gap audit 时，再追加：

- domain `pipeline_builder.py`
- domain `service.py`
- domain `models.py` / `schemas.py` / `helpers.py`
- 与该 domain 强相关的 shared helpers、mapping、resolver、backfill service

---

## 4. 推荐产物结构

对一个“值得升级”的 domain，优先采用下面的 durable 产物组合：

### 4.1 domain 导航页

保留薄导航页，回答：

- 这个 domain 处理什么业务事实
- 它接到哪些 concepts / standards / evidence

不要让 domain 页退化成实现 walkthrough。

### 4.2 input contract page

放在：

- `docs/wiki-bi/standards/input-reality/`

回答：

- 文件格式
- 路径
- file pattern
- sheet
- 版本策略
- 最小字段骨架
- 无效源条件

### 4.3 output contract page

放在：

- `docs/wiki-bi/standards/output-correctness/`

回答：

- direct fact sink
- refresh / delete scope
- backfill targets
- derived downstream outputs
- direct/backfill/derived 的边界

### 4.4 field-processing evidence page

放在：

- `docs/wiki-bi/evidence/`

回答：

- 关键字段有哪些
- 每个字段如何处理
- 处理是工程性还是业务性
- 对下游 sink 的影响

### 4.5 implementation-gap evidence page

仅在确有 drift 风险时创建，放在：

- `docs/wiki-bi/evidence/`

回答：

- wiki 说法与实现是否一致
- 哪些差距是 wiki 过窄 / 过宽
- 哪些差距更像代码问题
- 哪些是 intentional difference

---

## 5. 执行顺序

推荐按下面顺序执行：

1. 先评估当前 wiki 是否真有能力缺口
2. 先补 input / output / field-processing 三页
3. 把它们接回 domain / standards / evidence / index
4. 再只用 wiki 回答一次目标问题，验证答案质量是否实质提升
5. 如果还存在 contract-level 不确定性，再进入 code-gap audit
6. 对 gap 做 adjudication
7. 回到机会式维护模式

关键原则：

- **先让 wiki 能答**
- **再去查实现 drift**

不要一开始就先做代码审计，否则很容易把 wiki 重新拉回实现中心。

---

## 6. 分类 gate

从 raw sources 提取内容时，统一分成四类：

- `Stable Finding`
- `Evidence Record`
- `Open Question`
- `Working Trace`

规则不变：

- 只有 `Stable Finding` 才能进入主结论层
- `Evidence Record` 与 `Open Question` 优先进入 `evidence/`
- `Working Trace` 留在 audits / planning / 轮次沉淀中

在 domain 升级工作流里，尤其要注意：

- 字段处理矩阵里的“业务语义”只能写 `Stable Finding`
- 对实现是否有 bug 的判断，初期通常只能是 `Evidence Record` 或 `Open Question`

---

## 7. 何时追加 code-gap audit

不是每个 domain 升级都需要 code-gap audit。

只有在下面任一情况成立时才值得追加：

- 合同页写完后，用户还在问“这和实际代码一致吗”
- legacy 文档之间已经出现明显冲突
- schema、helper、service、config 对同一问题给出不同口径
- 这个 domain 正在成为后续实现/验收的依据，错误成本高

如果不满足这些条件，到 field-processing evidence page 为止通常就够了。

---

## 8. 输出质量检查

完成后至少要问下面几件事：

1. 现在能否只靠 wiki 回答：
   - 输入是什么
   - 输出是什么
   - 处理是什么
2. 新页是否都已进入 `index.md`
3. 是否仍保持：
   - domain 页薄导航
   - standards 页讲合同
   - evidence 页讲证据与处理
4. 有没有因为补充细节而把实现流程伪装成业务真理

---

## 9. 最小复用模板

下次为其他 domain 复用时，最小模板就是：

1. 评估当前 wiki 能不能回答目标问题
2. 读取最小原始材料集
3. 新增：
   - `<domain>-input-contract.md`
   - `<domain>-output-contract.md`
   - `<domain>-field-processing-evidence.md`
4. 更新：
   - domain 导航页
   - generic standard/evidence page
   - `index.md`
   - `log.md`
5. 必要时再新增：
   - `<domain>-implementation-gap-evidence.md`
6. 做一轮吸收沉淀文档

---

## 10. 推荐使用边界

优先适用于：

- `annuity_performance`
- `annual_award`
- `annual_loss`
- `annuity_income`

不推荐直接用于：

- 过于小的原子 concept
- 纯 surface 对象
- 仍主要停留在 exploratory / unresolved 阶段的 domain

---

## 11. 当前样板

当前最完整的样板是：

- [Round 15：`annuity_performance` I/O contracts](./absorption-rounds/round-15-annuity-performance-io-contracts.md)
- [Round 16：`annuity_performance` implementation gap audit](./absorption-rounds/round-16-annuity-performance-gap-audit.md)

它们一起展示了：

- 如何先补合同页
- 如何再做 code-gap audit
- 如何把 gap 再分流到 wiki 修正、代码问题候选与 intentional difference

# Round 15：`annuity_performance` I/O contracts

> 状态：Completed
> 日期：2026-04-14
> 主题簇：follow-on / annuity-performance / I-O contracts

## 本轮目标

- 让 `wiki-bi` 能回答 annuity-performance 的输入、输出与处理三类问题
- 把 annuity-performance 从“导航页能大致说明”推进到“合同级页面能具体回答”
- 不复制旧项目目录结构，只把最稳定的 input / output / field-processing 结论改写成 durable wiki 对象

## 使用的 raw sources

- `E:\Projects\WorkDataHub\docs\domains\annuity_performance.md`
- `E:\Projects\WorkDataHub\docs\domains\annuity_performance-capability-map.md`
- `E:\Projects\WorkDataHub\docs\cleansing-rules\annuity-performance.md`
- `E:\Projects\WorkDataHub\docs\runbooks\annuity_performance.md`
- `E:\Projects\WorkDataHub\config\data_sources.yml`
- `E:\Projects\WorkDataHub\config\foreign_keys.yml`
- 现有 `docs/wiki-bi/` 中与 input reality、output correctness、backfill、customer status 相关页面

## 本轮吸收的 Stable Findings

- `annuity_performance` 的输入现实已经足够稳定，可以写成专门的 input contract page，包括目录、file patterns、sheet、版本策略与最小字段骨架
- `annuity_performance` 的输出不应只被表述为“规模事实输出”，还应显式区分 direct fact sink、backfill targets 与 derived downstream tables
- annuity-performance 的字段处理可以稳定分成两类：工程性数据质量提升，以及基于明确业务语义的数据处理
- 让 domain page 保持薄导航，同时把合同级答案放在 standards/evidence 页，比把所有细节继续堆进 domain page 更符合 `wiki-bi` 设计

## 本轮更新的目标页

- `docs/wiki-bi/standards/input-reality/annuity-performance-input-contract.md`
- `docs/wiki-bi/standards/output-correctness/annuity-performance-output-contract.md`
- `docs/wiki-bi/evidence/annuity-performance-field-processing-evidence.md`
- `docs/wiki-bi/domains/annuity-performance.md`
- `docs/wiki-bi/standards/input-reality/input-reality-contracts.md`
- `docs/wiki-bi/standards/output-correctness/output-correctness.md`
- `docs/wiki-bi/evidence/input-reality-evidence.md`
- `docs/wiki-bi/concepts/backfill.md`
- `docs/wiki-bi/index.md`

## 可复用经验

- 对高价值 domain，单靠导航页通常不足以支撑 operator-grade 问答，必须有 input/output/field-processing 这类合同级页
- 最适合进入 wiki 的不是 pipeline 顺序，而是“哪些输入才算有效、哪些输出才算域的实际产出、哪些处理是工程性、哪些处理是业务性”
- 旧项目的 capability map 和 cleansing rules 特别适合作为 field-processing evidence 的 raw source

## 下一步建议

- 用同样模式继续优化其他高价值 domain，但只在用户真的需要更具体问答能力时再做
- 当前 annuity-performance 已经足以支撑“输入-转化-输出”结构化回答；后续先回到机会式维护模式

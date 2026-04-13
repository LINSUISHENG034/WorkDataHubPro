# Wiki BI Log

## [2026-04-14] scaffold | 初始化 `wiki-bi` 首批可用结构

- 新增 `_meta/wiki-implementation-plan.md`，将设计文档转为首批实施顺序与完成定义
- 新增 `index.md`，采用“阅读意图主轴 + 常见问题卡片 + 全量 catalog”的三层导航
- 新增 `log.md`，作为 append-only 时间线
- 新增首批 `concepts/`、`domains/`、`surfaces/`、`standards/`、`evidence/` seed pages
- 首批内容目标是建立知识骨架与稳定入口，不是一次性吸收全部 legacy 材料

## [2026-04-14] absorb | Round 01 闭环吸收 `status-and-snapshot`

- 新增 `_meta/wiki-absorption-workflow.md` 与 `_meta/wiki-absorption-roadmap.md`，把后续内容吸收机制和整体顺序显式化
- 新增 `_meta/absorption-rounds/index.md` 与 `round-01-status-and-snapshot.md`，把本轮经验与下一轮入口沉淀为可复用资产
- 更新 `evidence/status-and-snapshot-evidence.md`，将状态来源、粒度边界、customer MDM surface 相关 strong/supporting evidence 聚合并区分
- 更新 `concepts/customer-status.md`、`concepts/is-new.md`、`concepts/customer-type.md`、`concepts/snapshot-granularity.md`，把回填/状态/快照分层、`is_new` 公式与粒度边界写实
- 更新 `standards/semantic-correctness/customer-status-semantics.md` 与 `standards/output-correctness/output-correctness.md`，把状态语义检查表与输出约束补齐
- 更新 `surfaces/customer-mdm-commands.md` 与相关 domain 导航页，明确手工命令面和 event fact 对状态判断的支撑关系

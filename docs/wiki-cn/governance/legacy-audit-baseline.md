# 旧项目审计基线

> 类型：治理基线
> 日期：2026-04-12
> 状态：初版
> 适用范围：first-wave legacy coverage、Phase 2 及后续治理

本页把 `docs/superpowers/audits/` 中已经足够稳定的结论沉淀为中文 wiki。目标不是复制审计明细，而是把会影响 coverage matrix、phase planning、review，以及 `accepted / deferred / retired` 决策的事实固定下来。

---

## 开发速记

如果你当前是在推进 phase、开新 slice、做治理评审，先记住下面几条：

- accepted 的三个 slice 只代表 `annuity_performance`、`annual_award`、`annual_loss` 已有验证态 closure，不代表 first-wave 已经整体收口。
- 当前 first-wave 还必须同时盯住 `annuity_income` 的 `AI-001` 到 `AI-005`，以及 cross-cutting 的 `CT-011` 到 `CT-016`。
- `company_lookup_queue`、`reference_sync`、enterprise persistence、manual `customer-mdm` commands、shared operator artifacts 都是显式治理对象，不能被“业务表已覆盖”隐式吞掉。
- 当 wiki、audit、规划文档、legacy 叙述文档冲突时，legacy behavior 看旧项目代码；rebuild current state 看当前 Pro 代码和 accepted governance specs。
- `synthetic fixture` 不是 `real-data sample`；历史 `dataset_requirements.md`、`verification_guide_real_data.md`、`validation_results/` 是制度记忆和 adjudication 参考，不应被当作已经迁移完成。

推荐联读顺序：

- 本页
- `docs/superpowers/specs/2026-04-11-workdatahubpro-first-wave-legacy-coverage-matrix.md`
- `docs/superpowers/specs/2026-04-11-workdatahubpro-refactor-program.md`

---

## 吸收边界

本页吸收：

- 已被旧项目代码、当前 coverage matrix、refactor program 共同支撑的稳定治理结论
- 会影响 first-wave coverage、verification asset governance、operator/runtime closure 的结论

本页不吸收：

- 96 条候选清单
- 逐文件证据路径和一次性 line-level note
- collection metadata 与开放问题列表

这些细节继续保留在 audit 文档中，供需要时回溯。

---

## 冲突处理口径

当下面几类来源出现不一致时：

- `docs/wiki-cn/`
- `docs/superpowers/audits/`
- `.planning/` 或其他规划文档
- 旧项目叙述性文档

应采用下面的判断顺序：

- legacy behavior 以 `E:\Projects\WorkDataHub` 的代码实现为准
- rebuild current state 以 `WorkDataHubPro` 当前代码、accepted coverage matrix、refactor program 为准
- audit 文档负责汇总和解释，不单独覆盖代码事实

2026-04-12 已核对的代表性 legacy 代码入口包括：

- `src/work_data_hub/cli/__main__.py`
- `src/work_data_hub/cli/etl/domain_validation.py`
- `src/work_data_hub/cli/etl/executors.py`

---

## 已确认必须进入治理视野的 legacy surfaces

下表记录 2026-04-12 审计后已确认必须显式治理的 legacy surface。这些对象不是“后面再看”的实现细节，而是 first-wave closure 必须面对的 retained / deferred / retired 决策对象。

| Surface | Coverage Matrix | 治理口径 |
|------|-----------------|----------|
| `company_lookup_queue` special orchestration domain | `CT-011` | 它是独立的 operator/runtime surface，包含异步队列、重试与恢复语义，不能被普通业务域覆盖所隐式吞掉。 |
| `reference_sync` special orchestration domain | `CT-012` | 它不只是 pre-publication bootstrap 语义，还包括 authoritative target sync、schedule 与 sync-state persistence。 |
| enterprise queue/cache persistence (`enrichment_requests`, `enrichment_index`, `company_name_index`) | `CT-013` | 这是 identity runtime footprint，不是可忽略的临时缓存；必须显式决定保留、延期还是退役。 |
| enterprise EQC raw/cleansed persistence (`base_info`, `business_info`, `biz_label`) | `CT-014` | 这是 provider/runtime persistence surface，不应被“当前 replay 不依赖”这种理由默默遗忘。 |
| manual `customer-mdm` operator commands (`sync`, `snapshot`, `init-year`, `validate`, `cutover`) | `CT-015` | 这些命令是独立 operator surface，不能因为当前 projection slice 已 accepted 就被视为自动覆盖。 |
| shared unresolved-name / failed-record artifacts | `CT-016` | `unknown_names_csv` 与 failed-record CSV 是 operator artifact，不是偶发 debug 输出；它们影响排障与运行可操作性。 |

除上表外，审计还确认 legacy 中仍有 standalone `cleanse` CLI 与 GUI surface。它们当前优先级低于 `CT-011` 到 `CT-016`，但在 first-wave retirement review 前仍需显式 retain / defer / retire 决策，不能长期保持隐含状态。

---

## Verification Asset 与 Operator Artifact 结论

2026-04-12 的 verification-asset sweep 带来的稳定结论包括：

- `tests/fixtures/golden_dataset/curated/dataset_requirements.md` 是高价值 legacy-only 治理资产。它记录了大规模场景矩阵、identity fallback 假设与 parity 策略，不应被当作“旧测试附件”遗忘。
- 文档中提到的 error-case fixtures，例如 `threshold_exceeded.xlsx`、`missing_column.xlsx`、`empty_sheet.xlsx`，当前应按 `planned but not created` 处理，不能当成已存在保护。
- `docs/verification_guide_real_data.md` 属于缺失的 operator artifact。它更接近 runbook / real-data verification 指南，而不是当前 replay baseline 的替代物。
- legacy `tests/fixtures/validation_results/` 中的历史 parity 结果应视为 adjudication reference material，而不是当前 accepted replay baseline。
- 当前 Pro 仓库中的简化 workbook 输入仍然只是 `synthetic fixture`，不能替代 `real-data sample` 的角色。
- `annual_award` 与 `annual_loss` 是否需要独立 domain-level `golden set` 仍未闭合，wiki 不应把这件事写成已决。
- legacy company-id mapping catalog 与 `annuity_income` 的 ID5 fallback retirement decision 属于制度记忆。后续若推进 `annuity_income`，必须显式保留这些决策，而不是重新回到“凭印象实现”。

---

## First-Wave 当前治理位置

审计后的当前口径如下：

- `annuity_performance`、`annual_award`、`annual_loss` 的 accepted slice 状态没有被 audit 推翻
- 2026-04-12 audit 主要补齐的是“哪些 surface 还没被显式治理”，不是重写已 accepted slice 的验收结论
- `annuity_income` 仍是唯一未闭合的 first-wave domain；当前 Pro 只有 governance registration，还没有对应的 source implementation、replay baseline 与 replay runbook 落地
- first-wave completion 不能只看已 accepted 的三个 slice，还必须看 `CT-011` 到 `CT-016` 以及 `AI-001` 到 `AI-005` 是否已经进入明确的 `accepted / deferred / retired` 状态

---

## 使用方式

后续在下面几类场景，应先看本页再决定行动：

- 新 phase / 新 slice admission
- legacy coverage review
- runtime/operator surface retain-or-retire 决策
- verification asset 和 operator artifact 的缺口判断

详细证据继续留在以下审计文档中：

- `docs/superpowers/audits/2026-04-12-legacy-code-audit.md`
- `docs/superpowers/audits/2026-04-12-verification-assets-search-findings.md`

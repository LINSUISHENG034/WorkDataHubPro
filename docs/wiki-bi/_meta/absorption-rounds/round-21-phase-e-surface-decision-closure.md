# Round 21：Phase E surface decision closure

> 状态：Completed
> 日期：2026-04-15
> 主题簇：maintenance / Phase E surfaces / decision closure

## 本轮目标

- 把已登记的 Phase E operator/runtime surfaces 从“明确存在”推进到“明确 retain / replace / retire / defer 边界”
- 优先收口 `reference_sync`、`company_lookup_queue` 与 enterprise persistence 的对象级治理结论
- 将 cross-domain operator artifact parity 与 surface decision 的关系写清，避免继续分散在多页 open question 中

## 启动理由

- [operator 与 surface 证据](./../../evidence/operator-and-surface-evidence.md) 仍保留多个 retain / replace / retire 未决项
- [reference-sync](./../../surfaces/reference-sync.md) 和 [company-lookup-queue](./../../surfaces/company-lookup-queue.md) 已被识别为独立 surface，但当前重构处理状态仍停留在“需后续决策”
- Round 11 已经完成对象识别，下一步收益不在“再发现对象”，而在“关闭边界判断”

## 使用的 raw sources

- `E:\Projects\WorkDataHub\config\reference_sync.yml`
- `E:\Projects\WorkDataHub\src\work_data_hub\cli\__main__.py`
- `E:\Projects\WorkDataHub\src\work_data_hub\infrastructure\enrichment\resolver\backflow.py`
- `E:\Projects\WorkDataHub\src\work_data_hub\infrastructure\enrichment\repository\other_ops.py`
- `E:\Projects\WorkDataHub\src\work_data_hub\infrastructure\enrichment\eqc_provider.py`
- `E:\Projects\WorkDataHub\docs\deployment_run_guide.md`
- `docs/superpowers/specs/2026-04-11-workdatahubpro-refactor-program.md`
- `docs/superpowers/specs/2026-04-11-workdatahubpro-first-wave-legacy-coverage-matrix.md`
- `src/work_data_hub_pro/capabilities/identity_resolution/service.py`
- `tests/integration/test_reference_derivation.py`
- `tests/integration/test_publication_service.py`
- `tests/integration/test_annuity_income_operator_artifacts.py`

## 本轮吸收的 Stable Findings

- `reference_sync` 在 legacy 中是厚 runtime surface，但在 current accepted validation slices 中，hidden sync side effects 已经被显式 `reference_derivation -> publication` 链取代
- `company_lookup_queue` 当前没有 repo-native runtime；被 accepted 的是同步 identity chain、temp-id fallback 与 operator-visible unresolved artifacts，而不是 legacy queue orchestration
- enterprise persistence 不能整体打包判断；更合理的 closure 是把 cache、queue persistence、provider raw/cleansed persistence 分开写明 active / deferred 边界
- first-wave validation runtime 当前应明确拒绝把 legacy special orchestration surfaces 误写成“已保留”，但同时保留这些 surface 的治理记忆与 future design requirements
- `annuity_income` 的 operator artifact contract 已是 accepted replacement evidence，但 shared cross-domain artifact parity 仍未闭环，不应在本轮被过度宣称为已完成

## 本轮更新的目标页

- `docs/wiki-bi/evidence/operator-and-surface-evidence.md`
- `docs/wiki-bi/surfaces/reference-sync.md`
- `docs/wiki-bi/surfaces/company-lookup-queue.md`
- `docs/wiki-bi/surfaces/enterprise-enrichment-persistence.md`
- `docs/wiki-bi/index.md`
- `docs/wiki-bi/_meta/absorption-rounds/index.md`
- `docs/wiki-bi/_meta/wiki-absorption-roadmap.md`

## 可复用经验

- surface closure 最容易卡在“必须一次性决定最终 production design”，但更高价值的做法是先把 current accepted runtime 与 future deferred runtime 分层写清
- 对 special orchestration surfaces，最重要的不是一句 retain / replace，而是显式写出：被替代的是什么、被保留的治理记忆是什么、仍 deferred 的 runtime breadth 是什么
- evidence page 先收口成 decision package，再回写 surface 页，比直接逐页补结论更不容易出现判断漂移

## 下一步建议

- 下一轮应转到 Round 22，对高流量 aggregate evidence pages 做模板归一与 lint 友好化
- 若 surface closure 触发新的 architecture / implementation work，应将实现动作留在治理边界之外，只把稳定决策写回 wiki

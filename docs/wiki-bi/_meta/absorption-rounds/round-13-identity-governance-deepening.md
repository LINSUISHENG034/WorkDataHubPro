# Round 13：identity governance deepening

> 状态：Completed
> 日期：2026-04-14
> 主题簇：follow-on / identity governance

## 本轮目标

- 判断 identity governance 是否值得从概念/证据碎片提升为独立标准页
- 收紧 `company_id`、`temp_id`、mapping files、fallback chain 与 queue / cache / provider 边界
- 把 `annuity_income` 的 branch mapping / ID5 retirement 重新接回 broader identity governance，而不是继续作为孤立专题

## 使用的 raw sources

- `docs/wiki-bi/evidence/identity-and-lookup-evidence.md`
- `docs/wiki-bi/concepts/company-id.md`
- `docs/wiki-bi/concepts/temp-id.md`
- `docs/wiki-bi/surfaces/company-lookup-queue.md`
- `docs/wiki-bi/evidence/annuity-income-branch-mapping-evidence.md`
- `docs/wiki-bi/evidence/annuity-income-id5-retirement-evidence.md`
- `E:\Projects\WorkDataHub\tests\fixtures\golden_dataset\curated\dataset_requirements.md`
- `E:\Projects\WorkDataHub\config\mappings\company_id\company_id_overrides_plan.yml`
- `E:\Projects\WorkDataHub\config\mappings\company_id\company_id_overrides_hardcode.yml`
- `E:\Projects\WorkDataHub\config\mappings\company_id\company_id_overrides_name.yml`
- `E:\Projects\WorkDataHub\src\work_data_hub\infrastructure\enrichment\resolver\yaml_strategy.py`
- `E:\Projects\WorkDataHub\src\work_data_hub\infrastructure\enrichment\resolver\db_strategy.py`
- `E:\Projects\WorkDataHub\src\work_data_hub\infrastructure\enrichment\resolver\eqc_strategy.py`
- `tests/integration/test_temp_identity_policy.py`
- `tests/integration/test_identity_resolution.py`
- `src/work_data_hub_pro/capabilities/identity_resolution/service.py`

## 本轮吸收的 Stable Findings

- identity governance 值得独立成标准页，因为它已经同时约束概念定义、fallback 语义、operator visibility 与历史决策保护
- mapping / override family、cache、provider、queue 与 temp-id 应被视为一个治理对象簇，而不是零散实现点
- current project 已显式保护 deterministic / opaque temp identity、source-value-first 行为与 identity evidence refs
- `annuity_income` 的 branch mapping 与 ID5 retirement 更适合作为 identity governance 专题决策，而不是孤立 domain memory

## 本轮更新的目标页

- `docs/wiki-bi/standards/semantic-correctness/identity-governance.md`
- `docs/wiki-bi/evidence/identity-and-lookup-evidence.md`
- `docs/wiki-bi/concepts/company-id.md`
- `docs/wiki-bi/concepts/temp-id.md`
- `docs/wiki-bi/surfaces/company-lookup-queue.md`
- `docs/wiki-bi/evidence/annuity-income-branch-mapping-evidence.md`
- `docs/wiki-bi/evidence/annuity-income-id5-retirement-evidence.md`
- `docs/wiki-bi/index.md`

## 可复用经验

- 当一个主题同时横跨 concept、surface、verification 与 historical decision，通常就已经满足升级为标准页的阈值
- identity governance 的高价值不在“列出多少 resolver step”，而在明确哪些边界可以调整、哪些边界不能静默消失
- current implementation-backed statement 写回 wiki 时，最好优先使用 current tests 和 current service contract，而不是直接把代码细节翻译成业务结论

## 下一轮建议

- 进入 Round 14，只在真正满足阈值时继续做状态家族的对象级 evidence split

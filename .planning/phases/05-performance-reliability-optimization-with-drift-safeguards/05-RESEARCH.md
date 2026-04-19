# Phase 5: Performance Reliability Optimization with Drift Safeguards - Research

**Researched:** 2026-04-19
**Domain:** 两个已确认热点的性能优化、publication policy 的类型化安全失败路径、以及分层性能验证矩阵。
**Confidence:** HIGH

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

### PERF-01 — Hotspot optimization scope and indexing
- **D-01:** 范围严格锁定在 `.planning/codebase/CONCERNS.md` 已确认的两个热点：`src/work_data_hub_pro/capabilities/projections/contract_state.py::_has_match` 与 `src/work_data_hub_pro/platform/tracing/in_memory_trace_store.py::find`。本阶段不扩展到新的 opportunistic profiling 扫描。
- **D-02:** 优化策略固定为预构建索引：`set[(company_id, plan_code, period)]` 用于 projection membership，`dict[(batch_id, anchor_row_no), list[event]]` 用于 trace lookup。明确拒绝 `lru_cache` 和 store-level invalidate API。
- **D-03:** 变更必须 in-place 落在现有函数/方法中；不引入 `IndexedTraceStore`、不加 feature flag、不改 public signature。
- **D-04:** 索引生命周期是 build-once-at-call-site / first-use lazy build；不触碰 write path。

### PERF-01 ↔ Parity — Drift safety
- **D-05:** 语义漂移防线复用现有 `tests/replay/` 全 acceptance suite 与 Phase 02.1 fail-closed baseline 体系；不新建独立 parity harness。
- **D-06:** 每个热点优化必须支持 per-hotspot atomic landing / revert；计划应保持改动边界清晰。
- **D-07:** 如需加 hotspot 级 micro oracle，必须用 `reference/perf-baselines/` 下的预计算 `(input, expected_output)` fixture；不能在源码里保留 `_legacy()` 双实现。
- **D-08:** replay acceptance suite + Phase 02.1 baselines 是最终裁决者；micro oracle 只做辅助诊断，不能推翻 replay 结果。

### PERF-02 — Publication policy validation and failure semantics
- **D-09:** `config/policies/publication.json` 的读取与校验采用 Pydantic v2 model，而不是 JSON Schema 或手写验证函数。
- **D-10:** 错误层次固定为四类：`PolicyFileMissingError`、`PolicyParseError`、`UnknownDomainError`、`UnknownTargetError`，共同继承 `PublicationPolicyError`。
- **D-11:** 结构与解析校验在 `load_publication_policy` fail-fast 完成；`build_publication_plan` 只做 lookup-time target validation。
- **D-12:** `PublicationService.execute` 必须 fail-fast：首个 bundle 写入失败时抛 typed `PublicationExecutionError` 并停止；不能伪造部分成功。`PublicationResult.success` 需要从字面量 `True` 改成真实语义。
- **D-13:** 负路径覆盖必须补到 `tests/integration/test_publication_service.py`，至少覆盖 unknown domain、unknown target、malformed policy、mid-bundle execution failure。

### PERF-03 — Verification matrix and benchmark governance
- **D-14:** workload tier 固定为 `smoke` / `standard` / `large`。
- **D-15:** gate 对应关系固定为 `smoke@PR` / `standard@protected-branch` / `large@nightly`；不能发明新 gate tier。
- **D-16:** baseline 存放在 `reference/perf-baselines/`，使用相对阈值（例如 `<= baseline * 1.20`），最少包含 p50 / p95 wall-clock 与 peak resident memory。
- **D-17:** PERF-03 的 committed surface 必须同时存在：一个 Markdown 矩阵文档（放在 `docs/runbooks/`）和一个可执行 dispatcher（优先 `scripts/run_perf_matrix.py`）。pytest marker 不是主调度机制。

### the agent's Discretion
- `PublicationPolicy` / 错误类的精确落点可以在 `src/work_data_hub_pro/platform/publication/` 或 `src/work_data_hub_pro/platform/contracts/` 邻近位置，只要边界清晰、可导入。
- `reference/perf-baselines/*.json` 的精确文件拆分可按 tier 文件组织，但必须是 committed JSON 资产。
- `run_perf_matrix.py` 放 `scripts/` 还是 CLI 子命令可二选一；结合现有项目结构，优先 `scripts/run_perf_matrix.py` 更符合 D-17。
- “build-once” 可用私有 helper 或惰性缓存属性实现，但不能改变公共接口。

### Deferred Ideas (OUT OF SCOPE)
- 持久化 / 可插拔 storage / tracing / evidence adapter（RUN-01）
- 队列 / retry runtime（RUN-02）
- 新 publication channel（RUN-03）
- operator dashboard（UX-01）
- 对两个已知热点之外的系统性 hot-path profiling
- 真正 transactional 的 rollback 语义
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| PERF-01 | System can improve projection and trace-query hotspots identified in `.planning/codebase/CONCERNS.md` without parity drift | 规划应拆成两个独立热点计划：一个聚焦 `ContractStateProjection._has_match` 的 membership pre-index，另一个聚焦 `InMemoryTraceStore.find` 的 keyed index。两者都要附带 micro-benchmark / fixture-based regression proof，并把 `tests/replay/` 作为最终 drift gate。 |
| PERF-02 | Publication policy handling can fail safely with typed validation errors instead of unstructured key errors | 规划应在 `src/work_data_hub_pro/platform/publication/service.py` 邻近引入 Pydantic policy model 与 typed error hierarchy，修正 `PublicationResult.success` 与 mid-bundle failure 语义，并把负路径测试集中补到 `tests/integration/test_publication_service.py`。 |
| PERF-03 | System can enforce workload-scaled verification (contract/integration/replay/performance) before phase completion | 规划应新增 `docs/runbooks/performance-verification-matrix.md`、`scripts/run_perf_matrix.py`、`reference/perf-baselines/*.json`，并补齐 contract / integration / replay / performance 四层命令映射与 tier baseline 规则。 |
</phase_requirements>

## Summary

Phase 5 不应被规划成“大范围性能清理”或“通用可靠性重构”。代码现状和 `05-CONTEXT.md` 都明确要求它是一组窄边界、可回滚、可复验的外科式变更：两个热点、一个 publication policy 安全层、一个验证矩阵。

代码锚点也支持这种拆分。`ContractStateProjection._has_match` 目前在 `run()` 中对每条 performance row 多次遍历 award/loss fact+fixture rows，形成典型 O(n*m) membership check。`InMemoryTraceStore.find()` 目前每次查询全表线性扫描再排序，现有 benchmark 只验证“小数据集 <0.5s”，并没有把索引化前后行为与多 tier baseline 绑定起来。publication 路径则更直接：`load_publication_policy()` 现在是 `json.loads(...)` + `payload[domain]`，`build_publication_plan()` 是 `policy.targets[target_name]`，`PublicationService.execute()` 在任何异常下都没有结构化 failure contract，且对每个 result 一律写 `success=True`。

最稳妥的规划方式是 4 个 plans、2 个 waves：Wave 1 并行落 3 个代码计划（projection hotspot、trace hotspot、publication policy 安全），Wave 2 收口验证矩阵与 baseline 治理。这样既符合 Phase 5 的最小范围，也能让 PERF-03 建立在前 3 个计划已经产生的真实测试与基线上，而不是先写一份脱离实现的 perf 文档。

**Primary recommendation:** 将 Phase 5 拆成 4 个执行计划：
1. `05-01` — contract-state hotspot 索引化与 projection micro-benchmark；
2. `05-02` — trace-store keyed lookup 索引化与 trace micro-benchmark / fixture proof；
3. `05-03` — publication policy Pydantic model、typed errors、truthful execute failure semantics；
4. `05-04` — workload-tier verification matrix、baseline JSON、dispatcher script、runbook 对齐。

## Project Constraints

- 保持 capability-first 边界：业务语义仍留在 `capabilities/`；索引化只是实现细节优化，不能把 projection 语义搬到 generic helper 或 orchestration。
- 保持 public signatures 不变：`ContractStateProjection.run()`、`ContractStateProjection._has_match(...)` 的调用方式，以及 `InMemoryTraceStore.find(...)` 的对外接口都不能漂移。
- Phase 2 / Phase 02.1 的 replay baselines 与 fail-closed checkpoint truthfulness 是 Phase 5 的上游硬约束；任何 perf 优化不能弱化这些 gate。
- publication policy 安全修复必须沿用 Phase 3 的 typed diagnostic 风格，而不是引入临时 error-code dict 或裸 `ValueError`。
- 验证命令必须遵守 `uv run ...` 工具链 discipline；计划中不应出现 `pip`, `python` 直跑或 ad hoc shell harness。
- 在 claim completion 之前必须仍能跑 `uv run pytest -v`；Phase 5 的 perf 资产是补充，不是替代全量回归。

## Standard Stack

### Core

| Component | Version / State | Purpose | Why Standard |
|-----------|-----------------|---------|--------------|
| `pytest` via `uv run pytest` | current repo standard | 合同、集成、replay、performance 全边界验证 | 已被 `.planning/codebase/TESTING.md` 与 discipline docs 固定 |
| Pydantic v2 dataclasses/models pattern | current repo standard | publication policy 结构化校验 | 与 Phase 2/3/4 已有 typed contracts 风格一致 |
| `InMemoryTableStore` / `InMemoryTraceStore` | current repo runtime | 当前验证态 storage / trace adapter | Phase 5 明确只优化现有 in-memory adapter，不引入新 backend |
| file-backed `reference/` assets | current repo standard | perf baselines / fixtures / governance artifacts | 与 `reference/historical_replays/` 的 committed baseline 模式一致 |

### Supporting

| Component | Purpose | When to Use |
|-----------|---------|-------------|
| `tests/replay/*.py` | 最终 parity / drift gate | 每个 PERF-01 hotspot plan 完成后与 Phase 5 结束前都要跑 |
| `tests/performance/test_trace_lookup_micro_benchmark.py` | 现有 trace performance anchor | 扩展而不是替换；与新的 indexed lookup 结果绑定 |
| `tests/integration/test_publication_service.py` | publication path integration anchor | 承接 PERF-02 的全部负路径覆盖 |
| `docs/runbooks/` | 人可读、agent 可执行的 verification contract surface | 放置 perf verification matrix 文档 |
| `scripts/` | repo-native executable helper surface | 放 `run_perf_matrix.py` dispatcher |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| in-place lazy index on existing classes | new `IndexedTraceStore` / `IndexedProjection` | 违反 D-03，增加 abstraction surface，超出 Phase 5 需要 |
| Pydantic policy model | hand-written `_validate_policy()` | 更轻，但不符合已建立的 typed contract discipline，且容易漂移 |
| replay suite as final arbiter | keep `_legacy()` dual implementations in source | 便于单元对照，但违反 D-07，会让源码长期背负 dual-path 复杂度 |
| `scripts/run_perf_matrix.py` dispatcher | pytest marker-only routing | marker 可辅助，但不满足 D-17 对 single authoritative dispatcher 的要求 |
| relative-threshold baseline JSON | absolute milliseconds threshold | 对机器抖动过敏，容易产生假阳性 perf regression |

## Architecture Patterns

### Pattern 1: Projection Membership Index Built From Existing Row Collections

**What:** 在 `ContractStateProjection.run()` 内，读取现有 fact / fixture rows 后先派生 4 个 lookup set，例如：
- `award_fact_index = {(row["company_id"], row["plan_code"], row["period"]) ...}`
- `award_fixture_index = {...}`
- `loss_fact_index = {...}`
- `loss_fixture_index = {...}`

然后 `_has_match(...)` 从“遍历 list 判断”变成“对预建 set 做 membership lookup”。

**Why:** 当前 `_has_match(...)` 每次调用都遍历整段 rows；而 `run()` 对每个 performance row 至少调用四次，复杂度会随着 fixture/fact 增大迅速恶化。

**Guardrail:** 结果布尔语义必须保持完全一致；`has_award_fixture = has_award_fact or fixture_hit` 与 `has_loss_fixture = has_loss_fact or fixture_hit` 的短路逻辑不能被重写。

### Pattern 2: Trace Store Lazy Secondary Index

**What:** 在 `InMemoryTraceStore` 内保留 `_events: list[FieldTraceEvent]` 作为 source of truth，同时新增私有 lazy index：
- `_events_by_anchor: dict[tuple[str, int], list[FieldTraceEvent]] | None`
- `record()` append 时只让 index 失效或保持未建；`find()` 首次调用时构建 index，后续直接按 `(batch_id, anchor_row_no)` 命中并保证 `event_seq` 有序。

**Why:** 这样既满足 D-03 的 in-place 改造，又不改 public contract；同时把“每次查全表 + sort”压缩成“一次构建，多次命中”。

**Guardrail:** `find()` 的返回顺序仍必须是 `event_seq` 升序；不能因为 index append 顺序假设而失掉排序保证。

### Pattern 3: Load-Time Policy Validation + Execute-Time Typed Failure

**What:** 把 publication 安全层分成两个边界：
1. `load_publication_policy(path, domain=...)` 负责文件存在、JSON parse、domain schema shape、mode enum 解析；
2. `build_publication_plan(...)` 只负责 target lookup；
3. `PublicationService.execute(...)` 在 storage 调用抛错时包装成 typed `PublicationExecutionError(bundle.plan.target_name, bundle.plan.publication_id, ...)` 并停止后续 bundle。

**Why:** 这与 Phase 4 的 boundary validation discipline 一致：尽量把错误在 system boundary 处 loud fail，而不是让中间层掉出 `KeyError`。

**Guardrail:** `PublicationPlan` / `PublicationResult` 数据 shape 必须与现有 contracts 保持兼容；尤其 `transaction_group`, `mode`, `affected_rows` 语义不能变。

### Pattern 4: Tiered Perf Matrix As Committed Governance Surface

**What:** 建立一个 repo-native perf matrix，由三部分组成：
- `docs/runbooks/performance-verification-matrix.md`：人类可读矩阵；
- `scripts/run_perf_matrix.py`：命令调度入口；
- `reference/perf-baselines/{smoke,standard,large}.json`：各 tier baseline 数据。

**Why:** PERF-03 不是单一 benchmark file，而是“什么时候跑、跑什么、用什么阈值、以什么资产为基线”的治理契约。

**Guardrail:** 不应把 baseline 生成和 threshold 判定埋进单个 pytest 用例；脚本和 runbook 必须是显式 surface。

## Recommended Plan Decomposition

### Plan 05-01: Contract-State Membership Index and Projection Benchmark

Purpose:
- 以最小边界解决 `contract_state._has_match` 的 O(n*m) membership hotspot，并为 PERF-01 提供第一个可独立回滚的热点优化。

Key outputs:
- `src/work_data_hub_pro/capabilities/projections/contract_state.py` 中的预构建 membership index
- `tests/performance/test_contract_state_projection_benchmark.py`
- `reference/perf-baselines/contract_state-smoke.json`（如果把 micro baseline 单独拆出）或 tier baseline 中对应 target 指标
- targeted integration / replay proof，确保 projection rows 完全不漂移

### Plan 05-02: Trace Lookup Lazy Index and Trace Benchmark Governance

Purpose:
- 解决 `InMemoryTraceStore.find()` 的全量线性扫描问题，并让现有 trace micro-benchmark 真正与 indexed behavior 绑定。

Key outputs:
- `src/work_data_hub_pro/platform/tracing/in_memory_trace_store.py` 中的 keyed lazy index
- `tests/performance/test_trace_lookup_micro_benchmark.py` 扩展
- `tests/integration/` 或 `tests/contracts/` 中对排序稳定性、missing match、重复 event anchor 的行为验证
- optional fixture-based oracle under `reference/perf-baselines/trace-lookup-fixtures.json`

### Plan 05-03: Publication Policy Validation and Truthful Failure Semantics

Purpose:
- 把 publication path 从 `KeyError` / 恒真 success 语义提升为 typed contract + truthful failure path。

Key outputs:
- Pydantic publication policy model
- `PublicationPolicyError` hierarchy
- truthful `PublicationExecutionError` fail-fast semantics
- `tests/integration/test_publication_service.py` 中的负路径覆盖

### Plan 05-04: Workload-Tier Verification Matrix and Baseline Dispatcher

Purpose:
- 将 PERF-01 / PERF-02 的实现成果编织成 `smoke` / `standard` / `large` 验证矩阵，形成可重复执行的治理表面。

Key outputs:
- `docs/runbooks/performance-verification-matrix.md`
- `scripts/run_perf_matrix.py`
- `reference/perf-baselines/smoke.json`
- `reference/perf-baselines/standard.json`
- `reference/perf-baselines/large.json`
- contract tests / script tests 保证 runbook 与脚本、baseline 文件同步

## Key Risks And How Plans Should Address Them

### Risk 1: Indexed optimization changes semantics subtly
- **Failure mode:** set/dict index 忽略了某些 `None` / 空字符串 / period mismatch 情况，导致 projection flags 或 trace retrieval 结果发生细微漂移。
- **Plan response:** 每个 hotspot 计划都要保留 integration or fixture proof；最终由 `tests/replay/` 全 acceptance suite 做裁决。

### Risk 2: Lazy index becomes stale after additional writes
- **Failure mode:** `record()` 之后 `_events_by_anchor` 不更新，后续 `find()` 返回旧结果。
- **Plan response:** 明确计划动作里要求 `record()` 使 index 失效或同步 append；并用 integration / contract test 覆盖 “record after first find” 场景。

### Risk 3: Pydantic model validates shape but not domain-target lookup intent
- **Failure mode:** malformed JSON 被拦住了，但 typo target 仍在 `build_publication_plan()` 中以裸 KeyError 泄露。
- **Plan response:** 独立 `UnknownDomainError` 与 `UnknownTargetError`，并在 integration tests 断言精确异常类型。

### Risk 4: Publication failure semantics still claim success indirectly
- **Failure mode:** mid-bundle failure 抛了异常，但先前已追加的 `PublicationResult.success` 或 storage side effect 仍让调用方误判。
- **Plan response:** 计划动作里明确要求：失败 bundle 不产出 `success=True` 假结果；测试中断言抛 typed error 且后续 bundle 未执行。

### Risk 5: Perf matrix becomes documentation-only
- **Failure mode:** 有 runbook 但没有 script/baseline，或者有 script 但 baseline 不受契约保护。
- **Plan response:** Plan 05-04 同时修改 docs、scripts、reference、tests 四类工件；任何一类缺失都不满足 PERF-03。

## Validation Architecture

### Test Framework

| Property | Value |
|----------|-------|
| Framework | `pytest 8.4.x` via `uv run pytest` |
| Config file | `pyproject.toml` |
| Quick run command | `uv run pytest tests/integration/test_publication_service.py tests/performance/test_trace_lookup_micro_benchmark.py tests/performance/test_contract_state_projection_benchmark.py tests/contracts/test_perf_matrix_contracts.py -v` |
| Full suite command | `uv run pytest -v` |
| Estimated runtime | ~240 seconds |

### Phase Requirements → Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| PERF-01 | `contract_state` membership lookup remains semantically identical while improving hotspot behavior | integration + performance + replay | `uv run pytest tests/performance/test_contract_state_projection_benchmark.py -v` and `uv run pytest tests/replay -v` | ❌ Wave 0 |
| PERF-01 | `InMemoryTraceStore.find()` returns the same ordered events while avoiding full linear scan cost on repeated lookups | contract/integration + performance + replay | `uv run pytest tests/performance/test_trace_lookup_micro_benchmark.py -v` and `uv run pytest tests/replay -v` | ✅ partial / ❌ Wave 0 extension |
| PERF-02 | publication policy failures are typed, actionable, and stop unsafe execution | integration | `uv run pytest tests/integration/test_publication_service.py -v` | ✅ exists / ❌ negative paths |
| PERF-03 | matrix tiers, baselines, and dispatcher stay synchronized and executable | contract + script + full suite | `uv run pytest tests/contracts/test_perf_matrix_contracts.py -v` and `uv run pytest -v` | ❌ Wave 0 |

### Recommended Verification Commands by Plan

| Plan | Development Command | Completion Command |
|------|---------------------|--------------------|
| 05-01 | `uv run pytest tests/performance/test_contract_state_projection_benchmark.py -v` | `uv run pytest tests/performance/test_contract_state_projection_benchmark.py tests/replay/test_annuity_performance_slice.py tests/replay/test_annual_award_slice.py tests/replay/test_annual_loss_slice.py -v` |
| 05-02 | `uv run pytest tests/performance/test_trace_lookup_micro_benchmark.py -v` | `uv run pytest tests/performance/test_trace_lookup_micro_benchmark.py tests/replay/test_annuity_performance_explainability_slo.py tests/replay/test_annual_award_explainability_slo.py tests/replay/test_annual_loss_explainability_slo.py -v` |
| 05-03 | `uv run pytest tests/integration/test_publication_service.py -v` | `uv run pytest tests/integration/test_publication_service.py tests/contracts/test_system_contracts.py -v` |
| 05-04 | `uv run pytest tests/contracts/test_perf_matrix_contracts.py -v` | `uv run pytest -v` |

### Wave 0 Gaps

- `tests/performance/test_contract_state_projection_benchmark.py` — projection hotspot benchmark and semantic fixture proof
- `tests/contracts/test_perf_matrix_contracts.py` — matrix doc, script, baseline file contract coverage
- `reference/perf-baselines/smoke.json` / `standard.json` / `large.json` — committed baseline assets
- `docs/runbooks/performance-verification-matrix.md` — matrix contract document
- `scripts/run_perf_matrix.py` — authoritative tier dispatcher

## Assumptions Log

| # | Claim | Risk if Wrong |
|---|-------|---------------|
| A1 | `InMemoryTraceStore.record()` is the only mutation path that needs index invalidation. | 如果还有其他 mutation seam，lazy index 可能 stale，需要补充失效逻辑。 |
| A2 | `tests/replay/` 当前已经足以覆盖两个热点的语义面。 | 如果 replay suite 没命中特定 edge case，需要补充 fixture-based micro oracle。 |
| A3 | `scripts/run_perf_matrix.py` 比 CLI 子命令更适合当前 repo 的 PERF-03 surface。 | 如果项目要求所有操作都走 CLI，则 Plan 05-04 需微调落点，但不改变矩阵本身。 |
| A4 | `InMemoryTableStore` 的 fail-fast behavior 足够通过抛异常表达 publication bundle failure。 | 如果 storage adapter 当前不会抛出明确异常，Plan 05-03 需要先补一个可测试的 failing path。 |

## Sources

### Primary

- `.planning/phases/05-performance-reliability-optimization-with-drift-safeguards/05-CONTEXT.md`
- `.planning/ROADMAP.md`
- `.planning/REQUIREMENTS.md`
- `.planning/PROJECT.md`
- `.planning/STATE.md`
- `.planning/codebase/CONCERNS.md`
- `.planning/codebase/STRUCTURE.md`
- `.planning/codebase/TESTING.md`
- `.planning/phases/02-transparent-pipeline-contracts-parity-gates/02-CONTEXT.md`
- `.planning/phases/03-orchestration-refactor-failure-explainability/03-CONTEXT.md`
- `.planning/phases/04-agent-operations-governance-hardening/04-CONTEXT.md`
- `.planning/phases/02.1-phase-2-governance-remediation-truthful-gates-and-status-sync/02.1-CONTEXT.md`
- `docs/superpowers/specs/2026-04-11-workdatahubpro-rebuild-architecture-draft.md`
- `docs/superpowers/specs/2026-04-11-workdatahubpro-refactor-program.md`
- `docs/superpowers/specs/2026-04-11-workdatahubpro-first-wave-legacy-coverage-matrix.md`
- `src/work_data_hub_pro/capabilities/projections/contract_state.py`
- `src/work_data_hub_pro/platform/tracing/in_memory_trace_store.py`
- `src/work_data_hub_pro/platform/publication/service.py`
- `src/work_data_hub_pro/platform/contracts/publication.py`
- `config/policies/publication.json`
- `tests/integration/test_publication_service.py`
- `tests/performance/test_trace_lookup_micro_benchmark.py`

## Metadata

- Confidence in scope boundaries: HIGH
- Confidence in exact module/file placement: HIGH
- Confidence in required test boundaries: HIGH
- Confidence in benchmark threshold calibration: MEDIUM

**Research date:** 2026-04-19
**Valid until:** 2026-04-26, because this is an active planning surface but the implementation has not started yet.

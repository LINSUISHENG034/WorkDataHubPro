# Phase 5: Performance Reliability Optimization with Drift Safeguards - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in `05-CONTEXT.md` — this log preserves the alternatives considered.

**Date:** 2026-04-19
**Phase:** 05 — performance-reliability-optimization-with-drift-safeguards
**Areas discussed:** Hotspot 优化范围与索引策略 (PERF-01), 漂移安全机制 (PERF-01 ↔ parity), Publication policy 校验 & 失败语义 (PERF-02), 验证矩阵 & 基准治理 (PERF-03)

---

## Gray Area Selection

| Option | Description | Selected |
|--------|-------------|----------|
| Hotspot 优化范围与索引策略 (PERF-01) | Scope, index data structure, API impact, lifecycle | ✓ |
| 漂移安全机制 (PERF-01 ↔ parity) | Mechanism, rollback unit, oracle convention, conflict authority | ✓ |
| Publication policy 校验 & 失败语义 (PERF-02) | Validator choice, error granularity, when to validate, partial-write behavior | ✓ |
| 验证矩阵 & 基准治理 (PERF-03) | Workload tiers, gate mapping, baseline storage, matrix form | ✓ |

**User's choice:** All four areas selected.

---

## Hotspot 优化范围与索引策略 (PERF-01)

| Option | Description | Selected |
|--------|-------------|----------|
| 严格锁定 CONCERNS.md 两处 | Touch only the two named hotspots; no opportunistic scanning | ✓ |
| 两处 + 提供扩展点 | Fix two, list candidates in RESEARCH for plan-time decision | |
| 允许机会主义扩展 | Profile-driven hot-path system scan included in Phase 5 | |

**User's choice:** 严格锁定 CONCERNS.md 两处.

| Option | Description | Selected |
|--------|-------------|----------|
| 预构建 dict/set 索引 | `set[(company_id, plan_code, period)]` and `dict[(batch_id, anchor_row_no), list[event]]`, build-once | ✓ |
| lru_cache / 记忆化查询 | Memoize call results; underlying linear scan unchanged | |
| Store-level 索引 + invalidate API | Maintain incremental index inside stores with explicit invalidate | |

**User's choice:** 预构建 dict/set 索引.

| Option | Description | Selected |
|--------|-------------|----------|
| 原位替换 (in-place) | Rewrite the existing function bodies; signatures unchanged | ✓ |
| 新增 indexed adapter | New `IndexedTraceStore` / `IndexedProjection` parallel layer | |
| Feature-flag 切换 | Old/new implementations selectable at runtime | |

**User's choice:** 原位替换 (in-place).

| Option | Description | Selected |
|--------|-------------|----------|
| Build-once 在调用点 | Lazy build on first call inside `_has_match` / `find` | ✓ |
| Build-on-write（增量维护） | Update index inside `record` / `add` write paths | |
| 显式 rebuild() API | Caller-driven `build_index()` invocation | |

**User's choice:** Build-once 在调用点.

**Notes:** Most conservative path consistently selected — narrow scope, simple data structures, surgical signature-preserving change, lifecycle aligned to batch-oriented replay runs.

---

## 漂移安全机制 (PERF-01 ↔ parity)

| Option | Description | Selected |
|--------|-------------|----------|
| 复用现有 replay acceptance suite | Each optimization commit must pass `tests/replay/` full suite + Phase 02.1 fail-closed baselines | ✓ |
| 新增 "优化前后 snapshot diff" 专项测试 | Per-hotspot oracle test asserting set equality of legacy vs new implementation | |
| 两者叠加 | Replay suite as release gate + snapshot diff as hotspot-level proof | |

**User's choice:** 复用现有 replay acceptance suite.

| Option | Description | Selected |
|--------|-------------|----------|
| Per-hotspot 一个 commit | Each hotspot lands as its own atomic commit; revert at hotspot granularity | ✓ |
| Per-plan 一个 commit | One commit per Phase 5 plan; coarser revert unit | |
| Feature-flag 切换作为 rollback 手段 | Runtime flag flips back to legacy path | |

**User's choice:** Per-hotspot 一个 commit.

| Option | Description | Selected |
|--------|-------------|----------|
| Git 历史 oracle | Don't keep legacy in tree; CI compares output across commits | |
| 不存原函数，用预计算 fixture | Commit `(input, expected_output)` golden samples under `reference/perf-baselines/` | ✓ |
| 代码内保留 _legacy() 双实现 | Keep `_legacy()` shim for tests to call | |

**User's choice:** 不存原函数，用预计算 fixture.

| Option | Description | Selected |
|--------|-------------|----------|
| Replay suite 为最终判决 | Replay suite + Phase 02.1 baselines override any micro oracle disagreement | ✓ |
| Snapshot diff 为最终判决 | Micro oracle wins; replay suite gap requires expansion | |

**User's choice:** Replay suite 为最终判决.

**Notes:** Reuses existing governance machinery rather than inventing new harness. Per-hotspot commit cadence aligns with the hotspot-locked scope from Area 1. Pre-computed fixture convention captures D-07's intent without forcing any new oracle test to exist; if one is added, this is the convention.

---

## Publication policy 校验 & 失败语义 (PERF-02)

| Option | Description | Selected |
|--------|-------------|----------|
| Pydantic v2 model | Aligns with existing `platform/contracts/` Pydantic discipline | ✓ |
| JSON Schema (jsonschema lib) | External schema file + runtime validator | |
| 手写验证函数 | Custom `_validate_policy()` returning typed errors | |

**User's choice:** Pydantic v2 model.

| Option | Description | Selected |
|--------|-------------|----------|
| 细分 4 类 | `PolicyFileMissingError` / `PolicyParseError` / `UnknownDomainError` / `UnknownTargetError` under `PublicationPolicyError` base | ✓ |
| 粗粒度两类 | `PolicyValidationError` (load) + `PolicyLookupError` (build) | |
| 单一 PublicationPolicyError + code 字段 | Single class with error-code enum | |

**User's choice:** 细分 4 类.

| Option | Description | Selected |
|--------|-------------|----------|
| Load 时 fail-fast | Full structural validation in `load_publication_policy`; cheap lookups thereafter | ✓ |
| Build 时才验证（lazy） | Defer validation until first lookup | |
| 分层：结构验证@load + 引用验证@build | Both layers, both typed | |

**User's choice:** Load 时 fail-fast.

| Option | Description | Selected |
|--------|-------------|----------|
| Fail-fast，抛 typed error | Raise `PublicationExecutionError` on first failed bundle and stop | ✓ |
| Continue-and-collect | Keep going; return `PublicationResult` with real `success` per bundle | |
| Best-effort rollback | Reverse-apply already-applied bundles on failure | |

**User's choice:** Fail-fast，抛 typed error.

**Notes:** Pydantic + 4-class typed errors is fully consistent with established platform/contracts and Phase 3 typed-diagnostic patterns. Fail-fast on execute reflects the truth that `InMemoryTableStore` lacks transactional semantics — clearer to halt on first failure than to fake partial-success accounting. The `success=True` literal in `PublicationResult` should be replaced with truthful semantics regardless.

---

## 验证矩阵 & 基准治理 (PERF-03)

| Option | Description | Selected |
|--------|-------------|----------|
| 三级：smoke / standard / large | Tiered workload with explicit CI mapping | ✓ |
| 二级：fast / full | Just fast vs complete | |
| 不分级，使用现有 replay 全套 | Minimal extension to existing suite | |

**User's choice:** 三级：smoke / standard / large.

| Option | Description | Selected |
|--------|-------------|----------|
| smoke@PR / standard@protected / large@nightly | Fast feedback + release gate + nightly stress | ✓ |
| 全部 perf 只跑 nightly | PR / protected don't run perf; lighter PR | |
| 调用方自选 tier (手动触发) | Documented manual commands; no enforced gate | |

**User's choice:** smoke@PR / standard@protected / large@nightly.

| Option | Description | Selected |
|--------|-------------|----------|
| reference/perf-baselines/ + 相对阈值 | JSON baselines committed; thresholds expressed as relative ratios (e.g. ×1.20) | ✓ |
| 只记录"优化后 vs 优化前"相对比 | Per-PR relative comparison; no absolute numbers in tree | |
| 不提交 baseline，只保证 perf 测试跑起来不报错 | Smoke-only — does not satisfy PERF-03 reproducibility requirement | |

**User's choice:** reference/perf-baselines/ + 相对阈值.

| Option | Description | Selected |
|--------|-------------|----------|
| Markdown 矩阵表 + scripts/run_perf_matrix.py | Human-readable matrix + executable dispatcher | ✓ |
| 纯 pytest marker (slow/perf/large) + 在 CI yml 里过滤 | Marker-based tier filtering via CI config | |
| 两者叠加 | Markdown + markers + script | |

**User's choice:** Markdown 矩阵表 + scripts/run_perf_matrix.py.

**Notes:** Three-tier model maps cleanly onto the existing PR / protected / nightly gate tiers from Phase 2 — no new gate ownership invented. Baseline lives where the project already keeps reference assets, with relative thresholds to absorb machine variance. Markdown matrix + script gives a single dispatcher and a documented surface that runbooks can link to.

---

## the agent's Discretion

- Exact Pydantic field names and `PublicationPolicyError` base location.
- Optional metrics in `reference/perf-baselines/*.json` beyond required p50/p95 wall-clock and peak memory.
- Whether `run_perf_matrix.py` lives under top-level `scripts/` or as an `apps/etl_cli/` subcommand.
- Inline vs helper implementation of "build-once" inside the two hotspot functions.
- Whether to add an internal micro oracle test alongside `tests/performance/test_trace_lookup_micro_benchmark.py`; if added, must follow the precomputed-fixture convention.

## Deferred Ideas

- Persistent / pluggable storage / tracing / evidence adapters (v2 RUN-01).
- Queue / retry runtime for large replay backlogs (v2 RUN-02).
- Additional publication channels (v2 RUN-03).
- Operator dashboards (v2 UX-01).
- Profile-driven hot-path system scan beyond the two named hotspots (future phase).
- Best-effort rollback / transactional `PublicationService.execute` semantics (depends on RUN-01).
- Verification-asset rows for `golden_set`, `golden_baseline`, `real_data_sample`, and dedicated error-case fixtures (Phase 2 carry-forward, still deferred).

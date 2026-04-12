# WorkDataHubPro

## What This Is

WorkDataHubPro is a brownfield rebuild of `E:\Projects\WorkDataHub`, focused on preserving proven business data-processing outcomes while reconstructing the system for clarity, transparency, maintainability, and agent operability. It keeps legacy processing semantics and result quality, but replaces opaque and tightly coupled execution with explicit, traceable, and testable pipeline architecture.

## Core Value

在不牺牲旧项目业务结果一致性的前提下，把数据处理流程重构为可解释、可验证、可维护、可由 agent 接管的系统。

## Requirements

### Validated

- ✓ Replay CLI can run domain slices for annuity performance, annual award, and annual loss in `src/work_data_hub_pro/apps/etl_cli/main.py` and `src/work_data_hub_pro/apps/orchestration/replay/*.py` — existing
- ✓ Capability-first package boundaries exist across `capabilities/`, `platform/`, `governance/`, `apps/` — existing
- ✓ Config-driven cleansing manifest activation exists via `config/releases/*.json` + `config/domains/*/cleansing.json` — existing
- ✓ Trace/evidence/adjudication baseline flow exists for replay divergence analysis — existing
- ✓ Test boundaries already exist (`tests/contracts`, `tests/integration`, `tests/replay`, `tests/performance`) — existing
- ✓ Legacy-to-Pro capability and intake-path mapping artifacts for `annuity_performance`, `annual_award`, and `annual_loss` — validated in Phase 1
- ✓ Phase 1 rule-classification inventory and default-block severity policy for parity-critical legacy behavior — validated in Phase 1
- ✓ Phase 1 parity baseline, executed annuity deep-sample comparison, and approved offline checkpoint for `PAR-01` — validated in Phase 1

### Active

- [ ] Remove black-box behavior by making each processing stage, rule decision, and failure path explicit
- [ ] Upgrade agent-operable project surfaces (entrypoints, diagnostics, config contracts, runbooks)
- [ ] Reduce orchestration duplication and high-coupling hotspots across replay slices
- [ ] Improve runtime efficiency without introducing behavior drift

## Current State

- Phase 1 complete: authoritative mapping, rule-classification, parity-baseline, and offline checkpoint artifacts are in place
- Current focus has shifted to Phase 2: explicit pipeline contracts, deterministic parity gates, and adjudication behavior
- Deferred carry-forward from Phase 1: runtime compatibility models still do not persist mismatch severity as a first-class field

### Out of Scope

- Big-bang one-shot rewrite of all domains at once — high risk, low verifiability
- Cosmetic-only refactor that improves structure but does not prove result parity — violates rebuild acceptance
- Premature migration to distributed runtime before parity and explainability foundations are complete — sequencing risk

## Context

- Current repo: `E:\Projects\WorkDataHubPro`
- Legacy source of truth for business outcomes: `E:\Projects\WorkDataHub`
- Existing codebase map under `.planning/codebase/` shows a strong capability-first baseline but also identifies critical concerns:
  - Replay orchestration duplication across three slices
  - Hard-coded release/policy/fixture paths in runtime code
  - Evidence/tracing persistence and security governance gaps
  - Performance hotspots in projection matching and trace lookup
- Rebuild success must be judged by both architecture quality and output parity with legacy behavior.

## Constraints

- **Parity**: New outputs must match legacy business semantics and quality for scoped domains — this is a release gate
- **Transparency**: Pipeline stages, rule paths, intermediate products, and failure reasons must be observable — avoid black-box behavior
- **Incremental Delivery**: Prefer narrow, verifiable phase slices over broad rewrite — reduce regression blast radius
- **Agent Operability**: Module boundaries, task entrypoints, configuration layout, diagnostics, and runbooks must support AI-agent execution and handoff
- **Performance Safety**: Any optimization must include behavior-drift detection and parity checks
- **Brownfield Reality**: Reuse validated patterns from current codebase map, but do not mechanically copy legacy architecture

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Use progressive brownfield reconstruction instead of big-bang rewrite | Limits risk and enables per-phase parity validation | ✓ Good |
| Treat output parity as primary acceptance gate, not optional QA | Prevents architectural improvements from breaking business semantics | ✓ Good |
| Prioritize non-black-box pipeline contracts and observability early | Enables maintainability and agent diagnostics from first delivery phases | ✓ Good |
| Make high-risk migration areas explicit in roadmap and phase verification | Incomplete rule migration and source-recognition drift must be surfaced early | ✓ Good |
| Keep planning artifacts local-only by default (`commit_docs=false`) | Repo currently treats `.planning/` as local workflow state | — Pending |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd-transition`):
1. Requirements invalidated? -> Move to Out of Scope with reason
2. Requirements validated? -> Move to Validated with phase reference
3. New requirements emerged? -> Add to Active
4. Decisions to log? -> Add to Key Decisions
5. "What This Is" still accurate? -> Update if drifted

**After each milestone** (via `/gsd-complete-milestone`):
1. Full review of all sections
2. Core Value check - still the right priority?
3. Audit Out of Scope - reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-04-12 after Phase 1 completion*

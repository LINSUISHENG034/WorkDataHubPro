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
- ✓ Deterministic replay checkpoints and comparison-run evidence packages for the accepted slices — validated in Phase 2
- ✓ Explicit compatibility adjudication semantics for severity, precedent, exception scope, and checkpoint identity — validated in Phase 2
- ✓ Repository-native PR / protected-branch / nightly parity gate tiers — validated in Phase 2
- ✓ Phase 6 governance remediation: fail-closed baseline loading (`load_required_checkpoint_baseline`), multiset duplicate-row diff accuracy (`_build_diff`), and explicit bootstrap entrypoint (`scripts/bootstrap_phase2_checkpoint_baselines.py`) — validated in Phase 6
- ✓ Phase 6 governance status sync: PROJECT.md, ROADMAP.md, and wiki-cn docs now distinguish Phase 2 implementation-complete from governance sign-off-pending — validated in Phase 6

### Active

- [ ] Upgrade agent-operable project surfaces (entrypoints, diagnostics, config contracts, runbooks)
- [ ] Reduce orchestration duplication and high-coupling hotspots across replay slices
- [ ] Improve runtime efficiency without introducing behavior drift

## Current State

- Phase 1 complete: authoritative mapping, rule-classification, parity-baseline, and offline checkpoint artifacts are in place
- Phase 2 implementation complete: explicit stage contracts, deterministic parity gates, derivation checkpoint governance, and CI-ready gate tiers are in place
- Phase 2 governance sign-off pending: Phase 6 remediation (truthful intermediate gates via accepted baseline comparisons, and diff accuracy via multiset-subtraction correction) is required before Phase 2 governance sign-off closes
- Phase 6 complete: truthful gates remediation and governance status sync done — Phase 2 governance sign-off can now proceed
- Deferred carry-forward from Phase 2: verification-asset rows for `golden_set`, `golden_baseline`, `real_data_sample`, and dedicated error-case fixtures remain explicitly deferred

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
| Commit `.planning/` artifacts as repository workflow state | `.planning` is now part of the governed project record, not ignored local scratch space | ✓ Good |

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
*Last updated: 2026-04-12 after Phase 2 completion*

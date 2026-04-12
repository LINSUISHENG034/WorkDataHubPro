# Phase 1: Legacy Capability Mapping & Parity Harness - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-04-12
**Phase:** 01-legacy-capability-mapping-parity-harness
**Areas discussed:** Capability mapping unit, Legacy coverage scope, Parity comparison basis, Difference severity policy, First must-pass checkpoint form, Evidence and trace artifact scope

---

## Capability mapping unit

| Option | Description | Selected |
|--------|-------------|----------|
| Business-only mapping | Focus only on business behaviors | |
| Stage/chain-only mapping | Focus only on legacy execution chain | |
| Dual-layer mapping | Business capability as primary, stage/function as trace evidence | ✓ |

**User's choice:** Dual-layer mapping (approved via referenced recommendation memo)
**Notes:** `docs/gsd/discuss/2026-04-12-phase-1-gray-area-recommendations.md` accepted as decision baseline.

---

## Legacy coverage scope

| Option | Description | Selected |
|--------|-------------|----------|
| Equal deep mapping for all three domains | Broad initial depth | |
| One deep sample + breadth registration | Deep map `annuity_performance`, register others | ✓ |
| Single domain only | Exclude other domains entirely | |

**User's choice:** One deep sample + breadth registration
**Notes:** `annuity_performance` chosen as Phase 1 deep sample.

---

## Parity comparison basis

| Option | Description | Selected |
|--------|-------------|----------|
| Final output only | Compare only final outputs | |
| Full intermediate parity | Compare all intermediates strictly | |
| Hybrid parity | Final must-match + parity-critical intermediate checkpoints | ✓ |

**User's choice:** Hybrid parity
**Notes:** Critical intermediates must be selected explicitly, not full clone.

---

## Difference severity policy

| Option | Description | Selected |
|--------|-------------|----------|
| Single severity | Treat all differences uniformly | |
| Block/Warn with default-block on unknown | Strict two-tier control | ✓ |
| Multi-level taxonomy now | Fine-grained severity from Phase 1 | |

**User's choice:** Block/Warn with strict default-block
**Notes:** Any unclassified mismatch type is blocking until categorized.

---

## First must-pass checkpoint form

| Option | Description | Selected |
|--------|-------------|----------|
| CI hard-fail immediately | Automated blocker in Phase 1 | |
| Offline report + human confirmation | Human-governed first gate | ✓ |
| No formal gate | Delay gate definition | |

**User's choice:** Offline report + human confirmation
**Notes:** CI hard-fail promotion deferred until mismatch semantics stabilize.

---

## Evidence and trace artifact scope

| Option | Description | Selected |
|--------|-------------|----------|
| Full evidence standard now | Define complete taxonomy in Phase 1 | |
| Minimum set now, full standard later | Stabilize minimum first | ✓ |
| Ad hoc evidence | No upfront standardization | |

**User's choice:** Minimum set now, full standard later
**Notes:** Minimum set fixed now: mapping matrix, baseline set, mismatch report, severity decision log.

## the agent's Discretion

- File-format details for interim artifacts, as long as required identity fields and traceability links are preserved.

## Deferred Ideas

- CI hard-fail parity gate promotion after policy stabilization.
- Full evidence directory governance standard after real mismatch pattern collection.

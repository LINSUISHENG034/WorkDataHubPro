# Phase 2: Transparent Pipeline Contracts & Parity Gates - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md. This log preserves the alternatives considered and the approval path.

**Date:** 2026-04-12
**Phase:** 02-transparent-pipeline-contracts-parity-gates
**Areas discussed:** Gate checkpoints, Adjudication behavior, Contract strictness, CI scope, Evidence shape

---

## Gate checkpoints

| Option | Description | Selected |
|--------|-------------|----------|
| Keep review recommendation | Use layered checkpoint types; Wave 1 gates are `source_intake`, `fact_processing`, `identity_resolution`, `contract_state`, and `monthly_snapshot`; `publication` is operational only; `reference_derivation` closes in Wave 2 | ✓ |
| Change baseline | Override the checkpoint taxonomy, wave split, or stage roles from the review document | |

**User's choice:** Keep review recommendation.
**Notes:** The user explicitly asked to refer to `docs/gsd/reviews/2026-04-12-phase2-gray-area-review.md` and then confirmed the baseline unchanged.

---

## Adjudication behavior

| Option | Description | Selected |
|--------|-------------|----------|
| Keep review recommendation | Expand `CompatibilityCase` with severity, precedent, richer status, temporary exceptions, and explicit fail/pass semantics | ✓ |
| Change baseline | Override the operational meaning of compatibility review and precedent handling | |

**User's choice:** Keep review recommendation.
**Notes:** Accepted semantics include `block` and `warn`, explicit recording of every new difference, and auto-accept only for approved precedent.

---

## Contract strictness

| Option | Description | Selected |
|--------|-------------|----------|
| Keep review recommendation | Controlled tolerance at raw intake, strict validation after normalization into internal contracts, no large schema-registry project | ✓ |
| Change baseline | Replace the tolerance/strictness split or alter the accepted intake baseline | |

**User's choice:** Keep review recommendation.
**Notes:** This includes the real-data-style intake baseline, minimum usable skeleton logic, and strict internal validation of boundary invariants.

---

## CI scope

| Option | Description | Selected |
|--------|-------------|----------|
| Keep review recommendation | Tiered CI: PR gate, protected-branch replay gate across accepted slices, nightly/release full-suite gate | ✓ |
| Change baseline | Use a different gate tiering model or narrower/broader mandatory replay coverage | |

**User's choice:** Keep review recommendation.
**Notes:** The accepted rationale is that the replay runtime is now shared across slices, so protected-branch gating must include all accepted replay slices.

---

## Evidence shape

| Option | Description | Selected |
|--------|-------------|----------|
| Keep review recommendation | Emit a comparison-run evidence package with manifest, checkpoint summaries, diffs, trace, lineage impact, publication results, compatibility case, and report | ✓ |
| Change baseline | Use a different failed-gate package shape or reduce/expand the required evidence set | |

**User's choice:** Keep review recommendation.
**Notes:** The accepted target is a failed-gate package that serves both human reviewers and downstream agent diagnosis.

---

## the agent's Discretion

- Internal helper names, validator module layout, and checkpoint fingerprint implementation details remain open as long as they preserve the approved semantics.

## Deferred Ideas

- None added during discussion beyond the review's already-scoped deferrals for Wave 2 `reference_derivation` gating and broader runtime/storage questions.

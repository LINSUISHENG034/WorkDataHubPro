# Phase 3: Orchestration Refactor & Failure Explainability - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md. This log records the confirmed decision baseline used for the Phase 3 discuss step.

**Date:** 2026-04-13
**Phase:** 03-orchestration-refactor-failure-explainability
**Mode:** discuss
**Areas discussed:** Shared replay composition, Failure contract, Agent entrypoints, Temporary identity policy
**Decision source:** `docs/gsd/grey-areas/2026-04-13-phase3-gray-area-decisions.md`

---

## Shared replay composition

| Option | Description | Selected |
|--------|-------------|----------|
| Shared primitives + explicit runners | Extract shared replay mechanics while preserving visible per-domain runners and wiring | ✓ |
| One fully generic replay runner | Route all domains through one generic runner with domain adapters | |
| Keep current duplication | Leave orchestration duplicated across slice runners | |

**User's choice:** Use shared replay primitives while keeping explicit per-domain runners.
**Notes:** The decision baseline explicitly rejects a single fully generic replay runner because domain asset loading, enrichment steps, and future `annuity_income` constraints are not just parameter changes.

---

## Failure contract

| Option | Description | Selected |
|--------|-------------|----------|
| Typed run report + typed exceptions | Separate invalid-run failures from completed-run mismatch outcomes | ✓ |
| Typed run report only | Force every failure through one run-report contract | |
| Single unified failure object | Collapse setup failure and replay mismatch into one surface | |

**User's choice:** Adopt a typed run report plus typed exceptions.
**Notes:** Preflight, config, and setup failures stay as typed exceptions; completed runs surface typed outcome data including checkpoint results, primary failure, evidence paths, and compatibility case details.

---

## Agent entrypoints

| Option | Description | Selected |
|--------|-------------|----------|
| Keep wrappers + add unified agent layer | Preserve current domain commands and add `replay run`, `replay diagnose`, and `replay list-domains` | ✓ |
| Replace wrappers with one unified replay CLI | Remove per-domain wrappers and route all access through one new command surface | |
| Keep only current wrappers | Improve current commands without adding a unified agent-facing surface | |

**User's choice:** Keep current human-facing wrappers and add a unified agent-facing replay layer.
**Notes:** Minimum standardized agent output is `comparison_run_id`, `overall_outcome`, `primary_failed_checkpoint`, `evidence_root`, and `compatibility_case_id`.

---

## Temporary identity policy

| Option | Description | Selected |
|--------|-------------|----------|
| Deterministic opaque temp ids with governed `IN` prefix | Normalize before hashing, use governed salt, keep raw names in sidecar evidence only | ✓ |
| Run-scoped opaque temp ids | Hide names, but allow ids to vary per run | |
| Keep `TEMP-{company_name}` | Preserve current raw-name fallback behavior | |

**User's choice:** Replace raw-name temp ids with deterministic opaque temp ids using the legacy-style deterministic model as reference and default `IN` prefix.
**Notes:** Prefix remains one governed global compatibility parameter; empty or placeholder names should return `None` instead of a shared fake temp id.

---

## the agent's Discretion

- Final exception class names and exact CLI presentation format, within the locked failure and output contracts.
- Final helper/module placement for shared replay primitives and temp-id helpers, within the locked shared-versus-explicit boundary.

## Deferred Ideas

- Legacy-style `etl` parity such as `--all-domains`, file discovery controls, and DB diagnostics.
- Full `etl`, `operator`, and `adjudication` command trees.
- Final retain-or-replace decisions for `company_lookup_queue`, `reference_sync`, and manual `customer-mdm` surfaces.
- Broader future-domain generalization beyond first-wave needs.

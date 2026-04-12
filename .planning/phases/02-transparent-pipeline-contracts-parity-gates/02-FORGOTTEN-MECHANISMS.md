# Phase 2 Forgotten Mechanisms Sweep

This sweep records the phase-critical mechanisms that Phase 2 depends on so they
are not left in an implicit state.

## verification assets

| Mechanism | Status | Owner / Track | Reason / Reference |
|-----------|--------|---------------|--------------------|
| Accepted replay baselines for `annuity_performance`, `annual_award`, and `annual_loss` | accepted | Phase 02-04 | Registered in `reference/verification_assets/phase2-accepted-slices.json` |
| Synthetic deterministic fixtures for accepted slices | accepted | Phase 02-04 | Explicitly tracked as `synthetic_fixture` assets in the Phase 2 manifest |
| Domain-level `golden set` coverage beyond the current replay baselines | deferred | Future verification-asset governance | Required by governance baseline but not yet materialized as repo-native assets |
| Real-data samples for accepted slices | deferred | Future intake-governance work | Phase 2 confirms these are target baselines, but the actual samples are not yet repository-native |
| Standalone error-case fixtures | deferred | Future failure-path asset work | Failure-path coverage exists in tests, but not as dedicated reusable fixtures |

## hidden runtime contracts

| Mechanism | Status | Owner / Track | Reason / Reference |
|-----------|--------|---------------|--------------------|
| Stable `batch_id = <domain>:<period>` and anchor-row preservation across replay stages | accepted | Phase 02 foundation | Enforced by the new contract validators and existing trace/lineage runtime |
| Deterministic comparison-run package layout under `comparison_runs/<comparison_run_id>/` | accepted | Phase 02 foundation | Explicitly implemented and referenced by the shared gate runtime |
| Publication target metadata (`target_name`, `mode`, `transaction_group`, `affected_rows`) as an operational gate | accepted | Phase 02 Wave 2 | Emitted in failed-run packages without turning publication into a parity comparator |
| Physical storage location for long-lived compatibility/evidence artifacts | deferred | Refactor program decision backlog | Program spec still lists this as an unresolved cross-cutting decision |

## operator artifacts

| Mechanism | Status | Owner / Track | Reason / Reference |
|-----------|--------|---------------|--------------------|
| Replay runbooks for accepted slices | accepted | Existing runbooks + Phase 02-04 | Current replay runbooks remain explicit operator entrypoints for accepted slices |
| Manual `customer-mdm` command surface | deferred | CT-015 follow-on operator tooling plan | Still outside the current validation-only replay scope |
| Shared unresolved-name and failed-record artifacts | deferred | CT-016 follow-on operator artifact plan | Explicitly registered in the first-wave coverage matrix but not closed in Phase 2 |

## parity scripts

| Mechanism | Status | Owner / Track | Reason / Reference |
|-----------|--------|---------------|--------------------|
| Provider-neutral Phase 2 gate-tier runner | deferred | Plan 02-05 | CI/runtime hardening is the next wave after this sweep |
| Legacy parity/bootstrap scripts still needed to recreate missing verification assets | deferred | Future parity-tooling review | Not yet replaced with repository-native equivalents for all asset classes |
| Hook-centric hidden parity shortcuts from the legacy system | retired | Capability-first rebuild | Replaced by explicit replay slices, gate contracts, and file-backed evidence packages |

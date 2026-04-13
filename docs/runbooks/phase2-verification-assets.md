# Phase 2 Verification Assets

## Goal

Make the accepted-slice verification assets for Phase 2 explicit, queryable, and
status-driven before CI hardening starts.

## Manifest

Primary registry:

- `reference/verification_assets/phase2-accepted-slices.json`

Each asset entry records:

- `asset_id`
- `asset_kind`
- `slice`
- `status`
- `purpose`
- `refresh_trigger`
- `reference_location`
- `notes`

## Status Model

- `accepted`: repository-native asset exists and is part of the current Phase 2 protection story
- `deferred`: asset is required or expected by governance, but is not yet materialized and must be revisited deliberately
- `planned`: asset has an admitted follow-on path but is not yet implemented
- `retired`: asset is intentionally no longer required

## Accepted Slices

Current accepted Phase 2 slices:

- `annuity_performance`
- `annual_award`
- `annual_loss`

For each slice, the manifest now tracks the following asset kinds explicitly:

- `replay_baseline`
- `synthetic_fixture`
- `golden_set`
- `golden_baseline`
- `error_case_fixture`
- `real_data_sample`
- `checkpoint_baseline`

## Checkpoint Baseline Assets

In addition to the primary replay baselines (`legacy_monthly_snapshot_2026_03.json`), each accepted
slice now also carries **accepted checkpoint baseline assets** for the intermediate pipeline
checkpoints that were promoted from self-compare placeholders to independently falsifiable
comparisons:

| Slice | Checkpoint | Baseline File |
|-------|-----------|---------------|
| `annuity_performance` | `reference_derivation` | `reference/historical_replays/annuity_performance/legacy_reference_derivation_2026_03.json` |
| `annuity_performance` | `fact_processing` | `reference/historical_replays/annuity_performance/legacy_fact_processing_2026_03.json` |
| `annuity_performance` | `identity_resolution` | `reference/historical_replays/annuity_performance/legacy_identity_resolution_2026_03.json` |
| `annuity_performance` | `contract_state` | `reference/historical_replays/annuity_performance/legacy_contract_state_2026_03.json` |
| `annual_award` | `reference_derivation` | `reference/historical_replays/annual_award/legacy_reference_derivation_2026_03.json` |
| `annual_award` | `fact_processing` | `reference/historical_replays/annual_award/legacy_fact_processing_2026_03.json` |
| `annual_award` | `identity_resolution` | `reference/historical_replays/annual_award/legacy_identity_resolution_2026_03.json` |
| `annual_award` | `contract_state` | `reference/historical_replays/annual_award/legacy_contract_state_2026_03.json` |
| `annual_loss` | `reference_derivation` | `reference/historical_replays/annual_loss/legacy_reference_derivation_2026_03.json` |
| `annual_loss` | `fact_processing` | `reference/historical_replays/annual_loss/legacy_fact_processing_2026_03.json` |
| `annual_loss` | `identity_resolution` | `reference/historical_replays/annual_loss/legacy_identity_resolution_2026_03.json` |
| `annual_loss` | `contract_state` | `reference/historical_replays/annual_loss/legacy_contract_state_2026_03.json` |

These checkpoint baseline assets are of kind `checkpoint_baseline` in the registry and are
registered as `accepted`. They are loaded at replay time by `load_required_checkpoint_baseline`
from `gate_runtime.py`.

**Refresh trigger for checkpoint baselines:** Run
`scripts/bootstrap_phase2_checkpoint_baselines.py --checkpoint <name> --domain <domain> --period 2026-03 --workbook <path>`
when the corresponding checkpoint's processing semantics change.

`source_intake` is intentionally not listed above. After Phase 6 closure it is a fixed
`contract` checkpoint with explicit expectations, not a repo-native `checkpoint_baseline`
asset and not a `legacy_source_intake_*.json` file.

## Current Position

### `annuity_performance`

- `replay_baseline`: `accepted`
- `synthetic_fixture`: `accepted`
- `checkpoint_baseline (reference_derivation)`: `accepted`
- `checkpoint_baseline (fact_processing)`: `accepted`
- `checkpoint_baseline (identity_resolution)`: `accepted`
- `checkpoint_baseline (contract_state)`: `accepted`
- `golden_set`: `deferred`
- `golden_baseline`: `deferred`
- `error_case_fixture`: `deferred`
- `real_data_sample`: `deferred`

### `annual_award`

- `replay_baseline`: `accepted`
- `synthetic_fixture`: `accepted`
- `checkpoint_baseline (reference_derivation)`: `accepted`
- `checkpoint_baseline (fact_processing)`: `accepted`
- `checkpoint_baseline (identity_resolution)`: `accepted`
- `checkpoint_baseline (contract_state)`: `accepted`
- `golden_set`: `deferred`
- `golden_baseline`: `deferred`
- `error_case_fixture`: `deferred`
- `real_data_sample`: `deferred`

### `annual_loss`

- `replay_baseline`: `accepted`
- `synthetic_fixture`: `accepted`
- `checkpoint_baseline (reference_derivation)`: `accepted`
- `checkpoint_baseline (fact_processing)`: `accepted`
- `checkpoint_baseline (identity_resolution)`: `accepted`
- `checkpoint_baseline (contract_state)`: `accepted`
- `golden_set`: `deferred`
- `golden_baseline`: `deferred`
- `error_case_fixture`: `deferred`
- `real_data_sample`: `deferred`

## How To Use It

- Use the manifest to see whether an asset is already protecting a slice or still deferred.
- Treat `synthetic_fixture` and `real_data_sample` as different governance objects; do not let one silently stand in for the other.
- When a missing asset becomes important for parity, explainability, or operator behavior, update the manifest status rather than leaving the gap implicit.

## Refresh Triggers

Refresh the manifest when:

- a new accepted replay slice is added
- a deferred asset becomes repository-native
- a replay baseline or checkpoint baseline changes
- an error-case fixture or real-data sample is introduced
- a later phase retires or replaces a protection mechanism

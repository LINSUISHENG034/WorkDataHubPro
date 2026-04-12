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

## Current Position

### `annuity_performance`

- `replay_baseline`: `accepted`
- `synthetic_fixture`: `accepted`
- `golden_set`: `deferred`
- `golden_baseline`: `deferred`
- `error_case_fixture`: `deferred`
- `real_data_sample`: `deferred`

### `annual_award`

- `replay_baseline`: `accepted`
- `synthetic_fixture`: `accepted`
- `golden_set`: `deferred`
- `golden_baseline`: `deferred`
- `error_case_fixture`: `deferred`
- `real_data_sample`: `deferred`

### `annual_loss`

- `replay_baseline`: `accepted`
- `synthetic_fixture`: `accepted`
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
- a replay baseline changes
- an error-case fixture or real-data sample is introduced
- a later phase retires or replaces a protection mechanism

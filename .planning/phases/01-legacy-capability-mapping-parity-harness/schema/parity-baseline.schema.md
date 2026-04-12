# Phase 1 Parity Baseline Schema

## Purpose

This schema defines the reproducible artifact contract for the PAR-01 offline
parity baseline bundle.

Phase 1 scope is intentionally limited to:

- baseline dataset identity
- mapping completeness status
- parity summary
- mismatch severity table
- human decision log

The schema fixes the minimum evidence set from D-13 and explicitly defers the
full evidence-directory taxonomy from D-14.

## Required Identity Fields

Every Phase 1 parity artifact must preserve these stable identity fields:

| Field | Required | Description |
| --- | --- | --- |
| `domain` | yes | PAR-01 domain identifier such as `annuity_performance`, `annual_award`, or `annual_loss`. |
| `sample_batch_id` | yes | Stable sample or breadth-registration batch identifier. |
| `baseline_version` | yes | Version for the accepted baseline contract. |
| `comparison_run_id` | yes | Stable identifier linking the baseline, mismatch report, and human decision log. |
| `decision_owner` | checkpoint only | Human reviewer identity recorded during the offline gate. |

## Required Intermediate Checkpoints

Phase 1 uses a hybrid parity rule: final output must match plus selective
intermediate checkpoints.

Each domain entry must describe these checkpoint names exactly:

- `source_recognition`
- `canonical_fact_shape`
- `identity_resolution_category`
- `publication_key_fields`

## Artifact Contract

### `artifacts/parity-baseline.json`

Required top-level content:

- `baseline_dataset_identity`
- `checkpoint_outputs`
- `domains`
- `required_intermediate_checkpoints`
- `minimum_evidence_set`
- `deferred_scope`

Per-domain requirements:

- `domain`
- `sample_batch_id`
- `baseline_version`
- `comparison_run_id`
- `mapping completeness status`
- replay reference paths for accepted Phase 1 fixtures or snapshots

### `artifacts/mismatch-report.json`

Required top-level content:

- `comparison_run_id`
- `baseline_version`
- `mapping completeness status`
- `baseline dataset identity`
- `parity_summary`
- `mismatch_table`
- `execution_evidence`
- `minimum_evidence_set`

The `mismatch_table` payload must be severity-table-ready and preserve:

- `severity`
- `classification_reason`
- `status`
- `evidence_ref`

Executed deep-sample comparison rows may record `severity: none` when a real
parity run completes without differences. In that case the row must still carry
an `evidence_ref` path that points to the executed comparison evidence bundle.

### `artifacts/decision-log.md`

Required content:

- `comparison_run_id`
- `decision_owner`
- `decision`
- `scope`
- `follow_up`

The decision log is a stable template for the offline human checkpoint. It must
remain within offline review scope and must not claim CI hard-fail enforcement.

## Deferred Scope

Phase 1 does not define the full evidence-directory taxonomy. Any future
taxonomy expansion must preserve the identity fields above and remain backward
compatible with this minimum evidence set.

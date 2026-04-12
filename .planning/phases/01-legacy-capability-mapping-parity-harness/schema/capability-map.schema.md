# Phase 1 Mapping Artifact Schema

This file defines the authoritative schema for Phase 1 mapping artifacts.

## `capability-map.csv`

Purpose: map each Phase 1 legacy business capability to its WorkDataHubPro owner and supporting stage-chain evidence.

### Required columns

| Column | Required | Description |
| --- | --- | --- |
| `capability_id` | yes | Stable row identifier for the mapped capability. |
| `domain` | yes | One of `annuity_performance`, `annual_award`, `annual_loss`. |
| `business_capability` | yes | Primary business behavior being mapped. |
| `legacy_behavior_meaning` | yes | Plain-language description of the legacy behavior semantics. |
| `legacy_owner_path` | yes | Legacy code or document path that owns the behavior. |
| `legacy_stage_chain` | yes | Legacy execution-stage or function-chain evidence for the behavior. |
| `pro_owner_path` | yes | WorkDataHubPro code path that owns the rebuilt behavior. |
| `pro_stage_chain` | yes | WorkDataHubPro runtime stage-chain evidence. |
| `migration_status` | yes | Current rebuild status. See allowed values below. |
| `parity_criticality` | yes | Phase 1 parity importance. See allowed values below. |
| `ambiguity_notes` | yes | Explicit ambiguity or resolution note. Empty string is allowed, but the column may not be omitted. |

### Allowed enum values

#### `migration_status`

- `existing`: WorkDataHubPro already has an implemented owner for the mapped behavior.
- `partial`: WorkDataHubPro has a partial or bridge-era implementation that still carries follow-up risk.
- `missing`: No implemented WorkDataHubPro owner exists yet.

#### `parity_criticality`

- `critical`: Phase 1 parity gate depends on this behavior.
- `supporting`: Important traceability or context row, but not a direct parity gate by itself.
- `breadth`: Registered for inventory breadth only; not deep-mapped in Phase 1.

### Row rules

- Every row must include all required columns in the header.
- `capability_id` values must be unique.
- `domain` must use the exact Phase 1 domain slug.
- `legacy_stage_chain` and `pro_stage_chain` must be explicit stage or function chains, not free-form placeholders.
- `ambiguity_notes` must exist for every row. Empty string is permitted only when there is no active ambiguity.

## `intake-path-map.csv`

Purpose: map legacy source-recognition paths to explicit WorkDataHubPro intake contracts, validation checks, and test anchors.

### Required columns

| Column | Required | Description |
| --- | --- | --- |
| `domain` | yes | One of `annuity_performance`, `annual_award`, `annual_loss`. |
| `legacy_source_path` | yes | Legacy source or operator path that feeds the intake behavior. |
| `legacy_owner_path` | yes | Legacy implementation or documentation owner for the recognition rule. |
| `legacy_recognition_rule` | yes | Legacy source-recognition rule or routing behavior being preserved. |
| `pro_intake_contract` | yes | WorkDataHubPro intake service or contract path. |
| `validation_check` | yes | Concrete validation condition that proves the intake contract. |
| `test_anchor` | yes | Existing test file or contract anchor that asserts the behavior. |
| `status` | yes | Current intake-path mapping status. See allowed values below. |
| `ambiguity_notes` | yes | Explicit ambiguity or rationale note. Empty string is allowed, but the column may not be omitted. |

### Allowed enum values

#### `status`

- `existing`: WorkDataHubPro intake contract and test anchor already exist.
- `partial`: WorkDataHubPro covers the path partially and requires follow-up clarification.
- `missing`: No explicit WorkDataHubPro intake contract exists yet.

### Row rules

- Every row must include all required columns in the header.
- `validation_check` must be non-empty.
- `test_anchor` must be non-empty and must point to a repo test path.
- `legacy_source_path`, `legacy_owner_path`, and `pro_intake_contract` must be explicit paths, not generic labels.
- `ambiguity_notes` must exist for every row. Empty string is permitted only when there is no active ambiguity.

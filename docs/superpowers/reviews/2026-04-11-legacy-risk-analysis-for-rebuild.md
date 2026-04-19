# WorkDataHubPro Legacy Risk Analysis For Rebuild

Date: 2026-04-11
Status: Active Risk Register

## Current Position

- `annual_loss` remains an accepted breadth-closure slice.
- `annuity_income` is now an accepted validation slice.

## Current accepted event-domain slices prove:

- replay-backed and current-row lookup behavior is now explicitly covered for the accepted event-domain paths.
- broader Phase E runtime and operator closure still remains follow-on work.

## Risk Register

| Risk ID | Risk | Source | Status | Related Rows |
|---------|------|--------|--------|--------------|
| `CR-008` | history-aware event-domain lookup and temporal enrichment semantics | supplemental `SFR-004` | `pending first-wave gap` | `AA-004`, `AL-003`, `CT-005`, `XD-005` |
| `CR-009` | `annuity_income` operator-facing artifact contract | supplemental `SFR-005` | `accepted but narrowed` | `AI-004` |
| `CR-010` | `annuity_income` service-delegation and explicit no-hook runtime contract | supplemental `SFR-006` | `accepted but narrowed` | `AI-005` |
| `CR-014` | deferred-lookup queue runtime, retry semantics, and special orchestration domain closure | `2026-04-12 legacy audit` | `deferred runtime/operator gap` | `CT-011`, `XD-003` |
| `CR-019` | shared unresolved-name and failed-record operator artifact parity across first-wave runs | `2026-04-12 legacy audit` | `pending first-wave gap` | `CT-016` |

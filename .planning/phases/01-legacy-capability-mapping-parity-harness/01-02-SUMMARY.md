---
phase: 01
plan: 02
subsystem: legacy-capability-mapping-parity-harness
tags:
  - mapping
  - parity
  - governance
  - integration-tests
requires:
  - MAP-03
provides:
  - rule classification schema for parity-critical legacy behavior
  - Phase 1 block/warn severity policy with default-block fallback
  - integration validation for rule classes and severity policy integrity
affects:
  - .planning/phases/01-legacy-capability-mapping-parity-harness/schema/rule-classification.schema.md
  - .planning/phases/01-legacy-capability-mapping-parity-harness/artifacts/rule-classification.csv
  - .planning/phases/01-legacy-capability-mapping-parity-harness/artifacts/severity-policy.md
  - tests/integration/test_phase1_rule_classification.py
decisions:
  - Kept the rule inventory focused on parity-relevant legacy behaviors instead of duplicating the broader capability map.
  - Added machine-readable severity policy summary lines so MAP-03 policy constraints can be asserted deterministically in tests.
metrics:
  verification_commands:
    - rg -n "must-keep|replace-with-equivalent|retire-with-proof|block|warn|default.*block" .planning/phases/01-legacy-capability-mapping-parity-harness/schema/rule-classification.schema.md
    - rg -n "annuity_performance|annual_award|annual_loss|default.*block|semantic output drift|source recognition" .planning/phases/01-legacy-capability-mapping-parity-harness/artifacts/rule-classification.csv .planning/phases/01-legacy-capability-mapping-parity-harness/artifacts/severity-policy.md
    - uv run pytest tests/integration/test_phase1_rule_classification.py -v
    - uv run pytest tests/integration -v
  completed_at: 2026-04-12
---

# Phase 01 Plan 02: Rule Classification and Severity Policy Summary

Explicit MAP-03 rule-classification and severity-policy artifacts with
integration enforcement for allowed classes and default-to-block severity.

## Outcomes

- Defined `rule-classification.schema.md` with the required CSV contract, the
  allowed class taxonomy (`must-keep`, `replace-with-equivalent`,
  `retire-with-proof`), required rationale fields, and Phase 1 severity-policy
  linkage.
- Built `rule-classification.csv` with deep `annuity_performance` coverage plus
  breadth registration rows for `annual_award` and `annual_loss`.
- Wrote `severity-policy.md` with explicit `block` and `warn` tiers, the
  `default-unclassified=block` rule, and machine-readable summary lines that
  the integration tests can parse directly.
- Added `tests/integration/test_phase1_rule_classification.py` to enforce class
  validity, auditability fields, allowed severity tiers, and default-to-block
  behavior.

## Verification

- `rg -n "must-keep|replace-with-equivalent|retire-with-proof|block|warn|default.*block" .planning/phases/01-legacy-capability-mapping-parity-harness/schema/rule-classification.schema.md`
  Outcome: passed; schema contains the required MAP-03 class taxonomy and Phase
  1 severity references.
- `rg -n "annuity_performance|annual_award|annual_loss|default.*block|semantic output drift|source recognition" .planning/phases/01-legacy-capability-mapping-parity-harness/artifacts/rule-classification.csv .planning/phases/01-legacy-capability-mapping-parity-harness/artifacts/severity-policy.md`
  Outcome: passed; the rule inventory and policy contain the required domain
  coverage and severity language.
- `uv run pytest tests/integration/test_phase1_rule_classification.py -v`
  Outcome: red phase failed with 2 assertions because `severity-policy.md`
  lacked machine-readable `Severity tiers:` and `Default rule:` lines.
- `uv run pytest tests/integration/test_phase1_rule_classification.py -v`
  Outcome: green phase passed; 3 tests passed after the policy summary lines
  were added.
- `uv run pytest tests/integration -v`
  Outcome: passed; 34 integration tests passed.

## Commits

- `61aa9b8` `test(governance.compatibility): add phase 1 rule classification checks`

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 2 - Critical functionality] Added machine-readable severity policy summary lines**
- **Found during:** Task 3 TDD red phase
- **Issue:** The human-readable policy text expressed the right rules, but it
  could not be asserted deterministically for `Severity tiers` and `Default
  rule` constraints.
- **Fix:** Added `Severity tiers: block, warn` and `Default rule:
  default-unclassified=block` to `severity-policy.md`.
- **Files modified:** `.planning/phases/01-legacy-capability-mapping-parity-harness/artifacts/severity-policy.md`
- **Commit:** local-only `.planning/` artifact; not committed because repo policy ignores `.planning/`

## Notes

- `.planning/` remains ignored by `.gitignore`, so the schema, artifact, and
  summary files were updated locally but not committed.
- The only committable plan file was
  `tests/integration/test_phase1_rule_classification.py`; it was committed
  independently as required.
- `git status --short` still shows an unrelated untracked file:
  `tests/contracts/test_phase1_parity_baseline_artifacts.py`. It was left
  untouched.

## Self-Check

PASSED

- Summary file exists at `.planning/phases/01-legacy-capability-mapping-parity-harness/01-02-SUMMARY.md`.
- Commit `61aa9b8` exists in git history.

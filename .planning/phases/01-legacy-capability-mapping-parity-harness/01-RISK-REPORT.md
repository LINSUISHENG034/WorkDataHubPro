---
phase: 01
status: complete
created: 2026-04-12
updated: 2026-04-12
source:
  - .planning/ROADMAP.md
  - .planning/phases/01-legacy-capability-mapping-parity-harness/01-CONTEXT.md
  - .planning/phases/01-legacy-capability-mapping-parity-harness/01-RESEARCH.md
  - .planning/phases/01-legacy-capability-mapping-parity-harness/artifacts/capability-map.csv
  - .planning/phases/01-legacy-capability-mapping-parity-harness/artifacts/intake-path-map.csv
  - .planning/phases/01-legacy-capability-mapping-parity-harness/artifacts/rule-classification.csv
  - .planning/phases/01-legacy-capability-mapping-parity-harness/artifacts/mismatch-report.json
---

# Phase 01 Risk Report

Phase 01 closed the mapping and parity-baseline foundation, but the highest-risk
carry-over items must be owned explicitly in Phase 2 so the project does not
mistake inventory for closure.

## Top Migration Risks

| Rank | Risk | Why It Still Matters | Phase 2 Mitigation Owner | Mitigation Path |
| --- | --- | --- | --- | --- |
| 1 | Source-recognition drift between legacy operator discovery and current replay intake | `annuity_performance` still depends on an explicit workbook path, and the real workbook sample is tracked as a contract gap rather than an executed replay input. | Phase 2 — `PIPE-01` / `platform.contracts` with `capabilities/source_intake` | Turn the intake boundary into an explicit machine-checkable contract and document the unsupported real workbook shape as either supported or intentionally rejected. |
| 2 | Hidden intermediate transformation mismatch | Phase 1 proves final-output parity for one deep sample, but intermediate checkpoints still rely on artifact assertions rather than contract-enforced runtime comparisons. | Phase 2 — `PIPE-01` and `PIPE-02` / `platform.contracts` + `platform.tracing` | Add explicit stage contracts and per-stage evidence so `source_recognition`, `canonical_fact_shape`, `identity_resolution_category`, and `publication_key_fields` can be compared deterministically. |
| 3 | Incomplete parity-rule migration confidence | The rule inventory and severity doctrine exist, but they are governance artifacts until replay adjudication applies them during live parity checks. | Phase 2 — `PAR-03` / `governance.compatibility` | Bind the `must-keep` / `replace-with-equivalent` / `retire-with-proof` classifications and `block|warn` severity policy into the comparator and adjudication flow. |
| 4 | Real-world workbook shape remains outside the must-pass replay path | The supplemental annuity workbook is informative but not yet executable by the current replay contract, so real-input confidence is lower than deep-sample confidence. | Phase 2 — `PAR-02` / `apps.orchestration` + `capabilities/source_intake` | Add either a supported adapter path for the real workbook or a formal contract-gap rejection path with evidence so the sample stops being ambiguous. |
| 5 | Breadth domains are registered but not deep-sampled | `annual_award` and `annual_loss` are visible in the baseline and rule inventory, but their parity evidence remains breadth-only in Phase 1. | Phase 2 — `PAR-02` / replay verification slice owners | Expand parity comparison from annuity-only deep sample to deterministic multi-domain comparisons using the registered breadth baselines. |

## Carry-Forward Rule

Phase 2 planning should treat these items as explicit input constraints, not
background context. A Phase 2 pass is incomplete unless it either closes these
risks or records an explicit adjudicated carry-over with a narrower owner.

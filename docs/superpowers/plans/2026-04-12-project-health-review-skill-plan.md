# Project Health Review Skill - Creation Plan

Date: 2026-04-12
Status: Draft
Author: User + Codex

---

## 1. Problem Statement

The WorkDataHubPro rebuild is agent-driven. The user:
- Cannot manually review all agent code for correctness
- Cannot verify if agent's development direction is aligned with project goals
- Risks: pseudo-implementation (fake completion), direction drift, missed coverage

**Root Cause**: No objective, third-party validation of agent work at the project level.

---

## 2. Solution: Project Health Review Skill

A skill that provides independent, objective evaluation of project-level development direction and progress.

Unlike `superpowers:verification-before-completion` (single task review), this skill focuses on:
- **"Are we building the RIGHT things?"** (not "Is this implementation correct?")
- Project-level progress vs. goals
- Coverage gaps and priorities
- Architecture alignment
- Risk identification

---

## 3. Skill Design

### 3.1 Name

```
superpowers:project-health-review
```

### 3.2 Location

```
docs/superpowers/skills/project-health-review.md
```

### 3.3 Triggers

| Trigger | When |
|---------|------|
| Manual | User invokes via `/project-health-review` |
| Weekly | Scheduled check during weekly review |
| Before new major work | When starting a new domain or significant feature |
| Pre-PR | Before merging significant changes |

### 3.4 Required Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Legacy Audit Doc | `docs/superpowers/audits/2026-04-12-legacy-code-audit.md` | **Source of truth for ultimate coverage goal** |
| Coverage Matrix | `docs/superpowers/specs/...-coverage-matrix.md` | Current coverage status |
| Architecture Spec | `docs/superpowers/specs/...-rebuild-architecture-draft.md` | Design baseline |
| Refactor Program | `docs/superpowers/specs/...-refactor-program.md` | Phase sequence and governance rules |
| Current Implementation | `src/work_data_hub_pro/` | Actual code state |
| All Active Plans | `docs/superpowers/plans/*.md` | Planned work vs ultimate goal |
| Git Status | `git status` / `git log` | Recent progress |

### 3.5 Evaluation Dimensions

#### Dimension 1: Direction Check
```
Questions:
- What was the stated goal for this period?
- Is current work aligned with that goal?
- Are there any obvious direction drifts?

Evidence Required:
- Git commit messages / PR titles
- Active slice/plan documents
- User-provided goals (if any)
```

#### Dimension 2: Progress Check
```
Questions:
- How many legacy capabilities are covered?
- How many are pending vs accepted?
- Is progress rate adequate?

Evidence Required:
- Coverage matrix status counts
- Last review baseline comparison
```

#### Dimension 3: Coverage Gap Analysis
```
Questions:
- Which audit findings are not yet covered?
- Are the uncovered items critical or deferrable?
- What is the blocking risk?

Evidence Required:
- Audit Section 9.2 (Uncovered Systems)
- Audit Section 9.3 (Critical Gaps)
```

#### Dimension 4: Architecture Alignment
```
Questions:
- Does implementation match architecture spec?
- Are there undocumented deviations?
- Is the structure (capabilities/platform/governance/apps) respected?

Evidence Required:
- Source code structure
- Architecture spec alignment
```

#### Dimension 5: Risk Identification
```
Questions:
- What risks are known?
- Are deferred items accumulating?
- Is there architectural debt?

Evidence Required:
- Coverage matrix "deferred" rows
- Open questions in audit
- Technical debt observations
```

#### Dimension 6: Phase Alignment
```
Questions:
- What phase does the refactor program state we are in?
- Does current work match the expected phase sequence?
- Are exit gates for current phase satisfied before moving forward?
- Are Phase E blockers being tracked?

Evidence Required:
- Refactor program spec (Section 6: Program Phases)
- Coverage matrix phase progress
- Current phase gate status
- Phase E decision backlog status (Section 13)
```

#### Dimension 7: Ultimate Goal Alignment
```
Questions:
- What is the ULTIMATE goal of this refactor? (Full legacy replication + error correction)
- Does current plan/impl move toward that goal or away from it?
- Are there legacy behaviors NOT covered by any current plan?
- Are there planned items NOT justified by legacy audit findings?
- Has any plan introduced scope not supported by legacy audit?

Evidence Required:
- Legacy Audit Doc (all sections including Section 9)
- All active plan documents
- Coverage matrix completeness check against audit

Key Insight:
- Plan documents are means to an end, NOT the end itself
- The end is: complete legacy coverage + identified/optimized errors
- If a plan doesn't trace back to a legacy audit finding, question it
```

#### Dimension 8: Legacy Coverage Completeness
```
Questions:
- Is EVERY legacy behavior accounted for? (accepted/deferred/retired)
- Are there audit findings with no corresponding coverage matrix row?
- Are there coverage matrix rows not supported by audit findings?
- Has any legacy behavior been silently dropped without retirement decision?

Evidence Required:
- Legacy Audit Doc - walk ALL sections
- Coverage Matrix - cross-reference every audit finding
- Slice Admission Records - validate all new work traces to audit

Completeness Check:
- For each audit finding → must have coverage matrix row OR retirement rationale
- For each coverage matrix row → must trace to specific audit finding
```

---

## 4. Output Format

### 4.1 Project Health Score

```
Project Health: [ON TRACK | AT RISK | OFF TRACK]

Score: X/8 dimensions passing

Phase Alignment: [Phase X] | Phase E Readiness: [YES | NO | BLOCKED]
Ultimate Goal Alignment: [ALIGNED | DRIFTING | OFF-TRACK]
```

### 4.2 Detailed Report

```markdown
## Direction Assessment
**Status**: ALIGNED / MISALIGNED / UNCLEAR

[Evidence and analysis]

## Coverage Progress
**Status**: ADEQUATE / BEHIND / STALLED

| Category | Accepted | Pending | Planned | Deferred |
|----------|----------|---------|---------|----------|
| annuity_performance | X | X | - | X |
| annual_award | X | X | - | X |
| annual_loss | X | X | X | X |
| annuity_income | X | X | X | X |
| Cross-cutting | X | X | - | X |

## Gap Analysis

### Critical Gaps (blocking)
- [Gap description]

### Non-Blocking Gaps
- [Gap description]

## Risk Register

| Risk | Severity | Mitigation |
|------|----------|-------------|
| EQC not integrated | High | Defer to Phase 2 |
| ... | ... | ... |

## Recommendations

### Immediate Actions
1. [Action]

### Should Defer
1. [Item]

### Architecture Deviations to Fix
1. [Deviation]

## Phase E Readiness Assessment

**Purpose**: Determine if first-wave rollout can advance to Phase E (Production Runtime and Operator Closure).

### Gate Checklist

| Gate | Status | Blocking Issues |
|------|--------|----------------|
| Phase D complete | YES/NO/PARTIAL | [list of unclosed domain rows] |
| Storage design committed | YES/NO | [physical location decision] |
| Publication model committed | YES/NO | [synchronous vs deferred decision] |
| Identity integration strategy defined | YES/NO | [provider integration approach] |
| Operator tooling path clear | YES/NO | [Dagster/replay tooling status] |
| Cross-cutting tracks registered | YES/NO | [lookup queue, reference_sync, etc.] |

### Phase E Entry Readiness

```
CAN ENTER PHASE E: [YES | NO]
BLOCKERS: [list]
REMAINING PHASE D ITEMS: [list]
```

### Phase F Prerequisites

Phase F (Legacy Retirement Review) cannot begin until:
- All first-wave coverage matrix rows are in `accepted`, `deferred`, or `retired`
- No row remains in implicit state (unknown, assumed, probably)
- All deferred items have written rationale and trigger to revisit
- All retired items have replacement path or removal rationale documented

## Ultimate Goal Alignment (Dimension 7)
**Status**: ALIGNED / DRIFTING / OFF-TRACK

**Ultimate Goal**: Complete legacy replication + identified/optimized errors

### Plan-to-Audit Traceability
| Plan Document | Audit Finding(s) | Coverage Matrix Row | Status |
|--------------|-----------------|---------------------|--------|
| [plan name] | [audit ref] | [row] | [connected/gap/orphaned] |

### Goal Drift Indicators
- [List of plans not traceable to audit findings]
- [List of implementations adding unneeded features]

### Silent Gap Registry
Audit findings with NO coverage matrix row and NO retirement decision:
- [audit finding reference]

## Legacy Coverage Completeness (Dimension 8)
**Coverage Completeness**: X/Y audit findings accounted for

### Uncovered Legacy Behaviors
| Audit Finding | Why Not Covered | Should Defer or Retire? |
|--------------|----------------|------------------------|
| [ref] | [reason] | [defer/retire] |

### Orphaned Coverage Rows
Coverage matrix rows NOT traceable to audit findings:
- [coverage row]

### Silent Error Corrections
Legacy bugs fixed without CompatibilityCase:
- [item + expected action]

---

## 5. Anti-Pattern Detection

The skill must detect and flag:

| Pattern | Description | Red Flag |
|---------|-------------|----------|
| **Pseudo-Implementation** | Agent claims completion without evidence | No test output, no coverage matrix update |
| **Coverage Matrix Staleness** | Matrix not updated despite claimed progress | Row status unchanged |
| **Deferred Accumulation** | Too many items deferred without rationale | >50% items deferred |
| **Direction Drift** | Working on low-priority items while high-priority blocked | Unrelated to stated goals |
| **Architecture Deviation** | Implementation doesn't match spec structure | Wrong folder/capability mapping |
| **Boundary Violation** | Slice admitted without meeting Slice Admission Rules (Section 8 of refactor-program.md) | Missing coverage matrix entry, unknown validation evidence path, untracked cross-domain dependency |
| **Hard Rule Breach** | Implementation violates Hard Rules in Section 5 of refactor-program.md | Legacy behavior covered without validation evidence path |
| **Goal Drift** | Plan/impl diverges from ultimate goal (full legacy replication) | Work not traceable to legacy audit finding |
| **Scope Creep** | Planned work includes features not in legacy audit | New capability without legacy justification |
| **Scope Shrinkage** | Legacy behavior missing from coverage without retirement decision | Audit finding has no coverage matrix row |
| **Silent Error Correction** | Legacy bug fixed without documenting the error or the correction rationale | Legacy deviation handled without CompatibilityCase |

### 5.1 Pseudo-Implementation Detection Rules

A claim of completion should be validated against these evidence requirements:

| Claim | Required Evidence |
|-------|-------------------|
| Slice accepted | Coverage matrix row updated to `accepted`, validation command committed, runbook updated |
| Coverage matrix updated | Row status actually changed (not just touched), evidence references present |
| Replay successful | Actual replay output showing matching results |
| Compatibility adjudicated | `CompatibilityCase` created with business rationale and approval |
| Hard Rule satisfied | Explicit validation evidence path defined for every covered legacy behavior |

### 5.2 Phase Alignment Check (Dimension 6)

Verify the current work aligns with the refactor-program.md phase sequence:

| Current Phase | Must Have Completed | Next Gate |
|--------------|---------------------|-----------|
| Phase A (Governance) | Architecture spec, coverage matrix, discipline docs | Exit gate: governance baseline committed |
| Phase B (First Slice) | `annuity_performance` accepted, replay evidence, compatibility path | Exit gate: first slice accepted |
| Phase C (Multi-Sheet) | `annual_award` accepted, multi-sheet archetype validated | Exit gate: multi-sheet archetype closed |
| Phase D (Breadth) | `annual_loss`, `annuity_income` accepted or deferred/retired | Exit gate: all first-wave domains in final state |
| Phase E (Production) | Storage, publication, operator tooling, identity integration resolved | Exit gate: no Phase E items block first-wave rollout |
| Phase F (Retirement) | All first-wave behaviors have explicit accepted/deferred/retired state | Exit gate: retirement decisions queryable |

**Phase Misalignment Red Flags:**
- Working on Phase D items while Phase C exit gate is not closed
- Claiming Phase B complete without replay evidence
- Starting new domains before Phase A governance baseline is committed

### 5.3 Risk Severity Aligned with Phase E Blockers

Risk severity must be calibrated against the Phase E decision backlog:

| Severity | Phase E Blocker Type | Examples |
|----------|---------------------|----------|
| **Critical** | Blocks Phase E entry | No accepted slice for a first-wave domain |
| **High** | Defers production readiness | Production storage undefined, operator tooling missing |
| **Medium** | Accumulated technical debt | Architecture deviation without adjudication |
| **Low** | Governance hygiene | Documentation not updated, replay asset stale |

**Phase E Decision Backlog (from Section 13 of refactor-program.md):**
1. Physical storage location for `CompatibilityCase` and evidence index
2. Publication execution model (synchronous vs deferred groups)
3. External identity/provider integration design
4. `company_lookup_queue` retention decision
5. `reference_sync` surface replacement decision
6. Enterprise persistence surface scope
7. Manual `customer-mdm` command support
8. Unresolved-name/failed-record artifact mandate
9. Operator-tooling and Dagster rollout order

### 5.4 Ultimate Goal Alignment Check (Dimensions 7 & 8)

**Ultimate Goal Definition:**
The refactor must achieve: **Complete legacy coverage + identified/optimized errors**

**Completeness Test:**

```
FOR EACH audit section:
  FOR EACH finding:
    → Is there a coverage matrix row? (accepted/deferred/retired)
    → OR is there a documented optimization (not error)?
    → OR is there explicit retirement rationale?

FOR EACH coverage matrix row:
    → Is it traceable to a specific audit finding?
    → Does the status have evidence path?
```

**Goal Drift Detection:**
| Condition | Meaning |
|-----------|---------|
| Active plan doesn't cite audit finding | Possible goal drift |
| Implementation adds feature not in audit | Scope creep |
| Audit finding has no coverage row | Silent gap |
| Gap silently accepted without decision | Scope shrinkage |
| Legacy bug fixed without documentation | Silent error correction |

**Error vs Optimization Decision Tree:**
```
Is this legacy behavior an ERROR?
├── YES → Is the fix documented?
│         ├── YES → Create CompatibilityCase with "legacy bug correction" rationale
│         └── NO → FLAG: Silent Error Correction
└── NO → Is this an intentional improvement over legacy?
          ├── YES → Document as "optimization" with business rationale
          └── NO → Default to faithful replication
```

---

## 6. Implementation Plan

### Phase 1: Create Skill Document
- [ ] Draft `docs/superpowers/skills/project-health-review.md`
- [ ] Define evaluation criteria and thresholds
- [ ] Create output template

### Phase 2: Test on Current Project
- [ ] Run skill against current project state
- [ ] Validate findings match reality
- [ ] Tune thresholds based on findings

### Phase 3: Establish Review Cadence
- [ ] Set weekly review schedule
- [ ] Define trigger conditions
- [ ] Create action item follow-up process

### Phase 4: Ultimate Goal Alignment Validation
- [ ] Cross-reference all active plans against legacy audit
- [ ] Identify orphaned plans (no audit finding)
- [ ] Identify silent gaps (audit findings without coverage)
- [ ] Establish error vs optimization decision process

---

## 7. Open Questions

1. **Frequency**: Weekly? Bi-weekly? Trigger-based?
2. **Owner**: Who acts on recommendations? (User or Agent?)
3. **Scope**: Include WorkDataHub (legacy) or only WorkDataHubPro?
4. **Confidence Threshold**: What score triggers immediate action?
5. **Error Correction Policy**: When a legacy error is found, what is the bar for documenting vs silently fixing?
6. **Audit Maintenance**: Who updates the legacy audit doc when new legacy behaviors are discovered during implementation?

---

## 8. References

- Legacy Audit: `docs/superpowers/audits/2026-04-12-legacy-code-audit.md`
- Coverage Matrix: `docs/superpowers/specs/2026-04-11-workdatahubpro-first-wave-legacy-coverage-matrix.md`
- Architecture Spec: `docs/superpowers/specs/2026-04-11-workdatahubpro-rebuild-architecture-draft.md`
- Existing Skill (reference): `superpowers:verification-before-completion`

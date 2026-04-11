# Review Summary: WorkDataHubPro Refactor Program

Date: 2026-04-11
Reviewer: Claude Code
Scope: `docs/superpowers/specs/2026-04-11-workdatahubpro-refactor-program.md` and `docs/superpowers/specs/2026-04-11-workdatahubpro-first-wave-legacy-coverage-matrix.md`

## Review Result: CONDITIONALLY APPROVED

Both documents are well-structured governance artifacts. The following issues should be resolved before treating them as the committed governance baseline.

---

## Refactor Program (`refactor-program.md`)

**Strengths:**
- Hard rules (Section 5) are clear and enforceable
- Phase gated exit gates prevent premature advancement
- Slice admission/exit rules are explicit and measurable
- Decision backlog (Section 13) honestly tracks unresolved blockers

**Issues to Clarify:**

1. **Section 3 "Current Position"** states "first-wave legacy coverage has not been fully enumerated in committed matrix form" — but the coverage matrix is present and complete. This appears to be stale language from an earlier drafting state. The statement conflicts with what the documents actually show.

2. **Section 6.4 Phase D exit gate** says "every first-wave matrix row is `accepted`, `deferred`, or `retired`" — but Phase D targets are `annual_loss` and `annuity_income`. If `annuity_performance` rows are still partially `deferred` (AP-008) at that point, the gate definition may need refinement to clarify whether cross-cutting deferred items count as program-level blockers.

3. **Cross-cutting track status terminology** — Section 10 marks tracks as "deferred" and "open", but the status model in the coverage matrix (Section 3) only defines `pending`, `planned`, `in_progress`, `accepted`, `deferred`, `retired`. The word "open" appears nowhere in the status model. This should be reconciled.

---

## Coverage Matrix (`first-wave-legacy-coverage-matrix.md`)

**Strengths:**
- Status model with explicit definitions prevents ambiguity
- Usage rules are enforceable ("no new slice without matrix entry")
- Cross-domain dependencies (XD-001 through XD-004) are explicitly tracked
- Retirement decisions are required, not assumed

**Issues to Verify:**

1. **Legacy source paths** — Several rows reference `E:\Projects\WorkDataHub\docs\domains\annuity_performance-capability-map.md` and `annual_award-capability-map.md`. These should be verified to exist in the legacy workspace before being cited as authoritative sources.

2. **AP-007 validation evidence** — References `tests/replay/test_annuity_performance_explainability_slo.py`. If this test file doesn't exist yet, the row is claiming evidence prematurely.

3. **Row AI-001 through AI-003** are all `pending` without an owning slice plan yet, which is fine per the admission rules, but the matrix correctly notes they are "not yet designed in detail."

---

## Cross-Document Consistency

| Issue | Location |
|-------|----------|
| Phase A complete but Section 3 says matrix not committed | `refactor-program.md:79` vs matrix itself |
| "open" status not in coverage matrix status model | `refactor-program.md:260` |
| AP-008 deferred indefinitely — no trigger date | Matrix row AP-008, column "Notes / Risks" |

---

## Recommendation

The documents are fundamentally sound. Before treating them as the committed governance baseline:

1. Update Section 3 language to reflect that the coverage matrix **is** now committed
2. Resolve the "open" vs "deferred" terminology gap for cross-cutting tracks
3. Verify the legacy capability map files exist at the cited paths
4. Confirm `test_annuity_performance_explainability_slo.py` exists as evidence

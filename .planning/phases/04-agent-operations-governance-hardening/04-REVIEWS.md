---
phase: 4
reviewers:
  - claude
reviewers_attempted:
  - claude
  - gemini
reviewed_at: 2026-04-18T23:31:13.2575699+08:00
plans_reviewed:
  - 04-01-PLAN.md
  - 04-02-PLAN.md
  - 04-03-PLAN.md
  - 04-04-PLAN.md
---

# Cross-AI Plan Review — Phase 4

## Gemini Review

No usable review output was produced.

`gemini` is installed locally, but its headless review path did not complete in this environment:

- Minimal prompt probe timed out twice after about 94 seconds.
- Full Phase 4 review attempt timed out after about 124 seconds.

Treat Gemini as an attempted-but-failed reviewer for this run.

---

## Claude Review

# Phase 4 Plan Review

## 04-01 — Output-to-Source Lookup Contract and CLI

### 1. Summary
This is a strong first execution slice and the right Phase 4 starting point. It directly closes the biggest operability gap between what the runtime already writes and what operators can actually query: the package already persists `source-intake-adaptation.json` and `lineage-impact.json` in `src/work_data_hub_pro/governance/compatibility/gate_runtime.py:22-33`, but those paths are not surfaced through `ReplayEvidencePaths` in `src/work_data_hub_pro/apps/orchestration/replay/contracts.py:21-29` or the diagnostics payload built in `src/work_data_hub_pro/apps/orchestration/replay/diagnostics.py:156-217`. The decomposition is sensible, but the plan needs a few more negative-path and ambiguity checks to avoid shipping a “works for happy path” lookup surface only.

### 2. Strengths
- Starts with the highest-value OPS-03 gap rather than overreaching into broader runtime changes.
- Reuses existing replay package and CLI surfaces instead of inventing new infrastructure.
- Correctly keeps lookup file-backed and package-reader-based, matching Phase 4 scope.
- Explicitly covers passed and failed/warning runs, which is important for real incident response.
- The proposed fields are concrete and operationally useful: `record_id`, `batch_id`, `anchor_row_no`, `origin_row_nos`, `parent_record_ids`, `trace_path`.

### 3. Concerns
- **HIGH** — The plan says lookup must “resolve exactly one record entry,” but it does not require tests for ambiguous input: both `--record-id` and `--anchor-row-no` supplied, no match found, or multiple matches for `anchor_row_no`.
- **MEDIUM** — Threat T-04-01 mentions invalid `comparison_run_id` handling, but acceptance criteria do not require a contract test for path-like or invalid identifiers. Existing validation exists in `src/work_data_hub_pro/apps/orchestration/replay/diagnostics.py:35-40`; the new surface should prove it reuses that safely.
- **MEDIUM** — Task 3 allows edits to `src/work_data_hub_pro/platform/tracing/in_memory_trace_store.py:6-20` and `src/work_data_hub_pro/platform/lineage/registry.py:6-17`, but those are not obviously required for a package-reader-based lookup. That invites unnecessary scope.
- **MEDIUM** — The plan should define how failed runs behave when lineage or trace artifacts are partially missing because failure occurred before a full package was assembled.
- **LOW** — The contract tests appear string-focused; they should also assert output-shape semantics, not just command presence.

### 4. Suggestions
- Add explicit negative tests for:
  - missing both selectors,
  - both selectors provided,
  - invalid/path-like `comparison_run_id`,
  - unknown `record_id`,
  - ambiguous `anchor_row_no`.
- State that `load_replay_lookup(...)` must fail closed on missing or malformed lineage package data instead of returning partial silent output.
- Narrow Task 3 wording so trace/lineage helper changes are only allowed if truly needed for deterministic fixtures.
- Require one integration test proving lookup still works after redaction lands in 04-02, or at least state that lookup fields are redaction-safe and must remain preserved.

### 5. Risk Assessment
**Overall risk: MEDIUM.**
The scope is appropriate and the architecture fit is good, but without stronger ambiguity and invalid-input coverage this could become an incomplete operator surface.

---

## 04-02 — Evidence Redaction Policy and Writer Hardening

### 1. Summary
This plan targets the most important security/governance gap in the current codebase and correctly places the fix at the persistence boundary in `src/work_data_hub_pro/governance/evidence_index/file_store.py:67-267`. It is aligned with the phase decisions and `.planning/codebase/CONCERNS.md`, but the proposed policy shape is a bit too coarse in places and risks either under-redacting checkpoint payloads or over-redacting evidence so aggressively that auditability and downstream diagnostics degrade.

### 2. Strengths
- Keeps redaction at the write boundary, matching D-07 through D-09.
- Centralizes policy in `config/`, which is the right governance surface.
- Covers multiple artifact classes instead of only traces.
- Explicitly preserves audit anchors, which is essential for OPS-03/OPS-04.
- Adds both contract and integration coverage rather than relying on documentation.

### 3. Concerns
- **HIGH** — The policy only lists `legacy_result` and `pro_result`, but current checkpoint result files also persist `legacy_payload` and `pro_payload` through `CheckpointResult` serialization in `src/work_data_hub_pro/governance/evidence_index/file_store.py:38-52`. Those may still leak sensitive values unless the plan explicitly covers them.
- **HIGH** — Replacing entire `legacy_result` / `pro_result` objects with `***REDACTED***` may destroy too much audit value. That would satisfy masking, but weaken compatibility investigation and could undercut GOV-03.
- **MEDIUM** — `preserve_exact_fields` does not mention `trace_path`, `origin_row_nos`, or `parent_record_ids`, which become important once 04-01 introduces lookup contracts.
- **MEDIUM** — The plan says `save_case(...)` and `write_comparison_case(...)` should redact current and future owner/status fields “added later,” but that preservation rule is not frozen in the policy contract.
- **LOW** — Loading policy on every writer call could introduce noisy repeated IO. Not a blocker, but easy to avoid with instance caching.

### 4. Suggestions
- Expand the policy/tests to explicitly cover `legacy_payload` and `pro_payload` in checkpoint result persistence.
- Clarify redaction semantics:
  - mask sensitive leaf values,
  - preserve non-sensitive structure,
  - avoid replacing whole objects unless absolutely necessary.
- Add `trace_path`, `origin_row_nos`, and `parent_record_ids` to the preserved contract or explicitly state why they are unaffected.
- Add one regression test proving `load_replay_lookup(...)` still works on redacted lineage/source packages.
- Cache the loaded redaction policy in `FileEvidenceIndex` or in the redaction module to avoid repeated file reads.

### 5. Risk Assessment
**Overall risk: MEDIUM-HIGH.**
The intent is correct, but the current policy shape could either miss leak paths or erase too much useful evidence unless the masking rules are tightened.

---

## 04-03 — Compatibility Lifecycle and Closure-Proof Hardening

### 1. Summary
This plan addresses a real GOV-03 gap: `CompatibilityCase` today is still a shallow record in `src/work_data_hub_pro/governance/compatibility/models.py:7-24`, and `AdjudicationService` in `src/work_data_hub_pro/governance/adjudication/service.py:9-48` only creates cases. The proposed lifecycle fields and CLI are directionally right, but this plan has the most important hidden consistency risk of the four: compatibility cases currently exist in two persisted forms, and the plan does not yet say which is authoritative during transitions.

### 2. Strengths
- Focuses on auditable ownership and closure proof, which is exactly what GOV-03 requires.
- Keeps enforcement in the service layer rather than putting validation in CLI-only code.
- Adds explicit CLI commands instead of expecting humans to edit JSON by hand.
- Requires `decision_history`, which is useful if the final status collapses earlier states.
- Uses file-backed persistence, consistent with Phase 4 scope.

### 3. Concerns
- **HIGH** — There are currently two storage paths for cases:
  - `compatibility_cases/<case_id>.json` via `save_case(...)` in `src/work_data_hub_pro/governance/evidence_index/file_store.py:145-147`
  - `comparison_runs/<id>/compatibility-case.json` via `write_comparison_case(...)` in `src/work_data_hub_pro/governance/evidence_index/file_store.py:193-199` and `src/work_data_hub_pro/governance/compatibility/gate_runtime.py:315-333`
  The plan does not say how transitions keep both synchronized. That is the biggest issue.
- **MEDIUM** — `decision_status` is being used as both outcome and lifecycle stage. If a case moves `approved_exception -> closed`, the final state may lose the adjudication meaning unless history is guaranteed to preserve it.
- **MEDIUM** — `--evidence-root` as a free path for CLI operations is flexible, but it widens the trust boundary and should be treated carefully.
- **MEDIUM** — The plan does not specify a transition table. “Unknown statuses rejected” is good, but allowed transitions should also be constrained.
- **LOW** — The contract tests freeze command names/options, but should also verify exit behavior for invalid transitions.

### 4. Suggestions
- Make storage authority explicit:
  - either `compatibility_cases/<case_id>.json` becomes the source of truth and run packages mirror it,
  - or transitions must update both locations atomically.
- Add an explicit transition matrix, e.g.:
  - `pending_review -> approved_exception | rejected_difference`
  - `approved_exception | rejected_difference -> closed`
- Require one integration test proving a transitioned case is reflected both in the case store and in replay diagnostics / package readers.
- Consider keeping adjudication outcome separate from lifecycle closure, or at minimum require `decision_history` to retain the prior outcome when status becomes `closed`.
- Add CLI negative tests for missing owner, empty resolution note, empty closure evidence, and illegal state transitions.

### 5. Risk Assessment
**Overall risk: HIGH.**
The problem is important and the direction is right, but the plan currently underspecifies persistence consistency and lifecycle semantics. If implemented literally, it could create stale or conflicting case records.

---

## 04-04 — Agent Maintenance Workflow and Incident Runbooks

### 1. Summary
This is a good closing slice for Phase 4 and the dependency ordering is correct. It keeps OPS-02 grounded in repo-native paths and commands, and the contract-test approach is appropriate for guarding against documentation drift. The main limitation is that this plan can only be as truthful as Plans 01-03; if those surfaces are incomplete or semantically awkward, this runbook will faithfully document weak contracts rather than fix them.

### 2. Strengths
- Correctly depends on the earlier implementation plans.
- Keeps documentation bounded to committed repo surfaces instead of hidden local practice.
- Uses a single canonical runbook plus domain-specific references, which matches D-01 and avoids duplication.
- Adds executable drift protection instead of trusting docs by convention.
- Keeps scope narrow and avoids turning docs work into a UI or workflow engine project.

### 3. Concerns
- **MEDIUM** — The “add a source” workflow is mostly documentation over existing surfaces, not a newly enforced onboarding contract. That may be enough for OPS-02, but it is weaker than the other plans’ code-backed guarantees.
- **MEDIUM** — The tests only prove docs contain strings, not that those strings still correspond to working CLI behavior or valid registry/config relationships.
- **LOW** — The plan references only the three current domain runbooks, while the registry also includes `annuity_income` in `src/work_data_hub_pro/apps/orchestration/replay/registry.py:10-55`. That may be intentional, but the runbook should state current supported workflow scope explicitly.
- **LOW** — If 04-03 lands with unresolved lifecycle semantics, the workflow may have to document awkward compatibility-state behavior.

### 4. Suggestions
- Add one contract test that checks current registry entries expose `runbook_path`, `release_path`, and `domain_config_path` that actually exist, not just that docs mention those concepts.
- In the runbook, explicitly state that Phase 4 standardizes the bounded change surface for existing replay domains; adding a brand-new domain still requires code and config updates in the named files.
- Include one manual verification checklist item at the top of the canonical runbook, aligned with `.planning/phases/04-agent-operations-governance-hardening/04-VALIDATION.md:63-68`.
- If you keep the string-based doc tests, make them intentionally exact but minimal to reduce churn.

### 5. Risk Assessment
**Overall risk: LOW-MEDIUM.**
This plan is appropriately small and mostly about truthful documentation and drift protection. Its success depends more on earlier plans than on its own complexity.

---

# Overall Cross-Plan Assessment

## What is well-designed
- The four-plan decomposition is strong and matches the phase goals.
- Wave ordering is mostly correct: queryability first, then safety hardening, then adjudication lifecycle, then documentation.
- The plans consistently avoid out-of-scope runtime expansion.
- Security and auditability are treated as first-class requirements rather than optional cleanup.
- Validation strategy is better than average: each requirement is tied to concrete tests.

## Biggest cross-plan risks
- **Highest risk:** compatibility-case persistence authority is unclear across `compatibility_cases/` and per-run package files.
- **Second highest risk:** redaction policy may be too coarse and either miss checkpoint leaks or erase useful audit evidence.
- **Third risk:** lookup plan needs stronger invalid-input and ambiguity handling, not just happy-path coverage.

## Recommended adjustments before execution
1. Tighten 04-01 negative-path requirements.
2. Refine 04-02 masking semantics to preserve structure while redacting sensitive leaves.
3. Resolve 04-03 storage authority and transition model before implementation starts.
4. Keep 04-04’s claims tightly bounded to what 01-03 actually deliver.

## Overall Phase 4 plan risk
**Overall risk: MEDIUM.**
The phase is well-scoped and decomposed correctly, but a few underspecified contracts, especially compatibility-case persistence and redaction detail, could create rework if not clarified before execution.

---

## Consensus Summary

Only one external reviewer completed successfully, so there is no true multi-model consensus yet. Treat the items below as the highest-priority findings from the successful external review.

### Agreed Strengths
- Phase 4 is decomposed into the right four plans and follows a sound wave order.
- The plans stay inside the locked file-backed Phase 4 scope and avoid speculative runtime expansion.
- Validation is concrete and tied to specific contract and integration coverage.

### Agreed Concerns
- 04-03 underspecifies compatibility-case persistence authority across `compatibility_cases/` and per-run package files; this is the highest-risk issue.
- 04-02 redaction rules are too coarse and may either miss checkpoint leak paths or destroy too much diagnostic value.
- 04-01 needs explicit negative-path coverage for invalid IDs, selector ambiguity, no-match cases, and partial artifact conditions.

### Divergent Views
- No divergent views to compare in this run because only one external reviewer completed successfully.

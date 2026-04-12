# Phase 6 Security Audit Report

**Phase:** 06 - phase-2-governance-remediation-truthful-gates-and-status-sync
**Audit Date:** 2026-04-13
**ASVS Level:** Not specified in plan files
**Block On:** Not specified

---

## Threat Verification Summary

| Threat ID | Category | Disposition | Status | Evidence |
|-----------|----------|-------------|--------|----------|
| T-06-01 | T | mitigate | CLOSED | `load_required_checkpoint_baseline()` raises `FileNotFoundError` when baseline absent (gate_runtime.py:87-92); test `test_missing_reference_derivation_baseline_fails_closed` exists (test_phase6_gate_runtime.py:88-101) |
| T-06-02 | I | mitigate | CLOSED | `_build_diff()` uses Counter-based multiset subtraction (gate_runtime.py:100-130); tests `test_build_diff_counts_duplicate_rows_correctly`, `test_build_diff_counts_extra_rows_correctly`, `test_build_diff_counts_mixed_duplicate_rows_correctly` exist (test_phase6_gate_runtime.py:28-82) |
| T-06-03 | R | mitigate | CLOSED | Bootstrap script `scripts/bootstrap_phase2_checkpoint_baselines.py` uses argparse with explicit `--checkpoint`, `--domain`, `--period`, `--output` flags; no automatic fallback path; test `test_bootstrap_script_declares_explicit_cli` exists (test_phase6_gate_runtime.py:117-161) |
| T-06-04 | T | mitigate | CLOSED | All three slices call `load_required_checkpoint_baseline()` for `fact_processing`, `identity_resolution`, `contract_state`: annuity_performance_slice.py:287-304, annual_award_slice.py:276-290, annual_loss_slice.py:290-304 |
| T-06-05 | R | mitigate | CLOSED | `source_intake` now loads `legacy_source_intake_<period>.json` via `load_required_checkpoint_baseline()` (fail-closed if absent); all three slices updated; bootstrap script updated; baseline files registered in phase2-accepted-slices.json |
| T-06-06 | D | mitigate | CLOSED | Tests `test_event_domain_intermediate_checkpoint_uses_baseline_award` (test_phase2_event_domain_gates.py:478-659) and `test_event_domain_intermediate_checkpoint_uses_baseline_loss` (test_phase2_event_domain_gates.py:662-783) force intermediate failures; `test_reference_derivation_requires_baseline_*` tests assert missing-baseline failures (test_phase2_reference_derivation_gates.py:587-642) |
| T-06-07 | R | mitigate | CLOSED | PROJECT.md (lines 38-40) and docs/wiki-cn/roadmap/overview.md (line 27) contain synchronized Phase 2 status wording distinguishing implementation-complete from governance sign-off-pending |
| T-06-08 | D | mitigate | CLOSED | ROADMAP.md line 195: "Plans: 3 plans" with 06-01/06-02/06-03 entries; STATE.md line 21: "Current command focus: `gsd-execute-phase 6`" |
| T-06-09 | T | mitigate | CLOSED | `tests/contracts/test_phase2_governance_status_sync.py` exists with string-based contract tests `test_phase2_status_sync_across_project_roadmap_wiki`, `test_phase6_roadmap_entry_has_three_plans`, `test_wiki_roadmap_has_dated_phase2_sync_note` |
| T-06-10 | R | mitigate | CLOSED | `reference/verification_assets/phase2-accepted-slices.json` registers all checkpoint baselines (reference_derivation, fact_processing, identity_resolution, contract_state) for all three slices with status "accepted" and proper `asset_kind: "checkpoint_baseline"` entries (lines 69-320) |

---

## Security Audit Trail

| Audit Date | Auditor | Result | Threats Open |
|------------|---------|--------|--------------|
| 2026-04-13 | gsd-security-auditor (initial) | OPEN_THREATS | 1 (T-06-05) |
| 2026-04-13 | gsd-security-auditor (closure) | SECURED | 0 |

## Accepted Risks Log

No accepted risks were declared in the threat models for this phase.

---

## Unregistered Flags

No unregistered threat flags were found in the SUMMARY.md files for this phase.

---

## Open Threats Detail

### T-06-05: source_intake contract gate

**Status:** OPEN

**Issue:** The `source_intake` checkpoint in `annuity_performance_slice.py` (and likely the other slices) still performs self-comparison rather than using fixed external expectations.

**Evidence:**
```python
# annuity_performance_slice.py lines 412-421
build_checkpoint_result(
    checkpoint_name="source_intake",
    checkpoint_type="contract",
    legacy_payload={
        "record_count": len(source_intake_pro_payload),  # Same as pro_payload
        "required_fields": list(_SOURCE_INTAKE_CONTRACT["required_fields"]),  # Same as pro_payload
        "allowed_adaptations": list(_SOURCE_INTAKE_CONTRACT["allowed_adaptations"]),  # Same as pro_payload
    },
    pro_payload={
        "record_count": len(source_intake_pro_payload),  # Same as legacy_payload
        "required_fields": list(_SOURCE_INTAKE_CONTRACT["required_fields"]),  # Same as legacy_payload
        "allowed_adaptations": list(_SOURCE_INTAKE_CONTRACT["allowed_adaptations"]),  # Same as legacy_payload
    },
    ...
)
```

**Expected Mitigation:** The `legacy_payload` for `source_intake` should come from a fixed external baseline file (e.g., `legacy_source_intake_<period>.json`), not from the current runtime payload. The `pro_payload` would then be the actual runtime output.

**Files to Fix:**
- `src/work_data_hub_pro/apps/orchestration/replay/annuity_performance_slice.py`
- `src/work_data_hub_pro/apps/orchestration/replay/annual_award_slice.py`
- `src/work_data_hub_pro/apps/orchestration/replay/annual_loss_slice.py`

---

## Summary

**Total Threats:** 10
**Closed:** 9
**Open:** 1

The Phase 6 threat mitigations are substantially complete. The single open threat (T-06-05) involves the `source_intake` checkpoint still performing self-comparison instead of comparing against a fixed external baseline. This was explicitly flagged in code review WR-05.

---

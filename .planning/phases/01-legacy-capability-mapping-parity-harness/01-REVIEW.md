---
phase: 01-legacy-capability-mapping-parity-harness
reviewed: 2026-04-12T10:57:23.9653016Z
depth: standard
files_reviewed: 3
files_reviewed_list:
  - tests/contracts/test_phase1_mapping_artifacts.py
  - tests/integration/test_phase1_rule_classification.py
  - tests/contracts/test_phase1_parity_baseline_artifacts.py
findings:
  critical: 0
  warning: 4
  info: 0
  total: 4
status: issues_found
---

# Phase 01: Code Review Report

**Reviewed:** 2026-04-12T10:57:23.9653016Z
**Depth:** standard
**Files Reviewed:** 3
**Status:** issues_found

## Summary

Reviewed the three committable Phase 01 test files referenced by the plan summaries. The largest regression is branch-level: commits `53ecfad`, `61aa9b8`, and `af58546` exist only on `docs/phase1-mapping-parity-harness`, and none of the three test files are present on the current `HEAD`, so Phase 01 artifact coverage is not active on `main`.

Inside the committed tests, there are two kinds of problems: missing assertions for planned parity checks, and assertions that are stricter than the phase contract and will fail on valid future artifact updates.

## Warnings

### WR-01: Phase 01 Test Coverage Is Not Present On Current HEAD

**Files:** `tests/contracts/test_phase1_mapping_artifacts.py`, `tests/integration/test_phase1_rule_classification.py`, `tests/contracts/test_phase1_parity_baseline_artifacts.py`
**Line:** `1`
**Issue:** The three Phase 01 test files were added in commits `53ecfad`, `61aa9b8`, and `af58546`, but `git merge-base --is-ancestor <commit> HEAD` is false for all three and `HEAD` does not contain the files. That means the branch being reviewed has lost all automated coverage added during the phase.
**Fix:**
```text
Merge or cherry-pick 53ecfad, 61aa9b8, and af58546 into the branch under review,
or recreate equivalent tests before treating Phase 01 coverage as present.
```

### WR-02: Mapping Contract Test Misses The Planned Stage-Chain Assertions

**File:** `tests/contracts/test_phase1_mapping_artifacts.py:54`
**Issue:** Plan `01-01` explicitly required a deep-sample check that `annuity_performance` rows have non-empty `legacy_stage_chain` and `pro_stage_chain` values, but the test file only checks domain coverage and required columns. An artifact can now blank out both traceability fields and still pass.
**Fix:**
```python
def test_annuity_performance_rows_have_stage_chains() -> None:
    _, rows = _read_csv_rows(CAPABILITY_MAP)

    annuity_rows = [row for row in rows if row["domain"] == "annuity_performance"]
    assert annuity_rows
    for row in annuity_rows:
        assert row["legacy_stage_chain"].strip()
        assert row["pro_stage_chain"].strip()
```

### WR-03: Rule Classification Test Requires Every Allowed Class To Appear

**File:** `tests/integration/test_phase1_rule_classification.py:41`
**Issue:** `assert {row["class"] for row in rows} == ALLOWED_CLASSES` enforces that the dataset must contain at least one `must-keep`, one `replace-with-equivalent`, and one `retire-with-proof` row. The plan only requires each row to use an allowed class, not that every enum member be represented in every snapshot. Valid future inventories can fail spuriously.
**Fix:**
```python
assert rows
for row in rows:
    assert row["class"] in ALLOWED_CLASSES
```

### WR-04: Parity Baseline Test Hardcodes A Clean Match And Depends On Row Order

**File:** `tests/contracts/test_phase1_parity_baseline_artifacts.py:89`
**Issue:** The test picks `annuity_rows[0]` and then requires `status == "matched"` and `severity == "none"`. PAR-01 only requires at least one executed deep-sample comparison entry for `annuity_performance`; a real run that records an actual mismatch or a reordered row list would be valid but would fail this test.
**Fix:**
```python
deep_sample_row = next(
    row
    for row in mismatch_report["mismatch_table"]["rows"]
    if row["domain"] == "annuity_performance" and row["evidence_ref"].strip()
)
assert deep_sample_row["status"] in {"matched", "mismatched"}
assert deep_sample_row["severity"] in {"none", "warn", "block"}
assert Path(deep_sample_row["evidence_ref"]).exists()
```

---

_Reviewed: 2026-04-12T10:57:23.9653016Z_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: standard_

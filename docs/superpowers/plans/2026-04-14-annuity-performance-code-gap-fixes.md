# Annuity Performance Code Gap Fixes Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fix the confirmed annuity-performance legacy code issues currently recorded as `GAP-AP-003`, `GAP-AP-004`, and `GAP-AP-005`.

**Architecture:** Treat the wiki gap register as the source of truth for issue scope, then isolate the fixes into three narrow code paths: runtime gold-validation drift, organization backfill source-field mismatch, and `集团企业客户号` null propagation into `年金账户号`. Keep fixes local to the old repository and verify each one with targeted tests before any broader refactor.

**Tech Stack:** Python, Pandas, Pandera, YAML config, legacy `E:\Projects\WorkDataHub` codebase

---

## Scope

This plan covers:

- `GAP-AP-003`
- `GAP-AP-004`
- `GAP-AP-005`

This plan does not cover:

- wiki changes already completed
- `GAP-AP-007`
- broad identity-resolution redesign

## Files To Inspect Or Modify

- `E:\Projects\WorkDataHub\src\work_data_hub\domain\annuity_performance\service.py`
- `E:\Projects\WorkDataHub\src\work_data_hub\domain\annuity_performance\helpers.py`
- `E:\Projects\WorkDataHub\src\work_data_hub\domain\annuity_performance\pipeline_builder.py`
- `E:\Projects\WorkDataHub\config\foreign_keys.yml`
- related annuity-performance tests under `E:\Projects\WorkDataHub\tests\`

## Tasks

### Task 1: Decide and close `GAP-AP-003`

- [ ] Verify whether annuity-performance should call `validate_gold_dataframe()` like award/loss.
- [ ] If yes, add the missing gold-validation step in the active runtime path.
- [ ] Add or update targeted tests proving the stricter contract is now enforced.

### Task 2: Fix `GAP-AP-004`

- [ ] Confirm the correct source field for `fk_organization` on canonical annuity-performance rows.
- [ ] Update `config/foreign_keys.yml` so organization backfill uses the correct field.
- [ ] Add or update targeted coverage proving organization names are not silently lost.

### Task 3: Fix `GAP-AP-005`

- [ ] Prevent Python `None` from materializing as literal string `"None"` in `集团企业客户号` cleanup.
- [ ] Verify the derived `年金账户号` preserves true null semantics.
- [ ] Add or update targeted coverage for this exact null-handling path.

## Expected Outcome

After execution:

- annuity-performance runtime path and declared gold contract will be aligned
- organization backfill will read the intended canonical source field
- `年金账户号` will no longer risk carrying literal `"None"` from null source values

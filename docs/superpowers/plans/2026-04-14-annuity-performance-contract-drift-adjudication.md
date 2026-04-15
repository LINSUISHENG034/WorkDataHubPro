# Annuity Performance Contract Drift Adjudication Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Resolve the remaining annuity-performance contract drift item (`GAP-AP-007`) by deciding whether the old 5-level YAML priority description should be removed, rewritten, or backed by code cleanup.

**Architecture:** Focus on the annuity-performance-relevant identity documentation and resolver layers only. Compare config loader, facade docs, resolver core docs/comments, and active YAML strategy. The outcome should be one of: stale docs cleanup only, documentation plus dead-code cleanup, or a deeper intentional-difference record.

**Tech Stack:** Markdown plans, legacy Python code under `E:\Projects\WorkDataHub`

---

## Scope

This plan covers:

- `GAP-AP-007`

This plan does not cover:

- runtime bug fixes already isolated into the code-gap-fix plan
- broader company-id redesign

## Files To Inspect

- `E:\Projects\WorkDataHub\src\work_data_hub\config\mapping_loader.py`
- `E:\Projects\WorkDataHub\src\work_data_hub\infrastructure\enrichment\company_id_resolver.py`
- `E:\Projects\WorkDataHub\src\work_data_hub\infrastructure\enrichment\resolver\core.py`
- `E:\Projects\WorkDataHub\src\work_data_hub\infrastructure\enrichment\resolver\yaml_strategy.py`

## Tasks

### Task 1: Confirm the authoritative active priority model

- [ ] Identify which implementation path annuity-performance actually executes for YAML overrides.
- [ ] Confirm whether only `plan -> hardcode -> name` is active in practice.

### Task 2: Classify the remaining 5-level references

- [ ] Determine whether the 5-level descriptions are:
  - stale docs/comments only
  - dead but still shipped code/config semantics
  - still-active behavior through another path

### Task 3: Produce the cleanup action

- [ ] If stale docs/comments only, prepare a minimal cleanup change list.
- [ ] If dead code/config semantics remain, prepare a cleanup change list that removes or marks them clearly.
- [ ] If any part is still semantically active, write the intentional-difference note needed to stop future confusion.

## Expected Outcome

After execution:

- `GAP-AP-007` will have a final disposition
- the annuity-performance identity-priority story will no longer rely on contradictory descriptions

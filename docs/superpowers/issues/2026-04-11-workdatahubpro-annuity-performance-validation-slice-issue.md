# WorkDataHubPro Outstanding Issues

> Review date: 2026-04-11
> Basis: blueprint + file-by-file source review + test-suite validation

---

## Outstanding Issues By Priority

---

### P1 - Real Defect

#### 1. `LineageRegistry` Is Never Used, So the Lineage Chain Is Broken

**Location:** `src/work_data_hub_pro/platform/lineage/registry.py`

**Issue:** The `LineageLink` model and `LineageRegistry` class exist, but no registry is instantiated anywhere in the end-to-end `run_annuity_performance_slice()` flow, and nothing calls `register()` or `get()`. That means:

- the lineage path from input records to `CanonicalFactRecord` is never recorded
- `trace_ref` exists on `CanonicalFactRecord`, but lineage is intended to be a separate trace axis
- any future parent-record lookup by lineage will find an empty registry

**Impact:** The lineage traceability described in the blueprint is already broken in Phase 1.

**Suggested fix:** Create a `LineageLink` for each `InputRecord` and register it in a `LineageRegistry` inside `AnnuityPerformanceProcessor.process()` or `AnnuityPerformanceIntakeService.read_batch()`, with the registry passed through the local `run_annuity_performance_slice()` flow.

---

### P2 - Design Limitation / Production Risk

#### 2. Cleansing Logic Still Requires Python Code Changes

**Location:** `src/work_data_hub_pro/capabilities/fact_processing/cleansing/manifest.py`

**Issue:** `RULE_PACKS` is a `dict[tuple[rule_pack_id, rule_pack_version], dict[field_name, CleansingRule]]` whose values point to Python-defined transformation functions such as `strip_and_uppercase`, `normalize_plan_code`, and `parse_decimal`. The JSON config only controls:

- which fields are enabled (`enabled_fields`)
- execution order (`activation_order`)
- the rule-pack version identifier (`rule_pack_version`)

The JSON config cannot describe new transformation logic. Any new or changed cleansing rule still requires editing Python functions in `rules.py` and redeploying code.

**Impact:** This is not suitable for workflows where business users are expected to adjust cleansing behavior independently. Rule changes still carry deployment cost.

**Suggestion:** Document this explicitly as a known design limit. If stronger decoupling is needed, consider:

- moving rule-function registration into a serializable rule-pack definition
- or explicitly accepting "rule change = code change" and adding release-review gates for rule-pack updates in CI/CD

#### 3. Missing Columns Fail Hard With `KeyError`

**Location:**

- `src/work_data_hub_pro/capabilities/fact_processing/annuity_performance/service.py` line 33
- `src/work_data_hub_pro/capabilities/source_intake/annuity_performance/service.py` line 49

**Issue:** In `AnnuityPerformanceProcessor.process()`:

```python
before = cleaned_fields[active_rule.field_name]   # KeyError if column missing
```

`AnnuityPerformanceIntakeService.read_batch()` also uses `zip(headers, row, strict=True)`, so a real workbook with unexpected column count fails immediately.

**Impact:** Common real-data problems such as missing columns, whitespace in headers, or case differences will stop the entire intake or processing batch. There is no skip path, error counting, or structured degraded handling.

**Suggested fix:** Catch missing-field cases in `process()`, emit an error trace event with `success=False`, and populate `error_message` instead of raising immediately.

---

### P3 - Readability / Maintainability

#### 4. `normalize_plan_code` And `strip_and_uppercase` Are Identical

**Location:** `src/work_data_hub_pro/capabilities/fact_processing/cleansing/rules.py` lines 15-21

**Issue:**

```python
def strip_and_uppercase(value: Any) -> str:
    return str(value).strip().upper()

def normalize_plan_code(value: Any) -> str:
    return str(value).strip().upper()
```

`normalize_plan_code` does not express any additional "normalize" semantics such as special-character handling or truncation. It is currently equivalent to `strip_and_uppercase`.

**Suggestion:** Confirm whether the business meaning is actually the same. If it is, merge the functions under a clearer shared name such as `trim_upper`. If future plan-code normalization needs extra logic, implement it explicitly.

#### 5. `MonthlySnapshotProjection` Aggregate Naming Is Misleading

**Location:** `src/work_data_hub_pro/capabilities/projections/monthly_snapshot.py` lines 20-25

**Issue:**

```python
"award_fixture_rows": sum(
    1 for row in contract_state_rows if row["has_annual_award_fixture"]
)
```

The field is named `award_fixture_rows`, but it actually counts rows in `contract_state` where `has_annual_award_fixture=true`. It does not count rows in the fixture file itself, which makes the name easy to misread.

**Suggestion:** Rename it to `contracts_with_award_fixture` or `award_fixture_contract_count` so the metric meaning is explicit.

---

# WorkDataHubPro Legacy Semantic Map Registry Bootstrap Implementation Plan

> **Status:** Proposed

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Bootstrap the smallest checked-in semantic-map registry that is still governed, testable, and reusable by later discovery waves.

**Architecture:** Treat this slice as registry bootstrap only. The slice must establish controlled vocabularies, seeded discovery denominators, the active wave registry, and a bootstrap writer that can regenerate the minimal checked-in tree. It must not yet introduce claim compilation, integrity reporting, or wave-closeout mechanics that belong to later slices.

**Tech Stack:** Python 3.12, `uv`, `pytest`, `PyYAML`, JSON, YAML, Markdown

---

## Scope Check

This plan covers only `Slice 1: Registry Bootstrap` from `docs/superpowers/specs/2026-04-16-workdatahub-legacy-semantic-map-design.md`.

This plan does cover:

- controlled vocabularies and ID-shape contracts
- seeded execution-entry and source-family catalogs
- active wave metadata
- a bootstrap writer under `scripts/legacy_semantic_map/`
- a checked-in semantic-map subtree with boundary rules, owner, and archive trigger
- an explicit lint exclusion so the semantic-map subtree does not drift into durable wiki expectations

This plan does not cover:

- claim artifact creation
- canonical compilation from claims
- candidate triage workflow
- integrity or coverage report generation
- wave closeout logic
- first-wave discovery execution against legacy sources

Those belong to later implementation plans.

## Bootstrap Boundary

This slice is intentionally minimal.

It should create only the files required to make the discovery ledger real and governable:

- `README.md`
- `manifest.json`
- `execution/entry-surfaces.yaml`
- `sources/families.yaml`
- `waves/index.yaml`
- empty future-work directories that need to exist now for stable tree shape

This slice should not seed:

- `claims/`
- `reports/`
- `edges/`
- `candidates/`
- canonical subsystem/object files beyond empty directory placeholders

If a file is not required to define vocabularies, denominators, wave identity, or boundary rules, it should wait for a later slice.

## Proposed File Structure

### Files To Create

- `scripts/legacy_semantic_map/__init__.py`
- `scripts/legacy_semantic_map/models.py`
- `scripts/legacy_semantic_map/bootstrap.py`
- `tests/contracts/test_legacy_semantic_map_bootstrap.py`
- `tests/contracts/test_legacy_semantic_map_repo_docs.py`
- `docs/wiki-bi/_meta/legacy-semantic-map/README.md`
- `docs/wiki-bi/_meta/legacy-semantic-map/manifest.json`
- `docs/wiki-bi/_meta/legacy-semantic-map/execution/entry-surfaces.yaml`
- `docs/wiki-bi/_meta/legacy-semantic-map/execution/paths/.gitkeep`
- `docs/wiki-bi/_meta/legacy-semantic-map/execution/stages/.gitkeep`
- `docs/wiki-bi/_meta/legacy-semantic-map/sources/families.yaml`
- `docs/wiki-bi/_meta/legacy-semantic-map/waves/index.yaml`
- `docs/wiki-bi/_meta/legacy-semantic-map/subsystems/.gitkeep`
- `docs/wiki-bi/_meta/legacy-semantic-map/objects/.gitkeep`

### Files To Modify

- `pyproject.toml`
- `uv.lock`
- `docs/wiki-bi/_meta/wiki-maintenance-lint-checklist.md`

### Responsibilities

- `scripts/legacy_semantic_map/models.py` defines the controlled vocabulary and seed dataclasses reused by later slices.
- `scripts/legacy_semantic_map/bootstrap.py` writes the minimal registry tree deterministically.
- `README.md` carries the non-durable boundary, active owner, and archive trigger.
- `manifest.json` points only to canonical seed sources created by this slice.
- `wiki-maintenance-lint-checklist.md` explicitly excludes the semantic-map subtree from durable-page lint expectations.

---

## Task 1: Add Tooling-Only Semantic Map Contracts

**Files:**
- Modify: `pyproject.toml`
- Modify: `uv.lock`
- Create: `scripts/legacy_semantic_map/__init__.py`
- Create: `scripts/legacy_semantic_map/models.py`
- Create: `tests/contracts/test_legacy_semantic_map_bootstrap.py`

- [ ] **Step 1: Write a failing contract test for controlled vocabularies and wave ID shape**

The test must lock:

- `status`
- `claim_type`
- `source_type`
- `evidence_strength`
- `coverage_state`
- `triage_status`
- `wave_id` regex shape

- [ ] **Step 2: Run the targeted test and confirm it fails before implementation**

Run:

```bash
uv run pytest tests/contracts/test_legacy_semantic_map_bootstrap.py::test_semantic_map_enums_and_wave_id_shape -v
```

Expected: fail because `scripts.legacy_semantic_map` does not exist yet.

- [ ] **Step 3: Add the minimal contract module and tooling dependency**

Implementation requirements:

- add `PyYAML` only to the dev/tooling dependency group
- keep all semantic-map helper code under `scripts/legacy_semantic_map/`
- do not add anything under `src/work_data_hub_pro/`

- [ ] **Step 4: Refresh the lockfile and rerun the targeted contract test**

Run:

```bash
uv lock
uv sync --dev
uv run pytest tests/contracts/test_legacy_semantic_map_bootstrap.py::test_semantic_map_enums_and_wave_id_shape -v
```

Expected: pass.

## Task 2: Add The Minimal Bootstrap Writer

**Files:**
- Modify: `scripts/legacy_semantic_map/__init__.py`
- Create: `scripts/legacy_semantic_map/bootstrap.py`
- Modify: `tests/contracts/test_legacy_semantic_map_bootstrap.py`

- [ ] **Step 1: Extend the contract test to require minimal seeded registry output**

The bootstrap test must require only:

- `README.md`
- `manifest.json`
- `execution/entry-surfaces.yaml`
- `sources/families.yaml`
- `waves/index.yaml`
- empty future-work directories via `.gitkeep`

The test must also require that `README.md` contains:

- `not durable wiki content`
- an explicit owner field
- an explicit archive trigger

- [ ] **Step 2: Run the targeted bootstrap test and confirm it fails before implementation**

Run:

```bash
uv run pytest tests/contracts/test_legacy_semantic_map_bootstrap.py::test_bootstrap_semantic_map_writes_minimal_registry -v
```

Expected: fail because `bootstrap_semantic_map` does not exist yet.

- [ ] **Step 3: Implement the bootstrap writer**

Implementation requirements:

- seed the first-wave execution entry surfaces
- seed the first-wave high-priority source families
- seed one active bootstrap wave
- create only the minimal checked-in registry files listed in this plan
- write a `README.md` that states:
  - this subtree is an internal discovery ledger
  - it is not durable wiki content
  - it must never be added to `docs/wiki-bi/index.md`
  - the active owner is the main-thread maintainer of the current semantic-map wave
  - the archive trigger is acceptance of the target durable wiki updates plus disposition of remaining findings for that wave

- [ ] **Step 4: Run the bootstrap contract test**

Run:

```bash
uv run pytest tests/contracts/test_legacy_semantic_map_bootstrap.py -v
```

Expected: pass.

## Task 3: Materialize The Checked-In Tree And Lock The Boundary Rules

**Files:**
- Create: `tests/contracts/test_legacy_semantic_map_repo_docs.py`
- Create: `docs/wiki-bi/_meta/legacy-semantic-map/README.md`
- Create: `docs/wiki-bi/_meta/legacy-semantic-map/manifest.json`
- Create: `docs/wiki-bi/_meta/legacy-semantic-map/execution/entry-surfaces.yaml`
- Create: `docs/wiki-bi/_meta/legacy-semantic-map/execution/paths/.gitkeep`
- Create: `docs/wiki-bi/_meta/legacy-semantic-map/execution/stages/.gitkeep`
- Create: `docs/wiki-bi/_meta/legacy-semantic-map/sources/families.yaml`
- Create: `docs/wiki-bi/_meta/legacy-semantic-map/waves/index.yaml`
- Create: `docs/wiki-bi/_meta/legacy-semantic-map/subsystems/.gitkeep`
- Create: `docs/wiki-bi/_meta/legacy-semantic-map/objects/.gitkeep`
- Modify: `docs/wiki-bi/_meta/wiki-maintenance-lint-checklist.md`

- [ ] **Step 1: Write a failing repo-doc contract test**

The repo-doc test must assert:

- the checked-in semantic-map subtree exists
- `manifest.json` points to the three canonical seed sources from this slice
- `README.md` contains the non-durable boundary, owner, and archive trigger
- `docs/wiki-bi/index.md` does not contain `legacy-semantic-map`
- `wiki-maintenance-lint-checklist.md` explicitly excludes the subtree from durable-page lint checks

- [ ] **Step 2: Run the repo-doc contract test and confirm it fails**

Run:

```bash
uv run pytest tests/contracts/test_legacy_semantic_map_repo_docs.py -v
```

Expected: fail because the checked-in tree and lint exclusion do not exist yet.

- [ ] **Step 3: Generate the checked-in semantic-map tree**

Run:

```bash
uv run python -m scripts.legacy_semantic_map.bootstrap
```

Expected: the minimal checked-in tree is created deterministically.

- [ ] **Step 4: Update the wiki maintenance lint checklist**

Add an explicit rule that:

- `docs/wiki-bi/_meta/legacy-semantic-map/` is excluded from durable-page reachability and template checks
- maintainers must instead verify that the subtree remains absent from `docs/wiki-bi/index.md` and that its `README.md` still states owner, archive trigger, and non-durable boundary

- [ ] **Step 5: Run both contract files**

Run:

```bash
uv run pytest tests/contracts/test_legacy_semantic_map_bootstrap.py tests/contracts/test_legacy_semantic_map_repo_docs.py -v
```

Expected: pass.

## Validation

Run:

```bash
uv sync --dev
uv run python -m scripts.legacy_semantic_map.bootstrap
uv run pytest tests/contracts/test_legacy_semantic_map_bootstrap.py tests/contracts/test_legacy_semantic_map_repo_docs.py -v
rg -n "legacy-semantic-map" docs/wiki-bi/index.md docs/wiki-bi/_meta/wiki-maintenance-lint-checklist.md docs/wiki-bi/_meta/legacy-semantic-map/README.md
git diff -- docs/wiki-bi/_meta/legacy-semantic-map docs/wiki-bi/_meta/wiki-maintenance-lint-checklist.md scripts/legacy_semantic_map tests/contracts pyproject.toml uv.lock
git status -sb
```

Expected:

- `PyYAML` is locked only as a dev/tooling dependency
- the bootstrap writer regenerates the same minimal tree deterministically
- `docs/wiki-bi/index.md` still does not catalog the semantic-map subtree
- the lint checklist explicitly excludes the subtree from durable-page expectations
- the checked-in `README.md` makes owner and archive trigger visible in-tree
- no runtime code under `src/work_data_hub_pro/` is touched

## Expected Outcome

After this plan is executed:

- the repository has a minimal semantic-map registry skeleton rather than a speculative full registry tree
- the semantic-map subtree is explicitly governed as a temporary internal discovery ledger
- later slices can add claims, compilation, and reporting on top of stable seed contracts instead of re-deciding the bootstrap boundary

# Phase 1: Legacy Capability Mapping & Parity Harness - Research

**Researched:** 2026-04-12  
**Domain:** Legacy-to-Pro capability mapping and parity-harness design for replay verification  
**Confidence:** MEDIUM

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
### Capability mapping model
- **D-01:** Use dual-layer mapping, with business capability as the primary key and stage/function chain as supporting traceability evidence.
- **D-02:** Each mapping row must include legacy behavior meaning, legacy owner/path, Pro owner/path, migration status, parity criticality, and ambiguity notes.

### Legacy coverage strategy
- **D-03:** Use `annuity_performance` as the Phase 1 deep sample slice.
- **D-04:** Register `annual_award` and `annual_loss` in the same matrix for breadth visibility, but do not deep-map them to equal depth in Phase 1.

### Parity comparison basis
- **D-05:** Adopt hybrid parity rule: final output must match, plus selective parity-critical intermediate checks.
- **D-06:** Required intermediate checkpoints for Phase 1 include intake/source recognition, canonical fact shape, identity resolution category, and publication payload key fields.

### Difference severity policy
- **D-07:** Use two severity tiers in Phase 1: `block` and `warn`.
- **D-08:** Any unclassified/new difference type defaults to `block` until explicitly categorized.
- **D-09:** `block` includes semantic output drift, key/publication-key drift, source recognition routing drift, non-adjudicable mismatches, and missing evidence.
- **D-10:** `warn` includes explainable bounded non-semantic differences that preserve final business semantics.

### First must-pass checkpoint
- **D-11:** First checkpoint is an offline report gate with human confirmation, not CI hard-fail.
- **D-12:** Required checkpoint outputs: mapping completeness status, baseline dataset identity, parity summary, mismatch severity table, and human decision log.

### Evidence and trace scope
- **D-13:** Fix minimum evidence set now: mapping matrix, baseline set, mismatch report, severity decision log.
- **D-14:** Defer full evidence directory standard to later phase after mismatch patterns stabilize.
- **D-15:** Even with minimum evidence, enforce stable identity fields now: domain, sample/batch id, baseline version, comparison run id, decision owner.

### Claude's Discretion
- Exact artifact serialization format (Markdown table vs CSV + Markdown summary) as long as required columns and identity fields are preserved.
- Naming conventions for intermediate local working files, provided canonical evidence outputs remain stable and traceable.

### Deferred Ideas (OUT OF SCOPE)
- Promote parity gate from offline human-confirmed to CI hard-fail only after mismatch semantics stabilize (target: Phase 2 alignment).
- Define full evidence directory taxonomy and retention/governance standard after Phase 1 mismatch observations are available.
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| MAP-01 | Map each legacy business processing capability to Pro target modules and status | Dual-layer matrix schema, ownership columns, and capability-first mapping protocol [VERIFIED: `.planning/phases/01-legacy-capability-mapping-parity-harness/01-CONTEXT.md`] |
| MAP-02 | Map critical source-recognition paths to Pro intake contracts and validation checks | Intake-path mapping template tied to `source_intake/*` services and intake/integration test anchors [VERIFIED: `.planning/codebase/ARCHITECTURE.md`, `tests/integration/test_*_intake.py`] |
| MAP-03 | Classify parity-critical legacy rules as keep/replace/retire-with-proof | Rule classification model tied to `CleansingManifest` + severity policy + adjudication case flow [VERIFIED: `src/work_data_hub_pro/capabilities/fact_processing/cleansing/manifest.py`, `src/work_data_hub_pro/governance/adjudication/service.py`] |
| PAR-01 | Define parity datasets and golden outputs for annuity performance, annual award, annual loss | Existing replay baseline asset layout and per-domain snapshot/fixture files under `reference/historical_replays/*` [VERIFIED: repository file tree grep] |
</phase_requirements>

## Project Constraints (from CLAUDE.md)

`CLAUDE.md` is not present in repository root, so no CLAUDE-specific directives apply in this phase research. [VERIFIED: filesystem check]

## Summary

Phase 1 planning should optimize for governance-grade artifact clarity, not implementation breadth: build one authoritative mapping system and one deterministic parity-harness contract that later phases can enforce and automate. [VERIFIED: `.planning/phases/01-legacy-capability-mapping-parity-harness/01-CONTEXT.md`, `.planning/ROADMAP.md`]

The codebase already has replay execution, parity comparison hooks, compatibility-case persistence, and baseline fixtures for all three scoped domains, so the highest leverage is to standardize artifact schema, mismatch taxonomy, and checkpoint workflow around those existing surfaces rather than introducing new runtime abstractions now. [VERIFIED: `src/work_data_hub_pro/apps/orchestration/replay/*.py`, `reference/historical_replays/*`, `tests/replay/*`]

Main planning risk is false confidence: the project has strong replay tests, but MAP-01/02/03 artifacts are mostly documentation/governance outputs and currently lack dedicated contract tests, so Phase 1 plan must include Wave-0 verification additions for artifact shape and identity fields. [VERIFIED: test inventory grep + requirements mapping]

**Primary recommendation:** Plan Phase 1 as an artifact-first slice with deterministic file schemas, strict `block|warn` severity defaults, and an offline human-confirmed checkpoint bound to existing replay evidence paths. [VERIFIED: Phase 1 decisions D-07..D-15]

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Python (via `uv run python`) | 3.12.11 | Runtime for mapping/parity scripts and tests | Required by project (`requires-python >=3.12`) and already operational in this environment [VERIFIED: `pyproject.toml`, `uv run python --version`] |
| pytest | 8.4.2 (project lock); latest 9.0.3 published 2026-04-07 | Deterministic contract/integration/replay assertions | Existing repo test harness is pytest-based and locked to `<9.0` for stability [VERIFIED: `pyproject.toml`, `uv.lock`, PyPI JSON] |
| openpyxl | 3.1.5 (latest published 2024-06-28) | Workbook intake for parity datasets | Existing intake + replay tests rely on `.xlsx` parsing via openpyxl [VERIFIED: `pyproject.toml`, `uv.lock`, `tests/replay/test_annuity_performance_slice.py`, PyPI JSON] |
| typer | 0.24.1 (latest published 2026-02-21) | CLI replay entrypoints used by parity runs | Existing CLI contract is Typer and already wired for all three replay domains [VERIFIED: `src/work_data_hub_pro/apps/etl_cli/main.py`, `uv.lock`, PyPI JSON] |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| uv | 0.8.14 | Environment and command runner | Use for all phase verification commands because bare `python` is unavailable on PATH [VERIFIED: `uv --version`, environment probe] |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| pytest 8.4.2 lockline | pytest 9.x immediately | New major line may add migration overhead during governance-heavy Phase 1; defer unless a required feature is missing [VERIFIED: `pyproject.toml`, PyPI JSON] |
| openpyxl row iteration | ad-hoc CSV export pre-processing | Adds data-shape drift risk and duplicates intake semantics already tested in repo [VERIFIED: existing intake/replay test flow] |

**Installation:**
```bash
uv sync --dev
```

**Version verification commands used:**
```bash
uv lock data: openpyxl=3.1.5, typer=0.24.1, pytest=8.4.2
Invoke-RestMethod https://pypi.org/pypi/<package>/json
```

## Architecture Patterns

### Recommended Project Structure
```text
.planning/phases/01-legacy-capability-mapping-parity-harness/
├── 01-CONTEXT.md                # locked decisions + phase boundary
├── 01-RESEARCH.md               # prescriptive stack/pattern findings
├── artifacts/
│   ├── capability-map.csv       # MAP-01/02 dual-layer mapping rows
│   ├── parity-baseline.json     # PAR-01 dataset and expected outputs index
│   ├── mismatch-report.json     # run summary + block/warn classification
│   └── decision-log.md          # human checkpoint decisions
└── schema/
    ├── capability-map.schema.md
    └── parity-baseline.schema.md
```
Structure above is recommended for this phase and compatible with `commit_docs=false` local planning mode. [VERIFIED: `.planning/config.json`, Phase 1 decisions D-13..D-15]

### Pattern 1: Dual-Layer Capability Mapping
**What:** Keep business capability as primary row identity and attach stage/function chain as traceability evidence. [VERIFIED: decision D-01]  
**When to use:** All MAP-01 and MAP-02 inventory rows. [VERIFIED: requirements]  
**Example:**
```csv
capability_id,domain,business_capability,legacy_owner_path,legacy_stage_chain,pro_owner_path,pro_stage_chain,migration_status,parity_criticality,ambiguity_notes
CAP-AP-INTAKE,annuity_performance,source_recognition,WorkDataHub/.../intake.py,discover->read->normalize,work_data_hub_pro/capabilities/source_intake/annuity_performance/service.py,source_intake,existing,block,
```

### Pattern 2: Hybrid Parity Checkpoint
**What:** Compare final outputs plus a narrow set of parity-critical intermediate checkpoints. [VERIFIED: decisions D-05, D-06]  
**When to use:** First must-pass offline checkpoint for Phase 1. [VERIFIED: decisions D-11, D-12]  
**Example:**
```json
{
  "run_id": "cmp-2026-04-12-001",
  "domain": "annuity_performance",
  "final_output_match": true,
  "intermediate_checks": {
    "source_recognition": "match",
    "canonical_fact_shape": "match",
    "identity_resolution_category": "warn",
    "publication_key_fields": "match"
  },
  "severity": "warn"
}
```

### Pattern 3: Compatibility-Case Escalation for Blocking Drift
**What:** Persist divergence as explicit compatibility cases with human review status. [VERIFIED: `AdjudicationService.create_case`]  
**When to use:** Any `block` severity mismatch or unresolved mismatch category. [VERIFIED: decisions D-08, D-09]  
**Example:**
```python
# Source: src/work_data_hub_pro/governance/adjudication/service.py
case = AdjudicationService(evidence_index).create_case(
    sample_locator=str(snapshot_path),
    legacy_result={"rows": expected_rows},
    pro_result={"rows": actual_rows},
    involved_anchor_row_nos=[2, 5],
    rationale="Monthly snapshot replay differs from accepted legacy baseline",
    affected_rule_version="annuity-performance-core:1",
)
```

### Anti-Patterns to Avoid
- Hard-coding release/config paths into phase artifacts instead of recording versioned identity fields (`domain`, `batch`, `baseline_version`, `run_id`, `decision_owner`). [VERIFIED: decisions D-15 + concerns on hard-coded paths]
- Treating unclassified mismatch types as non-blocking; Phase 1 explicitly requires default `block`. [VERIFIED: decision D-08]
- Expanding Phase 1 into full CI enforcement before mismatch semantics stabilize. [VERIFIED: deferred ideas + D-11]

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Workbook parser behavior | Custom XLSX parser | `openpyxl.load_workbook` + worksheet iteration APIs | Existing stack already uses openpyxl and has test coverage around workbook-based intake [VERIFIED: codebase + Context7 openpyxl docs] |
| Test diff rendering | Manual string diff logger | pytest assertions/introspection | pytest already gives structured mismatch diagnostics and node-id targeting for fast reruns [CITED: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/assert.md, https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/usage.md] |
| Mismatch case persistence | Ad-hoc JSON dump conventions | `AdjudicationService` + `CompatibilityCase` model | Existing governance flow already stores adjudication-ready cases consistently [VERIFIED: governance service/model code] |
| UUID generation semantics | Handcrafted IDs | `uuid4` pattern already used in replay/case services | Avoids collision-prone local ID logic [VERIFIED: replay/adjudication code] |

**Key insight:** Phase 1 is primarily about codifying existing reliable mechanisms, not inventing new ones; each custom utility increases parity-risk surface without improving requirement coverage. [VERIFIED: phase scope + current code capabilities]

## Common Pitfalls

### Pitfall 1: Scope Creep from Mapping into Refactor
**What goes wrong:** MAP artifacts silently turn into runtime refactor tasks. [VERIFIED: phase boundary text]  
**Why it happens:** Replay orchestration duplication tempts immediate extraction work. [VERIFIED: `.planning/codebase/CONCERNS.md`]  
**How to avoid:** Enforce artifact-only deliverables in Phase 1 and register refactor actions as later-phase mitigations. [VERIFIED: roadmap sequencing]  
**Warning signs:** PR/plan starts changing orchestrator internals rather than map/baseline/severity artifacts. [ASSUMED]

### Pitfall 2: Non-Deterministic Baseline Assets
**What goes wrong:** Baseline/golden outputs cannot be reproduced or compared consistently. [VERIFIED: PAR-01 intent]  
**Why it happens:** Missing identity fields and inconsistent file naming across runs. [VERIFIED: decision D-15]  
**How to avoid:** Require stable identity keys in every parity artifact from day one. [VERIFIED: decision D-15]  
**Warning signs:** Same sample yields multiple baseline IDs or non-traceable mismatch reports. [ASSUMED]

### Pitfall 3: Evidence Cannot Support Adjudication
**What goes wrong:** Mismatch discovered but not classifiable due missing trace lineage or missing case metadata. [VERIFIED: decision D-09 and existing adjudication shape]  
**Why it happens:** Evidence set is produced ad hoc without required minimum bundle. [VERIFIED: decision D-13]  
**How to avoid:** Gate checkpoint on presence of all four evidence artifacts before human review. [VERIFIED: decisions D-12, D-13]  
**Warning signs:** `compatibility_case` exists but owner/rationale/severity history is incomplete. [ASSUMED]

## Code Examples

Verified patterns from official sources and current code:

### Select One Test Quickly by Node ID
```bash
uv run pytest tests/replay/test_annuity_performance_slice.py::test_full_slice_replay_closes_chain_and_matches_legacy_snapshot -v
```
Source: pytest usage docs (node IDs). [CITED: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/usage.md]

### Deterministic Assertion Diagnostics
```python
def test_monthly_snapshot_rows(actual_rows, expected_rows):
    assert actual_rows == expected_rows
```
Source: pytest assert introspection behavior. [CITED: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/assert.md]

### Workbook Row Iteration with Values Only
```python
from openpyxl import load_workbook

wb = load_workbook(filename=workbook_path, read_only=True)
ws = wb["AnnuityPerformance"]
for row in ws.iter_rows(min_row=2, values_only=True):
    ...
wb.close()
```
Source: openpyxl docs (`load_workbook`, `iter_rows`, read-only mode). [CITED: https://openpyxl.readthedocs.io/en/stable/tutorial.html, https://openpyxl.readthedocs.io/en/stable/optimized.html, https://openpyxl.readthedocs.io/en/stable/api/openpyxl.worksheet.worksheet.html]

### Existing Parity-Case Escalation Hook
```python
if monthly_snapshot.rows != expected_snapshot:
    compatibility_case = AdjudicationService(evidence_index).create_case(...)
```
Source: current replay orchestrator. [VERIFIED: `src/work_data_hub_pro/apps/orchestration/replay/annuity_performance_slice.py`]

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Implicit hook-centric write consequences | Explicit publication + projection chain in replay flow | Rebuild baseline documents dated 2026-04-11 | Better traceability and phase-gated parity evidence [VERIFIED: architecture blueprint + replay code] |
| Broad domain migration assumptions | One deep slice + registered breadth | Phase 1 decisions finalized 2026-04-12 | Reduced risk and clearer acceptance boundary [VERIFIED: `01-CONTEXT.md`] |
| Unstructured mismatch handling | `CompatibilityCase` with persisted evidence and human review state | Current governance module in repo | Enables adjudication workflow instead of silent drift [VERIFIED: governance code] |

**Deprecated/outdated:**
- Treating legacy structure as architecture template is explicitly rejected; behavior parity is retained, architecture shape is rebuilt. [VERIFIED: architecture blueprint]

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | Warning signs listed under pitfalls are good early indicators in this team workflow | Common Pitfalls | Medium: may miss early detection signals |
| A2 | Current phase reviewers will accept explicit `artifacts/` + `schema/` subfolders under phase directory | Architecture Patterns | Low: can rename without semantic impact |
| A3 | V2/V3 ASVS controls are non-applicable for this specific offline parity-harness phase | Security Domain | Medium: might under-scope security checklist items |

## Open Questions (RESOLVED)

1. **Should Phase 1 keep pytest pinned `<9.0` even though 9.0.3 exists as of April 7, 2026?** **RESOLVED**
   - What we know: Project constraint is `pytest>=8.2,<9.0`, lock currently 8.4.2. [VERIFIED: `pyproject.toml`, `uv.lock`, PyPI JSON]
   - Resolution: Keep `<9.0` for Phase 1. No PAR/MAP Phase 1 task requires pytest 9-only features based on current plan scope and test architecture.

2. **Where should Phase 1 artifact schemas be enforced (test contract vs manual checklist)?** **RESOLVED**
   - What we know: Existing tests focus runtime behavior, not MAP artifact schema compliance. [VERIFIED: tests inventory]
   - Resolution: Enforce via automated contract tests (not manual checklist) in Phase 1 plans: `tests/contracts/test_phase1_mapping_artifacts.py` and `tests/contracts/test_phase1_parity_baseline_artifacts.py`.

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| `uv` | All run/test commands in this repo | ✓ | 0.8.14 | — |
| Python runtime (`uv run python`) | parity scripts/tests | ✓ | 3.12.11 | — |
| `python` on PATH | direct `python ...` commands | ✗ | — | Use `uv run python ...` |
| Legacy workspace `E:\Projects\WorkDataHub` | MAP-01 source ownership mapping | ✓ | — | — |
| Replay baseline assets under `reference/historical_replays` | PAR-01 baseline/golden definition | ✓ | existing 2026-03 fixtures/snapshots | — |

**Missing dependencies with no fallback:**
- None found.

**Missing dependencies with fallback:**
- `python` binary missing on PATH; use `uv run python` consistently.

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest 8.4.2 [VERIFIED: `uv run pytest --version`] |
| Config file | `pyproject.toml` (`[tool.pytest.ini_options]`) [VERIFIED: file contents] |
| Quick run command | `uv run pytest tests/replay/test_annuity_performance_slice.py -v` |
| Full suite command | `uv run pytest -v` |

### Phase Requirements → Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| MAP-01 | Capability inventory schema and ownership completeness | contract | `uv run pytest tests/contracts/test_phase1_mapping_artifacts.py::test_capability_map_schema -v` | ❌ Wave 0 |
| MAP-02 | Source-recognition mapping references explicit intake contracts/checks | contract+integration | `uv run pytest tests/contracts/test_phase1_mapping_artifacts.py::test_source_recognition_links -v` | ❌ Wave 0 |
| MAP-03 | Rule classification includes keep/replace/retire-with-proof and severity default behavior | contract | `uv run pytest tests/contracts/test_phase1_mapping_artifacts.py::test_rule_classification_matrix -v` | ❌ Wave 0 |
| PAR-01 | Domain parity datasets/golden outputs are defined and reproducible | contract+replay | `uv run pytest tests/contracts/test_annuity_performance_replay_assets.py tests/contracts/test_annual_award_replay_assets.py tests/contracts/test_annual_loss_replay_assets.py -v` | ✅ |

### Sampling Rate
- **Per task commit:** `uv run pytest tests/contracts/test_phase1_mapping_artifacts.py -v` (after Wave 0 file exists)
- **Per wave merge:** `uv run pytest tests/replay/test_annuity_performance_slice.py tests/contracts/test_annuity_performance_replay_assets.py tests/contracts/test_annual_award_replay_assets.py tests/contracts/test_annual_loss_replay_assets.py -v`
- **Phase gate:** `uv run pytest -v`

### Wave 0 Gaps
- [ ] `tests/contracts/test_phase1_mapping_artifacts.py` — MAP-01/02/03 artifact schema and required identity-field checks.
- [ ] Artifact fixtures under `.planning/phases/01-legacy-capability-mapping-parity-harness/artifacts/` to test deterministic parity bundle shape.
- [ ] Optional helper fixture in `tests/contracts/conftest.py` for phase-artifact path resolution if repeated across tests.

## Security Domain

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|-----------------|
| V2 Authentication | no | Not directly in scope for offline mapping/parity artifact generation in this phase [ASSUMED] |
| V3 Session Management | no | Not directly in scope for this phase’s local/offline harness flow [ASSUMED] |
| V4 Access Control | yes | Enforce restricted artifact/evidence path ownership and reviewer-only decision log updates [VERIFIED: phase evidence model + concerns on evidence exposure] |
| V5 Input Validation | yes | Intake contracts and workbook schema checks via integration/contract tests [VERIFIED: existing intake tests + concerns test gaps] |
| V6 Cryptography | yes | If evidence-at-rest protection is introduced, use established crypto libraries; do not hand-roll encryption/redaction logic [VERIFIED: `.planning/codebase/CONCERNS.md`] [ASSUMED: future control mechanism details] |

### Known Threat Patterns for this Stack

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| Workbook schema spoofing / malformed intake files | Tampering | Explicit sheet/header validation with failing contract tests before processing [VERIFIED: concerns + MAP-02 need] |
| Evidence artifact leakage of business identifiers | Information Disclosure | Add redaction policy and enforce minimum evidence schema with sanitized fields [VERIFIED: `.planning/codebase/CONCERNS.md`] |
| Unclassified mismatch accepted accidentally | Tampering / Repudiation | Default unclassified mismatches to `block` and require human decision log entries [VERIFIED: decisions D-08, D-12] |

STRIDE category mapping referenced from Microsoft threat-model definitions. [CITED: https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool-threats]

## Sources

### Primary (HIGH confidence)
- `.planning/phases/01-legacy-capability-mapping-parity-harness/01-CONTEXT.md` - locked Phase 1 decisions and scope.
- `.planning/REQUIREMENTS.md` - MAP-01/02/03 and PAR-01 definitions.
- `.planning/ROADMAP.md` - phase success criteria and dependencies.
- `.planning/codebase/ARCHITECTURE.md` - current boundaries and replay flow.
- `.planning/codebase/CONCERNS.md` - known pitfalls/security/performance/test gaps.
- `src/work_data_hub_pro/apps/orchestration/replay/annuity_performance_slice.py` - current parity comparison and case escalation flow.
- `src/work_data_hub_pro/governance/adjudication/service.py` and `src/work_data_hub_pro/governance/compatibility/models.py` - mismatch adjudication model.
- `pyproject.toml`, `uv.lock` - dependency and test framework reality.

### Secondary (MEDIUM confidence)
- pytest docs on usage and assertions: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/usage.md, https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/assert.md
- openpyxl docs on workbook loading and row iteration: https://openpyxl.readthedocs.io/en/stable/tutorial.html, https://openpyxl.readthedocs.io/en/stable/optimized.html, https://openpyxl.readthedocs.io/en/stable/api/openpyxl.worksheet.worksheet.html
- OWASP ASVS repository (latest stable release statement): https://github.com/OWASP/ASVS/tree/v5.0.0

### Tertiary (LOW confidence)
- None.

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - directly verified from `pyproject.toml`, `uv.lock`, local runtime probes, and package registry lookups.
- Architecture: HIGH - directly verified from current code + committed architecture docs.
- Pitfalls: MEDIUM - high-confidence codebase concerns plus some workflow warning-sign assumptions.

**Research date:** 2026-04-12  
**Valid until:** 2026-05-12 (stable phase-domain assumptions; re-check dependency versions and security references before execution if delayed)

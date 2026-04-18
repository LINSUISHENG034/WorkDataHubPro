# WorkDataHubPro Semantic Map Agent Governance Reframe Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the active CT-017 follow-on with CT-018 and add a compatibility-preserving agent-governance front door for semantic-map discovery without reopening closed waves or breaking accepted semantic-map contracts.

**Architecture:** Keep the existing `slice-semantic-map-integration` registry, claim, compiler, manifest, and authoritative report contracts intact. Add CT-018 as a successor-wave adapter: workers still emit standard `ClaimArtifact` files, the main thread remains the only canonical writer, and new maturity/readiness views are additive over the current semantic/reporting baseline.

**Tech Stack:** Python, PyYAML, pytest, Markdown governance specs, semantic-map registry files under `docs/wiki-bi/_meta/legacy-semantic-map/`

---

## File Structure

### Governance and plan admission
- Modify: `docs/superpowers/specs/2026-04-11-workdatahubpro-refactor-program.md`
- Modify: `docs/superpowers/specs/2026-04-11-workdatahubpro-first-wave-legacy-coverage-matrix.md`
- Modify: `docs/wiki-bi/_meta/legacy-semantic-map/waves/index.yaml`
- Create: `docs/superpowers/plans/2026-04-18-workdatahubpro-semantic-map-agent-governance-reframe.md`

### Wave-guard and orchestration code
- Create: `scripts/legacy_semantic_map/waves.py`
- Create: `scripts/legacy_semantic_map/orchestrate_wave.py`
- Modify: `scripts/legacy_semantic_map/claims.py`
- Modify: `scripts/legacy_semantic_map/compiler.py`
- Modify: `scripts/legacy_semantic_map/reporting.py`
- Modify: `scripts/legacy_semantic_map/pilot.py`

### Additive semantic/reporting surfaces
- Modify: `scripts/legacy_semantic_map/models.py`
- Modify: `docs/wiki-bi/_meta/legacy-semantic-map/reports/current/coverage-status.json` via generated output only
- Modify: `docs/wiki-bi/_meta/legacy-semantic-map/reports/current/integrity-status.json` via generated output only
- Modify: `docs/wiki-bi/_meta/legacy-semantic-map/reports/waves/<wave_id>/coverage-status.json` via generated output only
- Modify: `docs/wiki-bi/_meta/legacy-semantic-map/reports/waves/<wave_id>/integrity-status.json` via generated output only
- Create via generated output: `docs/wiki-bi/_meta/legacy-semantic-map/reports/waves/wave-2026-04-17-semantic-governance-reframe/semantic-discovery-status.json`
- Create via generated output: `docs/wiki-bi/_meta/legacy-semantic-map/reports/waves/wave-2026-04-17-semantic-governance-reframe/semantic-readiness-status.json`
- Create via generated output: `docs/wiki-bi/_meta/legacy-semantic-map/reports/waves/wave-2026-04-17-semantic-governance-reframe/semantic-discovery-summary.md`
- Create via generated output: `docs/wiki-bi/_meta/legacy-semantic-map/reports/waves/wave-2026-04-17-semantic-governance-reframe/semantic-readiness-summary.md`

### Tests
- Create: `tests/contracts/test_legacy_semantic_map_ct018_governance_supersession.py`
- Create: `tests/contracts/test_legacy_semantic_map_wave_successor_open.py`
- Create: `tests/contracts/test_legacy_semantic_map_wave_guarding.py`
- Create: `tests/contracts/test_legacy_semantic_map_orchestrate_wave_adapter.py`
- Create: `tests/contracts/test_legacy_semantic_map_semantic_maturity_additive_schema.py`
- Create: `tests/contracts/test_legacy_semantic_map_semantic_auxiliary_views.py`
- Create: `tests/integration/test_legacy_semantic_map_orchestrate_successor_wave.py`
- Create: `tests/integration/test_legacy_semantic_map_closed_wave_compile_guard.py`
- Create: `tests/integration/test_legacy_semantic_map_trigger_idempotency.py`
- Create: `tests/integration/test_legacy_semantic_map_semantic_governance_reframe_flow.py`
- Reuse as regression guard:
  - `tests/contracts/test_legacy_semantic_map_claim_workflow.py`
  - `tests/contracts/test_legacy_semantic_map_canonical_compiler.py`
  - `tests/contracts/test_legacy_semantic_map_reporting.py`
  - `tests/contracts/test_legacy_semantic_map_semantic_compiler.py`
  - `tests/contracts/test_legacy_semantic_map_semantic_reporting.py`
  - `tests/contracts/test_legacy_semantic_map_repo_docs.py`
  - `tests/contracts/test_legacy_semantic_map_wave_closeout.py`
  - `tests/integration/test_legacy_semantic_map_customer_status_semantic_pilot.py`
  - `tests/integration/test_legacy_semantic_map_reporting_pipeline.py`
  - `tests/integration/test_legacy_semantic_map_first_wave_pilot_flow.py`

---

### Task 1: Admit CT-018 and open the successor wave

**Files:**
- Modify: `docs/superpowers/specs/2026-04-11-workdatahubpro-refactor-program.md`
- Modify: `docs/superpowers/specs/2026-04-11-workdatahubpro-first-wave-legacy-coverage-matrix.md`
- Modify: `docs/wiki-bi/_meta/legacy-semantic-map/waves/index.yaml`
- Test: `tests/contracts/test_legacy_semantic_map_ct018_governance_supersession.py`
- Test: `tests/contracts/test_legacy_semantic_map_wave_successor_open.py`

- [ ] **Step 1: Write failing governance tests**

```python
def test_ct018_becomes_only_active_semantic_map_follow_on() -> None:
    program_text = Path(
        "docs/superpowers/specs/2026-04-11-workdatahubpro-refactor-program.md"
    ).read_text(encoding="utf-8")
    matrix_text = Path(
        "docs/superpowers/specs/2026-04-11-workdatahubpro-first-wave-legacy-coverage-matrix.md"
    ).read_text(encoding="utf-8")

    assert "CT-018" in program_text
    assert "CT-017 is superseded by CT-018" in program_text
    assert "| CT-017 |" in matrix_text
    assert "| `retired` |" in matrix_text
    assert "| CT-018 |" in matrix_text


def test_successor_wave_is_open_and_active() -> None:
    payload = yaml.safe_load(
        Path(
            "docs/wiki-bi/_meta/legacy-semantic-map/waves/index.yaml"
        ).read_text(encoding="utf-8")
    )

    assert payload["active_wave_id"] == "wave-2026-04-17-semantic-governance-reframe"
    successor = next(
        item
        for item in payload["waves"]
        if item["wave_id"] == "wave-2026-04-17-semantic-governance-reframe"
    )
    assert successor["status"] == "active"
    assert successor["closed_at"] is None
```

- [ ] **Step 2: Run tests to confirm current docs fail**

Run:

```powershell
uv run pytest tests/contracts/test_legacy_semantic_map_ct018_governance_supersession.py -v
uv run pytest tests/contracts/test_legacy_semantic_map_wave_successor_open.py -v
```

Expected:
- both tests fail because `CT-018` is absent
- `active_wave_id` still points to `wave-2026-04-17-first-wave-pilot`

- [ ] **Step 3: Update refactor-program and coverage-matrix governance text**

Use these exact textual outcomes:

```markdown
Refactor program cross-cutting row:
| semantic-map agent-governance reframe (`CT-018`) | ... | planned | execute `docs/superpowers/plans/2026-04-18-workdatahubpro-semantic-map-agent-governance-reframe.md` on `slice/semantic-map-integration` |

Append sentence:
Historical CT-017 outputs remain retained for audit context and are not reopened.

Coverage matrix CT-017 row:
Status = `retired`
Retirement Decision = `superseded by CT-018 semantic-governance reframe; retained as historical prior-wave context only`

Coverage matrix CT-018 row:
Status = `planned`
Owning Spec / Plan = `docs/superpowers/plans/2026-04-18-workdatahubpro-semantic-map-agent-governance-reframe.md`
Notes = `active implementation occurs only on successor wave wave-2026-04-17-semantic-governance-reframe`
```

- [ ] **Step 4: Open the successor wave without mutating closed-wave records**

Add this wave block and set it active:

```yaml
active_wave_id: wave-2026-04-17-semantic-governance-reframe
waves:
  - wave_id: wave-2026-04-17-semantic-governance-reframe
    title: Semantic governance reframe
    status: active
    wave_ordinal: 4
    opened_at: '2026-04-17'
    seeded_entry_surfaces: []
    seeded_high_priority_source_families: []
    admitted_subsystems: []
    durable_wiki_targets_accepted: false
    findings_disposition_complete: false
    depends_on_active_wave_working_state: false
    closed_at: null
```

- [ ] **Step 5: Re-run the governance tests**

Run:

```powershell
uv run pytest tests/contracts/test_legacy_semantic_map_ct018_governance_supersession.py -v
uv run pytest tests/contracts/test_legacy_semantic_map_wave_successor_open.py -v
```

Expected:
- PASS

- [ ] **Step 6: Commit the governance admission**

```powershell
git add docs/superpowers/specs/2026-04-11-workdatahubpro-refactor-program.md docs/superpowers/specs/2026-04-11-workdatahubpro-first-wave-legacy-coverage-matrix.md docs/wiki-bi/_meta/legacy-semantic-map/waves/index.yaml tests/contracts/test_legacy_semantic_map_ct018_governance_supersession.py tests/contracts/test_legacy_semantic_map_wave_successor_open.py
git commit -m "docs(semantic-map): admit ct-018 successor-wave reframe"
```

---

### Task 2: Centralize active-wave and single-writer guards

**Files:**
- Create: `scripts/legacy_semantic_map/waves.py`
- Modify: `scripts/legacy_semantic_map/claims.py`
- Modify: `scripts/legacy_semantic_map/compiler.py`
- Modify: `scripts/legacy_semantic_map/reporting.py`
- Modify: `scripts/legacy_semantic_map/pilot.py`
- Test: `tests/contracts/test_legacy_semantic_map_wave_guarding.py`

- [ ] **Step 1: Write failing guard tests for each entrypoint**

```python
def test_write_claim_artifact_rejects_closed_or_non_active_wave(tmp_path: Path) -> None:
    registry_root = seeded_registry(tmp_path, active_wave_id="wave-open")
    closed_claim = build_claim(wave_id="wave-closed")

    with pytest.raises(ValueError, match="active open wave"):
        write_claim_artifact(registry_root, closed_claim)


def test_compile_claim_artifacts_rejects_closed_wave_inputs(tmp_path: Path) -> None:
    registry_root, closed_claim_path = seeded_closed_wave_claim(tmp_path)

    with pytest.raises(ValueError, match="closed or non-active wave"):
        compile_claim_artifacts(registry_root, [closed_claim_path])


def test_generate_reports_rejects_authoritative_write_for_closed_wave(tmp_path: Path) -> None:
    registry_root = seeded_registry(tmp_path, active_wave_id="wave-open")

    with pytest.raises(ValueError, match="authoritative report write"):
        generate_reports(registry_root, wave_id="wave-closed")


def test_pilot_uses_same_wave_guards(tmp_path: Path) -> None:
    registry_root = seeded_registry(tmp_path, active_wave_id="wave-open")

    with pytest.raises(ValueError, match="closed or non-active wave"):
        run_first_wave_pilot(registry_root, wave_id="wave-closed")
```

- [ ] **Step 2: Run the new guard test file**

Run:

```powershell
uv run pytest tests/contracts/test_legacy_semantic_map_wave_guarding.py -v
```

Expected:
- FAIL because no shared wave guard exists yet

- [ ] **Step 3: Add a shared wave helper module**

Create `scripts/legacy_semantic_map/waves.py` with this core API:

```python
from __future__ import annotations

from pathlib import Path
import yaml


def load_waves_index(registry_root: Path) -> dict[str, object]:
    return yaml.safe_load((registry_root / "waves" / "index.yaml").read_text(encoding="utf-8"))


def require_active_open_wave(registry_root: Path, wave_id: str) -> dict[str, object]:
    payload = load_waves_index(registry_root)
    active_wave_id = payload["active_wave_id"]
    waves = {item["wave_id"]: item for item in payload["waves"]}
    if wave_id != active_wave_id:
        raise ValueError(f"Operation requires the active open wave; got {wave_id}, active is {active_wave_id}")
    wave = waves[wave_id]
    if wave["status"] != "active" or wave.get("closed_at"):
        raise ValueError(f"Operation requires an active open wave; got {wave_id}")
    return wave


def allow_audit_wave_read(registry_root: Path, wave_id: str) -> dict[str, object]:
    payload = load_waves_index(registry_root)
    waves = {item["wave_id"]: item for item in payload["waves"]}
    return waves[wave_id]
```

- [ ] **Step 4: Harden all write entrypoints with the shared helper**

Apply these exact guard rules:

```python
# claims.py
def write_claim_artifact(registry_root: Path, claim: ClaimArtifact) -> Path:
    require_active_open_wave(registry_root, claim.wave_id)
    ...

# compiler.py
def compile_claim_artifacts(registry_root: Path, claim_paths: Sequence[Path]) -> CompilationResult:
    ...
    for claim in claims:
        require_active_open_wave(registry_root, claim.wave_id)
    ...

# reporting.py
def generate_reports(registry_root: Path, wave_id: str | None = None) -> ReportGenerationResult:
    target_wave_id = wave_id or active_wave_id
    if target_wave_id == active_wave_id:
        require_active_open_wave(registry_root, target_wave_id)
    else:
        allow_audit_wave_read(registry_root, target_wave_id)
    ...

# pilot.py
def run_first_wave_pilot(...):
    require_active_open_wave(registry_root, wave_id)
    ...
```

- [ ] **Step 5: Re-run the guard tests and regression tests**

Run:

```powershell
uv run pytest tests/contracts/test_legacy_semantic_map_wave_guarding.py -v
uv run pytest tests/contracts/test_legacy_semantic_map_claim_workflow.py -v
uv run pytest tests/contracts/test_legacy_semantic_map_reporting.py -v
uv run pytest tests/contracts/test_legacy_semantic_map_wave_closeout.py -v
```

Expected:
- PASS
- historical per-wave reporting tests still pass because closed waves remain readable for audit, not writable as authoritative current outputs

- [ ] **Step 6: Commit the guard layer**

```powershell
git add scripts/legacy_semantic_map/waves.py scripts/legacy_semantic_map/claims.py scripts/legacy_semantic_map/compiler.py scripts/legacy_semantic_map/reporting.py scripts/legacy_semantic_map/pilot.py tests/contracts/test_legacy_semantic_map_wave_guarding.py
git commit -m "feat(semantic-map): enforce active-wave write guards"
```

---

### Task 3: Add the orchestration adapter without changing accepted claim contracts

**Files:**
- Create: `scripts/legacy_semantic_map/orchestrate_wave.py`
- Modify: `scripts/legacy_semantic_map/claims.py`
- Test: `tests/contracts/test_legacy_semantic_map_orchestrate_wave_adapter.py`
- Test: `tests/integration/test_legacy_semantic_map_orchestrate_successor_wave.py`
- Test: `tests/integration/test_legacy_semantic_map_trigger_idempotency.py`

- [ ] **Step 1: Write failing adapter contract tests**

```python
def test_orchestrate_wave_writes_only_standard_claim_scopes(tmp_path: Path) -> None:
    result = run_orchestrator(tmp_path)
    claim_paths = sorted(result["claim_paths"])
    assert all("/execution/" in path or "/subsystems/" in path or "/objects/" in path or "/semantic/" in path for path in claim_paths)


def test_orchestrate_wave_is_idempotent_by_trigger_id(tmp_path: Path) -> None:
    first = run_orchestrator(tmp_path, trigger_id="trigger-001")
    second = run_orchestrator(tmp_path, trigger_id="trigger-001")
    assert first["compiled_claim_ids"] == second["compiled_claim_ids"]
    assert first["generated_canonical_files"] == second["generated_canonical_files"]
```

- [ ] **Step 2: Run the new adapter tests**

Run:

```powershell
uv run pytest tests/contracts/test_legacy_semantic_map_orchestrate_wave_adapter.py -v
uv run pytest tests/integration/test_legacy_semantic_map_orchestrate_successor_wave.py -v
uv run pytest tests/integration/test_legacy_semantic_map_trigger_idempotency.py -v
```

Expected:
- FAIL because `orchestrate_wave.py` does not exist yet

- [ ] **Step 3: Implement the adapter front door**

Create `scripts/legacy_semantic_map/orchestrate_wave.py` around the existing pipeline:

```python
from __future__ import annotations

import argparse
import json
from pathlib import Path

from .claims import write_claim_artifact
from .compiler import compile_claim_artifacts
from .reporting import generate_reports
from .waves import require_active_open_wave


def orchestrate_wave(registry_root: Path, wave_id: str) -> dict[str, object]:
    require_active_open_wave(registry_root, wave_id)
    trigger_id = "trigger-semantic-governance-reframe"
    accepted_claim_paths = []
    for claim in build_successor_wave_claims(wave_id):
        accepted_claim_paths.append(write_claim_artifact(registry_root, claim))
    compilation = compile_claim_artifacts(registry_root, accepted_claim_paths)
    reports = generate_reports(registry_root, wave_id=wave_id)
    return {
        "wave_id": wave_id,
        "claim_paths": [path.as_posix() for path in accepted_claim_paths],
        "compiled_claim_ids": compilation.compiled_claim_ids,
        "generated_canonical_files": compilation.written_files,
        "coverage_report": reports.wave_coverage_report.as_posix(),
        "integrity_report": reports.wave_integrity_report.as_posix(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry-root", type=Path, required=True)
    parser.add_argument("--wave-id", required=True)
    args = parser.parse_args()
    print(json.dumps(orchestrate_wave(args.registry_root.resolve(), args.wave_id), indent=2))
```

- [ ] **Step 4: Keep orchestration metadata additive**

Extend `ClaimArtifact` with optional fields only:

```python
@dataclass(frozen=True)
class ClaimArtifact:
    ...
    trigger_id: str | None = None
    orchestration_iteration: int | None = None
```

Do not add new `claim_scope` directories.

- [ ] **Step 5: Re-run adapter tests**

Run:

```powershell
uv run pytest tests/contracts/test_legacy_semantic_map_orchestrate_wave_adapter.py -v
uv run pytest tests/integration/test_legacy_semantic_map_orchestrate_successor_wave.py -v
uv run pytest tests/integration/test_legacy_semantic_map_trigger_idempotency.py -v
```

Expected:
- PASS

- [ ] **Step 6: Commit the adapter**

```powershell
git add scripts/legacy_semantic_map/orchestrate_wave.py scripts/legacy_semantic_map/claims.py tests/contracts/test_legacy_semantic_map_orchestrate_wave_adapter.py tests/integration/test_legacy_semantic_map_orchestrate_successor_wave.py tests/integration/test_legacy_semantic_map_trigger_idempotency.py
git commit -m "feat(semantic-map): add successor-wave orchestration adapter"
```

---

### Task 4: Add semantic maturity and auxiliary readiness views additively

**Files:**
- Modify: `scripts/legacy_semantic_map/models.py`
- Modify: `scripts/legacy_semantic_map/compiler.py`
- Modify: `scripts/legacy_semantic_map/reporting.py`
- Test: `tests/contracts/test_legacy_semantic_map_semantic_maturity_additive_schema.py`
- Test: `tests/contracts/test_legacy_semantic_map_semantic_auxiliary_views.py`
- Test: `tests/integration/test_legacy_semantic_map_semantic_governance_reframe_flow.py`

- [ ] **Step 1: Write failing additive-schema tests**

```python
def test_compiled_semantic_nodes_keep_existing_fields_and_add_maturity_fields(tmp_path: Path) -> None:
    payload = compile_semantic_fixture(tmp_path)
    assert "primary_semantic_sources" in payload
    assert "semantic_authority" in payload
    assert "durable_target_pages" in payload
    assert payload["semantic_maturity_level"] in {
        "observed",
        "inferred",
        "contested",
        "consumption-candidate",
    }
    assert payload["compiled_from_wave_id"] == "wave-2026-04-17-semantic-governance-reframe"


def test_auxiliary_views_do_not_replace_authoritative_reports(tmp_path: Path) -> None:
    reports = run_successor_wave_reporting(tmp_path)
    assert reports["coverage_status_path"].endswith("coverage-status.json")
    assert reports["integrity_status_path"].endswith("integrity-status.json")
    assert reports["semantic_discovery_status_path"].endswith("semantic-discovery-status.json")
    assert reports["semantic_readiness_status_path"].endswith("semantic-readiness-status.json")
```

- [ ] **Step 2: Run the new schema/view tests**

Run:

```powershell
uv run pytest tests/contracts/test_legacy_semantic_map_semantic_maturity_additive_schema.py -v
uv run pytest tests/contracts/test_legacy_semantic_map_semantic_auxiliary_views.py -v
```

Expected:
- FAIL because the new additive fields and files do not exist yet

- [ ] **Step 3: Add additive semantic fields in compiler output**

In the semantic payload inside `compile_claim_artifacts()`, keep the current fields and append:

```python
payload = {
    ...
    "semantic_maturity_level": "observed",
    "discovery_view_status": "sufficient",
    "consumption_readiness_status": "reviewable",
    "readiness_notes": [],
    "compiled_from_wave_id": claim.wave_id,
    "compiled_at": claim.submitted_at,
}
```

Use this promotion rule:
- `observed` when only direct evidence exists
- `inferred` when multiple claim sources synthesize a conclusion
- `contested` when open questions or non-equivalence conflicts remain
- `consumption-candidate` when durable target pages exist and `blocked_by` is empty

- [ ] **Step 4: Generate additive auxiliary views from authoritative data**

Add to `generate_reports()`:

```python
semantic_discovery_payload = {
    "wave_id": target_wave_id,
    "discovery_view_status": coverage_payload["wave_status"],
    "semantic_maturity_counts": maturity_counts,
    "contested_semantic_ids": contested_semantic_ids,
}

semantic_readiness_payload = {
    "wave_id": target_wave_id,
    "handoff_ready_semantic_ids": handoff_ready_ids,
    "blocked_semantic_ids": blocked_semantic_ids,
    "durable_target_page_count": durable_target_page_count,
}
```

Write them under:

```python
registry_root / "reports" / "waves" / target_wave_id / "semantic-discovery-status.json"
registry_root / "reports" / "waves" / target_wave_id / "semantic-readiness-status.json"
registry_root / "reports" / "waves" / target_wave_id / "semantic-discovery-summary.md"
registry_root / "reports" / "waves" / target_wave_id / "semantic-readiness-summary.md"
```

Do **not** replace `coverage-status.json` or `integrity-status.json`.

- [ ] **Step 5: Re-run semantic schema and reporting regressions**

Run:

```powershell
uv run pytest tests/contracts/test_legacy_semantic_map_semantic_maturity_additive_schema.py -v
uv run pytest tests/contracts/test_legacy_semantic_map_semantic_auxiliary_views.py -v
uv run pytest tests/contracts/test_legacy_semantic_map_semantic_compiler.py -v
uv run pytest tests/contracts/test_legacy_semantic_map_semantic_reporting.py -v
```

Expected:
- PASS

- [ ] **Step 6: Commit the additive maturity/reporting work**

```powershell
git add scripts/legacy_semantic_map/models.py scripts/legacy_semantic_map/compiler.py scripts/legacy_semantic_map/reporting.py tests/contracts/test_legacy_semantic_map_semantic_maturity_additive_schema.py tests/contracts/test_legacy_semantic_map_semantic_auxiliary_views.py tests/integration/test_legacy_semantic_map_semantic_governance_reframe_flow.py
git commit -m "feat(semantic-map): add additive maturity and readiness views"
```

---

### Task 5: Run the successor-wave verification flow

**Files:**
- Test: `tests/integration/test_legacy_semantic_map_closed_wave_compile_guard.py`
- Test: `tests/integration/test_legacy_semantic_map_semantic_governance_reframe_flow.py`

- [ ] **Step 1: Add the closed-wave and end-to-end verification tests**

```python
def test_closed_wave_compile_guard_rejects_historical_write(tmp_path: Path) -> None:
    registry_root = seeded_registry_with_closed_wave(tmp_path)
    with pytest.raises(ValueError, match="active open wave"):
        run_first_wave_pilot(registry_root, wave_id="wave-2026-04-17-customer-status-semantic-pilot")


def test_semantic_governance_reframe_flow_generates_additive_outputs(tmp_path: Path) -> None:
    registry_root = seeded_registry_with_successor_wave(tmp_path)
    payload = orchestrate_wave(registry_root, "wave-2026-04-17-semantic-governance-reframe")
    assert payload["wave_id"] == "wave-2026-04-17-semantic-governance-reframe"
    assert any(path.endswith("coverage-status.json") for path in payload.values() if isinstance(path, str))
    assert (registry_root / "reports" / "waves" / "wave-2026-04-17-semantic-governance-reframe" / "semantic-readiness-status.json").exists()
```

- [ ] **Step 2: Run the targeted regression stack**

Run:

```powershell
uv run pytest tests/contracts/test_legacy_semantic_map_claim_workflow.py -v
uv run pytest tests/contracts/test_legacy_semantic_map_canonical_compiler.py -v
uv run pytest tests/contracts/test_legacy_semantic_map_reporting.py -v
uv run pytest tests/contracts/test_legacy_semantic_map_semantic_compiler.py -v
uv run pytest tests/contracts/test_legacy_semantic_map_semantic_reporting.py -v
uv run pytest tests/contracts/test_legacy_semantic_map_repo_docs.py -v
uv run pytest tests/contracts/test_legacy_semantic_map_wave_closeout.py -v
uv run pytest tests/contracts/test_legacy_semantic_map_ct018_governance_supersession.py -v
uv run pytest tests/contracts/test_legacy_semantic_map_wave_successor_open.py -v
uv run pytest tests/contracts/test_legacy_semantic_map_wave_guarding.py -v
uv run pytest tests/contracts/test_legacy_semantic_map_orchestrate_wave_adapter.py -v
uv run pytest tests/contracts/test_legacy_semantic_map_semantic_maturity_additive_schema.py -v
uv run pytest tests/contracts/test_legacy_semantic_map_semantic_auxiliary_views.py -v
```

Expected:
- PASS

- [ ] **Step 3: Run the integration stack**

Run:

```powershell
uv run pytest tests/integration/test_legacy_semantic_map_customer_status_semantic_pilot.py -v
uv run pytest tests/integration/test_legacy_semantic_map_reporting_pipeline.py -v
uv run pytest tests/integration/test_legacy_semantic_map_first_wave_pilot_flow.py -v
uv run pytest tests/integration/test_legacy_semantic_map_orchestrate_successor_wave.py -v
uv run pytest tests/integration/test_legacy_semantic_map_closed_wave_compile_guard.py -v
uv run pytest tests/integration/test_legacy_semantic_map_trigger_idempotency.py -v
uv run pytest tests/integration/test_legacy_semantic_map_semantic_governance_reframe_flow.py -v
```

Expected:
- PASS

- [ ] **Step 4: Execute the successor-wave front door and compatibility rerun**

Run:

```powershell
uv run python -m scripts.legacy_semantic_map.orchestrate_wave --registry-root docs/wiki-bi/_meta/legacy-semantic-map --wave-id wave-2026-04-17-semantic-governance-reframe
uv run python -m scripts.legacy_semantic_map.pilot --registry-root docs/wiki-bi/_meta/legacy-semantic-map --wave-id wave-2026-04-17-semantic-governance-reframe
```

Expected:
- the orchestrator emits standard claim artifacts only
- authoritative `coverage-status.json` and `integrity-status.json` remain present
- additive semantic discovery/readiness views are created under the successor-wave report directory

- [ ] **Step 5: Run the full suite**

Run:

```powershell
uv run pytest -v
```

Expected:
- PASS

- [ ] **Step 6: Commit the final verification pass**

```powershell
git add tests/integration/test_legacy_semantic_map_closed_wave_compile_guard.py tests/integration/test_legacy_semantic_map_semantic_governance_reframe_flow.py
git commit -m "test(semantic-map): verify ct-018 successor-wave flow"
```

---

## Self-Review

### 1. Spec coverage
- Deep-interview requirement to reframe the slice into agent-driven governance: covered by Tasks 1, 3, and 4.
- Preserve semantic-map boundary and avoid direct `docs/wiki-bi` mutation: covered by Tasks 2 and 3.
- Keep closed waves immutable and use successor-wave-only execution: covered by Tasks 1, 2, and 5.
- Preserve accepted compiler/report/manifest contracts and make changes additive: covered by Tasks 3 and 4.
- Separate discovery coverage from consumption readiness: covered by Task 4.
- Make single-writer enforcement explicit across entrypoints: covered by Task 2.

### 2. Placeholder scan
- No `TBD`, `TODO`, or unresolved “later” steps remain.
- All commands reference exact files or exact new files.
- All new surfaces are named concretely.

### 3. Type consistency
- Successor wave ID is consistently `wave-2026-04-17-semantic-governance-reframe`.
- Active follow-on slice is consistently `CT-018`.
- Additive semantic field names are consistently:
  - `semantic_maturity_level`
  - `discovery_view_status`
  - `consumption_readiness_status`
  - `readiness_notes`
  - `compiled_from_wave_id`
  - `compiled_at`

---

Plan complete and saved to `docs/superpowers/plans/2026-04-18-workdatahubpro-semantic-map-agent-governance-reframe.md`.

# WorkDataHubPro Legacy Semantic Map Claim Artifact Creation Implementation Plan

> **Status:** Proposed

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add governed, wave-local claim artifacts so agents can write semantic-map discoveries without touching canonical registry files directly.

**Architecture:** Treat this slice as `18.2.1 Plan A: Claim Artifact Creation` only. The slice should define the claim artifact schema, add a deterministic claim writer under `scripts/legacy_semantic_map/`, and extend the bootstrap tree so the active wave has checked-in claim directories and visible ownership rules. It must not yet compile claims into canonical files, triage candidates, or generate integrity / coverage reports.

**Tech Stack:** Python 3.12, `uv`, `pytest`, `PyYAML`, JSON, YAML, Markdown

---

## Scope Check

This plan covers only `18.2.1 Plan A: Claim Artifact Creation` from `docs/superpowers/specs/2026-04-16-workdatahub-legacy-semantic-map-design.md`.

This plan does cover:

- claim artifact schema and deterministic file naming
- claim scope to directory mapping under `claims/<wave_id>/`
- writer-side boundary checks that prevent canonical registry writes
- bootstrap support for checked-in claim directories under the active wave
- checked-in README language that makes the claim write boundary explicit

This plan does not cover:

- canonical compilation from claims into `execution/paths/`, `subsystems/`, `objects/`, `edges/`, or `candidates/`
- candidate triage workflow
- manifest regeneration beyond retaining canonical seed sources
- integrity or coverage report generation
- wave closeout or claim immutability enforcement after acceptance

Those belong to later implementation plans, especially `18.2.2 Plan B: Canonical Compilation` and `Slice 3: Reporting And Wave Closure`.

## Claim Workflow Boundary

This slice should introduce only the minimum machinery required to make claim artifacts real and safe:

- a typed claim artifact schema for task-local discoveries
- a deterministic writer that always writes under `claims/<wave_id>/<scope>/`
- registered-wave checks so claims cannot be written to ad hoc wave folders
- checked-in `.gitkeep` claim directories for the active wave
- visible README guidance that distributed agents may write claims, but canonical registry files remain main-thread-managed

This slice should not yet:

- create canonical `execution/paths/*.yaml`
- create canonical subsystem or object YAML files
- create `edges/`, `candidates/`, or `reports/`
- decide how accepted claims are merged
- decide compiler conflict resolution rules

If a behavior would require choosing how claims alter canonical facts, it belongs to the canonical compiler plan instead of this one.

## Proposed File Structure

### Files To Create

- `scripts/legacy_semantic_map/claims.py`
- `tests/contracts/test_legacy_semantic_map_claim_workflow.py`
- `docs/wiki-bi/_meta/legacy-semantic-map/claims/wave-2026-04-16-registry-bootstrap/execution/.gitkeep`
- `docs/wiki-bi/_meta/legacy-semantic-map/claims/wave-2026-04-16-registry-bootstrap/subsystems/.gitkeep`
- `docs/wiki-bi/_meta/legacy-semantic-map/claims/wave-2026-04-16-registry-bootstrap/objects/.gitkeep`

### Files To Modify

- `scripts/legacy_semantic_map/__init__.py`
- `scripts/legacy_semantic_map/models.py`
- `scripts/legacy_semantic_map/bootstrap.py`
- `tests/contracts/test_legacy_semantic_map_bootstrap.py`
- `tests/contracts/test_legacy_semantic_map_repo_docs.py`
- `docs/wiki-bi/_meta/legacy-semantic-map/README.md`

### Responsibilities

- `scripts/legacy_semantic_map/models.py` continues to hold shared semantic-map vocabulary and adds any shared constants required by claim artifacts.
- `scripts/legacy_semantic_map/claims.py` defines the typed claim schema, payload serialization helpers, and deterministic writer.
- `scripts/legacy_semantic_map/bootstrap.py` creates active-wave claim directories in addition to the existing registry bootstrap tree.
- `README.md` explains that distributed agents may write only wave-local claim artifacts, while canonical registry files remain main-thread-managed.
- `test_legacy_semantic_map_claim_workflow.py` locks the claim schema, path rules, and writer boundary checks.
- the existing bootstrap and repo-doc contract files keep the checked-in tree and governance wording aligned with the new claim workflow boundary.

---

## Task 1: Add Claim Artifact Schema Contracts

**Files:**
- Modify: `scripts/legacy_semantic_map/models.py`
- Create: `scripts/legacy_semantic_map/claims.py`
- Create: `tests/contracts/test_legacy_semantic_map_claim_workflow.py`

- [ ] **Step 1: Write failing contract tests for claim schema, scope mapping, and deterministic relative paths**

Add a new contract file with tests that lock:

- allowed confidence values
- allowed claim scope directory mapping
- required claim artifact fields
- deterministic relative path shape under `claims/<wave_id>/<scope>/`
- rejection of unsupported claim scopes

Use this test content:

```python
from __future__ import annotations

from pathlib import Path

import pytest

from scripts.legacy_semantic_map.claims import (
    CLAIM_SCOPE_DIRECTORIES,
    ClaimArtifact,
    ClaimCandidateRecord,
    ClaimDiscoveredObjectRecord,
    ClaimEdgeRecord,
    ClaimSourceRecord,
    claim_relative_path,
)
from scripts.legacy_semantic_map.models import CONFIDENCE_LEVELS


def _build_execution_claim() -> ClaimArtifact:
    return ClaimArtifact(
        claim_id="claim-wave-2026-04-16-registry-bootstrap-annuity-performance-manual-entry",
        wave_id="wave-2026-04-16-registry-bootstrap",
        claim_scope="execution",
        claim_target_id="ep-manual-cli-entrypoints-annuity-performance-manual-entry",
        sources_read=[
            ClaimSourceRecord(
                source_ref="src/work_data_hub/cli/etl/domain_validation.py",
                source_type="legacy_code",
                note="Manual domain validation entrypoint for annuity performance.",
            )
        ],
        objects_discovered=[
            ClaimDiscoveredObjectRecord(
                object_id="obj-annuity-performance-manual-entry",
                title="Annuity performance manual entry",
                summary="Manual CLI execution surface for annuity performance.",
                source_refs=[
                    "src/work_data_hub/cli/etl/domain_validation.py",
                ],
                source_type="legacy_code",
                claim_type="direct_observation",
                evidence_strength="strong",
                coverage_state="partial",
                confidence="high",
                last_verified="2026-04-16",
                open_questions=[],
            )
        ],
        edges_added=[
            ClaimEdgeRecord(
                from_id="ep-manual-cli-entrypoints-annuity-performance-manual-entry",
                to_id="obj-annuity-performance-manual-entry",
                relationship="discovers_object",
                source_refs=[
                    "src/work_data_hub/cli/etl/domain_validation.py",
                ],
                source_type="legacy_code",
                claim_type="direct_observation",
                evidence_strength="strong",
                coverage_state="partial",
                confidence="high",
                last_verified="2026-04-16",
                open_questions=[],
            )
        ],
        candidates_raised=[
            ClaimCandidateRecord(
                candidate_id="cand-subsystem-annuity-performance-manual-entry",
                candidate_type="subsystem",
                proposed_name="annuity-performance-manual-entry",
                reason="Manual entrypoint may deserve a dedicated subsystem boundary.",
                trigger_files=[
                    "src/work_data_hub/cli/etl/domain_validation.py",
                ],
                source_type="legacy_code",
                claim_type="direct_observation",
                confidence="medium",
                triage_status="new",
                first_seen_wave="wave-2026-04-16-registry-bootstrap",
                last_verified="2026-04-16",
            )
        ],
        open_questions=[],
        compiled_into=[],
        submitted_at="2026-04-16T00:00:00Z",
    )


def test_claim_artifact_contract_and_relative_path_shape() -> None:
    claim = _build_execution_claim()

    assert CONFIDENCE_LEVELS == ("high", "medium", "low")
    assert CLAIM_SCOPE_DIRECTORIES == {
        "execution": "execution",
        "subsystems": "subsystems",
        "objects": "objects",
    }

    assert claim_relative_path(claim) == Path(
        "claims"
    ) / "wave-2026-04-16-registry-bootstrap" / "execution" / (
        "claim-wave-2026-04-16-registry-bootstrap-annuity-performance-manual-entry.yaml"
    )

    payload = claim.to_payload()
    assert payload["claim_id"] == claim.claim_id
    assert payload["claim_scope"] == "execution"
    assert payload["claim_target_id"] == (
        "ep-manual-cli-entrypoints-annuity-performance-manual-entry"
    )
    assert payload["sources_read"][0]["source_type"] == "legacy_code"
    assert payload["objects_discovered"][0]["confidence"] == "high"
    assert payload["edges_added"][0]["relationship"] == "discovers_object"
    assert payload["candidates_raised"][0]["triage_status"] == "new"


def test_claim_scope_rejects_unsupported_directory_targets() -> None:
    claim = _build_execution_claim()
    invalid_claim = ClaimArtifact(**(claim.to_payload() | {"claim_scope": "paths"}))

    with pytest.raises(ValueError, match="Unsupported claim_scope"):
        claim_relative_path(invalid_claim)
```

- [ ] **Step 2: Run the targeted claim workflow contract test and confirm it fails before implementation**

Run:

```bash
uv run pytest tests/contracts/test_legacy_semantic_map_claim_workflow.py -v
```

Expected: fail because `scripts.legacy_semantic_map.claims` and `CONFIDENCE_LEVELS` do not exist yet.

- [ ] **Step 3: Implement the shared claim schema and path helpers**

Add `CONFIDENCE_LEVELS` to `models.py`, then create `claims.py` with typed records and serialization helpers.

Use this implementation shape:

```python
from __future__ import annotations

from dataclasses import asdict
from dataclasses import dataclass
from pathlib import Path

from .models import (
    CLAIM_TYPES,
    CONFIDENCE_LEVELS,
    COVERAGE_STATES,
    EVIDENCE_STRENGTHS,
    SOURCE_TYPES,
    TRIAGE_STATUSES,
    WAVE_ID_PATTERN,
)

CLAIM_SCOPE_DIRECTORIES = {
    "execution": "execution",
    "subsystems": "subsystems",
    "objects": "objects",
}


@dataclass(frozen=True)
class ClaimSourceRecord:
    source_ref: str
    source_type: str
    note: str


@dataclass(frozen=True)
class ClaimDiscoveredObjectRecord:
    object_id: str
    title: str
    summary: str
    source_refs: list[str]
    source_type: str
    claim_type: str
    evidence_strength: str
    coverage_state: str
    confidence: str
    last_verified: str
    open_questions: list[str]


@dataclass(frozen=True)
class ClaimEdgeRecord:
    from_id: str
    to_id: str
    relationship: str
    source_refs: list[str]
    source_type: str
    claim_type: str
    evidence_strength: str
    coverage_state: str
    confidence: str
    last_verified: str
    open_questions: list[str]


@dataclass(frozen=True)
class ClaimCandidateRecord:
    candidate_id: str
    candidate_type: str
    proposed_name: str
    reason: str
    trigger_files: list[str]
    source_type: str
    claim_type: str
    confidence: str
    triage_status: str
    first_seen_wave: str
    last_verified: str


@dataclass(frozen=True)
class ClaimArtifact:
    claim_id: str
    wave_id: str
    claim_scope: str
    claim_target_id: str
    sources_read: list[ClaimSourceRecord]
    objects_discovered: list[ClaimDiscoveredObjectRecord]
    edges_added: list[ClaimEdgeRecord]
    candidates_raised: list[ClaimCandidateRecord]
    open_questions: list[str]
    compiled_into: list[str]
    submitted_at: str

    def to_payload(self) -> dict[str, object]:
        return {
            **asdict(self),
            "sources_read": [asdict(item) for item in self.sources_read],
            "objects_discovered": [asdict(item) for item in self.objects_discovered],
            "edges_added": [asdict(item) for item in self.edges_added],
            "candidates_raised": [asdict(item) for item in self.candidates_raised],
        }


def claim_relative_path(claim: ClaimArtifact) -> Path:
    if claim.claim_scope not in CLAIM_SCOPE_DIRECTORIES:
        raise ValueError(f"Unsupported claim_scope: {claim.claim_scope}")
    return (
        Path("claims")
        / claim.wave_id
        / CLAIM_SCOPE_DIRECTORIES[claim.claim_scope]
        / f"{claim.claim_id}.yaml"
    )
```

Keep this slice intentionally minimal:

- validate only the vocabulary and directory boundary required by the tests
- do not add compiler logic
- do not add canonical file writing helpers

- [ ] **Step 4: Export the new helpers and rerun the targeted test**

Update `scripts/legacy_semantic_map/__init__.py` so later slices can import the claim helpers:

```python
from .claims import (
    CLAIM_SCOPE_DIRECTORIES,
    ClaimArtifact,
    ClaimCandidateRecord,
    ClaimDiscoveredObjectRecord,
    ClaimEdgeRecord,
    ClaimSourceRecord,
    claim_relative_path,
)
```

Run:

```bash
uv run pytest tests/contracts/test_legacy_semantic_map_claim_workflow.py -v
```

Expected: pass.

## Task 2: Add A Deterministic Claim Writer With Registered-Wave Checks

**Files:**
- Modify: `scripts/legacy_semantic_map/claims.py`
- Modify: `scripts/legacy_semantic_map/__init__.py`
- Modify: `tests/contracts/test_legacy_semantic_map_claim_workflow.py`

- [ ] **Step 1: Extend the claim workflow contract to require YAML writing under registered waves**

Add tests that require:

- writing YAML under `claims/<wave_id>/<scope>/`
- rejecting claim writes for unregistered waves
- preserving nested claim payload data on disk

Use this test content:

```python
from pathlib import Path

import pytest
import yaml

from scripts.legacy_semantic_map.bootstrap import bootstrap_semantic_map
from scripts.legacy_semantic_map.claims import write_claim_artifact


def test_write_claim_artifact_writes_yaml_under_registered_wave(tmp_path: Path) -> None:
    registry_root = tmp_path / "legacy-semantic-map"
    bootstrap_semantic_map(registry_root)

    claim = _build_execution_claim()
    output_path = write_claim_artifact(registry_root, claim)

    assert output_path == (
        registry_root
        / "claims"
        / "wave-2026-04-16-registry-bootstrap"
        / "execution"
        / "claim-wave-2026-04-16-registry-bootstrap-annuity-performance-manual-entry.yaml"
    )

    payload = yaml.safe_load(output_path.read_text(encoding="utf-8"))
    assert payload["claim_id"] == claim.claim_id
    assert payload["sources_read"][0]["source_ref"] == (
        "src/work_data_hub/cli/etl/domain_validation.py"
    )
    assert payload["objects_discovered"][0]["object_id"] == (
        "obj-annuity-performance-manual-entry"
    )


def test_write_claim_artifact_rejects_unregistered_wave(tmp_path: Path) -> None:
    registry_root = tmp_path / "legacy-semantic-map"
    bootstrap_semantic_map(registry_root)

    claim = _build_execution_claim()
    invalid_claim = ClaimArtifact(**(claim.to_payload() | {
        "wave_id": "wave-2026-04-17-unregistered",
    }))

    with pytest.raises(ValueError, match="Unregistered wave_id"):
        write_claim_artifact(registry_root, invalid_claim)
```

- [ ] **Step 2: Run the writer contract tests and confirm they fail before implementation**

Run:

```bash
uv run pytest tests/contracts/test_legacy_semantic_map_claim_workflow.py -v
```

Expected: fail because `write_claim_artifact` does not exist yet.

- [ ] **Step 3: Implement the registered-wave loader and deterministic YAML writer**

Add these helpers to `claims.py`:

```python
from __future__ import annotations

from pathlib import Path

import yaml


def _registered_wave_ids(registry_root: Path) -> set[str]:
    waves_index = yaml.safe_load(
        (registry_root / "waves" / "index.yaml").read_text(encoding="utf-8")
    )
    return {item["wave_id"] for item in waves_index["waves"]}


def write_claim_artifact(registry_root: Path, claim: ClaimArtifact) -> Path:
    if claim.wave_id not in _registered_wave_ids(registry_root):
        raise ValueError(f"Unregistered wave_id: {claim.wave_id}")

    output_path = registry_root / claim_relative_path(claim)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        yaml.safe_dump(claim.to_payload(), sort_keys=False, allow_unicode=False),
        encoding="utf-8",
    )
    return output_path
```

Export the writer from `__init__.py`:

```python
from .claims import write_claim_artifact
```

Implementation guardrails:

- write only YAML claim artifacts under the claim directories
- do not accept arbitrary output paths from callers
- do not mutate canonical registry files in this slice
- do not yet add claim acceptance or compiler-state tracking

- [ ] **Step 4: Run the targeted claim workflow contract file**

Run:

```bash
uv run pytest tests/contracts/test_legacy_semantic_map_claim_workflow.py -v
```

Expected: pass.

## Task 3: Extend Bootstrap And Repo Contracts For Active-Wave Claim Directories

**Files:**
- Modify: `scripts/legacy_semantic_map/bootstrap.py`
- Modify: `tests/contracts/test_legacy_semantic_map_bootstrap.py`
- Modify: `tests/contracts/test_legacy_semantic_map_repo_docs.py`
- Modify: `docs/wiki-bi/_meta/legacy-semantic-map/README.md`
- Create: `docs/wiki-bi/_meta/legacy-semantic-map/claims/wave-2026-04-16-registry-bootstrap/execution/.gitkeep`
- Create: `docs/wiki-bi/_meta/legacy-semantic-map/claims/wave-2026-04-16-registry-bootstrap/subsystems/.gitkeep`
- Create: `docs/wiki-bi/_meta/legacy-semantic-map/claims/wave-2026-04-16-registry-bootstrap/objects/.gitkeep`

- [ ] **Step 1: Extend bootstrap and repo-doc contracts to require claim directories and a visible claim write boundary**

Update `test_legacy_semantic_map_bootstrap.py` so the expected files include:

```python
expected_files = {
    "README.md",
    "manifest.json",
    "execution/entry-surfaces.yaml",
    "execution/paths/.gitkeep",
    "execution/stages/.gitkeep",
    "sources/families.yaml",
    "waves/index.yaml",
    "subsystems/.gitkeep",
    "objects/.gitkeep",
    "claims/wave-2026-04-16-registry-bootstrap/execution/.gitkeep",
    "claims/wave-2026-04-16-registry-bootstrap/subsystems/.gitkeep",
    "claims/wave-2026-04-16-registry-bootstrap/objects/.gitkeep",
}
```

Also require `README.md` to contain:

```python
assert "distributed agents may write only under `claims/<wave_id>/`" in readme_text
assert "canonical registry files remain main-thread-managed" in readme_text
```

Update `test_legacy_semantic_map_repo_docs.py` so `expected_paths` includes:

```python
SEMANTIC_MAP_ROOT / "claims" / "wave-2026-04-16-registry-bootstrap" / "execution" / ".gitkeep",
SEMANTIC_MAP_ROOT / "claims" / "wave-2026-04-16-registry-bootstrap" / "subsystems" / ".gitkeep",
SEMANTIC_MAP_ROOT / "claims" / "wave-2026-04-16-registry-bootstrap" / "objects" / ".gitkeep",
```

And require the checked-in README to keep the same claim boundary wording:

```python
assert "distributed agents may write only under `claims/<wave_id>/`" in readme_text
assert "canonical registry files remain main-thread-managed" in readme_text
```

- [ ] **Step 2: Run the bootstrap and repo-doc contract files and confirm they fail before implementation**

Run:

```bash
uv run pytest tests/contracts/test_legacy_semantic_map_bootstrap.py tests/contracts/test_legacy_semantic_map_repo_docs.py -v
```

Expected: fail because the bootstrap writer and checked-in tree do not create claim directories yet.

- [ ] **Step 3: Update the bootstrap writer and checked-in README boundary text**

Modify `bootstrap.py` so it creates claim directories for the active wave:

```python
from .models import BOOTSTRAP_WAVE


for relative_dir in (
    "execution/paths",
    "execution/stages",
    "subsystems",
    "objects",
    f"claims/{BOOTSTRAP_WAVE.wave_id}/execution",
    f"claims/{BOOTSTRAP_WAVE.wave_id}/subsystems",
    f"claims/{BOOTSTRAP_WAVE.wave_id}/objects",
):
    directory = registry_root / relative_dir
    directory.mkdir(parents=True, exist_ok=True)
    _write_text(directory / ".gitkeep", "")
```

Update `README_TEXT` so it becomes:

```python
README_TEXT = """# Legacy Semantic Map

This subtree is an internal discovery ledger for legacy semantic mapping work.
It is not durable wiki content.
It must never be added to `docs/wiki-bi/index.md`.

distributed agents may write only under `claims/<wave_id>/`.
canonical registry files remain main-thread-managed.

active owner: the main-thread maintainer of the current semantic-map wave
archive trigger: acceptance of the target durable wiki updates plus disposition of remaining findings for that wave
"""
```

Then regenerate the checked-in tree:

```bash
uv run python -m scripts.legacy_semantic_map.bootstrap
```

- [ ] **Step 4: Run the claim, bootstrap, and repo-doc contract files together**

Run:

```bash
uv run pytest tests/contracts/test_legacy_semantic_map_claim_workflow.py tests/contracts/test_legacy_semantic_map_bootstrap.py tests/contracts/test_legacy_semantic_map_repo_docs.py -v
```

Expected: pass.

## Validation

Run:

```bash
uv sync --dev
uv run python -m scripts.legacy_semantic_map.bootstrap
uv run pytest tests/contracts/test_legacy_semantic_map_claim_workflow.py tests/contracts/test_legacy_semantic_map_bootstrap.py tests/contracts/test_legacy_semantic_map_repo_docs.py -v
uv run pytest -v
rg -n "claims/<wave_id>|main-thread-managed|wave-2026-04-16-registry-bootstrap" docs/wiki-bi/_meta/legacy-semantic-map/README.md tests/contracts/test_legacy_semantic_map_claim_workflow.py tests/contracts/test_legacy_semantic_map_repo_docs.py
git diff -- docs/wiki-bi/_meta/legacy-semantic-map scripts/legacy_semantic_map tests/contracts
git status -sb
```

Expected:

- claim artifacts can be serialized and written only under registered wave-local claim directories
- unsupported claim scopes and unregistered waves fail closed
- the bootstrap writer creates active-wave claim directories deterministically
- the checked-in README makes the claim write boundary visible in-tree
- canonical registry files are still untouched by the claim writer
- the full suite still passes after claim workflow support is added

## Expected Outcome

After this plan is executed:

- distributed agents have one governed way to write claim artifacts without editing canonical registry files
- the active wave has a stable checked-in `claims/` tree shape that later plans can consume
- the semantic-map README now distinguishes claim-write surfaces from main-thread canonical surfaces
- the next plan can focus on canonical compilation instead of re-deciding claim schema and write boundaries

# WorkDataHubPro Legacy Semantic Map Canonical Compilation Implementation Plan

> **Status:** Proposed

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Compile accepted semantic-map claim artifacts into canonical registry files through one main-thread-only path while preserving claim provenance.

**Architecture:** Treat this slice as `18.2.2 Plan B: Canonical Compilation` only. The compiler should accept an explicit list of accepted claim artifact paths, normalize those claims into canonical execution, subsystem, object, edge, and candidate registry files, and regenerate a generated-only manifest summary. It must not introduce integrity reporting, wave closeout, or an acceptance-state registry in this slice.

**Tech Stack:** Python 3.12, `uv`, `pytest`, `PyYAML`, JSON, YAML, Markdown

---

## Scope Check

This plan covers only `18.2.2 Plan B: Canonical Compilation` from `docs/superpowers/specs/2026-04-16-workdatahub-legacy-semantic-map-design.md`.

This plan does cover:

- main-thread canonical compilation from an explicit set of accepted claim files
- deterministic canonical writers for `execution/paths/`, `subsystems/`, `objects/`, `edges/`, and `candidates/`
- canonical index files for subsystems and objects
- generated manifest regeneration after compilation
- checked-in bootstrap support for canonical compiler output files
- provenance fields in canonical outputs so compiled claims remain traceable

This plan does not cover:

- claim acceptance workflow or an accepted-claims registry
- integrity / coverage report generation
- candidate staleness metrics
- wave closeout or archive readiness
- first-wave discovery execution against the legacy repository

Those belong to later implementation plans, especially `Slice 3: Reporting And Wave Closure` and `Slice 4: First-Wave Pilot`.

## Canonical Compiler Boundary

This slice should introduce only the minimum machinery required to make canonical compilation real and reviewable:

- the main thread chooses accepted claim files explicitly by path
- the compiler validates those paths remain under `claims/<wave_id>/`
- canonical files record `compiled_from_claims` so provenance stays visible
- the manifest remains generated-only and must not become a hand-maintained fact source

This slice should not yet:

- mutate claim artifacts to mark acceptance
- infer a separate approval state from git history or timestamps
- generate `reports/current/*.json` or `reports/waves/<wave_id>/*.json`
- decide wave closure, archive readiness, or candidate staleness

### Edge Taxonomy Correction

The current claim workflow already allows execution claims to emit `ep -> obj`
edges.

That means canonical compilation needs one additional edge registry:

- `edges/execution-to-object.yaml`

Do not force execution-to-object links into `execution-to-subsystem.yaml` or
`subsystem-to-object.yaml`. That would mis-state the discovered graph.

## Proposed File Structure

### Files To Create

- `scripts/legacy_semantic_map/compiler.py`
- `tests/contracts/test_legacy_semantic_map_canonical_compiler.py`
- `docs/wiki-bi/_meta/legacy-semantic-map/subsystems/index.yaml`
- `docs/wiki-bi/_meta/legacy-semantic-map/objects/index.yaml`
- `docs/wiki-bi/_meta/legacy-semantic-map/edges/execution-to-subsystem.yaml`
- `docs/wiki-bi/_meta/legacy-semantic-map/edges/execution-to-object.yaml`
- `docs/wiki-bi/_meta/legacy-semantic-map/edges/subsystem-to-object.yaml`
- `docs/wiki-bi/_meta/legacy-semantic-map/edges/object-to-object.yaml`
- `docs/wiki-bi/_meta/legacy-semantic-map/edges/source-to-node.yaml`
- `docs/wiki-bi/_meta/legacy-semantic-map/candidates/subsystem-candidates.yaml`
- `docs/wiki-bi/_meta/legacy-semantic-map/candidates/object-candidates.yaml`

### Files To Modify

- `scripts/legacy_semantic_map/__init__.py`
- `scripts/legacy_semantic_map/bootstrap.py`
- `tests/contracts/test_legacy_semantic_map_bootstrap.py`
- `tests/contracts/test_legacy_semantic_map_repo_docs.py`
- `docs/wiki-bi/_meta/legacy-semantic-map/README.md`
- `docs/wiki-bi/_meta/legacy-semantic-map/manifest.json`

### Responsibilities

- `scripts/legacy_semantic_map/compiler.py` owns claim loading, validation, canonical aggregation, edge routing, candidate routing, and manifest regeneration.
- `subsystems/index.yaml` and `objects/index.yaml` summarize canonical registry membership without replacing the per-file canonical records.
- `edges/*.yaml` hold normalized relationship registries grouped by edge family.
- `candidates/*.yaml` hold normalized canonical candidate lists grouped by candidate type.
- `README.md` keeps the main-thread-only canonical compilation rule visible in-tree.
- `test_legacy_semantic_map_canonical_compiler.py` locks path validation, canonical output shape, provenance, and determinism.

---

## Task 1: Lock Canonical Compiler Contracts

**Files:**
- Create: `tests/contracts/test_legacy_semantic_map_canonical_compiler.py`
- Modify: `scripts/legacy_semantic_map/__init__.py`

- [ ] **Step 1: Write failing contract tests for canonical compilation, provenance, and claim-path validation**

Add a new contract file that:

- bootstraps an empty semantic-map registry
- writes one execution claim, one subsystem claim, and one object claim
- compiles those accepted claim files through one explicit function call
- asserts canonical files, edge registries, candidate registries, object/subsystem indexes, and manifest provenance are written deterministically
- rejects claim paths that are outside `claims/<wave_id>/`

Use this test content:

```python
from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

from scripts.legacy_semantic_map.bootstrap import bootstrap_semantic_map
from scripts.legacy_semantic_map.claims import (
    ClaimArtifact,
    ClaimCandidateRecord,
    ClaimDiscoveredObjectRecord,
    ClaimEdgeRecord,
    ClaimSourceRecord,
    write_claim_artifact,
)
from scripts.legacy_semantic_map.compiler import compile_claim_artifacts


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
                note="Manual annuity-performance CLI entrypoint.",
            )
        ],
        objects_discovered=[
            ClaimDiscoveredObjectRecord(
                object_id="obj-annuity-performance-manual-entry",
                title="Annuity performance manual entry",
                summary="Manual CLI execution surface for annuity performance.",
                source_refs=["src/work_data_hub/cli/etl/domain_validation.py"],
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
                source_refs=["src/work_data_hub/cli/etl/domain_validation.py"],
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
                trigger_files=["src/work_data_hub/cli/etl/domain_validation.py"],
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
```

Continue the same test file with:

```python
def _build_subsystem_claim() -> ClaimArtifact:
    return ClaimArtifact(
        claim_id="claim-wave-2026-04-16-registry-bootstrap-annuity-performance-subsystem",
        wave_id="wave-2026-04-16-registry-bootstrap",
        claim_scope="subsystems",
        claim_target_id="ss-annuity-performance-manual-entry",
        sources_read=[
            ClaimSourceRecord(
                source_ref="src/work_data_hub/cli/etl/domain_validation.py",
                source_type="legacy_code",
                note="Subsystem evidence for manual annuity-performance entrypoint.",
            )
        ],
        objects_discovered=[
            ClaimDiscoveredObjectRecord(
                object_id="obj-annuity-performance-manual-entry",
                title="Annuity performance manual entry",
                summary="Manual CLI execution surface for annuity performance.",
                source_refs=["src/work_data_hub/cli/etl/domain_validation.py"],
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
                from_id="ss-annuity-performance-manual-entry",
                to_id="obj-annuity-performance-manual-entry",
                relationship="owns_object",
                source_refs=["src/work_data_hub/cli/etl/domain_validation.py"],
                source_type="legacy_code",
                claim_type="direct_observation",
                evidence_strength="strong",
                coverage_state="partial",
                confidence="high",
                last_verified="2026-04-16",
                open_questions=[],
            )
        ],
        candidates_raised=[],
        open_questions=[],
        compiled_into=[],
        submitted_at="2026-04-16T00:05:00Z",
    )


def _build_object_claim() -> ClaimArtifact:
    return ClaimArtifact(
        claim_id="claim-wave-2026-04-16-registry-bootstrap-annuity-performance-object",
        wave_id="wave-2026-04-16-registry-bootstrap",
        claim_scope="objects",
        claim_target_id="obj-annuity-performance-manual-entry",
        sources_read=[
            ClaimSourceRecord(
                source_ref="src/work_data_hub/cli/etl/domain_validation.py",
                source_type="legacy_code",
                note="Object-level evidence for manual annuity-performance entrypoint.",
            )
        ],
        objects_discovered=[
            ClaimDiscoveredObjectRecord(
                object_id="obj-annuity-performance-manual-entry",
                title="Annuity performance manual entry",
                summary="Manual CLI execution surface for annuity performance.",
                source_refs=["src/work_data_hub/cli/etl/domain_validation.py"],
                source_type="legacy_code",
                claim_type="direct_observation",
                evidence_strength="strong",
                coverage_state="partial",
                confidence="high",
                last_verified="2026-04-16",
                open_questions=[],
            )
        ],
        edges_added=[],
        candidates_raised=[],
        open_questions=[],
        compiled_into=[],
        submitted_at="2026-04-16T00:10:00Z",
    )


def test_compile_claim_artifacts_writes_canonical_registry_files(tmp_path: Path) -> None:
    registry_root = tmp_path / "legacy-semantic-map"
    bootstrap_semantic_map(registry_root)

    execution_path = write_claim_artifact(registry_root, _build_execution_claim())
    subsystem_path = write_claim_artifact(registry_root, _build_subsystem_claim())
    object_path = write_claim_artifact(registry_root, _build_object_claim())

    result = compile_claim_artifacts(
        registry_root,
        [execution_path, subsystem_path, object_path],
    )

    assert result.compiled_claim_ids == [
        "claim-wave-2026-04-16-registry-bootstrap-annuity-performance-manual-entry",
        "claim-wave-2026-04-16-registry-bootstrap-annuity-performance-object",
        "claim-wave-2026-04-16-registry-bootstrap-annuity-performance-subsystem",
    ]

    path_payload = yaml.safe_load(
        (registry_root / "execution" / "paths" / "ep-manual-cli-entrypoints-annuity-performance-manual-entry.yaml").read_text(
            encoding="utf-8"
        )
    )
    assert path_payload["path_id"] == "ep-manual-cli-entrypoints-annuity-performance-manual-entry"
    assert path_payload["entry_surface"] == "manual_cli_entrypoints"
    assert path_payload["domain_or_surface"] == "annuity_performance"
    assert path_payload["compiled_from_claims"] == [
        "claim-wave-2026-04-16-registry-bootstrap-annuity-performance-manual-entry"
    ]

    subsystem_payload = yaml.safe_load(
        (registry_root / "subsystems" / "ss-annuity-performance-manual-entry.yaml").read_text(
            encoding="utf-8"
        )
    )
    assert subsystem_payload["subsystem_id"] == "ss-annuity-performance-manual-entry"
    assert subsystem_payload["compiled_from_claims"] == [
        "claim-wave-2026-04-16-registry-bootstrap-annuity-performance-subsystem"
    ]

    object_payload = yaml.safe_load(
        (registry_root / "objects" / "obj-annuity-performance-manual-entry.yaml").read_text(
            encoding="utf-8"
        )
    )
    assert object_payload["object_id"] == "obj-annuity-performance-manual-entry"
    assert object_payload["compiled_from_claims"] == [
        "claim-wave-2026-04-16-registry-bootstrap-annuity-performance-object"
    ]

    edge_payload = yaml.safe_load(
        (registry_root / "edges" / "execution-to-object.yaml").read_text(encoding="utf-8")
    )
    assert edge_payload["edges"][0]["from_id"] == (
        "ep-manual-cli-entrypoints-annuity-performance-manual-entry"
    )
    assert edge_payload["edges"][0]["to_id"] == "obj-annuity-performance-manual-entry"

    candidate_payload = yaml.safe_load(
        (registry_root / "candidates" / "subsystem-candidates.yaml").read_text(
            encoding="utf-8"
        )
    )
    assert candidate_payload["subsystem_candidates"][0]["candidate_id"] == (
        "cand-subsystem-annuity-performance-manual-entry"
    )

    manifest = json.loads((registry_root / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["generated_canonical_files"] == sorted(result.written_files)
    assert manifest["compiled_claim_ids"] == result.compiled_claim_ids


def test_compile_claim_artifacts_rejects_non_claim_paths(tmp_path: Path) -> None:
    registry_root = tmp_path / "legacy-semantic-map"
    bootstrap_semantic_map(registry_root)

    rogue_claim = registry_root / "rogue.yaml"
    rogue_claim.write_text("claim_id: rogue\n", encoding="utf-8")

    with pytest.raises(ValueError, match="must live under claims/"):
        compile_claim_artifacts(registry_root, [rogue_claim])
```

- [ ] **Step 2: Run the targeted canonical compiler contract file and confirm it fails before implementation**

Run:

```bash
uv run python -m pytest tests/contracts/test_legacy_semantic_map_canonical_compiler.py -v
```

Expected: fail because `scripts.legacy_semantic_map.compiler` does not exist yet.

- [ ] **Step 3: Export compiler symbols from the package surface**

Once the compiler module exists later in this plan, export:

```python
from .compiler import CompilationResult, compile_claim_artifacts
```

and add them to `__all__`:

```python
    "CompilationResult",
    "compile_claim_artifacts",
```

- [ ] **Step 4: Re-run the targeted compiler contract file**

Run:

```bash
uv run python -m pytest tests/contracts/test_legacy_semantic_map_canonical_compiler.py -v
```

Expected: pass after Tasks 2 through 4 are complete.

## Task 2: Extend Bootstrap For Canonical Compiler Surfaces

**Files:**
- Modify: `scripts/legacy_semantic_map/bootstrap.py`
- Modify: `tests/contracts/test_legacy_semantic_map_bootstrap.py`
- Modify: `tests/contracts/test_legacy_semantic_map_repo_docs.py`
- Modify: `docs/wiki-bi/_meta/legacy-semantic-map/README.md`
- Modify: `docs/wiki-bi/_meta/legacy-semantic-map/manifest.json`
- Create: `docs/wiki-bi/_meta/legacy-semantic-map/subsystems/index.yaml`
- Create: `docs/wiki-bi/_meta/legacy-semantic-map/objects/index.yaml`
- Create: `docs/wiki-bi/_meta/legacy-semantic-map/edges/execution-to-subsystem.yaml`
- Create: `docs/wiki-bi/_meta/legacy-semantic-map/edges/execution-to-object.yaml`
- Create: `docs/wiki-bi/_meta/legacy-semantic-map/edges/subsystem-to-object.yaml`
- Create: `docs/wiki-bi/_meta/legacy-semantic-map/edges/object-to-object.yaml`
- Create: `docs/wiki-bi/_meta/legacy-semantic-map/edges/source-to-node.yaml`
- Create: `docs/wiki-bi/_meta/legacy-semantic-map/candidates/subsystem-candidates.yaml`
- Create: `docs/wiki-bi/_meta/legacy-semantic-map/candidates/object-candidates.yaml`

- [ ] **Step 1: Extend bootstrap and repo-doc contract tests to require the canonical compiler tree**

Update the bootstrap test so `expected_files` includes:

```python
    "subsystems/index.yaml",
    "objects/index.yaml",
    "edges/execution-to-subsystem.yaml",
    "edges/execution-to-object.yaml",
    "edges/subsystem-to-object.yaml",
    "edges/object-to-object.yaml",
    "edges/source-to-node.yaml",
    "candidates/subsystem-candidates.yaml",
    "candidates/object-candidates.yaml",
```

Add README assertions:

```python
    assert "canonical compilation is a main-thread-only operation" in readme_text
```

Update the repo-doc contract file so `expected_paths` includes the same checked-in files and so the manifest assertion becomes:

```python
    assert manifest["canonical_seed_sources"] == [
        "execution/entry-surfaces.yaml",
        "sources/families.yaml",
        "waves/index.yaml",
    ]
    assert manifest["generated_canonical_files"] == []
    assert manifest["compiled_claim_ids"] == []
```

- [ ] **Step 2: Run the bootstrap and repo-doc contract files and confirm they fail before implementation**

Run:

```bash
uv run python -m pytest tests/contracts/test_legacy_semantic_map_bootstrap.py tests/contracts/test_legacy_semantic_map_repo_docs.py -v
```

Expected: fail because the checked-in tree does not yet contain canonical compiler files.

- [ ] **Step 3: Update the bootstrap writer so it creates the canonical compiler files deterministically**

Use this implementation shape in `bootstrap.py`:

```python
EMPTY_REGISTRY_PAYLOADS = {
    "subsystems/index.yaml": {"subsystems": []},
    "objects/index.yaml": {"objects": []},
    "edges/execution-to-subsystem.yaml": {"edges": []},
    "edges/execution-to-object.yaml": {"edges": []},
    "edges/subsystem-to-object.yaml": {"edges": []},
    "edges/object-to-object.yaml": {"edges": []},
    "edges/source-to-node.yaml": {"edges": []},
    "candidates/subsystem-candidates.yaml": {"subsystem_candidates": []},
    "candidates/object-candidates.yaml": {"object_candidates": []},
}

README_TEXT = """# Legacy Semantic Map

This subtree is an internal discovery ledger for legacy semantic mapping work.
It is not durable wiki content.
It must never be added to `docs/wiki-bi/index.md`.

distributed agents may write only under `claims/<wave_id>/`.
canonical registry files remain main-thread-managed.
canonical compilation is a main-thread-only operation.

active owner: the main-thread maintainer of the current semantic-map wave
archive trigger: acceptance of the target durable wiki updates plus disposition of remaining findings for that wave
"""

_write_json(
    registry_root / "manifest.json",
    {
        "artifact": "legacy-semantic-map-registry",
        "canonical_seed_sources": list(CANONICAL_SEED_SOURCES),
        "generated_canonical_files": [],
        "compiled_claim_ids": [],
    },
)

for relative_path, payload in EMPTY_REGISTRY_PAYLOADS.items():
    _write_yaml(registry_root / relative_path, payload)
```

Then regenerate the checked-in tree:

```bash
uv run python -m scripts.legacy_semantic_map.bootstrap
```

- [ ] **Step 4: Run the bootstrap and repo-doc contract files**

Run:

```bash
uv run python -m pytest tests/contracts/test_legacy_semantic_map_bootstrap.py tests/contracts/test_legacy_semantic_map_repo_docs.py -v
```

Expected: pass.

## Task 3: Implement Canonical Aggregation And Writers

**Files:**
- Create: `scripts/legacy_semantic_map/compiler.py`
- Modify: `scripts/legacy_semantic_map/__init__.py`
- Modify: `tests/contracts/test_legacy_semantic_map_canonical_compiler.py`

- [ ] **Step 1: Extend the compiler contract to require deterministic edge routing, index generation, and provenance**

Add assertions that:

- `ep -> ss` edges land in `edges/execution-to-subsystem.yaml`
- `ep -> obj` edges land in `edges/execution-to-object.yaml`
- `ss -> obj` edges land in `edges/subsystem-to-object.yaml`
- `obj -> obj` edges land in `edges/object-to-object.yaml`
- every `sources_read` record becomes a `source -> node` edge in `edges/source-to-node.yaml`
- `subsystems/index.yaml` and `objects/index.yaml` contain canonical file references

Add this test:

```python
def test_compile_claim_artifacts_is_deterministic(tmp_path: Path) -> None:
    registry_root = tmp_path / "legacy-semantic-map"
    bootstrap_semantic_map(registry_root)

    execution_path = write_claim_artifact(registry_root, _build_execution_claim())
    subsystem_path = write_claim_artifact(registry_root, _build_subsystem_claim())
    object_path = write_claim_artifact(registry_root, _build_object_claim())

    first = compile_claim_artifacts(registry_root, [execution_path, subsystem_path, object_path])
    second = compile_claim_artifacts(registry_root, [subsystem_path, object_path, execution_path])

    assert first.compiled_claim_ids == second.compiled_claim_ids
    assert first.written_files == second.written_files

    manifest = json.loads((registry_root / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["compiled_claim_ids"] == first.compiled_claim_ids
    assert manifest["generated_canonical_files"] == first.written_files
```

- [ ] **Step 2: Run the targeted compiler contract file and confirm the new assertions fail**

Run:

```bash
uv run python -m pytest tests/contracts/test_legacy_semantic_map_canonical_compiler.py -v
```

Expected: fail because edge routing and canonical writers are not implemented yet.

- [ ] **Step 3: Implement the main compiler entrypoint and canonical writer helpers**

Create `scripts/legacy_semantic_map/compiler.py` with this structure:

```python
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

import json
import yaml

from .claims import ClaimArtifact
from .models import CANONICAL_SEED_SOURCES


@dataclass(frozen=True)
class CompilationResult:
    compiled_claim_ids: list[str]
    written_files: list[str]


def _load_claim(path: Path) -> ClaimArtifact:
    return ClaimArtifact(**yaml.safe_load(path.read_text(encoding="utf-8")))


def _assert_claim_path(registry_root: Path, claim_path: Path) -> Path:
    resolved_root = registry_root.resolve()
    resolved_path = claim_path.resolve()
    claims_root = (registry_root / "claims").resolve()
    if claims_root not in resolved_path.parents:
        raise ValueError(f"Accepted claim path must live under claims/: {claim_path}")
    return resolved_path.relative_to(resolved_root)


def _write_yaml(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        yaml.safe_dump(payload, sort_keys=False, allow_unicode=False),
        encoding="utf-8",
    )


def _sorted_unique(values: Iterable[str]) -> list[str]:
    return sorted({value for value in values if value})


def _path_entry_surface(path_id: str) -> str:
    parts = path_id.split("-")
    return "_".join(parts[1:4])


def _path_domain_or_surface(path_id: str) -> str:
    parts = path_id.split("-")
    return "_".join(parts[4:-2])


def _title_from_id(identifier: str) -> str:
    return identifier.split("-", 1)[1].replace("-", " ").title()


def compile_claim_artifacts(
    registry_root: Path,
    claim_paths: Sequence[Path],
) -> CompilationResult:
    relative_claim_paths = [_assert_claim_path(registry_root, path) for path in claim_paths]
    claims = [_load_claim(registry_root / relative_path) for relative_path in relative_claim_paths]
    claims = sorted(claims, key=lambda item: item.claim_id)

    written_files: list[str] = []

    for claim in claims:
        if claim.claim_scope == "execution":
            payload = {
                "path_id": claim.claim_target_id,
                "entry_surface": _path_entry_surface(claim.claim_target_id),
                "domain_or_surface": _path_domain_or_surface(claim.claim_target_id),
                "stages": [],
                "touches_subsystems": [],
                "touches_outputs": [],
                "branches_to": [],
                "rebuild_target_boundary": [],
                "rebuild_capability": [],
                "governance_relevance": [],
                "source_refs": _sorted_unique(
                    [item.source_ref for item in claim.sources_read]
                    + [ref for obj in claim.objects_discovered for ref in obj.source_refs]
                ),
                "source_type": claim.sources_read[0].source_type,
                "claim_type": "compiled_summary",
                "evidence_strength": "strong",
                "coverage_state": "partial",
                "confidence": "high",
                "last_verified": max(
                    (item.last_verified for item in claim.objects_discovered),
                    default="not_yet_verified",
                ),
                "open_questions": claim.open_questions,
                "compiled_from_claims": [claim.claim_id],
            }
            output_path = registry_root / "execution" / "paths" / f"{claim.claim_target_id}.yaml"
            _write_yaml(output_path, payload)
            written_files.append(output_path.relative_to(registry_root).as_posix())

        if claim.claim_scope == "subsystems":
            payload = {
                "subsystem_id": claim.claim_target_id,
                "title": _title_from_id(claim.claim_target_id),
                "status": "active",
                "semantic_scope": f"Compiled subsystem summary for {claim.claim_target_id}.",
                "source_families": [],
                "primary_sources": _sorted_unique(item.source_ref for item in claim.sources_read),
                "secondary_sources": [],
                "execution_nodes": [],
                "owned_surfaces": [],
                "owned_outputs": [],
                "discovered_objects": _sorted_unique(
                    item.object_id for item in claim.objects_discovered
                ),
                "candidate_objects": [],
                "candidate_subsystems": [],
                "upstream_dependencies": [],
                "downstream_dependencies": [],
                "claim_type": "compiled_summary",
                "source_type": claim.sources_read[0].source_type,
                "evidence_strength": "strong",
                "coverage_state": "partial",
                "open_questions": claim.open_questions,
                "confidence": "high",
                "last_verified": max(
                    (item.last_verified for item in claim.objects_discovered),
                    default="not_yet_verified",
                ),
                "last_audited_at": claim.submitted_at,
                "compiled_from_claims": [claim.claim_id],
            }
            output_path = registry_root / "subsystems" / f"{claim.claim_target_id}.yaml"
            _write_yaml(output_path, payload)
            written_files.append(output_path.relative_to(registry_root).as_posix())

        if claim.claim_scope == "objects":
            target_object = next(
                item for item in claim.objects_discovered if item.object_id == claim.claim_target_id
            )
            payload = {
                "object_id": target_object.object_id,
                "title": target_object.title,
                "status": "active",
                "object_type": "discovered_semantic_object",
                "summary": target_object.summary,
                "source_refs": target_object.source_refs,
                "seen_in_subsystems": [],
                "related_objects": [],
                "claim_type": "compiled_summary",
                "source_type": target_object.source_type,
                "evidence_strength": target_object.evidence_strength,
                "coverage_state": target_object.coverage_state,
                "confidence": target_object.confidence,
                "last_verified": target_object.last_verified,
                "open_questions": target_object.open_questions,
                "compiled_from_claims": [claim.claim_id],
            }
            output_path = registry_root / "objects" / f"{claim.claim_target_id}.yaml"
            _write_yaml(output_path, payload)
            written_files.append(output_path.relative_to(registry_root).as_posix())

    written_files = sorted(set(written_files))
    compiled_claim_ids = [claim.claim_id for claim in claims]
    _write_manifest(
        registry_root,
        compiled_claim_ids=compiled_claim_ids,
        written_files=written_files,
    )
    return CompilationResult(
        compiled_claim_ids=compiled_claim_ids,
        written_files=written_files,
    )
```

Implement the rest of the file with helper functions that:

- aggregate `subsystems/index.yaml`
- aggregate `objects/index.yaml`
- route edges by prefix pair into the correct `edges/*.yaml`
- route candidates by `candidate_type` into `candidates/*.yaml`
- add `source -> node` edges from every `sources_read` record to the claim target

- [ ] **Step 4: Run the targeted compiler contract file**

Run:

```bash
uv run python -m pytest tests/contracts/test_legacy_semantic_map_canonical_compiler.py -v
```

Expected: pass.

## Task 4: Add CLI Entry Point And Regenerated Manifest Summary

**Files:**
- Modify: `scripts/legacy_semantic_map/compiler.py`
- Modify: `scripts/legacy_semantic_map/__init__.py`
- Modify: `tests/contracts/test_legacy_semantic_map_canonical_compiler.py`
- Modify: `docs/wiki-bi/_meta/legacy-semantic-map/manifest.json`

- [ ] **Step 1: Extend the compiler contract to require a manifest summary and CLI execution path**

Add a CLI-focused test:

```python
from scripts.legacy_semantic_map.compiler import main as compiler_main


def test_compile_claim_artifacts_cli_updates_manifest(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    registry_root = tmp_path / "legacy-semantic-map"
    bootstrap_semantic_map(registry_root)

    execution_path = write_claim_artifact(registry_root, _build_execution_claim())
    subsystem_path = write_claim_artifact(registry_root, _build_subsystem_claim())
    object_path = write_claim_artifact(registry_root, _build_object_claim())

    monkeypatch.setattr(
        "sys.argv",
        [
            "compiler",
            "--registry-root",
            str(registry_root),
            "--claim",
            str(execution_path),
            "--claim",
            str(subsystem_path),
            "--claim",
            str(object_path),
        ],
    )

    compiler_main()

    manifest = json.loads((registry_root / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["artifact"] == "legacy-semantic-map-registry"
    assert manifest["compiled_claim_ids"] == [
        "claim-wave-2026-04-16-registry-bootstrap-annuity-performance-manual-entry",
        "claim-wave-2026-04-16-registry-bootstrap-annuity-performance-object",
        "claim-wave-2026-04-16-registry-bootstrap-annuity-performance-subsystem",
    ]
    assert "execution/paths/ep-manual-cli-entrypoints-annuity-performance-manual-entry.yaml" in manifest["generated_canonical_files"]
```

- [ ] **Step 2: Run the targeted compiler contract file and confirm the CLI assertion fails**

Run:

```bash
uv run python -m pytest tests/contracts/test_legacy_semantic_map_canonical_compiler.py -v
```

Expected: fail because the compiler CLI and manifest regeneration are not complete yet.

- [ ] **Step 3: Add the CLI parser and generated manifest writer**

Finish `compiler.py` with:

```python
import argparse
import json


def _write_manifest(
    registry_root: Path,
    *,
    compiled_claim_ids: list[str],
    written_files: list[str],
) -> None:
    manifest_path = registry_root / "manifest.json"
    manifest_path.write_text(
        json.dumps(
            {
                "artifact": "legacy-semantic-map-registry",
                "canonical_seed_sources": list(CANONICAL_SEED_SOURCES),
                "generated_canonical_files": written_files,
                "compiled_claim_ids": compiled_claim_ids,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry-root", type=Path, required=True)
    parser.add_argument("--claim", type=Path, action="append", default=[])
    args = parser.parse_args()

    compile_claim_artifacts(args.registry_root, args.claim)


if __name__ == "__main__":
    main()
```

Make sure `compile_claim_artifacts()` also calls `_write_manifest()` directly so the function and the CLI stay consistent.

- [ ] **Step 4: Run the canonical compiler contracts, then the existing semantic-map contracts**

Run:

```bash
uv run python -m pytest tests/contracts/test_legacy_semantic_map_canonical_compiler.py tests/contracts/test_legacy_semantic_map_bootstrap.py tests/contracts/test_legacy_semantic_map_claim_workflow.py tests/contracts/test_legacy_semantic_map_repo_docs.py -v
```

Expected: pass.

## Validation

Run:

```bash
uv sync --dev
uv run python -m scripts.legacy_semantic_map.bootstrap
uv run python -m pytest tests/contracts/test_legacy_semantic_map_canonical_compiler.py tests/contracts/test_legacy_semantic_map_bootstrap.py tests/contracts/test_legacy_semantic_map_claim_workflow.py tests/contracts/test_legacy_semantic_map_repo_docs.py -v
# Requires a real accepted claim artifact path. If the repository still has only .gitkeep
# placeholders under claims/, first create a temporary accepted claim file via the contract
# test fixtures or another explicit main-thread claim-writing step, then pass that file here.
uv run python -m scripts.legacy_semantic_map.compiler --registry-root docs/wiki-bi/_meta/legacy-semantic-map --claim <accepted-claim-path>
rg -n "main-thread-only operation|generated_canonical_files|execution-to-object" docs/wiki-bi/_meta/legacy-semantic-map/README.md docs/wiki-bi/_meta/legacy-semantic-map/manifest.json tests/contracts/test_legacy_semantic_map_canonical_compiler.py
git diff -- docs/wiki-bi/_meta/legacy-semantic-map scripts/legacy_semantic_map tests/contracts
git status -sb
```

Expected:

- accepted claim paths are selected explicitly by the main thread
- canonical compilation writes deterministic registry files under `execution/paths/`, `subsystems/`, `objects/`, `edges/`, and `candidates/`
- canonical files expose `compiled_from_claims`
- the manifest remains generated-only and lists compiled claim IDs plus generated canonical file paths
- `execution-to-object.yaml` exists so current execution-claim edge shapes are not normalized into the wrong registry family
- reporting and wave-closeout artifacts remain untouched in this slice

## Expected Outcome

After this plan is executed:

- the semantic-map registry has one governed path from accepted claims to canonical registry files
- claim provenance remains visible in every canonical write surface
- canonical edges and candidates are normalized without introducing reporting logic
- later reporting and wave-closeout work can build on stable canonical files instead of reading raw claims directly

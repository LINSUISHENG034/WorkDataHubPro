# Semantic Map Ingress Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a repository-local semantic-ingress workflow that writes lighter-weight ingress findings from legacy-only evidence, runs a mechanical guard, and optionally auto-promotes promotion-ready ingress records into new semantic claim artifacts under the active open wave.

**Architecture:** Extend the existing semantic-map wave, claim, compiler, and reporting stack instead of adding a parallel pipeline. Introduce one new ingress ledger under `docs/wiki-bi/_meta/legacy-semantic-map/ingress/`, one new mechanical guard under `scripts/legacy_semantic_map/semantic_ingress_guard.py`, and one repo-local skill under `.codex/skills/wdhp-semantic-map-ingress/`. The new workflow may write ingress records and new semantic claim artifacts, but it must not compile canonical semantic files automatically and it must never write durable `docs/wiki-bi/` pages.

**Tech Stack:** Python 3.12, `uv`, `pytest`, `PyYAML`, Markdown, local Codex skill packaging

---

## Scope Check

This spec is still one cohesive implementation slice, not multiple unrelated plans.

The work crosses these surfaces together on purpose:

- semantic-map registry bootstrap and checked-in tree
- semantic-map helper tooling under `scripts/legacy_semantic_map/`
- contract tests under `tests/contracts/`
- repo-local skill packaging under `.codex/skills/`

Do not split canonical compilation or reporting into this slice. Those flows already exist and should be reused as-is.

Do not use the docs-only fast path for implementation. This slice changes Python helpers, tests, checked-in semantic-map artifacts, and local skill packaging. Use an isolated implementation path in a dedicated worktree before executing the plan.

## File Structure

### Files To Create

- `scripts/legacy_semantic_map/ingress.py`
- `scripts/legacy_semantic_map/semantic_ingress_guard.py`
- `tests/contracts/test_legacy_semantic_map_ingress_workflow.py`
- `tests/contracts/test_legacy_semantic_map_semantic_ingress_guard.py`
- `tests/contracts/test_legacy_semantic_map_ingress_skill_docs.py`
- `.codex/skills/wdhp-semantic-map-ingress/SKILL.md`
- `.codex/skills/wdhp-semantic-map-ingress/references/ingress-template.md`
- `.codex/skills/wdhp-semantic-map-ingress/references/promotion-gates.md`
- `.codex/skills/wdhp-semantic-map-ingress/references/claim-minimum-fields.md`
- `.codex/skills/wdhp-semantic-map-ingress/scripts/semantic_ingress_guard.py`
- `docs/wiki-bi/_meta/legacy-semantic-map/ingress/waves/wave-2026-04-17-semantic-governance-reframe/index.yaml`
- `docs/wiki-bi/_meta/legacy-semantic-map/ingress/waves/wave-2026-04-17-semantic-governance-reframe/question-clusters/.gitkeep`
- `docs/wiki-bi/_meta/legacy-semantic-map/ingress/waves/wave-2026-04-17-semantic-governance-reframe/findings/.gitkeep`

### Files To Modify

- `scripts/legacy_semantic_map/__init__.py`
- `scripts/legacy_semantic_map/bootstrap.py`
- `scripts/legacy_semantic_map/waves.py`
- `docs/wiki-bi/_meta/legacy-semantic-map/README.md`
- `docs/wiki-bi/_meta/legacy-semantic-map/AGENTS.md`
- `tests/contracts/test_legacy_semantic_map_bootstrap.py`
- `tests/contracts/test_legacy_semantic_map_repo_docs.py`

### Responsibilities

- `scripts/legacy_semantic_map/ingress.py` owns ingress schema validation, deterministic ingress paths, index maintenance, and semantic-claim promotion using the existing `claims.py` writer.
- `scripts/legacy_semantic_map/semantic_ingress_guard.py` owns active-wave resolution, legacy-evidence boundary checks, overlap detection, and conservative promotion-gate evaluation. It must stay mechanical and must not interpret business meaning.
- `scripts/legacy_semantic_map/waves.py` exposes a reusable helper that resolves the active or explicitly requested open wave for ingress tooling.
- `bootstrap.py`, `README.md`, and `AGENTS.md` keep the ingress tree and its write boundary visible in both bootstrap registries and the checked-in registry.
- `.codex/skills/wdhp-semantic-map-ingress/` packages the operator-facing instructions and reusable references, but it must reuse the repo-root guard/helper code instead of duplicating semantic logic inside the skill.
- the new contract tests lock path shapes, wave guards, evidence provenance, overlap handling, promotion rules, and skill-packaging expectations.

---

### Task 1: Bootstrap The Ingress Tree And Governance Docs

**Files:**
- Modify: `scripts/legacy_semantic_map/bootstrap.py`
- Modify: `docs/wiki-bi/_meta/legacy-semantic-map/README.md`
- Modify: `docs/wiki-bi/_meta/legacy-semantic-map/AGENTS.md`
- Modify: `tests/contracts/test_legacy_semantic_map_bootstrap.py`
- Modify: `tests/contracts/test_legacy_semantic_map_repo_docs.py`
- Create: `docs/wiki-bi/_meta/legacy-semantic-map/ingress/waves/wave-2026-04-17-semantic-governance-reframe/index.yaml`
- Create: `docs/wiki-bi/_meta/legacy-semantic-map/ingress/waves/wave-2026-04-17-semantic-governance-reframe/question-clusters/.gitkeep`
- Create: `docs/wiki-bi/_meta/legacy-semantic-map/ingress/waves/wave-2026-04-17-semantic-governance-reframe/findings/.gitkeep`

- [ ] **Step 1: Extend the bootstrap and repo-doc contracts so ingress becomes a first-class registry surface**

Update `tests/contracts/test_legacy_semantic_map_bootstrap.py` so `expected_files` also requires:

```python
        "claims/wave-2026-04-16-registry-bootstrap/semantic/.gitkeep",
        "ingress/waves/wave-2026-04-16-registry-bootstrap/index.yaml",
        "ingress/waves/wave-2026-04-16-registry-bootstrap/question-clusters/.gitkeep",
        "ingress/waves/wave-2026-04-16-registry-bootstrap/findings/.gitkeep",
```

Add these bootstrap assertions:

```python
    ingress_index = yaml.safe_load(
        (
            registry_root
            / "ingress"
            / "waves"
            / "wave-2026-04-16-registry-bootstrap"
            / "index.yaml"
        ).read_text(encoding="utf-8")
    )
    assert ingress_index == {
        "wave_id": "wave-2026-04-16-registry-bootstrap",
        "question_clusters": [],
        "findings": [],
    }

    assert "ingress/waves/<wave_id>/" in readme_text
    assert "semantic ingress uses legacy-only business-semantic evidence from `E:\\Projects\\WorkDataHub`" in readme_text
    assert "promotion to final shared truth is also main-thread-only" in readme_text
```

Update `tests/contracts/test_legacy_semantic_map_repo_docs.py` so `expected_paths` also requires:

```python
        SEMANTIC_MAP_ROOT / "AGENTS.md",
        SEMANTIC_MAP_ROOT
        / "ingress"
        / "waves"
        / "wave-2026-04-17-semantic-governance-reframe"
        / "index.yaml",
        SEMANTIC_MAP_ROOT
        / "ingress"
        / "waves"
        / "wave-2026-04-17-semantic-governance-reframe"
        / "question-clusters"
        / ".gitkeep",
        SEMANTIC_MAP_ROOT
        / "ingress"
        / "waves"
        / "wave-2026-04-17-semantic-governance-reframe"
        / "findings"
        / ".gitkeep",
```

Then add these repo-doc assertions:

```python
    agents_text = (SEMANTIC_MAP_ROOT / "AGENTS.md").read_text(encoding="utf-8")
    assert "semantic ingress workflow" in agents_text
    assert "ingress/waves/<wave_id>/" in agents_text
    assert "current repo materials may be read only for routing, duplicate detection, or durable target awareness" in agents_text
    assert "must not be cited as business-semantic evidence for ingress" in agents_text
```

- [ ] **Step 2: Run the bootstrap and repo-doc contracts and confirm they fail before implementation**

Run:

```bash
uv run pytest tests/contracts/test_legacy_semantic_map_bootstrap.py tests/contracts/test_legacy_semantic_map_repo_docs.py -v
```

Expected: fail because the ingress tree, semantic claim bootstrap directory, and ingress-specific README / AGENTS language do not exist yet.

- [ ] **Step 3: Implement ingress bootstrap helpers and update the checked-in guidance**

Modify `scripts/legacy_semantic_map/bootstrap.py` so it creates both the semantic claim directory and an ingress tree for the bootstrap wave:

```python
README_TEXT = """# Legacy Semantic Map

This subtree is an internal discovery ledger for legacy semantic mapping work.
It is not durable wiki content.
It must never be added to `docs/wiki-bi/index.md`.

ingress under `ingress/waves/<wave_id>/` is the discovery front door.
semantic ingress uses legacy-only business-semantic evidence from `E:\\Projects\\WorkDataHub`.
distributed agents may write only under `claims/<wave_id>/`.
semantic ingress may also write proposal-grade records under `ingress/waves/<wave_id>/`.
canonical registry files remain main-thread-managed.
canonical compilation is a main-thread-only operation.
promotion to final shared truth is also main-thread-only.

active owner: the main-thread maintainer of the current semantic-map wave
archive trigger: acceptance of the target durable wiki updates plus disposition of remaining findings for that wave
"""


def _ensure_ingress_wave_tree(registry_root: Path, wave_id: str) -> None:
    for relative_dir in (
        f"ingress/waves/{wave_id}/question-clusters",
        f"ingress/waves/{wave_id}/findings",
    ):
        directory = registry_root / relative_dir
        directory.mkdir(parents=True, exist_ok=True)
        _write_text(directory / ".gitkeep", "")
    _write_yaml(
        registry_root / "ingress" / "waves" / wave_id / "index.yaml",
        {
            "wave_id": wave_id,
            "question_clusters": [],
            "findings": [],
        },
    )
```

Then update the directory creation loop so it includes:

```python
        f"claims/{BOOTSTRAP_WAVE.wave_id}/semantic",
```

and call:

```python
    _ensure_ingress_wave_tree(registry_root, BOOTSTRAP_WAVE.wave_id)
```

Update the checked-in `docs/wiki-bi/_meta/legacy-semantic-map/README.md` to match `README_TEXT`.

Add an ingress-specific section to `docs/wiki-bi/_meta/legacy-semantic-map/AGENTS.md`:

```markdown
## Semantic ingress workflow

- ingress lives under `ingress/waves/<wave_id>/` and is the lighter discovery front door
- semantic ingress may write ingress records under `ingress/waves/<wave_id>/` and new proposal claims under `claims/<wave_id>/semantic/`
- current repo materials may be read only for routing, duplicate detection, or durable target awareness
- current repo materials must not be cited as business-semantic evidence for ingress
- overlap that would require modifying an existing semantic claim or canonical semantic file must stop for user review
```

Create the checked-in active-wave ingress files with these contents:

```yaml
# docs/wiki-bi/_meta/legacy-semantic-map/ingress/waves/wave-2026-04-17-semantic-governance-reframe/index.yaml
wave_id: wave-2026-04-17-semantic-governance-reframe
question_clusters: []
findings: []
```

Then regenerate the bootstrap tree locally if needed:

```bash
uv run python -m scripts.legacy_semantic_map.bootstrap
```

- [ ] **Step 4: Re-run the ingress bootstrap and repo-doc contract files**

Run:

```bash
uv run pytest tests/contracts/test_legacy_semantic_map_bootstrap.py tests/contracts/test_legacy_semantic_map_repo_docs.py -v
```

Expected: pass.

- [ ] **Step 5: Commit the bootstrap and guidance slice**

Run:

```bash
git add scripts/legacy_semantic_map/bootstrap.py docs/wiki-bi/_meta/legacy-semantic-map/README.md docs/wiki-bi/_meta/legacy-semantic-map/AGENTS.md docs/wiki-bi/_meta/legacy-semantic-map/ingress/waves/wave-2026-04-17-semantic-governance-reframe/index.yaml docs/wiki-bi/_meta/legacy-semantic-map/ingress/waves/wave-2026-04-17-semantic-governance-reframe/question-clusters/.gitkeep docs/wiki-bi/_meta/legacy-semantic-map/ingress/waves/wave-2026-04-17-semantic-governance-reframe/findings/.gitkeep tests/contracts/test_legacy_semantic_map_bootstrap.py tests/contracts/test_legacy_semantic_map_repo_docs.py
git commit -m "feat(platform.execution): bootstrap semantic ingress registry surface"
```

### Task 2: Add Ingress Schema, Writer, And Wave Index Maintenance

**Files:**
- Create: `scripts/legacy_semantic_map/ingress.py`
- Create: `tests/contracts/test_legacy_semantic_map_ingress_workflow.py`
- Modify: `scripts/legacy_semantic_map/__init__.py`

- [ ] **Step 1: Write the failing ingress workflow contracts**

Create `tests/contracts/test_legacy_semantic_map_ingress_workflow.py` with this content:

```python
from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from scripts.legacy_semantic_map.bootstrap import bootstrap_semantic_map
from scripts.legacy_semantic_map.claims import ClaimSourceRecord
from scripts.legacy_semantic_map.ingress import (
    INGRESS_KIND_DIRECTORIES,
    IngressPromotionRecommendation,
    IngressRecord,
    LEGACY_WORKSPACE_ID,
    ingress_relative_path,
    write_ingress_record,
)


def _legacy_source(
    relative_path: str,
    *,
    authority: str = "authoritative_semantic_source",
) -> ClaimSourceRecord:
    return ClaimSourceRecord(
        source_ref=relative_path,
        source_type="legacy_doc",
        note="Legacy ingress evidence.",
        workspace_id=LEGACY_WORKSPACE_ID,
        relative_path=relative_path,
        semantic_authority=authority,
    )


def _build_finding() -> IngressRecord:
    return IngressRecord(
        ingress_id="ingress-wave-2026-04-16-registry-bootstrap-customer-status-anchor",
        wave_id="wave-2026-04-16-registry-bootstrap",
        ingress_kind="finding",
        title="Customer status annual anchor",
        granularity_rationale="One conclusion is already stable enough to stand alone.",
        questions=[
            "Is status_year a yearly semantic anchor rather than a generic timestamp label?",
        ],
        candidate_conclusions=[
            "status_year behaves like an annual identity anchor for customer-status semantics.",
        ],
        primary_semantic_sources=[
            _legacy_source("docs/business-background/customer_status_rules.md"),
        ],
        supporting_witness_sources=[
            _legacy_source(
                "src/work_data_hub/customer_status/service.py",
                authority="runtime_witness",
            ),
        ],
        possible_non_equivalences=[
            "status_year is not the same field as snapshot_month.",
        ],
        proxy_usage_refs=[
            "src/work_data_hub/customer_status/service.py",
        ],
        open_points=[
            "Need to confirm whether the same anchor is reused in the manual customer-status export.",
        ],
        promotion_recommendation=IngressPromotionRecommendation(
            recommended_action="hold_ingress",
            rationale="Evidence is discussion-ready but promotion has not been evaluated yet.",
            gate_failures=[],
            requires_user_review=False,
        ),
        promoted_claim_ids=[],
        created_at="2026-04-19T10:00:00Z",
    )


def test_ingress_record_relative_path_shape() -> None:
    record = _build_finding()

    assert INGRESS_KIND_DIRECTORIES == {
        "question_cluster": "question-clusters",
        "finding": "findings",
    }
    assert ingress_relative_path(record) == Path(
        "ingress"
    ) / "waves" / "wave-2026-04-16-registry-bootstrap" / "findings" / (
        "ingress-wave-2026-04-16-registry-bootstrap-customer-status-anchor.yaml"
    )


def test_write_ingress_record_writes_yaml_and_updates_wave_index(tmp_path: Path) -> None:
    registry_root = tmp_path / "legacy-semantic-map"
    bootstrap_semantic_map(registry_root)

    record = _build_finding()
    output_path = write_ingress_record(registry_root, record)

    assert output_path == (
        registry_root
        / "ingress"
        / "waves"
        / "wave-2026-04-16-registry-bootstrap"
        / "findings"
        / "ingress-wave-2026-04-16-registry-bootstrap-customer-status-anchor.yaml"
    )

    payload = yaml.safe_load(output_path.read_text(encoding="utf-8"))
    assert payload["questions"] == [
        "Is status_year a yearly semantic anchor rather than a generic timestamp label?",
    ]
    assert payload["primary_semantic_sources"][0]["workspace_id"] == LEGACY_WORKSPACE_ID
    assert payload["promotion_recommendation"]["recommended_action"] == "hold_ingress"

    index_payload = yaml.safe_load(
        (
            registry_root
            / "ingress"
            / "waves"
            / "wave-2026-04-16-registry-bootstrap"
            / "index.yaml"
        ).read_text(encoding="utf-8")
    )
    assert index_payload["findings"] == [
        {
            "ingress_id": "ingress-wave-2026-04-16-registry-bootstrap-customer-status-anchor",
            "title": "Customer status annual anchor",
            "path": "ingress/waves/wave-2026-04-16-registry-bootstrap/findings/ingress-wave-2026-04-16-registry-bootstrap-customer-status-anchor.yaml",
            "promotion_state": "hold_ingress",
        }
    ]
    assert index_payload["question_clusters"] == []


def test_write_ingress_record_rejects_non_legacy_source_records(tmp_path: Path) -> None:
    registry_root = tmp_path / "legacy-semantic-map"
    bootstrap_semantic_map(registry_root)
    record = _build_finding()
    invalid = IngressRecord(
        **(
            record.to_payload()
            | {
                "primary_semantic_sources": [
                    {
                        "source_ref": "docs/wiki-bi/concepts/customer-status.md",
                        "source_type": "current_wiki",
                        "note": "Current wiki is not ingress evidence.",
                        "workspace_id": "work_data_hub_pro",
                        "relative_path": "docs/wiki-bi/concepts/customer-status.md",
                        "semantic_authority": "runtime_witness",
                    }
                ]
            }
        )
    )

    with pytest.raises(ValueError, match="legacy_work_data_hub"):
        write_ingress_record(registry_root, invalid)
```

- [ ] **Step 2: Run the targeted ingress workflow contract file and confirm it fails**

Run:

```bash
uv run pytest tests/contracts/test_legacy_semantic_map_ingress_workflow.py -v
```

Expected: fail because `scripts.legacy_semantic_map.ingress` does not exist yet.

- [ ] **Step 3: Implement the ingress dataclasses, path helper, and writer**

Create `scripts/legacy_semantic_map/ingress.py` with this structure:

```python
from __future__ import annotations

from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import field
from pathlib import Path

import yaml

from .claims import ClaimSourceRecord
from .waves import require_active_open_wave

LEGACY_WORKSPACE_ID = "legacy_work_data_hub"
INGRESS_KIND_DIRECTORIES = {
    "question_cluster": "question-clusters",
    "finding": "findings",
}
PROMOTION_ACTIONS = (
    "hold_ingress",
    "promote_to_semantic_claim",
    "requires_user_review",
)


@dataclass(frozen=True)
class IngressPromotionRecommendation:
    recommended_action: str
    rationale: str
    gate_failures: list[str] = field(default_factory=list)
    requires_user_review: bool = False

    def __post_init__(self) -> None:
        if self.recommended_action not in PROMOTION_ACTIONS:
            raise ValueError(f"Unsupported recommended_action: {self.recommended_action}")


@dataclass(frozen=True)
class IngressRecord:
    ingress_id: str
    wave_id: str
    ingress_kind: str
    title: str
    granularity_rationale: str
    questions: list[str]
    candidate_conclusions: list[str]
    primary_semantic_sources: list[ClaimSourceRecord]
    supporting_witness_sources: list[ClaimSourceRecord]
    possible_non_equivalences: list[str]
    proxy_usage_refs: list[str]
    open_points: list[str]
    promotion_recommendation: IngressPromotionRecommendation
    promoted_claim_ids: list[str] = field(default_factory=list)
    created_at: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "primary_semantic_sources",
            [
                item if isinstance(item, ClaimSourceRecord) else ClaimSourceRecord(**item)
                for item in self.primary_semantic_sources
            ],
        )
        object.__setattr__(
            self,
            "supporting_witness_sources",
            [
                item if isinstance(item, ClaimSourceRecord) else ClaimSourceRecord(**item)
                for item in self.supporting_witness_sources
            ],
        )
        if not self.questions:
            raise ValueError("Ingress records require at least one question")
        if self.ingress_kind not in INGRESS_KIND_DIRECTORIES:
            raise ValueError(f"Unsupported ingress_kind: {self.ingress_kind}")
        if not self.primary_semantic_sources:
            raise ValueError("Ingress records require at least one primary_semantic_source")
        if not isinstance(self.promotion_recommendation, IngressPromotionRecommendation):
            object.__setattr__(
                self,
                "promotion_recommendation",
                IngressPromotionRecommendation(**self.promotion_recommendation),
            )

    def to_payload(self) -> dict[str, object]:
        return asdict(self)
```

Continue the same file with the deterministic write helpers:

```python
def _validate_legacy_sources(records: list[ClaimSourceRecord]) -> None:
    for record in records:
        if record.workspace_id != LEGACY_WORKSPACE_ID:
            raise ValueError(
                "Ingress evidence must come from legacy_work_data_hub workspace_id"
            )
        if not record.relative_path:
            raise ValueError("Ingress evidence must carry a legacy relative_path")
        if not record.source_type.startswith("legacy_"):
            raise ValueError("Ingress evidence must use legacy_* source_type values")


def ingress_relative_path(record: IngressRecord) -> Path:
    if record.ingress_kind not in INGRESS_KIND_DIRECTORIES:
        raise ValueError(f"Unsupported ingress_kind: {record.ingress_kind}")
    return (
        Path("ingress")
        / "waves"
        / record.wave_id
        / INGRESS_KIND_DIRECTORIES[record.ingress_kind]
        / f"{record.ingress_id}.yaml"
    )


def _load_ingress_index(registry_root: Path, wave_id: str) -> dict[str, object]:
    index_path = registry_root / "ingress" / "waves" / wave_id / "index.yaml"
    return yaml.safe_load(index_path.read_text(encoding="utf-8")) or {
        "wave_id": wave_id,
        "question_clusters": [],
        "findings": [],
    }


def _write_ingress_index(registry_root: Path, wave_id: str, payload: dict[str, object]) -> None:
    index_path = registry_root / "ingress" / "waves" / wave_id / "index.yaml"
    index_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.write_text(
        yaml.safe_dump(payload, sort_keys=False, allow_unicode=False),
        encoding="utf-8",
    )


def write_ingress_record(registry_root: Path, record: IngressRecord) -> Path:
    require_active_open_wave(registry_root, record.wave_id)
    _validate_legacy_sources(record.primary_semantic_sources)
    _validate_legacy_sources(record.supporting_witness_sources)

    output_path = registry_root / ingress_relative_path(record)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        yaml.safe_dump(record.to_payload(), sort_keys=False, allow_unicode=False),
        encoding="utf-8",
    )

    index_payload = _load_ingress_index(registry_root, record.wave_id)
    key = "question_clusters" if record.ingress_kind == "question_cluster" else "findings"
    other_key = "findings" if key == "question_clusters" else "question_clusters"
    entries = {
        item["ingress_id"]: item
        for item in index_payload.get(key, [])
    }
    entries[record.ingress_id] = {
        "ingress_id": record.ingress_id,
        "title": record.title,
        "path": ingress_relative_path(record).as_posix(),
        "promotion_state": record.promotion_recommendation.recommended_action,
    }
    index_payload["wave_id"] = record.wave_id
    index_payload[key] = [entries[item_id] for item_id in sorted(entries)]
    index_payload.setdefault(other_key, [])
    _write_ingress_index(registry_root, record.wave_id, index_payload)
    return output_path
```

Export the new symbols from `scripts/legacy_semantic_map/__init__.py`:

```python
from .ingress import (
    INGRESS_KIND_DIRECTORIES,
    LEGACY_WORKSPACE_ID,
    IngressPromotionRecommendation,
    IngressRecord,
    ingress_relative_path,
    write_ingress_record,
)
```

and add them to `__all__`.

- [ ] **Step 4: Re-run the targeted ingress workflow contracts**

Run:

```bash
uv run pytest tests/contracts/test_legacy_semantic_map_ingress_workflow.py -v
```

Expected: pass.

- [ ] **Step 5: Commit the ingress writer slice**

Run:

```bash
git add scripts/legacy_semantic_map/ingress.py scripts/legacy_semantic_map/__init__.py tests/contracts/test_legacy_semantic_map_ingress_workflow.py
git commit -m "feat(platform.execution): add semantic ingress writer"
```

### Task 3: Add The Mechanical Semantic Ingress Guard

**Files:**
- Create: `scripts/legacy_semantic_map/semantic_ingress_guard.py`
- Create: `tests/contracts/test_legacy_semantic_map_semantic_ingress_guard.py`
- Modify: `scripts/legacy_semantic_map/waves.py`
- Modify: `scripts/legacy_semantic_map/__init__.py`

- [ ] **Step 1: Write the failing guard contracts**

Create `tests/contracts/test_legacy_semantic_map_semantic_ingress_guard.py` with this content:

```python
from __future__ import annotations

from pathlib import Path

import yaml

from scripts.legacy_semantic_map.bootstrap import bootstrap_semantic_map
from scripts.legacy_semantic_map.ingress import IngressPromotionRecommendation, IngressRecord, LEGACY_WORKSPACE_ID
from scripts.legacy_semantic_map.claims import ClaimSourceRecord
from scripts.legacy_semantic_map.semantic_ingress_guard import (
    IngressGuardResult,
    SemanticPromotionDraft,
    guard_ingress_record,
)


def _legacy_source(relative_path: str, *, authority: str) -> ClaimSourceRecord:
    return ClaimSourceRecord(
        source_ref=relative_path,
        source_type="legacy_doc" if relative_path.endswith(".md") else "legacy_code",
        note="Legacy ingress guard fixture.",
        workspace_id=LEGACY_WORKSPACE_ID,
        relative_path=relative_path,
        semantic_authority=authority,
    )


def _record() -> IngressRecord:
    return IngressRecord(
        ingress_id="ingress-wave-2026-04-16-registry-bootstrap-status-year-anchor",
        wave_id="wave-2026-04-16-registry-bootstrap",
        ingress_kind="finding",
        title="Status year anchor",
        granularity_rationale="One stable conclusion is ready for standalone review.",
        questions=["Is status_year an annual anchor for customer-status semantics?"],
        candidate_conclusions=[
            "status_year behaves like an annual identity anchor rather than a generic timestamp label.",
        ],
        primary_semantic_sources=[
            _legacy_source(
                "docs/business-background/customer_status_rules.md",
                authority="authoritative_semantic_source",
            )
        ],
        supporting_witness_sources=[
            _legacy_source(
                "src/work_data_hub/customer_status/service.py",
                authority="runtime_witness",
            )
        ],
        possible_non_equivalences=["status_year is not snapshot_month"],
        proxy_usage_refs=["src/work_data_hub/customer_status/service.py"],
        open_points=["Manual export reuse still needs confirmation."],
        promotion_recommendation=IngressPromotionRecommendation(
            recommended_action="hold_ingress",
            rationale="Not evaluated yet.",
        ),
        created_at="2026-04-19T11:00:00Z",
    )


def _promotion() -> SemanticPromotionDraft:
    return SemanticPromotionDraft(
        semantic_id="sem-rule-status-year-identity-anchor",
        semantic_node_type="semantic_rule",
        title="Status year identity anchor",
        summary="status_year is an annual semantic anchor for customer-status semantics.",
        business_conclusion="status_year is an annual identity anchor for customer-status semantics, not a generic timestamp label.",
        non_equivalent_to=["sem-non-equivalence-status-year-vs-snapshot-month"],
        confidence="high",
        last_verified="2026-04-19",
        main_conclusion_stable=True,
        open_points_do_not_overturn=True,
    )


def test_guard_resolves_active_open_wave_and_allowed_targets(tmp_path: Path) -> None:
    registry_root = tmp_path / "legacy-semantic-map"
    bootstrap_semantic_map(registry_root)

    result = guard_ingress_record(registry_root, _record(), _promotion())

    assert result.wave_id == "wave-2026-04-16-registry-bootstrap"
    assert result.allowed_write_targets == [
        "ingress/waves/wave-2026-04-16-registry-bootstrap/findings",
        "claims/wave-2026-04-16-registry-bootstrap/semantic",
    ]
    assert result.promotion_status == "ready"
    assert result.evidence_boundary_failures == []
    assert result.overlap_hits == []


def test_guard_rejects_current_repo_business_evidence(tmp_path: Path) -> None:
    registry_root = tmp_path / "legacy-semantic-map"
    bootstrap_semantic_map(registry_root)
    record = _record()
    invalid = IngressRecord(
        **(
            record.to_payload()
            | {
                "primary_semantic_sources": [
                    {
                        "source_ref": "docs/wiki-bi/concepts/customer-status.md",
                        "source_type": "current_wiki",
                        "note": "Current wiki is not valid ingress evidence.",
                        "workspace_id": "work_data_hub_pro",
                        "relative_path": "docs/wiki-bi/concepts/customer-status.md",
                        "semantic_authority": "implementation_hint",
                    }
                ]
            }
        )
    )

    result = guard_ingress_record(registry_root, invalid, _promotion())

    assert result.promotion_status == "blocked"
    assert "non_legacy_primary_source" in result.evidence_boundary_failures


def test_guard_requires_user_review_when_semantic_id_already_exists(tmp_path: Path) -> None:
    registry_root = tmp_path / "legacy-semantic-map"
    bootstrap_semantic_map(registry_root)
    canonical_path = (
        registry_root
        / "semantic"
        / "rules"
        / "sem-rule-status-year-identity-anchor.yaml"
    )
    canonical_path.parent.mkdir(parents=True, exist_ok=True)
    canonical_path.write_text(
        yaml.safe_dump(
            {
                "semantic_id": "sem-rule-status-year-identity-anchor",
                "semantic_node_type": "semantic_rule",
            },
            sort_keys=False,
            allow_unicode=False,
        ),
        encoding="utf-8",
    )

    result = guard_ingress_record(registry_root, _record(), _promotion())

    assert result.promotion_status == "requires_user_review"
    assert result.requires_user_review is True
    assert result.overlap_hits[0]["path"] == (
        "semantic/rules/sem-rule-status-year-identity-anchor.yaml"
    )
```

- [ ] **Step 2: Run the targeted guard contract file and confirm it fails**

Run:

```bash
uv run pytest tests/contracts/test_legacy_semantic_map_semantic_ingress_guard.py -v
```

Expected: fail because the guard module and wave-resolution helper do not exist yet.

- [ ] **Step 3: Implement the reusable open-wave resolver and the guard module**

Add this helper to `scripts/legacy_semantic_map/waves.py`:

```python
def resolve_requested_or_active_open_wave(
    registry_root: Path,
    wave_id: str | None = None,
) -> tuple[str, dict[str, object]]:
    active_wave_id, waves = wave_lookup(registry_root)
    target_wave_id = wave_id or active_wave_id
    if target_wave_id not in waves:
        raise ValueError(f"Unknown wave_id: {target_wave_id}")
    return target_wave_id, require_active_open_wave(registry_root, target_wave_id)
```

Create `scripts/legacy_semantic_map/semantic_ingress_guard.py` with this structure:

```python
from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

import yaml

from .ingress import INGRESS_KIND_DIRECTORIES, IngressRecord, LEGACY_WORKSPACE_ID
from .waves import resolve_requested_or_active_open_wave


@dataclass(frozen=True)
class SemanticPromotionDraft:
    semantic_id: str
    semantic_node_type: str
    title: str
    summary: str
    business_conclusion: str
    non_equivalent_to: list[str]
    confidence: str
    last_verified: str
    main_conclusion_stable: bool
    open_points_do_not_overturn: bool


@dataclass(frozen=True)
class IngressGuardResult:
    wave_id: str
    allowed_write_targets: list[str]
    promotion_status: str
    promotion_gate_failures: list[str]
    evidence_boundary_failures: list[str]
    overlap_hits: list[dict[str, str]]
    requires_user_review: bool

    def to_payload(self) -> dict[str, object]:
        return asdict(self)
```

Continue the same file with the guard logic:

```python
def _source_failure_prefix(source_kind: str) -> str:
    return f"non_legacy_{source_kind}_source"


def _check_sources(records, *, source_kind: str) -> list[str]:
    failures: list[str] = []
    for record in records:
        if record.workspace_id != LEGACY_WORKSPACE_ID:
            failures.append(_source_failure_prefix(source_kind))
        if not record.relative_path:
            failures.append(f"{source_kind}_source_missing_relative_path")
        if not record.source_type.startswith("legacy_"):
            failures.append(_source_failure_prefix(source_kind))
    return sorted(set(failures))


def _overlap_hits(registry_root: Path, promotion: SemanticPromotionDraft | None) -> list[dict[str, str]]:
    if promotion is None:
        return []
    hits: list[dict[str, str]] = []
    for path in (registry_root / "claims").rglob("*.yaml"):
        payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        if payload.get("claim_target_id") == promotion.semantic_id:
            hits.append(
                {
                    "path": path.resolve().relative_to(registry_root.resolve()).as_posix(),
                    "match_reason": "existing_semantic_claim_target",
                }
            )
    for path in (registry_root / "semantic").rglob("*.yaml"):
        payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        if payload.get("semantic_id") == promotion.semantic_id:
            hits.append(
                {
                    "path": path.resolve().relative_to(registry_root.resolve()).as_posix(),
                    "match_reason": "existing_canonical_semantic_id",
                }
            )
    deduped = {json.dumps(item, sort_keys=True): item for item in hits}
    return [deduped[key] for key in sorted(deduped)]


def guard_ingress_record(
    registry_root: Path,
    record: IngressRecord,
    promotion: SemanticPromotionDraft | None = None,
    *,
    wave_id: str | None = None,
) -> IngressGuardResult:
    resolved_wave_id, _ = resolve_requested_or_active_open_wave(registry_root, wave_id or record.wave_id)
    evidence_failures = _check_sources(
        record.primary_semantic_sources,
        source_kind="primary",
    ) + _check_sources(
        record.supporting_witness_sources,
        source_kind="supporting",
    )
    evidence_failures = sorted(set(evidence_failures))
    overlap_hits = _overlap_hits(registry_root, promotion)

    gate_failures: list[str] = []
    if not record.primary_semantic_sources:
        gate_failures.append("missing_primary_semantic_source")
    if not record.supporting_witness_sources:
        gate_failures.append("missing_supporting_witness_source")
    if promotion is None:
        gate_failures.append("missing_promotion_draft")
    else:
        if not promotion.main_conclusion_stable:
            gate_failures.append("main_conclusion_not_stable")
        if not promotion.open_points_do_not_overturn:
            gate_failures.append("open_points_may_overturn_conclusion")
        if not promotion.business_conclusion.strip():
            gate_failures.append("missing_business_conclusion")
        if not promotion.semantic_node_type.strip():
            gate_failures.append("missing_semantic_node_type")

    requires_user_review = bool(overlap_hits)
    if requires_user_review:
        promotion_status = "requires_user_review"
    elif evidence_failures or gate_failures:
        promotion_status = "blocked"
    else:
        promotion_status = "ready"

    return IngressGuardResult(
        wave_id=resolved_wave_id,
        allowed_write_targets=[
            f"ingress/waves/{resolved_wave_id}/{INGRESS_KIND_DIRECTORIES[record.ingress_kind]}",
            f"claims/{resolved_wave_id}/semantic",
        ],
        promotion_status=promotion_status,
        promotion_gate_failures=sorted(set(gate_failures)),
        evidence_boundary_failures=evidence_failures,
        overlap_hits=overlap_hits,
        requires_user_review=requires_user_review,
    )
```

Add a small CLI at the bottom of the same file:

```python
def main(argv: Sequence[str] | None = None) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry-root", type=Path, required=True)
    parser.add_argument("--record", type=Path, required=True)
    parser.add_argument("--promotion", type=Path)
    args = parser.parse_args(argv)

    record = IngressRecord(**yaml.safe_load(args.record.read_text(encoding="utf-8")))
    promotion = None
    if args.promotion:
        promotion = SemanticPromotionDraft(
            **yaml.safe_load(args.promotion.read_text(encoding="utf-8"))
        )
    result = guard_ingress_record(args.registry_root.resolve(), record, promotion)
    print(json.dumps(result.to_payload(), indent=2))


if __name__ == "__main__":
    main()
```

Export `SemanticPromotionDraft`, `IngressGuardResult`, `guard_ingress_record`, and `resolve_requested_or_active_open_wave` from `scripts/legacy_semantic_map/__init__.py`.

- [ ] **Step 4: Re-run the targeted guard contracts**

Run:

```bash
uv run pytest tests/contracts/test_legacy_semantic_map_semantic_ingress_guard.py -v
```

Expected: pass.

- [ ] **Step 5: Commit the guard slice**

Run:

```bash
git add scripts/legacy_semantic_map/semantic_ingress_guard.py scripts/legacy_semantic_map/waves.py scripts/legacy_semantic_map/__init__.py tests/contracts/test_legacy_semantic_map_semantic_ingress_guard.py
git commit -m "feat(platform.execution): add semantic ingress guard"
```

### Task 4: Add Conservative Auto-Promotion From Ingress To Semantic Claims

**Files:**
- Modify: `scripts/legacy_semantic_map/ingress.py`
- Modify: `scripts/legacy_semantic_map/__init__.py`
- Modify: `tests/contracts/test_legacy_semantic_map_ingress_workflow.py`

- [ ] **Step 1: Extend the ingress workflow contract to require minimal semantic-claim promotion**

Append these tests to `tests/contracts/test_legacy_semantic_map_ingress_workflow.py`:

```python
from scripts.legacy_semantic_map.semantic_ingress_guard import SemanticPromotionDraft


def _promotion_draft() -> SemanticPromotionDraft:
    return SemanticPromotionDraft(
        semantic_id="sem-rule-status-year-identity-anchor",
        semantic_node_type="semantic_rule",
        title="Status year identity anchor",
        summary="status_year is an annual semantic anchor for customer-status interpretation.",
        business_conclusion="status_year is an annual identity anchor for customer-status semantics, not a generic timestamp label.",
        non_equivalent_to=["sem-non-equivalence-status-year-vs-snapshot-month"],
        confidence="high",
        last_verified="2026-04-19",
        main_conclusion_stable=True,
        open_points_do_not_overturn=True,
    )


def test_promote_ingress_record_writes_minimum_semantic_claim(tmp_path: Path) -> None:
    registry_root = tmp_path / "legacy-semantic-map"
    bootstrap_semantic_map(registry_root)

    record = _build_finding()
    write_ingress_record(registry_root, record)
    claim_path = promote_ingress_record(registry_root, record, _promotion_draft())

    assert claim_path == (
        registry_root
        / "claims"
        / "wave-2026-04-16-registry-bootstrap"
        / "semantic"
        / "claim-wave-2026-04-16-registry-bootstrap-status-year-identity-anchor.yaml"
    )

    payload = yaml.safe_load(claim_path.read_text(encoding="utf-8"))
    assert payload["claim_scope"] == "semantic"
    assert payload["claim_target_id"] == "sem-rule-status-year-identity-anchor"
    assert payload["semantic_findings"][0] == {
        "semantic_id": "sem-rule-status-year-identity-anchor",
        "semantic_node_type": "semantic_rule",
        "title": "Status year identity anchor",
        "summary": "status_year is an annual semantic anchor for customer-status interpretation.",
        "business_conclusion": "status_year is an annual identity anchor for customer-status semantics, not a generic timestamp label.",
        "primary_source_refs": ["docs/business-background/customer_status_rules.md"],
        "supporting_source_refs": ["src/work_data_hub/customer_status/service.py"],
        "semantic_authority": "authoritative_semantic_source",
        "durable_target_pages": [],
        "confidence": "high",
        "last_verified": "2026-04-19",
        "open_questions": [
            "Need to confirm whether the same anchor is reused in the manual customer-status export.",
        ],
        "non_equivalent_to": ["sem-non-equivalence-status-year-vs-snapshot-month"],
        "proposal_governance": None,
    }

    ingress_payload = yaml.safe_load(
        (
            registry_root
            / "ingress"
            / "waves"
            / "wave-2026-04-16-registry-bootstrap"
            / "findings"
            / "ingress-wave-2026-04-16-registry-bootstrap-customer-status-anchor.yaml"
        ).read_text(encoding="utf-8")
    )
    assert ingress_payload["promoted_claim_ids"] == [
        "claim-wave-2026-04-16-registry-bootstrap-status-year-identity-anchor"
    ]


def test_promote_ingress_record_rejects_structurally_blocked_promotion(tmp_path: Path) -> None:
    registry_root = tmp_path / "legacy-semantic-map"
    bootstrap_semantic_map(registry_root)

    record = _build_finding()
    blocked_draft = SemanticPromotionDraft(
        **(_promotion_draft().__dict__ | {"open_points_do_not_overturn": False})
    )

    with pytest.raises(ValueError, match="Promotion is not structurally allowed"):
        promote_ingress_record(registry_root, record, blocked_draft)
```

- [ ] **Step 2: Run the ingress workflow contract file again and confirm the new promotion assertions fail**

Run:

```bash
uv run pytest tests/contracts/test_legacy_semantic_map_ingress_workflow.py -v
```

Expected: fail because `promote_ingress_record` does not exist yet.

- [ ] **Step 3: Implement the promotion helper on top of the existing semantic claim writer**

Extend `scripts/legacy_semantic_map/ingress.py` with:

```python
from .claims import ClaimArtifact, ClaimSemanticFindingRecord, write_claim_artifact
from .semantic_ingress_guard import SemanticPromotionDraft, guard_ingress_record


def _promoted_claim_id(wave_id: str, semantic_id: str) -> str:
    return f"claim-{wave_id}-{semantic_id.removeprefix('sem-')}"


def promote_ingress_record(
    registry_root: Path,
    record: IngressRecord,
    promotion: SemanticPromotionDraft,
) -> Path:
    guard_result = guard_ingress_record(registry_root, record, promotion)
    if guard_result.promotion_status != "ready":
        raise ValueError(
            f"Promotion is not structurally allowed: {guard_result.promotion_status}"
        )

    claim_id = _promoted_claim_id(record.wave_id, promotion.semantic_id)
    claim = ClaimArtifact(
        claim_id=claim_id,
        wave_id=record.wave_id,
        claim_scope="semantic",
        claim_target_id=promotion.semantic_id,
        sources_read=record.primary_semantic_sources + record.supporting_witness_sources,
        objects_discovered=[],
        edges_added=[],
        candidates_raised=[],
        semantic_findings=[
            ClaimSemanticFindingRecord(
                semantic_id=promotion.semantic_id,
                semantic_node_type=promotion.semantic_node_type,
                title=promotion.title,
                summary=promotion.summary,
                business_conclusion=promotion.business_conclusion,
                primary_source_refs=[
                    item.relative_path or item.source_ref
                    for item in record.primary_semantic_sources
                ],
                supporting_source_refs=[
                    item.relative_path or item.source_ref
                    for item in record.supporting_witness_sources
                ],
                semantic_authority=(
                    record.primary_semantic_sources[0].semantic_authority
                    or "authoritative_semantic_source"
                ),
                durable_target_pages=[],
                confidence=promotion.confidence,
                last_verified=promotion.last_verified,
                open_questions=record.open_points,
                non_equivalent_to=promotion.non_equivalent_to,
                proposal_governance=None,
            )
        ],
        open_questions=record.open_points,
        compiled_into=[],
        submitted_at=record.created_at,
    )
    claim_path = write_claim_artifact(registry_root, claim)

    promoted_record = IngressRecord(
        **(
            record.to_payload()
            | {
                "promotion_recommendation": {
                    "recommended_action": "promote_to_semantic_claim",
                    "rationale": "All structural promotion gates passed.",
                    "gate_failures": [],
                    "requires_user_review": False,
                },
                "promoted_claim_ids": [claim_id],
            }
        )
    )
    write_ingress_record(registry_root, promoted_record)
    return claim_path
```

Export `promote_ingress_record` from `scripts/legacy_semantic_map/__init__.py`.

- [ ] **Step 4: Re-run the ingress workflow contracts**

Run:

```bash
uv run pytest tests/contracts/test_legacy_semantic_map_ingress_workflow.py -v
```

Expected: pass.

- [ ] **Step 5: Commit the promotion slice**

Run:

```bash
git add scripts/legacy_semantic_map/ingress.py scripts/legacy_semantic_map/__init__.py tests/contracts/test_legacy_semantic_map_ingress_workflow.py
git commit -m "feat(platform.execution): add semantic ingress promotion workflow"
```

### Task 5: Package The Repo-Local Skill And Reference Docs

**Files:**
- Create: `.codex/skills/wdhp-semantic-map-ingress/SKILL.md`
- Create: `.codex/skills/wdhp-semantic-map-ingress/references/ingress-template.md`
- Create: `.codex/skills/wdhp-semantic-map-ingress/references/promotion-gates.md`
- Create: `.codex/skills/wdhp-semantic-map-ingress/references/claim-minimum-fields.md`
- Create: `.codex/skills/wdhp-semantic-map-ingress/scripts/semantic_ingress_guard.py`
- Create: `tests/contracts/test_legacy_semantic_map_ingress_skill_docs.py`

- [ ] **Step 1: Write the failing skill-packaging contract**

Create `tests/contracts/test_legacy_semantic_map_ingress_skill_docs.py` with this content:

```python
from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL_ROOT = REPO_ROOT / ".codex" / "skills" / "wdhp-semantic-map-ingress"


def test_semantic_ingress_skill_assets_exist_and_reference_repo_guard() -> None:
    expected_paths = [
        SKILL_ROOT / "SKILL.md",
        SKILL_ROOT / "references" / "ingress-template.md",
        SKILL_ROOT / "references" / "promotion-gates.md",
        SKILL_ROOT / "references" / "claim-minimum-fields.md",
        SKILL_ROOT / "scripts" / "semantic_ingress_guard.py",
    ]
    for path in expected_paths:
        assert path.exists(), f"Missing skill asset: {path}"

    skill_text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
    assert "docs/wiki-bi/_meta/legacy-semantic-map/ingress/" in skill_text
    assert "E:\\Projects\\WorkDataHub" in skill_text
    assert "must not write `docs/wiki-bi/` durable pages" in skill_text
    assert "scripts/legacy_semantic_map/semantic_ingress_guard.py" in skill_text
    assert "call the ingress guard helper again for promotion evaluation" in skill_text
    assert "stop and ask the user before modifying an existing semantic claim or canonical semantic file" in skill_text

    wrapper_text = (SKILL_ROOT / "scripts" / "semantic_ingress_guard.py").read_text(
        encoding="utf-8"
    )
    assert "from scripts.legacy_semantic_map.semantic_ingress_guard import main" in wrapper_text
```

- [ ] **Step 2: Run the skill-packaging contract and confirm it fails**

Run:

```bash
uv run pytest tests/contracts/test_legacy_semantic_map_ingress_skill_docs.py -v
```

Expected: fail because the new skill package does not exist yet.

- [ ] **Step 3: Create the skill, references, and wrapper script**

Create `.codex/skills/wdhp-semantic-map-ingress/SKILL.md` with this content:

```markdown
---
name: wdhp-semantic-map-ingress
description: Use only when the user explicitly invokes semantic-ingress work for `docs/wiki-bi/_meta/legacy-semantic-map/ingress/` or asks to capture legacy business semantics through the ingress workflow. Do not auto-activate for ordinary wiki work or for canonical semantic compilation.
---

# WDHP Semantic Map Ingress

## Overview

Use this skill to capture legacy-only business-semantic findings into the semantic-map ingress ledger under `docs/wiki-bi/_meta/legacy-semantic-map/ingress/`.

This skill may:

- write ingress records under `ingress/waves/<wave_id>/`
- auto-promote structurally ready ingress findings into new proposal claims under `claims/<wave_id>/semantic/`

This skill must not:

- write `docs/wiki-bi/` durable pages
- compile canonical semantic files automatically
- modify existing semantic claims or canonical semantic files without user confirmation

## Workflow

1. Resolve the active or explicitly requested open wave.
2. Draft the ingress record and call `scripts/legacy_semantic_map/semantic_ingress_guard.py` before writing.
3. Read only legacy evidence from `E:\Projects\WorkDataHub`.
4. Decide whether the ingress unit is a `question_cluster` or a `finding`.
5. Write the ingress record and update the ingress index.
6. Call the ingress guard helper again for promotion evaluation.
7. If promotion is structurally ready, promote into `claims/<wave_id>/semantic/`.
8. Stop and ask the user before modifying an existing semantic claim or canonical semantic file.

## Boundary Rules

- business-semantic evidence must come from `E:\Projects\WorkDataHub`
- current repo materials may be read only for routing, duplicate detection, or durable target awareness
- current repo materials must not be cited as business-semantic evidence for ingress
- use `scripts/legacy_semantic_map/semantic_ingress_guard.py` for structural checks
- use `references/ingress-template.md`, `references/promotion-gates.md`, and `references/claim-minimum-fields.md` when drafting the ingress and promoted claim payloads
```

Create `.codex/skills/wdhp-semantic-map-ingress/references/ingress-template.md`:

```markdown
# Ingress Template

- `ingress_id`
- `wave_id`
- `ingress_kind`
- `title`
- `granularity_rationale`
- `questions`
- `candidate_conclusions`
- `primary_semantic_sources`
- `supporting_witness_sources`
- `possible_non_equivalences`
- `proxy_usage_refs`
- `open_points`
- `promotion_recommendation`
```

Create `.codex/skills/wdhp-semantic-map-ingress/references/promotion-gates.md`:

```markdown
# Promotion Gates

Auto-promotion is allowed only when all of these are true:

- at least one primary semantic source exists
- at least one supporting witness source exists
- all cited evidence is legacy-only
- the business conclusion is stable
- a semantic node type is named confidently
- remaining open points do not overturn the main conclusion
- no existing semantic claim or canonical semantic file would need modification
```

Create `.codex/skills/wdhp-semantic-map-ingress/references/claim-minimum-fields.md`:

```markdown
# Minimum Promoted Claim Fields

- `semantic_id`
- `semantic_node_type`
- `title`
- `summary`
- `business_conclusion`
- `primary_source_refs`
- `supporting_source_refs`
- `semantic_authority`
- `non_equivalent_to`
- `open_questions`
- `confidence`
- `last_verified`
```

Create the thin wrapper `.codex/skills/wdhp-semantic-map-ingress/scripts/semantic_ingress_guard.py`:

```python
from scripts.legacy_semantic_map.semantic_ingress_guard import main


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run the skill-packaging contract**

Run:

```bash
uv run pytest tests/contracts/test_legacy_semantic_map_ingress_skill_docs.py -v
```

Expected: pass.

- [ ] **Step 5: Commit the skill package**

Run:

```bash
git add .codex/skills/wdhp-semantic-map-ingress tests/contracts/test_legacy_semantic_map_ingress_skill_docs.py
git commit -m "docs(docs.architecture): add semantic ingress skill package"
```

## Validation

Run:

```bash
uv sync --dev
uv run pytest tests/contracts/test_legacy_semantic_map_bootstrap.py tests/contracts/test_legacy_semantic_map_repo_docs.py tests/contracts/test_legacy_semantic_map_ingress_workflow.py tests/contracts/test_legacy_semantic_map_semantic_ingress_guard.py tests/contracts/test_legacy_semantic_map_ingress_skill_docs.py tests/contracts/test_legacy_semantic_map_wave_guarding.py tests/contracts/test_legacy_semantic_map_semantic_schema.py -v
uv run pytest -v
git diff -- docs/wiki-bi/_meta/legacy-semantic-map scripts/legacy_semantic_map .codex/skills/wdhp-semantic-map-ingress tests/contracts
git status -sb
```

Expected:

- the semantic-map bootstrap tree now includes ingress directories and a semantic claim directory
- ingress records are written only under `ingress/waves/<wave_id>/question-clusters/` or `ingress/waves/<wave_id>/findings/`
- ingress evidence fails closed when it cites current-repo pages as business-semantic evidence
- the guard resolves the active open wave, reports allowed write targets, and returns `blocked`, `ready`, or `requires_user_review`
- auto-promotion writes only new semantic claim artifacts under `claims/<wave_id>/semantic/`
- auto-promotion stops before any existing semantic claim or canonical semantic file would need modification
- the local skill package exists, reuses the repo-root guard, and documents the legacy-only evidence boundary
- the full suite still passes

## Spec Coverage Check

- `ingress` becomes the lighter discovery front door: covered by Task 1 and Task 2.
- the new write surface remains inside `docs/wiki-bi/_meta/legacy-semantic-map/`: covered by Task 1 and Task 2.
- legacy-only evidence boundary: enforced in Task 2 and Task 3.
- conservative promotion into `claims/<wave_id>/semantic/`: covered by Task 3 and Task 4.
- no silent modification of existing semantic claims or canonical semantic files: covered by Task 3 and Task 4.
- repo-local skill packaging with references: covered by Task 5.

No further split is required unless execution expands into canonical compiler changes or wave-closeout/reporting changes. If that happens, stop and write a follow-on plan instead of widening this slice.

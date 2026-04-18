from __future__ import annotations

from pathlib import Path

import yaml

from scripts.legacy_semantic_map.bootstrap import bootstrap_semantic_map
from scripts.legacy_semantic_map.claims import (
    ClaimArtifact,
    ClaimSemanticFindingRecord,
    ClaimSourceRecord,
    write_claim_artifact,
)
from scripts.legacy_semantic_map.compiler import compile_claim_artifacts
from scripts.legacy_semantic_map.reporting import generate_reports


SUCCESSOR_WAVE_ID = "wave-2026-04-17-semantic-governance-reframe"


def _seed_successor_wave(registry_root: Path) -> None:
    payload = yaml.safe_load((registry_root / "waves" / "index.yaml").read_text(encoding="utf-8"))
    payload["active_wave_id"] = SUCCESSOR_WAVE_ID
    payload["waves"] = [
        {
            "wave_id": SUCCESSOR_WAVE_ID,
            "title": "Semantic governance reframe",
            "status": "active",
            "wave_ordinal": 4,
            "opened_at": "2026-04-17",
            "seeded_entry_surfaces": [],
            "seeded_high_priority_source_families": [],
            "admitted_subsystems": [],
            "durable_wiki_targets_accepted": False,
            "findings_disposition_complete": False,
            "depends_on_active_wave_working_state": False,
            "closed_at": None,
        }
    ]
    (registry_root / "waves" / "index.yaml").write_text(
        yaml.safe_dump(payload, sort_keys=False, allow_unicode=False),
        encoding="utf-8",
    )


def _run_successor_wave_reporting(tmp_path: Path) -> dict[str, str]:
    registry_root = tmp_path / "legacy-semantic-map"
    bootstrap_semantic_map(registry_root)
    _seed_successor_wave(registry_root)

    claim = ClaimArtifact(
        claim_id="claim-wave-2026-04-17-semantic-governance-reframe-customer-status-core",
        wave_id=SUCCESSOR_WAVE_ID,
        claim_scope="semantic",
        claim_target_id="sem-concept-customer-status",
        sources_read=[
            ClaimSourceRecord(
                source_ref="docs/business-background/客户主数据回填与状态来源分析.md",
                source_type="legacy_doc",
                note="Auxiliary-view fixture source.",
                workspace_id="legacy_work_data_hub",
                relative_path="docs/business-background/客户主数据回填与状态来源分析.md",
                semantic_authority="authoritative_semantic_source",
            )
        ],
        objects_discovered=[],
        edges_added=[],
        candidates_raised=[],
        semantic_findings=[
            ClaimSemanticFindingRecord(
                semantic_id="sem-concept-customer-status",
                semantic_node_type="semantic_concept",
                title="Customer status",
                summary="Customer status is a distinct semantic layer.",
                business_conclusion="Customer status is a distinct semantic layer.",
                primary_source_refs=["docs/business-background/客户主数据回填与状态来源分析.md"],
                supporting_source_refs=["docs/wiki-bi/concepts/customer-status.md"],
                semantic_authority="authoritative_semantic_source",
                durable_target_pages=["docs/wiki-bi/concepts/customer-status.md"],
                confidence="high",
                last_verified="2026-04-18",
                open_questions=[],
            )
        ],
        open_questions=[],
        compiled_into=["docs/wiki-bi/concepts/customer-status.md"],
        submitted_at="2026-04-18T00:00:00Z",
    )
    claim_path = write_claim_artifact(registry_root, claim)
    compile_claim_artifacts(registry_root, [claim_path])
    result = generate_reports(registry_root)
    return {
        "coverage_status_path": result.current_coverage_report.as_posix(),
        "integrity_status_path": result.current_integrity_report.as_posix(),
        "semantic_discovery_status_path": (
            registry_root
            / "reports"
            / "waves"
            / SUCCESSOR_WAVE_ID
            / "semantic-discovery-status.json"
        ).as_posix(),
        "semantic_readiness_status_path": (
            registry_root
            / "reports"
            / "waves"
            / SUCCESSOR_WAVE_ID
            / "semantic-readiness-status.json"
        ).as_posix(),
    }


def test_auxiliary_views_do_not_replace_authoritative_reports(tmp_path: Path) -> None:
    reports = _run_successor_wave_reporting(tmp_path)

    assert reports["coverage_status_path"].endswith("coverage-status.json")
    assert reports["integrity_status_path"].endswith("integrity-status.json")
    assert reports["semantic_discovery_status_path"].endswith("semantic-discovery-status.json")
    assert reports["semantic_readiness_status_path"].endswith("semantic-readiness-status.json")
    assert Path(reports["semantic_discovery_status_path"]).exists()
    assert Path(reports["semantic_readiness_status_path"]).exists()


from __future__ import annotations

import json
from pathlib import Path

import yaml

from scripts.legacy_semantic_map.pilot import FIRST_WAVE_PILOT_WAVE_ID

REPO_ROOT = Path(__file__).resolve().parents[2]
LEGACY_REPO_ROOT = Path("E:/Projects/WorkDataHub")
SEMANTIC_MAP_ROOT = REPO_ROOT / "docs" / "wiki-bi" / "_meta" / "legacy-semantic-map"
SUCCESSOR_WAVE_ID = "wave-2026-04-17-semantic-governance-reframe"
TIER_A_SURFACES = [
    "annuity_performance",
    "annual_award",
    "annual_loss",
    "annuity_income",
]
TIER_B_SURFACES = [
    "customer_mdm",
    "company_lookup_queue",
    "reference_sync",
]


def test_first_wave_pilot_repo_state_is_populated_and_real_evidence_backed() -> None:
    waves_index = yaml.safe_load(
        (SEMANTIC_MAP_ROOT / "waves" / "index.yaml").read_text(encoding="utf-8")
    )
    assert waves_index["active_wave_id"] == SUCCESSOR_WAVE_ID
    wave_lookup = {item["wave_id"]: item for item in waves_index["waves"]}

    bootstrap_wave = wave_lookup["wave-2026-04-16-registry-bootstrap"]
    assert bootstrap_wave["status"] == "closed"
    assert bootstrap_wave["closed_at"] == "2026-04-17"

    pilot_wave = wave_lookup[FIRST_WAVE_PILOT_WAVE_ID]
    assert pilot_wave["status"] == "closed"
    assert pilot_wave["closed_at"] == "2026-04-17"
    assert pilot_wave["durable_wiki_targets_accepted"] is True
    assert pilot_wave["findings_disposition_complete"] is True
    assert pilot_wave["seeded_entry_surfaces"] == [*TIER_A_SURFACES, *TIER_B_SURFACES]
    assert pilot_wave["pilot_depth_tiers"] == {
        "tier_a": TIER_A_SURFACES,
        "tier_b": TIER_B_SURFACES,
    }
    assert (REPO_ROOT / pilot_wave["pilot_execution_note"]).exists()

    successor_wave = wave_lookup[SUCCESSOR_WAVE_ID]
    assert successor_wave["status"] == "active"
    assert successor_wave["closed_at"] is None
    families = yaml.safe_load(
        (SEMANTIC_MAP_ROOT / "sources" / "families.yaml").read_text(encoding="utf-8")
    )["seeded_high_priority_source_families"]
    family_prefixes = {
        family["family_id"]: tuple(family["source_ref_prefixes"])
        for family in families
    }
    assert family_prefixes["legacy-domain-capability-maps"] == (
        "docs/domains/",
        "docs/guides/domain-migration/",
    )
    assert family_prefixes["legacy-operator-runtime-surfaces"] == (
        "src/work_data_hub/cli/",
        "src/work_data_hub/orchestration/",
    )
    assert family_prefixes["legacy-identity-and-reference-runtime"] == (
        "src/work_data_hub/services/",
        "src/work_data_hub/reference/",
        "src/work_data_hub/backfill/",
    )

    claim_paths = sorted(
        path
        for path in (SEMANTIC_MAP_ROOT / "claims" / FIRST_WAVE_PILOT_WAVE_ID).rglob("*.yaml")
    )
    assert len(claim_paths) == 18

    claim_payloads = [
        yaml.safe_load(path.read_text(encoding="utf-8"))
        for path in claim_paths
    ]
    execution_claims = [
        payload for payload in claim_payloads if payload["claim_scope"] == "execution"
    ]
    object_claims = [
        payload for payload in claim_payloads if payload["claim_scope"] == "objects"
    ]
    subsystem_claims = [
        payload for payload in claim_payloads if payload["claim_scope"] == "subsystems"
    ]
    assert len(execution_claims) == 7
    assert len(object_claims) == 7
    assert len(subsystem_claims) == 4
    legacy_claim_source_count = 0
    covered_families: set[str] = set()

    execution_targets = {payload["claim_target_id"] for payload in execution_claims}
    assert execution_targets == {
        "ep-manual-cli-entrypoints-annuity-performance-manual-entry",
        "ep-manual-cli-entrypoints-annual-award-manual-entry",
        "ep-manual-cli-entrypoints-annual-loss-manual-entry",
        "ep-manual-cli-entrypoints-annuity-income-manual-entry",
        "ep-manual-cli-entrypoints-customer-mdm-manual-entry",
        "ep-scheduled-orchestrated-entrypoints-company-lookup-queue-flow-entry",
        "ep-scheduled-orchestrated-entrypoints-reference-sync-flow-entry",
    }

    for payload in execution_claims:
        assert payload["sources_read"]
        assert payload["objects_discovered"]
        assert payload["edges_added"]
    for payload in object_claims:
        assert payload["sources_read"]
        assert payload["objects_discovered"]

    for payload in claim_payloads:
        for source in payload["sources_read"]:
            source_ref = source["source_ref"]
            workspace_root = (
                LEGACY_REPO_ROOT
                if source.get("workspace_id") == "legacy_work_data_hub"
                or source["source_type"].startswith("legacy_")
                else REPO_ROOT
            )
            legacy_migration_alias = source_ref.startswith("docs/guides/domain-migration/")
            historical_stub_ref = source_ref.endswith(".txt")
            assert legacy_migration_alias or historical_stub_ref or (workspace_root / source_ref).exists(), source_ref
            if source["source_type"].startswith("legacy_"):
                legacy_claim_source_count += 1
            for family_id, prefixes in family_prefixes.items():
                if source_ref.startswith(prefixes):
                    covered_families.add(family_id)
        for candidate in payload["candidates_raised"]:
            for trigger_file in candidate["trigger_files"]:
                trigger_root = LEGACY_REPO_ROOT if (LEGACY_REPO_ROOT / trigger_file).exists() else REPO_ROOT
                historical_stub_trigger = trigger_file.endswith('.txt')
                assert historical_stub_trigger or (trigger_root / trigger_file).exists(), trigger_file
            assert candidate["source_type"] == "legacy_code"

    assert legacy_claim_source_count >= len(claim_payloads)
    assert covered_families == set(family_prefixes)

    manifest = json.loads((SEMANTIC_MAP_ROOT / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["generated_canonical_files"]
    assert manifest["compiled_claim_ids"]
    assert manifest["compiled_claim_ids"] == manifest["compiled_claims_by_wave"][SUCCESSOR_WAVE_ID]
    assert FIRST_WAVE_PILOT_WAVE_ID in manifest["compiled_claims_by_wave"]
    assert len(manifest["compiled_claims_by_wave"][SUCCESSOR_WAVE_ID]) == 5
    assert len(manifest["compiled_claims_by_wave"][FIRST_WAVE_PILOT_WAVE_ID]) == 18
    assert "semantic/index.yaml" in manifest["generated_canonical_files"]
    assert "semantic/concepts/sem-concept-customer-status.yaml" in manifest[
        "generated_canonical_files"
    ]

    coverage = json.loads(
        (SEMANTIC_MAP_ROOT / "reports" / "current" / "coverage-status.json").read_text(
            encoding="utf-8"
        )
    )
    integrity = json.loads(
        (SEMANTIC_MAP_ROOT / "reports" / "current" / "integrity-status.json").read_text(
            encoding="utf-8"
        )
    )
    assert coverage["wave_id"] == SUCCESSOR_WAVE_ID
    assert coverage["wave_status"] == "green"
    assert coverage["entrypoint_coverage_pct"] == 100.0
    assert coverage["high_priority_source_family_coverage_pct"] == 100.0
    assert coverage["orphan_high_priority_source_count"] == 0
    assert coverage["stale_high_priority_candidate_count"] == 0
    assert coverage["semantic_question_coverage_pct"] == 100.0
    assert integrity["wave_status"] == "green"
    assert integrity["closeout_ready"] is False
    assert integrity["archive_ready"] is False
    assert integrity["blocking_reasons"] == [
        "durable_wiki_targets_not_accepted",
        "findings_disposition_incomplete",
    ]

from __future__ import annotations

from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[2]
REGISTRY_ROOT = REPO_ROOT / "docs" / "wiki-bi" / "_meta" / "legacy-semantic-map"

RUNTIME_SCOPE_NODE_PATHS = {
    "sem-rule-annuity-performance-post-hook-chain": "semantic/rules/sem-rule-annuity-performance-post-hook-chain.yaml",
    "sem-rule-company-lookup-queue-single-domain-boundary": "semantic/rules/sem-rule-company-lookup-queue-single-domain-boundary.yaml",
    "sem-lifecycle-company-lookup-queue-recovery-cycle": "semantic/lifecycles/sem-lifecycle-company-lookup-queue-recovery-cycle.yaml",
    "sem-lifecycle-reference-sync-preload-cycle": "semantic/lifecycles/sem-lifecycle-reference-sync-preload-cycle.yaml",
    "sem-fact-family-reference-sync-target-inventory": "semantic/fact-families/sem-fact-family-reference-sync-target-inventory.yaml",
    "sem-rule-reference-sync-incremental-state": "semantic/rules/sem-rule-reference-sync-incremental-state.yaml",
    "sem-rule-enrichment-index-cache-boundary": "semantic/rules/sem-rule-enrichment-index-cache-boundary.yaml",
    "sem-rule-first-wave-artifact-operator-evidence": "semantic/rules/sem-rule-first-wave-artifact-operator-evidence.yaml",
}


def _load_yaml(path: Path) -> dict[str, object]:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def test_runtime_scope_nodes_are_not_marked_as_absorption_ready_semantic_canon() -> None:
    incorrect_statuses: list[str] = []

    for semantic_id, relative_path in RUNTIME_SCOPE_NODE_PATHS.items():
        payload = _load_yaml(REGISTRY_ROOT / relative_path)
        recommendation_status = (
            payload.get("proposal_governance", {}) or {}
        ).get("recommendation_status")
        readiness_status = payload.get("consumption_readiness_status")

        if recommendation_status != "claim_level_only":
            incorrect_statuses.append(
                f"{semantic_id} recommendation_status={recommendation_status}"
            )
        if readiness_status != "discovery-only":
            incorrect_statuses.append(
                f"{semantic_id} consumption_readiness_status={readiness_status}"
            )

    assert incorrect_statuses == []

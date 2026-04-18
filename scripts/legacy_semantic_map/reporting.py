from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import yaml

from .closeout import claim_digests_for_wave, mutable_claim_ids, prior_integrity_report_digests
from .models import GREEN_OBJECT_EDGE_COVERAGE_THRESHOLD
from .waves import allow_audit_wave_read, require_active_open_wave, wave_lookup


@dataclass(frozen=True)
class ReportGenerationResult:
    wave_id: str
    current_coverage_report: Path
    current_integrity_report: Path
    wave_coverage_report: Path
    wave_integrity_report: Path
    semantic_discovery_report: Path
    semantic_readiness_report: Path
    semantic_discovery_summary: Path
    semantic_readiness_summary: Path


def _load_yaml(path: Path) -> dict[str, object]:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def _load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def _write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def _pct(numerator: int, denominator: int) -> float:
    if denominator == 0:
        return 100.0
    return round((numerator / denominator) * 100, 2)


def _claim_ids_for_wave(registry_root: Path, wave_id: str) -> set[str]:
    claim_ids: set[str] = set()
    claims_root = registry_root / "claims" / wave_id
    if not claims_root.exists():
        return claim_ids
    for path in claims_root.rglob("*.yaml"):
        payload = _load_yaml(path)
        claim_id = payload.get("claim_id")
        if isinstance(claim_id, str):
            claim_ids.add(claim_id)
    return claim_ids


def _all_registry_claim_ids(registry_root: Path) -> set[str]:
    claim_ids: set[str] = set()
    claims_root = registry_root / "claims"
    if not claims_root.exists():
        return claim_ids
    for path in claims_root.rglob("*.yaml"):
        payload = _load_yaml(path)
        claim_id = payload.get("claim_id")
        if isinstance(claim_id, str):
            claim_ids.add(claim_id)
    return claim_ids


def _claim_payloads_for_wave(registry_root: Path, wave_id: str) -> list[dict[str, object]]:
    payloads: list[dict[str, object]] = []
    claims_root = registry_root / "claims" / wave_id
    if not claims_root.exists():
        return payloads
    for path in claims_root.rglob("*.yaml"):
        payloads.append(_load_yaml(path))
    return payloads


def _claim_ids_visible_to_wave(
    registry_root: Path,
    wave_ordinals: dict[str, int],
    target_wave_ordinal: int,
) -> set[str]:
    visible_claim_ids: set[str] = set()
    claims_root = registry_root / "claims"
    if not claims_root.exists():
        return visible_claim_ids
    for path in claims_root.rglob("*.yaml"):
        payload = _load_yaml(path)
        wave_id = payload.get("wave_id")
        claim_id = payload.get("claim_id")
        if (
            isinstance(wave_id, str)
            and isinstance(claim_id, str)
            and wave_ordinals[wave_id] <= target_wave_ordinal
        ):
            visible_claim_ids.add(claim_id)
    return visible_claim_ids


def _paths_for_wave(registry_root: Path, wave_claim_ids: set[str]) -> list[dict[str, object]]:
    results: list[dict[str, object]] = []
    for path in (registry_root / "execution" / "paths").glob("*.yaml"):
        payload = _load_yaml(path)
        compiled = set(payload.get("compiled_from_claims", []))
        if not compiled or compiled & wave_claim_ids:
            results.append(payload)
    return results


def _object_ids_for_wave(registry_root: Path, wave_claim_ids: set[str]) -> list[str]:
    object_index = _load_yaml(registry_root / "objects" / "index.yaml").get("objects", [])
    object_ids: list[str] = []
    for item in object_index:
        path = registry_root / str(item["path"])
        payload = _load_yaml(path)
        compiled = set(payload.get("compiled_from_claims", []))
        if not compiled or compiled & wave_claim_ids:
            object_ids.append(str(payload["object_id"]))
    return sorted(object_ids)


def _semantic_nodes_for_wave(
    registry_root: Path,
    wave_claim_ids: set[str],
) -> list[dict[str, object]]:
    semantic_index_path = registry_root / "semantic" / "index.yaml"
    if not semantic_index_path.exists():
        return []
    semantic_index = _load_yaml(semantic_index_path).get("semantic_nodes", [])
    nodes: list[dict[str, object]] = []
    for item in semantic_index:
        path = registry_root / str(item["path"])
        payload = _load_yaml(path)
        compiled = set(payload.get("compiled_from_claims", []))
        if not compiled or compiled & wave_claim_ids:
            nodes.append(payload)
    return nodes


def _edge_payloads(
    registry_root: Path,
    filename: str,
    wave_claim_ids: set[str] | None = None,
) -> list[dict[str, object]]:
    payload = _load_yaml(registry_root / "edges" / filename)
    edges = list(payload.get("edges", []))
    if wave_claim_ids is None:
        return edges
    filtered: list[dict[str, object]] = []
    for edge in edges:
        compiled = set(edge.get("compiled_from_claims", []))
        if not compiled or compiled & wave_claim_ids:
            filtered.append(edge)
    return filtered


def _source_family_results(
    registry_root: Path,
    target_wave: dict[str, object],
    wave_claim_ids: set[str],
) -> tuple[int, int]:
    families = _load_yaml(registry_root / "sources" / "families.yaml")["seeded_high_priority_source_families"]
    target_ids = set(target_wave["seeded_high_priority_source_families"])
    source_edges = _edge_payloads(registry_root, "source-to-node.yaml", wave_claim_ids)
    covered = 0
    orphan = 0
    for family in families:
        if family["family_id"] not in target_ids:
            continue
        prefixes = tuple(family.get("source_ref_prefixes", []))
        matched = any(
            isinstance(edge.get("from_id"), str)
            and edge["from_id"].startswith(prefix)
            for prefix in prefixes
            for edge in source_edges
        )
        if matched:
            covered += 1
        else:
            orphan += 1
    return covered, orphan


def _candidate_age_summary(
    registry_root: Path,
    *,
    active_wave_ordinal: int,
    target_wave_ordinal: int,
    wave_ordinals: dict[str, int],
) -> tuple[dict[str, int], int]:
    by_candidate: dict[str, int] = {}
    stale_count = 0
    for filename, key in (
        ("object-candidates.yaml", "object_candidates"),
        ("subsystem-candidates.yaml", "subsystem_candidates"),
    ):
        payload = _load_yaml(registry_root / "candidates" / filename)
        for candidate in payload.get(key, []):
            if candidate.get("priority", "high") != "high":
                continue
            if candidate.get("triage_status") != "new":
                continue
            first_seen_wave = candidate["first_seen_wave"]
            if wave_ordinals[first_seen_wave] > target_wave_ordinal:
                continue
            age = max(active_wave_ordinal - wave_ordinals[first_seen_wave], 0)
            by_candidate[str(candidate["candidate_id"])] = age
            if age > 1:
                stale_count += 1
    return by_candidate, stale_count


def _object_edge_coverage(
    registry_root: Path,
    object_ids: list[str],
    wave_claim_ids: set[str],
) -> float:
    participating: set[str] = set()
    for filename in (
        "subsystem-to-object.yaml",
        "object-to-object.yaml",
        "source-to-node.yaml",
    ):
        for edge in _edge_payloads(registry_root, filename, wave_claim_ids):
            for endpoint in (edge.get("from_id"), edge.get("to_id")):
                if isinstance(endpoint, str) and endpoint.startswith("obj-"):
                    participating.add(endpoint)
    numerator = len(set(object_ids) & participating)
    return _pct(numerator, len(object_ids))


def _classify_wave_status(
    *,
    entrypoint_coverage_pct: float,
    high_priority_source_family_coverage_pct: float,
    object_edge_coverage_pct: float,
    orphan_high_priority_source_count: int,
    stale_high_priority_candidate_count: int,
    semantic_question_coverage_pct: float = 100.0,
    stub_primary_source_count: int = 0,
) -> str:
    if (
        entrypoint_coverage_pct < 100.0
        or high_priority_source_family_coverage_pct < 100.0
        or orphan_high_priority_source_count > 0
        or stale_high_priority_candidate_count > 0
        or semantic_question_coverage_pct < 100.0
        or stub_primary_source_count > 0
    ):
        return "red"
    if object_edge_coverage_pct >= GREEN_OBJECT_EDGE_COVERAGE_THRESHOLD:
        return "green"
    return "yellow"


def _deterministic_generated_at(
    *,
    target_wave: dict[str, object],
    claim_payloads: list[dict[str, object]],
    accepted_claim_ids: set[str],
) -> str:
    submitted_times = sorted(
        {
            str(payload["submitted_at"])
            for payload in claim_payloads
            if isinstance(payload.get("claim_id"), str)
            and payload["claim_id"] in accepted_claim_ids
            and isinstance(payload.get("submitted_at"), str)
        }
    )
    if submitted_times:
        return submitted_times[-1]
    if isinstance(target_wave.get("closed_at"), str) and target_wave["closed_at"]:
        return f"{target_wave['closed_at']}T00:00:00Z"
    return f"{target_wave['opened_at']}T00:00:00Z"


def generate_reports(registry_root: Path, wave_id: str | None = None) -> ReportGenerationResult:
    active_wave_id, waves = wave_lookup(registry_root)
    target_wave_id = wave_id or active_wave_id
    explicit_wave_id = wave_id is not None
    if not explicit_wave_id:
        target_wave = require_active_open_wave(registry_root, target_wave_id)
    else:
        target_wave = allow_audit_wave_read(registry_root, target_wave_id)
    wave_ordinals = {key: int(value["wave_ordinal"]) for key, value in waves.items()}
    wave_claim_ids = _claim_ids_for_wave(registry_root, target_wave_id)
    visible_claim_ids = _claim_ids_visible_to_wave(
        registry_root,
        wave_ordinals,
        int(target_wave["wave_ordinal"]),
    )
    wave_claim_payloads = _claim_payloads_for_wave(registry_root, target_wave_id)
    all_registry_claim_ids = _all_registry_claim_ids(registry_root)

    entry_surfaces = _load_yaml(registry_root / "execution" / "entry-surfaces.yaml")["seeded_entry_surfaces"]
    target_surface_ids = set(target_wave["seeded_entry_surfaces"])
    mapped_surfaces = {
        item["surface_id"]
        for item in entry_surfaces
        for payload in _paths_for_wave(registry_root, visible_claim_ids)
        if item["surface_id"] in target_surface_ids
        and payload.get("entry_surface") == item["entry_family"]
        and payload.get("domain_or_surface") == item["surface_id"]
    }
    entrypoint_coverage_pct = _pct(len(mapped_surfaces), len(target_surface_ids))

    covered_source_families, orphan_high_priority_source_count = _source_family_results(
        registry_root,
        target_wave,
        visible_claim_ids,
    )
    high_priority_source_family_coverage_pct = _pct(
        covered_source_families,
        len(target_wave["seeded_high_priority_source_families"]),
    )

    object_ids = _object_ids_for_wave(registry_root, wave_claim_ids)
    object_edge_coverage_pct = _object_edge_coverage(
        registry_root,
        object_ids,
        visible_claim_ids,
    )

    semantic_nodes = _semantic_nodes_for_wave(registry_root, visible_claim_ids)
    question_set_id = target_wave.get("semantic_question_set_id")
    required_semantic_node_ids: list[str] = []
    required_non_equivalence_ids: list[str] = []
    if isinstance(question_set_id, str) and question_set_id:
        question_set = _load_yaml(
            registry_root / "semantic" / "question-sets" / f"{question_set_id}.yaml"
        )
        required_semantic_node_ids = list(question_set.get("required_semantic_node_ids", []))
        required_non_equivalence_ids = list(question_set.get("required_non_equivalence_ids", []))

    semantic_node_ids = {
        str(node["semantic_id"])
        for node in semantic_nodes
        if isinstance(node.get("semantic_id"), str)
    }
    semantic_question_coverage_pct = _pct(
        len(set(required_semantic_node_ids) & semantic_node_ids),
        len(required_semantic_node_ids),
    )
    semantic_non_equivalence_coverage_pct = _pct(
        len(set(required_non_equivalence_ids) & semantic_node_ids),
        len(required_non_equivalence_ids),
    )
    stub_primary_source_count = sum(
        1
        for node in semantic_nodes
        if any(
            isinstance(source_ref, str) and source_ref.endswith(".txt")
            for source_ref in node.get("primary_semantic_sources", [])
        )
    )
    authoritative_primary_source_pct = _pct(
        sum(
            1
            for node in semantic_nodes
            if node.get("semantic_authority") == "authoritative_semantic_source"
        ),
        len(semantic_nodes),
    )
    absorption_contract_completion_pct = _pct(
        sum(
            1
            for node in semantic_nodes
            if node.get("durable_target_pages") or node.get("blocked_by")
        ),
        len(semantic_nodes),
    )

    by_candidate, stale_high_priority_candidate_count = _candidate_age_summary(
        registry_root,
        active_wave_ordinal=int(waves[active_wave_id]["wave_ordinal"]),
        target_wave_ordinal=int(target_wave["wave_ordinal"]),
        wave_ordinals=wave_ordinals,
    )
    wave_status = _classify_wave_status(
        entrypoint_coverage_pct=entrypoint_coverage_pct,
        high_priority_source_family_coverage_pct=high_priority_source_family_coverage_pct,
        object_edge_coverage_pct=object_edge_coverage_pct,
        orphan_high_priority_source_count=orphan_high_priority_source_count,
        stale_high_priority_candidate_count=stale_high_priority_candidate_count,
        semantic_question_coverage_pct=semantic_question_coverage_pct,
        stub_primary_source_count=stub_primary_source_count,
    )

    manifest = _load_json(registry_root / "manifest.json")
    manifest_compiled_ids = set(manifest.get("compiled_claim_ids", []))
    compiled_claims_by_wave = {
        str(wave_key): set(claim_ids)
        for wave_key, claim_ids in manifest.get("compiled_claims_by_wave", {}).items()
    }
    relevant_manifest_ids = compiled_claims_by_wave.get(target_wave_id)
    manifest_wave_index_missing = target_wave_id != active_wave_id and relevant_manifest_ids is None
    if relevant_manifest_ids is None:
        relevant_manifest_ids = manifest_compiled_ids if target_wave_id == active_wave_id else set()
    missing_claim_ids = sorted(relevant_manifest_ids - all_registry_claim_ids)
    accepted_claim_ids = relevant_manifest_ids & wave_claim_ids
    current_digests = claim_digests_for_wave(
        registry_root,
        target_wave_id,
        allowed_claim_ids=accepted_claim_ids,
    )
    wave_integrity_path = (
        registry_root / "reports" / "waves" / target_wave_id / "integrity-status.json"
    )
    prior_digests = prior_integrity_report_digests(wave_integrity_path)
    mutable_ids = mutable_claim_ids(current_digests, prior_digests) if prior_digests else []
    immutability_check_passed = not mutable_ids
    closeout_ready = (
        wave_status == "green"
        and not missing_claim_ids
        and immutability_check_passed
        and not manifest_wave_index_missing
        and bool(target_wave.get("durable_wiki_targets_accepted", False))
        and bool(target_wave.get("findings_disposition_complete", False))
    )
    archive_ready = (
        closeout_ready
        and not bool(target_wave.get("depends_on_active_wave_working_state", False))
        and target_wave.get("status") == "closed"
    )

    blocking_reasons: list[str] = []
    if wave_status != "green":
        blocking_reasons.append(f"wave_status_{wave_status}")
    if semantic_question_coverage_pct < 100.0:
        blocking_reasons.append("semantic_question_coverage_incomplete")
    if stub_primary_source_count > 0:
        blocking_reasons.append("stub_primary_sources_detected")
    if missing_claim_ids:
        blocking_reasons.append("missing_compiled_claim_ids")
    if mutable_ids:
        blocking_reasons.append("mutable_accepted_claims_detected")
    if manifest_wave_index_missing:
        blocking_reasons.append("missing_wave_compiled_claim_index")
    if not target_wave.get("durable_wiki_targets_accepted", False):
        blocking_reasons.append("durable_wiki_targets_not_accepted")
    if not target_wave.get("findings_disposition_complete", False):
        blocking_reasons.append("findings_disposition_incomplete")
    if target_wave.get("depends_on_active_wave_working_state", False):
        blocking_reasons.append("active_wave_dependency_open")

    generated_at = _deterministic_generated_at(
        target_wave=target_wave,
        claim_payloads=wave_claim_payloads,
        accepted_claim_ids=accepted_claim_ids,
    )
    coverage_payload = {
        "wave_id": target_wave_id,
        "wave_status": wave_status,
        "entrypoint_coverage_pct": entrypoint_coverage_pct,
        "high_priority_source_family_coverage_pct": high_priority_source_family_coverage_pct,
        "object_edge_coverage_pct": object_edge_coverage_pct,
        "orphan_high_priority_source_count": orphan_high_priority_source_count,
        "stale_high_priority_candidate_count": stale_high_priority_candidate_count,
        "semantic_question_coverage_pct": semantic_question_coverage_pct,
        "semantic_non_equivalence_coverage_pct": semantic_non_equivalence_coverage_pct,
        "stub_primary_source_count": stub_primary_source_count,
        "authoritative_primary_source_pct": authoritative_primary_source_pct,
        "absorption_contract_completion_pct": absorption_contract_completion_pct,
        "untriaged_candidate_age_by_wave": {
            "max": max(by_candidate.values(), default=0),
            "count_gt_0": sum(1 for value in by_candidate.values() if value > 0),
            "count_gt_1": sum(1 for value in by_candidate.values() if value > 1),
            "by_candidate": dict(sorted(by_candidate.items())),
        },
        "generated_at": generated_at,
    }
    integrity_payload = {
        "wave_id": target_wave_id,
        "wave_status": wave_status,
        "closeout_ready": closeout_ready,
        "archive_ready": archive_ready,
        "immutability_check_passed": immutability_check_passed,
        "required_claim_ids": sorted(accepted_claim_ids),
        "compiled_claim_ids": sorted(relevant_manifest_ids),
        "missing_claim_ids": missing_claim_ids,
        "mutable_claim_ids_detected": mutable_ids,
        "blocking_reasons": blocking_reasons,
        "accepted_claim_digests": current_digests,
        "generated_at": generated_at,
    }

    current_coverage_path = registry_root / "reports" / "current" / "coverage-status.json"
    current_integrity_path = registry_root / "reports" / "current" / "integrity-status.json"
    wave_coverage_path = registry_root / "reports" / "waves" / target_wave_id / "coverage-status.json"
    wave_reports_dir = registry_root / "reports" / "waves" / target_wave_id
    semantic_discovery_path = wave_reports_dir / "semantic-discovery-status.json"
    semantic_readiness_path = wave_reports_dir / "semantic-readiness-status.json"
    semantic_discovery_summary_path = wave_reports_dir / "semantic-discovery-summary.md"
    semantic_readiness_summary_path = wave_reports_dir / "semantic-readiness-summary.md"

    maturity_counts = {
        level: sum(
            1
            for node in semantic_nodes
            if node.get("semantic_maturity_level") == level
        )
        for level in (
            "observed",
            "inferred",
            "contested",
            "consumption-candidate",
        )
    }
    contested_semantic_ids = sorted(
        str(node["semantic_id"])
        for node in semantic_nodes
        if node.get("semantic_maturity_level") == "contested"
    )
    recommendation_counts = {
        status: sum(
            1
            for node in semantic_nodes
            if isinstance(node.get("proposal_governance"), dict)
            and node["proposal_governance"].get("recommendation_status") == status
        )
        for status in (
            "recommended_stable_canonical",
            "recommended_contested",
            "claim_level_only",
        )
    }
    contested_proposal_ids = sorted(
        str(node["semantic_id"])
        for node in semantic_nodes
        if isinstance(node.get("proposal_governance"), dict)
        and node["proposal_governance"].get("recommendation_status")
        == "recommended_contested"
    )
    governance_implication_ids: dict[str, list[str]] = {
        "slice_admission": [],
        "defer_candidates": [],
        "retire_candidates": [],
        "durable_wiki_absorption": [],
    }
    carrier_scope_mismatch_ids: list[str] = []
    unresolved_proxy_conflict_ids: list[str] = []
    for node in semantic_nodes:
        proposal_governance = node.get("proposal_governance")
        if not isinstance(proposal_governance, dict):
            continue
        semantic_id = str(node["semantic_id"])
        semantic_scope_type = proposal_governance.get("semantic_scope_type")
        if semantic_scope_type in {"runtime_carrier", "witness_surface"}:
            carrier_scope_mismatch_ids.append(semantic_id)
        contradiction_status = proposal_governance.get("contradiction_accounting_status")
        gate_blockers = proposal_governance.get("gate_blockers", [])
        if contradiction_status in {"real_contradiction", "unresolved"} or any(
            blocker in {"contradiction_real_contradiction", "contradiction_unresolved"}
            for blocker in gate_blockers
        ):
            unresolved_proxy_conflict_ids.append(semantic_id)
        governance_implications = proposal_governance.get("governance_implications")
        if not isinstance(governance_implications, dict):
            continue
        for key in governance_implication_ids:
            implication = governance_implications.get(key)
            if not isinstance(implication, dict):
                continue
            summary = implication.get("summary")
            affected = implication.get("affected_surfaces", [])
            targets = implication.get("target_pages", [])
            blocked = implication.get("blocked_by", [])
            if summary or affected or targets or blocked:
                governance_implication_ids[key].append(semantic_id)
    handoff_ready_ids = sorted(
        str(node["semantic_id"])
        for node in semantic_nodes
        if node.get("consumption_readiness_status") == "reviewable"
    )
    blocked_semantic_ids = sorted(
        str(node["semantic_id"])
        for node in semantic_nodes
        if node.get("consumption_readiness_status") == "blocked"
        or node.get("blocked_by")
    )
    blocked_by_gate_reasons: dict[str, int] = {}
    for node in semantic_nodes:
        for reason in node.get("blocked_by", []):
            if isinstance(reason, str) and reason:
                blocked_by_gate_reasons[reason] = blocked_by_gate_reasons.get(reason, 0) + 1
    durable_target_page_count = len(
        {
            str(page)
            for node in semantic_nodes
            for page in node.get("durable_target_pages", [])
            if isinstance(page, str)
        }
    )
    semantic_discovery_payload = {
        "wave_id": target_wave_id,
        "discovery_view_status": coverage_payload["wave_status"],
        "semantic_maturity_counts": maturity_counts,
        "contested_semantic_ids": contested_semantic_ids,
        "recommendation_counts": recommendation_counts,
        "contested_proposal_ids": contested_proposal_ids,
        "governance_implication_summaries": {
            key: {
                "count": len(sorted(set(ids))),
                "ids": sorted(set(ids)),
            }
            for key, ids in governance_implication_ids.items()
        },
        "carrier_scope_mismatch_ids": sorted(set(carrier_scope_mismatch_ids)),
        "unresolved_proxy_conflict_ids": sorted(set(unresolved_proxy_conflict_ids)),
        "generated_at": generated_at,
    }
    semantic_readiness_payload = {
        "wave_id": target_wave_id,
        "handoff_ready_semantic_ids": handoff_ready_ids,
        "blocked_semantic_ids": blocked_semantic_ids,
        "blocked_by_gate_reasons": dict(sorted(blocked_by_gate_reasons.items())),
        "durable_target_page_count": durable_target_page_count,
        "generated_at": generated_at,
    }

    if (
        target_wave_id == active_wave_id
        and target_wave.get("status") == "active"
        and not target_wave.get("closed_at")
    ):
        _write_json(current_coverage_path, coverage_payload)
        _write_json(current_integrity_path, integrity_payload)
    _write_json(wave_coverage_path, coverage_payload)
    _write_json(wave_integrity_path, integrity_payload)
    _write_json(semantic_discovery_path, semantic_discovery_payload)
    _write_json(semantic_readiness_path, semantic_readiness_payload)
    _write_text(
        semantic_discovery_summary_path,
        "\n".join(
            [
                f"# Semantic discovery summary: {target_wave_id}",
                "",
                f"- discovery view status: {semantic_discovery_payload['discovery_view_status']}",
                f"- contested semantic ids: {', '.join(contested_semantic_ids) if contested_semantic_ids else 'none'}",
            ]
        ),
    )
    _write_text(
        semantic_readiness_summary_path,
        "\n".join(
            [
                f"# Semantic readiness summary: {target_wave_id}",
                "",
                f"- reviewable proposal ids: {', '.join(handoff_ready_ids) if handoff_ready_ids else 'none'}",
                f"- blocked proposal ids: {', '.join(blocked_semantic_ids) if blocked_semantic_ids else 'none'}",
                f"- durable target page count: {durable_target_page_count}",
            ]
        ),
    )

    return ReportGenerationResult(
        wave_id=target_wave_id,
        current_coverage_report=current_coverage_path,
        current_integrity_report=current_integrity_path,
        wave_coverage_report=wave_coverage_path,
        wave_integrity_report=wave_integrity_path,
        semantic_discovery_report=semantic_discovery_path,
        semantic_readiness_report=semantic_readiness_path,
        semantic_discovery_summary=semantic_discovery_summary_path,
        semantic_readiness_summary=semantic_readiness_summary_path,
    )

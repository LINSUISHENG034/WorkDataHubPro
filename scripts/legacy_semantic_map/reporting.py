from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import yaml

from .closeout import claim_digests_for_wave, mutable_claim_ids, prior_integrity_report_digests
from .models import GREEN_OBJECT_EDGE_COVERAGE_THRESHOLD


@dataclass(frozen=True)
class ReportGenerationResult:
    wave_id: str
    current_coverage_report: Path
    current_integrity_report: Path
    wave_coverage_report: Path
    wave_integrity_report: Path


def _load_yaml(path: Path) -> dict[str, object]:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def _load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def _pct(numerator: int, denominator: int) -> float:
    if denominator == 0:
        return 100.0
    return round((numerator / denominator) * 100, 2)


def _wave_lookup(registry_root: Path) -> tuple[str, dict[str, dict[str, object]]]:
    waves_index = _load_yaml(registry_root / "waves" / "index.yaml")
    return waves_index["active_wave_id"], {item["wave_id"]: item for item in waves_index["waves"]}


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
) -> str:
    if (
        entrypoint_coverage_pct < 100.0
        or high_priority_source_family_coverage_pct < 100.0
        or orphan_high_priority_source_count > 0
        or stale_high_priority_candidate_count > 0
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
    active_wave_id, wave_lookup = _wave_lookup(registry_root)
    target_wave_id = wave_id or active_wave_id
    target_wave = wave_lookup[target_wave_id]
    wave_ordinals = {key: int(value["wave_ordinal"]) for key, value in wave_lookup.items()}
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

    by_candidate, stale_high_priority_candidate_count = _candidate_age_summary(
        registry_root,
        active_wave_ordinal=int(wave_lookup[active_wave_id]["wave_ordinal"]),
        target_wave_ordinal=int(target_wave["wave_ordinal"]),
        wave_ordinals=wave_ordinals,
    )
    wave_status = _classify_wave_status(
        entrypoint_coverage_pct=entrypoint_coverage_pct,
        high_priority_source_family_coverage_pct=high_priority_source_family_coverage_pct,
        object_edge_coverage_pct=object_edge_coverage_pct,
        orphan_high_priority_source_count=orphan_high_priority_source_count,
        stale_high_priority_candidate_count=stale_high_priority_candidate_count,
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

    if target_wave_id == active_wave_id:
        _write_json(current_coverage_path, coverage_payload)
        _write_json(current_integrity_path, integrity_payload)
    _write_json(wave_coverage_path, coverage_payload)
    _write_json(wave_integrity_path, integrity_payload)

    return ReportGenerationResult(
        wave_id=target_wave_id,
        current_coverage_report=current_coverage_path,
        current_integrity_report=current_integrity_path,
        wave_coverage_report=wave_coverage_path,
        wave_integrity_report=wave_integrity_path,
    )

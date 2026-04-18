from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

import yaml

from .claims import (
    ClaimArtifact,
    ClaimCandidateRecord,
    ClaimEdgeRecord,
    ClaimSemanticFindingRecord,
    ClaimSourceRecord,
)
from .models import CANONICAL_SEED_SOURCES
from .waves import require_active_open_wave


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


def _load_yaml_if_exists(path: Path) -> dict[str, object]:
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def _sorted_unique(values: Iterable[str]) -> list[str]:
    return sorted({value for value in values if value})


def _dedupe_payloads(payloads: Iterable[dict[str, object]]) -> list[dict[str, object]]:
    deduped: dict[str, dict[str, object]] = {}
    for payload in payloads:
        deduped[json.dumps(payload, sort_keys=True)] = payload
    return list(deduped.values())


def _merge_index_entries(
    entries: list[dict[str, str]],
    key_name: str,
) -> list[dict[str, str]]:
    merged = {entry[key_name]: entry for entry in entries}
    return [merged[key] for key in sorted(merged)]


def _title_from_id(identifier: str) -> str:
    return identifier.split("-", 1)[1].replace("-", " ").title()


def _path_entry_surface(path_id: str) -> str:
    parts = path_id.split("-")
    return "_".join(parts[1:4])


def _path_domain_or_surface(path_id: str) -> str:
    parts = path_id.split("-")
    return "_".join(parts[4:-2])


def _route_edge(edge: ClaimEdgeRecord) -> str | None:
    if edge.from_id.startswith("ep-") and edge.to_id.startswith("ss-"):
        return "execution-to-subsystem.yaml"
    if edge.from_id.startswith("ep-") and edge.to_id.startswith("obj-"):
        return "execution-to-object.yaml"
    if edge.from_id.startswith("ss-") and edge.to_id.startswith("obj-"):
        return "subsystem-to-object.yaml"
    if edge.from_id.startswith("obj-") and edge.to_id.startswith("obj-"):
        return "object-to-object.yaml"
    return None


def _semantic_directory_name(node_type: str) -> str:
    return {
        "semantic_concept": "concepts",
        "semantic_rule": "rules",
        "semantic_non_equivalence": "non-equivalences",
        "semantic_lifecycle": "lifecycles",
        "semantic_fact_family": "fact-families",
        "semantic_decision_anchor": "decision-anchors",
    }[node_type]


def _semantic_maturity_level(finding: ClaimSemanticFindingRecord) -> str:
    if finding.open_questions:
        return "contested"
    if finding.durable_target_pages:
        return "consumption-candidate"
    if len(set(finding.primary_source_refs + finding.supporting_source_refs)) > 1:
        return "inferred"
    return "observed"


def _source_edge(source: ClaimSourceRecord, claim: ClaimArtifact) -> dict[str, object]:
    return {
        "from_id": source.source_ref,
        "to_id": claim.claim_target_id,
        "relationship": "supports_claim_target",
        "source_refs": [source.source_ref],
        "source_type": source.source_type,
        "claim_type": "compiled_summary",
        "evidence_strength": "supporting",
        "coverage_state": "partial",
        "confidence": "high",
        "last_verified": claim.submitted_at.split("T", 1)[0],
        "open_questions": [],
        "compiled_from_claims": [claim.claim_id],
    }


def _compiled_edge_payload(edge: ClaimEdgeRecord, claim_id: str) -> dict[str, object]:
    return {
        "from_id": edge.from_id,
        "to_id": edge.to_id,
        "relationship": edge.relationship,
        "source_refs": edge.source_refs,
        "source_type": edge.source_type,
        "claim_type": "compiled_summary",
        "evidence_strength": edge.evidence_strength,
        "coverage_state": edge.coverage_state,
        "confidence": edge.confidence,
        "last_verified": edge.last_verified,
        "open_questions": edge.open_questions,
        "compiled_from_claims": [claim_id],
    }


def _compiled_candidate_payload(candidate: ClaimCandidateRecord, claim_id: str) -> dict[str, object]:
    payload = {
        "candidate_id": candidate.candidate_id,
        "proposed_name": candidate.proposed_name,
        "candidate_type": candidate.candidate_type,
        "reason": candidate.reason,
        "trigger_files": candidate.trigger_files,
        "source_type": candidate.source_type,
        "claim_type": "compiled_summary",
        "confidence": candidate.confidence,
        "priority": candidate.priority,
        "triage_status": candidate.triage_status,
        "first_seen_wave": candidate.first_seen_wave,
        "last_verified": candidate.last_verified,
        "compiled_from_claims": [claim_id],
    }
    if candidate.candidate_type == "subsystem":
        payload["discovered_from_claim"] = claim_id
        payload["discovered_from_subsystem"] = None
    else:
        payload["discovered_from_claim"] = claim_id
    return payload


def _write_manifest(
    registry_root: Path,
    *,
    compiled_claim_ids: list[str],
    compiled_claims_by_wave: dict[str, list[str]],
    written_files: list[str],
) -> None:
    manifest_path = registry_root / "manifest.json"
    existing_payload: dict[str, object] = {}
    if manifest_path.exists():
        existing_payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    merged_compiled_claims_by_wave = {
        str(wave_id): sorted(claim_ids)
        for wave_id, claim_ids in existing_payload.get("compiled_claims_by_wave", {}).items()
    }
    merged_compiled_claims_by_wave.update(compiled_claims_by_wave)
    merged_generated_files = sorted(
        set(existing_payload.get("generated_canonical_files", [])) | set(written_files)
    )
    manifest_path.write_text(
        json.dumps(
            {
                "artifact": "legacy-semantic-map-registry",
                "canonical_seed_sources": list(CANONICAL_SEED_SOURCES),
                "generated_canonical_files": merged_generated_files,
                "compiled_claim_ids": compiled_claim_ids,
                "compiled_claims_by_wave": merged_compiled_claims_by_wave,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def compile_claim_artifacts(
    registry_root: Path,
    claim_paths: Sequence[Path],
) -> CompilationResult:
    relative_claim_paths = [_assert_claim_path(registry_root, path) for path in claim_paths]
    claims = [_load_claim(registry_root / relative_path) for relative_path in relative_claim_paths]
    claims = sorted(claims, key=lambda item: item.claim_id)

    for claim in claims:
        require_active_open_wave(registry_root, claim.wave_id)

    written_files: list[str] = []
    subsystem_index: list[dict[str, str]] = list(
        _load_yaml_if_exists(registry_root / "subsystems" / "index.yaml").get("subsystems", [])
    )
    object_index: list[dict[str, str]] = list(
        _load_yaml_if_exists(registry_root / "objects" / "index.yaml").get("objects", [])
    )
    semantic_index: list[dict[str, str]] = []
    edge_payloads: dict[str, list[dict[str, object]]] = {
        "execution-to-subsystem.yaml": list(
            _load_yaml_if_exists(registry_root / "edges" / "execution-to-subsystem.yaml").get(
                "edges", []
            )
        ),
        "execution-to-object.yaml": list(
            _load_yaml_if_exists(registry_root / "edges" / "execution-to-object.yaml").get(
                "edges", []
            )
        ),
        "subsystem-to-object.yaml": list(
            _load_yaml_if_exists(registry_root / "edges" / "subsystem-to-object.yaml").get(
                "edges", []
            )
        ),
        "object-to-object.yaml": list(
            _load_yaml_if_exists(registry_root / "edges" / "object-to-object.yaml").get(
                "edges", []
            )
        ),
        "source-to-node.yaml": list(
            _load_yaml_if_exists(registry_root / "edges" / "source-to-node.yaml").get(
                "edges", []
            )
        ),
    }
    candidate_payloads: dict[str, list[dict[str, object]]] = {
        "subsystem-candidates.yaml": list(
            _load_yaml_if_exists(registry_root / "candidates" / "subsystem-candidates.yaml").get(
                "subsystem_candidates", []
            )
        ),
        "object-candidates.yaml": list(
            _load_yaml_if_exists(registry_root / "candidates" / "object-candidates.yaml").get(
                "object_candidates", []
            )
        ),
    }

    for claim in claims:
        for source in claim.sources_read:
            edge_payloads["source-to-node.yaml"].append(_source_edge(source, claim))

        for edge in claim.edges_added:
            routed_file = _route_edge(edge)
            if routed_file is not None:
                edge_payloads[routed_file].append(_compiled_edge_payload(edge, claim.claim_id))

        for candidate in claim.candidates_raised:
            if candidate.candidate_type == "subsystem":
                candidate_payloads["subsystem-candidates.yaml"].append(
                    _compiled_candidate_payload(candidate, claim.claim_id)
                )
            elif candidate.candidate_type == "object":
                candidate_payloads["object-candidates.yaml"].append(
                    _compiled_candidate_payload(candidate, claim.claim_id)
                )

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
            subsystem_index.append(
                {
                    "subsystem_id": claim.claim_target_id,
                    "path": f"subsystems/{claim.claim_target_id}.yaml",
                }
            )

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
            object_index.append(
                {
                    "object_id": claim.claim_target_id,
                    "path": f"objects/{claim.claim_target_id}.yaml",
                }
            )

        if claim.claim_scope == "semantic":
            for finding in claim.semantic_findings:
                directory_name = _semantic_directory_name(finding.semantic_node_type)
                maturity_level = _semantic_maturity_level(finding)
                relative_path = f"semantic/{directory_name}/{finding.semantic_id}.yaml"
                output_path = registry_root / relative_path
                existing_payload = _load_yaml_if_exists(output_path)
                payload = {
                    "semantic_id": finding.semantic_id,
                    "semantic_node_type": finding.semantic_node_type,
                    "title": finding.title,
                    "summary": finding.summary,
                    "business_conclusion": finding.business_conclusion,
                    "primary_semantic_sources": finding.primary_source_refs,
                    "supporting_witness_sources": finding.supporting_source_refs,
                    "semantic_authority": finding.semantic_authority,
                    "related_execution_nodes": [],
                    "related_subsystems": [],
                    "related_objects": [],
                    "non_equivalent_to": finding.non_equivalent_to,
                    "open_questions": finding.open_questions,
                    "durable_target_pages": finding.durable_target_pages,
                    "durable_summary_ready": bool(finding.durable_target_pages),
                    "requires_human_judgement": False,
                    "blocked_by": [],
                    "archive_after_absorption": True,
                    "semantic_maturity_level": maturity_level,
                    "discovery_view_status": (
                        "contested" if maturity_level == "contested" else "sufficient"
                    ),
                    "consumption_readiness_status": (
                        "reviewable"
                        if finding.durable_target_pages
                        else "discovery-only"
                    ),
                    "readiness_notes": list(finding.open_questions),
                    "compiled_from_wave_id": claim.wave_id,
                    "compiled_at": claim.submitted_at,
                    "confidence": finding.confidence,
                    "last_verified": finding.last_verified,
                    "compiled_from_claims": _sorted_unique(
                        list(existing_payload.get("compiled_from_claims", [])) + [claim.claim_id]
                    ),
                }
                _write_yaml(output_path, payload)
                written_files.append(relative_path)
                semantic_index.append(
                    {
                        "semantic_id": finding.semantic_id,
                        "semantic_node_type": finding.semantic_node_type,
                        "path": relative_path,
                    }
                )

    subsystem_index = _merge_index_entries(subsystem_index, "subsystem_id")
    object_index = _merge_index_entries(object_index, "object_id")
    _write_yaml(registry_root / "subsystems" / "index.yaml", {"subsystems": subsystem_index})
    _write_yaml(registry_root / "objects" / "index.yaml", {"objects": object_index})
    written_files.extend(["subsystems/index.yaml", "objects/index.yaml"])
    if semantic_index:
        semantic_index = sorted(semantic_index, key=lambda item: item["semantic_id"])
        _write_yaml(registry_root / "semantic" / "index.yaml", {"semantic_nodes": semantic_index})
        written_files.append("semantic/index.yaml")

    for filename, payload in edge_payloads.items():
        payload = _dedupe_payloads(payload)
        payload = sorted(
            payload,
            key=lambda item: (item["from_id"], item["to_id"], item["relationship"]),
        )
        _write_yaml(registry_root / "edges" / filename, {"edges": payload})
        written_files.append(f"edges/{filename}")

    for filename, key in (
        ("subsystem-candidates.yaml", "subsystem_candidates"),
        ("object-candidates.yaml", "object_candidates"),
    ):
        payload = {
            item["candidate_id"]: item for item in candidate_payloads[filename]
        }
        payload = [payload[candidate_id] for candidate_id in sorted(payload)]
        _write_yaml(registry_root / "candidates" / filename, {key: payload})
        written_files.append(f"candidates/{filename}")

    written_files = sorted(set(written_files))
    compiled_claim_ids = [claim.claim_id for claim in claims]
    compiled_claims_by_wave: dict[str, list[str]] = {}
    for claim in claims:
        compiled_claims_by_wave.setdefault(claim.wave_id, []).append(claim.claim_id)
    compiled_claims_by_wave = {
        wave_id: sorted(claim_ids)
        for wave_id, claim_ids in sorted(compiled_claims_by_wave.items())
    }
    _write_manifest(
        registry_root,
        compiled_claim_ids=compiled_claim_ids,
        compiled_claims_by_wave=compiled_claims_by_wave,
        written_files=written_files,
    )
    return CompilationResult(
        compiled_claim_ids=compiled_claim_ids,
        written_files=written_files,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry-root", type=Path, required=True)
    parser.add_argument("--claim", type=Path, action="append", default=[])
    args = parser.parse_args()

    compile_claim_artifacts(args.registry_root, args.claim)


if __name__ == "__main__":
    main()

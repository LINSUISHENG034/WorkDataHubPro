from __future__ import annotations

from dataclasses import asdict
from dataclasses import dataclass
from pathlib import Path
import re

import yaml

from .models import (
    CLAIM_TYPES,
    CONFIDENCE_LEVELS,
    COVERAGE_STATES,
    EVIDENCE_STRENGTHS,
    SOURCE_TYPES,
    TRIAGE_STATUSES,
    WAVE_ID_PATTERN,
)

CLAIM_ID_PATTERN = r"[a-z0-9]+(?:-[a-z0-9]+)*"
CLAIM_SCOPE_DIRECTORIES = {
    "execution": "execution",
    "subsystems": "subsystems",
    "objects": "objects",
}


def _validate_choice(field_name: str, value: str, allowed_values: tuple[str, ...]) -> None:
    if value not in allowed_values:
        raise ValueError(f"Unsupported {field_name}: {value}")


def _validate_pattern(field_name: str, value: str, pattern: str) -> None:
    if re.fullmatch(pattern, value) is None:
        raise ValueError(f"Malformed {field_name}: {value}")


@dataclass(frozen=True)
class ClaimSourceRecord:
    source_ref: str
    source_type: str
    note: str

    def __post_init__(self) -> None:
        _validate_choice("source_type", self.source_type, SOURCE_TYPES)


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

    def __post_init__(self) -> None:
        _validate_choice("source_type", self.source_type, SOURCE_TYPES)
        _validate_choice("claim_type", self.claim_type, CLAIM_TYPES)
        _validate_choice("evidence_strength", self.evidence_strength, EVIDENCE_STRENGTHS)
        _validate_choice("coverage_state", self.coverage_state, COVERAGE_STATES)
        _validate_choice("confidence", self.confidence, CONFIDENCE_LEVELS)


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

    def __post_init__(self) -> None:
        _validate_choice("source_type", self.source_type, SOURCE_TYPES)
        _validate_choice("claim_type", self.claim_type, CLAIM_TYPES)
        _validate_choice("evidence_strength", self.evidence_strength, EVIDENCE_STRENGTHS)
        _validate_choice("coverage_state", self.coverage_state, COVERAGE_STATES)
        _validate_choice("confidence", self.confidence, CONFIDENCE_LEVELS)


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

    def __post_init__(self) -> None:
        _validate_choice("source_type", self.source_type, SOURCE_TYPES)
        _validate_choice("claim_type", self.claim_type, CLAIM_TYPES)
        _validate_choice("confidence", self.confidence, CONFIDENCE_LEVELS)
        _validate_choice("triage_status", self.triage_status, TRIAGE_STATUSES)
        _validate_pattern("first_seen_wave", self.first_seen_wave, WAVE_ID_PATTERN)


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
    _validate_pattern("wave_id", claim.wave_id, WAVE_ID_PATTERN)
    _validate_pattern("claim_id", claim.claim_id, CLAIM_ID_PATTERN)
    return (
        Path("claims")
        / claim.wave_id
        / CLAIM_SCOPE_DIRECTORIES[claim.claim_scope]
        / f"{claim.claim_id}.yaml"
    )


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

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

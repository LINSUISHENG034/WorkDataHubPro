from __future__ import annotations

from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import field
from dataclasses import replace
import ntpath
from pathlib import Path
from pathlib import PureWindowsPath

import yaml

from .claims import (
    ClaimArtifact,
    ClaimSemanticFindingRecord,
    ClaimSourceRecord,
    _coerce_record,
    _coerce_record_list,
    _validate_choice,
    _validate_pattern,
    write_claim_artifact,
)
from .models import WAVE_ID_PATTERN
from .waves import require_active_open_wave

LEGACY_WORKSPACE_ID = "legacy_work_data_hub"
LEGACY_REPO_ROOT = PureWindowsPath("E:/Projects/WorkDataHub")
INGRESS_KIND_DIRECTORIES = {
    "question_cluster": "question-clusters",
    "finding": "findings",
}
PROMOTION_ACTIONS = (
    "hold_ingress",
    "promote_to_semantic_claim",
    "requires_user_review",
)
INGRESS_ID_PATTERN = r"[a-z0-9]+(?:-[a-z0-9]+)*"


@dataclass(frozen=True)
class IngressPromotionRecommendation:
    recommended_action: str
    rationale: str
    gate_failures: list[str] = field(default_factory=list)
    requires_user_review: bool = False

    def __post_init__(self) -> None:
        _validate_choice(
            "recommended_action",
            self.recommended_action,
            PROMOTION_ACTIONS,
        )


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
    supporting_witness_sources: list[ClaimSourceRecord] = field(default_factory=list)
    possible_non_equivalences: list[str] = field(default_factory=list)
    proxy_usage_refs: list[str] = field(default_factory=list)
    open_points: list[str] = field(default_factory=list)
    promotion_recommendation: IngressPromotionRecommendation | dict[str, object] = field(
        default_factory=lambda: IngressPromotionRecommendation(
            recommended_action="hold_ingress",
            rationale="No promotion recommendation recorded.",
        )
    )
    promoted_claim_ids: list[str] = field(default_factory=list)
    created_at: str = ""

    def __post_init__(self) -> None:
        _validate_pattern("ingress_id", self.ingress_id, INGRESS_ID_PATTERN)
        _validate_pattern("wave_id", self.wave_id, WAVE_ID_PATTERN)
        if self.ingress_kind not in INGRESS_KIND_DIRECTORIES:
            raise ValueError(f"Unsupported ingress_kind: {self.ingress_kind}")
        if not self.questions:
            raise ValueError("Ingress records require at least one question.")
        object.__setattr__(
            self,
            "primary_semantic_sources",
            _coerce_record_list(ClaimSourceRecord, self.primary_semantic_sources),
        )
        object.__setattr__(
            self,
            "supporting_witness_sources",
            _coerce_record_list(ClaimSourceRecord, self.supporting_witness_sources),
        )
        if not self.primary_semantic_sources:
            raise ValueError("Ingress records require at least one primary source.")
        object.__setattr__(
            self,
            "promotion_recommendation",
            _coerce_record(IngressPromotionRecommendation, self.promotion_recommendation),
        )

    def to_payload(self) -> dict[str, object]:
        return asdict(self)


def ingress_relative_path(record: IngressRecord) -> Path:
    kind_directory = INGRESS_KIND_DIRECTORIES[record.ingress_kind]
    return Path("ingress") / "waves" / record.wave_id / kind_directory / f"{record.ingress_id}.yaml"


def _promoted_claim_id(wave_id: str, semantic_id: str) -> str:
    return f"claim-{wave_id}-{semantic_id.removeprefix('sem-')}"


def _source_ref(record: ClaimSourceRecord) -> str:
    return record.relative_path or record.source_ref


def legacy_relative_path_within_root(relative_path: str) -> bool:
    candidate = PureWindowsPath(relative_path)
    if ".." in candidate.parts:
        return False
    normalized = PureWindowsPath(
        ntpath.normpath(
            str(candidate if candidate.is_absolute() else LEGACY_REPO_ROOT / candidate)
        )
    )
    try:
        normalized.relative_to(LEGACY_REPO_ROOT)
    except ValueError:
        return False
    return True


def _validate_legacy_sources(records: list[ClaimSourceRecord]) -> None:
    for record in records:
        if record.workspace_id != LEGACY_WORKSPACE_ID:
            raise ValueError("Ingress records require legacy source records.")
        if not record.relative_path:
            raise ValueError("Ingress records require legacy source records.")
        if not record.source_type.startswith("legacy_"):
            raise ValueError("Ingress records require legacy source records.")
        if not legacy_relative_path_within_root(record.relative_path):
            raise ValueError("Ingress records require legacy source records under the legacy root.")


def _load_ingress_index(registry_root: Path, wave_id: str) -> dict[str, object]:
    return yaml.safe_load(
        (registry_root / "ingress" / "waves" / wave_id / "index.yaml").read_text(encoding="utf-8")
    )


def _write_ingress_index(registry_root: Path, wave_id: str, payload: dict[str, object]) -> None:
    index_path = registry_root / "ingress" / "waves" / wave_id / "index.yaml"
    index_path.write_text(
        yaml.safe_dump(payload, sort_keys=False, allow_unicode=False),
        encoding="utf-8",
    )


def _upsert_index_entry(entries: list[dict[str, object]], entry: dict[str, object]) -> list[dict[str, object]]:
    retained = [item for item in entries if item.get("ingress_id") != entry["ingress_id"]]
    retained.append(entry)
    return sorted(retained, key=lambda item: str(item["ingress_id"]))


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
    index_entry = {
        "ingress_id": record.ingress_id,
        "title": record.title,
        "path": ingress_relative_path(record).as_posix(),
        "promotion_state": record.promotion_recommendation.recommended_action,
    }
    list_key = "question_clusters" if record.ingress_kind == "question_cluster" else "findings"
    other_key = "findings" if list_key == "question_clusters" else "question_clusters"
    index_payload[list_key] = _upsert_index_entry(list(index_payload.get(list_key, [])), index_entry)
    index_payload[other_key] = list(index_payload.get(other_key, []))
    _write_ingress_index(registry_root, record.wave_id, index_payload)

    return output_path


# Late import avoids a circular import because semantic_ingress_guard imports
# ingress symbols defined above.
from .semantic_ingress_guard import SemanticPromotionDraft, guard_ingress_record


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
    semantic_authority = (
        record.primary_semantic_sources[0].semantic_authority
        or "authoritative_semantic_source"
    )
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
                    _source_ref(source) for source in record.primary_semantic_sources
                ],
                supporting_source_refs=[
                    _source_ref(source) for source in record.supporting_witness_sources
                ],
                semantic_authority=semantic_authority,
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

    write_ingress_record(
        registry_root,
        replace(
            record,
            promotion_recommendation=IngressPromotionRecommendation(
                recommended_action="promote_to_semantic_claim",
                rationale="All structural promotion gates passed.",
                gate_failures=[],
                requires_user_review=False,
            ),
            promoted_claim_ids=[claim_id],
        ),
    )

    return claim_path

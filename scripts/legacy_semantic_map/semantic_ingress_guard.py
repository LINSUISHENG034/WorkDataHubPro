from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping
from typing import Sequence

import yaml

from .claims import ClaimSourceRecord
from .ingress import (
    INGRESS_KIND_DIRECTORIES,
    IngressRecord,
    LEGACY_WORKSPACE_ID,
    legacy_relative_path_within_root,
)
from .models import CONFIDENCE_LEVELS, SEMANTIC_NODE_TYPES
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

    def __post_init__(self) -> None:
        if self.semantic_node_type not in SEMANTIC_NODE_TYPES:
            raise ValueError(f"Unsupported semantic_node_type: {self.semantic_node_type}")
        if self.confidence not in CONFIDENCE_LEVELS:
            raise ValueError(f"Unsupported confidence: {self.confidence}")


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


def _check_sources(
    records: Sequence[ClaimSourceRecord],
    *,
    source_kind: str,
) -> list[str]:
    failures: list[str] = []
    for record in records:
        if (
            record.workspace_id != LEGACY_WORKSPACE_ID
            or not record.relative_path
            or not record.source_type.startswith("legacy_")
        ):
            failures.append(f"non_legacy_{source_kind}_source")
            continue
        if not legacy_relative_path_within_root(record.relative_path):
            failures.append(f"escaped_legacy_{source_kind}_source_path")
    return sorted(set(failures))


def _load_yaml(path: Path) -> dict[str, object]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if isinstance(payload, dict):
        return payload
    return {}


def _promoted_claim_id(wave_id: str, semantic_id: str) -> str:
    return f"claim-{wave_id}-{semantic_id.removeprefix('sem-')}"


def _overlap_hits(
    registry_root: Path,
    record: Mapping[str, object],
    promotion: Mapping[str, object] | None,
    *,
    wave_id: str,
    self_ingress_path: str | None = None,
) -> list[dict[str, str]]:
    semantic_id = str(promotion.get("semantic_id", "")) if promotion is not None else ""
    expected_claim_id = _promoted_claim_id(wave_id, semantic_id) if semantic_id else ""
    ingress_id = str(record.get("ingress_id", ""))
    title = str(record.get("title", ""))

    hits: list[dict[str, str]] = []
    for ingress_path in sorted((registry_root / "ingress" / "waves").glob("**/*.yaml")):
        if ingress_path.name == "index.yaml":
            continue
        relative_ingress_path = ingress_path.relative_to(registry_root).as_posix()
        if self_ingress_path and relative_ingress_path == self_ingress_path:
            continue
        payload = _load_yaml(ingress_path)
        match_type = None
        if expected_claim_id and expected_claim_id in list(payload.get("promoted_claim_ids", [])):
            match_type = "promoted_semantic_target"
        elif ingress_id and payload.get("ingress_id") == ingress_id:
            match_type = "ingress_id"
        elif title and payload.get("title") == title:
            match_type = "title"
        if match_type is not None:
            hits.append(
                {
                    "path": relative_ingress_path,
                    "match_type": match_type,
                }
            )

    if not semantic_id:
        return hits

    for claim_path in sorted((registry_root / "claims").glob("**/*.yaml")):
        payload = _load_yaml(claim_path)
        if payload.get("claim_target_id") == semantic_id:
            hits.append(
                {
                    "path": claim_path.relative_to(registry_root).as_posix(),
                    "match_type": "claim_target_id",
                }
            )

    for semantic_path in sorted((registry_root / "semantic").glob("**/*.yaml")):
        payload = _load_yaml(semantic_path)
        if payload.get("semantic_id") == semantic_id:
            hits.append(
                {
                    "path": semantic_path.relative_to(registry_root).as_posix(),
                    "match_type": "semantic_id",
                }
            )

    return hits


def _record_payload(record: IngressRecord | Mapping[str, object]) -> dict[str, object]:
    if isinstance(record, IngressRecord):
        return record.to_payload()
    return dict(record)


def _promotion_payload(
    promotion: SemanticPromotionDraft | Mapping[str, object] | None,
) -> dict[str, object] | None:
    if promotion is None:
        return None
    if isinstance(promotion, SemanticPromotionDraft):
        return asdict(promotion)
    return dict(promotion)


def _normalize_source_records(
    values: object,
    *,
    source_kind: str,
) -> tuple[list[ClaimSourceRecord], list[str]]:
    if not isinstance(values, list):
        return [], [f"malformed_{source_kind}_source"]

    records: list[ClaimSourceRecord] = []
    failures: list[str] = []
    for value in values:
        if isinstance(value, ClaimSourceRecord):
            records.append(value)
            continue
        if isinstance(value, dict):
            try:
                records.append(ClaimSourceRecord(**value))
            except (TypeError, ValueError):
                failures.append(f"malformed_{source_kind}_source")
            continue
        failures.append(f"malformed_{source_kind}_source")
    return records, sorted(set(failures))


def _write_target_failures(
    registry_root: Path,
    *,
    wave_id: str,
) -> list[str]:
    failures: list[str] = []
    if not (registry_root / "ingress" / "waves" / wave_id / "index.yaml").is_file():
        failures.append("missing_wave_ingress_index")
    if not (registry_root / "claims" / wave_id / "semantic").is_dir():
        failures.append("missing_wave_semantic_claim_dir")
    return failures


def _raw_promotion_validation_failures(promotion_payload: Mapping[str, object]) -> list[str]:
    failures: list[str] = []
    semantic_node_type = str(promotion_payload.get("semantic_node_type", "")).strip()
    if semantic_node_type and semantic_node_type not in SEMANTIC_NODE_TYPES:
        failures.append("invalid_semantic_node_type")
    confidence = str(promotion_payload.get("confidence", "")).strip()
    if confidence not in CONFIDENCE_LEVELS:
        failures.append("invalid_confidence")
    return failures


def _raw_record_validation_failures(record_payload: Mapping[str, object]) -> list[str]:
    failures: list[str] = []
    ingress_kind = str(record_payload.get("ingress_kind", "")).strip()
    if not ingress_kind:
        failures.append("missing_ingress_kind")
    elif ingress_kind not in INGRESS_KIND_DIRECTORIES:
        failures.append("invalid_ingress_kind")
    return failures


def _advertised_wave_id(record_payload: Mapping[str, object], *, target_wave_id: str) -> str:
    record_wave_id = str(record_payload.get("wave_id", "")).strip()
    return record_wave_id or target_wave_id


def _allowed_write_targets(
    record_payload: Mapping[str, object],
    *,
    wave_id: str,
) -> list[str]:
    ingress_kind = str(record_payload.get("ingress_kind", "")).strip()
    allowed_write_targets = [f"claims/{wave_id}/semantic"]
    kind_directory = INGRESS_KIND_DIRECTORIES.get(ingress_kind)
    if kind_directory is not None:
        allowed_write_targets.insert(0, f"ingress/waves/{wave_id}/{kind_directory}")
    return allowed_write_targets


def guard_ingress_record(
    registry_root: Path,
    record: IngressRecord | Mapping[str, object],
    promotion: SemanticPromotionDraft | Mapping[str, object] | None,
    *,
    wave_id: str | None = None,
) -> IngressGuardResult:
    record_payload = _record_payload(record)
    promotion_payload = _promotion_payload(promotion)
    target_wave_id, _ = resolve_requested_or_active_open_wave(registry_root, wave_id)
    advertised_wave_id = _advertised_wave_id(record_payload, target_wave_id=target_wave_id)
    self_ingress_path = None
    ingress_id = str(record_payload.get("ingress_id", ""))
    ingress_kind = str(record_payload.get("ingress_kind", "")).strip()
    if ingress_id and ingress_kind in INGRESS_KIND_DIRECTORIES:
        self_ingress_path = (
            f"ingress/waves/{advertised_wave_id}/"
            f"{INGRESS_KIND_DIRECTORIES[ingress_kind]}/"
            f"{ingress_id}.yaml"
        )
    primary_sources, primary_failures = _normalize_source_records(
        record_payload.get("primary_semantic_sources"),
        source_kind="primary",
    )
    supporting_sources, supporting_failures = _normalize_source_records(
        record_payload.get("supporting_witness_sources"),
        source_kind="supporting",
    )
    evidence_boundary_failures = (
        primary_failures
        + supporting_failures
        + _check_sources(
        primary_sources,
        source_kind="primary",
    )
        + _check_sources(
        supporting_sources,
        source_kind="supporting",
    )
    )
    evidence_boundary_failures = sorted(set(evidence_boundary_failures))

    promotion_gate_failures: list[str] = _write_target_failures(
        registry_root,
        wave_id=target_wave_id,
    )
    promotion_gate_failures.extend(_raw_record_validation_failures(record_payload))
    if advertised_wave_id != target_wave_id:
        promotion_gate_failures.append("record_wave_mismatch")
    if not primary_sources:
        promotion_gate_failures.append("missing_primary_semantic_source")
    if not supporting_sources:
        promotion_gate_failures.append("missing_supporting_witness_source")
    if promotion_payload is None:
        promotion_gate_failures.append("missing_promotion_draft")
    else:
        if not isinstance(promotion, SemanticPromotionDraft):
            promotion_gate_failures.extend(
                _raw_promotion_validation_failures(promotion_payload)
            )
        if not promotion_payload.get("main_conclusion_stable", False):
            promotion_gate_failures.append("main_conclusion_not_stable")
        if not promotion_payload.get("open_points_do_not_overturn", False):
            promotion_gate_failures.append("open_points_may_overturn_conclusion")
        if not str(promotion_payload.get("business_conclusion", "")).strip():
            promotion_gate_failures.append("missing_business_conclusion")
        if not str(promotion_payload.get("semantic_node_type", "")).strip():
            promotion_gate_failures.append("missing_semantic_node_type")
    promotion_gate_failures = sorted(set(promotion_gate_failures))

    overlap_hits = _overlap_hits(
        registry_root,
        record_payload,
        promotion_payload,
        wave_id=advertised_wave_id,
        self_ingress_path=self_ingress_path,
    )
    requires_user_review = bool(overlap_hits)
    if requires_user_review:
        promotion_status = "requires_user_review"
    elif evidence_boundary_failures or promotion_gate_failures:
        promotion_status = "blocked"
    else:
        promotion_status = "ready"

    return IngressGuardResult(
        wave_id=advertised_wave_id,
        allowed_write_targets=_allowed_write_targets(
            record_payload,
            wave_id=advertised_wave_id,
        ),
        promotion_status=promotion_status,
        promotion_gate_failures=promotion_gate_failures,
        evidence_boundary_failures=evidence_boundary_failures,
        overlap_hits=overlap_hits,
        requires_user_review=requires_user_review,
    )


def _load_record(path: Path) -> dict[str, object]:
    return _load_yaml(path)


def _load_promotion(path: Path | None) -> dict[str, object] | None:
    if path is None:
        return None
    return _load_yaml(path)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry-root", type=Path, required=True)
    parser.add_argument("--record", type=Path, required=True)
    parser.add_argument("--promotion", type=Path)
    parser.add_argument("--wave-id")
    args = parser.parse_args(argv)

    result = guard_ingress_record(
        args.registry_root,
        _load_record(args.record),
        _load_promotion(args.promotion),
        wave_id=args.wave_id,
    )
    print(json.dumps(result.to_payload(), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

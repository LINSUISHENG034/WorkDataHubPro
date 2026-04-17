from __future__ import annotations

import hashlib
import json
from pathlib import Path

import yaml


def _load_yaml(path: Path) -> dict[str, object]:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def _claim_paths_for_wave(registry_root: Path, wave_id: str) -> list[Path]:
    claims_root = registry_root / "claims" / wave_id
    if not claims_root.exists():
        return []
    return sorted(path for path in claims_root.rglob("*.yaml") if path.is_file())


def claim_digests_for_wave(
    registry_root: Path,
    wave_id: str,
    allowed_claim_ids: set[str] | None = None,
) -> dict[str, str]:
    digests: dict[str, str] = {}
    for path in _claim_paths_for_wave(registry_root, wave_id):
        payload = _load_yaml(path)
        claim_id = payload.get("claim_id")
        if isinstance(claim_id, str) and (
            allowed_claim_ids is None or claim_id in allowed_claim_ids
        ):
            digests[claim_id] = hashlib.sha256(path.read_bytes()).hexdigest()
    return dict(sorted(digests.items()))


def mutable_claim_ids(
    current_digests: dict[str, str],
    prior_digests: dict[str, str],
) -> list[str]:
    mutated = [
        claim_id
        for claim_id, digest in prior_digests.items()
        if current_digests.get(claim_id) != digest
    ]
    late_additions = [
        claim_id for claim_id in current_digests if claim_id not in prior_digests
    ]
    return sorted(set(mutated + late_additions))


def prior_integrity_report_digests(report_path: Path) -> dict[str, str]:
    if not report_path.exists():
        return {}
    payload = json.loads(report_path.read_text(encoding="utf-8"))
    digests = payload.get("accepted_claim_digests", {})
    if not isinstance(digests, dict):
        return {}
    return {str(key): str(value) for key, value in digests.items()}

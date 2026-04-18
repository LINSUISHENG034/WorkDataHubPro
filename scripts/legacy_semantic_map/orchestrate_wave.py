from __future__ import annotations

import argparse
from dataclasses import replace
import json
from pathlib import Path

import yaml

from .bootstrap import DEFAULT_REGISTRY_ROOT
from .claims import ClaimArtifact, write_claim_artifact
from .compiler import compile_claim_artifacts
from .reporting import generate_reports
from .waves import require_active_open_wave

SOURCE_WAVE_ID = "wave-2026-04-17-customer-status-semantic-pilot"
SUCCESSOR_WAVE_ID = "wave-2026-04-17-semantic-governance-reframe"
DEFAULT_TRIGGER_ID = "trigger-semantic-governance-reframe"


def _source_claim_paths(registry_root: Path) -> list[Path]:
    claims_root = registry_root / "claims" / SOURCE_WAVE_ID / "semantic"
    return sorted(claims_root.glob("*.yaml"))


def build_successor_wave_claims(
    registry_root: Path,
    wave_id: str,
    *,
    trigger_id: str = DEFAULT_TRIGGER_ID,
    orchestration_iteration: int = 1,
) -> list[ClaimArtifact]:
    source_prefix = f"claim-{SOURCE_WAVE_ID}-"
    successor_claims: list[ClaimArtifact] = []
    for path in _source_claim_paths(registry_root):
        source_claim = ClaimArtifact(**yaml.safe_load(path.read_text(encoding="utf-8")))
        suffix = source_claim.claim_id.removeprefix(source_prefix)
        successor_claims.append(
            replace(
                source_claim,
                claim_id=f"claim-{wave_id}-{suffix}",
                wave_id=wave_id,
                trigger_id=trigger_id,
                orchestration_iteration=orchestration_iteration,
            )
        )
    if not successor_claims:
        raise ValueError(f"No semantic source claims found under {SOURCE_WAVE_ID}")
    return successor_claims


def orchestrate_wave(
    registry_root: Path,
    wave_id: str,
    *,
    trigger_id: str = DEFAULT_TRIGGER_ID,
    orchestration_iteration: int = 1,
) -> dict[str, object]:
    resolved_root = registry_root.resolve()
    require_active_open_wave(resolved_root, wave_id)
    accepted_claim_paths = [
        write_claim_artifact(resolved_root, claim)
        for claim in build_successor_wave_claims(
            resolved_root,
            wave_id,
            trigger_id=trigger_id,
            orchestration_iteration=orchestration_iteration,
        )
    ]
    compilation = compile_claim_artifacts(resolved_root, accepted_claim_paths)
    reports = generate_reports(resolved_root, wave_id=wave_id)
    return {
        "wave_id": wave_id,
        "trigger_id": trigger_id,
        "claim_paths": [
            path.resolve().relative_to(resolved_root).as_posix()
            for path in accepted_claim_paths
        ],
        "compiled_claim_ids": compilation.compiled_claim_ids,
        "generated_canonical_files": compilation.written_files,
        "coverage_report": reports.wave_coverage_report.resolve()
        .relative_to(resolved_root)
        .as_posix(),
        "integrity_report": reports.wave_integrity_report.resolve()
        .relative_to(resolved_root)
        .as_posix(),
        "semantic_discovery_report": reports.semantic_discovery_report.resolve()
        .relative_to(resolved_root)
        .as_posix(),
        "semantic_readiness_report": reports.semantic_readiness_report.resolve()
        .relative_to(resolved_root)
        .as_posix(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry-root", type=Path, default=DEFAULT_REGISTRY_ROOT)
    parser.add_argument("--wave-id", default=SUCCESSOR_WAVE_ID)
    parser.add_argument("--trigger-id", default=DEFAULT_TRIGGER_ID)
    parser.add_argument("--orchestration-iteration", type=int, default=1)
    args = parser.parse_args()
    print(
        json.dumps(
            orchestrate_wave(
                args.registry_root.resolve(),
                args.wave_id,
                trigger_id=args.trigger_id,
                orchestration_iteration=args.orchestration_iteration,
            ),
            indent=2,
        )
    )


if __name__ == "__main__":
    main()

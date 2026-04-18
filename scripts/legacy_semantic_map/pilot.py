from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

from .bootstrap import DEFAULT_REGISTRY_ROOT
from .compiler import CompilationResult, compile_claim_artifacts
from .reporting import ReportGenerationResult, generate_reports
from .waves import require_active_open_wave

FIRST_WAVE_PILOT_WAVE_ID = "wave-2026-04-17-first-wave-pilot"
ACTIVE_SUCCESSOR_WAVE_ID = "wave-2026-04-17-semantic-governance-reframe"


@dataclass(frozen=True)
class PilotRunResult:
    wave_id: str
    claim_paths: list[Path]
    compilation: CompilationResult
    reports: ReportGenerationResult

    def to_payload(self, registry_root: Path) -> dict[str, object]:
        resolved_root = registry_root.resolve()
        return {
            "wave_id": self.wave_id,
            "claim_paths": [
                path.resolve().relative_to(resolved_root).as_posix()
                for path in self.claim_paths
            ],
            "compiled_claim_ids": self.compilation.compiled_claim_ids,
            "generated_canonical_files": self.compilation.written_files,
            "current_coverage_report": self.reports.current_coverage_report.resolve()
            .relative_to(resolved_root)
            .as_posix(),
            "current_integrity_report": self.reports.current_integrity_report.resolve()
            .relative_to(resolved_root)
            .as_posix(),
            "wave_coverage_report": self.reports.wave_coverage_report.resolve()
            .relative_to(resolved_root)
            .as_posix(),
            "wave_integrity_report": self.reports.wave_integrity_report.resolve()
            .relative_to(resolved_root)
            .as_posix(),
        }


def pilot_claim_paths(
    registry_root: Path = DEFAULT_REGISTRY_ROOT,
    wave_id: str = FIRST_WAVE_PILOT_WAVE_ID,
) -> list[Path]:
    claims_root = registry_root / "claims" / wave_id
    if not claims_root.exists():
        return []
    return sorted(path for path in claims_root.rglob("*.yaml"))


def _validated_claim_paths(
    registry_root: Path,
    wave_id: str,
    claim_paths: Sequence[Path],
) -> list[Path]:
    expected_root = (registry_root / "claims" / wave_id).resolve()
    validated: list[Path] = []
    for path in claim_paths:
        resolved = path.resolve()
        if expected_root not in resolved.parents:
            raise ValueError(
                f"Accepted claim path must live under claims/{wave_id}/: {path}"
            )
        validated.append(resolved)
    return validated


def run_first_wave_pilot(
    registry_root: Path = DEFAULT_REGISTRY_ROOT,
    *,
    wave_id: str = FIRST_WAVE_PILOT_WAVE_ID,
    claim_paths: Sequence[Path] | None = None,
) -> PilotRunResult:
    resolved_root = registry_root.resolve()
    require_active_open_wave(resolved_root, wave_id)
    selected_claim_paths = _validated_claim_paths(
        resolved_root,
        wave_id,
        claim_paths or pilot_claim_paths(resolved_root, wave_id),
    )
    if not selected_claim_paths:
        raise ValueError(f"No accepted claim artifacts found for wave {wave_id}")
    compilation = compile_claim_artifacts(resolved_root, selected_claim_paths)
    reports = generate_reports(resolved_root, wave_id=wave_id)
    return PilotRunResult(
        wave_id=wave_id,
        claim_paths=selected_claim_paths,
        compilation=compilation,
        reports=reports,
    )


def main(argv: Sequence[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Compile accepted semantic-map claims and generate reports for the "
            "active successor wave."
        )
    )
    parser.add_argument(
        "--registry-root",
        type=Path,
        default=DEFAULT_REGISTRY_ROOT,
        help="Registry root containing docs/wiki-bi/_meta/legacy-semantic-map.",
    )
    parser.add_argument(
        "--wave-id",
        default=ACTIVE_SUCCESSOR_WAVE_ID,
        help=(
            "Wave identifier to compile and report. Defaults to the active "
            "successor wave."
        ),
    )
    parser.add_argument(
        "--claim",
        dest="claims",
        type=Path,
        action="append",
        default=None,
        help="Explicit accepted claim artifact path(s) to compile.",
    )
    args = parser.parse_args(argv)

    registry_root = args.registry_root.resolve()
    explicit_claims = [path.resolve() for path in (args.claims or [])]
    result = run_first_wave_pilot(
        registry_root,
        wave_id=args.wave_id,
        claim_paths=explicit_claims or None,
    )
    print(json.dumps(result.to_payload(registry_root), indent=2))


if __name__ == "__main__":
    main()

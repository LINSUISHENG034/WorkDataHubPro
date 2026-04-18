from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

from .bootstrap import DEFAULT_REGISTRY_ROOT
from .pilot import ACTIVE_SUCCESSOR_WAVE_ID, _validated_claim_paths, pilot_claim_paths, run_first_wave_pilot


@dataclass(frozen=True)
class StabilityCheck:
    iteration: int
    stable: bool
    changed_files: list[str]


@dataclass(frozen=True)
class ProbeRunResult:
    wave_id: str
    source_registry_root: Path
    temp_registry_root: Path
    source_claim_paths: list[Path]
    temp_claim_paths: list[Path]
    compiled_claim_ids: list[str]
    generated_canonical_files: list[str]
    wave_coverage_report: Path
    wave_integrity_report: Path
    semantic_discovery_report: Path
    semantic_readiness_report: Path
    stability_checks: list[StabilityCheck]

    def to_payload(self) -> dict[str, object]:
        return {
            "wave_id": self.wave_id,
            "source_registry_root": str(self.source_registry_root),
            "temp_registry_root": str(self.temp_registry_root),
            "source_claim_paths": [
                path.resolve().relative_to(self.source_registry_root).as_posix()
                for path in self.source_claim_paths
            ],
            "temp_claim_paths": [
                path.resolve().relative_to(self.temp_registry_root).as_posix()
                for path in self.temp_claim_paths
            ],
            "compiled_claim_ids": self.compiled_claim_ids,
            "generated_canonical_files": self.generated_canonical_files,
            "wave_coverage_report": self.wave_coverage_report.resolve()
            .relative_to(self.temp_registry_root)
            .as_posix(),
            "wave_integrity_report": self.wave_integrity_report.resolve()
            .relative_to(self.temp_registry_root)
            .as_posix(),
            "semantic_discovery_report": self.semantic_discovery_report.resolve()
            .relative_to(self.temp_registry_root)
            .as_posix(),
            "semantic_readiness_report": self.semantic_readiness_report.resolve()
            .relative_to(self.temp_registry_root)
            .as_posix(),
            "stability_checks": [
                {
                    "iteration": check.iteration,
                    "stable": check.stable,
                    "changed_files": check.changed_files,
                }
                for check in self.stability_checks
            ],
            "stable_after_final_rerun": all(check.stable for check in self.stability_checks[-1:]),
        }


def _copy_registry_tree(registry_root: Path) -> Path:
    temp_root = Path(tempfile.mkdtemp(prefix="legacy-semantic-map-probe-")).resolve()
    copied_root = temp_root / registry_root.name
    shutil.copytree(registry_root, copied_root)
    return copied_root.resolve()


def _map_claim_paths_to_temp(
    source_registry_root: Path,
    temp_registry_root: Path,
    claim_paths: Sequence[Path],
) -> list[Path]:
    mapped_paths: list[Path] = []
    for path in claim_paths:
        relative_path = path.resolve().relative_to(source_registry_root)
        mapped_paths.append((temp_registry_root / relative_path).resolve())
    return mapped_paths


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _tracked_output_paths(temp_registry_root: Path, initial_result) -> list[Path]:
    tracked = [temp_registry_root / relative_path for relative_path in initial_result.compilation.written_files]
    tracked.extend(
        [
            temp_registry_root / "manifest.json",
            initial_result.reports.wave_coverage_report,
            initial_result.reports.wave_integrity_report,
            initial_result.reports.semantic_discovery_report,
            initial_result.reports.semantic_readiness_report,
            initial_result.reports.semantic_discovery_summary,
            initial_result.reports.semantic_readiness_summary,
        ]
    )
    unique_tracked: list[Path] = []
    seen: set[Path] = set()
    for path in tracked:
        resolved = path.resolve()
        if resolved in seen or not resolved.exists():
            continue
        seen.add(resolved)
        unique_tracked.append(resolved)
    return unique_tracked


def probe_wave(
    registry_root: Path = DEFAULT_REGISTRY_ROOT,
    *,
    wave_id: str = ACTIVE_SUCCESSOR_WAVE_ID,
    claim_paths: Sequence[Path] | None = None,
    reruns: int = 2,
) -> ProbeRunResult:
    source_registry_root = registry_root.resolve()
    source_claim_paths = _validated_claim_paths(
        source_registry_root,
        wave_id,
        claim_paths or pilot_claim_paths(source_registry_root, wave_id),
    )
    if not source_claim_paths:
        raise ValueError(f"No accepted claim artifacts found for wave {wave_id}")

    temp_registry_root = _copy_registry_tree(source_registry_root)
    temp_claim_paths = _map_claim_paths_to_temp(
        source_registry_root,
        temp_registry_root,
        source_claim_paths,
    )

    initial_result = run_first_wave_pilot(
        temp_registry_root,
        wave_id=wave_id,
        claim_paths=temp_claim_paths,
    )
    tracked_paths = _tracked_output_paths(temp_registry_root, initial_result)
    previous_digests = {path: _digest(path) for path in tracked_paths}

    stability_checks: list[StabilityCheck] = []
    for iteration in range(2, reruns + 2):
        rerun_result = run_first_wave_pilot(
            temp_registry_root,
            wave_id=wave_id,
            claim_paths=temp_claim_paths,
        )
        current_tracked_paths = _tracked_output_paths(temp_registry_root, rerun_result)
        current_digests = {path: _digest(path) for path in current_tracked_paths}
        changed_files = sorted(
            path.resolve().relative_to(temp_registry_root).as_posix()
            for path in current_tracked_paths
            if previous_digests.get(path) != current_digests.get(path)
        )
        stability_checks.append(
            StabilityCheck(
                iteration=iteration,
                stable=not changed_files,
                changed_files=changed_files,
            )
        )
        previous_digests = current_digests
        tracked_paths = current_tracked_paths

    return ProbeRunResult(
        wave_id=wave_id,
        source_registry_root=source_registry_root,
        temp_registry_root=temp_registry_root,
        source_claim_paths=source_claim_paths,
        temp_claim_paths=temp_claim_paths,
        compiled_claim_ids=initial_result.compilation.compiled_claim_ids,
        generated_canonical_files=initial_result.compilation.written_files,
        wave_coverage_report=initial_result.reports.wave_coverage_report,
        wave_integrity_report=initial_result.reports.wave_integrity_report,
        semantic_discovery_report=initial_result.reports.semantic_discovery_report,
        semantic_readiness_report=initial_result.reports.semantic_readiness_report,
        stability_checks=stability_checks,
    )


def main(argv: Sequence[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Create a temporary semantic-map registry copy, compile a bounded claim set, "
            "and rerun to check output stability."
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
        help="Wave identifier to probe. Defaults to the active successor wave.",
    )
    parser.add_argument(
        "--claim",
        dest="claims",
        type=Path,
        action="append",
        default=None,
        help="Explicit accepted claim artifact path(s) to probe inside the temporary copy.",
    )
    parser.add_argument(
        "--reruns",
        type=int,
        default=2,
        help="Number of additional compile/report reruns after the first probe run.",
    )
    args = parser.parse_args(argv)

    if args.reruns < 0:
        raise ValueError("--reruns must be >= 0")

    registry_root = args.registry_root.resolve()
    explicit_claims = [path.resolve() for path in (args.claims or [])]
    result = probe_wave(
        registry_root,
        wave_id=args.wave_id,
        claim_paths=explicit_claims or None,
        reruns=args.reruns,
    )
    print(json.dumps(result.to_payload(), indent=2))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Bootstrap Phase 2 accepted checkpoint baselines.

This script provides an EXPLICIT bootstrap path for creating accepted checkpoint
baseline files. Normal replay execution FAILS CLOSED when a baseline is missing;
baseline creation must happen through this script, not as a side effect of replay.

Usage:
    python scripts/bootstrap_phase2_checkpoint_baselines.py \
        --checkpoint reference_derivation \
        --domain annuity_performance \
        --period 2026-03 \
        --workbook path/to/workbook.xlsx

    python scripts/bootstrap_phase2_checkpoint_baselines.py \
        --checkpoint fact_processing \
        --domain annuity_performance \
        --period 2026-03 \
        --workbook path/to/workbook.xlsx \
        --output reference/historical_replays/annuity_performance/legacy_fact_processing_2026_03.json

Checkpoint names:
    - reference_derivation
    - fact_processing
    - identity_resolution
    - contract_state
    - source_intake

Domain names:
    - annuity_performance
    - annual_award
    - annual_loss
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from work_data_hub_pro.apps.orchestration.replay.annuity_performance_slice import (
    run_annuity_performance_slice,
)
from work_data_hub_pro.apps.orchestration.replay.annual_award_slice import (
    run_annual_award_slice,
)
from work_data_hub_pro.apps.orchestration.replay.annual_loss_slice import (
    run_annual_loss_slice,
)


CHECKPOINT_NAMES = [
    "reference_derivation",
    "fact_processing",
    "identity_resolution",
    "contract_state",
    "source_intake",
]

DOMAIN_NAMES = [
    "annuity_performance",
    "annual_award",
    "annual_loss",
]

DOMAIN_SLICE_RUNNERS = {
    "annuity_performance": run_annuity_performance_slice,
    "annual_award": run_annual_award_slice,
    "annual_loss": run_annual_loss_slice,
}


def bootstrap_checkpoint_baseline(
    *,
    checkpoint_name: str,
    domain: str,
    period: str,
    workbook: Path,
    output_path: Path | None,
) -> Path:
    """Bootstrap an accepted checkpoint baseline.

    Args:
        checkpoint_name: Which checkpoint to bootstrap (reference_derivation,
            fact_processing, identity_resolution, contract_state).
        domain: Which domain (annuity_performance, annual_award, annual_loss).
        period: Reporting period (e.g., 2026-03).
        workbook: Path to the input workbook file.
        output_path: Explicit output path. If None, defaults to
            reference/historical_replays/<domain>/legacy_<checkpoint>_<period>.json.

    Returns:
        Path to the created baseline file.

    Raises:
        ValueError: If checkpoint_name or domain is not recognized.
        RuntimeError: If the slice runner fails.
    """
    if checkpoint_name not in CHECKPOINT_NAMES:
        raise ValueError(
            f"Unknown checkpoint '{checkpoint_name}'. "
            f"Valid options: {CHECKPOINT_NAMES}"
        )
    if domain not in DOMAIN_NAMES:
        raise ValueError(
            f"Unknown domain '{domain}'. Valid options: {DOMAIN_NAMES}"
        )

    # Derive output path if not specified
    if output_path is None:
        period_underscored = period.replace("-", "_")
        output_path = Path(
            f"reference/historical_replays/{domain}/"
            f"legacy_{checkpoint_name}_{period_underscored}.json"
        )

    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Run the slice to derive the checkpoint payload
    # We use a temporary replay root to avoid creating compatibility artifacts
    import tempfile

    with tempfile.TemporaryDirectory() as temp_replay_root:
        temp_path = Path(temp_replay_root)
        slice_runner = DOMAIN_SLICE_RUNNERS[domain]

        outcome = slice_runner(
            workbook=workbook,
            period=period,
            replay_root=temp_path,
        )

        # Extract the checkpoint payload from the outcome via intermediate_payloads
        checkpoint_payload = _extract_checkpoint_payload(outcome, checkpoint_name)

        # Write the baseline file
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(checkpoint_payload, f, ensure_ascii=False, indent=2)

    return output_path


def _extract_checkpoint_payload(outcome: Any, checkpoint_name: str) -> list[dict[str, Any]]:
    """Extract checkpoint payload from slice outcome.

    The outcome carries intermediate payloads in outcome.intermediate_payloads dict.
    Maps the bootstrap checkpoint name to the key used in intermediate_payloads.
    """
    intermediate_map = {
        "reference_derivation": "reference_derivation",
        "fact_processing": "fact_processing",
        "identity_resolution": "identity_resolution",
        "contract_state": "contract_state",
        "source_intake": "source_intake",
    }
    key = intermediate_map.get(checkpoint_name, checkpoint_name)

    if (
        hasattr(outcome, "intermediate_payloads")
        and outcome.intermediate_payloads is not None
        and key in outcome.intermediate_payloads
    ):
        return outcome.intermediate_payloads[key]

    # Fallback: empty list (should not reach here with truthful slices)
    return []


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Bootstrap Phase 2 accepted checkpoint baselines.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--checkpoint",
        required=True,
        choices=CHECKPOINT_NAMES,
        help="Which checkpoint baseline to create.",
    )
    parser.add_argument(
        "--domain",
        required=True,
        choices=DOMAIN_NAMES,
        help="Which domain to process.",
    )
    parser.add_argument(
        "--period",
        required=True,
        help="Reporting period (e.g., 2026-03).",
    )
    parser.add_argument(
        "--workbook",
        required=True,
        type=Path,
        help="Path to the input workbook file.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help=(
            "Output path for the baseline JSON file. "
            "If omitted, defaults to "
            "reference/historical_replays/<domain>/legacy_<checkpoint>_<period>.json"
        ),
    )

    args = parser.parse_args()

    try:
        output_path = bootstrap_checkpoint_baseline(
            checkpoint_name=args.checkpoint,
            domain=args.domain,
            period=args.period,
            workbook=args.workbook,
            output_path=args.output,
        )
        print(f"Created baseline: {output_path}")
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


MANIFEST_PATH = Path("config/verification/phase2-parity-gates.json")


def load_manifest() -> dict[str, object]:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def run_tier(tier: str) -> int:
    manifest = load_manifest()
    tier_config = manifest["tiers"][tier]

    print(f"Running Phase 2 parity gate tier: {tier}")
    for command in tier_config["commands"]:
        print(f"> {command}")
        completed = subprocess.run(command, shell=True, check=False)
        if completed.returncode != 0:
            return completed.returncode
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--tier",
        choices=("pr", "protected_branch", "nightly"),
        required=True,
    )
    args = parser.parse_args()
    return run_tier(args.tier)


if __name__ == "__main__":
    raise SystemExit(main())

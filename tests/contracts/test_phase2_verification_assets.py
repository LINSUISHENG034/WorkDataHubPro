from __future__ import annotations

import json
import re
from pathlib import Path


def test_phase2_asset_manifest_has_status_fields() -> None:
    manifest_path = Path("reference/verification_assets/phase2-accepted-slices.json")
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))

    assert payload["phase"] == "02"
    assert payload["accepted_slices"] == [
        "annuity_performance",
        "annual_award",
        "annual_loss",
    ]
    for asset in payload["assets"]:
        assert asset["asset_id"]
        assert asset["asset_kind"]
        assert asset["slice"]
        assert asset["status"] in {"accepted", "deferred", "planned", "retired"}
        assert asset["purpose"]
        assert asset["refresh_trigger"]
        assert asset["reference_location"]


def test_phase2_checkpoint_baseline_assets_are_registered() -> None:
    """Verify that checkpoint baseline assets are registered for all accepted slices (T-06-10)."""
    manifest_path = Path("reference/verification_assets/phase2-accepted-slices.json")
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))

    # Map of domain -> set of expected checkpoint baselines
    expected_checkpoints = {
        "annuity_performance": {
            "reference_derivation",
            "fact_processing",
            "identity_resolution",
            "contract_state",
        },
        "annual_award": {
            "reference_derivation",
            "fact_processing",
            "identity_resolution",
            "contract_state",
        },
        "annual_loss": {
            "reference_derivation",
            "fact_processing",
            "identity_resolution",
            "contract_state",
        },
    }

    # Build map of registered checkpoint baselines: slice -> set of checkpoints
    registered_checkpoints: dict[str, set[str]] = {}
    for asset in payload["assets"]:
        if asset["asset_kind"] == "checkpoint_baseline":
            slice_name = asset["slice"]
            registered_checkpoints.setdefault(slice_name, set()).add(asset["checkpoint"])

    # Assert each accepted slice has all four checkpoint baselines registered
    for slice_name, checkpoints in expected_checkpoints.items():
        assert slice_name in registered_checkpoints, (
            f"Slice '{slice_name}' has no checkpoint_baseline assets registered"
        )
        registered = registered_checkpoints[slice_name]
        assert checkpoints.issubset(registered), (
            f"Slice '{slice_name}' missing checkpoint baselines: "
            f"{checkpoints - registered}"
        )
        for checkpoint in checkpoints:
            # Find the corresponding asset
            matching = [
                a for a in payload["assets"]
                if a["asset_kind"] == "checkpoint_baseline"
                and a["slice"] == slice_name
                and a["checkpoint"] == checkpoint
            ]
            assert len(matching) == 1, (
                f"Expected exactly one asset for {slice_name}/{checkpoint}"
            )
            asset = matching[0]
            assert asset["status"] == "accepted", (
                f"Checkpoint baseline {slice_name}/{checkpoint} must be 'accepted'"
            )
            assert Path(asset["reference_location"]).exists(), (
                f"Checkpoint baseline file does not exist: {asset['reference_location']}"
            )


def test_phase2_asset_manifest_has_all_required_fields() -> None:
    """Verify every asset entry has all required governance fields."""
    manifest_path = Path("reference/verification_assets/phase2-accepted-slices.json")
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))

    required_fields = {
        "asset_id",
        "asset_kind",
        "slice",
        "status",
        "purpose",
        "refresh_trigger",
        "reference_location",
    }

    for asset in payload["assets"]:
        missing = required_fields - set(asset.keys())
        assert not missing, f"Asset {asset.get('asset_id', '?')} missing fields: {missing}"


def test_forgotten_mechanism_output_uses_explicit_statuses() -> None:
    forgotten_path = Path(
        ".planning/phases/02-transparent-pipeline-contracts-parity-gates/02-FORGOTTEN-MECHANISMS.md"
    )
    contents = forgotten_path.read_text(encoding="utf-8")

    assert "verification assets" in contents
    assert "hidden runtime contracts" in contents
    assert "operator artifacts" in contents
    assert "parity scripts" in contents

    statuses = re.findall(r"\|\s*(accepted|deferred|retired)\s*\|", contents)
    assert statuses
    assert set(statuses) <= {"accepted", "deferred", "retired"}

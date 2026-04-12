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

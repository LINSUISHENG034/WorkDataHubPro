from __future__ import annotations

import json
from pathlib import Path


def test_phase2_gate_matrix_has_three_tiers() -> None:
    manifest = json.loads(
        Path("config/verification/phase2-parity-gates.json").read_text(
            encoding="utf-8"
        )
    )

    assert set(manifest["tiers"]) == {"pr", "protected_branch", "nightly"}
    for tier_name in ("pr", "protected_branch", "nightly"):
        assert manifest["tiers"][tier_name]["commands"]


def test_phase2_gate_runner_supports_all_tiers() -> None:
    runner_source = Path("scripts/run_phase2_parity_gates.py").read_text(
        encoding="utf-8"
    )
    runbook = Path("docs/runbooks/phase2-parity-gates.md").read_text(
        encoding="utf-8"
    )

    assert "--tier" in runner_source
    assert "pr" in runner_source
    assert "protected_branch" in runner_source
    assert "nightly" in runner_source
    assert "## PR Gate" in runbook
    assert "## Protected Branch Gate" in runbook
    assert "## Nightly Gate" in runbook
    assert "run_phase2_parity_gates.py" in runbook

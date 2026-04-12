"""Phase 6 contract tests for gate_runtime.py.

Verifies:
- Fail-closed baseline loading for reference-derivation checkpoints
- Correct duplicate-row diff accounting using multiset subtraction
- Explicit bootstrap script declares required CLI arguments
"""
from __future__ import annotations

import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

import pytest

# Import from the gate runtime under test
from work_data_hub_pro.governance.compatibility.gate_runtime import (
    _build_diff,
    load_required_checkpoint_baseline,
)


class TestBuildDiffDuplicateRows:
    """Tests for correct multiset subtraction in _build_diff."""

    def test_build_diff_counts_duplicate_rows_correctly(self):
        """Legacy has 3 identical rows, Pro has 1 identical row.

        Expected: 2 missing rows (3 - 1 = 2), 0 extra rows.
        """
        row = {"id": 1, "name": "test"}
        legacy_payload = [row, row, row]  # 3 copies
        pro_payload = [row]  # 1 copy

        result = _build_diff(legacy_payload, pro_payload)

        assert len(result.missing_rows) == 2, (
            f"Expected 2 missing rows (3 legacy - 1 pro), got {len(result.missing_rows)}"
        )
        assert len(result.extra_rows) == 0, (
            f"Expected 0 extra rows, got {len(result.extra_rows)}"
        )

    def test_build_diff_counts_extra_rows_correctly(self):
        """Legacy has 1 identical row, Pro has 3 identical rows.

        Expected: 0 missing rows, 2 extra rows (3 - 1 = 2).
        """
        row = {"id": 1, "name": "test"}
        legacy_payload = [row]  # 1 copy
        pro_payload = [row, row, row]  # 3 copies

        result = _build_diff(legacy_payload, pro_payload)

        assert len(result.missing_rows) == 0, (
            f"Expected 0 missing rows, got {len(result.missing_rows)}"
        )
        assert len(result.extra_rows) == 2, (
            f"Expected 2 extra rows (3 pro - 1 legacy), got {len(result.extra_rows)}"
        )

    def test_build_diff_counts_mixed_duplicate_rows_correctly(self):
        """Legacy has 2 copies of row A, 1 copy of row B.
        Pro has 1 copy of row A, 2 copies of row B.

        Expected: 1 missing row A, 1 extra row B.
        """
        row_a = {"id": 1, "name": "a"}
        row_b = {"id": 2, "name": "b"}
        legacy_payload = [row_a, row_a, row_b]  # 2 A, 1 B
        pro_payload = [row_a, row_b, row_b]  # 1 A, 2 B

        result = _build_diff(legacy_payload, pro_payload)

        assert len(result.missing_rows) == 1, (
            f"Expected 1 missing row (row A), got {len(result.missing_rows)}"
        )
        assert len(result.extra_rows) == 1, (
            f"Expected 1 extra row (row B), got {len(result.extra_rows)}"
        )


class TestLoadRequiredCheckpointBaseline:
    """Tests for fail-closed baseline loading."""

    def test_missing_reference_derivation_baseline_fails_closed(self, tmp_path):
        """When the accepted baseline file is absent, raise FileNotFoundError.

        The error message must contain 'Missing accepted baseline for checkpoint'.
        """
        missing_file = tmp_path / "legacy_reference_derivation_2026_03.json"

        with pytest.raises(FileNotFoundError) as exc_info:
            load_required_checkpoint_baseline(missing_file, "reference_derivation")

        assert "Missing accepted baseline for checkpoint" in str(exc_info.value), (
            f"Expected error message to contain 'Missing accepted baseline for checkpoint', "
            f"got: {exc_info.value}"
        )

    def test_existing_baseline_loads_successfully(self, tmp_path):
        """When the baseline file exists, return its parsed JSON content."""
        baseline_file = tmp_path / "legacy_reference_derivation_2026_03.json"
        expected_content = [{"id": 1, "data": "test"}]
        baseline_file.write_text(json.dumps(expected_content), encoding="utf-8")

        result = load_required_checkpoint_baseline(baseline_file, "reference_derivation")

        assert result == expected_content


class TestBootstrapScriptExplicitCli:
    """Contract tests verifying the bootstrap script has explicit CLI."""

    def test_bootstrap_script_declares_explicit_cli(self):
        """Bootstrap script must declare --checkpoint, --domain, --period, --output.

        This ensures baseline creation is explicit and discoverable, not hidden.
        """
        script_path = Path("scripts/bootstrap_phase2_checkpoint_baselines.py")

        if not script_path.exists():
            pytest.skip(f"Bootstrap script not yet created at {script_path}")

        content = script_path.read_text(encoding="utf-8")

        # Verify argparse is used
        assert "argparse" in content, (
            "Bootstrap script must use argparse for explicit CLI"
        )

        # Verify required arguments are declared
        required_args = [
            "--checkpoint",
            "--domain",
            "--period",
            "--output",
        ]
        for arg in required_args:
            assert arg in content, (
                f"Bootstrap script must declare {arg}"
            )

        # Verify checkpoint names are present
        checkpoint_names = [
            "reference_derivation",
            "fact_processing",
            "identity_resolution",
            "contract_state",
        ]
        for name in checkpoint_names:
            assert name in content, (
                f"Bootstrap script must mention checkpoint name: {name}"
            )

        # Verify legacy_ prefix is used for output files
        assert "legacy_" in content, (
            "Bootstrap script output must use legacy_ prefix convention"
        )

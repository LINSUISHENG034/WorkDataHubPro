from __future__ import annotations

from pathlib import Path

from scripts.legacy_semantic_map.pilot import ACTIVE_SUCCESSOR_WAVE_ID


REPO_ROOT = Path(__file__).resolve().parents[2]


def test_pilot_cli_defaults_to_active_successor_wave() -> None:
    pilot_source = (
        REPO_ROOT / "scripts" / "legacy_semantic_map" / "pilot.py"
    ).read_text(encoding="utf-8")

    assert ACTIVE_SUCCESSOR_WAVE_ID == "wave-2026-04-17-semantic-governance-reframe"
    assert 'default=ACTIVE_SUCCESSOR_WAVE_ID' in pilot_source
    assert "active successor wave" in pilot_source


def test_semantic_map_runbook_points_default_command_at_successor_wave() -> None:
    runbook = (
        REPO_ROOT / "docs" / "runbooks" / "legacy-semantic-map-first-wave-pilot.md"
    ).read_text(encoding="utf-8")

    assert "default front door now targets `wave-2026-04-17-semantic-governance-reframe`" in runbook
    assert (
        "uv run python -m scripts.legacy_semantic_map.pilot --registry-root docs/wiki-bi/_meta/legacy-semantic-map"
        in runbook
    )
    assert "--wave-id wave-2026-04-17-first-wave-pilot" in runbook
    assert "`closeout_ready = false`" in runbook

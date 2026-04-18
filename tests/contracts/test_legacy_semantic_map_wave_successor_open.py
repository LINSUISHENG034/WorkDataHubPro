from __future__ import annotations

from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[2]
WAVES_INDEX = (
    REPO_ROOT
    / "docs"
    / "wiki-bi"
    / "_meta"
    / "legacy-semantic-map"
    / "waves"
    / "index.yaml"
)


def test_successor_wave_is_open_and_active() -> None:
    payload = yaml.safe_load(WAVES_INDEX.read_text(encoding="utf-8"))

    assert payload["active_wave_id"] == "wave-2026-04-17-semantic-governance-reframe"
    waves = {item["wave_id"]: item for item in payload["waves"]}

    successor = waves["wave-2026-04-17-semantic-governance-reframe"]
    assert successor["status"] == "active"
    assert successor["closed_at"] is None
    assert successor["wave_ordinal"] == 4

    assert waves["wave-2026-04-17-first-wave-pilot"]["status"] == "closed"
    assert waves["wave-2026-04-17-customer-status-semantic-pilot"]["status"] == "closed"


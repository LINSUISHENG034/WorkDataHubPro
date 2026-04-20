from __future__ import annotations

from pathlib import Path

import yaml


def load_waves_index(registry_root: Path) -> dict[str, object]:
    return yaml.safe_load(
        (registry_root / "waves" / "index.yaml").read_text(encoding="utf-8")
    )


def wave_lookup(registry_root: Path) -> tuple[str, dict[str, dict[str, object]]]:
    payload = load_waves_index(registry_root)
    return str(payload["active_wave_id"]), {
        str(item["wave_id"]): item for item in payload["waves"]
    }


def require_active_open_wave(registry_root: Path, wave_id: str) -> dict[str, object]:
    active_wave_id, waves = wave_lookup(registry_root)
    if wave_id != active_wave_id:
        raise ValueError(
            f"Operation requires an active open wave; got {wave_id}, active is {active_wave_id}"
        )
    wave = waves[wave_id]
    if wave["status"] != "active" or wave.get("closed_at"):
        raise ValueError(f"Operation requires an active open wave; got {wave_id}")
    return wave


def allow_audit_wave_read(registry_root: Path, wave_id: str) -> dict[str, object]:
    _, waves = wave_lookup(registry_root)
    return waves[wave_id]


def resolve_requested_or_active_open_wave(
    registry_root: Path,
    wave_id: str | None = None,
) -> tuple[str, dict[str, object]]:
    active_wave_id, waves = wave_lookup(registry_root)
    target_wave_id = wave_id or active_wave_id
    if target_wave_id not in waves:
        raise ValueError(f"Unknown wave_id: {target_wave_id}")
    return target_wave_id, require_active_open_wave(registry_root, target_wave_id)

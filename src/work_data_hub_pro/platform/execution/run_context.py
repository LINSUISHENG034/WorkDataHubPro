from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RunContext:
    run_id: str
    domain: str
    period: str
    config_release_id: str

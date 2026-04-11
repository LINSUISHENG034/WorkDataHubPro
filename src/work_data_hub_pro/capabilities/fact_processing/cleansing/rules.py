from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable


@dataclass(frozen=True)
class CleansingRule:
    rule_id: str
    version: str
    field_name: str
    transform: Callable[[Any], Any]


def strip_and_uppercase(value: Any) -> str:
    return str(value).strip().upper()


def normalize_plan_code(value: Any) -> str:
    return str(value).strip().upper()


def parse_decimal(value: Any) -> float:
    return float(str(value).replace(",", "").strip())

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable


@dataclass(frozen=True)
class CleansingRule:
    rule_id: str
    version: str
    field_name: str
    transform: Callable[[Any], Any]


EVENT_BUSINESS_TYPE_MAPPING = {
    "受托": "企年受托",
    "投资": "企年投资",
    "投管": "企年投资",
    "企年受托": "企年受托",
    "企年投资": "企年投资",
}

EVENT_PLAN_TYPE_MAPPING = {
    "集合": "集合计划",
    "单一": "单一计划",
    "集合计划": "集合计划",
    "单一计划": "单一计划",
}


def strip_and_uppercase(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip().upper()


def normalize_plan_code(value: Any) -> str:
    if value is None:
        return ""
    return strip_and_uppercase(value)


def parse_decimal(value: Any) -> float:
    if value is None or str(value).strip() == "":
        return 0.0
    return float(str(value).replace(",", "").strip())


def normalize_event_business_type(value: Any) -> str:
    normalized = str(value or "").strip()
    return EVENT_BUSINESS_TYPE_MAPPING.get(normalized, normalized)


def normalize_event_plan_type(value: Any) -> str:
    normalized = str(value or "").strip()
    return EVENT_PLAN_TYPE_MAPPING.get(normalized, normalized)


def normalize_period(value: Any) -> str:
    digits = "".join(character for character in str(value or "") if character.isdigit())
    if len(digits) >= 6:
        return f"{digits[:4]}-{digits[4:6]}"
    return str(value or "").strip()


def normalize_event_date(value: Any) -> str | None:
    digits = "".join(character for character in str(value or "") if character.isdigit())
    if not digits:
        return None
    if len(digits) == 6:
        return f"{digits[:4]}-{digits[4:6]}-01"
    return f"{digits[:4]}-{digits[4:6]}-{digits[6:8]}"

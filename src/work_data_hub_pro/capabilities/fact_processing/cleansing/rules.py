from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date, datetime
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
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.date().isoformat()
    if isinstance(value, date):
        return value.isoformat()

    text = str(value).strip()
    if text == "":
        return None

    date_with_time_match = re.match(
        r"^\s*(\d{4}\D\d{1,2}\D\d{1,2})[T\s]+\d{1,2}:\d{1,2}(?::\d{1,2})?\s*$",
        text,
    )
    if date_with_time_match:
        text = date_with_time_match.group(1)

    groups = re.findall(r"\d+", text)
    if len(groups) in {2, 3} and len(groups[0]) == 4:
        year = int(groups[0])
        month = int(groups[1])
        day = int(groups[2]) if len(groups) == 3 else 1
        try:
            return date(year, month, day).isoformat()
        except ValueError:
            return None

    digits = "".join(character for character in text if character.isdigit())
    if len(digits) == 8:
        year = int(digits[:4])
        month = int(digits[4:6])
        day = int(digits[6:8])
        try:
            return date(year, month, day).isoformat()
        except ValueError:
            return None
    if len(digits) == 6:
        year = int(digits[:4])
        month = int(digits[4:6])
        try:
            return date(year, month, 1).isoformat()
        except ValueError:
            return None
    return None

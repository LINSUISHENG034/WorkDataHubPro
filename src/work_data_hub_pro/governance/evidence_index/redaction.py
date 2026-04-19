from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REQUIRED_POLICY_KEYS = {
    "policy_id",
    "mask_token",
    "sensitive_trace_fields",
    "sensitive_payload_keys",
    "structured_payload_roots",
    "preserve_exact_fields",
}


JsonValue = dict[str, Any] | list[Any] | str | int | float | bool | None


def load_redaction_policy(policy_path: Path) -> dict[str, Any]:
    payload = json.loads(policy_path.read_text(encoding="utf-8"))
    missing = REQUIRED_POLICY_KEYS.difference(payload)
    if missing:
        missing_keys = ", ".join(sorted(missing))
        raise ValueError(f"missing_redaction_policy_keys:{missing_keys}")
    return payload


def redact_trace_events(events: list[dict[str, Any]], policy: dict[str, Any]) -> list[dict[str, Any]]:
    sensitive_fields = set(policy["sensitive_trace_fields"])
    mask_token = policy["mask_token"]
    redacted_events: list[dict[str, Any]] = []
    for event in events:
        redacted = dict(event)
        if redacted.get("field_name") in sensitive_fields:
            redacted["value_before"] = mask_token
            redacted["value_after"] = mask_token
        redacted_events.append(redacted)
    return redacted_events


def redact_mapping_payload(payload: JsonValue, policy: dict[str, Any]) -> JsonValue:
    preserve_exact_fields = set(policy["preserve_exact_fields"])
    sensitive_payload_keys = set(policy["sensitive_payload_keys"])
    structured_payload_roots = set(policy["structured_payload_roots"])
    mask_token = policy["mask_token"]

    def _redact(value: JsonValue, *, current_key: str | None = None) -> JsonValue:
        if current_key in preserve_exact_fields:
            return value
        if current_key in sensitive_payload_keys:
            return mask_token
        if isinstance(value, dict):
            return {
                key: _redact(
                    item,
                    current_key=key if key in structured_payload_roots else key,
                )
                for key, item in value.items()
            }
        if isinstance(value, list):
            return [_redact(item, current_key=current_key) for item in value]
        return value

    return _redact(payload)


def redact_compatibility_case(case_payload: dict[str, Any], policy: dict[str, Any]) -> dict[str, Any]:
    return dict(redact_mapping_payload(case_payload, policy))

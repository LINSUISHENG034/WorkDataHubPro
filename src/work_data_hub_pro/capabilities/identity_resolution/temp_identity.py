from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
import re
from functools import lru_cache
from pathlib import Path
from typing import Any

_POLICY_PATH = (
    Path(__file__).resolve().parents[4] / "config" / "releases" / "temp_identity_policy.json"
)
_FULLWIDTH_CHAR_START = ord("！")
_FULLWIDTH_CHAR_END = ord("～")
_FULLWIDTH_TO_HALFWIDTH_OFFSET = 0xFEE0
_DECORATIVE_CHARS = '「」『』"'
_STATUS_MARKERS = sorted(
    [
        "已转出",
        "待转出",
        "待转移",
        "终止",
        "转出",
        "转移",
        "保留",
        "暂停",
        "注销",
        "清算",
        "解散",
        "吊销",
        "撤销",
        "停业",
        "歇业",
        "关闭",
        "迁出",
        "迁入",
        "变更",
        "合并",
        "分立",
        "破产",
        "重整",
        "托管",
        "接管",
        "整顿",
        "清盘",
        "退出",
        "终结",
        "结束",
        "完结",
        "已作废",
        "作废",
        "存量",
        "原",
        "转移终止",
        "已终止",
        "保留账户",
        "已转移终止",
        "本部",
        "未使用",
        "集合",
        "企业年金计划",
    ],
    key=len,
    reverse=True,
)
_ENTERPRISE_TYPES = sorted(
    [
        "特殊普通合伙",
        "普通合伙",
        "有限合伙",
        "有限公司",
        "个人独资",
        "全民所有制",
        "集体所有制",
        "股份合作",
        "个体工商户",
    ],
    key=len,
    reverse=True,
)
_PROTECTED_NAMES = {"保留账户管理"}


@lru_cache(maxsize=1)
def load_temp_identity_policy() -> dict[str, Any]:
    payload = json.loads(_POLICY_PATH.read_text(encoding="utf-8"))
    required_keys = {
        "policy_release_id",
        "prefix",
        "salt_env_var",
        "placeholder_values",
    }
    payload_keys = set(payload)
    if payload_keys != required_keys:
        raise ValueError(
            "Temp identity policy must contain only "
            "policy_release_id, prefix, salt_env_var, and placeholder_values"
        )
    if not isinstance(payload["placeholder_values"], list) or not all(
        isinstance(value, str) for value in payload["placeholder_values"]
    ):
        raise ValueError("placeholder_values must be a list of strings")
    return payload


def temp_identity_prefix() -> str:
    prefix = str(load_temp_identity_policy()["prefix"]).strip().upper()
    if not prefix or not prefix.isalnum():
        raise ValueError("Temp identity prefix must be a non-empty alphanumeric value")
    return prefix


def normalize_identity_fallback_input(name: str | None) -> str | None:
    if name is None:
        return None

    candidate = str(name)
    stripped = candidate.strip()
    if not stripped:
        return None

    placeholder_values = {
        value.strip()
        for value in load_temp_identity_policy()["placeholder_values"]
        if isinstance(value, str)
    }
    if stripped in placeholder_values:
        return None

    protected_upper = stripped.upper()
    if protected_upper in _PROTECTED_NAMES:
        return protected_upper

    normalized = candidate.replace("\u3000", " ")
    normalized = re.sub(r"\s+", "", normalized)

    for char in _DECORATIVE_CHARS:
        normalized = normalized.replace(char, "")

    normalized = re.sub(r"^[（\(][^）\)]*[）\)]", "", normalized)
    normalized = re.sub(r"及下属子企业", "", normalized)
    normalized = re.sub(
        r"(?:\(团托\)|（团托）|-[A-Za-z][A-Za-z0-9]*|-\d+|-养老|-福利)$",
        "",
        normalized,
    )

    for marker in _STATUS_MARKERS:
        normalized = re.sub(
            rf"^[\(\（]?{re.escape(marker)}[\)\）]?[\-]?",
            "",
            normalized,
        )
        normalized = re.sub(
            rf"[—\-\(\（]{re.escape(marker)}[\)\）]?$",
            "",
            normalized,
        )
        normalized = re.sub(
            rf"[\(\（]{re.escape(marker)}[\)\）]$",
            "",
            normalized,
        )

    normalized = _clean_trailing_parenthesis(normalized)
    normalized = "".join(_to_halfwidth(char) for char in normalized)
    normalized = normalized.replace("(", "（").replace(")", "）")
    normalized = re.sub(r"[—\-\.。]+$", "", normalized)
    normalized = re.sub(r"（）$", "", normalized)
    normalized = re.sub(r"[—\-]+$", "", normalized)
    normalized = normalized.upper()

    return normalized or None


def generate_temp_identity(name: str, *, salt: str, prefix: str) -> str:
    normalized = normalize_identity_fallback_input(name)
    if normalized is None:
        raise ValueError("Cannot generate a temp identity from an empty placeholder value")

    digest = hmac.new(
        salt.encode("utf-8"),
        normalized.encode("utf-8"),
        hashlib.sha1,
    ).digest()
    encoded = base64.b32encode(digest[:10]).decode("ascii")
    return f"{prefix.upper()}{encoded}"


def is_temp_identity(company_id: str | None) -> bool:
    if company_id is None:
        return False
    prefix = temp_identity_prefix()
    return bool(re.fullmatch(rf"{re.escape(prefix)}[A-Z2-7]{{16}}", company_id))


def _load_temp_identity_salt() -> str:
    policy = load_temp_identity_policy()
    env_var = str(policy["salt_env_var"]).strip()
    salt = os.getenv(env_var)
    if not salt:
        raise ValueError(
            f"Temp identity salt environment variable {env_var} is not configured"
        )
    return salt


def _clean_trailing_parenthesis(name: str) -> str:
    match = re.search(r"[（\(]([^）\)]+)[）\)]$", name)
    if not match:
        return name

    content = match.group(1)
    if any(enterprise_type in content for enterprise_type in _ENTERPRISE_TYPES):
        return name
    return name[: match.start()]


def _to_halfwidth(char: str) -> str:
    codepoint = ord(char)
    if _FULLWIDTH_CHAR_START <= codepoint <= _FULLWIDTH_CHAR_END:
        return chr(codepoint - _FULLWIDTH_TO_HALFWIDTH_OFFSET)
    return char


__all__ = [
    "generate_temp_identity",
    "is_temp_identity",
    "load_temp_identity_policy",
    "normalize_identity_fallback_input",
    "temp_identity_prefix",
]

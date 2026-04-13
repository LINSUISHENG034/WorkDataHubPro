from __future__ import annotations

import os

import pytest

from work_data_hub_pro.capabilities.identity_resolution.temp_identity import (
    generate_temp_identity,
    is_temp_identity,
    load_temp_identity_policy,
    normalize_identity_fallback_input,
    temp_identity_prefix,
)


@pytest.fixture(autouse=True)
def _temp_identity_salt(monkeypatch: pytest.MonkeyPatch) -> None:
    policy = load_temp_identity_policy()
    monkeypatch.setenv(str(policy["salt_env_var"]), "phase3-test-temp-identity-salt")


def test_generate_temp_identity_is_deterministic() -> None:
    policy = load_temp_identity_policy()
    salt = os.environ[str(policy["salt_env_var"])]

    first = generate_temp_identity(
        "Omega Holdings - 已转出",
        salt=salt,
        prefix=temp_identity_prefix(),
    )
    second = generate_temp_identity(
        "Omega Holdings - 已转出",
        salt=salt,
        prefix=temp_identity_prefix(),
    )

    assert first == second
    assert first.startswith("IN")
    assert len(first) == 18


def test_generate_temp_identity_is_opaque() -> None:
    policy = load_temp_identity_policy()
    salt = os.environ[str(policy["salt_env_var"])]
    raw_name = "Omega Holdings"

    generated = generate_temp_identity(
        raw_name,
        salt=salt,
        prefix=temp_identity_prefix(),
    )

    assert raw_name not in generated
    assert "OMEGA" not in generated
    assert is_temp_identity(generated) is True


def test_normalize_identity_fallback_input_applies_legacy_cleanup() -> None:
    assert normalize_identity_fallback_input(" 中国平安-已转出 ") == "中国平安"


@pytest.mark.parametrize("placeholder", [None, "", "   ", "0", "空白"])
def test_placeholder_name_returns_none(placeholder: str | None) -> None:
    assert normalize_identity_fallback_input(placeholder) is None

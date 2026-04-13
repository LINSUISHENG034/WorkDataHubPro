from __future__ import annotations

import pytest

from work_data_hub_pro.capabilities.identity_resolution.temp_identity import (
    load_temp_identity_policy,
)


@pytest.fixture(autouse=True)
def _temp_identity_salt(monkeypatch: pytest.MonkeyPatch) -> None:
    policy = load_temp_identity_policy()
    monkeypatch.setenv(str(policy["salt_env_var"]), "phase3-test-temp-identity-salt")

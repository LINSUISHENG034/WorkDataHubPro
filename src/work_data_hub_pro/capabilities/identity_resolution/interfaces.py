from __future__ import annotations

from typing import Protocol


class IdentityProvider(Protocol):
    def lookup(self, company_name: str) -> str | None:
        ...


class IdentityCache(Protocol):
    def get(self, company_name: str) -> str | None:
        ...

    def set(self, company_name: str, company_id: str) -> None:
        ...

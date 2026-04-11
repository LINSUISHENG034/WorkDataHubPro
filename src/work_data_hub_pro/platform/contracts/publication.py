from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class PublicationMode(str, Enum):
    REFRESH = "REFRESH"
    UPSERT = "UPSERT"
    APPEND_ONLY = "APPEND_ONLY"


@dataclass(frozen=True)
class PublicationTarget:
    target_name: str
    target_kind: str
    storage_adapter: str
    write_contract: str
    transaction_scope: str


@dataclass(frozen=True)
class PublicationPlan:
    publication_id: str
    target_name: str
    target_kind: str
    mode: PublicationMode
    refresh_keys: list[str]
    upsert_keys: list[str]
    source_batch_id: str
    source_run_id: str
    idempotency_scope: str
    transaction_group: str


@dataclass(frozen=True)
class PublicationResult:
    publication_id: str
    target_name: str
    mode: PublicationMode
    affected_rows: int
    transaction_group: str
    success: bool
    error_message: str | None = None

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from pydantic import BaseModel, ValidationError

from work_data_hub_pro.platform.contracts.publication import (
    PublicationMode,
    PublicationPlan,
    PublicationResult,
)
from work_data_hub_pro.platform.storage.in_memory_tables import InMemoryTableStore


class PublicationPolicyError(Exception):
    pass


class PolicyFileMissingError(PublicationPolicyError):
    pass


class PolicyParseError(PublicationPolicyError):
    pass


class UnknownDomainError(PublicationPolicyError):
    pass


class UnknownTargetError(PublicationPolicyError):
    pass


@dataclass(frozen=True)
class PublicationBundle:
    plan: PublicationPlan
    rows: list[dict[str, object]]


@dataclass(frozen=True)
class PublicationPolicyEntry:
    mode: PublicationMode
    transaction_group: str
    idempotency_scope: str


@dataclass(frozen=True)
class PublicationPolicy:
    domain: str
    targets: dict[str, PublicationPolicyEntry]


class PublicationPolicyEntryModel(BaseModel):
    mode: PublicationMode
    transaction_group: str
    idempotency_scope: str


class PublicationPolicyFileModel(BaseModel):
    root: dict[str, dict[str, PublicationPolicyEntryModel]]


def load_publication_policy(path: Path, *, domain: str) -> PublicationPolicy:
    if not path.exists():
        raise PolicyFileMissingError(f"Publication policy file not found: {path}")

    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        validated = PublicationPolicyFileModel.model_validate({"root": payload})
    except (OSError, json.JSONDecodeError, ValidationError) as exc:
        raise PolicyParseError(
            f"Publication policy file could not be parsed: {path}"
        ) from exc

    try:
        domain_targets = validated.root[domain]
    except KeyError as exc:
        raise UnknownDomainError(
            f"Publication policy domain is not configured: {domain}"
        ) from exc

    return PublicationPolicy(
        domain=domain,
        targets={
            target_name: PublicationPolicyEntry(
                mode=target_payload.mode,
                transaction_group=target_payload.transaction_group,
                idempotency_scope=target_payload.idempotency_scope,
            )
            for target_name, target_payload in domain_targets.items()
        },
    )


def build_publication_plan(
    *,
    policy: PublicationPolicy,
    publication_id: str,
    target_name: str,
    target_kind: str,
    refresh_keys: list[str],
    upsert_keys: list[str],
    source_batch_id: str,
    source_run_id: str,
) -> PublicationPlan:
    target_policy = policy.targets[target_name]
    return PublicationPlan(
        publication_id=publication_id,
        target_name=target_name,
        target_kind=target_kind,
        mode=target_policy.mode,
        refresh_keys=refresh_keys,
        upsert_keys=upsert_keys,
        source_batch_id=source_batch_id,
        source_run_id=source_run_id,
        idempotency_scope=target_policy.idempotency_scope,
        transaction_group=target_policy.transaction_group,
    )


class PublicationService:
    def __init__(self, storage: InMemoryTableStore) -> None:
        self._storage = storage

    def execute(self, bundles: list[PublicationBundle]) -> list[PublicationResult]:
        results: list[PublicationResult] = []
        for bundle in bundles:
            if bundle.plan.mode is PublicationMode.REFRESH:
                affected_rows = self._storage.refresh(bundle.plan.target_name, bundle.rows)
            elif bundle.plan.mode is PublicationMode.UPSERT:
                affected_rows = self._storage.upsert(
                    bundle.plan.target_name,
                    bundle.rows,
                    key_fields=bundle.plan.upsert_keys,
                )
            else:
                affected_rows = self._storage.append(bundle.plan.target_name, bundle.rows)

            results.append(
                PublicationResult(
                    publication_id=bundle.plan.publication_id,
                    target_name=bundle.plan.target_name,
                    mode=bundle.plan.mode,
                    affected_rows=affected_rows,
                    transaction_group=bundle.plan.transaction_group,
                    success=True,
                )
            )
        return results

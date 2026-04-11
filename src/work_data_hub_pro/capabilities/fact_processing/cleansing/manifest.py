from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from work_data_hub_pro.capabilities.fact_processing.cleansing.rules import (
    CleansingRule,
    normalize_plan_code,
    parse_decimal,
    strip_and_uppercase,
)


RULE_PACKS: dict[tuple[str, str], dict[str, CleansingRule]] = {
    ("annuity-performance-core", "2026.04.11"): {
        "company_name": CleansingRule(
            rule_id="uppercase-company-name",
            version="1",
            field_name="company_name",
            transform=strip_and_uppercase,
        ),
        "plan_code": CleansingRule(
            rule_id="normalize-plan-code",
            version="1",
            field_name="plan_code",
            transform=normalize_plan_code,
        ),
        "sales_amount": CleansingRule(
            rule_id="parse-sales-amount",
            version="1",
            field_name="sales_amount",
            transform=parse_decimal,
        ),
    }
}


@dataclass(frozen=True)
class ActiveRule:
    field_name: str
    rule: CleansingRule


@dataclass(frozen=True)
class CleansingManifest:
    release_id: str
    domain: str
    rule_pack_id: str
    rule_pack_version: str
    active_rules: list[ActiveRule]

    @classmethod
    def load(cls, *, release_path: Path, domain_path: Path) -> "CleansingManifest":
        release_payload = json.loads(release_path.read_text(encoding="utf-8"))
        domain_payload = json.loads(domain_path.read_text(encoding="utf-8"))
        expected_rule_pack_version = release_payload["rule_pack_versions"][
            domain_payload["domain"]
        ]
        if domain_payload["rule_pack_version"] != expected_rule_pack_version:
            raise ValueError("Domain config rule pack version does not match release")

        rule_pack = RULE_PACKS[
            (domain_payload["rule_pack_id"], domain_payload["rule_pack_version"])
        ]
        active_rules = [
            ActiveRule(field_name=field_name, rule=rule_pack[field_name])
            for field_name in domain_payload["activation_order"]
            if field_name in domain_payload["enabled_fields"]
        ]
        return cls(
            release_id=release_payload["release_id"],
            domain=domain_payload["domain"],
            rule_pack_id=domain_payload["rule_pack_id"],
            rule_pack_version=domain_payload["rule_pack_version"],
            active_rules=active_rules,
        )

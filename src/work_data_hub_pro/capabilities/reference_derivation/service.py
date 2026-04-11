from __future__ import annotations

from work_data_hub_pro.platform.contracts.models import (
    CanonicalFactRecord,
    DerivationCandidate,
)


class ReferenceDerivationService:
    def derive(self, facts: list[CanonicalFactRecord]) -> list[DerivationCandidate]:
        candidates: list[DerivationCandidate] = []
        for fact in facts:
            candidates.append(
                DerivationCandidate(
                    target_object="company_reference",
                    candidate_payload={
                        "company_id": fact.fields["company_id"],
                        "company_name": fact.fields["company_name"],
                        "period": fact.fields["period"],
                        "source_fact_id": fact.record_id,
                    },
                    source_record_ids=[fact.record_id],
                    derivation_rule_id="company-reference-from-annuity-performance",
                    derivation_rule_version="1",
                )
            )
        return candidates

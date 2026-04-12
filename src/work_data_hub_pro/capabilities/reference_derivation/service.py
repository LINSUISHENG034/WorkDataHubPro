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
                    derivation_rule_id=f"company-reference-from-{fact.domain.replace('_', '-')}",
                    derivation_rule_version="1",
                )
            )
            if fact.domain == "annual_award":
                period = str(fact.fields["period"])
                candidates.append(
                    DerivationCandidate(
                        target_object="customer_master_signal",
                        candidate_payload={
                            "company_id": fact.fields["company_id"],
                            "period": period,
                            "plan_code": fact.fields["plan_code"],
                            "customer_type": "WINNING_CUSTOMER",
                            "award_tag": f"{period[2:4]}{period[5:7]}-AWARD",
                            "source_fact_id": fact.record_id,
                        },
                        source_record_ids=[fact.record_id],
                        derivation_rule_id="customer-master-from-annual-award",
                        derivation_rule_version="1",
                    )
                )
            if fact.domain == "annual_loss":
                period = str(fact.fields["period"])
                candidates.append(
                    DerivationCandidate(
                        target_object="customer_loss_signal",
                        candidate_payload={
                            "company_id": fact.fields["company_id"],
                            "period": period,
                            "plan_code": fact.fields["plan_code"],
                            "customer_type": "LOSS_CUSTOMER",
                            "loss_tag": f"{period[2:4]}{period[5:7]}-LOSS",
                            "source_fact_id": fact.record_id,
                        },
                        source_record_ids=[fact.record_id],
                        derivation_rule_id="customer-loss-from-annual-loss",
                        derivation_rule_version="1",
                    )
                )
        return candidates

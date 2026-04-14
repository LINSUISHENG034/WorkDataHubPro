from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from work_data_hub_pro.capabilities.fact_processing.cleansing.manifest import (
    CleansingManifest,
)
from work_data_hub_pro.capabilities.identity_resolution.service import ResolvedFact
from work_data_hub_pro.platform.contracts.models import (
    CanonicalFactRecord,
    FieldTraceEvent,
    InputRecord,
)


COMPANY_BRANCH_MAPPING = {
    "内蒙": "G31",
    "战略": "G37",
    "中国": "G37",
    "济南": "G21",
    "北京其他": "G37",
    "北分": "G37",
}


@dataclass(frozen=True)
class ProcessingResult:
    fact: CanonicalFactRecord
    trace_events: list[FieldTraceEvent]


@dataclass(frozen=True)
class ArtifactExportResult:
    unknown_names_csv: Path | None
    failed_records_csv: Path | None


class AnnuityIncomeProcessor:
    stage_id = "fact_processing"

    def __init__(self, manifest: CleansingManifest) -> None:
        self._manifest = manifest

    def process(self, record: InputRecord) -> ProcessingResult:
        original_company_name = record.raw_payload.get("客户名称")
        cleaned_fields = {
            "company_name": original_company_name,
            "account_name": record.raw_payload.get("年金账户名") or original_company_name,
            "plan_code": record.raw_payload.get("计划号")
            or record.raw_payload.get("计划代码"),
            "plan_type": record.raw_payload.get("计划类型"),
            "business_type": record.raw_payload.get("业务类型"),
            "period": record.raw_payload.get("月度"),
            "institution_name": record.raw_payload.get("机构名称")
            or record.raw_payload.get("机构"),
            "fixed_fee": record.raw_payload.get("固费"),
            "source_sheet": record.raw_payload.get("source_sheet"),
            "source_row_no": record.raw_payload.get("source_row_no"),
        }
        trace_events: list[FieldTraceEvent] = []

        for event_seq, active_rule in enumerate(self._manifest.active_rules, start=1):
            before = cleaned_fields.get(active_rule.field_name)
            error_message: str | None = None
            success = True

            if active_rule.field_name not in cleaned_fields:
                after = None
                success = False
                error_message = f"missing field: {active_rule.field_name}"
            else:
                after = active_rule.rule.transform(before)
                cleaned_fields[active_rule.field_name] = after

            trace_events.append(
                FieldTraceEvent(
                    trace_id=f"trace:{record.record_id}",
                    event_id=f"{record.record_id}:{event_seq}",
                    event_seq=event_seq,
                    run_id=record.run_id,
                    batch_id=record.batch_id,
                    record_id=record.record_id,
                    anchor_row_no=record.anchor_row_no,
                    stage_id=self.stage_id,
                    field_name=active_rule.field_name,
                    value_before=before,
                    value_after=after,
                    rule_id=active_rule.rule.rule_id,
                    rule_version=f"{self._manifest.rule_pack_version}.{active_rule.rule.version}",
                    config_release_id=self._manifest.release_id,
                    action_type="cleanse",
                    timestamp=datetime.now(UTC).isoformat(),
                    success=success,
                    error_message=error_message,
                )
            )

        cleaned_fields["institution_code"] = self._resolve_institution_code(
            institution_name=cleaned_fields.get("institution_name"),
            source_institution=record.raw_payload.get("机构"),
        )

        fact = CanonicalFactRecord(
            run_id=record.run_id,
            record_id=f"fact:{record.record_id}",
            batch_id=record.batch_id,
            domain="annuity_income",
            fact_type="annuity_income",
            fields=cleaned_fields,
            lineage_ref=record.record_id,
            trace_ref=f"trace:{record.record_id}",
        )
        return ProcessingResult(fact=fact, trace_events=trace_events)

    @staticmethod
    def _resolve_institution_code(
        *,
        institution_name: object,
        source_institution: object,
    ) -> str:
        mapped_code = COMPANY_BRANCH_MAPPING.get(str(institution_name or "").strip(), "")
        if mapped_code:
            return mapped_code

        fallback_code = str(source_institution or "").strip()
        if fallback_code.lower() == "null" or fallback_code == "":
            return "G00"
        return fallback_code


class AnnuityIncomeArtifactExporter:
    def __init__(self, output_dir: Path) -> None:
        self._output_dir = Path(output_dir)
        self._output_dir.mkdir(parents=True, exist_ok=True)

    def export_for_resolution(
        self,
        resolved: ResolvedFact,
        *,
        export_unknown_names: bool,
    ) -> ArtifactExportResult:
        unknown_names_csv: Path | None = None
        failed_records_csv: Path | None = None

        if export_unknown_names and resolved.result.resolution_method == "temp_id_fallback":
            unknown_names_csv = self._output_dir / "unknown_names_csv.csv"
            self._write_csv(
                unknown_names_csv,
                fieldnames=[
                    "record_id",
                    "company_name",
                    "account_name",
                    "company_id",
                    "resolution_method",
                ],
                rows=[
                    {
                        "record_id": resolved.fact.record_id,
                        "company_name": resolved.fact.fields.get("company_name"),
                        "account_name": resolved.fact.fields.get("account_name"),
                        "company_id": resolved.fact.fields.get("company_id"),
                        "resolution_method": resolved.result.resolution_method,
                    }
                ],
            )

        if resolved.result.resolved_identity is None:
            failed_records_csv = self._output_dir / "failed_records.csv"
            self._write_csv(
                failed_records_csv,
                fieldnames=[
                    "record_id",
                    "company_name",
                    "account_name",
                    "reason",
                ],
                rows=[
                    {
                        "record_id": resolved.fact.record_id,
                        "company_name": resolved.fact.fields.get("company_name"),
                        "account_name": resolved.fact.fields.get("account_name"),
                        "reason": "unresolved_identity",
                    }
                ],
            )

        return ArtifactExportResult(
            unknown_names_csv=unknown_names_csv,
            failed_records_csv=failed_records_csv,
        )

    @staticmethod
    def _write_csv(
        path: Path,
        *,
        fieldnames: list[str],
        rows: list[dict[str, object]],
    ) -> None:
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

# Annual Award Validation Slice Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the second executable `WorkDataHubPro` validation slice so `annual_award` runs end to end through merge-aware multi-sheet intake, governed award fact processing, source-aware identity resolution, conditional plan-code enrichment, explicit publication, downstream status projection consumption, replay, and compatibility adjudication.

**Architecture:** Extend the accepted `annuity_performance` runtime instead of building a parallel stack. Keep multi-sheet behavior isolated to `capabilities/source_intake/annual_award`, keep annual-award-specific normalization and plan-code enrichment inside `capabilities/fact_processing/annual_award`, and reuse the existing publication, tracing, lineage, replay, and adjudication runtime. Use replay fixtures for `annuity_performance`, `annual_loss`, and customer-plan history so the `annual_award` slice can validate downstream status behavior without pulling Phase D breadth work or Phase E production-runtime work into Phase C.

**Tech Stack:** Python 3.12+, `uv`, `pytest`, `openpyxl`, `typer`, standard-library `dataclasses`, `enum`, `json`, `pathlib`

---

## Scope Check

This plan covers:

- a merge-aware multi-sheet intake contract for `annual_award`
- governed annual-award normalization and canonical fact processing
- source-company-id preservation and fallback identity evidence
- conditional `plan_code` enrichment from replayed customer-plan history
- explicit annual-award fact publication plus customer-master signal derivation
- downstream projection consumption of published `annual_award` facts
- replay orchestration, runbook, explainability evidence, and compatibility adjudication
- governance-document updates required to close Phase C

This plan does not cover:

- the `annual_loss` executable slice
- `annuity_income` breadth work
- live external provider integration beyond the existing provider interface
- production storage/publication runtime or deferred transaction groups
- Dagster or broader operator-tooling rollout

The deliberate consequence is that this slice keeps `annuity_performance` as a replay fixture dependency for downstream status projection. That lets Phase C close the multi-sheet archetype with explicit evidence before Phase D expands remaining breadth and before Phase E replaces validation-only runtime choices.

## Suggested Branch

- `slice/annual-award-closure`

## File Structure

Create or modify these files in this order so the multi-sheet slice closes with one explicit chain:

- `src/work_data_hub_pro/capabilities/source_intake/annual_award/service.py`: merge-aware workbook intake with stable merged anchors and preserved sheet provenance
- `tests/integration/test_annual_award_intake.py`: multi-sheet intake contract test
- `src/work_data_hub_pro/capabilities/fact_processing/cleansing/rules.py`: `None`-safe shared cleansing transforms reused by `annual_award`
- `src/work_data_hub_pro/capabilities/fact_processing/cleansing/manifest.py`: `annual_award` rule-pack registration
- `config/domains/annual_award/cleansing.json`: `annual_award` enablement and activation order
- `config/releases/2026-04-11-annual-award-baseline.json`: release binding for the second slice
- `src/work_data_hub_pro/capabilities/fact_processing/annual_award/service.py`: canonical award-event processing
- `tests/integration/test_annual_award_processing.py`: annual-award processing contract
- `src/work_data_hub_pro/capabilities/identity_resolution/service.py`: source-aware identity preservation
- `tests/integration/test_identity_resolution.py`: regression plus source-value preservation coverage
- `src/work_data_hub_pro/capabilities/fact_processing/annual_award/plan_code_lookup.py`: customer-plan lookup and fallback plan-code enrichment
- `tests/integration/test_annual_award_plan_code_enrichment.py`: enrichment tests
- `src/work_data_hub_pro/capabilities/reference_derivation/service.py`: annual-award customer-master signal derivation
- `config/policies/publication.json`: `annual_award` publication targets
- `tests/integration/test_reference_derivation.py`: annual-award derivation coverage
- `tests/integration/test_publication_service.py`: annual-award publication policy coverage
- `src/work_data_hub_pro/capabilities/projections/contract_state.py`: published annual-award fact consumption with compatibility bridge
- `tests/integration/test_projection_outputs.py`: cross-domain projection regression
- `src/work_data_hub_pro/apps/orchestration/replay/annual_award_slice.py`: explicit second-slice runner
- `src/work_data_hub_pro/apps/etl_cli/main.py`: CLI entrypoint for `annual_award` replay
- `tests/replay/test_annual_award_slice.py`: end-to-end replay path and diff-path adjudication
- `reference/historical_replays/annual_award/annuity_performance_fixture_2026_03.json`: read-only dependency fixture
- `reference/historical_replays/annual_award/annual_loss_fixture_2026_03.json`: read-only dependency fixture
- `reference/historical_replays/annual_award/customer_plan_history_2026_03.json`: replayed customer-plan lookup history
- `reference/historical_replays/annual_award/legacy_monthly_snapshot_2026_03.json`: locked baseline for adjudication
- `docs/runbooks/annual-award-replay.md`: operator replay instructions
- `tests/contracts/test_annual_award_replay_assets.py`: replay asset contract
- `tests/replay/test_annual_award_explainability_slo.py`: slice-level explainability retrieval acceptance test
- `docs/superpowers/specs/2026-04-11-workdatahubpro-first-wave-legacy-coverage-matrix.md`: Phase C coverage updates
- `docs/superpowers/specs/2026-04-11-workdatahubpro-refactor-program.md`: Phase C program-position updates
- `tests/contracts/test_annual_award_governance_docs.py`: governance-doc closure checks

### Task 1: Implement Merge-Aware `annual_award` Intake

**Files:**
- Create: `src/work_data_hub_pro/capabilities/source_intake/annual_award/service.py`
- Test: `tests/integration/test_annual_award_intake.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/integration/test_annual_award_intake.py
from openpyxl import Workbook

from work_data_hub_pro.capabilities.source_intake.annual_award.service import (
    AnnualAwardIntakeService,
)


def test_annual_award_intake_merges_sheet_rows_into_stable_anchor_sequence(
    tmp_path,
) -> None:
    workbook_path = tmp_path / "annual_award_2026_03.xlsx"
    workbook = Workbook()
    trustee = workbook.active
    trustee.title = "TrusteeAwards"
    trustee.append(
        [
            "company_name",
            "source_company_id",
            "plan_code",
            "plan_type",
            "product_line_code",
            "period",
            "award_amount",
        ]
    )
    trustee.append(["Acme", "company-001", "", "collective", "pl-ret", "2026-03", "5000"])
    investee = workbook.create_sheet("InvesteeAwards")
    investee.append(
        [
            "company_name",
            "source_company_id",
            "plan_code",
            "plan_type",
            "product_line_code",
            "period",
            "award_amount",
        ]
    )
    investee.append(["Beta", "", "", "single", "pl-alt", "2026-03", "1000"])
    workbook.save(workbook_path)

    result = AnnualAwardIntakeService().read_batch(
        run_id="run-001",
        period="2026-03",
        source_files=[workbook_path],
    )

    assert result.batch.batch_id == "annual_award:2026-03"
    assert result.batch.row_count == 2
    assert [record.anchor_row_no for record in result.records] == [2, 3]
    assert [record.origin_row_nos for record in result.records] == [[2], [2]]
    assert [record.raw_payload["source_sheet"] for record in result.records] == [
        "TrusteeAwards",
        "InvesteeAwards",
    ]
    assert [record.raw_payload["source_row_no"] for record in result.records] == [2, 2]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/integration/test_annual_award_intake.py -v`
Expected: FAIL with `ModuleNotFoundError` for `work_data_hub_pro.capabilities.source_intake.annual_award.service`

- [ ] **Step 3: Write minimal implementation**

```python
# src/work_data_hub_pro/capabilities/source_intake/annual_award/service.py
from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from hashlib import sha256
from pathlib import Path

from openpyxl import load_workbook

from work_data_hub_pro.platform.contracts.models import (
    FieldTraceEvent,
    InputBatch,
    InputRecord,
)


@dataclass(frozen=True)
class IntakeResult:
    batch: InputBatch
    records: list[InputRecord]
    trace_events: list[FieldTraceEvent]


class AnnualAwardIntakeService:
    domain = "annual_award"
    sheet_names = ("TrusteeAwards", "InvesteeAwards")
    stage_id = "source_intake"

    def read_batch(
        self,
        *,
        run_id: str,
        period: str,
        source_files: list[Path],
    ) -> IntakeResult:
        snapshot_hash = sha256()
        records: list[InputRecord] = []
        trace_events: list[FieldTraceEvent] = []
        merged_anchor_row_no = 2

        for source_file in source_files:
            workbook = load_workbook(source_file, read_only=True, data_only=True)
            try:
                for sheet_name in self.sheet_names:
                    sheet = workbook[sheet_name]
                    headers = [
                        cell.value
                        for cell in next(sheet.iter_rows(min_row=1, max_row=1))
                    ]
                    for source_row_no, row in enumerate(
                        sheet.iter_rows(min_row=2, values_only=True),
                        start=2,
                    ):
                        payload = dict(zip(headers, row, strict=True)) | {
                            "source_sheet": sheet_name,
                            "source_row_no": source_row_no,
                        }
                        snapshot_hash.update(
                            repr(
                                (
                                    source_file.name,
                                    sheet_name,
                                    source_row_no,
                                    payload,
                                )
                            ).encode("utf-8")
                        )
                        record_id = (
                            f"{run_id}:{source_file.stem}:{sheet_name}:{source_row_no}"
                        )
                        record = InputRecord(
                            run_id=run_id,
                            record_id=record_id,
                            batch_id=f"{self.domain}:{period}",
                            anchor_row_no=merged_anchor_row_no,
                            origin_row_nos=[source_row_no],
                            parent_record_ids=[],
                            stage_row_no=merged_anchor_row_no,
                            raw_payload=payload,
                        )
                        records.append(record)
                        trace_events.append(
                            FieldTraceEvent(
                                trace_id=f"trace:{record_id}",
                                event_id=f"{record_id}:intake",
                                event_seq=0,
                                run_id=run_id,
                                batch_id=record.batch_id,
                                record_id=record.record_id,
                                anchor_row_no=record.anchor_row_no,
                                stage_id=self.stage_id,
                                field_name="raw_payload",
                                value_before=None,
                                value_after=payload,
                                rule_id="capture-input",
                                rule_version="1",
                                config_release_id="system:source-intake",
                                action_type="snapshot",
                                timestamp=datetime.now(UTC).isoformat(),
                                success=True,
                            )
                        )
                        merged_anchor_row_no += 1
            finally:
                workbook.close()

        batch = InputBatch(
            batch_id=f"{self.domain}:{period}",
            domain=self.domain,
            period=period,
            source_files=[str(path) for path in source_files],
            input_snapshot_id=snapshot_hash.hexdigest(),
            row_count=len(records),
        )
        return IntakeResult(batch=batch, records=records, trace_events=trace_events)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/integration/test_annual_award_intake.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/work_data_hub_pro/capabilities/source_intake/annual_award/service.py tests/integration/test_annual_award_intake.py
@'
feat(source-intake): add merge-aware annual_award intake

Introduce the multi-sheet intake service for `annual_award` so trustee and
investee rows enter one explicit input stream with stable merged anchors and
preserved source-sheet provenance.

Validation:
- uv run pytest tests/integration/test_annual_award_intake.py -v

Refs:
- Spec: docs/superpowers/specs/2026-04-11-workdatahubpro-rebuild-architecture-draft.md
- ADR: N/A
- Compat: N/A
'@ | git commit -F -
```

### Task 2: Implement Governed `annual_award` Fact Processing

**Files:**
- Modify: `src/work_data_hub_pro/capabilities/fact_processing/cleansing/rules.py`
- Modify: `src/work_data_hub_pro/capabilities/fact_processing/cleansing/manifest.py`
- Create: `config/domains/annual_award/cleansing.json`
- Create: `config/releases/2026-04-11-annual-award-baseline.json`
- Create: `src/work_data_hub_pro/capabilities/fact_processing/annual_award/service.py`
- Test: `tests/integration/test_annual_award_processing.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/integration/test_annual_award_processing.py
from pathlib import Path

from work_data_hub_pro.capabilities.fact_processing.annual_award.service import (
    AnnualAwardProcessor,
)
from work_data_hub_pro.capabilities.fact_processing.cleansing.manifest import (
    CleansingManifest,
)
from work_data_hub_pro.platform.contracts.models import InputRecord


def test_annual_award_processor_normalizes_fields_and_business_type() -> None:
    manifest = CleansingManifest.load(
        release_path=Path("config/releases/2026-04-11-annual-award-baseline.json"),
        domain_path=Path("config/domains/annual_award/cleansing.json"),
    )
    record = InputRecord(
        run_id="run-001",
        record_id="run-001:annual_award:2",
        batch_id="annual_award:2026-03",
        anchor_row_no=2,
        origin_row_nos=[2],
        parent_record_ids=[],
        stage_row_no=2,
        raw_payload={
            "company_name": " Acme ",
            "source_company_id": "company-001",
            "plan_code": None,
            "plan_type": " collective ",
            "product_line_code": " pl-ret ",
            "period": "2026-03",
            "award_amount": "5,000.25",
            "source_sheet": "TrusteeAwards",
            "source_row_no": 2,
        },
    )

    result = AnnualAwardProcessor(manifest).process(record)

    assert result.fact.domain == "annual_award"
    assert result.fact.fact_type == "annual_award"
    assert result.fact.fields["company_name"] == "ACME"
    assert result.fact.fields["plan_code"] == ""
    assert result.fact.fields["plan_type"] == "COLLECTIVE"
    assert result.fact.fields["product_line_code"] == "PL-RET"
    assert result.fact.fields["award_amount"] == 5000.25
    assert result.fact.fields["business_type"] == "trustee_award"
    assert len(result.trace_events) == 5
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/integration/test_annual_award_processing.py -v`
Expected: FAIL with `FileNotFoundError` for `config/releases/2026-04-11-annual-award-baseline.json` or `ModuleNotFoundError` for `annual_award.service`

- [ ] **Step 3: Write minimal implementation**

```python
# src/work_data_hub_pro/capabilities/fact_processing/cleansing/rules.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable


@dataclass(frozen=True)
class CleansingRule:
    rule_id: str
    version: str
    field_name: str
    transform: Callable[[Any], Any]


def strip_and_uppercase(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip().upper()


def normalize_plan_code(value: Any) -> str:
    if value is None:
        return ""
    return strip_and_uppercase(value)


def parse_decimal(value: Any) -> float:
    if value is None or str(value).strip() == "":
        return 0.0
    return float(str(value).replace(",", "").strip())
```

```python
# src/work_data_hub_pro/capabilities/fact_processing/cleansing/manifest.py
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
    },
    ("annual-award-core", "2026.04.11"): {
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
        "plan_type": CleansingRule(
            rule_id="normalize-plan-type",
            version="1",
            field_name="plan_type",
            transform=strip_and_uppercase,
        ),
        "product_line_code": CleansingRule(
            rule_id="normalize-product-line-code",
            version="1",
            field_name="product_line_code",
            transform=strip_and_uppercase,
        ),
        "award_amount": CleansingRule(
            rule_id="parse-award-amount",
            version="1",
            field_name="award_amount",
            transform=parse_decimal,
        ),
    },
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
```

```json
// config/domains/annual_award/cleansing.json
{
  "domain": "annual_award",
  "rule_pack_id": "annual-award-core",
  "rule_pack_version": "2026.04.11",
  "activation_order": [
    "company_name",
    "plan_code",
    "plan_type",
    "product_line_code",
    "award_amount"
  ],
  "enabled_fields": [
    "company_name",
    "plan_code",
    "plan_type",
    "product_line_code",
    "award_amount"
  ]
}
```

```json
// config/releases/2026-04-11-annual-award-baseline.json
{
  "release_id": "2026-04-11-annual-award-baseline",
  "rule_pack_versions": {
    "annual_award": "2026.04.11"
  },
  "domains": {
    "annual_award": "config/domains/annual_award/cleansing.json"
  }
}
```

```python
# src/work_data_hub_pro/capabilities/fact_processing/annual_award/service.py
from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime

from work_data_hub_pro.capabilities.fact_processing.cleansing.manifest import (
    CleansingManifest,
)
from work_data_hub_pro.platform.contracts.models import (
    CanonicalFactRecord,
    FieldTraceEvent,
    InputRecord,
)


@dataclass(frozen=True)
class ProcessingResult:
    fact: CanonicalFactRecord
    trace_events: list[FieldTraceEvent]


class AnnualAwardProcessor:
    stage_id = "fact_processing"

    def __init__(self, manifest: CleansingManifest) -> None:
        self._manifest = manifest

    def process(self, record: InputRecord) -> ProcessingResult:
        cleaned_fields = dict(record.raw_payload)
        trace_events: list[FieldTraceEvent] = []

        for event_seq, active_rule in enumerate(self._manifest.active_rules, start=1):
            before = cleaned_fields.get(active_rule.field_name)
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
                    success=True,
                )
            )

        cleaned_fields["business_type"] = (
            "trustee_award"
            if cleaned_fields["source_sheet"] == "TrusteeAwards"
            else "investee_award"
        )

        fact = CanonicalFactRecord(
            run_id=record.run_id,
            record_id=f"fact:{record.record_id}",
            batch_id=record.batch_id,
            domain="annual_award",
            fact_type="annual_award",
            fields=cleaned_fields,
            lineage_ref=record.record_id,
            trace_ref=f"trace:{record.record_id}",
        )
        return ProcessingResult(fact=fact, trace_events=trace_events)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/integration/test_annual_award_processing.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/work_data_hub_pro/capabilities/fact_processing/cleansing/rules.py src/work_data_hub_pro/capabilities/fact_processing/cleansing/manifest.py config/domains/annual_award/cleansing.json config/releases/2026-04-11-annual-award-baseline.json src/work_data_hub_pro/capabilities/fact_processing/annual_award/service.py tests/integration/test_annual_award_processing.py
@'
feat(fact-processing.annual-award): add annual_award processor

Add the governed rule-pack binding and canonical event processor for the
`annual_award` slice while keeping transformation semantics code-owned.

Validation:
- uv run pytest tests/integration/test_annual_award_processing.py -v

Refs:
- Spec: docs/superpowers/specs/2026-04-11-workdatahubpro-rebuild-architecture-draft.md
- ADR: N/A
- Compat: N/A
'@ | git commit -F -
```

### Task 3: Preserve Source `company_id` Before Cache/Provider Fallback

**Files:**
- Modify: `src/work_data_hub_pro/capabilities/identity_resolution/service.py`
- Modify: `tests/integration/test_identity_resolution.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/integration/test_identity_resolution.py
from work_data_hub_pro.capabilities.identity_resolution.service import (
    CacheFirstIdentityResolutionService,
    InMemoryIdentityCache,
    StaticIdentityProvider,
)
from work_data_hub_pro.platform.contracts.models import CanonicalFactRecord


def test_identity_resolution_preserves_source_company_id_before_cache_lookup() -> None:
    service = CacheFirstIdentityResolutionService(
        cache=InMemoryIdentityCache({"ACME": "company-cache-999"}),
        provider=StaticIdentityProvider({"ACME": "company-provider-999"}),
    )
    fact = CanonicalFactRecord(
        run_id="run-001",
        record_id="fact-001",
        batch_id="annual_award:2026-03",
        domain="annual_award",
        fact_type="annual_award",
        fields={
            "company_name": "ACME",
            "company_id": "company-source-001",
            "plan_code": "",
            "period": "2026-03",
        },
        lineage_ref="record-001",
        trace_ref="trace:record-001",
    )

    resolved = service.resolve(
        fact,
        anchor_row_no=2,
        config_release_id="2026-04-11-annual-award-baseline",
    )

    assert resolved.fact.fields["company_id"] == "company-source-001"
    assert resolved.result.resolution_method == "source_value"
    assert resolved.result.evidence_refs == ["identity:source_value:ACME"]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/integration/test_identity_resolution.py -v`
Expected: FAIL because the service resolves through cache/provider logic instead of preserving the source value

- [ ] **Step 3: Write minimal implementation**

```python
# src/work_data_hub_pro/capabilities/identity_resolution/service.py
from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime

from work_data_hub_pro.capabilities.identity_resolution.interfaces import (
    IdentityCache,
    IdentityProvider,
)
from work_data_hub_pro.platform.contracts.models import (
    CanonicalFactRecord,
    FieldTraceEvent,
    IdentityResolutionResult,
)


class InMemoryIdentityCache:
    def __init__(self, seed: dict[str, str] | None = None) -> None:
        self._values = dict(seed or {})

    def get(self, company_name: str) -> str | None:
        return self._values.get(company_name)

    def set(self, company_name: str, company_id: str) -> None:
        self._values[company_name] = company_id


class StaticIdentityProvider:
    def __init__(self, mapping: dict[str, str]) -> None:
        self._mapping = mapping

    def lookup(self, company_name: str) -> str | None:
        return self._mapping.get(company_name)


@dataclass(frozen=True)
class ResolvedFact:
    fact: CanonicalFactRecord
    result: IdentityResolutionResult
    trace_events: list[FieldTraceEvent]


class CacheFirstIdentityResolutionService:
    stage_id = "identity_resolution"

    def __init__(self, *, cache: IdentityCache, provider: IdentityProvider) -> None:
        self._cache = cache
        self._provider = provider

    def resolve(
        self,
        fact: CanonicalFactRecord,
        *,
        anchor_row_no: int,
        config_release_id: str,
    ) -> ResolvedFact:
        company_name = str(fact.fields["company_name"])
        source_company_id = str(
            fact.fields.get("company_id") or fact.fields.get("source_company_id") or ""
        )

        if source_company_id:
            company_id = source_company_id
            method = "source_value"
            fallback_level = "none"
        else:
            cached_id = self._cache.get(company_name)
            if cached_id is not None:
                company_id = cached_id
                method = "cache_hit"
                fallback_level = "none"
            else:
                provider_id = self._provider.lookup(company_name)
                if provider_id is not None:
                    company_id = provider_id
                    self._cache.set(company_name, provider_id)
                    method = "provider_lookup"
                    fallback_level = "none"
                else:
                    company_id = f"TEMP-{company_name}"
                    method = "temp_id_fallback"
                    fallback_level = "temporary"

        updated_fields = dict(fact.fields)
        updated_fields["company_id"] = company_id
        updated_fact = CanonicalFactRecord(
            run_id=fact.run_id,
            record_id=fact.record_id,
            batch_id=fact.batch_id,
            domain=fact.domain,
            fact_type=fact.fact_type,
            fields=updated_fields,
            lineage_ref=fact.lineage_ref,
            trace_ref=fact.trace_ref,
        )
        result = IdentityResolutionResult(
            record_id=fact.record_id,
            resolved_identity=company_id,
            resolution_method=method,
            fallback_level=fallback_level,
            evidence_refs=[f"identity:{method}:{company_name}"],
        )
        trace_event = FieldTraceEvent(
            trace_id=fact.trace_ref,
            event_id=f"{fact.record_id}:identity",
            event_seq=100,
            run_id=fact.run_id,
            batch_id=fact.batch_id,
            record_id=fact.record_id,
            anchor_row_no=anchor_row_no,
            stage_id=self.stage_id,
            field_name="company_id",
            value_before=fact.fields.get("company_id"),
            value_after=company_id,
            rule_id=method,
            rule_version="1",
            config_release_id=config_release_id,
            action_type="resolve_identity",
            timestamp=datetime.now(UTC).isoformat(),
            success=True,
        )
        return ResolvedFact(
            fact=updated_fact,
            result=result,
            trace_events=[trace_event],
        )
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/integration/test_identity_resolution.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/work_data_hub_pro/capabilities/identity_resolution/service.py tests/integration/test_identity_resolution.py
@'
feat(identity-resolution): preserve source company ids for annual_award

Teach the shared identity-resolution path to honor source-provided company IDs
before cache or provider fallback so the event slice remains explainable.

Validation:
- uv run pytest tests/integration/test_identity_resolution.py -v

Refs:
- Spec: docs/superpowers/specs/2026-04-11-workdatahubpro-rebuild-architecture-draft.md
- ADR: N/A
- Compat: N/A
'@ | git commit -F -
```

### Task 4: Add Conditional `plan_code` Enrichment From Customer-Plan History

**Files:**
- Create: `src/work_data_hub_pro/capabilities/fact_processing/annual_award/plan_code_lookup.py`
- Test: `tests/integration/test_annual_award_plan_code_enrichment.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/integration/test_annual_award_plan_code_enrichment.py
from work_data_hub_pro.capabilities.fact_processing.annual_award.plan_code_lookup import (
    AnnualAwardPlanCodeEnrichmentService,
    CustomerPlanHistoryLookup,
)
from work_data_hub_pro.platform.contracts.models import CanonicalFactRecord


def test_plan_code_enrichment_prefers_customer_history_for_collective_plans() -> None:
    lookup = CustomerPlanHistoryLookup(
        [
            {
                "company_id": "company-001",
                "product_line_code": "PL-RET",
                "plan_code": "P9001",
                "effective_period": "2025-12",
            },
            {
                "company_id": "company-001",
                "product_line_code": "PL-RET",
                "plan_code": "S9001",
                "effective_period": "2025-12",
            },
        ]
    )
    fact = CanonicalFactRecord(
        run_id="run-001",
        record_id="fact-001",
        batch_id="annual_award:2026-03",
        domain="annual_award",
        fact_type="annual_award",
        fields={
            "company_name": "ACME",
            "company_id": "company-001",
            "plan_code": "",
            "plan_type": "COLLECTIVE",
            "product_line_code": "PL-RET",
            "period": "2026-03",
        },
        lineage_ref="record-001",
        trace_ref="trace:record-001",
    )

    enriched = AnnualAwardPlanCodeEnrichmentService(lookup).enrich(
        fact,
        anchor_row_no=2,
        config_release_id="2026-04-11-annual-award-baseline",
    )

    assert enriched.fact.fields["plan_code"] == "P9001"
    assert enriched.trace_events[0].rule_id == "customer_plan_history_lookup"


def test_plan_code_enrichment_falls_back_to_domain_default_when_history_misses() -> None:
    fact = CanonicalFactRecord(
        run_id="run-001",
        record_id="fact-002",
        batch_id="annual_award:2026-03",
        domain="annual_award",
        fact_type="annual_award",
        fields={
            "company_name": "BETA",
            "company_id": "company-002",
            "plan_code": "",
            "plan_type": "SINGLE",
            "product_line_code": "PL-ALT",
            "period": "2026-03",
        },
        lineage_ref="record-002",
        trace_ref="trace:record-002",
    )

    enriched = AnnualAwardPlanCodeEnrichmentService(CustomerPlanHistoryLookup([])).enrich(
        fact,
        anchor_row_no=3,
        config_release_id="2026-04-11-annual-award-baseline",
    )

    assert enriched.fact.fields["plan_code"] == "AN002"
    assert enriched.trace_events[0].rule_id == "domain_default_plan_code"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/integration/test_annual_award_plan_code_enrichment.py -v`
Expected: FAIL with `ModuleNotFoundError` for `plan_code_lookup`

- [ ] **Step 3: Write minimal implementation**

```python
# src/work_data_hub_pro/capabilities/fact_processing/annual_award/plan_code_lookup.py
from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime

from work_data_hub_pro.platform.contracts.models import (
    CanonicalFactRecord,
    FieldTraceEvent,
)


@dataclass(frozen=True)
class EnrichedAwardFact:
    fact: CanonicalFactRecord
    trace_events: list[FieldTraceEvent]


class CustomerPlanHistoryLookup:
    def __init__(self, rows: list[dict[str, object]]) -> None:
        self._rows = rows

    def select_plan_code(
        self,
        *,
        company_id: str,
        product_line_code: str,
        plan_type: str,
    ) -> str | None:
        candidates = sorted(
            [
                row
                for row in self._rows
                if row["company_id"] == company_id
                and row["product_line_code"] == product_line_code
            ],
            key=lambda row: str(row["effective_period"]),
            reverse=True,
        )
        preferred_prefix = "P" if plan_type == "COLLECTIVE" else "S"
        for row in candidates:
            plan_code = str(row["plan_code"])
            if plan_code.startswith(preferred_prefix):
                return plan_code
        return str(candidates[0]["plan_code"]) if candidates else None


class AnnualAwardPlanCodeEnrichmentService:
    stage_id = "fact_processing.plan_code_enrichment"

    def __init__(self, lookup: CustomerPlanHistoryLookup) -> None:
        self._lookup = lookup

    def enrich(
        self,
        fact: CanonicalFactRecord,
        *,
        anchor_row_no: int,
        config_release_id: str,
    ) -> EnrichedAwardFact:
        before = str(fact.fields.get("plan_code") or "")

        if before:
            plan_code = before
            method = "preserve_source_plan_code"
        else:
            lookup_plan_code = self._lookup.select_plan_code(
                company_id=str(fact.fields["company_id"]),
                product_line_code=str(fact.fields["product_line_code"]),
                plan_type=str(fact.fields["plan_type"]),
            )
            if lookup_plan_code is not None:
                plan_code = lookup_plan_code
                method = "customer_plan_history_lookup"
            else:
                plan_code = (
                    "AN001" if str(fact.fields["plan_type"]) == "COLLECTIVE" else "AN002"
                )
                method = "domain_default_plan_code"

        updated_fields = dict(fact.fields)
        updated_fields["plan_code"] = plan_code
        updated_fact = CanonicalFactRecord(
            run_id=fact.run_id,
            record_id=fact.record_id,
            batch_id=fact.batch_id,
            domain=fact.domain,
            fact_type=fact.fact_type,
            fields=updated_fields,
            lineage_ref=fact.lineage_ref,
            trace_ref=fact.trace_ref,
        )
        trace_event = FieldTraceEvent(
            trace_id=fact.trace_ref,
            event_id=f"{fact.record_id}:plan-code",
            event_seq=150,
            run_id=fact.run_id,
            batch_id=fact.batch_id,
            record_id=fact.record_id,
            anchor_row_no=anchor_row_no,
            stage_id=self.stage_id,
            field_name="plan_code",
            value_before=before,
            value_after=plan_code,
            rule_id=method,
            rule_version="1",
            config_release_id=config_release_id,
            action_type="enrich_plan_code",
            timestamp=datetime.now(UTC).isoformat(),
            success=True,
        )
        return EnrichedAwardFact(fact=updated_fact, trace_events=[trace_event])
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/integration/test_annual_award_plan_code_enrichment.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/work_data_hub_pro/capabilities/fact_processing/annual_award/plan_code_lookup.py tests/integration/test_annual_award_plan_code_enrichment.py
@'
feat(fact-processing.annual-award): add plan-code enrichment service

Add the replay-backed customer-plan lookup and domain-default fallback path so
`annual_award` can close its conditional plan-code enrichment chain explicitly.

Validation:
- uv run pytest tests/integration/test_annual_award_plan_code_enrichment.py -v

Refs:
- Spec: docs/superpowers/specs/2026-04-11-workdatahubpro-rebuild-architecture-draft.md
- ADR: N/A
- Compat: N/A
'@ | git commit -F -
```

### Task 5: Publish Annual-Award Reference And Customer-Signal Outputs Explicitly

**Files:**
- Modify: `src/work_data_hub_pro/capabilities/reference_derivation/service.py`
- Modify: `config/policies/publication.json`
- Modify: `tests/integration/test_reference_derivation.py`
- Modify: `tests/integration/test_publication_service.py`

- [ ] **Step 1: Write the failing tests**

```python
# tests/integration/test_reference_derivation.py
from work_data_hub_pro.capabilities.reference_derivation.service import (
    ReferenceDerivationService,
)
from work_data_hub_pro.platform.contracts.models import CanonicalFactRecord


def test_reference_derivation_adds_customer_master_signal_for_annual_award() -> None:
    service = ReferenceDerivationService()
    fact = CanonicalFactRecord(
        run_id="run-001",
        record_id="fact-001",
        batch_id="annual_award:2026-03",
        domain="annual_award",
        fact_type="annual_award",
        fields={
            "company_name": "ACME",
            "company_id": "company-001",
            "plan_code": "P9001",
            "period": "2026-03",
        },
        lineage_ref="record-001",
        trace_ref="trace:record-001",
    )

    candidates = service.derive([fact])

    assert [candidate.target_object for candidate in candidates] == [
        "company_reference",
        "customer_master_signal",
    ]
    assert candidates[1].candidate_payload["customer_type"] == "WINNING_CUSTOMER"
    assert candidates[1].candidate_payload["award_tag"] == "2603-AWARD"
```

```python
# tests/integration/test_publication_service.py
from pathlib import Path

from work_data_hub_pro.platform.publication.service import (
    PublicationBundle,
    PublicationService,
    build_publication_plan,
    load_publication_policy,
)
from work_data_hub_pro.platform.storage.in_memory_tables import InMemoryTableStore


def test_publication_service_supports_annual_award_fact_and_signal_targets() -> None:
    storage = InMemoryTableStore()
    service = PublicationService(storage)
    policy = load_publication_policy(
        Path("config/policies/publication.json"),
        domain="annual_award",
    )

    results = service.execute(
        [
            PublicationBundle(
                plan=build_publication_plan(
                    policy=policy,
                    publication_id="publication-award-facts",
                    target_name="fact_annual_award",
                    target_kind="fact",
                    refresh_keys=["batch_id"],
                    upsert_keys=[],
                    source_batch_id="annual_award:2026-03",
                    source_run_id="run-001",
                ),
                rows=[
                    {
                        "record_id": "fact-001",
                        "batch_id": "annual_award:2026-03",
                        "company_id": "company-001",
                        "plan_code": "P9001",
                        "period": "2026-03",
                    }
                ],
            ),
            PublicationBundle(
                plan=build_publication_plan(
                    policy=policy,
                    publication_id="publication-customer-signal",
                    target_name="customer_master_signal",
                    target_kind="reference",
                    refresh_keys=[],
                    upsert_keys=["company_id", "period"],
                    source_batch_id="annual_award:2026-03",
                    source_run_id="run-001",
                ),
                rows=[
                    {
                        "company_id": "company-001",
                        "period": "2026-03",
                        "customer_type": "WINNING_CUSTOMER",
                    }
                ],
            ),
        ]
    )

    assert [result.target_name for result in results] == [
        "fact_annual_award",
        "customer_master_signal",
    ]
    assert storage.read("customer_master_signal")[0]["customer_type"] == "WINNING_CUSTOMER"
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/integration/test_reference_derivation.py tests/integration/test_publication_service.py -v`
Expected: FAIL because `ReferenceDerivationService` only emits `company_reference` and `publication.json` has no `annual_award` domain entries

- [ ] **Step 3: Write minimal implementation**

```python
# src/work_data_hub_pro/capabilities/reference_derivation/service.py
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
        return candidates
```

```json
// config/policies/publication.json
{
  "annuity_performance": {
    "fact_annuity_performance": {
      "mode": "REFRESH",
      "transaction_group": "fact-publication",
      "idempotency_scope": "batch"
    },
    "company_reference": {
      "mode": "UPSERT",
      "transaction_group": "reference-publication",
      "idempotency_scope": "company_id"
    },
    "contract_state": {
      "mode": "REFRESH",
      "transaction_group": "projection-publication",
      "idempotency_scope": "period"
    },
    "monthly_snapshot": {
      "mode": "APPEND_ONLY",
      "transaction_group": "projection-publication",
      "idempotency_scope": "run"
    }
  },
  "annual_award": {
    "fact_annual_award": {
      "mode": "REFRESH",
      "transaction_group": "fact-publication",
      "idempotency_scope": "batch"
    },
    "company_reference": {
      "mode": "UPSERT",
      "transaction_group": "reference-publication",
      "idempotency_scope": "company_id"
    },
    "customer_master_signal": {
      "mode": "UPSERT",
      "transaction_group": "reference-publication",
      "idempotency_scope": "company_id+period"
    },
    "contract_state": {
      "mode": "REFRESH",
      "transaction_group": "projection-publication",
      "idempotency_scope": "period"
    },
    "monthly_snapshot": {
      "mode": "APPEND_ONLY",
      "transaction_group": "projection-publication",
      "idempotency_scope": "run"
    }
  }
}
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run pytest tests/integration/test_reference_derivation.py tests/integration/test_publication_service.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/work_data_hub_pro/capabilities/reference_derivation/service.py config/policies/publication.json tests/integration/test_reference_derivation.py tests/integration/test_publication_service.py
@'
feat(reference-derivation): publish annual_award customer signals

Extend explicit derivation and publication policy so the multi-sheet slice
emits both company-reference updates and customer-master award signals.

Validation:
- uv run pytest tests/integration/test_reference_derivation.py tests/integration/test_publication_service.py -v

Refs:
- Spec: docs/superpowers/specs/2026-04-11-workdatahubpro-rebuild-architecture-draft.md
- ADR: N/A
- Compat: N/A
'@ | git commit -F -
```

### Task 6: Consume Published `annual_award` Facts In Downstream Projections

**Files:**
- Modify: `src/work_data_hub_pro/capabilities/projections/contract_state.py`
- Modify: `tests/integration/test_projection_outputs.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/integration/test_projection_outputs.py
from work_data_hub_pro.capabilities.projections.contract_state import (
    ContractStateProjection,
)
from work_data_hub_pro.capabilities.projections.monthly_snapshot import (
    MonthlySnapshotProjection,
)
from work_data_hub_pro.platform.storage.in_memory_tables import InMemoryTableStore


def test_projections_consume_published_annual_award_facts_with_compatibility_bridge() -> None:
    storage = InMemoryTableStore(
        seed={
            "fact_annuity_performance": [
                {
                    "record_id": "fact-perf-001",
                    "company_id": "company-001",
                    "plan_code": "P9001",
                    "period": "2026-03",
                }
            ],
            "fact_annual_award": [
                {
                    "record_id": "fact-award-001",
                    "company_id": "company-001",
                    "plan_code": "P9001",
                    "period": "2026-03",
                }
            ],
            "fixture_annual_loss": [
                {
                    "company_id": "company-001",
                    "plan_code": "PLAN-Z",
                    "period": "2026-03",
                    "loss_code": "LOSS-99",
                }
            ],
        }
    )
    contract_state = ContractStateProjection(storage)
    contract_rows = contract_state.run(
        publication_ids=["publication-fact-001"],
        period="2026-03",
    )
    storage.refresh("contract_state", contract_rows.rows)

    monthly_snapshot = MonthlySnapshotProjection(storage)
    snapshot_rows = monthly_snapshot.run(
        publication_ids=["publication-projection-001"],
        period="2026-03",
    )

    assert contract_rows.rows == [
        {
            "company_id": "company-001",
            "plan_code": "P9001",
            "period": "2026-03",
            "has_annuity_performance": True,
            "has_annual_award_fact": True,
            "has_annual_award_fixture": True,
            "has_annual_loss_fixture": False,
        }
    ]
    assert snapshot_rows.rows == [
        {
            "period": "2026-03",
            "contract_state_rows": 1,
            "award_fixture_rows": 1,
            "loss_fixture_rows": 0,
        }
    ]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/integration/test_projection_outputs.py -v`
Expected: FAIL because `ContractStateProjection` has no `has_annual_award_fact` field and only reads `fixture_annual_award`

- [ ] **Step 3: Write minimal implementation**

```python
# src/work_data_hub_pro/capabilities/projections/contract_state.py
from __future__ import annotations

from dataclasses import dataclass

from work_data_hub_pro.platform.contracts.models import ProjectionResult
from work_data_hub_pro.platform.storage.in_memory_tables import InMemoryTableStore


@dataclass(frozen=True)
class ProjectionRows:
    rows: list[dict[str, object]]
    result: ProjectionResult


class ContractStateProjection:
    def __init__(self, storage: InMemoryTableStore) -> None:
        self._storage = storage

    @staticmethod
    def _has_match(
        rows: list[dict[str, object]],
        *,
        company_id: str,
        plan_code: str,
        period: str,
    ) -> bool:
        return any(
            row["company_id"] == company_id
            and row["plan_code"] == plan_code
            and row["period"] == period
            for row in rows
        )

    def run(self, *, publication_ids: list[str], period: str) -> ProjectionRows:
        performance_rows = [
            row
            for row in self._storage.read("fact_annuity_performance")
            if row["period"] == period
        ]
        award_fact_rows = self._storage.read("fact_annual_award")
        award_fixture_rows = self._storage.read("fixture_annual_award")
        loss_rows = self._storage.read("fixture_annual_loss")

        rows: list[dict[str, object]] = []
        for row in performance_rows:
            company_id = row["company_id"]
            plan_code = row["plan_code"]
            has_award_fact = self._has_match(
                award_fact_rows,
                company_id=company_id,
                plan_code=plan_code,
                period=period,
            )
            has_award_fixture = has_award_fact or self._has_match(
                award_fixture_rows,
                company_id=company_id,
                plan_code=plan_code,
                period=period,
            )
            rows.append(
                {
                    "company_id": company_id,
                    "plan_code": plan_code,
                    "period": period,
                    "has_annuity_performance": True,
                    "has_annual_award_fact": has_award_fact,
                    "has_annual_award_fixture": has_award_fixture,
                    "has_annual_loss_fixture": self._has_match(
                        loss_rows,
                        company_id=company_id,
                        plan_code=plan_code,
                        period=period,
                    ),
                }
            )

        return ProjectionRows(
            rows=rows,
            result=ProjectionResult(
                projection_name="contract_state",
                source_publications=publication_ids,
                affected_rows=len(rows),
                success=True,
            ),
        )
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/integration/test_projection_outputs.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/work_data_hub_pro/capabilities/projections/contract_state.py tests/integration/test_projection_outputs.py
@'
feat(projections): consume annual_award facts in contract_state

Update the downstream projection path so published `annual_award` facts become
first-class status inputs while preserving the accepted snapshot key shape.

Validation:
- uv run pytest tests/integration/test_projection_outputs.py -v

Refs:
- Spec: docs/superpowers/specs/2026-04-11-workdatahubpro-rebuild-architecture-draft.md
- ADR: N/A
- Compat: reference/historical_replays/annuity_performance/legacy_monthly_snapshot_2026_03.json
'@ | git commit -F -
```

### Task 7: Add The End-To-End `annual_award` Replay Slice

**Files:**
- Create: `src/work_data_hub_pro/apps/orchestration/replay/annual_award_slice.py`
- Modify: `src/work_data_hub_pro/apps/etl_cli/main.py`
- Test: `tests/replay/test_annual_award_slice.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/replay/test_annual_award_slice.py
import json
from pathlib import Path

from openpyxl import Workbook

from work_data_hub_pro.apps.orchestration.replay.annual_award_slice import (
    run_annual_award_slice,
)


def _write_replay_assets(
    replay_root: Path,
    *,
    legacy_snapshot_rows: list[dict[str, object]],
) -> None:
    replay_root.mkdir(parents=True, exist_ok=True)
    (replay_root / "annuity_performance_fixture_2026_03.json").write_text(
        json.dumps(
            [
                {
                    "record_id": "perf-001",
                    "company_id": "company-001",
                    "plan_code": "P9001",
                    "period": "2026-03",
                    "source_record_id": "perf-001",
                }
            ],
            indent=2,
        ),
        encoding="utf-8",
    )
    (replay_root / "annual_loss_fixture_2026_03.json").write_text(
        json.dumps(
            [
                {
                    "company_id": "company-001",
                    "plan_code": "LOSS-99",
                    "period": "2026-03",
                    "loss_code": "LOSS-99",
                    "source_sheet": "LossRegister",
                    "source_record_id": "loss-001",
                }
            ],
            indent=2,
        ),
        encoding="utf-8",
    )
    (replay_root / "customer_plan_history_2026_03.json").write_text(
        json.dumps(
            [
                {
                    "company_id": "company-001",
                    "product_line_code": "PL-RET",
                    "plan_code": "P9001",
                    "effective_period": "2025-12",
                },
                {
                    "company_id": "company-002",
                    "product_line_code": "PL-ALT",
                    "plan_code": "S9009",
                    "effective_period": "2025-12",
                }
            ],
            indent=2,
        ),
        encoding="utf-8",
    )
    (replay_root / "legacy_monthly_snapshot_2026_03.json").write_text(
        json.dumps(legacy_snapshot_rows, indent=2),
        encoding="utf-8",
    )


def _write_workbook(workbook_path: Path) -> None:
    workbook = Workbook()
    trustee = workbook.active
    trustee.title = "TrusteeAwards"
    trustee.append(
        [
            "company_name",
            "source_company_id",
            "plan_code",
            "plan_type",
            "product_line_code",
            "period",
            "award_amount",
        ]
    )
    trustee.append(["Acme", "company-001", "", "collective", "pl-ret", "2026-03", "5000"])
    investee = workbook.create_sheet("InvesteeAwards")
    investee.append(
        [
            "company_name",
            "source_company_id",
            "plan_code",
            "plan_type",
            "product_line_code",
            "period",
            "award_amount",
        ]
    )
    investee.append(["Beta", "", "", "single", "pl-alt", "2026-03", "1000"])
    workbook.save(workbook_path)


def test_annual_award_slice_replay_closes_chain_and_matches_legacy_snapshot(
    tmp_path,
) -> None:
    workbook_path = tmp_path / "annual_award_2026_03.xlsx"
    _write_workbook(workbook_path)
    replay_root = tmp_path / "reference" / "historical_replays" / "annual_award"
    _write_replay_assets(
        replay_root,
        legacy_snapshot_rows=[
            {
                "period": "2026-03",
                "contract_state_rows": 1,
                "award_fixture_rows": 1,
                "loss_fixture_rows": 0,
            }
        ],
    )

    outcome = run_annual_award_slice(
        workbook=workbook_path,
        period="2026-03",
        replay_root=replay_root,
    )

    assert [result.target_name for result in outcome.publication_results] == [
        "fact_annual_award",
        "company_reference",
        "customer_master_signal",
        "contract_state",
        "monthly_snapshot",
    ]
    assert [result.projection_name for result in outcome.projection_results] == [
        "contract_state",
        "monthly_snapshot",
    ]
    assert outcome.compatibility_case is None
    row_events = outcome.trace_store.find(
        batch_id="annual_award:2026-03",
        anchor_row_no=3,
    )
    assert {event.stage_id for event in row_events} == {
        "source_intake",
        "fact_processing",
        "identity_resolution",
        "fact_processing.plan_code_enrichment",
    }
    assert [link.anchor_row_no for link in outcome.lineage_registry.all()] == [2, 3]


def test_annual_award_slice_replay_creates_compatibility_case_when_snapshot_differs(
    tmp_path,
) -> None:
    workbook_path = tmp_path / "annual_award_2026_03.xlsx"
    _write_workbook(workbook_path)
    replay_root = tmp_path / "reference" / "historical_replays" / "annual_award"
    _write_replay_assets(
        replay_root,
        legacy_snapshot_rows=[
            {
                "period": "2026-03",
                "contract_state_rows": 99,
                "award_fixture_rows": 99,
                "loss_fixture_rows": 99,
            }
        ],
    )

    outcome = run_annual_award_slice(
        workbook=workbook_path,
        period="2026-03",
        replay_root=replay_root,
    )

    assert outcome.compatibility_case is not None
    case_path = (
        replay_root
        / "evidence"
        / "compatibility_cases"
        / f"{outcome.compatibility_case.case_id}.json"
    )
    assert case_path.exists()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/replay/test_annual_award_slice.py -v`
Expected: FAIL with `ModuleNotFoundError` for `annual_award_slice`

- [ ] **Step 3: Write minimal implementation**

```python
# src/work_data_hub_pro/apps/orchestration/replay/annual_award_slice.py
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from uuid import uuid4

from work_data_hub_pro.capabilities.fact_processing.annual_award.plan_code_lookup import (
    AnnualAwardPlanCodeEnrichmentService,
    CustomerPlanHistoryLookup,
)
from work_data_hub_pro.capabilities.fact_processing.annual_award.service import (
    AnnualAwardProcessor,
)
from work_data_hub_pro.capabilities.fact_processing.cleansing.manifest import (
    CleansingManifest,
)
from work_data_hub_pro.capabilities.identity_resolution.service import (
    CacheFirstIdentityResolutionService,
    InMemoryIdentityCache,
    StaticIdentityProvider,
)
from work_data_hub_pro.capabilities.projections.contract_state import (
    ContractStateProjection,
)
from work_data_hub_pro.capabilities.projections.monthly_snapshot import (
    MonthlySnapshotProjection,
)
from work_data_hub_pro.capabilities.reference_derivation.service import (
    ReferenceDerivationService,
)
from work_data_hub_pro.capabilities.source_intake.annual_award.service import (
    AnnualAwardIntakeService,
)
from work_data_hub_pro.governance.adjudication.service import AdjudicationService
from work_data_hub_pro.governance.compatibility.models import CompatibilityCase
from work_data_hub_pro.governance.evidence_index.file_store import FileEvidenceIndex
from work_data_hub_pro.platform.contracts.models import ProjectionResult
from work_data_hub_pro.platform.contracts.publication import PublicationResult
from work_data_hub_pro.platform.lineage.models import LineageLink
from work_data_hub_pro.platform.lineage.registry import LineageRegistry
from work_data_hub_pro.platform.publication.service import (
    PublicationBundle,
    PublicationService,
    build_publication_plan,
    load_publication_policy,
)
from work_data_hub_pro.platform.storage.in_memory_tables import InMemoryTableStore
from work_data_hub_pro.platform.tracing.in_memory_trace_store import InMemoryTraceStore


@dataclass(frozen=True)
class SliceRunOutcome:
    publication_results: list[PublicationResult]
    projection_results: list[ProjectionResult]
    compatibility_case: CompatibilityCase | None
    trace_store: InMemoryTraceStore
    lineage_registry: LineageRegistry


def _load_rows(path: Path) -> list[dict[str, object]]:
    return json.loads(path.read_text(encoding="utf-8"))


def run_annual_award_slice(
    *,
    workbook: Path,
    period: str,
    replay_root: Path,
) -> SliceRunOutcome:
    run_id = f"run-{uuid4().hex[:8]}"
    trace_store = InMemoryTraceStore()
    lineage_registry = LineageRegistry()
    evidence_index = FileEvidenceIndex(replay_root / "evidence")
    intake = AnnualAwardIntakeService()
    intake_result = intake.read_batch(
        run_id=run_id,
        period=period,
        source_files=[workbook],
    )
    batch = intake_result.batch
    records = intake_result.records
    intake_events_by_record = {
        record.record_id: [
            event
            for event in intake_result.trace_events
            if event.record_id == record.record_id
        ]
        for record in records
    }
    manifest = CleansingManifest.load(
        release_path=Path("config/releases/2026-04-11-annual-award-baseline.json"),
        domain_path=Path("config/domains/annual_award/cleansing.json"),
    )
    processor = AnnualAwardProcessor(manifest)
    resolver = CacheFirstIdentityResolutionService(
        cache=InMemoryIdentityCache({"ACME": "company-001"}),
        provider=StaticIdentityProvider({"BETA": "company-002"}),
    )
    plan_code_enrichment = AnnualAwardPlanCodeEnrichmentService(
        CustomerPlanHistoryLookup(
            _load_rows(replay_root / "customer_plan_history_2026_03.json")
        )
    )
    derivation = ReferenceDerivationService()
    storage = InMemoryTableStore(
        seed={
            "fact_annuity_performance": _load_rows(
                replay_root / "annuity_performance_fixture_2026_03.json"
            ),
            "fixture_annual_loss": _load_rows(
                replay_root / "annual_loss_fixture_2026_03.json"
            ),
        }
    )
    publication = PublicationService(storage)
    publication_policy = load_publication_policy(
        Path("config/policies/publication.json"),
        domain="annual_award",
    )

    award_facts = []
    for record in records:
        processing_result = processor.process(record)
        resolved = resolver.resolve(
            processing_result.fact,
            anchor_row_no=record.anchor_row_no,
            config_release_id=manifest.release_id,
        )
        enriched = plan_code_enrichment.enrich(
            resolved.fact,
            anchor_row_no=record.anchor_row_no,
            config_release_id=manifest.release_id,
        )
        row_trace_events = (
            intake_events_by_record[record.record_id]
            + processing_result.trace_events
            + resolved.trace_events
            + enriched.trace_events
        )
        for event in row_trace_events:
            trace_store.record(event)
        evidence_index.index_trace_events(
            batch_id=batch.batch_id,
            anchor_row_no=record.anchor_row_no,
            events=row_trace_events,
        )
        lineage_registry.register(
            LineageLink(
                record_id=enriched.fact.record_id,
                parent_record_ids=[record.record_id],
                origin_row_nos=record.origin_row_nos,
                anchor_row_no=record.anchor_row_no,
            )
        )
        award_facts.append(enriched.fact)

    derivation_candidates = derivation.derive(award_facts)
    publication_results = publication.execute(
        [
            PublicationBundle(
                plan=build_publication_plan(
                    policy=publication_policy,
                    publication_id="publication-award-facts",
                    target_name="fact_annual_award",
                    target_kind="fact",
                    refresh_keys=["batch_id"],
                    upsert_keys=[],
                    source_batch_id=batch.batch_id,
                    source_run_id=run_id,
                ),
                rows=[
                    fact.fields | {"record_id": fact.record_id, "batch_id": fact.batch_id}
                    for fact in award_facts
                ],
            ),
            PublicationBundle(
                plan=build_publication_plan(
                    policy=publication_policy,
                    publication_id="publication-company-reference",
                    target_name="company_reference",
                    target_kind="reference",
                    refresh_keys=[],
                    upsert_keys=["company_id"],
                    source_batch_id=batch.batch_id,
                    source_run_id=run_id,
                ),
                rows=[
                    candidate.candidate_payload
                    for candidate in derivation_candidates
                    if candidate.target_object == "company_reference"
                ],
            ),
            PublicationBundle(
                plan=build_publication_plan(
                    policy=publication_policy,
                    publication_id="publication-customer-signal",
                    target_name="customer_master_signal",
                    target_kind="reference",
                    refresh_keys=[],
                    upsert_keys=["company_id", "period"],
                    source_batch_id=batch.batch_id,
                    source_run_id=run_id,
                ),
                rows=[
                    candidate.candidate_payload
                    for candidate in derivation_candidates
                    if candidate.target_object == "customer_master_signal"
                ],
            ),
        ]
    )

    contract_state = ContractStateProjection(storage).run(
        publication_ids=["publication-award-facts"],
        period=period,
    )
    contract_state_publication_results = publication.execute(
        [
            PublicationBundle(
                plan=build_publication_plan(
                    policy=publication_policy,
                    publication_id="publication-contract-state",
                    target_name="contract_state",
                    target_kind="projection",
                    refresh_keys=["period"],
                    upsert_keys=[],
                    source_batch_id=batch.batch_id,
                    source_run_id=run_id,
                ),
                rows=contract_state.rows,
            )
        ]
    )
    monthly_snapshot = MonthlySnapshotProjection(storage).run(
        publication_ids=["publication-contract-state"],
        period=period,
    )
    monthly_snapshot_publication_results = publication.execute(
        [
            PublicationBundle(
                plan=build_publication_plan(
                    policy=publication_policy,
                    publication_id="publication-monthly-snapshot",
                    target_name="monthly_snapshot",
                    target_kind="projection",
                    refresh_keys=[],
                    upsert_keys=[],
                    source_batch_id=batch.batch_id,
                    source_run_id=run_id,
                ),
                rows=monthly_snapshot.rows,
            )
        ]
    )

    expected_snapshot = _load_rows(replay_root / "legacy_monthly_snapshot_2026_03.json")
    compatibility_case = None
    if monthly_snapshot.rows != expected_snapshot:
        compatibility_case = AdjudicationService(evidence_index).create_case(
            sample_locator=str(replay_root / "legacy_monthly_snapshot_2026_03.json"),
            legacy_result={"rows": expected_snapshot},
            pro_result={"rows": monthly_snapshot.rows},
            rationale="Monthly snapshot replay differs from accepted legacy baseline",
            affected_rule_version="annual-award-core:1",
        )

    return SliceRunOutcome(
        publication_results=(
            publication_results
            + contract_state_publication_results
            + monthly_snapshot_publication_results
        ),
        projection_results=[contract_state.result, monthly_snapshot.result],
        compatibility_case=compatibility_case,
        trace_store=trace_store,
        lineage_registry=lineage_registry,
    )
```

```python
# src/work_data_hub_pro/apps/etl_cli/main.py
from __future__ import annotations

from pathlib import Path

import typer

from work_data_hub_pro.apps.orchestration.replay.annual_award_slice import (
    run_annual_award_slice,
)
from work_data_hub_pro.apps.orchestration.replay.annuity_performance_slice import (
    run_annuity_performance_slice,
)


app = typer.Typer(help="WorkDataHubPro replay utilities")


@app.command("replay-annuity-performance")
def replay_annuity_performance(
    workbook: Path,
    period: str,
    replay_root: Path = Path("reference/historical_replays/annuity_performance"),
) -> None:
    outcome = run_annuity_performance_slice(
        workbook=workbook,
        period=period,
        replay_root=replay_root,
    )
    typer.echo(f"publication_results={len(outcome.publication_results)}")
    typer.echo(f"projection_results={len(outcome.projection_results)}")
    typer.echo(f"compatibility_case={outcome.compatibility_case is not None}")


@app.command("replay-annual-award")
def replay_annual_award(
    workbook: Path,
    period: str,
    replay_root: Path = Path("reference/historical_replays/annual_award"),
) -> None:
    outcome = run_annual_award_slice(
        workbook=workbook,
        period=period,
        replay_root=replay_root,
    )
    typer.echo(f"publication_results={len(outcome.publication_results)}")
    typer.echo(f"projection_results={len(outcome.projection_results)}")
    typer.echo(f"compatibility_case={outcome.compatibility_case is not None}")


if __name__ == "__main__":
    app()
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/replay/test_annual_award_slice.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/work_data_hub_pro/apps/orchestration/replay/annual_award_slice.py src/work_data_hub_pro/apps/etl_cli/main.py tests/replay/test_annual_award_slice.py
@'
feat(apps.orchestration): add annual_award replay slice

Wire the second executable slice end to end so `annual_award` closes through
intake, processing, identity, plan-code enrichment, publication, projections,
and compatibility adjudication.

Validation:
- uv run pytest tests/replay/test_annual_award_slice.py -v

Refs:
- Spec: docs/superpowers/specs/2026-04-11-workdatahubpro-refactor-program.md
- ADR: N/A
- Compat: reference/historical_replays/annual_award/legacy_monthly_snapshot_2026_03.json
'@ | git commit -F -
```

### Task 8: Add Replay Assets, Runbook, And Explainability Validation

**Files:**
- Create: `reference/historical_replays/annual_award/annuity_performance_fixture_2026_03.json`
- Create: `reference/historical_replays/annual_award/annual_loss_fixture_2026_03.json`
- Create: `reference/historical_replays/annual_award/customer_plan_history_2026_03.json`
- Create: `reference/historical_replays/annual_award/legacy_monthly_snapshot_2026_03.json`
- Create: `docs/runbooks/annual-award-replay.md`
- Create: `tests/contracts/test_annual_award_replay_assets.py`
- Create: `tests/replay/test_annual_award_explainability_slo.py`

- [ ] **Step 1: Write the failing tests**

```python
# tests/contracts/test_annual_award_replay_assets.py
from pathlib import Path


def test_annual_award_replay_assets_and_runbook_exist() -> None:
    replay_root = Path("reference/historical_replays/annual_award")

    assert (replay_root / "annuity_performance_fixture_2026_03.json").exists()
    assert (replay_root / "annual_loss_fixture_2026_03.json").exists()
    assert (replay_root / "customer_plan_history_2026_03.json").exists()
    assert (replay_root / "legacy_monthly_snapshot_2026_03.json").exists()
    assert Path("docs/runbooks/annual-award-replay.md").exists()
```

```python
# tests/replay/test_annual_award_explainability_slo.py
import json
from pathlib import Path
from time import perf_counter

from openpyxl import Workbook

from work_data_hub_pro.apps.orchestration.replay.annual_award_slice import (
    run_annual_award_slice,
)


def _write_replay_assets(replay_root: Path) -> None:
    replay_root.mkdir(parents=True, exist_ok=True)
    (replay_root / "annuity_performance_fixture_2026_03.json").write_text(
        json.dumps(
            [
                {
                    "record_id": "perf-001",
                    "company_id": "company-001",
                    "plan_code": "P9001",
                    "period": "2026-03",
                    "source_record_id": "perf-001",
                }
            ],
            indent=2,
        ),
        encoding="utf-8",
    )
    (replay_root / "annual_loss_fixture_2026_03.json").write_text(
        json.dumps([], indent=2),
        encoding="utf-8",
    )
    (replay_root / "customer_plan_history_2026_03.json").write_text(
        json.dumps(
            [
                {
                    "company_id": "company-002",
                    "product_line_code": "PL-ALT",
                    "plan_code": "S9009",
                    "effective_period": "2025-12",
                }
            ],
            indent=2,
        ),
        encoding="utf-8",
    )
    (replay_root / "legacy_monthly_snapshot_2026_03.json").write_text(
        json.dumps(
            [
                {
                    "period": "2026-03",
                    "contract_state_rows": 1,
                    "award_fixture_rows": 0,
                    "loss_fixture_rows": 0,
                }
            ],
            indent=2,
        ),
        encoding="utf-8",
    )


def test_annual_award_replay_keeps_primary_evidence_retrieval_inside_five_minutes(
    tmp_path,
) -> None:
    workbook_path = tmp_path / "annual_award_2026_03.xlsx"
    workbook = Workbook()
    trustee = workbook.active
    trustee.title = "TrusteeAwards"
    trustee.append(
        [
            "company_name",
            "source_company_id",
            "plan_code",
            "plan_type",
            "product_line_code",
            "period",
            "award_amount",
        ]
    )
    investee = workbook.create_sheet("InvesteeAwards")
    investee.append(
        [
            "company_name",
            "source_company_id",
            "plan_code",
            "plan_type",
            "product_line_code",
            "period",
            "award_amount",
        ]
    )
    investee.append(["Beta", "", "", "single", "pl-alt", "2026-03", "1000"])
    workbook.save(workbook_path)

    replay_root = tmp_path / "reference" / "historical_replays" / "annual_award"
    _write_replay_assets(replay_root)

    started = perf_counter()
    run_annual_award_slice(
        workbook=workbook_path,
        period="2026-03",
        replay_root=replay_root,
    )
    evidence_path = replay_root / "evidence" / "trace" / "annual_award_2026-03__row_2.json"
    payload = json.loads(evidence_path.read_text(encoding="utf-8"))
    elapsed = perf_counter() - started

    assert evidence_path.exists()
    assert elapsed < 300
    assert any(
        item["stage_id"] == "source_intake"
        and item["value_after"]["source_sheet"] == "InvesteeAwards"
        for item in payload
    )
    assert any(
        item["stage_id"] == "fact_processing.plan_code_enrichment"
        and item["value_after"] == "S9009"
        for item in payload
    )
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/contracts/test_annual_award_replay_assets.py tests/replay/test_annual_award_explainability_slo.py -v`
Expected: FAIL because the replay assets and runbook are missing

- [ ] **Step 3: Write minimal implementation**

```json
// reference/historical_replays/annual_award/annuity_performance_fixture_2026_03.json
[
  {
    "record_id": "perf-001",
    "company_id": "company-001",
    "plan_code": "P9001",
    "period": "2026-03",
    "source_record_id": "perf-001"
  }
]
```

```json
// reference/historical_replays/annual_award/annual_loss_fixture_2026_03.json
[
  {
    "company_id": "company-001",
    "plan_code": "LOSS-99",
    "period": "2026-03",
    "loss_code": "LOSS-99",
    "source_sheet": "LossRegister",
    "source_record_id": "loss-001"
  }
]
```

```json
// reference/historical_replays/annual_award/customer_plan_history_2026_03.json
[
  {
    "company_id": "company-001",
    "product_line_code": "PL-RET",
    "plan_code": "P9001",
    "effective_period": "2025-12"
  },
  {
    "company_id": "company-002",
    "product_line_code": "PL-ALT",
    "plan_code": "S9009",
    "effective_period": "2025-12"
  }
]
```

```json
// reference/historical_replays/annual_award/legacy_monthly_snapshot_2026_03.json
[
  {
    "period": "2026-03",
    "contract_state_rows": 1,
    "award_fixture_rows": 1,
    "loss_fixture_rows": 0
  }
]
```

````markdown
# docs/runbooks/annual-award-replay.md
# Annual Award Replay Runbook

## Goal

Run the `annual_award` validation slice end to end and determine whether the
`monthly_snapshot` output matches the accepted replay baseline.

## Inputs

- workbook path containing `TrusteeAwards` and `InvesteeAwards`
- config release `2026-04-11-annual-award-baseline`
- replay root `reference/historical_replays/annual_award`

## Command

```bash
uv run python -m work_data_hub_pro.apps.etl_cli.main replay-annual-award data/annual_award_2026_03.xlsx 2026-03
```

## Expected Output

- `publication_results=5`
- `projection_results=2`
- `compatibility_case=False`

If `compatibility_case=True`, inspect
`reference/historical_replays/annual_award/evidence/compatibility_cases/`
before merging.
````

Asset rule for this task:

- derive these JSON artifacts from locked legacy replay extracts, not handwritten synthetic rows
- keep the projection join keys actually used by the current Phase C status path: `company_id`, `plan_code`, and `period`
- keep provenance fields such as `source_sheet` and `source_record_id` where the dependency artifact supports them
- treat the replay-level explainability test as the actual slice acceptance gate for evidence retrieval

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run pytest tests/contracts/test_annual_award_replay_assets.py tests/replay/test_annual_award_explainability_slo.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add reference/historical_replays/annual_award/annuity_performance_fixture_2026_03.json reference/historical_replays/annual_award/annual_loss_fixture_2026_03.json reference/historical_replays/annual_award/customer_plan_history_2026_03.json reference/historical_replays/annual_award/legacy_monthly_snapshot_2026_03.json docs/runbooks/annual-award-replay.md tests/contracts/test_annual_award_replay_assets.py tests/replay/test_annual_award_explainability_slo.py
@'
docs(docs.architecture): add annual_award replay assets and runbook

Check in the replay fixtures, locked baseline, and operator instructions that
the multi-sheet slice needs for replay and explainability validation.

Validation:
- uv run pytest tests/contracts/test_annual_award_replay_assets.py tests/replay/test_annual_award_explainability_slo.py -v

Refs:
- Spec: docs/superpowers/specs/2026-04-11-workdatahubpro-refactor-program.md
- ADR: N/A
- Compat: reference/historical_replays/annual_award/legacy_monthly_snapshot_2026_03.json
'@ | git commit -F -
```

### Task 9: Close Phase C Governance And Run Full Verification

**Files:**
- Modify: `docs/superpowers/specs/2026-04-11-workdatahubpro-first-wave-legacy-coverage-matrix.md`
- Modify: `docs/superpowers/specs/2026-04-11-workdatahubpro-refactor-program.md`
- Create: `tests/contracts/test_annual_award_governance_docs.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/contracts/test_annual_award_governance_docs.py
from pathlib import Path


def test_annual_award_governance_docs_mark_phase_c_closed() -> None:
    coverage_matrix = Path(
        "docs/superpowers/specs/2026-04-11-workdatahubpro-first-wave-legacy-coverage-matrix.md"
    ).read_text(encoding="utf-8")
    refactor_program = Path(
        "docs/superpowers/specs/2026-04-11-workdatahubpro-refactor-program.md"
    ).read_text(encoding="utf-8")

    assert "| `annual_award` | accepted multi-sheet slice |" in coverage_matrix
    assert "| AA-001 | multi-sheet workbook merge intake |" in coverage_matrix
    assert "| `accepted` |" in coverage_matrix
    assert "| 2 | `annual_award` | accepted multi-sheet slice |" in refactor_program
    assert "| 3 | `annual_loss` | next recommended slice |" in refactor_program
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/contracts/test_annual_award_governance_docs.py -v`
Expected: FAIL because the governance specs still describe `annual_award` as planned/next recommended

- [ ] **Step 3: Write minimal implementation**

````markdown
# docs/superpowers/specs/2026-04-11-workdatahubpro-first-wave-legacy-coverage-matrix.md
## 5. Coverage Summary

| Domain | Current Position | Highest-Risk Gap |
|------|-------------------|------------------|
| `annuity_performance` | first executable slice accepted | production runtime and operator follow-on work still deferred |
| `annual_award` | accepted multi-sheet slice | `annual_loss` and `annuity_income` remain unclosed first-wave breadth work |
| `annual_loss` | next recommended event-domain slice | no accepted executable slice yet |
| `annuity_income` | identified first-wave single-sheet domain | no accepted executable slice yet |

### 6.2 `annual_award`

| Row ID | Behavior / Asset | Category | Legacy Source | Rebuild Target | Target Boundary | Owning Spec / Plan | Status | Validation Evidence | Retirement Decision | Notes / Risks |
|------|-------------------|----------|---------------|----------------|-----------------|--------------------|--------|---------------------|--------------------|---------------|
| AA-001 | multi-sheet workbook merge intake | capability | `docs/domains/annual_award-capability-map.md`, legacy migration workflow | `capabilities/source_intake/annual_award/service.py` | `capabilities` | architecture blueprint + annual award slice plan | `accepted` | `tests/integration/test_annual_award_intake.py`, `tests/replay/test_annual_award_slice.py` | N/A | merged anchors stay queryable by batch + anchor row |
| AA-002 | canonical award event transformation | capability | `docs/domains/annual_award-capability-map.md` | `capabilities/fact_processing/annual_award/` | `capabilities` | architecture blueprint + annual award slice plan | `accepted` | `tests/integration/test_annual_award_processing.py`, `tests/replay/test_annual_award_slice.py` | N/A | governed rule-pack binding is explicit |
| AA-003 | optional `company_id` resolution path for award rows | mechanism | annual award capability map, legacy enrichment behavior | shared `identity_resolution` contract plus award-specific wiring | `capabilities` | architecture blueprint + annual award slice plan | `accepted` | `tests/integration/test_identity_resolution.py`, replay evidence | N/A | source company id now wins before cache/provider fallback |
| AA-004 | conditional plan-code enrichment from customer contract history | mechanism | annual award capability map | `capabilities/fact_processing/annual_award/plan_code_lookup.py` | `capabilities` | annual award slice plan | `accepted` | `tests/integration/test_annual_award_plan_code_enrichment.py`, replay evidence | N/A | replay fixture keeps lookup behavior explicit before production storage exists |
| AA-005 | customer-master backfill signals from award events | mechanism | annual award capability map and legacy backfill behavior | explicit derivation/publication path | `capabilities` + `platform` | annual award slice plan | `accepted` | `tests/integration/test_reference_derivation.py`, `tests/integration/test_publication_service.py` | N/A | hidden side effects remain out of the hot path |
| AA-006 | award fact publication used by downstream status logic | projection | annual award capability map, downstream snapshot dependency | explicit publication and replay fixture coverage | `platform` + `reference` | annual award slice plan | `accepted` | `tests/integration/test_projection_outputs.py`, `tests/replay/test_annual_award_slice.py`, `tests/replay/test_annual_award_explainability_slo.py` | N/A | projection keeps compatibility field shape while reading published award facts |
````

````markdown
# docs/superpowers/specs/2026-04-11-workdatahubpro-refactor-program.md
## 3. Current Position

The program has completed:

- the first executable validation slice for `annuity_performance`
- the default Phase C multi-sheet slice for `annual_award`

What is already true:

- a capability-first package exists under `src/work_data_hub_pro/`
- explicit platform contracts, tracing, lineage, publication, and replay flow exist
- compatibility adjudication and evidence indexing exist for the first two accepted slices
- replay assets and runbooks exist for `annuity_performance` and `annual_award`
- one multi-sheet executable slice is now accepted with committed coverage updates

What is not yet true:

- `annual_loss` and `annuity_income` do not have accepted executable slices yet
- production storage/publication and operator tooling remain deferred
- first-wave legacy retirement decisions are not yet recorded

## 7. Domain Sequencing

| Order | Domain | Program Status | Rationale |
|------|--------|----------------|-----------|
| 1 | `annuity_performance` | accepted baseline slice | proves the corrected architecture in code |
| 2 | `annual_award` | accepted multi-sheet slice | closes the second intake archetype and downstream award-status dependency |
| 3 | `annual_loss` | next recommended slice | validates the paired event-domain dependency path |
| 4 | `annuity_income` | follow-on single-sheet breadth slice | extends first-wave coverage after archetype risks are reduced |
````

- [ ] **Step 4: Run verification**

Run:
- `uv run pytest tests/integration/test_annual_award_intake.py tests/integration/test_annual_award_processing.py tests/integration/test_annual_award_plan_code_enrichment.py tests/integration/test_identity_resolution.py tests/integration/test_reference_derivation.py tests/integration/test_publication_service.py tests/integration/test_projection_outputs.py tests/contracts/test_annual_award_replay_assets.py tests/contracts/test_annual_award_governance_docs.py tests/replay/test_annual_award_slice.py tests/replay/test_annual_award_explainability_slo.py tests/replay/test_annuity_performance_slice.py tests/replay/test_annuity_performance_explainability_slo.py -v`
- `uv run pytest -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add docs/superpowers/specs/2026-04-11-workdatahubpro-first-wave-legacy-coverage-matrix.md docs/superpowers/specs/2026-04-11-workdatahubpro-refactor-program.md tests/contracts/test_annual_award_governance_docs.py
@'
docs(docs.architecture): close annual_award slice governance loop

Update the first-wave governance assets so Phase C is explicitly recorded as
accepted and the next breadth work is unambiguous.

Validation:
- uv run pytest tests/contracts/test_annual_award_governance_docs.py -v
- uv run pytest -v

Refs:
- Spec: docs/superpowers/specs/2026-04-11-workdatahubpro-refactor-program.md
- ADR: N/A
- Compat: reference/historical_replays/annual_award/legacy_monthly_snapshot_2026_03.json
'@ | git commit -F -
```

## Self-Review

### Spec Coverage

- The architecture blueprint Section 3 invariants are respected by keeping award business semantics in `capabilities/`, publication semantics in `platform/`, and adjudication in `governance/`.
- The blueprint Sections 5 and 7 are covered by Tasks 1 through 8: the slice closes through merge-aware intake, fact processing, identity resolution, explicit publication, projections, runtime evidence, and adjudication.
- The refactor program Phase C goal and default-domain rule are implemented by Tasks 1 through 9 with `annual_award` as the explicit multi-sheet slice.
- Coverage-matrix rows `AA-001` through `AA-006` each map to one or more concrete tasks, tests, replay assets, and final governance updates.
- The plan deliberately keeps production runtime, deferred publication design, operator tooling, and live provider integration out of scope so Phase C stays aligned with the admitted program boundary.

### Placeholder Scan

- No `TBD`, `TODO`, `implement later`, `fill in details`, or `Similar to Task` placeholders remain.
- Every task contains exact file paths, concrete code, exact commands, and explicit expected outcomes.
- The replay assets and governance updates are named explicitly instead of being left as generic follow-up notes.

### Type Consistency

- Intake identifiers stay consistent across the plan: `batch_id="annual_award:2026-03"`, merged `anchor_row_no`, and preserved `origin_row_nos`.
- Annual-award target names stay consistent across publication, replay, and projection tasks: `fact_annual_award`, `company_reference`, `customer_master_signal`, `contract_state`, and `monthly_snapshot`.
- The release ID stays consistent across the plan: `2026-04-11-annual-award-baseline`.
- The plan-code enrichment stage name stays consistent across tests and implementation: `fact_processing.plan_code_enrichment`.
- The compatibility bridge stays consistent across projection and replay tasks: `has_annual_award_fact` is explicit, while `has_annual_award_fixture` remains the stable snapshot-facing compatibility field.

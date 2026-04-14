from pathlib import Path

import pytest

from work_data_hub_pro.capabilities.fact_processing.annuity_income.service import (
    AnnuityIncomeArtifactExporter,
    AnnuityIncomeProcessor,
)
from work_data_hub_pro.capabilities.fact_processing.cleansing.manifest import (
    CleansingManifest,
)
from work_data_hub_pro.capabilities.identity_resolution.service import (
    CacheFirstIdentityResolutionService,
    InMemoryIdentityCache,
    StaticIdentityProvider,
)
from work_data_hub_pro.capabilities.identity_resolution.temp_identity import (
    load_temp_identity_policy,
)
from work_data_hub_pro.platform.contracts.models import InputRecord


@pytest.fixture(autouse=True)
def _temp_identity_salt(monkeypatch: pytest.MonkeyPatch) -> None:
    policy = load_temp_identity_policy()
    monkeypatch.setenv(str(policy["salt_env_var"]), "annuity-income-test-salt")


def _manifest() -> CleansingManifest:
    return CleansingManifest.load(
        release_path=Path("config/releases/2026-04-14-annuity-income-baseline.json"),
        domain_path=Path("config/domains/annuity_income/cleansing.json"),
    )


def test_annuity_income_identity_resolution_does_not_restore_id5_fallback() -> None:
    record = InputRecord(
        run_id="run-001",
        record_id="run-001:annuity_income:3",
        batch_id="annuity_income:2026-03",
        anchor_row_no=3,
        origin_row_nos=[3],
        parent_record_ids=[],
        stage_row_no=3,
        raw_payload={
            "月度": "2026年03月",
            "业务类型": "职年受托",
            "计划类型": "单一计划",
            "客户名称": "未知客户",
            "年金账户名": "历史账户名",
            "机构名称": "北京其他",
            "计划号": "",
            "固费": None,
            "source_sheet": "收入明细",
            "source_row_no": 3,
        },
    )
    fact = AnnuityIncomeProcessor(_manifest()).process(record).fact
    resolved = CacheFirstIdentityResolutionService(
        cache=InMemoryIdentityCache({}),
        provider=StaticIdentityProvider({}),
    ).resolve(
        fact,
        anchor_row_no=record.anchor_row_no,
        config_release_id="2026-04-14-annuity-income-baseline",
    )

    assert resolved.result.resolution_method == "temp_id_fallback"
    assert resolved.fact.fields["company_id"].startswith("IN")


def test_annuity_income_exports_unknown_name_and_failed_record_artifacts_for_unresolved_identity(
    tmp_path,
) -> None:
    record = InputRecord(
        run_id="run-001",
        record_id="run-001:annuity_income:4",
        batch_id="annuity_income:2026-03",
        anchor_row_no=4,
        origin_row_nos=[4],
        parent_record_ids=[],
        stage_row_no=4,
        raw_payload={
            "月度": "2026年03月",
            "业务类型": "职年受托",
            "计划类型": "单一计划",
            "客户名称": "空白",
            "年金账户名": "历史账户名",
            "机构名称": "北京其他",
            "计划号": "",
            "固费": None,
            "source_sheet": "收入明细",
            "source_row_no": 4,
        },
    )
    fact = AnnuityIncomeProcessor(_manifest()).process(record).fact
    resolved = CacheFirstIdentityResolutionService(
        cache=InMemoryIdentityCache({}),
        provider=StaticIdentityProvider({}),
    ).resolve(
        fact,
        anchor_row_no=record.anchor_row_no,
        config_release_id="2026-04-14-annuity-income-baseline",
    )

    artifacts = AnnuityIncomeArtifactExporter(tmp_path).export_for_resolution(
        resolved,
        export_unknown_names=True,
    )

    assert artifacts.unknown_names_csv is not None
    assert artifacts.failed_records_csv is not None
    assert artifacts.unknown_names_csv.exists()
    assert artifacts.failed_records_csv.exists()

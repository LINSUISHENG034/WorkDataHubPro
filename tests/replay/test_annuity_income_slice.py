import json
from pathlib import Path

import pytest
from openpyxl import Workbook

from work_data_hub_pro.apps.orchestration.replay.annuity_income_slice import (
    run_annuity_income_slice,
)
from work_data_hub_pro.capabilities.identity_resolution.temp_identity import (
    generate_temp_identity,
    load_temp_identity_policy,
)


@pytest.fixture(autouse=True)
def _temp_identity_salt(monkeypatch: pytest.MonkeyPatch) -> None:
    policy = load_temp_identity_policy()
    monkeypatch.setenv(str(policy["salt_env_var"]), "annuity-income-replay-salt")


def _write_workbook(workbook_path: Path) -> None:
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "收入明细"
    sheet.append(["月度", "机构", "机构名称", "计划号", "客户名称", "业务类型", "计划类型", "固费"])
    sheet.append(["2026年03月", "", "北京其他", "", "未知客户", "职年受托", "单一计划", None])
    workbook.save(workbook_path)


def _write_replay_assets(replay_root: Path) -> None:
    replay_root.mkdir(parents=True, exist_ok=True)
    expected_company_id = generate_temp_identity(
        "未知客户",
        salt="annuity-income-replay-salt",
        prefix="IN",
    )
    (replay_root / "legacy_fact_processing_2026_03.json").write_text(
        json.dumps(
            [
                {
                    "record_id": "income-002",
                    "company_name": "未知客户",
                    "account_name": "未知客户",
                    "plan_code": "",
                    "plan_type": "单一计划",
                    "business_type": "职年受托",
                    "period": "2026-03",
                    "institution_name": "北京其他",
                    "fixed_fee": 0.0,
                    "source_sheet": "收入明细",
                    "source_row_no": 2,
                    "institution_code": "G37",
                    "company_id": expected_company_id,
                }
            ],
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    (replay_root / "legacy_identity_resolution_2026_03.json").write_text(
        json.dumps(
            [
                {
                    "record_id": "income-002",
                    "resolved_identity": expected_company_id,
                    "resolution_method": "temp_id_fallback",
                    "fallback_level": "temporary",
                    "evidence_refs": ["identity:temp_id_fallback:收入明细:2"],
                }
            ],
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    (replay_root / "legacy_reference_derivation_2026_03.json").write_text(
        json.dumps(
            [
                {
                    "target_object": "company_reference",
                    "candidate_payload": {
                        "company_id": expected_company_id,
                        "company_name": "未知客户",
                        "period": "2026-03",
                        "source_fact_id": "income-002",
                    },
                    "source_record_ids": ["income-002"],
                    "derivation_rule_id": "company-reference-from-annuity-income",
                    "derivation_rule_version": "1",
                },
                {
                    "target_object": "customer_master_signal",
                    "candidate_payload": {
                        "company_id": expected_company_id,
                        "period": "2026-03",
                        "plan_code": "",
                        "customer_type": "INCOME_CUSTOMER",
                        "income_tag": "2603-INCOME",
                        "source_fact_id": "income-002",
                    },
                    "source_record_ids": ["income-002"],
                    "derivation_rule_id": "customer-master-from-annuity-income",
                    "derivation_rule_version": "1",
                },
            ],
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    (replay_root / "legacy_operator_artifacts_2026_03.json").write_text(
        json.dumps(
            [
                {
                    "record_id": "income-002",
                    "unknown_names_csv": True,
                    "failed_records_csv": False,
                }
            ],
            indent=2,
        ),
        encoding="utf-8",
    )


def test_annuity_income_slice_replay_closes_chain_without_projection_hooks(tmp_path) -> None:
    workbook_path = tmp_path / "annuity_income_2026_03.xlsx"
    replay_root = tmp_path / "reference" / "historical_replays" / "annuity_income"
    _write_workbook(workbook_path)
    _write_replay_assets(replay_root)

    outcome = run_annuity_income_slice(
        workbook=workbook_path,
        period="2026-03",
        replay_root=replay_root,
    )

    assert [result.target_name for result in outcome.publication_results] == [
        "fact_annuity_income",
        "company_reference",
        "customer_master_signal",
    ]
    assert outcome.projection_results == []
    assert outcome.gate_summary.overall_outcome == "passed"
    assert outcome.run_report.primary_failure is None

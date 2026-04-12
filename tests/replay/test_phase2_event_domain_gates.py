from __future__ import annotations

import json
from pathlib import Path

from openpyxl import Workbook

from work_data_hub_pro.apps.orchestration.replay.annual_award_slice import (
    run_annual_award_slice,
)
from work_data_hub_pro.apps.orchestration.replay.annual_loss_slice import (
    run_annual_loss_slice,
)


def _write_award_assets(
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


def _write_loss_assets(
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
    (replay_root / "annual_award_fixture_2026_03.json").write_text(
        json.dumps(
            [
                {
                    "company_id": "company-001",
                    "plan_code": "P9001",
                    "period": "2026-03",
                    "award_code": "AWARD-01",
                    "source_sheet": "AwardRegister",
                    "source_record_id": "award-001",
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
                    "product_line_code": "PL202",
                    "plan_code": "P9001",
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


def _write_award_workbook(path: Path) -> None:
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
    workbook.save(path)


def _write_loss_workbook(path: Path) -> None:
    workbook = Workbook()
    trustee = workbook.active
    trustee.title = "企年受托流失(解约)"
    trustee.append(
        [
            "上报月份",
            "业务类型",
            "计划类型",
            "客户全称",
            "机构",
            "年金计划号",
            "流失日期",
            "计划规模",
            "受托人",
            "company_id",
        ]
    )
    trustee.append(
        [
            "2026年03月",
            "受托",
            "集合",
            "共享客户（流失）",
            "北京",
            "",
            "",
            "80",
            "原受托机构A",
            "company-001",
        ]
    )
    investee = workbook.create_sheet("企年投资流失(解约)")
    investee.append(
        [
            "上报月份",
            "业务类型",
            "计划类型",
            "客户全称",
            "机构",
            "年金计划号",
            "流失日期",
            "计划规模",
            "受托人",
            "company_id",
        ]
    )
    investee.append(
        [
            "2026年03月",
            "投管",
            "单一",
            "新客流失",
            "未知机构",
            "",
            "2026-03-15",
            "60",
            "原受托机构B",
            "",
        ]
    )
    workbook.save(path)


def test_event_domain_gates_use_same_checkpoint_names(tmp_path) -> None:
    award_workbook = tmp_path / "annual_award.xlsx"
    loss_workbook = tmp_path / "annual_loss.xlsx"
    _write_award_workbook(award_workbook)
    _write_loss_workbook(loss_workbook)
    award_replay_root = tmp_path / "reference" / "historical_replays" / "annual_award"
    loss_replay_root = tmp_path / "reference" / "historical_replays" / "annual_loss"
    _write_award_assets(
        award_replay_root,
        legacy_snapshot_rows=[
            {
                "period": "2026-03",
                "contract_state_rows": 1,
                "award_fixture_rows": 1,
                "loss_fixture_rows": 0,
            }
        ],
    )
    _write_loss_assets(
        loss_replay_root,
        legacy_snapshot_rows=[
            {
                "period": "2026-03",
                "contract_state_rows": 1,
                "award_fixture_rows": 1,
                "loss_fixture_rows": 1,
            }
        ],
    )

    award_outcome = run_annual_award_slice(
        workbook=award_workbook,
        period="2026-03",
        replay_root=award_replay_root,
    )
    loss_outcome = run_annual_loss_slice(
        workbook=loss_workbook,
        period="2026-03",
        replay_root=loss_replay_root,
    )

    expected_checkpoints = [
        "source_intake",
        "fact_processing",
        "identity_resolution",
        "reference_derivation",
        "contract_state",
        "monthly_snapshot",
    ]

    assert [result.checkpoint_name for result in award_outcome.checkpoint_results] == expected_checkpoints
    assert [result.checkpoint_name for result in loss_outcome.checkpoint_results] == expected_checkpoints


def test_event_domain_failed_runs_write_same_package(tmp_path) -> None:
    award_workbook = tmp_path / "annual_award.xlsx"
    loss_workbook = tmp_path / "annual_loss.xlsx"
    _write_award_workbook(award_workbook)
    _write_loss_workbook(loss_workbook)
    award_replay_root = tmp_path / "reference" / "historical_replays" / "annual_award"
    loss_replay_root = tmp_path / "reference" / "historical_replays" / "annual_loss"
    failing_snapshot = [
        {
            "period": "2026-03",
            "contract_state_rows": 99,
            "award_fixture_rows": 99,
            "loss_fixture_rows": 99,
        }
    ]
    _write_award_assets(award_replay_root, legacy_snapshot_rows=failing_snapshot)
    _write_loss_assets(loss_replay_root, legacy_snapshot_rows=failing_snapshot)

    award_outcome = run_annual_award_slice(
        workbook=award_workbook,
        period="2026-03",
        replay_root=award_replay_root,
    )
    loss_outcome = run_annual_loss_slice(
        workbook=loss_workbook,
        period="2026-03",
        replay_root=loss_replay_root,
    )

    award_package_root = (
        award_replay_root / "evidence" / "comparison_runs" / award_outcome.comparison_run_id
    )
    loss_package_root = (
        loss_replay_root / "evidence" / "comparison_runs" / loss_outcome.comparison_run_id
    )

    for package_root in (award_package_root, loss_package_root):
        assert (package_root / "manifest.json").exists()
        assert (package_root / "gate-summary.json").exists()
        assert (package_root / "checkpoint-results.json").exists()
        assert (package_root / "source-intake-adaptation.json").exists()
        assert (package_root / "lineage-impact.json").exists()
        assert (package_root / "publication-results.json").exists()
        assert (package_root / "compatibility-case.json").exists()
        assert (package_root / "report.md").exists()
        assert (package_root / "diffs" / "monthly_snapshot.json").exists()

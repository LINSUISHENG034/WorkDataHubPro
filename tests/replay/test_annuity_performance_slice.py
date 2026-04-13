import json
from pathlib import Path

import pytest
from openpyxl import Workbook

from work_data_hub_pro.apps.orchestration.replay.annuity_performance_slice import (
    run_annuity_performance_slice,
)


def _write_replay_assets(
    replay_root: Path,
    *,
    legacy_snapshot_rows: list[dict[str, object]],
    legacy_reference_derivation_rows: list[dict[str, object]] | None = None,
    legacy_fact_processing_rows: list[dict[str, object]] | None = None,
    legacy_identity_resolution_rows: list[dict[str, object]] | None = None,
    legacy_contract_state_rows: list[dict[str, object]] | None = None,
) -> None:
    """Write annuity replay root assets.

    Pass intermediate baseline rows to embed them in the replay root so the slice
    runner's truthful checkpoints pass. If not provided, those baselines are absent
    and the runner fails closed at the corresponding checkpoint.
    """
    replay_root.mkdir(parents=True, exist_ok=True)
    (replay_root / "annual_award_fixture_2026_03.json").write_text(
        json.dumps(
            [
                {
                    "company_id": "company-001",
                    "plan_code": "PLAN-A",
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
    (replay_root / "annual_loss_fixture_2026_03.json").write_text(
        json.dumps(
            [
                {
                    "company_id": "company-001",
                    "plan_code": "PLAN-Z",
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
    (replay_root / "legacy_monthly_snapshot_2026_03.json").write_text(
        json.dumps(legacy_snapshot_rows, indent=2),
        encoding="utf-8",
    )
    # Intermediate checkpoint baselines (required for truthful gate passes)
    if legacy_reference_derivation_rows is not None:
        (replay_root / "legacy_reference_derivation_2026_03.json").write_text(
            json.dumps(legacy_reference_derivation_rows, indent=2),
            encoding="utf-8",
        )
    if legacy_fact_processing_rows is not None:
        (replay_root / "legacy_fact_processing_2026_03.json").write_text(
            json.dumps(legacy_fact_processing_rows, indent=2),
            encoding="utf-8",
        )
    if legacy_identity_resolution_rows is not None:
        (replay_root / "legacy_identity_resolution_2026_03.json").write_text(
            json.dumps(legacy_identity_resolution_rows, indent=2),
            encoding="utf-8",
        )
    if legacy_contract_state_rows is not None:
        (replay_root / "legacy_contract_state_2026_03.json").write_text(
            json.dumps(legacy_contract_state_rows, indent=2),
            encoding="utf-8",
        )


def _write_workbook(workbook_path: Path) -> None:
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "AnnuityPerformance"
    sheet.append(["company_name", "plan_code", "period", "sales_amount"])
    sheet.append(["Acme", "PLAN-A", "2026-03", "1200.50"])
    workbook.save(workbook_path)


def _bootstrap_intermediate_baselines(workbook_path: Path, replay_root: Path) -> None:
    for checkpoint_name in (
        "reference_derivation",
        "fact_processing",
        "identity_resolution",
        "contract_state",
    ):
        (replay_root / f"legacy_{checkpoint_name}_2026_03.json").write_text(
            "[]",
            encoding="utf-8",
        )
    outcome = run_annuity_performance_slice(
        workbook=workbook_path,
        period="2026-03",
        replay_root=replay_root,
    )
    for checkpoint_name in (
        "reference_derivation",
        "fact_processing",
        "identity_resolution",
        "contract_state",
    ):
        (replay_root / f"legacy_{checkpoint_name}_2026_03.json").write_text(
            json.dumps(
                outcome.intermediate_payloads[checkpoint_name],
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )


def test_full_slice_replay_closes_chain_and_matches_legacy_snapshot(tmp_path) -> None:
    """Test 4: successful replay produces full checkpoint list and passes all gates."""
    workbook_path = tmp_path / "annuity_performance_2026_03.xlsx"
    _write_workbook(workbook_path)
    replay_root = tmp_path / "reference" / "historical_replays" / "annuity_performance"
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
    _bootstrap_intermediate_baselines(workbook_path, replay_root)

    outcome = run_annuity_performance_slice(
        workbook=workbook_path,
        period="2026-03",
        replay_root=replay_root,
    )

    assert [result.target_name for result in outcome.publication_results] == [
        "fact_annuity_performance",
        "company_reference",
        "contract_state",
        "monthly_snapshot",
    ]
    assert [result.projection_name for result in outcome.projection_results] == [
        "contract_state",
        "monthly_snapshot",
    ]
    assert outcome.gate_summary.overall_outcome == "passed"
    assert [result.checkpoint_name for result in outcome.checkpoint_results] == [
        "source_intake",
        "fact_processing",
        "identity_resolution",
        "reference_derivation",
        "contract_state",
        "monthly_snapshot",
    ]
    # Verify source_intake uses explicit contract model (not self-compare)
    source_intake_result = next(
        r for r in outcome.checkpoint_results if r.checkpoint_name == "source_intake"
    )
    assert source_intake_result.checkpoint_type == "contract"
    assert source_intake_result.severity == "warn"
    # Contract payloads should have record_count and required_fields keys
    assert "record_count" in source_intake_result.legacy_payload
    assert "required_fields" in source_intake_result.legacy_payload
    assert "allowed_adaptations" in source_intake_result.legacy_payload
    assert outcome.compatibility_case is None
    row_events = outcome.trace_store.find(
        batch_id="annuity_performance:2026-03",
        anchor_row_no=2,
    )
    assert {event.stage_id for event in row_events} == {
        "source_intake",
        "fact_processing",
        "identity_resolution",
    }
    lineage_links = outcome.lineage_registry.all()
    assert len(lineage_links) == 1
    assert lineage_links[0].origin_row_nos == [2]
    assert lineage_links[0].anchor_row_no == 2
    assert lineage_links[0].parent_record_ids == [row_events[0].record_id]


def test_full_slice_replay_creates_compatibility_case_when_snapshot_differs(tmp_path) -> None:
    """Test 3: source_intake can surface warning/failed status from contract assertions."""
    workbook_path = tmp_path / "annuity_performance_2026_03.xlsx"
    _write_workbook(workbook_path)
    replay_root = tmp_path / "reference" / "historical_replays" / "annuity_performance"
    # Include all intermediate baselines so failure is at monthly_snapshot
    _write_replay_assets(
        replay_root,
        legacy_snapshot_rows=[
            {
                "period": "2026-03",
                "contract_state_rows": 99,  # Deliberately mismatched
                "award_fixture_rows": 99,
                "loss_fixture_rows": 99,
            }
        ],
    )
    _bootstrap_intermediate_baselines(workbook_path, replay_root)

    outcome = run_annuity_performance_slice(
        workbook=workbook_path,
        period="2026-03",
        replay_root=replay_root,
    )

    assert outcome.compatibility_case is not None
    assert outcome.compatibility_case.checkpoint_name == "monthly_snapshot"
    assert outcome.compatibility_case.comparison_run_id == outcome.comparison_run_id
    assert outcome.compatibility_case.involved_anchor_row_nos == [2]
    case_path = (
        replay_root
        / "evidence"
        / "compatibility_cases"
        / f"{outcome.compatibility_case.case_id}.json"
    )
    assert case_path.exists()

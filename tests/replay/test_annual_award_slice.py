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
    legacy_reference_derivation_rows: list[dict[str, object]] | None = None,
    legacy_fact_processing_rows: list[dict[str, object]] | None = None,
    legacy_identity_resolution_rows: list[dict[str, object]] | None = None,
    legacy_contract_state_rows: list[dict[str, object]] | None = None,
) -> None:
    """Write award replay root assets with optional intermediate baselines."""
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
                },
            ],
            indent=2,
        ),
        encoding="utf-8",
    )
    (replay_root / "legacy_monthly_snapshot_2026_03.json").write_text(
        json.dumps(legacy_snapshot_rows, indent=2),
        encoding="utf-8",
    )
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
    trustee.append(
        ["Acme", "company-001", "", "collective", "pl-ret", "2026-03", "5000"]
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
    outcome = run_annual_award_slice(
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


def test_annual_award_slice_replay_closes_chain_and_matches_legacy_snapshot(
    tmp_path,
) -> None:
    """Test 4: successful replay produces full checkpoint list and passes all gates."""
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
    _bootstrap_intermediate_baselines(workbook_path, replay_root)

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
    assert outcome.gate_summary.overall_outcome == "passed"
    assert outcome.run_report.comparison_run_id == outcome.comparison_run_id
    assert outcome.run_report.overall_outcome == "passed"
    assert outcome.run_report.primary_failure is None
    package_root = (
        replay_root / "evidence" / "comparison_runs" / outcome.comparison_run_id
    )
    assert package_root.exists()
    assert Path(outcome.run_report.evidence_paths.comparison_run_root) == package_root
    assert Path(outcome.run_report.evidence_paths.manifest).exists()
    assert Path(outcome.run_report.evidence_paths.gate_summary).exists()
    assert Path(outcome.run_report.evidence_paths.checkpoint_results).exists()
    assert Path(outcome.run_report.evidence_paths.publication_results).exists()
    assert Path(outcome.run_report.evidence_paths.report).exists()
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
    assert "record_count" in source_intake_result.legacy_payload
    assert "required_fields" in source_intake_result.legacy_payload
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
    """Test 3: source_intake contract assertions surface non-pass status through explicit expectations."""
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
    _bootstrap_intermediate_baselines(workbook_path, replay_root)

    outcome = run_annual_award_slice(
        workbook=workbook_path,
        period="2026-03",
        replay_root=replay_root,
    )

    assert outcome.compatibility_case is not None
    assert outcome.compatibility_case.checkpoint_name == "monthly_snapshot"
    assert outcome.compatibility_case.comparison_run_id == outcome.comparison_run_id
    assert outcome.compatibility_case.involved_anchor_row_nos == [2, 3]
    assert outcome.run_report.primary_failure is not None
    assert outcome.run_report.primary_failure.checkpoint_name == "monthly_snapshot"
    assert outcome.run_report.compatibility_case == outcome.compatibility_case
    case_path = (
        replay_root
        / "evidence"
        / "compatibility_cases"
        / f"{outcome.compatibility_case.case_id}.json"
    )
    assert case_path.exists()


def test_annual_award_slice_replay_uses_failed_checkpoint_payloads(tmp_path) -> None:
    """Test: when an intermediate checkpoint fails, the compatibility case truthfully
    points to that checkpoint's payload rather than monthly_snapshot."""
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
    baselines = _bootstrap_intermediate_baselines(workbook_path, replay_root)

    # --- Verify passing with correct baselines ---
    outcome_pass = run_annual_award_slice(
        workbook=workbook_path,
        period="2026-03",
        replay_root=replay_root,
    )
    assert outcome_pass.run_report.primary_failure is None
    assert outcome_pass.compatibility_case is None

    # --- Test fact_processing failure ---
    (replay_root / "legacy_fact_processing_2026_03.json").write_text(
        json.dumps(
            [
                {
                    "record_id": "award-001",
                    "company_id": "company-FORCED-FAIL",
                    "plan_code": "WRONG",
                    "period": "2026-03",
                    "award_amount": 0,
                    "source_sheet": "TrusteeAwards",
                },
                {
                    "record_id": "award-002",
                    "company_id": "company-FORCED-FAIL",
                    "plan_code": "WRONG",
                    "period": "2026-03",
                    "award_amount": 0,
                    "source_sheet": "InvesteeAwards",
                },
            ],
            indent=2,
        ),
        encoding="utf-8",
    )
    outcome_fp = run_annual_award_slice(
        workbook=workbook_path,
        period="2026-03",
        replay_root=replay_root,
    )
    assert outcome_fp.compatibility_case is not None
    assert outcome_fp.run_report.primary_failure is not None
    assert outcome_fp.run_report.primary_failure.checkpoint_name == "fact_processing"
    assert outcome_fp.compatibility_case.checkpoint_name == "fact_processing"
    assert outcome_fp.compatibility_case.sample_locator.endswith(
        "legacy_fact_processing_2026_03.json"
    )
    assert outcome_fp.compatibility_case.legacy_result["rows"] == baselines["fact_processing"]
    assert outcome_fp.compatibility_case.pro_result["rows"] is not None

    # Restore
    (replay_root / "legacy_fact_processing_2026_03.json").write_text(
        json.dumps(baselines["fact_processing"], indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    # --- Test identity_resolution failure ---
    (replay_root / "legacy_identity_resolution_2026_03.json").write_text(
        json.dumps(
            [
                {
                    "record_id": "award-001",
                    "resolved_identity": "company-IR-FAIL",
                    "resolution_method": "static",
                    "fallback_level": "none",
                    "evidence_refs": [],
                },
                {
                    "record_id": "award-002",
                    "resolved_identity": "company-IR-FAIL",
                    "resolution_method": "static",
                    "fallback_level": "none",
                    "evidence_refs": [],
                },
            ],
            indent=2,
        ),
        encoding="utf-8",
    )
    outcome_ir = run_annual_award_slice(
        workbook=workbook_path,
        period="2026-03",
        replay_root=replay_root,
    )
    assert outcome_ir.compatibility_case is not None
    assert outcome_ir.run_report.primary_failure is not None
    assert outcome_ir.run_report.primary_failure.checkpoint_name == "identity_resolution"
    assert outcome_ir.compatibility_case.checkpoint_name == "identity_resolution"
    assert outcome_ir.compatibility_case.sample_locator.endswith(
        "legacy_identity_resolution_2026_03.json"
    )
    assert outcome_ir.compatibility_case.legacy_result["rows"] == baselines["identity_resolution"]
    assert outcome_ir.compatibility_case.pro_result["rows"] is not None

    # Restore
    (replay_root / "legacy_identity_resolution_2026_03.json").write_text(
        json.dumps(baselines["identity_resolution"], indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    # --- Test contract_state failure ---
    (replay_root / "legacy_contract_state_2026_03.json").write_text(
        json.dumps(
            [
                {
                    "period": "2026-03",
                    "contract_state_rows": 99,
                    "award_fixture_rows": 99,
                    "loss_fixture_rows": 99,
                }
            ],
            indent=2,
        ),
        encoding="utf-8",
    )
    outcome_cs = run_annual_award_slice(
        workbook=workbook_path,
        period="2026-03",
        replay_root=replay_root,
    )
    assert outcome_cs.compatibility_case is not None
    assert outcome_cs.run_report.primary_failure is not None
    assert outcome_cs.run_report.primary_failure.checkpoint_name == "contract_state"
    assert outcome_cs.compatibility_case.checkpoint_name == "contract_state"
    assert outcome_cs.compatibility_case.sample_locator.endswith(
        "legacy_contract_state_2026_03.json"
    )
    assert outcome_cs.compatibility_case.legacy_result["rows"] == baselines["contract_state"]
    assert outcome_cs.compatibility_case.pro_result["rows"] is not None

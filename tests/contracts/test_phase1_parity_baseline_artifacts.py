import json
from pathlib import Path


PHASE_ROOT = Path(".planning/phases/01-legacy-capability-mapping-parity-harness")
PARITY_BASELINE = PHASE_ROOT / "artifacts/parity-baseline.json"
MISMATCH_REPORT = PHASE_ROOT / "artifacts/mismatch-report.json"
DECISION_LOG = PHASE_ROOT / "artifacts/decision-log.md"

PHASE1_DOMAINS = {"annuity_performance", "annual_award", "annual_loss"}
REQUIRED_CHECKPOINT_OUTPUTS = {
    "mapping completeness status",
    "baseline dataset identity",
    "parity summary",
    "mismatch severity table",
    "human decision log",
}


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_identity_fields_present() -> None:
    baseline = _read_json(PARITY_BASELINE)

    identity = baseline["baseline_dataset_identity"]
    assert identity["baseline_version"].strip()
    assert identity["comparison_run_id"].strip()
    assert set(identity["sample_batch_id_index"]) == PHASE1_DOMAINS

    domains = baseline["domains"]
    assert {entry["domain"] for entry in domains} == PHASE1_DOMAINS

    for entry in domains:
        assert entry["sample_batch_id"].strip()
        assert entry["baseline_version"] == identity["baseline_version"]
        assert entry["comparison_run_id"] == identity["comparison_run_id"]

    sample_strategy = baseline["sample_strategy"]
    assert sample_strategy["review_ref"].endswith(
        "2026-04-12-phase1-sample-strategy-review.md"
    )
    assert Path(sample_strategy["must_pass_deep_sample"]["path"]).exists()
    assert Path(sample_strategy["supplemental_real_sample"]["path"]).exists()
    assert (
        sample_strategy["supplemental_real_sample"]["status"]
        == "supplemental-contract-gap"
    )


def test_checkpoint_outputs_present() -> None:
    baseline = _read_json(PARITY_BASELINE)
    mismatch_report = _read_json(MISMATCH_REPORT)

    assert set(baseline["checkpoint_outputs"]) == REQUIRED_CHECKPOINT_OUTPUTS
    assert "parity_summary" in mismatch_report
    assert "mismatch_table" in mismatch_report
    assert "execution_evidence" in mismatch_report
    assert set(mismatch_report["mismatch_table"]["columns"]) >= {
        "severity",
        "classification_reason",
        "status",
        "evidence_ref",
    }
    assert set(mismatch_report["parity_summary"]["domains_reviewed"]) == {
        "annuity_performance"
    }
    assert set(mismatch_report["parity_summary"]["registered_scope_only"]) == {
        "annual_award",
        "annual_loss",
    }


def test_mismatch_report_contains_real_annuity_execution_evidence() -> None:
    mismatch_report = _read_json(MISMATCH_REPORT)

    execution_evidence_path = Path(mismatch_report["execution_evidence"]["evidence_ref"])
    assert execution_evidence_path.exists()
    assert Path(mismatch_report["execution_evidence"]["must_pass_input"]).exists()
    assert Path(
        mismatch_report["execution_evidence"]["supplemental_real_sample"]
    ).exists()
    assert (
        mismatch_report["execution_evidence"]["supplemental_real_sample_status"]
        == "tracked-as-contract-gap"
    )

    annuity_rows = [
        row
        for row in mismatch_report["mismatch_table"]["rows"]
        if row["domain"] == "annuity_performance"
    ]
    assert annuity_rows

    deep_sample_row = annuity_rows[0]
    assert deep_sample_row["status"] == "matched"
    assert deep_sample_row["severity"] == "none"
    assert Path(deep_sample_row["evidence_ref"]).exists()
    assert "real annuity_performance replay execution matched" in deep_sample_row[
        "classification_reason"
    ]

    assert mismatch_report["sample_strategy"]["review_ref"].endswith(
        "2026-04-12-phase1-sample-strategy-review.md"
    )
    assert Path(mismatch_report["sample_strategy"]["must_pass_input"]).exists()
    assert Path(mismatch_report["sample_strategy"]["supplemental_real_sample"]).exists()
    assert (
        mismatch_report["sample_strategy"]["supplemental_real_sample_status"]
        == "not executed in must-pass parity run"
    )


def test_decision_log_template_requires_human_fields() -> None:
    decision_log = DECISION_LOG.read_text(encoding="utf-8")

    for required_text in (
        "decision_owner",
        "decision",
        "scope",
        "follow_up",
        "comparison_run_id",
        "approved",
        "approved-with-warn",
    ):
        assert required_text in decision_log

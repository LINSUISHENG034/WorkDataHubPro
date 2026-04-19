from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

import pytest
from typer.testing import CliRunner

from work_data_hub_pro.apps.etl_cli import main as cli_main
from work_data_hub_pro.apps.orchestration.replay.contracts import ReplayEvidencePaths
from work_data_hub_pro.apps.orchestration.replay.lookup import ReplayLookupError, ReplayLookupResult
from work_data_hub_pro.apps.orchestration.replay.runtime import finalize_replay_run
from work_data_hub_pro.governance.compatibility.gate_models import (
    CheckpointFingerprint,
    CheckpointResult,
)
from work_data_hub_pro.governance.evidence_index.file_store import FileEvidenceIndex


class _LineageRegistryStub:
    def __init__(self, links: list[SimpleNamespace]) -> None:
        self._links = links

    def all(self) -> list[SimpleNamespace]:
        return list(self._links)


class _BatchStub:
    def __init__(self, *, batch_id: str) -> None:
        self.batch_id = batch_id
        self.domain = "annual_award"
        self.period = "2026-03"



def _checkpoint_result(comparison_run_id: str) -> CheckpointResult:
    return CheckpointResult(
        comparison_run_id=comparison_run_id,
        checkpoint_name="monthly_snapshot",
        checkpoint_type="parity",
        status="passed",
        severity="block",
        legacy_fingerprint=CheckpointFingerprint(fingerprint="same", row_count=1),
        pro_fingerprint=CheckpointFingerprint(fingerprint="same", row_count=1),
        diff_path=None,
        trace_anchor_rows=[7],
    )



def test_replay_evidence_paths_include_lookup_ready_package_fields() -> None:
    fields = ReplayEvidencePaths.__dataclass_fields__

    assert "source_intake_adaptation" in fields
    assert "lineage_impact" in fields



def test_finalize_replay_run_persists_lookup_ready_lineage_records(tmp_path: Path) -> None:
    comparison_run_id = "comparison-lookup-001"
    evidence_index = FileEvidenceIndex(tmp_path / "evidence")
    batch = _BatchStub(batch_id="batch:001")
    trace_path = evidence_index.index_trace_events(
        batch_id=batch.batch_id,
        anchor_row_no=7,
        events=[],
    )
    context = SimpleNamespace(
        comparison_run_id=comparison_run_id,
        evidence_index=evidence_index,
        lineage_registry=_LineageRegistryStub(
            [
                SimpleNamespace(
                    record_id="record-001",
                    anchor_row_no=7,
                    origin_row_nos=[70, 71],
                    parent_record_ids=["parent-001"],
                ),
                SimpleNamespace(
                    record_id="record-002",
                    anchor_row_no=9,
                    origin_row_nos=[90],
                    parent_record_ids=["parent-002"],
                ),
            ]
        ),
    )

    _, run_report = finalize_replay_run(
        context=context,
        batch=batch,
        baseline_version="baseline-001",
        config_release_id="release-001",
        rule_pack_version="rules-001",
        checkpoint_results=[_checkpoint_result(comparison_run_id)],
        source_intake_adaptation={"records": []},
        lineage_impact={"affected_anchor_rows": [7, 9]},
        publication_results=[],
        compatibility_case=None,
        report_markdown="# Report\n",
    )

    lineage_payload = json.loads(
        Path(run_report.evidence_paths.lineage_impact).read_text(encoding="utf-8")
    )

    assert run_report.evidence_paths.source_intake_adaptation.endswith(
        "source-intake-adaptation.json"
    )
    assert run_report.evidence_paths.lineage_impact.endswith("lineage-impact.json")
    assert lineage_payload == {
        "records": [
            {
                "record_id": "record-001",
                "batch_id": "batch:001",
                "anchor_row_no": 7,
                "origin_row_nos": [70, 71],
                "parent_record_ids": ["parent-001"],
                "trace_path": trace_path.as_posix(),
                "artifact_gaps": [],
            },
            {
                "record_id": "record-002",
                "batch_id": "batch:001",
                "anchor_row_no": 9,
                "origin_row_nos": [90],
                "parent_record_ids": ["parent-002"],
                "trace_path": None,
                "artifact_gaps": ["trace_missing"],
            },
        ]
    }



def test_file_evidence_index_load_lineage_impact_fails_closed_for_missing_package(
    tmp_path: Path,
) -> None:
    evidence_index = FileEvidenceIndex(tmp_path / "evidence")
    run_root = evidence_index.comparison_run_root("comparison-001")
    (run_root / "manifest.json").write_text(
        json.dumps(
            {
                "comparison_run_id": "comparison-001",
                "domain": "annual_award",
                "period": "2026-03",
                "baseline_version": "baseline-001",
                "config_release_id": "release-001",
                "rule_pack_version": "rules-001",
                "decision_owner": "compatibility-review",
                "package_root": "comparison_runs/comparison-001",
                "package_paths": {
                    "lineage_impact": "comparison_runs/comparison-001/lineage-impact.json"
                },
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="missing_lineage_package"):
        evidence_index.load_lineage_impact("comparison-001")


@pytest.mark.parametrize(
    "payload",
    [
        "{not-json",
        json.dumps({"affected_anchor_rows": [1]}),
        json.dumps({"records": [{"record_id": "record-001"}]}),
        json.dumps(
            {
                "records": [
                    {
                        "record_id": "record-001",
                        "batch_id": "batch-001",
                        "anchor_row_no": 7,
                        "origin_row_nos": "70",
                        "parent_record_ids": ["parent-001"],
                        "trace_path": None,
                        "artifact_gaps": [],
                    }
                ]
            }
        ),
    ],
)
def test_file_evidence_index_load_lineage_impact_fails_closed_for_malformed_package(
    tmp_path: Path,
    payload: str,
) -> None:
    evidence_index = FileEvidenceIndex(tmp_path / "evidence")
    run_root = evidence_index.comparison_run_root("comparison-001")
    (run_root / "manifest.json").write_text(
        json.dumps(
            {
                "comparison_run_id": "comparison-001",
                "domain": "annual_award",
                "period": "2026-03",
                "baseline_version": "baseline-001",
                "config_release_id": "release-001",
                "rule_pack_version": "rules-001",
                "decision_owner": "compatibility-review",
                "package_root": "comparison_runs/comparison-001",
                "package_paths": {
                    "lineage_impact": "comparison_runs/comparison-001/lineage-impact.json"
                },
            }
        ),
        encoding="utf-8",
    )
    (run_root / "lineage-impact.json").write_text(payload, encoding="utf-8")

    with pytest.raises(ValueError, match="malformed_lineage_package"):
        evidence_index.load_lineage_impact("comparison-001")



def test_replay_lookup_result_fields_match_cli_contract() -> None:
    fields = ReplayLookupResult.__dataclass_fields__

    assert list(fields) == [
        "comparison_run_id",
        "record_id",
        "batch_id",
        "anchor_row_no",
        "origin_row_nos",
        "parent_record_ids",
        "trace_path",
        "artifact_gaps",
        "checkpoint_statuses",
        "compatibility_case_id",
    ]


@pytest.mark.parametrize(
    "code",
    [
        "missing_selector",
        "conflicting_selectors",
        "invalid_comparison_run_id",
        "record_not_found",
        "ambiguous_anchor",
        "missing_lineage_package",
        "malformed_lineage_package",
    ],
)
def test_replay_lookup_cli_returns_machine_readable_error_codes(
    monkeypatch: pytest.MonkeyPatch,
    code: str,
) -> None:
    runner = CliRunner()

    def _raise(*args, **kwargs):
        raise ReplayLookupError(code)

    monkeypatch.setattr(cli_main, "load_replay_lookup", _raise)

    result = runner.invoke(
        cli_main.app,
        ["replay", "lookup", "--comparison-run-id", "comparison-001", "--record-id", "record-001"],
    )

    assert result.exit_code == 1
    assert json.loads(result.stdout) == {
        "error": code,
        "comparison_run_id": "comparison-001",
    }



def test_replay_lookup_cli_returns_machine_readable_success_payload(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    runner = CliRunner()
    monkeypatch.setattr(
        cli_main,
        "load_replay_lookup",
        lambda comparison_run_id, record_id=None, anchor_row_no=None: ReplayLookupResult(
            comparison_run_id=comparison_run_id,
            record_id=record_id or "record-001",
            batch_id="batch:001",
            anchor_row_no=7 if anchor_row_no is None else anchor_row_no,
            origin_row_nos=[70, 71],
            parent_record_ids=["parent-001"],
            trace_path="/tmp/trace.json",
            artifact_gaps=[],
            checkpoint_statuses={"monthly_snapshot": "passed"},
            compatibility_case_id=None,
        ),
    )

    result = runner.invoke(
        cli_main.app,
        ["replay", "lookup", "--comparison-run-id", "comparison-001", "--record-id", "record-001"],
    )

    assert result.exit_code == 0
    assert json.loads(result.stdout) == {
        "comparison_run_id": "comparison-001",
        "record_id": "record-001",
        "batch_id": "batch:001",
        "anchor_row_no": 7,
        "origin_row_nos": [70, 71],
        "parent_record_ids": ["parent-001"],
        "trace_path": "/tmp/trace.json",
        "artifact_gaps": [],
        "checkpoint_statuses": {"monthly_snapshot": "passed"},
        "compatibility_case_id": None,
    }



def test_replay_lookup_cli_exposes_expected_option_names() -> None:
    runner = CliRunner()
    result = runner.invoke(cli_main.app, ["replay", "lookup", "--help"])

    assert result.exit_code == 0
    assert "--comparison-run-id" in result.stdout
    assert "--record-id" in result.stdout
    assert "--anchor-row-no" in result.stdout

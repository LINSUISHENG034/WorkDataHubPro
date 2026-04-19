from __future__ import annotations

import json
from pathlib import Path


POLICY_PATH = Path("config/policies/evidence_redaction.json")
EXPECTED_POLICY = {
    "policy_id": "phase4-evidence-redaction-v1",
    "mask_token": "***REDACTED***",
    "sensitive_trace_fields": [
        "company_name",
        "customer_name",
        "raw_company_name",
        "normalized_company_name",
    ],
    "sensitive_payload_keys": [
        "company_name",
        "customer_name",
        "raw_company_name",
        "normalized_company_name",
        "raw_payload",
    ],
    "structured_payload_roots": [
        "legacy_result",
        "pro_result",
        "legacy_payload",
        "pro_payload",
    ],
    "preserve_exact_fields": [
        "comparison_run_id",
        "batch_id",
        "record_id",
        "anchor_row_no",
        "origin_row_nos",
        "parent_record_ids",
        "trace_path",
        "artifact_gaps",
        "stage_id",
        "rule_id",
        "rule_version",
        "checkpoint_name",
        "case_id",
        "compatibility_case_id",
        "severity",
        "decision_status",
        "decision_owner",
        "resolution_note",
        "closure_evidence",
        "closed_at",
        "closed_by",
        "resolved_outcome",
    ],
}


def test_evidence_redaction_policy_exists() -> None:
    assert POLICY_PATH.exists()


def test_evidence_redaction_policy_contains_required_structure() -> None:
    payload = json.loads(POLICY_PATH.read_text(encoding="utf-8"))

    assert payload == EXPECTED_POLICY

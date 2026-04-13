from __future__ import annotations

import json
from pathlib import Path

import pytest

from work_data_hub_pro.apps.orchestration.replay.errors import (
    ReplayAssetNotFoundError,
    ReplayConfigurationError,
    ReplayContractSetupError,
    ReplayDiagnosticsNotFoundError,
    ReplaySetupError,
    translate_replay_setup_error,
)
from work_data_hub_pro.governance.compatibility.gate_runtime import (
    load_required_checkpoint_baseline,
)
from work_data_hub_pro.platform.contracts.publication import (
    PublicationMode,
    PublicationPlan,
)
from work_data_hub_pro.platform.contracts.validators import validate_publication_plan
from work_data_hub_pro.platform.publication.service import (
    PublicationPolicy,
    PublicationPolicyEntry,
    build_publication_plan,
    load_publication_policy,
)


def test_translate_replay_setup_error_maps_missing_baseline() -> None:
    baseline_path = Path("reference/historical_replays/annual_award/missing.json")

    with pytest.raises(FileNotFoundError) as excinfo:
        load_required_checkpoint_baseline(baseline_path, "reference_derivation")

    error = translate_replay_setup_error(
        domain="annual_award",
        stage="baseline_load",
        exc=excinfo.value,
        context={"baseline_path": str(baseline_path)},
    )

    assert isinstance(error, ReplayAssetNotFoundError)
    assert isinstance(error, ReplaySetupError)
    assert error.domain == "annual_award"
    assert error.stage == "baseline_load"
    assert error.original_exception_type == "FileNotFoundError"
    assert "Missing accepted baseline" in error.original_exception_message
    assert error.context["baseline_path"] == str(baseline_path)


def test_translate_replay_setup_error_maps_malformed_baseline_json_type(
    tmp_path: Path,
) -> None:
    baseline_path = tmp_path / "legacy_identity_resolution_2026_03.json"
    baseline_path.write_text(
        json.dumps({"not": "a list"}),
        encoding="utf-8",
    )

    with pytest.raises(TypeError) as excinfo:
        load_required_checkpoint_baseline(baseline_path, "identity_resolution")

    error = translate_replay_setup_error(
        domain="annual_loss",
        stage="baseline_load",
        exc=excinfo.value,
        context={"baseline_path": str(baseline_path)},
    )

    assert isinstance(error, ReplayConfigurationError)
    assert error.original_exception_type == "TypeError"
    assert "must contain a JSON array" in error.original_exception_message


@pytest.mark.parametrize(
    ("stage", "exc"),
    [
        (
            "publication_policy_domain",
            KeyError("annual_award"),
        ),
        (
            "publication_policy_target",
            KeyError("monthly_snapshot"),
        ),
    ],
)
def test_translate_replay_setup_error_maps_missing_publication_policy_domain_or_target(
    stage: str,
    exc: KeyError,
) -> None:
    error = translate_replay_setup_error(
        domain="annuity_performance",
        stage=stage,
        exc=exc,
        context={"policy_path": "config/policies/publication.json"},
    )

    assert isinstance(error, ReplayConfigurationError)
    assert error.original_exception_type == "KeyError"
    assert error.context["policy_path"] == "config/policies/publication.json"


def test_missing_publication_policy_domain_translates_from_real_loader(
    tmp_path: Path,
) -> None:
    policy_path = tmp_path / "publication.json"
    policy_path.write_text(
        json.dumps(
            {
                "annual_loss": {
                    "monthly_snapshot": {
                        "mode": "REFRESH",
                        "transaction_group": "monthly-snapshot",
                        "idempotency_scope": "period",
                    }
                }
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(KeyError) as excinfo:
        load_publication_policy(policy_path, domain="annual_award")

    error = translate_replay_setup_error(
        domain="annual_award",
        stage="publication_policy_domain",
        exc=excinfo.value,
        context={"policy_path": str(policy_path)},
    )

    assert isinstance(error, ReplayConfigurationError)
    assert error.original_exception_message == "'annual_award'"


def test_missing_publication_policy_target_translates_from_real_builder() -> None:
    policy = PublicationPolicy(
        domain="annual_award",
        targets={
            "fact_annuity_performance": PublicationPolicyEntry(
                mode=PublicationMode.REFRESH,
                transaction_group="facts",
                idempotency_scope="batch",
            )
        },
    )

    with pytest.raises(KeyError) as excinfo:
        build_publication_plan(
            policy=policy,
            publication_id="publication-monthly-snapshot",
            target_name="monthly_snapshot",
            target_kind="projection",
            refresh_keys=["period"],
            upsert_keys=[],
            source_batch_id="annual_award:2026-03",
            source_run_id="run-001",
        )

    error = translate_replay_setup_error(
        domain="annual_award",
        stage="publication_policy_target",
        exc=excinfo.value,
        context={"target_name": "monthly_snapshot"},
    )

    assert isinstance(error, ReplayConfigurationError)
    assert error.original_exception_message == "'monthly_snapshot'"


def test_translate_replay_setup_error_maps_publication_plan_validation_failures() -> None:
    plan = PublicationPlan(
        publication_id="publication-facts",
        target_name="fact_annuity_performance",
        target_kind="fact",
        mode=PublicationMode.REFRESH,
        refresh_keys=[],
        upsert_keys=[],
        source_batch_id="annuity_performance:2026-03",
        source_run_id="run-001",
        idempotency_scope="batch",
        transaction_group="facts",
    )

    with pytest.raises(ValueError) as excinfo:
        validate_publication_plan(plan)

    error = translate_replay_setup_error(
        domain="annuity_performance",
        stage="publication_plan_validation",
        exc=excinfo.value,
        context={"target_name": plan.target_name},
    )

    assert isinstance(error, ReplayContractSetupError)
    assert error.original_exception_type == "ValueError"
    assert "REFRESH publication plans must define refresh_keys." in (
        error.original_exception_message
    )


def test_replay_diagnostics_not_found_error_is_typed_setup_error() -> None:
    error = ReplayDiagnosticsNotFoundError(
        domain="annual_award",
        stage="diagnostics_lookup",
        message="Replay diagnostics package was not found.",
        context={"comparison_run_id": "missing-run"},
        original_exception_type="FileNotFoundError",
        original_exception_message="comparison_run_id not found: missing-run",
    )

    assert isinstance(error, ReplaySetupError)
    assert error.context["comparison_run_id"] == "missing-run"

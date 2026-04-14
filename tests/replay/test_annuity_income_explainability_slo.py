import json
import shutil
from pathlib import Path
from time import perf_counter

import pytest
from openpyxl import Workbook

from work_data_hub_pro.apps.etl_cli.main import replay_annuity_income
from work_data_hub_pro.capabilities.identity_resolution.temp_identity import (
    load_temp_identity_policy,
)


@pytest.fixture(autouse=True)
def _temp_identity_salt(monkeypatch: pytest.MonkeyPatch) -> None:
    policy = load_temp_identity_policy()
    monkeypatch.setenv(str(policy["salt_env_var"]), "annuity-income-replay-salt")


def _copy_committed_replay_assets(replay_root: Path) -> None:
    repo_root = Path(__file__).resolve().parents[2]
    replay_root.parent.mkdir(parents=True, exist_ok=True)
    committed_root = repo_root / "reference" / "historical_replays" / "annuity_income"
    shutil.copytree(committed_root, replay_root)
    shutil.copytree(repo_root / "config", replay_root.parents[2] / "config")


def test_annuity_income_replay_keeps_primary_evidence_retrieval_inside_five_minutes(
    tmp_path, monkeypatch
) -> None:
    workspace_root = tmp_path / "workspace"
    workspace_root.mkdir(parents=True, exist_ok=True)
    monkeypatch.chdir(workspace_root)

    workbook_path = workspace_root / "annuity_income_2026_03.xlsx"
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "收入明细"
    sheet.append(["月度", "机构", "机构名称", "计划号", "客户名称", "业务类型", "计划类型", "固费"])
    sheet.append(["2026年03月", "", "北京其他", "", "未知客户", "职年受托", "单一计划", None])
    workbook.save(workbook_path)

    replay_root = workspace_root / "reference" / "historical_replays" / "annuity_income"
    _copy_committed_replay_assets(replay_root)

    started = perf_counter()
    replay_annuity_income(
        workbook=workbook_path,
        period="2026-03",
    )
    evidence_path = replay_root / "evidence" / "trace" / "annuity_income_2026-03__row_2.json"
    payload = json.loads(evidence_path.read_text(encoding="utf-8"))
    elapsed = perf_counter() - started

    assert evidence_path.exists()
    assert elapsed < 300
    assert any(
        item["stage_id"] == "source_intake"
        and item["value_after"]["source_sheet"] == "收入明细"
        for item in payload
    )
    assert any(
        item["stage_id"] == "identity_resolution"
        and item["field_name"] == "company_id"
        for item in payload
    )

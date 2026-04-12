import json
import shutil
from pathlib import Path
from time import perf_counter

from openpyxl import Workbook

from work_data_hub_pro.apps.etl_cli.main import replay_annual_loss


def _copy_committed_replay_assets(replay_root: Path) -> None:
    repo_root = Path(__file__).resolve().parents[2]
    replay_root.parent.mkdir(parents=True, exist_ok=True)
    committed_root = repo_root / "reference" / "historical_replays" / "annual_loss"
    shutil.copytree(committed_root, replay_root)
    shutil.copytree(repo_root / "config", replay_root.parents[2] / "config")


def test_annual_loss_replay_keeps_primary_evidence_retrieval_inside_five_minutes(
    tmp_path, monkeypatch
) -> None:
    workspace_root = tmp_path / "workspace"
    workspace_root.mkdir(parents=True, exist_ok=True)
    monkeypatch.chdir(workspace_root)

    workbook_path = workspace_root / "annual_loss_2026_03.xlsx"
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
            "区域",
            "年金中心",
            "上报人",
            "考核标签",
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
            "区域",
            "年金中心",
            "上报人",
            "考核标签",
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
            "华东",
            "中心B",
            "测试",
            "drop-me",
        ]
    )
    workbook.save(workbook_path)

    replay_root = workspace_root / "reference" / "historical_replays" / "annual_loss"
    _copy_committed_replay_assets(replay_root)

    started = perf_counter()
    replay_annual_loss(
        workbook=workbook_path,
        period="2026-03",
    )
    evidence_path = replay_root / "evidence" / "trace" / "annual_loss_2026-03__row_2.json"
    payload = json.loads(evidence_path.read_text(encoding="utf-8"))
    elapsed = perf_counter() - started

    assert evidence_path.exists()
    assert elapsed < 300
    assert any(
        item["stage_id"] == "source_intake"
        and item["value_after"]["source_sheet"] == "企年投资流失(解约)"
        for item in payload
    )
    assert any(
        item["stage_id"] == "fact_processing.plan_code_enrichment"
        and item["value_after"] == "S9009"
        for item in payload
    )

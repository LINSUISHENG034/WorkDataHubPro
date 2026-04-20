from __future__ import annotations

from pathlib import Path
import subprocess
import yaml


REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL_ROOT = REPO_ROOT / ".codex" / "skills" / "wdhp-semantic-ingress"


def test_semantic_ingress_skill_package_exists() -> None:
    assert SKILL_ROOT.is_dir()

    expected_paths = [
        SKILL_ROOT / "SKILL.md",
        SKILL_ROOT / "agents" / "openai.yaml",
        SKILL_ROOT / "references" / "ingress-template.md",
        SKILL_ROOT / "references" / "promotion-gates.md",
        SKILL_ROOT / "references" / "claim-minimum-fields.md",
        SKILL_ROOT / "scripts" / "semantic_ingress_guard.py",
    ]
    for path in expected_paths:
        assert path.exists(), f"Expected skill package artifact at {path}"


def test_semantic_ingress_skill_doc_contract() -> None:
    skill_text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
    assert (
        "Use only when the user explicitly invokes `wdhp-semantic-ingress` or directly "
        "asks for semantic-ingress work"
    ) in skill_text
    assert "docs/wiki-bi/_meta/legacy-semantic-map/ingress/" in skill_text
    assert "E:\\Projects\\WorkDataHub" in skill_text
    assert (
        "may auto-promote structurally ready findings into `claims/<wave_id>/semantic/`"
    ) in skill_text
    assert "must not write `docs/wiki-bi/` durable pages" in skill_text
    assert "scripts/legacy_semantic_map/semantic_ingress_guard.py" in skill_text
    assert "Call `scripts/legacy_semantic_map/semantic_ingress_guard.py` before writing." in skill_text
    assert "call the ingress guard helper again for promotion evaluation" in skill_text
    assert (
        "stop and ask the user before modifying an existing semantic claim or canonical "
        "semantic file"
    ) in skill_text


def test_semantic_ingress_openai_yaml_contract() -> None:
    payload = yaml.safe_load((SKILL_ROOT / "agents" / "openai.yaml").read_text(encoding="utf-8"))
    assert payload["interface"]["display_name"] == "Semantic Ingress"
    assert 25 <= len(payload["interface"]["short_description"]) <= 64
    assert payload["interface"]["default_prompt"] == (
        "Use $wdhp-semantic-ingress to capture a legacy semantic finding and evaluate promotion readiness."
    )


def test_semantic_ingress_guard_wrapper_imports_repo_helper() -> None:
    wrapper_text = (SKILL_ROOT / "scripts" / "semantic_ingress_guard.py").read_text(
        encoding="utf-8"
    )
    assert "from scripts.legacy_semantic_map.semantic_ingress_guard import main" in wrapper_text


def test_semantic_ingress_guard_wrapper_executes_from_repo_root() -> None:
    wrapper_path = SKILL_ROOT / "scripts" / "semantic_ingress_guard.py"
    result = subprocess.run(
        ["uv", "run", "python", str(wrapper_path), "--help"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert "usage:" in result.stdout.lower()

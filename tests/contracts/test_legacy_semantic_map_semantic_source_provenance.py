from __future__ import annotations

from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[2]
REGISTRY_ROOT = REPO_ROOT / "docs" / "wiki-bi" / "_meta" / "legacy-semantic-map"


def _load_yaml(path: Path) -> dict[str, object]:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def test_active_compiled_semantic_nodes_do_not_use_current_wiki_as_primary_semantic_source() -> None:
    waves_index = _load_yaml(REGISTRY_ROOT / "waves" / "index.yaml")
    active_wave_id = waves_index["active_wave_id"]
    offenders: list[str] = []

    for path in sorted((REGISTRY_ROOT / "semantic").rglob("*.yaml")):
        if path.name == "index.yaml":
            continue
        payload = _load_yaml(path)
        if payload.get("compiled_from_wave_id") != active_wave_id:
            continue
        primary_sources = payload.get("primary_semantic_sources", [])
        for source in primary_sources:
            if isinstance(source, str) and source.startswith("docs/wiki-bi/"):
                offenders.append(
                    f"{path.relative_to(REPO_ROOT).as_posix()} -> {source}"
                )

    assert offenders == []


def test_active_wave_claims_do_not_mark_current_wiki_as_authoritative_semantic_source() -> None:
    waves_index = _load_yaml(REGISTRY_ROOT / "waves" / "index.yaml")
    active_wave_id = waves_index["active_wave_id"]
    claim_root = REGISTRY_ROOT / "claims" / active_wave_id
    offenders: list[str] = []

    for path in sorted(claim_root.rglob("*.yaml")):
        payload = _load_yaml(path)

        for source in payload.get("sources_read", []):
            if (
                isinstance(source, dict)
                and source.get("source_type") == "current_wiki"
                and source.get("semantic_authority") == "authoritative_semantic_source"
            ):
                offenders.append(
                    f"{path.relative_to(REPO_ROOT).as_posix()} -> "
                    f"sources_read:{source.get('relative_path')}"
                )

        for finding in payload.get("semantic_findings", []):
            if not isinstance(finding, dict):
                continue
            for source in finding.get("primary_source_refs", []):
                if isinstance(source, str) and source.startswith("docs/wiki-bi/"):
                    offenders.append(
                        f"{path.relative_to(REPO_ROOT).as_posix()} -> "
                        f"semantic_findings.primary_source_refs:{source}"
                    )

    assert offenders == []

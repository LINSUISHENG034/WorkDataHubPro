from __future__ import annotations

from pathlib import Path


def test_phase2_status_sync_across_project_phase6_artifacts() -> None:
    """
    Phase 2 implementation-complete and governance-sign-off-closed wording
    must remain visible in the committed planning artifacts after legacy-wiki
    removal.
    """
    project_md = Path(".planning/PROJECT.md").read_text(encoding="utf-8")
    roadmap_md = Path(".planning/ROADMAP.md").read_text(encoding="utf-8")
    requirements_md = Path(".planning/REQUIREMENTS.md").read_text(encoding="utf-8")

    assert "Phase 2 implementation complete" in project_md
    assert "Phase 2 governance sign-off closed" in project_md

    assert "Phase 6" in roadmap_md
    assert "2026-04-13" in roadmap_md

    assert "Phase 6 Re-Verification Note" in requirements_md
    assert "2026-04-13" in requirements_md


def test_phase6_roadmap_entry_has_three_plans() -> None:
    """
    The Phase 6 roadmap entry must still list the executed three-plan shape.
    """
    roadmap_md = Path(".planning/ROADMAP.md").read_text(encoding="utf-8")

    assert "3 plans" in roadmap_md or "3 plan" in roadmap_md

    for plan_ref in ("06-01", "06-02", "06-03"):
        assert plan_ref in roadmap_md, (
            f"ROADMAP.md Phase 6 section does not reference {plan_ref}"
        )


def test_requirements_keep_dated_phase6_reverification_note() -> None:
    """
    REQUIREMENTS.md must retain the dated Phase 6 re-verification note after
    legacy-wiki removal.
    """
    requirements_md = Path(".planning/REQUIREMENTS.md").read_text(encoding="utf-8")

    assert "Phase 6 Re-Verification Note" in requirements_md
    assert "2026-04-13" in requirements_md
    assert "governance status-sync contract suite" in requirements_md

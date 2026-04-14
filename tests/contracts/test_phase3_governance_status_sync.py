from __future__ import annotations

from pathlib import Path


def test_phase3_status_sync_across_project_verification_and_state() -> None:
    """
    The committed planning artifacts must distinguish Phase 3 implementation
    completeness from governance-sign-off closure after legacy-wiki removal.
    """
    project_md = Path(".planning/PROJECT.md").read_text(encoding="utf-8")
    verification_md = Path(
        ".planning/phases/03-orchestration-refactor-failure-explainability/03-VERIFICATION.md"
    ).read_text(encoding="utf-8")
    state_md = Path(".planning/STATE.md").read_text(encoding="utf-8")

    phase3_patterns = [
        "Phase 3 implementation",
        "Phase 3 complete",
        "Phase 3 实现",
        "Phase 3 完成",
        "Phase 3：",
    ]
    for label, content in [
        ("PROJECT.md", project_md),
        ("03-VERIFICATION.md", verification_md),
        ("STATE.md", state_md),
    ]:
        assert any(pattern in content for pattern in phase3_patterns), (
            f"{label} does not mention Phase 3 status"
        )

    sign_off_terms = [
        "governance sign-off",
        "governance sign-off closed",
        "governance sign-off pending",
        "sign-off closed",
        "sign-off pending",
    ]
    for label, content in [
        ("PROJECT.md", project_md),
        ("03-VERIFICATION.md", verification_md),
        ("STATE.md", state_md),
    ]:
        assert any(term in content for term in sign_off_terms), (
            f"{label} does not reference Phase 3 governance sign-off status"
        )
        assert "2026-04-13" in content or "2026-04-14" in content, (
            f"{label} is missing a dated Phase 03.1 remediation note"
        )


def test_verification_no_stale_unconditional_closure_sentence() -> None:
    verification_md = Path(
        ".planning/phases/03-orchestration-refactor-failure-explainability/03-VERIFICATION.md"
    ).read_text(encoding="utf-8")

    stale_sentence = "No blocking gaps remain for Phase 3 goal achievement."
    assert stale_sentence not in verification_md


def test_state_and_roadmap_reference_phase03_1_and_phase3_signoff() -> None:
    state_md = Path(".planning/STATE.md").read_text(encoding="utf-8")
    roadmap_md = Path(".planning/ROADMAP.md").read_text(encoding="utf-8")

    assert "Phase 03.1" in state_md
    assert "Phase 03.1" in roadmap_md

    sign_off_terms = [
        "governance sign-off",
        "governance sign-off closed",
        "sign-off closed",
    ]
    assert any(term in state_md for term in sign_off_terms)
    assert any(term in roadmap_md for term in sign_off_terms)


def test_phase03_1_summary_references_closure() -> None:
    summary_path = Path(
        ".planning/phases/03.1-phase-3-governance-remediation-truthful-failure-evidence-and/03.1-03-SUMMARY.md"
    )
    assert summary_path.exists(), "03.1-03-SUMMARY.md not found"

    summary_md = summary_path.read_text(encoding="utf-8")
    assert "Phase 03.1" in summary_md
    assert "governance sign-off" in summary_md or "sign-off" in summary_md

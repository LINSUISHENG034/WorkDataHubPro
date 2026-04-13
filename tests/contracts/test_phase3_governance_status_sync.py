# test_phase3_governance_status_sync.py
# Contract coverage for Phase 3 governance-status wording synchronization
# across .planning/ and wiki-cn docs.
#
# This test mirrors the pattern established in test_phase2_governance_status_sync.py
# but targets Phase 3 implementation-vs-governance-sign-off consistency.
#
# REF-2 rule: "diagnose hardening" refers to fail-closed package-path enforcement
#   and typed invalid-id CLI handling from 03.1-02.

from __future__ import annotations

from pathlib import Path


# ---------------------------------------------------------------------------
# Test 1: project and committed wiki docs distinguish Phase 3 implementation
# completeness from Phase 3 governance sign-off closure.
# ---------------------------------------------------------------------------


def test_phase3_status_sync_across_project_verification_and_wiki() -> None:
    """
    The project, verification, and wiki docs must use consistent wording
    around Phase 3 implementation versus governance sign-off.

    The accepted states are:
      - "Phase 3 implementation complete" (implementation surface delivered)
      - "Phase 3 governance sign-off closed" (from executed Phase 03.1 evidence)

    The docs must NOT retain stale wording that implies Phase 3 closed
    unconditionally before the 2026-04-13 audit blockers were fixed.
    """
    project_md = Path(".planning/PROJECT.md").read_text(encoding="utf-8")
    verification_md = Path(
        ".planning/phases/03-orchestration-refactor-failure-explainability/03-VERIFICATION.md"
    ).read_text(encoding="utf-8")
    wiki_md = Path("docs/wiki-cn/roadmap/overview.md").read_text(encoding="utf-8")

    # All three files must mention Phase 3 implementation status
    # (English or Chinese - wiki uses "Phase 3：" without "implementation")
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
        ("wiki/roadmap/overview.md", wiki_md),
    ]:
        assert any(
            pattern in content for pattern in phase3_patterns
        ), f"{label} does not mention Phase 3 implementation status"

    # All three files must reference Phase 3 governance sign-off
    # (not just "Phase 3 complete" as an unconditional close)
    # Accepts English and Chinese variants used in the wiki
    sign_off_terms = [
        "governance sign-off",
        "governance sign-off closed",
        "governance sign-off pending",
        "sign-off closed",
        "sign-off pending",
        "governance sign-off 已闭合",
        "governance sign-off 已关闭",
        "sign-off 已闭合",
        "sign-off 已关闭",
    ]

    project_has_sign_off = any(term in project_md for term in sign_off_terms)
    verification_has_sign_off = any(term in verification_md for term in sign_off_terms)
    wiki_has_sign_off = any(term in wiki_md for term in sign_off_terms)

    assert project_has_sign_off, (
        "PROJECT.md does not reference Phase 3 governance sign-off status"
    )
    assert verification_has_sign_off, (
        "03-VERIFICATION.md does not reference Phase 3 governance sign-off status"
    )
    assert wiki_has_sign_off, (
        "wiki/roadmap/overview.md does not reference Phase 3 governance sign-off status"
    )

    # The docs must carry a dated Phase 03.1 note (2026-04-13 or later)
    dated_patterns = ["2026-04-13", "2026-04-14"]
    for label, content in [
        ("PROJECT.md", project_md),
        ("03-VERIFICATION.md", verification_md),
        ("wiki/roadmap/overview.md", wiki_md),
    ]:
        assert any(
            pattern in content for pattern in dated_patterns
        ), f"{label} is missing a dated Phase 03.1 remediation note (2026-04-13 or later)"


# ---------------------------------------------------------------------------
# Test 2: 03-VERIFICATION.md no longer contains the stale unconditional-
# closure sentence.
# ---------------------------------------------------------------------------


def test_verification_no_stale_unconditional_closure_sentence() -> None:
    """
    The stale sentence 'No blocking gaps remain for Phase 3 goal achievement.'
    must NOT be present in 03-VERIFICATION.md.

    This sentence was true after initial Phase 3 implementation but ignored
    the three governance findings surfaced in the 2026-04-13 audit review.
    Phase 03.1 remediation replaced this wording with a dated note citing
    the executed evidence.
    """
    verification_md = Path(
        ".planning/phases/03-orchestration-refactor-failure-explainability/03-VERIFICATION.md"
    ).read_text(encoding="utf-8")

    stale_sentence = "No blocking gaps remain for Phase 3 goal achievement."
    assert stale_sentence not in verification_md, (
        "Stale unconditional-closure sentence still present in 03-VERIFICATION.md"
    )


# ---------------------------------------------------------------------------
# Test 3: STATE.md and ROADMAP.md reference Phase 03.1 closure and Phase 3
# governance sign-off concepts.
# ---------------------------------------------------------------------------


def test_state_and_roadmap_reference_phase03_1_and_phase3_signoff() -> None:
    """
    .planning/STATE.md and .planning/ROADMAP.md must reference Phase 03.1
    and Phase 3 governance sign-off status.

    This ensures the Phase 03.1 closure is recorded in the workflow-state
    docs that feed future planning and context selection.
    """
    state_md = Path(".planning/STATE.md").read_text(encoding="utf-8")
    roadmap_md = Path(".planning/ROADMAP.md").read_text(encoding="utf-8")

    # Both must mention Phase 03.1
    assert "Phase 03.1" in state_md, (
        "STATE.md does not reference Phase 03.1"
    )
    assert "Phase 03.1" in roadmap_md, (
        "ROADMAP.md does not reference Phase 03.1"
    )

    # Both must mention Phase 3 governance sign-off
    sign_off_terms = ["governance sign-off", "governance sign-off closed", "sign-off closed"]
    state_has_sign_off = any(term in state_md for term in sign_off_terms)
    roadmap_has_sign_off = any(term in roadmap_md for term in sign_off_terms)

    assert state_has_sign_off, (
        "STATE.md does not reference Phase 3 governance sign-off"
    )
    assert roadmap_has_sign_off, (
        "ROADMAP.md does not reference Phase 3 governance sign-off"
    )


# ---------------------------------------------------------------------------
# Test 4: wiki log references Phase 03.1 remediation.
# ---------------------------------------------------------------------------


def test_wiki_log_references_phase03_1_remediation() -> None:
    """
    docs/wiki-cn/log.md must retain a Phase 03.1 synchronization entry
    recording the post-remediation status.
    """
    log_md = Path("docs/wiki-cn/log.md").read_text(encoding="utf-8")

    assert "Phase 03.1" in log_md, (
        "wiki/log.md does not reference Phase 03.1"
    )
    assert "governance sign-off" in log_md or "sign-off" in log_md, (
        "wiki/log.md does not reference Phase 3 governance sign-off"
    )


# ---------------------------------------------------------------------------
# Test 5: Phase 03.1 plan-03 summary exists (last plan executed).
# ---------------------------------------------------------------------------


def test_phase03_1_plan_03_summary_exists() -> None:
    """
    The Phase 03.1 plan-03 summary must exist in .planning/phases/ to
    provide a verifiable completion record.
    """
    summary_path = Path(
        ".planning/phases/03.1-phase-3-governance-remediation-truthful-failure-evidence-and/03.1-03-SUMMARY.md"
    )
    assert summary_path.exists(), (
        "03.1-03-SUMMARY.md not found — plan-03 completion record missing"
    )

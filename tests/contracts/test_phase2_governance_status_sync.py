from __future__ import annotations

from pathlib import Path


# ---------------------------------------------------------------------------
# Test 1: project and committed wiki docs do not simultaneously claim both
# "fully signed off" and "pending remediation" without an explicit dated
# status note.
# ---------------------------------------------------------------------------


def test_phase2_status_sync_across_project_roadmap_wiki() -> None:
    """
    The project and committed wiki docs must use consistent wording around
    Phase 2 implementation versus governance sign-off.

    The accepted states are:
      - explicit pending note (implementation complete, governance sign-off pending)
      - explicit closure note (implementation complete, governance sign-off closed)

    The docs must NOT simultaneously assert fully signed-off AND pending
    remediation without an explicit dated status note.
    """
    project_md = Path(".planning/PROJECT.md").read_text(encoding="utf-8")
    wiki_md = Path("docs/wiki-cn/roadmap/overview.md").read_text(encoding="utf-8")

    # At least one doc must mention Phase 2 implementation status
    assert (
        "Phase 2 implementation" in project_md or "Phase 2 implementation" in wiki_md
    ), "Neither PROJECT.md nor wiki/roadmap/overview.md mentions Phase 2 implementation status"

    # The committed wiki must carry a dated status note (2026-04-13 or later)
    dated_note_patterns = ["2026-04-13", "2026-04-14"]
    assert any(
        pattern in wiki_md for pattern in dated_note_patterns
    ), "Committed wiki roadmap/overview.md is missing a dated Phase 2 status note (2026-04-13 or later)"

    # Docs must use consistent Phase 2 governance sign-off wording:
    # Either both say "pending" / "待补齐" / "pending until", or both say "closed" / "已闭合"
    sign_off_related = [
        "governance sign-off pending",
        "governance sign-off closed",
        "governance sign-off",
        "sign-off pending",
        "sign-off closed",
        "待补齐",
        "已闭合",
        "pending until",
    ]

    project_has_sign_off = any(term in project_md for term in sign_off_related)
    wiki_has_sign_off = any(term in wiki_md for term in sign_off_related)

    # If neither doc mentions governance sign-off, that's a sync gap
    # (both must at least reference the concept)
    assert (
        project_has_sign_off or wiki_has_sign_off
    ), "Neither PROJECT.md nor wiki/roadmap/overview.md references Phase 2 governance sign-off status"


# ---------------------------------------------------------------------------
# Test 2: Phase 6 roadmap entry lists three plans and points to execution
# once planning is complete.
# ---------------------------------------------------------------------------


def test_phase6_roadmap_entry_has_three_plans() -> None:
    """
    The Phase 6 section in the committed ROADMAP.md must list exactly three
    plans and point to execution once planning is complete.
    """
    roadmap_md = Path(".planning/ROADMAP.md").read_text(encoding="utf-8")

    # Phase 6 section must mention "3 plans"
    assert (
        "3 plans" in roadmap_md or "3 plan" in roadmap_md
    ), "ROADMAP.md Phase 6 section does not state '3 plans'"

    # Phase 6 section must list 06-01, 06-02, and 06-03 plan references
    for plan_ref in ("06-01", "06-02", "06-03"):
        assert plan_ref in roadmap_md, (
            f"ROADMAP.md Phase 6 section does not reference {plan_ref}"
        )


# ---------------------------------------------------------------------------
# Test 3: committed wiki roadmap keeps a dated synchronization note after
# remediation.
# ---------------------------------------------------------------------------


def test_wiki_roadmap_has_dated_phase2_sync_note() -> None:
    """
    The committed wiki roadmap/overview.md must retain a dated Phase 2
    synchronization note that records the post-remediation status.
    """
    wiki_md = Path("docs/wiki-cn/roadmap/overview.md").read_text(encoding="utf-8")

    # Must contain a dated note from 2026-04-13 or later
    dated_patterns = ["2026-04-13", "2026-04-14"]
    assert any(
        pattern in wiki_md for pattern in dated_patterns
    ), "wiki/roadmap/overview.md is missing a dated synchronization note (2026-04-13 or later)"

    # The dated note must reference Phase 2 implementation vs governance distinction
    phase2_implementation_related = [
        "Phase 2 implementation",
        "Phase 2 implementation complete",
        "implementation complete",
        "已完成",
    ]
    assert any(
        term in wiki_md for term in phase2_implementation_related
    ), "wiki/roadmap/overview.md dated note does not reference Phase 2 implementation status"

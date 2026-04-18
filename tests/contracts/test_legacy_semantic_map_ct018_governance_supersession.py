from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


def _line_containing(path: Path, needle: str) -> str:
    for line in path.read_text(encoding="utf-8").splitlines():
        if needle in line:
            return line
    raise AssertionError(f"Could not find line containing {needle!r} in {path}")


def test_ct018_becomes_only_active_semantic_map_follow_on() -> None:
    program_path = (
        REPO_ROOT
        / "docs"
        / "superpowers"
        / "specs"
        / "2026-04-11-workdatahubpro-refactor-program.md"
    )
    matrix_path = (
        REPO_ROOT
        / "docs"
        / "superpowers"
        / "specs"
        / "2026-04-11-workdatahubpro-first-wave-legacy-coverage-matrix.md"
    )

    program_text = program_path.read_text(encoding="utf-8")
    matrix_text = matrix_path.read_text(encoding="utf-8")

    assert "CT-018" in program_text
    assert "CT-017 is superseded by CT-018" in program_text
    assert "docs/superpowers/plans/2026-04-18-workdatahubpro-semantic-map-agent-governance-reframe.md" in program_text

    ct017_line = _line_containing(matrix_path, "| CT-017 |")
    ct018_line = _line_containing(matrix_path, "| CT-018 |")
    assert "`retired`" in ct017_line
    assert "superseded by CT-018 semantic-governance reframe" in ct017_line
    assert "`planned`" in ct018_line
    assert (
        "docs/superpowers/plans/2026-04-18-workdatahubpro-semantic-map-agent-governance-reframe.md"
        in matrix_text
    )


from pathlib import Path


def test_annual_award_governance_docs_mark_phase_c_closed() -> None:
    coverage_matrix = Path(
        "docs/superpowers/specs/2026-04-11-workdatahubpro-first-wave-legacy-coverage-matrix.md"
    ).read_text(encoding="utf-8")
    refactor_program = Path(
        "docs/superpowers/specs/2026-04-11-workdatahubpro-refactor-program.md"
    ).read_text(encoding="utf-8")

    assert "| `annual_award` | accepted multi-sheet slice |" in coverage_matrix
    assert "| AA-001 | multi-sheet workbook merge intake |" in coverage_matrix
    assert "| `accepted` |" in coverage_matrix
    assert "| 2 | `annual_award` | accepted multi-sheet slice |" in refactor_program
    assert "| 3 | `annual_loss` | next recommended slice |" in refactor_program

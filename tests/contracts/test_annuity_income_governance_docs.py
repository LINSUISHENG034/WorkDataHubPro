from pathlib import Path


def test_annuity_income_governance_docs_mark_slice_as_accepted() -> None:
    coverage_matrix = Path(
        "docs/superpowers/specs/2026-04-11-workdatahubpro-first-wave-legacy-coverage-matrix.md"
    ).read_text(encoding="utf-8")
    refactor_program = Path(
        "docs/superpowers/specs/2026-04-11-workdatahubpro-refactor-program.md"
    ).read_text(encoding="utf-8")
    risk_register = Path(
        "docs/superpowers/reviews/2026-04-11-legacy-risk-analysis-for-rebuild.md"
    ).read_text(encoding="utf-8")
    slice_plan = Path(
        "docs/superpowers/plans/2026-04-14-workdatahubpro-annuity-income-validation-slice.md"
    ).read_text(encoding="utf-8")

    assert (
        "| `annuity_income` | accepted validation slice | broader operator-artifact parity and Phase E runtime closure remain follow-on |"
        in coverage_matrix
    )
    assert "| AI-001 | single-sheet workbook intake |" in coverage_matrix
    assert "| `accepted` |" in coverage_matrix
    assert "tests/integration/test_annuity_income_intake.py" in coverage_matrix
    assert "tests/replay/test_annuity_income_slice.py" in coverage_matrix

    assert "- the final Phase D breadth slice for `annuity_income`" in refactor_program
    assert "- replay assets and runbooks exist for all four first-wave domains" in refactor_program
    assert "- first-wave domain coverage is now accepted across Sections 6.1 through 6.4 of the matrix" in refactor_program
    assert "| 4 | `annuity_income` | accepted final first-wave breadth slice | closes first-wave domain coverage while keeping Phase E runtime/operator work explicit |" in refactor_program

    assert "- `annuity_income` is now an accepted validation slice." in risk_register
    assert "`accepted but narrowed`" in risk_register
    assert "| `CR-009` | `annuity_income` operator-facing artifact contract | supplemental `SFR-005` | `accepted but narrowed` | `AI-004` |" in risk_register
    assert "| `CR-010` | `annuity_income` service-delegation and explicit no-hook runtime contract | supplemental `SFR-006` | `accepted but narrowed` | `AI-005` |" in risk_register

    assert "**Status:** Done" in slice_plan

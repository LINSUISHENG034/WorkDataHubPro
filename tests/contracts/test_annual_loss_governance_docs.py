from pathlib import Path


def test_annual_loss_governance_docs_mark_slice_as_accepted_and_advance_annuity_income() -> None:
    coverage_matrix = Path(
        "docs/superpowers/specs/2026-04-11-workdatahubpro-first-wave-legacy-coverage-matrix.md"
    ).read_text(encoding="utf-8")
    refactor_program = Path(
        "docs/superpowers/specs/2026-04-11-workdatahubpro-refactor-program.md"
    ).read_text(encoding="utf-8")

    assert (
        "| `annual_award` | accepted multi-sheet slice | `annuity_income` remains the only unclosed first-wave breadth work |"
        in coverage_matrix
    )
    assert (
        "| `annual_loss` | accepted breadth-closure slice | `annuity_income` remains the only unclosed first-wave domain |"
        in coverage_matrix
    )
    assert (
        "| `annuity_income` | next recommended single-sheet breadth slice | no accepted executable slice yet |"
        in coverage_matrix
        or "| `annuity_income` | admitted validation slice plan | no accepted executable slice yet |"
        in coverage_matrix
        or "| `annuity_income` | validation slice in progress | full slice acceptance and broader operator-artifact closure still pending |"
        in coverage_matrix
        or "| `annuity_income` | accepted validation slice | broader operator-artifact parity and Phase E runtime closure remain follow-on |"
        in coverage_matrix
    )

    assert (
        "| AL-001 | multi-sheet loss-domain intake contract | capability | legacy migration workflow and paired event-domain references | `capabilities/source_intake/annual_loss/service.py` | `capabilities` | architecture blueprint + annual loss slice plan | `accepted` | `tests/integration/test_annual_loss_intake.py`, `tests/replay/test_annual_loss_slice.py` | N/A | merged anchors stay queryable by batch + anchor row |"
        in coverage_matrix
    )
    assert (
        "| AL-002 | canonical loss event transformation | capability | legacy domain behavior and capability-map-equivalent references | `capabilities/fact_processing/annual_loss/` | `capabilities` | architecture blueprint + annual loss slice plan | `accepted` | `tests/integration/test_annual_loss_processing.py`, `tests/replay/test_annual_loss_slice.py` | N/A | governed rule-pack binding and date parsing are explicit |"
        in coverage_matrix
    )
    assert (
        "| AL-003 | identity / plan-code handling for loss rows | mechanism | legacy event-domain behavior | shared identity contract plus loss-specific current-contract lookup | `capabilities` | annual loss slice plan | `accepted` | `tests/integration/test_identity_resolution.py`, `tests/integration/test_annual_loss_plan_code_enrichment.py`, replay evidence | N/A | source company id now wins before cache/provider fallback and current-row lookup keeps `valid_to` filtering explicit |"
        in coverage_matrix
    )
    assert (
        "| AL-004 | loss fact publication consumed by downstream status rules | projection | downstream snapshot dependency implied by current fixtures and blueprint | explicit publication plus projection evidence | `platform` + `capabilities` | annual loss slice plan | `accepted` | `tests/integration/test_projection_outputs.py`, `tests/replay/test_annual_loss_slice.py`, `tests/replay/test_annual_loss_explainability_slo.py` | N/A | the slice replaces fixture-only loss dependency with published fact coverage |"
        in coverage_matrix
    )

    assert (
        "| XD-002 | `annual_loss` facts influence downstream snapshot status triggered by `annuity_performance` | event-domain closure matters for customer status correctness | active dependency | closed by the accepted `annual_loss` slice with published-fact projection coverage |"
        in coverage_matrix
    )

    assert "- the first Phase D breadth slice for `annual_loss`" in refactor_program
    assert (
        "- compatibility adjudication and evidence indexing exist for the first three accepted slices"
        in refactor_program
        or "- compatibility adjudication and evidence indexing exist for all four accepted slices"
        in refactor_program
    )
    assert (
        "- replay assets and runbooks exist for `annuity_performance`, `annual_award`, and `annual_loss`"
        in refactor_program
        or "- replay assets and runbooks exist for all four first-wave domains"
        in refactor_program
    )
    assert (
        "- `annuity_income` does not have an accepted executable slice yet"
        in refactor_program
        or "- the final Phase D breadth slice for `annuity_income`" in refactor_program
    )
    assert (
        "| 3 | `annual_loss` | accepted breadth-closure slice | closes the paired event-domain dependency path before the final single-sheet breadth slice |"
        in refactor_program
    )
    assert (
        "| 4 | `annuity_income` | next recommended single-sheet breadth slice | extends first-wave coverage after event-domain breadth risk is reduced |"
        in refactor_program
        or "| 4 | `annuity_income` | accepted final first-wave breadth slice | closes first-wave domain coverage while keeping Phase E runtime/operator work explicit |"
        in refactor_program
    )

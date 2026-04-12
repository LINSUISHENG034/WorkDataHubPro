from pathlib import Path


COVERAGE_MATRIX = Path(
    "docs/superpowers/specs/2026-04-11-workdatahubpro-first-wave-legacy-coverage-matrix.md"
)


def test_annual_loss_acceptance_updates_coverage_matrix_without_dropping_runtime_surfaces() -> None:
    coverage_matrix = COVERAGE_MATRIX.read_text(encoding="utf-8")

    assert "| `annual_loss` | accepted breadth-closure slice |" in coverage_matrix
    assert "| `annuity_income` | next recommended single-sheet breadth slice |" in coverage_matrix
    assert (
        "| AL-001 | multi-sheet loss-domain intake contract | capability |"
        " legacy migration workflow and paired event-domain references |"
        " `capabilities/source_intake/annual_loss/service.py` | `capabilities` |"
        " architecture blueprint + annual loss slice plan | `accepted` |"
        " `tests/integration/test_annual_loss_intake.py`, `tests/replay/test_annual_loss_slice.py` |"
        " N/A | merged anchors stay queryable by batch + anchor row |"
    ) in coverage_matrix
    assert (
        "| AL-002 | canonical loss event transformation | capability |"
        " legacy domain behavior and capability-map-equivalent references |"
        " `capabilities/fact_processing/annual_loss/` | `capabilities` |"
        " architecture blueprint + annual loss slice plan | `accepted` |"
        " `tests/integration/test_annual_loss_processing.py`, `tests/replay/test_annual_loss_slice.py` |"
        " N/A | governed rule-pack binding and date parsing are explicit |"
    ) in coverage_matrix
    assert (
        "| AL-003 | identity / plan-code handling for loss rows | mechanism |"
        " legacy event-domain behavior | shared identity contract plus loss-specific current-contract lookup |"
        " `capabilities` | annual loss slice plan | `accepted` |"
        " `tests/integration/test_identity_resolution.py`,"
        " `tests/integration/test_annual_loss_plan_code_enrichment.py`, replay evidence |"
        " N/A | source company id now wins before cache/provider fallback and current-row lookup keeps `valid_to` filtering explicit |"
    ) in coverage_matrix
    assert (
        "| AL-004 | loss fact publication consumed by downstream status rules | projection |"
        " downstream snapshot dependency implied by current fixtures and blueprint |"
        " explicit publication plus projection evidence | `platform` + `capabilities` |"
        " annual loss slice plan | `accepted` |"
        " `tests/integration/test_projection_outputs.py`, `tests/replay/test_annual_loss_slice.py`,"
        " `tests/replay/test_annual_loss_explainability_slo.py` |"
        " N/A | the slice replaces fixture-only loss dependency with published fact coverage |"
    ) in coverage_matrix
    assert "| CT-011 | `company_lookup_queue` special orchestration domain and async retry/runtime contract |" in coverage_matrix
    assert "| CT-012 | `reference_sync` special orchestration domain, daily schedule, and sync-state persistence for authoritative business-schema targets |" in coverage_matrix
    assert "| CT-013 | enterprise identity cache and queue persistence surfaces (`enrichment_requests`, `enrichment_index`, `company_name_index`) |" in coverage_matrix
    assert "| CT-014 | enterprise EQC raw and cleansed persistence surfaces (`base_info`, `business_info`, `biz_label`) |" in coverage_matrix
    assert "| CT-015 | manual `customer-mdm` operator command surface outside ETL hook execution (`sync`, `snapshot`, `init-year`, `validate`, `cutover`) |" in coverage_matrix
    assert "| CT-016 | shared unresolved-name and failed-record operator artifact parity across first-wave runs |" in coverage_matrix
    assert "current accepted event-domain slices prove replay-backed and current-row lookup behavior" in coverage_matrix
    assert "| XD-005 | contract-state output (`customer.客户年金计划`) influences `annual_award` and `annual_loss` plan-code enrichment behavior |" in coverage_matrix
    assert "annual_loss acceptance now proves this dependency explicitly while it remains active for both event-domain slices" in coverage_matrix

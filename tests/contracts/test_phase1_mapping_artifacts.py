import csv
from pathlib import Path


PHASE_ROOT = Path(
    ".planning/phases/01-legacy-capability-mapping-parity-harness"
)
CAPABILITY_MAP = PHASE_ROOT / "artifacts/capability-map.csv"
INTAKE_PATH_MAP = PHASE_ROOT / "artifacts/intake-path-map.csv"

REQUIRED_CAPABILITY_COLUMNS = {
    "capability_id",
    "domain",
    "business_capability",
    "legacy_behavior_meaning",
    "legacy_owner_path",
    "legacy_stage_chain",
    "pro_owner_path",
    "pro_stage_chain",
    "migration_status",
    "parity_criticality",
    "ambiguity_notes",
}

REQUIRED_INTAKE_COLUMNS = {
    "domain",
    "legacy_source_path",
    "legacy_owner_path",
    "legacy_recognition_rule",
    "pro_intake_contract",
    "validation_check",
    "test_anchor",
    "status",
    "ambiguity_notes",
}

PHASE1_DOMAINS = {"annuity_performance", "annual_award", "annual_loss"}


def _read_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        assert reader.fieldnames is not None
        return reader.fieldnames, list(reader)


def test_capability_map_required_columns() -> None:
    fieldnames, rows = _read_csv_rows(CAPABILITY_MAP)

    assert set(fieldnames) == REQUIRED_CAPABILITY_COLUMNS
    assert rows


def test_capability_map_includes_all_phase1_domains() -> None:
    _, rows = _read_csv_rows(CAPABILITY_MAP)

    assert {row["domain"] for row in rows} == PHASE1_DOMAINS


def test_annuity_performance_rows_have_stage_chains() -> None:
    _, rows = _read_csv_rows(CAPABILITY_MAP)

    annuity_rows = [row for row in rows if row["domain"] == "annuity_performance"]

    assert annuity_rows
    for row in annuity_rows:
        assert row["legacy_stage_chain"].strip()
        assert row["pro_stage_chain"].strip()


def test_intake_map_required_columns() -> None:
    fieldnames, rows = _read_csv_rows(INTAKE_PATH_MAP)

    assert set(fieldnames) == REQUIRED_INTAKE_COLUMNS
    assert rows


def test_intake_rows_have_validation_check_and_test_anchor() -> None:
    _, rows = _read_csv_rows(INTAKE_PATH_MAP)

    for row in rows:
        assert row["validation_check"].strip()
        assert row["test_anchor"].strip()

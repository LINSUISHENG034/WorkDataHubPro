import csv
from pathlib import Path


PHASE_ROOT = Path(
    ".planning/phases/01-legacy-capability-mapping-parity-harness"
)
RULE_CLASSIFICATION = PHASE_ROOT / "artifacts/rule-classification.csv"
SEVERITY_POLICY = PHASE_ROOT / "artifacts/severity-policy.md"

ALLOWED_CLASSES = {
    "must-keep",
    "replace-with-equivalent",
    "retire-with-proof",
}
ALLOWED_PHASE1_TIERS = {"block", "warn"}


def _read_rule_rows() -> list[dict[str, str]]:
    with RULE_CLASSIFICATION.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _read_policy() -> str:
    return SEVERITY_POLICY.read_text(encoding="utf-8")


def _policy_value(policy_text: str, label: str) -> str:
    prefix = f"{label}: "

    for line in policy_text.splitlines():
        if line.startswith(prefix):
            return line.removeprefix(prefix).strip()

    raise AssertionError(f"Missing policy line for {label!r}")


def test_rule_classes_are_allowed() -> None:
    rows = _read_rule_rows()

    assert rows
    assert {row["class"] for row in rows} == ALLOWED_CLASSES

    for row in rows:
        assert row["rule_id"].strip()
        assert row["domain"].strip()
        assert row["proof_or_equivalence_note"].strip()
        assert row["class"] in ALLOWED_CLASSES


def test_severity_policy_uses_only_phase1_tiers() -> None:
    policy = _read_policy()
    tiers = {
        tier.strip()
        for tier in _policy_value(policy, "Severity tiers").split(",")
        if tier.strip()
    }

    assert tiers == ALLOWED_PHASE1_TIERS


def test_unclassified_defaults_to_block() -> None:
    policy = _read_policy()

    assert _policy_value(policy, "Default rule") == "default-unclassified=block"

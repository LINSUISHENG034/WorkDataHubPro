from __future__ import annotations

from dataclasses import asdict
from dataclasses import dataclass

STATUSES = (
    "seeded",
    "active",
    "candidate",
    "deferred",
    "archived",
)
CLAIM_TYPES = (
    "direct_observation",
    "inferred_from_sources",
    "compiled_summary",
    "open_question",
)
SOURCE_TYPES = (
    "legacy_doc",
    "legacy_config",
    "legacy_test",
    "legacy_code",
    "current_spec",
    "current_audit",
    "current_wiki",
    "current_reference_asset",
)
EVIDENCE_STRENGTHS = (
    "strong",
    "supporting",
    "weak",
)
CONFIDENCE_LEVELS = (
    "high",
    "medium",
    "low",
)
COVERAGE_STATES = (
    "seeded",
    "mapped",
    "partial",
    "closed",
    "deferred",
)
TRIAGE_STATUSES = (
    "new",
    "accepted",
    "rejected",
    "deferred",
    "merged",
)
WAVE_ID_PATTERN = r"wave-\d{4}-\d{2}-\d{2}-[a-z0-9]+(?:-[a-z0-9]+)*"


@dataclass(frozen=True)
class SeededEntrySurface:
    entry_family: str
    surface_id: str
    title: str
    status: str = "seeded"
    coverage_state: str = "seeded"


@dataclass(frozen=True)
class SeededSourceFamily:
    family_id: str
    title: str
    status: str = "seeded"
    coverage_state: str = "seeded"


@dataclass(frozen=True)
class SeededWave:
    wave_id: str
    title: str
    status: str
    opened_at: str
    seeded_entry_surfaces: tuple[str, ...]
    seeded_high_priority_source_families: tuple[str, ...]
    admitted_subsystems: tuple[str, ...] = ()
    closed_at: str | None = None


CANONICAL_SEED_SOURCES = (
    "execution/entry-surfaces.yaml",
    "sources/families.yaml",
    "waves/index.yaml",
)

SEEDED_ENTRY_SURFACES = (
    SeededEntrySurface(
        entry_family="manual_cli_entrypoints",
        surface_id="annuity_performance",
        title="Annuity performance replay and operator entrypoints",
    ),
    SeededEntrySurface(
        entry_family="manual_cli_entrypoints",
        surface_id="annual_award",
        title="Annual award replay and operator entrypoints",
    ),
    SeededEntrySurface(
        entry_family="manual_cli_entrypoints",
        surface_id="annual_loss",
        title="Annual loss replay and operator entrypoints",
    ),
    SeededEntrySurface(
        entry_family="manual_cli_entrypoints",
        surface_id="annuity_income",
        title="Annuity income replay and operator entrypoints",
    ),
    SeededEntrySurface(
        entry_family="manual_cli_entrypoints",
        surface_id="customer_mdm",
        title="Manual customer MDM command surfaces",
    ),
    SeededEntrySurface(
        entry_family="scheduled_orchestrated_entrypoints",
        surface_id="company_lookup_queue",
        title="Deferred company lookup queue orchestration surface",
    ),
    SeededEntrySurface(
        entry_family="scheduled_orchestrated_entrypoints",
        surface_id="reference_sync",
        title="Reference sync orchestration surface",
    ),
)

SEEDED_HIGH_PRIORITY_SOURCE_FAMILIES = (
    SeededSourceFamily(
        family_id="legacy-domain-capability-maps",
        title="Legacy domain capability maps and migration workflow guides",
    ),
    SeededSourceFamily(
        family_id="legacy-operator-runtime-surfaces",
        title="Legacy operator CLI, schedules, sensors, and runtime entry surfaces",
    ),
    SeededSourceFamily(
        family_id="legacy-identity-and-reference-runtime",
        title="Legacy identity, queue, reference, and persistence runtime surfaces",
    ),
    SeededSourceFamily(
        family_id="current-first-wave-governance-specs",
        title="Current first-wave governance specs and coverage matrix inputs",
    ),
    SeededSourceFamily(
        family_id="current-wiki-bi-surfaces",
        title="Current wiki-bi durable surfaces and semantic governance pages",
    ),
    SeededSourceFamily(
        family_id="current-replay-and-reference-assets",
        title="Current replay assets, reference artifacts, and validation runbooks",
    ),
)

BOOTSTRAP_WAVE = SeededWave(
    wave_id="wave-2026-04-16-registry-bootstrap",
    title="Registry bootstrap",
    status="active",
    opened_at="2026-04-16",
    seeded_entry_surfaces=tuple(item.surface_id for item in SEEDED_ENTRY_SURFACES),
    seeded_high_priority_source_families=tuple(
        item.family_id for item in SEEDED_HIGH_PRIORITY_SOURCE_FAMILIES
    ),
)


def seeded_entry_surfaces_payload() -> dict[str, list[dict[str, str]]]:
    return {
        "seeded_entry_surfaces": [asdict(item) for item in SEEDED_ENTRY_SURFACES],
    }


def seeded_source_families_payload() -> dict[str, list[dict[str, str]]]:
    return {
        "seeded_high_priority_source_families": [
            asdict(item) for item in SEEDED_HIGH_PRIORITY_SOURCE_FAMILIES
        ],
    }


def bootstrap_wave_payload() -> dict[str, object]:
    return {
        "active_wave_id": BOOTSTRAP_WAVE.wave_id,
        "waves": [
            {
                **asdict(BOOTSTRAP_WAVE),
                "seeded_entry_surfaces": list(BOOTSTRAP_WAVE.seeded_entry_surfaces),
                "seeded_high_priority_source_families": list(
                    BOOTSTRAP_WAVE.seeded_high_priority_source_families
                ),
                "admitted_subsystems": list(BOOTSTRAP_WAVE.admitted_subsystems),
            }
        ],
    }

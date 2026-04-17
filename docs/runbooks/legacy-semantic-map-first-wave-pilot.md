# Legacy Semantic Map First-Wave Pilot

## Purpose

Run the Slice 4 first-wave pilot from checked-in evidence, then review the
generated semantic-map artifacts without promoting them into durable wiki
content.

## Scope

- pilot wave: `wave-2026-04-17-first-wave-pilot`
- Tier A deep coverage:
  - `annuity_performance`
  - `annual_award`
  - `annual_loss`
  - `annuity_income`
- Tier B representative coverage:
  - `customer_mdm`
  - `company_lookup_queue`
  - `reference_sync`

## Commands

Compile the accepted checked-in pilot claims and generate reports:

```bash
uv run python -m scripts.legacy_semantic_map.pilot --registry-root docs/wiki-bi/_meta/legacy-semantic-map
```

Targeted validation:

```bash
uv run pytest tests/contracts/test_legacy_semantic_map_first_wave_pilot.py -v
uv run pytest tests/integration/test_legacy_semantic_map_first_wave_pilot_flow.py -v
uv run pytest tests/contracts/test_legacy_semantic_map_*.py tests/integration/test_legacy_semantic_map_reporting_pipeline.py tests/integration/test_legacy_semantic_map_first_wave_pilot_flow.py -v
```

## Expected Outputs

After a successful run from the accepted claim set:

- `docs/wiki-bi/_meta/legacy-semantic-map/waves/index.yaml`
  - bootstrap wave is closed
  - `wave-2026-04-17-first-wave-pilot` is active
  - pilot depth tiers point to Tier A and Tier B surfaces
- `docs/wiki-bi/_meta/legacy-semantic-map/claims/wave-2026-04-17-first-wave-pilot/`
  - 7 execution claims
  - 7 object claims
  - 4 subsystem claims
  - every admitted surface has at least one checked-in `legacy_doc` or `legacy_code`
    source reference plus current governance/reference context
- `docs/wiki-bi/_meta/legacy-semantic-map/manifest.json`
  - `generated_canonical_files` is populated
  - `compiled_claim_ids` is populated
  - `compiled_claims_by_wave.wave-2026-04-17-first-wave-pilot` is populated
- `docs/wiki-bi/_meta/legacy-semantic-map/reports/current/coverage-status.json`
  - `wave_status = "green"`
  - `entrypoint_coverage_pct = 100.0`
  - `high_priority_source_family_coverage_pct = 100.0`
  - `orphan_high_priority_source_count = 0`
  - `stale_high_priority_candidate_count = 0`
- `docs/wiki-bi/_meta/legacy-semantic-map/reports/current/integrity-status.json`
  - `closeout_ready = false`
  - blockers stay limited to:
    - `durable_wiki_targets_not_accepted`
    - `findings_disposition_incomplete`

## Interpretation

What the pilot proves:

- the semantic-map model can compile real checked-in claims into execution,
  subsystem, object, edge, and candidate outputs
- the current reporting pipeline can classify the admitted pilot denominator as
  mechanically green without claiming durable wiki closure
- Tier A surfaces support deeper subsystem/object mapping while Tier B surfaces
  remain representative-only and candidate-heavy

What the pilot does not prove:

- durable wiki placement is settled
- operator/runtime-adjacent surfaces are fully closed
- the semantic map is ready to replace later absorption work

## Follow-On Questions

- whether the next wave should deepen one Tier B runtime surface or begin an
  absorption-adjacent pass
- whether any representative candidate should be promoted into a stable
  subsystem/object in a later wave
- whether the admitted denominator should stay at seven surfaces or split into
  separate fact-domain and operator/runtime waves

# Legacy Semantic Map First-Wave Pilot

## Purpose

Run the Slice 4 first-wave pilot from checked-in evidence, then review the
generated semantic-map artifacts. On the current integration branch, the pilot
and its Phase B closeout are already accepted; use this runbook to reproduce
the checked-in state before merge review, not to reopen pilot scope.

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

The default front door now targets `wave-2026-04-17-semantic-governance-reframe`.

Compile the active successor wave and generate reports:

```bash
uv run python -m scripts.legacy_semantic_map.pilot --registry-root docs/wiki-bi/_meta/legacy-semantic-map
```

Re-run the historical first-wave pilot explicitly:

```bash
uv run python -m scripts.legacy_semantic_map.pilot --registry-root docs/wiki-bi/_meta/legacy-semantic-map --wave-id wave-2026-04-17-first-wave-pilot
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
  - `wave-2026-04-17-first-wave-pilot` is closed
  - `closed_at = '2026-04-17'`
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
  - `wave_id = "wave-2026-04-17-semantic-governance-reframe"`
  - `wave_status = "green"`
  - `semantic_question_coverage_pct = 100.0`
- `docs/wiki-bi/_meta/legacy-semantic-map/reports/current/integrity-status.json`
  - `closeout_ready = false`
  - `archive_ready = false`
  - `blocking_reasons = ["durable_wiki_targets_not_accepted", "findings_disposition_incomplete"]`

When running the explicit historical first-wave command above, expect the
command to fail unless the target wave is reopened; closed waves remain audit
read-only under CT-018.

## Interpretation

What the pilot proves:

- the semantic-map model can compile real checked-in claims into execution,
  subsystem, object, edge, and candidate outputs
- the current reporting pipeline can classify the admitted pilot denominator as
  mechanically green through formal closeout and archive readiness
- Tier A surfaces support deeper subsystem/object mapping while Tier B surfaces
  remain representative-only and candidate-heavy

What the pilot still does not prove:

- that every future semantic-map wave should follow the same denominator or
  depth split
- that operator/runtime-adjacent surfaces need no further semantic analysis in
  later waves
- that the semantic map should replace durable wiki maintenance as the long-term
  answer surface

## Next Stage

- primary branch decision: treat the semantic-map package as merge-ready for
  `main` review
- if review requires more semantic-map work before merge, open one new bounded
  slice from `slice/semantic-map-integration` instead of reopening broad pilot
  discovery
- see `docs/runbooks/legacy-semantic-map-first-wave-closeout.md` for the
  accepted closeout summary

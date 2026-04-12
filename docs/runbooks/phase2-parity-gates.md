# Phase 2 Parity Gates

## Goal

Provide explicit, repository-native gate tiers for the completed Phase 2 parity
surface without binding the project to a specific CI provider.

## Runner

Use:

```bash
uv run python scripts/run_phase2_parity_gates.py --tier <tier>
```

Supported tiers:

- `pr`
- `protected_branch`
- `nightly`

## PR Gate

Blocks pull requests on the fast annuity-focused Phase 2 protection set.

Command:

```bash
uv run pytest tests/integration/test_phase2_intake_validation.py tests/replay/test_annuity_performance_slice.py tests/replay/test_phase2_annuity_performance_gates.py tests/replay/test_annuity_performance_explainability_slo.py -v
```

What it protects:

- intake tolerance and minimum-skeleton failures
- annuity-performance replay parity
- failed-gate package behavior
- explainability retrieval latency and trace evidence

## Protected Branch Gate

Blocks merge candidates on the accepted-slice replay matrix plus explicit
`reference_derivation` checkpoint coverage.

Command:

```bash
uv run pytest tests/replay/test_annuity_performance_slice.py tests/replay/test_annual_award_slice.py tests/replay/test_annual_loss_slice.py tests/replay/test_phase2_reference_derivation_gates.py -v
```

What it protects:

- annuity, award, and loss replay parity
- cross-slice checkpoint taxonomy consistency
- explicit `reference_derivation` checkpoint coverage

## Nightly Gate

Runs the full repository suite for nightly or release-level verification.

Command:

```bash
uv run pytest -v
```

What it protects:

- the entire repository test surface
- regressions outside the narrower Phase 2 targeted gates

## Usage Notes

- The runner is fail-fast by design; it stops on the first failing command.
- Keep the manifest in `config/verification/phase2-parity-gates.json` as the machine-readable source of truth.
- Update this runbook when any command or blocking intent changes.

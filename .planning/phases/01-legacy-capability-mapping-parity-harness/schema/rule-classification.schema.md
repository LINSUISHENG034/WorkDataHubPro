# Rule Classification Schema

## Purpose

`rule-classification.csv` is the authoritative Phase 1 inventory for MAP-03.
Each row records one parity-critical legacy rule, the WorkDataHubPro owner path
that now carries or replaces that behavior, the approved migration class, and
the rationale needed for auditability.

This artifact works with
`.planning/phases/01-legacy-capability-mapping-parity-harness/artifacts/severity-policy.md`.
Phase 1 severity references are limited to `block` and `warn`, and
`default-unclassified=block` is mandatory for any mismatch category not yet
classified in the policy.

## CSV Contract

Required header order:

```text
rule_id,domain,legacy_rule_meaning,legacy_path,pro_owner_path,class,proof_or_equivalence_note,parity_criticality
```

## Column Rules

| Column | Required | Rule |
|------|------|------|
| `rule_id` | yes | Stable identifier. Unique within the file. |
| `domain` | yes | Phase 1 domain scope: `annuity_performance`, `annual_award`, or `annual_loss`. |
| `legacy_rule_meaning` | yes | Human-readable description of the legacy behavior that matters for parity decisions. |
| `legacy_path` | yes | Concrete legacy code, config, or doc path that anchors the rule meaning. |
| `pro_owner_path` | yes | Canonical WorkDataHubPro owner path that keeps, replaces, or governs the behavior. |
| `class` | yes | Allowed values: `must-keep`, `replace-with-equivalent`, `retire-with-proof`. |
| `proof_or_equivalence_note` | yes | Non-empty rationale. For `must-keep`, explain why parity requires retention. For `replace-with-equivalent`, identify the equivalence claim. For `retire-with-proof`, name the proof or replacement rationale. |
| `parity_criticality` | yes | Allowed values: `critical`, `supporting`, `breadth`. |

## Classification Rules

- `must-keep`: legacy behavior is parity-critical and must remain materially
  present in WorkDataHubPro.
- `replace-with-equivalent`: legacy behavior may move to a different explicit
  implementation as long as semantic equivalence is stated and reviewable.
- `retire-with-proof`: legacy behavior may only be removed when replacement or
  removal proof is written down explicitly.

Unknown class values are invalid. Empty `proof_or_equivalence_note` values are
invalid. Unknown domains are invalid.

## Severity Policy References

- Phase 1 severity tiers are only `block` and `warn`.
- `block` covers semantic output drift, publication-key drift, source
  recognition routing drift, non-adjudicable mismatches, and missing evidence.
- `warn` is reserved for explainable bounded differences that preserve final
  business semantics.
- `default-unclassified=block` applies to every unclassified or newly observed
  mismatch category.
- Reviewers must treat a missing rule row as `block` until the rule is added
  and classified explicitly.

## Auditability Rules

- Every row must preserve attributable lineage from `legacy_path` to
  `pro_owner_path`.
- `rule_id` and `domain` together define the review key used by Phase 1
  adjudication artifacts.
- Breadth rows are allowed for `annual_award` and `annual_loss`, but they still
  require a concrete `class` and `proof_or_equivalence_note`.

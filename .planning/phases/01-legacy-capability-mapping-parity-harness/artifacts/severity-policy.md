# Phase 1 Severity Policy

## Purpose

This document defines how Phase 1 parity mismatches are interpreted while
reviewing the legacy-to-pro mapping artifacts and early replay evidence for
MAP-03.

Phase 1 uses an offline report gate with human confirmation. It does not
introduce a CI hard-fail parity gate in this plan.

## Machine-Readable Summary

Severity tiers: block, warn
Default rule: default-unclassified=block

## Allowed Severity Tiers

Only two severity tiers are valid in Phase 1:

- `block`
- `warn`

No other tier names are allowed in Phase 1 artifacts or review notes.

## Default Rule

`default-unclassified=block`

Any mismatch category that is new, ambiguous, or not explicitly listed below
must be treated as `block` until a later approved artifact updates this policy.
Unknown mismatch categories are not silently accepted.

## Block Conditions

Use `block` when the mismatch changes business semantics, prevents trustworthy
adjudication, or removes required evidence.

`block` includes:

- semantic output drift
- publication-key drift or missing key-field stability
- source recognition routing drift
- non-adjudicable mismatches
- missing evidence, missing rule classification, or missing rationale

When a `block` mismatch is observed, reviewers should escalate it into the
Phase 1 mismatch report and, when replay evidence exists, a compatibility case.

## Warn Conditions

Use `warn` only for explainable bounded differences that preserve final
business semantics and keep the evidence chain attributable.

`warn` includes:

- representation-only differences that do not change the accepted business
  interpretation
- bounded structural differences already explained by explicit equivalence notes
- review noise that still preserves source recognition, canonical fact meaning,
  and publication payload intent

If a reviewer cannot explain why the difference is non-semantic, it is not a
`warn`; it falls back to `block`.

## Decision Discipline

- `rule-classification.csv` decides whether a legacy rule must be kept,
  replaced-with-equivalent, or retired-with-proof.
- This policy decides whether an observed mismatch is `block` or `warn`.
- A `retire-with-proof` classification does not downgrade an unclassified
  mismatch. The mismatch still defaults to `block`.

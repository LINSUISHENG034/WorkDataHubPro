---
name: wdhp-semantic-map-ingress
description: Use only when the user explicitly invokes `wdhp-semantic-map-ingress` or directly asks for semantic-ingress work that writes proposal-grade ingress records for `docs/wiki-bi/_meta/legacy-semantic-map/ingress/`. Do not auto-activate from repository context alone.
---

# WDHP Semantic Map Ingress

## Overview

Use this skill only for explicit semantic-ingress work inside `E:\Projects\WorkDataHubPro`.

The skill writes bounded ingress records under `docs/wiki-bi/_meta/legacy-semantic-map/ingress/` and may auto-promote structurally ready findings into `claims/<wave_id>/semantic/`.

It must not write `docs/wiki-bi/` durable pages.

## Required Inputs

- one or more tightly related semantic questions
- optional `wave_id`
- legacy evidence rooted in `E:\Projects\WorkDataHub`

## Workflow

1. Resolve the active or explicitly requested open wave.
2. Call `scripts/legacy_semantic_map/semantic_ingress_guard.py` before writing.
3. Read only legacy evidence from `E:\Projects\WorkDataHub`.
4. Choose whether the ingress unit is a `question_cluster` or a `finding`.
5. Write the ingress record and update the ingress index for that wave.
6. call the ingress guard helper again for promotion evaluation.
7. If promotion is structurally ready, promote into `claims/<wave_id>/semantic/`.
8. stop and ask the user before modifying an existing semantic claim or canonical semantic file.

## Boundary Rules

- business-semantic evidence must come from `E:\Projects\WorkDataHub`
- current repo materials may be read only for routing, duplicate detection, or durable target awareness
- current repo materials must not be cited as business-semantic evidence for ingress
- use the repo-root guard helper plus the three reference docs in this skill package
- do not treat this skill as a durable wiki-maintenance or governance workflow
- do not perform canonical compilation or durable wiki promotion from this skill

## Required References

- `references/ingress-template.md`
- `references/promotion-gates.md`
- `references/claim-minimum-fields.md`
- `scripts/semantic_ingress_guard.py`

## Notes

- The repo-local wrapper at `scripts/semantic_ingress_guard.py` forwards to `scripts/legacy_semantic_map/semantic_ingress_guard.py`.
- Use conservative promotion. When structural overlap or modification risk appears, stop instead of silently editing formal semantic artifacts.

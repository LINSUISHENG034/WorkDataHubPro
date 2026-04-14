# WorkDataHubPro System Docs

## Purpose

`docs/system/` is the framework-neutral top-level design layer for `WorkDataHubPro`.

It exists to define:

- the product-level architecture that all development frameworks must respect
- the source-of-truth hierarchy between system docs, wiki knowledge, framework docs, and runtime evidence
- the stable constraints that should not move when planning frameworks or workflow tooling change

## Documents

- [Framework-Neutral Foundation](./framework-neutral-foundation.md)
  - Product-level design goals, invariant boundaries, logical architecture, and acceptance axes.
- [Document Authority Model](./document-authority-model.md)
  - Which document layer answers which kind of question, and how to resolve conflicts between system docs, wiki, framework docs, and code.

## Reading Order

For strong guidance, read in this order:

1. `docs/system/`
2. `docs/wiki-bi/`
3. framework-specific docs such as `docs/superpowers/` or `.planning/`
4. current code, tests, config, replay assets, and runbooks

## Non-Goals

`docs/system/` does not replace:

- `docs/wiki-bi/` as the business-semantic and evidence layer
- framework-specific planning/execution documents
- current code and tests as the source of truth for what is actually implemented

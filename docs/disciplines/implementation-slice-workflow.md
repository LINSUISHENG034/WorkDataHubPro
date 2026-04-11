# Implementation Slice Workflow Discipline

## Read This When

- starting a new implementation slice
- deciding execution order across capabilities, platform, governance, and apps
- determining whether work belongs in one slice or should be split
- deciding how plans, runbooks, and replay artifacts should be tracked

## Do Not Read This When

- the task is purely about toolchain commands or environment setup
- the task is only about final verification or completion claims

## Hard Gates

- do not start implementation directly on `main`
- prefer one explicit validation slice over partially building multiple independent subsystems
- do not continue from a local-only plan that can block checkout, merge, or review flow later

## 1. Preferred Slice Execution Order

For executable validation slices, prefer this order unless an approved plan says
otherwise:

1. bootstrap the workspace and toolchain
2. define runtime contracts
3. define trace and lineage runtime
4. implement source intake
5. implement fact processing and governed cleansing
6. implement identity resolution
7. implement reference derivation
8. implement publication and storage
9. implement projections
10. implement governance evidence and adjudication
11. wire replay orchestration
12. check in replay assets, runbooks, and explainability validation

This order reduces hidden coupling. If a later stage reveals a missing upstream
contract, fix the contract deliberately instead of patching around it downstream.

## 2. Documentation Tracking Rule

Execution-critical documents must be intentionally tracked.

- specs belong in `docs/superpowers/specs/`
- implementation plans belong in `docs/superpowers/plans/`
- runbooks belong in `docs/runbooks/`
- durable workflow rules belong in `docs/disciplines/`

Do not leave active plans or runbooks as untracked local files once execution is
underway.

## 3. Scope Rule

- use a short-lived boundary branch for single-boundary work
- use an explicit slice branch only when the work intentionally crosses boundaries
- if a change cannot be explained as one boundary or one slice, split it before implementation

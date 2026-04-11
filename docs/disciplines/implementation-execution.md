# Implementation Execution Discipline

## Read This When

- starting or resuming implementation work
- executing an approved plan
- changing code, configuration, or validation workflow for a slice
- deciding which deeper implementation discipline to load next

## Do Not Read This When

- the task is only about branch, merge, PR, or worktree decisions
- the task is only about Serena activation or symbol-aware exploration
- the task is docs-only and does not affect implementation workflow

## Hard Gates

- do not continue implementation after a toolchain or execution-assumption change until the governing plan is updated
- do not execute large implementation work from local-only documents that are not intentionally tracked
- do not bulk-read all implementation discipline files; load only the child document that matches the next action

## 1. Purpose

This document is the entry point for implementation workflow in
`WorkDataHubPro`.

It exists to keep `AGENTS.md` short while still giving agents a predictable way
to load only the implementation rules they need for the current action.

## 2. Load Order

Read this file first for implementation work. Then read only the next matching
discipline document.

- toolchain, dependencies, `uv`, lockfiles, command style, environment noise:
  `docs/disciplines/implementation-toolchain.md`
- slice ordering, contract-first rollout, document tracking, execution scope:
  `docs/disciplines/implementation-slice-workflow.md`
- completion claims, validation evidence, full-suite verification:
  `docs/disciplines/implementation-verification.md`

For git mechanics such as branching, merging, PRs, and worktree cleanup, switch
to `docs/disciplines/git-workflow.md` instead of extending implementation rules.

## 3. Core Rules

- Prefer one end-to-end validation slice over partially advancing multiple unrelated subsystems.
- Establish shared contracts and runtime boundaries before layering downstream behavior on top of them.
- Keep business semantics inside `capabilities/`, not in CLI code, replay wiring, publication helpers, or governance code.
- Keep `AGENTS.md` as a router and summary. Put durable detailed rules in `docs/disciplines/`.

## 4. Anti-Patterns

Avoid these behaviors:

- changing the package manager or test command style mid-execution without updating the plan first
- reading every discipline doc just because implementation is happening somewhere
- treating the implementation plan as disposable local scratch state
- using downstream orchestration code to patch around missing upstream contracts

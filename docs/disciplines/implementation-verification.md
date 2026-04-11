# Implementation Verification Discipline

## Read This When

- claiming a task, slice, or merge candidate is complete
- deciding what validation evidence is required
- preparing to merge after implementation work

## Do Not Read This When

- the task is still in early implementation and no completion claim is being made
- the task is only about git branch mechanics

## Hard Gates

- do not claim completion from task-level intuition or partial evidence
- run the full relevant verification command before declaring a slice complete
- for merge mechanics and branch cleanup, pair this document with `docs/disciplines/git-workflow.md`

## 1. Verification Rules

- run the narrowest relevant test while developing each task
- run the full relevant slice acceptance path before claiming a slice is closed
- before merge or completion, run the full test suite from the current branch or merge candidate
- state validation using the actual command that was run
- if verification depends on replay assets or accepted baselines, include those artifacts in the validation story

## 2. Minimum Completion Evidence

Before saying implementation is complete, confirm:

- the relevant targeted tests passed during development
- the full suite passed on the current branch or merge result
- replay assets and runbooks are present when they are part of the slice contract
- documentation changes do not contradict the active blueprint or discipline docs

## 3. Anti-Patterns

Avoid these behaviors:

- relying on accumulated partial passes as the only completion evidence
- skipping the final full-suite run because earlier targeted runs were green
- merging from a dirty context because the code itself already passed somewhere else
